#!/bin/bash
# 同步版本号：从 VERSION 读取版本，批量更新所有 skills/kflow-*/SKILL.md front matter 中的 version 字段
# 用法: ./scripts/sync-version.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION_FILE="$REPO_ROOT/VERSION"
SKILLS_DIR="$REPO_ROOT/skills"

if [ ! -f "$VERSION_FILE" ]; then
  echo "错误: 未找到 VERSION 文件 ($VERSION_FILE)"
  exit 1
fi

VERSION=$(head -1 "$VERSION_FILE" | tr -d '[:space:]')
if [ -z "$VERSION" ]; then
  echo "错误: 无法从 VERSION 文件读取版本号"
  exit 1
fi

echo "=== 版本同步 ==="
echo "目标版本: $VERSION"
echo ""

UPDATED=0
SKIPPED=0
MISSING=0

for skill_md in "$SKILLS_DIR"/kflow-*/SKILL.md; do
  if [ ! -f "$skill_md" ]; then
    continue
  fi
  skill_name=$(basename "$(dirname "$skill_md")")

  # 检测 front matter 范围（第一个 --- 到第二个 ---）
  fm_end=$(grep -n '^---$' "$skill_md" | head -2 | tail -1 | cut -d: -f1 || echo "")

  if [ -z "$fm_end" ]; then
    echo "  ⚠ $skill_name: 未找到 front matter 结束标记，跳过"
    MISSING=$((MISSING + 1))
    continue
  fi

  # 在 front matter 范围内查找 version 字段
  version_abs_line=$(head -"$fm_end" "$skill_md" | grep -n '^version:' | head -1 | cut -d: -f1 || echo "")

  if [ -n "$version_abs_line" ]; then
    current_version=$(sed -n "${version_abs_line}s/^version:[[:space:]]*//p" "$skill_md" | tr -d '[:space:]' || echo "")
    if [ "$current_version" = "$VERSION" ]; then
      echo "  ✓ $skill_name: 已是 $VERSION"
      SKIPPED=$((SKIPPED + 1))
    else
      sed -i "${version_abs_line}s/^version:.*/version: $VERSION/" "$skill_md"
      echo "  ✓ $skill_name: $current_version → $VERSION"
      UPDATED=$((UPDATED + 1))
    fi
  else
    # version 字段不存在，在 name 行后插入
    name_abs_line=$(head -"$fm_end" "$skill_md" | grep -n '^name:' | head -1 | cut -d: -f1 || echo "")
    if [ -z "$name_abs_line" ]; then
      echo "  ⚠ $skill_name: 未找到 name 字段，跳过"
      MISSING=$((MISSING + 1))
      continue
    fi
    sed -i "${name_abs_line}a\\version: $VERSION" "$skill_md"
    echo "  + $skill_name: 新增 version: $VERSION"
    UPDATED=$((UPDATED + 1))
  fi
done

echo ""
echo "=== 完成 ==="
echo "更新: $UPDATED, 已同步: $SKIPPED, 异常: $MISSING"
