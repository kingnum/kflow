# -*- coding: utf-8 -*-
"""生成 references-src/slice-manifest.tsv —— 各共享 references 文件的按阶段切片清单。

sections 指令语法（详见 scripts/sync-references.sh 头部）：
  N         保留整节 N
  -N        排除整节 N
  N:a:b     在节 N 内仅保留子节 a 与 b
  ~N:LO-HI  用权威源第 LO-HI 行替换节 N 的正文（行号由本脚本从权威源动态求得）
  ^N:KEY    在节 N 的表格内仅保留含 KEY 的数据行
"""
import io
import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'references-src')
SRC = os.path.normpath(SRC)


def read(fn):
    with io.open(os.path.join(SRC, fn), encoding='utf-8') as f:
        return f.read()


def sections(fn):
    """返回 [(编号, 起始行号), ...]，编号为 '1' / '一' 这类规范形式。"""
    out = []
    for i, line in enumerate(read(fn).split('\n'), 1):
        if not line.startswith('## '):
            continue
        title = line[3:].strip()
        if not title:
            continue
        num = title.split(' ')[0].rstrip('.').rstrip('、')
        if not num:
            continue
        if num[0].isdigit() or title[0] in u'一二三四五六七八九十':
            out.append((num, i))
    return out


def block(fn, first, last=None):
    """取 [first, last] 两节（含）的起止行号，返回 (起行, 止行)。"""
    secs = sections(fn)
    idx = {n: i for i, (n, _) in enumerate(secs)}
    start = secs[idx[first]][1]
    if last is None:
        last = first
    if idx[last] + 1 < len(secs):
        end = secs[idx[last] + 1][1] - 1
    else:
        end = len(read(fn).rstrip('\n').split('\n'))
    return start, end


def entry_lines(fn, first, last=None):
    """取 [first, last] 两节正文（不含起始节标题行），返回 (起行, 止行)。"""
    s, e = block(fn, first, last)
    return s + 1, e


def sub_spans(fn, num, subs):
    """返回一级节 num 下「仅含指定子节」的行区间列表 [(lo, hi), ...]（绝对行号，含节标题行）。

    用于 ~N:LO-HI 指令。首段自节标题行起（保留节标题与节首引言），
    各段止于下一个被排除子节的标题行之前，末段止于下一一级节之前。
    """
    lines = read(fn).split('\n')
    inside = False
    marks = []                       # (行号, 子节号 或 None)
    end_of_sec = len(lines)
    for i, l in enumerate(lines, 1):
        if l.startswith('## '):
            if inside:
                end_of_sec = i - 1
                break
            inside = l[3:].strip().split(' ')[0].rstrip('.').rstrip('、') == num
            if inside:
                marks.append((i, None))
            continue
        if inside and l.startswith('### '):
            marks.append((i, l[4:].strip().split(' ')[0].rstrip('.')))
    if not marks:
        raise SystemExit('sub_spans 未找到节: %s' % num)

    spans = []
    cur = marks[0][0]
    in_span = True                   # 首段自节标题行起，节首引言属首段
    for ln, sid in marks[1:]:
        if sid in subs:
            if not in_span:
                cur = ln
                in_span = True
            continue
        if in_span:
            spans.append((cur, ln - 1))
            in_span = False
    if in_span:
        spans.append((cur, end_of_sec))
    if not spans:
        raise SystemExit('sub_spans 结果为空: §%s subs=%s' % (num, subs))
    return spans


# ── 各文件的通用基础集合 ──────────────────────────────────────────────
# repetition.md：执行模型核心特征 / 阶段分类 / 执行流程 / 复杂度评估 / Agent 完成判断
#   / 主 Agent 验收标准 / 验收失败处理 / 子代理 prompt 规范 / 子代理隔离规则
#   §14 终止模型按阶段类型子节切片（见 build()），§13 轮间摘要与 §15~§18 按阶段追加。

# gates.md §2 按阶段切片：以「一阶段一条目」为单位做定点替换。
# 键 = 阶段；值 = (起始条目首行文本片段, 终止条目首行文本片段 或 None 表示到节末)。
# 区间为前闭后闭：自起始条目的首行起，至终止条目的首行前一行止。
GATE_ENTRIES = {
    'prototype-design': ('0. 进入原型设计阶段', '2. 进入计划阶段'),
    'explore': ('1. 进入详细设计阶段', '1.5 原型设计用户评审门控'),
    'design': ('2. 进入计划阶段', '3. 进入编码阶段'),
    'plan': ('3. 进入编码阶段', '4. 进入接口单元测试阶段'),
    'code': ('3. 进入编码阶段', '4. 进入接口单元测试阶段'),
    'code-review': ('4. 进入接口单元测试阶段', '5. 进入 E2E 测试阶段'),
    'api-test': ('4. 进入接口单元测试阶段', '5. 进入 E2E 测试阶段'),
    'e2e-test': ('5. 进入 E2E 测试阶段', '6. 进入集成测试阶段'),
    'integration-test': ('6. 进入集成测试阶段', '7. 进入归档阶段'),
    'audit': ('7. 进入归档阶段', '9. 中断恢复产物完整性验证门控'),
    'archive': ('7. 进入归档阶段', '9. 中断恢复产物完整性验证门控'),
    'bug-fix': ('3. 进入编码阶段', '4. 进入接口单元测试阶段'),
    'resume': ('9. 中断恢复产物完整性验证门控', None),
}


def gate_range(key):
    """求 §2 中某阶段门控条目的行区间（含条目首行与全部下属子节）。"""
    start_pat, end_pat = GATE_ENTRIES[key]
    lines = read('gates.md').split('\n')
    in_sec2 = False
    start = None
    for i, l in enumerate(lines, 1):
        if l.startswith('## 2. '):
            in_sec2 = True
            continue
        if in_sec2 and l.startswith('## '):
            break
        if not in_sec2:
            continue
        s = l.strip()
        if start is None:
            if s.startswith(start_pat):
                start = i
            continue
        if end_pat is not None and s.startswith(end_pat):
            return start, i - 1
    if start is None:
        raise SystemExit('gate_range 未找到条目: %s' % key)
    return start, len(lines)

# phase-transition.md：概述 + 衔接决策表 + 阶段→Skill 调度映射表 + 归档闸口
PT_BASE = '1,2,3,5'

# self-review.md：概述 + 签署清单 + 单轮验证 + 修复责任与交付 + 自审流程 + 验证报告内容
SR_BASE = '1,3,4,5,6,10,13'

# service-lifecycle.md：全文（再做阶段排除）
SL_BASE = '1,2,3,4,5,6,7'

# hooks.md：配置表 + PRE_HOOK + POST_HOOK + RELOAD 清单 + 服务生命周期操作步骤
HK_BASE = '1,2,3,4,5'

# state-values.md：阶段流转状态值 + 变更档位字段
SV_BASE = '1,4'


# ── 各文件的按阶段差异化部分 ────────────────────────────────────────
GATES_EXTRA = {
    'explore': '',
    'prototype-design': '',
    'design': '',
    'plan': ',7',                       # HITL 阻塞 plan 入口规则
    'code': ',8',                       # 编码阶段上游问题决策流程
    'code-review': ',4,5',              # 代码审查门控 + 审查闭环验证
    'api-test': ',6',                   # 子变更依赖规则
    'e2e-test': ',6',
    'integration-test': ',6',
    'audit': '',
    'archive': '',
    'bug-fix': ',8,9',                  # 上游问题决策 + 缺陷修复快车道门控
    'resume': '',
}

REP_EXTRA = {
    'plan': '',
    'code': ',13,15,16,17',
    'code-review': ',13,15,16,17',
    'api-test': '',
    'e2e-test': '',
    'integration-test': '',
    'bug-fix': ',13,15,16,17,18',
    'bug-triage': '',
}

PT_EXTRA = {
    'explore': ',6^6:设计探索',
    'prototype-design': ',4,6^6:原型设计',
    'design': ',6^6:详细设计',
    'plan': ',4',
    'code': ',4',
    'code-review': ',4',
    'api-test': ',4',
    'e2e-test': ',4',
    'integration-test': ',4',
    'audit': ',6^6:审计',
    'archive': '',
    'resume': '',
}

# state-values.md 按阶段追加的字段节（仅保留本阶段产生或消费的状态值）
SV_EXTRA = {
    'explore': '',            # 产出变更档位初判值（§4 已在基础集合）
    'prototype-design': ',3',  # 审查方式记录字段（本阶段写入并消费）
    'design': ',2,5,6',        # 用户评审状态值 + 阶段适用性声明（本阶段生成）+ 耗时遥测
    'plan': ',2,6',            # 用户评审状态值 + 耗时遥测
    'code': ',6',              # 耗时遥测
    'code-review': ',6',       # 耗时遥测
    'api-test': ',5,6',        # 阶段适用性声明（裁剪判定）+ 耗时遥测
    'e2e-test': ',2,5,6',      # 用户评审 + 适用性声明 + 耗时遥测
    'integration-test': ',2,5,6',
    'bug-fix': ',6',           # 耗时遥测
}

# self-review.md 按阶段保留的自审维度子节（§2 下的 2.1/2.2/2.3）
SR_EXTRA = {
    'explore': '2:2.1',
    'prototype-design': '2:2.2',
    'design': '2:2.3',
}

# service-lifecycle.md 按阶段排除的章节
#   2 = 端口冲突检测 / 4 = 健康检查 / 6 = 浏览器进程清理 / 7 = 数据库迁移
SL_DROP = {
    'api-test': '-6',       # 后端服务阶段：不启动浏览器，排除浏览器进程清理
    'e2e-test': '-7',       # 前后端测试阶段：迁移由 PRE_HOOK 的 MIGRATE 承载，非本节
    'integration-test': '-7',
    'code': '-2,-4,-6,-7',  # 仅编译验证：无端口检测 / 健康检查 / 浏览器 / 迁移
}

# hooks.md 按阶段保留的 PRE_HOOK(§2) 与 POST_HOOK(§3) 子节
HK_SUB = {
    'explore': ('2:2.1', '3:3.1'),
    'prototype-design': ('2:2.2', '3:3.2'),
    'design': ('2:2.1', '3:3.1'),
    'plan': ('2:2.1', '3:3.1'),
    'code': ('2:2.3', '3:3.3'),
    'code-review': ('2:2.1', '3:3.1'),
    'api-test': ('2:2.4', '3:3.4'),
    'e2e-test': ('2:2.5', '3:3.4'),
    'integration-test': ('2:2.5', '3:3.4'),
    'audit': ('2:2.1', '3:3.1'),
    'archive': ('2:2.1', '3:3.1'),
    'bug-fix': ('2:2.6', '3:3.5'),
    'bug-triage': ('2:2.6', '3:3.5'),
}

# ── 各文件的持有者清单 ──────────────────────────────────────────────
HOLDERS = {
    'gates.md': ['kflow-api-test', 'kflow-bug-fix', 'kflow-code', 'kflow-code-review',
                 'kflow-design', 'kflow-e2e-test', 'kflow-explore', 'kflow-integration-test',
                 'kflow-plan', 'kflow-prototype-design'],
    'repetition.md': ['kflow-api-test', 'kflow-bug-fix', 'kflow-bug-triage', 'kflow-code',
                      'kflow-code-review', 'kflow-e2e-test', 'kflow-integration-test', 'kflow-plan'],
    'state-values.md': ['kflow-api-test', 'kflow-bug-fix', 'kflow-code', 'kflow-code-review',
                        'kflow-design', 'kflow-e2e-test', 'kflow-explore', 'kflow-integration-test',
                        'kflow-plan', 'kflow-prototype-design'],
    'self-review.md': ['kflow-design', 'kflow-explore', 'kflow-prototype-design'],
    'phase-transition.md': ['kflow-api-test', 'kflow-audit', 'kflow-code', 'kflow-code-review',
                            'kflow-design', 'kflow-e2e-test', 'kflow-explore', 'kflow-integration-test',
                            'kflow-plan', 'kflow-prototype-design', 'kflow-resume'],
    'service-lifecycle.md': ['kflow-api-test', 'kflow-code', 'kflow-e2e-test', 'kflow-integration-test'],
    'hooks.md': ['kflow-api-test', 'kflow-archive', 'kflow-audit', 'kflow-bug-fix', 'kflow-bug-triage',
                 'kflow-code', 'kflow-code-review', 'kflow-design', 'kflow-e2e-test', 'kflow-explore',
                 'kflow-integration-test', 'kflow-plan', 'kflow-prototype-design'],
}

# gates.md 阶段键映射（skill 名 → 阶段键）
GATES_KEY = {
    'kflow-explore': 'explore',
    'kflow-prototype-design': 'prototype-design',
    'kflow-design': 'design',
    'kflow-plan': 'plan',
    'kflow-code': 'code',
    'kflow-code-review': 'code-review',
    'kflow-api-test': 'api-test',
    'kflow-e2e-test': 'e2e-test',
    'kflow-integration-test': 'integration-test',
    'kflow-bug-fix': 'bug-fix',
}


def build():
    L = []
    L.append(u'# 切片清单 — references 文件的权威源与按阶段切片规则')
    L.append(u'#')
    L.append(u'# 字段: <权威源文件名>\t<所属 skill>\t<sections>')
    L.append(u'#')
    L.append(u'# 权威源位于 references-src/；各 skill 的副本位于 skills/<skill>/references/<文件>，')
    L.append(u'# 由 scripts/sync-references.sh 依据本清单生成并校验，SHALL NOT 逐一手工编辑。')
    L.append(u'# sections 指令语法见 scripts/sync-references.sh 头部注释；留空 = 全量形态。')
    L.append(u'# 切片规则权威定义见 docs/designs/core-mechanisms/07-agent-model.md §17.3。')
    L.append(u'#')

    def emit(fn, sk, spec):
        L.append(u'%s\t%s\t%s' % (fn, sk, spec))

    # ── gates.md ──
    L.append(u'')
    L.append(u'# ── gates.md — 门控标注约定(§1) + 本阶段正向门控(§2 定点) + 阶段回退门控(§3) + 本阶段专属规则 ──')
    for sk in HOLDERS['gates.md']:
        key = GATES_KEY[sk]
        a, b = gate_range(key)
        emit('gates.md', sk, '1,~2:%d-%d,3%s' % (a, b, GATES_EXTRA[key]))

    # ── repetition.md ──
    L.append(u'')
    L.append(u'# ── repetition.md — 执行模型/执行流程/验收/prompt 规范/隔离规则 + 本阶段适用章节 ──')
    s14_end = block('repetition.md', '14')[1]
    s141 = sub_spans('repetition.md', '14', ['14.1', '14.4', '14.5'])
    s142 = sub_spans('repetition.md', '14', ['14.1', '14.2', '14.4', '14.5'])
    s143 = sub_spans('repetition.md', '14', ['14.1', '14.3', '14.4', '14.5'])

    def rep_spec(spans, extra):
        # ~N:LO-HI+LO-HI → 用多段行区间（按序拼接）替换节 N 的正文
        rep = '+'.join('%d-%d' % (a, b) for a, b in spans)
        return ','.join(['2', '3', '4', '5', '7', '8', '9', '10', '12', '~14:' + rep] + extra)

    for sk in HOLDERS['repetition.md']:
        key = sk[len('kflow-'):]
        extra = [e for e in REP_EXTRA.get(key, '').split(',') if e]
        if key in ('api-test', 'e2e-test', 'integration-test'):
            spec = rep_spec(s142, extra)      # 单轮类：保留 14.2 定向重验，排除 14.3
        else:
            spec = rep_spec(s143, extra)      # 重复制类：保留 14.3 循环终止，排除 14.2
        emit('repetition.md', sk, spec)

    # ── state-values.md ──
    L.append(u'')
    L.append(u'# ── state-values.md — 阶段流转状态值(§1) + 变更档位字段(§4) + 本阶段相关字段 ──')
    for sk in HOLDERS['state-values.md']:
        key = sk[len('kflow-'):]
        emit('state-values.md', sk, SV_BASE + SV_EXTRA.get(key, ''))

    # ── self-review.md ──
    L.append(u'')
    L.append(u'# ── self-review.md — 本阶段自审维度(§2) + 签署清单 + 单轮验证 + 交付与门控 ──')
    for sk in HOLDERS['self-review.md']:
        key = sk[len('kflow-'):]
        emit('self-review.md', sk, SR_EXTRA[key] + ',' + SR_BASE)

    # ── phase-transition.md ──
    L.append(u'')
    L.append(u'# ── phase-transition.md — 衔接决策表 + 调度映射表 + 归档闸口 + 本阶段门控边界 ──')
    for sk in HOLDERS['phase-transition.md']:
        key = sk[len('kflow-'):]
        emit('phase-transition.md', sk, PT_BASE + PT_EXTRA.get(key, ''))

    # ── service-lifecycle.md ──
    L.append(u'')
    L.append(u'# ── service-lifecycle.md — 服务启动/停止/健康检查操作指令（按阶段排除不适用章节）──')
    for sk in HOLDERS['service-lifecycle.md']:
        key = sk[len('kflow-'):]
        drop = [d for d in SL_DROP.get(key, '').split(',') if d]
        spec = ','.join(['1', '2', '3', '4', '5', '6', '7'] + drop)
        emit('service-lifecycle.md', sk, spec)

    # ── hooks.md ──
    L.append(u'')
    L.append(u'# ── hooks.md — 钩子配置表(§1) + 本阶段 PRE_HOOK/POST_HOOK + RELOAD 清单(§4) + 服务操作映射(§5) ──')
    for sk in HOLDERS['hooks.md']:
        key = sk[len('kflow-'):]
        pre, post = HK_SUB[key]
        emit('hooks.md', sk, '1,%s,%s,4,5' % (pre, post))

    L.append(u'')
    with io.open(os.path.join(SRC, 'slice-manifest.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L))


if __name__ == '__main__':
    build()
    print('written')
