# -*- coding: utf-8 -*-
"""从权威源生成按阶段切片的 references 副本，并校验与权威源一致。

用法: python scripts/sync_references.py  （scripts/sync-references.sh 为其入口包装）

切片语义与指令语法见 scripts/sync-references.sh 头部注释。
本实现使用 Python 而非 awk：gawk 在部分 locale 下对多字节字符的正则匹配与数组下标
语义不可靠（章节标题含中文顿号、全数字章节号与 strnum 作数值等价），改用 Python 可稳定处理。
"""
from __future__ import unicode_literals

import io
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, 'skills')
SRC_DIR = os.path.join(REPO_ROOT, 'references-src')
MANIFEST = os.path.join(SRC_DIR, 'slice-manifest.tsv')

# 一级章节标题：`## 2. 标题` / `## 一、标题`
SEC_RE = re.compile(r'^## ([0-9]+|[一二三四五六七八九十]+)[.、]')
SUB_RE = re.compile(r'^#{3,4} ')
NUM_SUB_RE = re.compile(r'^[0-9]+(\.[0-9]+)*$')
SKILL_REF_RE = re.compile(r'skills/kflow-[a-z0-9-]+/')

# 中文序号 → 阿拉伯数字：清单与代码统一使用后者定位章节
# （部分 references 文件以 `## 一、` 而非 `## 1.` 编号）
CN_NUM = {
    u'一': '1', u'二': '2', u'三': '3', u'四': '4', u'五': '5',
    u'六': '6', u'七': '7', u'八': '8', u'九': '9', u'十': '10',
}


def read_lines(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        return f.read().split('\n')


def normalize(line):
    """用于匹配的归一化：剔除行尾 CR；顿号→句点+空格。"""
    line = line.rstrip('\n').rstrip('\r')
    return line.replace('、', '. ')


def secnum(line):
    """取章节编号，中文序号归一为阿拉伯数字：`## 2. 标题` → '2'；`## 一、标题` → '1'。"""
    m = SEC_RE.match(normalize(line))
    if not m:
        return None
    tok = m.group(1)
    return CN_NUM.get(tok, tok)


def subnum(line):
    """取子节编号：`### 2.1 标题` → '2.1'；非编号子节返回 None。"""
    if not SUB_RE.match(line):
        return None
    body = normalize(line).lstrip('#').strip()
    tok = body.split(' ')[0].rstrip('.').rstrip('、')
    return tok if NUM_SUB_RE.match(tok) else None


def parse_spec(spec):
    """解析 sections 指令，返回 (keep, drop, subkeep, repl, rowfilters)。"""
    keep = set()
    drop = set()
    subkeep = {}
    repl = []
    rowfilters = []
    if not spec:
        keep.add('*')
        return keep, drop, subkeep, repl, rowfilters

    for tok in spec.split(','):
        tok = tok.strip()
        if not tok:
            continue
        if tok.startswith('~'):
            sec, _, ranges = tok[1:].partition(':')
            spans = []
            for part in ranges.split('+'):
                lo, _, hi = part.partition('-')
                spans.append((int(lo), int(hi)))
            repl.append((sec, spans))
            continue
        if tok.startswith('^'):
            sec, _, key = tok[1:].partition(':')
            rowfilters.append((sec, key))
            continue
        if tok.startswith('-'):
            drop.add(tok[1:])
            continue
        sec, sep, subs = tok.partition(':')
        keep.add(sec)
        if sep:
            subkeep[sec] = subs.split(':')

    if not keep:
        keep.add('*')
    return keep, drop, subkeep, repl, rowfilters


def extract_sections(lines, parsed):
    """按 keep/drop/subkeep 抽取章节；输出保留原文行。"""
    keep, drop, subkeep, _, _ = parsed
    all_keep = '*' in keep
    out = []
    in_sec = False
    in_sub = False
    seen = False
    cur_subs = None

    for raw in lines:
        n = secnum(raw)
        if n is not None:
            in_sec = (all_keep or n in keep) and (n not in drop)
            cur_subs = subkeep.get(n)
            if in_sec:
                out.append(raw)
            in_sub = in_sec
            seen = True
            continue
        if SUB_RE.match(raw):
            if not seen:
                out.append(raw)
                continue
            if not in_sec:
                continue
            if cur_subs is None:
                out.append(raw)
                continue
            sid = subnum(raw)
            in_sub = bool(sid) and sid in cur_subs
            if in_sub:
                out.append(raw)
            continue
        if not seen:
            out.append(raw)
            continue
        if in_sec and in_sub:
            out.append(raw)
    return out


def apply_replacements(lines, src_lines, parsed):
    """应用行区间替换与表格行过滤；输出保留原文行。"""
    _, _, _, repl, rowfilters = parsed

    for sec, spans in repl:
        new = []
        in_sec = False
        for raw in lines:
            n = secnum(raw)
            if n is not None:
                if n == sec:
                    new.append(raw)
                    for lo, hi in spans:
                        new.extend(src_lines[lo - 1:hi])
                    in_sec = True
                    continue
                in_sec = False
            if not in_sec:
                new.append(raw)
        lines = new

    for sec, key in rowfilters:
        new = []
        in_sec = False
        for raw in lines:
            n = secnum(raw)
            if n is not None:
                in_sec = (n == sec)
                new.append(raw)
                continue
            if not in_sec:
                new.append(raw)
                continue
            s = normalize(raw)
            if s.startswith('|'):
                if re.match(r'^\|[ :\-|]+\|[ \t]*$', s):
                    new.append(raw)
                    continue
                if key in s:
                    new.append(raw)
                continue
            new.append(raw)
        lines = new

    return lines


def render(ref_file, skill, spec):
    """生成某 skill 的某 references 文件内容。"""
    src = os.path.join(SRC_DIR, ref_file)
    if spec:
        src_lines = read_lines(src)
        parsed = parse_spec(spec)
        lines = extract_sections(src_lines, parsed)
        lines = apply_replacements(lines, src_lines, parsed)
        text = '\n'.join(lines)
        if not text.endswith('\n'):
            text += '\n'
    else:
        with io.open(src, encoding='utf-8', newline='') as f:
            text = f.read()
    return text.replace('skills/<SKILL>/', 'skills/%s/' % skill)


def normalize_skill_refs(text):
    return SKILL_REF_RE.sub('skills/<SKILL>/', text)


def load_manifest():
    entries = []
    with io.open(MANIFEST, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            ref_file, skill = parts[0], parts[1]
            spec = parts[2].strip() if len(parts) > 2 else ''
            entries.append((ref_file, skill, spec))
    return entries


def main():
    if not os.path.exists(MANIFEST):
        sys.stderr.write('错误: 未找到切片清单 %s\n' % MANIFEST)
        return 2

    entries = load_manifest()

    print('=== References 生成 ===')
    print('')
    print('权威源: %s' % SRC_DIR)
    print('切片清单: %s' % MANIFEST)
    print('')

    generated = 0
    bad = 0
    for ref_file, skill, spec in entries:
        if not os.path.exists(os.path.join(SRC_DIR, ref_file)):
            print('  x 权威源不存在: references-src/%s（条目: %s）' % (ref_file, skill))
            bad += 1
            continue
        if not os.path.isdir(os.path.join(SKILLS_DIR, skill)):
            print('  x skill 目录不存在: %s' % skill)
            bad += 1
            continue
        dest_dir = os.path.join(SKILLS_DIR, skill, 'references')
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        text = render(ref_file, skill, spec)
        with io.open(os.path.join(dest_dir, ref_file), 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        if not text.strip():
            print('  x 生成结果为空: %s/references/%s' % (skill, ref_file))
            bad += 1
            continue
        generated += 1

    print('生成条目: %d' % generated)
    if bad:
        print('状态: x %d 个条目生成失败' % bad)
        return 2

    print('')
    print('=== References 一致性校验 ===')
    print('')

    has_diff = False
    details = []
    total_checks = 0
    files = []
    for ref_file, _, _ in entries:
        if ref_file not in files:
            files.append(ref_file)

    for ref_file in sorted(files):
        if not os.path.exists(os.path.join(SRC_DIR, ref_file)):
            continue
        holders = [(sk, sp) for f, sk, sp in entries if f == ref_file]
        total_checks += 1
        print('  %s: %d 个 skill 持有，对比中...' % (ref_file, len(holders)))

        mismatches = []
        for skill, spec in holders:
            copy = os.path.join(SKILLS_DIR, skill, 'references', ref_file)
            expected = render(ref_file, skill, spec)
            if not os.path.exists(copy):
                mismatches.append('%s (副本缺失)' % skill)
                has_diff = True
                continue
            with io.open(copy, encoding='utf-8', newline='') as f:
                actual = f.read()
            ne = normalize_skill_refs(expected)
            na = normalize_skill_refs(actual)
            if ne != na:
                mismatches.append(skill)
                has_diff = True
                el = ne.split('\n')
                al = na.split('\n')
                first = ''
                for i in range(max(len(el), len(al))):
                    ei = el[i] if i < len(el) else '<EOF>'
                    ai = al[i] if i < len(al) else '<EOF>'
                    if ei != ai:
                        first = '第 %d 行: expected=%r actual=%r' % (i + 1, ei[:60], ai[:60])
                        break
                details.append('      - %s: %s' % (skill, first))

        if not mismatches:
            print('    OK 全部与权威源一致')
        else:
            print('    x 不一致 (%d 个 skill):' % len(mismatches))
            for m in mismatches:
                print('      - %s' % m)
        print('')

    if details:
        print('=== 差异位置 ===')
        for d in details:
            print(d)
        print('')

    print('=== 结果 ===')
    print('检查项: %d' % total_checks)
    if not has_diff:
        print('状态: OK 全部副本与权威源的阶段切片一致')
        return 0
    print('状态: x 存在与权威源不一致的副本，请检查切片清单')
    return 1


if __name__ == '__main__':
    sys.exit(main())
