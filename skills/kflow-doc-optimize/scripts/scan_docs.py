# -*- coding: utf-8 -*-
"""kflow-doc-optimize / SCAN：扫描项目文档，按阈值输出优化清单。

用法:
    python scan_docs.py [--root <项目根>] [--json] [--min-kb N] [--max-records N]

输出:
    默认输出 Markdown 清单（可直接用于 REPORT 步骤）；
    --json 输出结构化 JSON（供后续脚本或自动化消费）。

判定规则（权威定义见 scan-rules.md）:
    修订记录超量   : 头部修订记录表的数据行 > 3
    超出分片阈值   : 单文件体积 > 80 KB
    缺少章节索引   : 单文件体积 > 30 KB 且无章节索引
    CONTEXT.md     : 术语表例外——不拆分；> 30 KB 时要求术语索引

扫描范围:
    CONTEXT.md、docs/designs/**、docs/open/**、docs/changes/**（活跃变更，排除 archive）
排除:
    .status.md、status-log.md、docs/changes/archive/**
"""
from __future__ import unicode_literals

import argparse
import io
import json
import os
import re
import sys

KB = 1024
INDEX_THRESHOLD_KB = 30
SPLIT_THRESHOLD_KB = 80
RECORD_LIMIT = 3

# 修订记录章节标题：`## 修订记录`、`## 七、修订记录`、`## 本册修订记录`
REV_HEADING_RE = re.compile(r'^#{2,4}\s*.*修订记录\s*$')
# 表格分隔行
SEP_RE = re.compile(r'^\|[ :\-|]+\|[ \t]*$')
# 章节索引导航的标题
INDEX_HEADING_RE = re.compile(r'^#{2,4}\s*.*(章节导航|章节索引|目录)\s*$', re.IGNORECASE)
EXCLUDED_NAMES = {'.status.md', 'status-log.md'}


def is_excluded(path, root):
    rel = os.path.relpath(path, root).replace('\\', '/')
    if os.path.basename(path) in EXCLUDED_NAMES:
        return True
    if rel.startswith('docs/changes/archive/'):
        return True
    return False


def iter_docs(root):
    """遍历扫描范围内的 Markdown 文档。"""
    targets = []
    context = os.path.join(root, 'CONTEXT.md')
    if os.path.isfile(context):
        targets.append(context)
    for base in ('docs/designs', 'docs/open', 'docs/changes'):
        d = os.path.join(root, base)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            if base == 'docs/changes' and 'archive' in dirnames:
                rel = os.path.relpath(dirpath, root).replace('\\', '/')
                if rel == 'docs/changes':
                    dirnames.remove('archive')
            for name in filenames:
                if name.endswith('.md'):
                    p = os.path.join(dirpath, name)
                    if not is_excluded(p, root):
                        targets.append(p)
    return sorted(set(targets))


def count_revision_rows(lines):
    """统计首个修订记录章节表格的数据行数（不含表头与分隔行）。"""
    in_sec = False
    rows = 0
    seen_table = False
    for line in lines:
        s = line.rstrip('\r\n')
        if REV_HEADING_RE.match(s):
            in_sec = True
            continue
        if in_sec and s.startswith('#'):
            break
        if not in_sec:
            continue
        if s.startswith('|'):
            if SEP_RE.match(s):
                seen_table = True
                continue
            # 表头行（分隔行之前）不计入
            if not seen_table:
                continue
            rows += 1
    return rows


def has_section_index(lines):
    for line in lines:
        s = line.rstrip('\r\n')
        if INDEX_HEADING_RE.match(s):
            return True
        # 形如 `| 章节 | 行号 |` 的导航表
        if s.startswith('|') and ('行号' in s or '所在文件' in s):
            return True
    return False


def has_term_index(lines):
    for line in lines:
        s = line.rstrip('\r\n')
        if '术语索引' in s:
            return True
    return False


def scan(root):
    items = []
    for path in iter_docs(root):
        rel = os.path.relpath(path, root).replace('\\', '/')
        try:
            size = os.path.getsize(path)
            with io.open(path, encoding='utf-8', errors='replace') as f:
                lines = f.read().split('\n')
        except Exception:
            continue
        size_kb = size / float(KB)
        is_context = os.path.basename(path) == 'CONTEXT.md'
        problems = []

        rev_rows = count_revision_rows(lines)
        if rev_rows > RECORD_LIMIT:
            problems.append({
                'type': '修订记录超量',
                'detail': '%d 条 > %d' % (rev_rows, RECORD_LIMIT),
                'action': '裁剪修订记录至最近 %d 条，其余移入历史承载位置' % RECORD_LIMIT,
            })

        if is_context:
            if size_kb > INDEX_THRESHOLD_KB and not has_term_index(lines):
                problems.append({
                    'type': '缺少章节索引',
                    'detail': '术语表 %.1f KB > %d KB 且无术语索引' % (size_kb, INDEX_THRESHOLD_KB),
                    'action': '建立按模块/首字母的术语索引（保持单文件，不拆分）',
                })
        else:
            if size_kb > SPLIT_THRESHOLD_KB:
                problems.append({
                    'type': '超出分片阈值',
                    'detail': '%.1f KB > %d KB' % (size_kb, SPLIT_THRESHOLD_KB),
                    'action': '拆分为目录化结构 <name>/index.md + <name>/<section>.md',
                })
            elif size_kb > INDEX_THRESHOLD_KB and not has_section_index(lines):
                problems.append({
                    'type': '缺少章节索引',
                    'detail': '%.1f KB > %d KB 且无章节索引' % (size_kb, INDEX_THRESHOLD_KB),
                    'action': '在文件头部添加章节导航表，或建立同级 index.md',
                })

        if problems:
            items.append({
                'path': rel,
                'size_kb': round(size_kb, 1),
                'revision_rows': rev_rows,
                'is_context': is_context,
                'problems': problems,
            })
    return items


def to_markdown(items):
    if not items:
        return '无需优化：未发现超过留存边界或体积阈值的文档。\n'
    out = ['| # | 文档路径 | 问题类型 | 当前体积 | 优化方式 |', '|---|---------|---------|---------|---------|']
    for i, it in enumerate(items, 1):
        types = '；'.join(p['type'] for p in it['problems'])
        actions = '；'.join(p['action'] for p in it['problems'])
        out.append('| %d | `%s` | %s | %.1f KB / %d 条修订 | %s |' % (
            i, it['path'], types, it['size_kb'], it['revision_rows'], actions))
    out.append('')
    out.append('> 受影响引用位置需在 EXECUTE 前扫描并留档（见 verify-rules.md §1）。')
    return '\n'.join(out) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    items = scan(root)
    if args.json:
        sys.stdout.write(json.dumps({'root': root, 'items': items}, ensure_ascii=False, indent=2))
        sys.stdout.write('\n')
    else:
        sys.stdout.write(to_markdown(items))
    return 0


if __name__ == '__main__':
    sys.exit(main())
