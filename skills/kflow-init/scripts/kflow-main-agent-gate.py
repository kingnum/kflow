#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KFlow 主 Agent 执行门控（PreToolUse hook）。

判定规则
--------
1. 阶段来源：变更级 `.status.md` 的「当前阶段」字段。无法判定（无活跃变更、文件缺失、
   字段不可解析、存在多个活跃变更）时**放行**——门控的目的是降低上下文消耗，不是安全边界。
2. 执行类阶段（plan / code / code-review / api-test / e2e-test / integration-test / bug-fix）：
   - 主 Agent 的 `Edit` / `Write`：目标路径不在白名单内时拒绝
   - 主 Agent 的 `Bash`：命令匹配长输出构建/测试模式时拒绝
   - 设计类阶段（explore / prototype-design / design）与其他阶段：放行
3. 子代理放行。子代理识别按以下优先级：
   a. stdin 中的 `agent_id` / `agent_type` 字段。实测 Claude Code 2.1.278：子代理的
      PreToolUse 输入含该两字段，主 Agent 不含。二者均为未文档化字段，升级后可能变化。
   b. `transcript_path` 启发式：实测主 Agent 与子代理的 transcript 均为会话级 `.jsonl`，
      路径中不含 `/subagents/` 标识，故本版本不构成有效判据；保留为未来版本的可能降级。
   c. 以上均不可判定时按主 Agent 处理（保证门控生效）。若上游移除 agent 字段，子代理会被
      误判为主 Agent；此时可设置 `KFLOW_GATING_DISABLE=1` 临时关闭门控。
4. 任何异常均放行（fail-open），并记录到 `.claude/kflow-gating.log`。

输出格式（官方约定）
--------------------
拒绝：stdout 输出
    {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": "..."}}
放行：不输出（退出码 0），以免覆盖用户的权限提示。

依赖与风险
----------
`agent_id` / `agent_type` 未在官方 hook 输入文档中列出，属未文档化行为。若上游版本移除该
字段，脚本降级到 transcript_path 启发式；若两者均失效，门控会把子代理也视为主 Agent——此时
子代理的写入会被拒绝。此时可通过环境变量 `KFLOW_GATING_DISABLE=1` 临时关闭门控。
"""
from __future__ import unicode_literals

import io
import json
import os
import re
import sys
import time

# 执行类阶段（主 Agent 仅调度与验收）
EXECUTION_PHASES = {
    'plan', 'code', 'code-review', 'api-test', 'e2e-test', 'integration-test', 'bug-fix',
}

# 白名单：主 Agent 在执行类阶段仍可写入的路径
#   .status.md / status-log.md —— 状态双写
#   docs/skill-suggestion.md —— skill 改进建议
#   docs/doc-optimize-*.md —— 独立维护工具 kflow-doc-optimize 的报告（非阶段主工作）
WHITELIST_SUFFIXES = (
    '.status.md',
    '/status-log.md',
    '\\status-log.md',
    'status-log.md',
)
WHITELIST_EXACT = (
    'docs/skill-suggestion.md',
    'docs/doc-optimize-report.md',
    'docs/doc-optimize-references.md',
)

# 长输出构建/测试命令模式（在执行类阶段由主 Agent 直接执行时拒绝）
LONG_OUTPUT_PATTERNS = [
    re.compile(r'(^|[;&|]\s*)pytest\b'),
    re.compile(r'(^|[;&|]\s*)python3?\s+-m\s+pytest\b'),
    re.compile(r'(^|[;&|]\s*)npx\s+tsc\b'),
    re.compile(r'(^|[;&|]\s*)tsc\b'),
    re.compile(r'(^|[;&|]\s*)npx\s+eslint\b'),
    re.compile(r'(^|[;&|]\s*)eslint\b'),
    re.compile(r'(^|[;&|]\s*)vite\s+build\b'),
    re.compile(r'(^|[;&|]\s*)npm\s+run\s+(test|build)\b'),
    re.compile(r'(^|[;&|]\s*)yarn\b'),
    re.compile(r'(^|[;&|]\s*)pnpm\b'),
]

PHASE_ALIASES = {
    'explore': 'explore',
    '设计探索': 'explore',
    'prototype-design': 'prototype-design',
    '原型设计': 'prototype-design',
    'design': 'design',
    '详细设计': 'design',
    'plan': 'plan',
    '计划': 'plan',
    'code': 'code',
    '编码': 'code',
    'code-review': 'code-review',
    '代码审查': 'code-review',
    'api-test': 'api-test',
    '接口单元测试': 'api-test',
    'e2e-test': 'e2e-test',
    'e2e测试': 'e2e-test',
    'integration-test': 'integration-test',
    '集成测试': 'integration-test',
    'audit': 'audit',
    '审计': 'audit',
    'archive': 'archive',
    '归档': 'archive',
    'bug-fix': 'bug-fix',
    '缺陷修复': 'bug-fix',
}

REASON_EDIT = (
    '主 Agent 在执行类阶段（当前阶段：{phase}）仅承担调度与验收，不得直接编写生产代码、'
    '测试代码或阶段产物。请创建子代理执行该工作：Edit/Write 应在子代理上下文中完成。'
    '若为状态或建议记录，请写入 .status.md、status-log.md 或 docs/skill-suggestion.md。'
)
REASON_BASH = (
    '主 Agent 在执行类阶段（当前阶段：{phase}）不得直接运行长输出构建/测试命令（{cmd}）。'
    '该类命令的输出会在后续每一轮被重读，显著放大上下文消耗。请创建子代理执行并仅接收摘要。'
)


def log(project_root, message):
    try:
        log_dir = os.path.join(project_root, '.claude')
        if not os.path.isdir(log_dir):
            return
        with io.open(os.path.join(log_dir, 'kflow-gating.log'), 'a', encoding='utf-8') as f:
            f.write('%s\t%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), message))
    except Exception:
        pass


def find_active_status(project_root):
    """返回唯一的活跃变更 `.status.md` 路径；无法唯一确定时返回 None。"""
    changes_dir = os.path.join(project_root, 'docs', 'changes')
    if not os.path.isdir(changes_dir):
        return None
    candidates = []
    try:
        for name in os.listdir(changes_dir):
            if name == 'archive':
                continue
            path = os.path.join(changes_dir, name, '.status.md')
            if os.path.isfile(path):
                candidates.append(path)
    except Exception:
        return None
    if len(candidates) != 1:
        return None
    return candidates[0]


def read_phase(status_path):
    """从 `.status.md` 读取「当前阶段」字段并归一为阶段键；不可解析时返回 None。"""
    try:
        with io.open(status_path, encoding='utf-8', errors='replace') as f:
            text = f.read()
    except Exception:
        return None
    m = re.search(r'\*\*当前阶段\*\*\s*[:：]\s*([^\n|]+)', text)
    if not m:
        return None
    raw = m.group(1).strip().strip('*` ')
    # 去掉括号注释，如「编码（子变更级）」
    raw = re.sub(r'[（(].*?[)）]', '', raw).strip()
    return PHASE_ALIASES.get(raw) or PHASE_ALIASES.get(raw.lower())


def is_subagent(payload):
    if payload.get('agent_id') or payload.get('agent_type'):
        return True
    # 仅保留 `/subagents/` 目录标识作为未来版本的保守降级；实测 2.1.278 的 transcript
    # 为会话级路径，不命中该标识。不使用宽泛的 `/agent-` 匹配，避免项目名误判。
    tp = (payload.get('transcript_path') or '').replace('\\', '/')
    if '/subagents/' in tp:
        return True
    return False


def is_whitelisted(path):
    if not path:
        return False
    p = path.replace('\\', '/')
    for exact in WHITELIST_EXACT:
        if p == exact or p.endswith('/' + exact):
            return True
    base = os.path.basename(p)
    if base == 'status-log.md':
        return True
    if base == '.status.md':
        return True
    return False


def is_long_output_command(command):
    if not command:
        return False
    for pat in LONG_OUTPUT_PATTERNS:
        if pat.search(command):
            return True
    return False


def deny(project_root, phase, reason):
    log(project_root, 'DENY\tphase=%s\t%s' % (phase, reason.replace('\n', ' ')))
    out = {
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': reason,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    sys.stdout.flush()
    return 0


def main():
    project_root = os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    if os.environ.get('KFLOW_GATING_DISABLE') == '1':
        return 0

    project_root = payload.get('cwd') or project_root
    tool_name = payload.get('tool_name') or ''
    tool_input = payload.get('tool_input') or {}

    # 子代理不受门控约束
    if is_subagent(payload):
        return 0

    status_path = find_active_status(project_root)
    if not status_path:
        return 0
    phase = read_phase(status_path)
    if not phase or phase not in EXECUTION_PHASES:
        return 0

    if tool_name in ('Edit', 'Write', 'MultiEdit'):
        path = tool_input.get('file_path') or tool_input.get('path') or ''
        if is_whitelisted(path):
            return 0
        return deny(project_root, phase, REASON_EDIT.format(phase=phase))

    if tool_name == 'Bash':
        command = tool_input.get('command') or ''
        if is_long_output_command(command):
            short = command.strip().split('\n')[0][:80]
            return deny(project_root, phase, REASON_BASH.format(phase=phase, cmd=short))
        return 0

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        # fail-open：门控异常不得阻塞正常流程
        sys.exit(0)
