# -*- coding: utf-8 -*-
"""kflow-doc-optimize / VERIFY：引用扫描与完整性校验。

用法:
    # 1) 执行前：扫描项目中对某文档的全部引用
    python check_refs.py find --root <项目根> --target docs/open/guide.md

    # 2) 执行前：把引用清单写入留档文件（TSV：引用文件<TAB>行号<TAB>引用路径）
    python check_refs.py find --root <项目根> --target docs/open/guide.md --write docs/doc-optimize-references.md

    # 3) 执行后：校验清单中的全部引用是否可解析
    python check_refs.py verify --root <项目根> --list docs/doc-optimize-references.md

    # 4) 执行后：批量替换引用（先 dry-run，确认后加 --apply）
    python check_refs.py replace --root <项目根> --old docs/open/guide.md --new docs/open/guide/index.md [--apply]

退出码:
    0  通过（verify 无断链）
    1  存在无法解析的引用（verify）或存在待替换项（replace dry-run 且不 apply）
    2  参数或文件错误
"""
from __future__ import unicode_literals

import argparse
import io
import os
import re
import sys

SKIP_DIRS = {'.git', 'node_modules', 'targets', '__pycache__', '.venv', '.idea', '.vscode'}
SCAN_EXTS = {'.md', '.py', '.sh', '.json', '.yaml', '.yml', '.txt'}
# 执行前留档的引用清单：包含「原路径」，SHALL NOT 被替换（否则丢失反向还原依据）
REF_LIST_REL = 'docs/doc-optimize-references.md'
# 从 Markdown 表格/列表行中提取路径：优先反引号内，其次裸路径
BACKTICK_PATH_RE = re.compile(r'`([^`]+\.(?:md|py|sh|json|yaml|yml|txt))`')
BARE_PATH_RE = re.compile(r'((?:\.?/)?(?:[\w.\-{}/]+/)*[\w.\-{}]+\.(?:md|py|sh|json|yaml|yml|txt))')
MAPPING_RE = re.compile(r'替换映射:\s*`?([^`\s]+)`?\s*(?:→|->)\s*`?([^`\s]+)`?')


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in SCAN_EXTS:
                yield os.path.join(dirpath, name)


def extract_paths(line):
    paths = BACKTICK_PATH_RE.findall(line)
    if paths:
        return paths
    return [m for m in BARE_PATH_RE.findall(line)]


def find_refs(root, target):
    """返回 [(引用文件相对路径, 行号, 行内容)]。"""
    target_norm = target.replace('\\', '/').lstrip('./')
    base = os.path.basename(target_norm)
    out = []
    for path in iter_files(root):
        rel = os.path.relpath(path, root).replace('\\', '/')
        if rel == target_norm or rel == REF_LIST_REL:
            continue
        try:
            with io.open(path, encoding='utf-8', errors='replace') as f:
                for no, line in enumerate(f, 1):
                    if target_norm in line or base in line:
                        out.append((rel, no, line.rstrip('\n')))
        except Exception:
            continue
    return out


def write_list(root, refs, out_path):
    lines = ['# 受影响引用清单（kflow-doc-optimize 执行前留档）',
             '',
             '| 引用文件 | 行号 | 引用内容 |',
             '|---------|------|---------|']
    for rel, no, line in refs:
        safe = line.replace('|', '\\|')
        lines.append('| `%s` | %d | %s |' % (rel, no, safe))
    lines.append('')
    lines.append('> 本文件用于反向还原；优化执行后由 verify 校验全部引用可解析。')
    with io.open(out_path, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(lines) + '\n')


def parse_list(root, list_path):
    """从清单中提取 (引用文件, 引用路径) 对。"""
    pairs = []
    with io.open(list_path, encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s.startswith('|'):
                continue
            parts = [p.strip() for p in s.strip('|').split('|')]
            if len(parts) < 3:
                continue
            ref_file = parts[0].strip('` ')
            if ref_file in ('引用文件', '') or ref_file.startswith('---'):
                continue
            content = parts[-1]
            for p in extract_paths(content):
                pairs.append((ref_file, p))
    # 去重保序
    seen = set()
    out = []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def resolve(root, ref, ref_file=None):
    """判断引用能否解析为存在的文件。

    依次尝试：相对项目根、相对引用文件所在目录、常见文档目录前缀。
    """
    ref = ref.strip().strip('`').replace('\\', '/')
    if ref.startswith('http://') or ref.startswith('https://'):
        return True
    if '...' in ref:
        return True
    candidates = []
    if ref_file:
        candidates.append(os.path.join(root, os.path.dirname(ref_file), ref))
    candidates.append(os.path.join(root, ref))
    for prefix in ('', 'docs/', 'docs/designs/', 'docs/open/', 'skills/'):
        candidates.append(os.path.join(root, prefix, ref))
    return any(os.path.exists(c) for c in candidates)


def cmd_find(args):
    root = os.path.abspath(args.root)
    refs = find_refs(root, args.target)
    if args.write:
        write_list(root, refs, args.write)
        sys.stdout.write('已写入 %s（%d 条引用）\n' % (args.write, len(refs)))
    else:
        for rel, no, line in refs:
            sys.stdout.write('%s:%d: %s\n' % (rel, no, line))
    return 0


def read_mappings(list_path):
    """读取留档清单中的替换映射（old -> new）。"""
    mapping = {}
    try:
        with io.open(list_path, encoding='utf-8', errors='replace') as f:
            for line in f:
                m = MAPPING_RE.search(line)
                if m:
                    mapping[m.group(1)] = m.group(2)
    except Exception:
        pass
    return mapping


def cmd_verify(args):
    root = os.path.abspath(args.root)
    if not os.path.isfile(args.list):
        sys.stderr.write('错误: 未找到引用清单 %s\n' % args.list)
        return 2

    pairs = parse_list(root, args.list)
    mapping = read_mappings(args.list)
    ref_files = sorted({rf for rf, _ in pairs})

    broken = []
    checked = 0
    for rf in ref_files:
        path = os.path.join(root, rf)
        if not os.path.exists(path):
            broken.append((rf, '<引用文件缺失>'))
            continue
        try:
            with io.open(path, encoding='utf-8', errors='replace') as f:
                lines = f.read().split('\n')
        except Exception:
            broken.append((rf, '<引用文件不可读>'))
            continue
        for no, line in enumerate(lines, 1):
            for p in extract_paths(line):
                checked += 1
                if not resolve(root, p, rf):
                    broken.append((rf, p))

    # 替换映射的目标路径必须存在
    for old, new in mapping.items():
        checked += 1
        if not os.path.exists(os.path.join(root, new)):
            broken.append(('<替换映射>', '%s -> %s（目标不存在）' % (old, new)))

    sys.stdout.write('校验引用: %d 条（涉及 %d 个引用文件）\n' % (checked, len(ref_files)))
    if mapping:
        sys.stdout.write('替换映射: %d 条\n' % len(mapping))
    if broken:
        sys.stdout.write('断链: %d 条\n' % len(broken))
        for rf, p in broken:
            sys.stdout.write('  - %s (在 %s)\n' % (p, rf))
        return 1
    sys.stdout.write('状态: OK 全部引用可解析\n')
    return 0


def cmd_replace(args):
    root = os.path.abspath(args.root)
    old = args.old.replace('\\', '/').lstrip('./')
    new = args.new.replace('\\', '/').lstrip('./')
    refs = find_refs(root, old)
    if not refs:
        sys.stdout.write('未发现对 %s 的引用\n' % old)
        return 0
    files = sorted({rel for rel, _, _ in refs if rel != REF_LIST_REL})
    sys.stdout.write('待替换: %d 处，涉及 %d 个文件\n' % (len(refs), len(files)))
    for rel in files:
        sys.stdout.write('  - %s\n' % rel)
    if not args.apply:
        sys.stdout.write('（dry-run；确认后加 --apply 执行替换）\n')
        return 1

    old_abs = os.path.join(root, old)
    new_abs = os.path.join(root, new)
    changed = 0
    total_repl = 0
    for rel in files:
        path = os.path.join(root, rel)
        ref_dir = os.path.dirname(path)
        # 同时处理：项目根相对路径、引用文件相对路径、去掉 ./ 前缀的形式
        forms = {old}
        try:
            rel_old = os.path.relpath(old_abs, ref_dir).replace('\\', '/')
            rel_new = os.path.relpath(new_abs, ref_dir).replace('\\', '/')
        except Exception:
            rel_old = rel_new = None
        with io.open(path, encoding='utf-8', errors='replace') as f:
            text = f.read()
        before = text
        cnt = 0
        for form, repl in [(old, new)] + ([(rel_old, rel_new)] if rel_old else []):
            if form and form != repl:
                cnt += text.count(form)
                text = text.replace(form, repl)
        if text != before:
            with io.open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(text)
            changed += 1
            total_repl += cnt
    sys.stdout.write('已替换 %d 处，涉及 %d 个文件\n' % (total_repl, changed))

    # 在留档清单中记录替换映射（保留原路径用于反向还原，映射用于执行后校验）
    list_path = os.path.join(root, REF_LIST_REL)
    if os.path.isfile(list_path):
        with io.open(list_path, encoding='utf-8', errors='replace') as f:
            text = f.read()
        text = re.sub(r'^> 替换映射: `%s` .*$\n?' % re.escape(old), '', text, flags=re.M)
        if not text.endswith('\n'):
            text += '\n'
        text += '> 替换映射: `%s` → `%s`\n' % (old, new)
        with io.open(list_path, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        sys.stdout.write('已在 %s 记录替换映射\n' % REF_LIST_REL)

    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')

    p_find = sub.add_parser('find')
    p_find.add_argument('--root', default=os.getcwd())
    p_find.add_argument('--target', required=True)
    p_find.add_argument('--write')

    p_ver = sub.add_parser('verify')
    p_ver.add_argument('--root', default=os.getcwd())
    p_ver.add_argument('--list', required=True)

    p_rep = sub.add_parser('replace')
    p_rep.add_argument('--root', default=os.getcwd())
    p_rep.add_argument('--old', required=True)
    p_rep.add_argument('--new', required=True)
    p_rep.add_argument('--apply', action='store_true')

    args = ap.parse_args()
    if args.cmd == 'find':
        return cmd_find(args)
    if args.cmd == 'verify':
        return cmd_verify(args)
    if args.cmd == 'replace':
        return cmd_replace(args)
    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
