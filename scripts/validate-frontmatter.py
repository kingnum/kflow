#!/usr/bin/env python3
"""
校验 SKILL.md front matter 与设计规格 YAML 块的合法性。

用途: 防止 front matter 中出现非法 YAML —— 典型场景是未加引号的 plain scalar
内出现 ASCII ": "（例如 `RELOAD: 全量产物`），YAML 解析器会将其判定为嵌套
mapping 并整块报错，`npx skills add` 会静默跳过该 Skill（不报错、不提示），
导致安装数量少于实际 Skill 数量。

校验点:
  1. front matter 可被 YAML 解析（核心，违反即致命）
  2. 必填字段 name / description 存在且非空
  3. skills/ 下 name 与所在目录名一致
  4. skills/ 下 version 与仓库根 VERSION 一致
  5. skills/ 下 description 含中文触发词（CLAUDE.md 发布要求：无中文触发词不发布）
  6. 设计规格 docs/designs/skills/*.md 中的 ```yaml 代码块可被 YAML 解析
     —— 该代码块是 SKILL.md front matter 的复制来源，必须同样合法

模板文件 docs/designs/templates/skills/SKILL-template.md 含 {占位符}，无法直接
解析；校验前先将 {…} 统一替换为占位符文本，使模板仍能被覆盖到（模板是错误写法
的传播源头，必须纳入校验）。

用法: python scripts/validate-frontmatter.py
退出码: 0 = 全部通过, 1 = 存在失败项
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
RUNTIME_SKILLS_DIR = ROOT / ".claude" / "skills"
DESIGN_SKILLS_DIR = ROOT / "docs" / "designs" / "skills"
TEMPLATE_FILE = ROOT / "docs" / "designs" / "templates" / "skills" / "SKILL-template.md"

sys.stdout.reconfigure(encoding="utf-8")

FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
FENCE_RE = re.compile(r"```ya?ml\r?\n(.*?)```", re.S)
CJK_RE = re.compile(r"[一-鿿]")

placeholders_used = False


def read_text(path):
    return path.read_text(encoding="utf-8").lstrip("﻿")


def split_front_matter(text):
    """返回 front matter 文本；无 front matter 时返回 None。"""
    m = FM_RE.match(text)
    return m.group(1) if m else None


def parse_yaml(block, tolerant):
    """解析 YAML；tolerant=True 时先把 {…} 占位符替换为纯文本。"""
    global placeholders_used
    if tolerant:
        if "{" in block:
            placeholders_used = True
        block = re.sub(r"\{[^}\n]*\}", "PLACEHOLDER", block)
    return yaml.safe_load(block)


def check_front_matter(path, text, label, tolerant=False):
    """校验真实 front matter，返回错误信息列表。"""
    errors = []
    block = split_front_matter(text)
    if block is None:
        return [f"{label}: 未找到 front matter（文件须以 --- 开头并以 --- 结束元数据块）"]

    try:
        meta = parse_yaml(block, tolerant)
    except yaml.YAMLError as exc:
        first = str(exc).splitlines()[0]
        errors.append(f"{label}: front matter YAML 解析失败 → {first}")
        return errors

    if not isinstance(meta, dict):
        return [f"{label}: front matter 不是 YAML mapping"]

    for field in ("name", "description"):
        if not str(meta.get(field) or "").strip():
            errors.append(f"{label}: 缺少必填字段 {field}")

    name = str(meta.get("name") or "").strip()
    if name and name != path.parent.name:
        errors.append(
            f"{label}: name 与目录名不一致 → name={name}, 目录={path.parent.name}"
        )

    return errors


def check_version(label, meta, expected_version):
    errors = []
    version = str((meta or {}).get("version") or "").strip()
    if not version:
        errors.append(f"{label}: 缺少 version 字段（须与根 VERSION 一致）")
    elif version != expected_version:
        errors.append(f"{label}: version={version} 与 VERSION={expected_version} 不一致")
    return errors


def check_chinese_trigger(label, description):
    if not CJK_RE.search(description or ""):
        return [f"{label}: description 缺少中文触发词（CLAUDE.md 要求无中文触发词不发布）"]
    return []


def check_design_yaml_blocks(path, label):
    """校验设计规格中的 ```yaml 代码块（front matter 的复制来源）。"""
    errors = []
    text = read_text(path)
    blocks = FENCE_RE.findall(text)
    if not blocks:
        return errors
    for idx, block in enumerate(blocks, start=1):
        if not re.search(r"^\s*name:", block, re.M):
            continue  # 非 Skill front matter 示例，跳过
        try:
            parse_yaml(block, tolerant=True)
        except yaml.YAMLError as exc:
            first = str(exc).splitlines()[0]
            errors.append(f"{label}: 第 {idx} 个 yaml 代码块解析失败 → {first}")
    return errors


def main():
    version_file = ROOT / "VERSION"
    if not version_file.exists():
        print(f"错误: 未找到 VERSION 文件 ({version_file})")
        return 1
    expected_version = read_text(version_file).splitlines()[0].strip()

    failures = []
    checked = 0

    print("=== Front Matter 校验 ===")
    print(f"目标版本: {expected_version}")
    print("")

    # 1) 待发布的 Skills（严格校验）
    print("skills/ (待发布 Skills)")
    publish_targets = sorted(SKILLS_DIR.glob("kflow-*/SKILL.md"))
    # 防空跑：源目录为空或路径错误时，glob 无匹配会让校验「0 通过 0 失败」地假通过
    if not publish_targets:
        failures.append(f"未发现任何 kflow-*/SKILL.md（源目录 {SKILLS_DIR} 为空或路径错误）")
        print(f"  ✗ 未发现任何待发布 Skill（{SKILLS_DIR}）")
    for skill_md in publish_targets:
        label = f"skills/{skill_md.parent.name}/SKILL.md"
        text = read_text(skill_md)
        errs = check_front_matter(skill_md, text, label)
        if not errs:
            meta = yaml.safe_load(split_front_matter(text))
            errs += check_version(label, meta, expected_version)
            errs += check_chinese_trigger(label, str(meta.get("description") or ""))
        if errs:
            failures += errs
            print(f"  ✗ {skill_md.parent.name}")
            for e in errs:
                print(f"      {e}")
        else:
            checked += 1
            print(f"  ✓ {skill_md.parent.name}")

    # 2) 运行时注册的 Skills（只校验 front matter 合法性）
    print("")
    print(".claude/skills/ (运行时注册 Skills)")
    runtime = sorted(RUNTIME_SKILLS_DIR.glob("*/SKILL.md")) if RUNTIME_SKILLS_DIR.exists() else []
    if not runtime:
        print("  - 无")
    for skill_md in runtime:
        label = f".claude/skills/{skill_md.parent.name}/SKILL.md"
        errs = check_front_matter(skill_md, read_text(skill_md), label)
        if errs:
            failures += errs
            print(f"  ✗ {skill_md.parent.name}")
            for e in errs:
                print(f"      {e}")
        else:
            checked += 1
            print(f"  ✓ {skill_md.parent.name}")

    # 3) 设计规格中的 yaml 代码块
    print("")
    print("docs/designs/skills/ (设计规格 yaml 代码块)")
    targets = sorted(DESIGN_SKILLS_DIR.glob("kflow-*.md"))
    if TEMPLATE_FILE.exists():
        targets.append(TEMPLATE_FILE)
    for path in targets:
        label = str(path.relative_to(ROOT)).replace("\\", "/")
        errs = check_design_yaml_blocks(path, label)
        if errs:
            failures += errs
            print(f"  ✗ {path.name}")
            for e in errs:
                print(f"      {e}")
        else:
            checked += 1
            print(f"  ✓ {path.name}")

    print("")
    print("=== 结果 ===")
    print(f"通过: {checked}, 失败: {len(failures)}")
    if placeholders_used:
        print("注: 模板文件中的 {占位符} 已在解析前替换为 PLACEHOLDER")
    if failures:
        print("状态: ✗ 存在校验失败项；非法 front matter 会导致 `npx skills add` 静默跳过对应 Skill")
        print("修复建议: 未加引号的 plain scalar 内禁止出现 ASCII \": \"，改用全角 \"：\" 或为其加引号")
        return 1
    print("状态: ✓ 所有 front matter 与设计规格 yaml 代码块合法")
    return 0


if __name__ == "__main__":
    sys.exit(main())
