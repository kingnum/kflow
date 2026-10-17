# -*- coding: utf-8 -*-
"""kflow-init / 上下文与门控配置校验。

用法:
    python verify_project_config.py [--root <项目根>] [--json]

校验项:
    1. .claude/settings.json 存在且可解析
    2. 顶层 autoCompactWindow 存在且 <= 300000（更小的值视为更强节流，同样通过）
    3. .claude/hooks/kflow-main-agent-gate.py 存在
    4. hooks.PreToolUse 中存在指向门控脚本的注册条目，且 matcher 覆盖 Edit/Write/Bash
    5. permissions.allow 含全局必需权限（缺项仅告警，不判失败）

退出码:
    0  全部必需项通过
    1  存在缺失或不合规项
    2  参数或文件错误
"""
from __future__ import unicode_literals

import argparse
import io
import json
import os
import sys

AUTO_COMPACT_MAX = 300000
GATE_SCRIPT_REL = '.claude/hooks/kflow-main-agent-gate.py'
REQUIRED_MATCHERS = {'Edit', 'Write', 'Bash'}
REQUIRED_PERMISSIONS = [
    'Bash(npm *)', 'Bash(yarn *)', 'Bash(pnpm *)', 'Bash(npx *)', 'Bash(node *)',
    'Bash(git *)', 'Bash(curl *)', 'Bash(python *)', 'Bash(python3 *)',
    'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Agent', 'WebFetch',
]


def load_json(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def check(root):
    results = []

    def add(name, ok, detail, required=True):
        results.append({'check': name, 'ok': ok, 'detail': detail, 'required': required})

    settings_path = os.path.join(root, '.claude', 'settings.json')
    settings = None
    if not os.path.isfile(settings_path):
        add('settings.json', False, '不存在: %s' % settings_path)
    else:
        try:
            settings = load_json(settings_path)
            add('settings.json', True, '可解析')
        except Exception as e:
            add('settings.json', False, '解析失败: %s' % e)

    if settings is not None:
        val = settings.get('autoCompactWindow')
        if val is None:
            add('autoCompactWindow', False, '缺失')
        elif not isinstance(val, int):
            add('autoCompactWindow', False, '取值类型非法: %r' % (val,))
        elif val <= AUTO_COMPACT_MAX:
            add('autoCompactWindow', True, '%d <= %d' % (val, AUTO_COMPACT_MAX))
        else:
            add('autoCompactWindow', False, '%d > %d（阈值过高）' % (val, AUTO_COMPACT_MAX))

        allow = (settings.get('permissions') or {}).get('allow') or []
        missing = [p for p in REQUIRED_PERMISSIONS if p not in allow]
        add('permissions.allow', not missing,
            '齐全' if not missing else '缺少 %d 项: %s' % (len(missing), ', '.join(missing)),
            required=False)

        hooks = settings.get('hooks') or {}
        pre = hooks.get('PreToolUse') or []
        found = None
        for entry in pre:
            if not isinstance(entry, dict):
                continue
            cmds = []
            for h in entry.get('hooks') or []:
                if isinstance(h, dict):
                    cmds.append(str(h.get('command') or ''))
            if any('kflow-main-agent-gate' in c for c in cmds):
                found = entry
                break
        if found is None:
            add('hooks.PreToolUse', False, '未找到门控脚本注册条目')
        else:
            matcher = str(found.get('matcher') or '')
            covered = {m.strip() for m in matcher.split('|') if m.strip()}
            missing_m = REQUIRED_MATCHERS - covered
            add('hooks.PreToolUse', not missing_m,
                'matcher=%s' % matcher if not missing_m else 'matcher 缺少: %s' % ', '.join(sorted(missing_m)))
            timeout = None
            for h in found.get('hooks') or []:
                if isinstance(h, dict) and 'kflow-main-agent-gate' in str(h.get('command') or ''):
                    timeout = h.get('timeout')
            add('hook.timeout', timeout is not None and isinstance(timeout, (int, float)),
                'timeout=%r（建议 5 秒）' % (timeout,), required=False)

    gate_path = os.path.join(root, GATE_SCRIPT_REL)
    add('门控脚本', os.path.isfile(gate_path),
        '存在' if os.path.isfile(gate_path) else '缺失: %s' % GATE_SCRIPT_REL)

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    results = check(root)
    failed = [r for r in results if r['required'] and not r['ok']]

    if args.json:
        sys.stdout.write(json.dumps({'root': root, 'results': results, 'failed': len(failed)},
                                    ensure_ascii=False, indent=2))
        sys.stdout.write('\n')
    else:
        sys.stdout.write('=== KFlow 项目配置校验 ===\n')
        sys.stdout.write('项目根: %s\n\n' % root)
        for r in results:
            mark = 'OK ' if r['ok'] else ('x  ' if r['required'] else '!  ')
            sys.stdout.write('  %s %-24s %s\n' % (mark, r['check'], r['detail']))
        sys.stdout.write('\n')
        if failed:
            sys.stdout.write('状态: x %d 项必需配置不合规\n' % len(failed))
        else:
            sys.stdout.write('状态: OK 必需配置全部通过\n')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
