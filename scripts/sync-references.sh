#!/bin/bash
# 校验同名 references 文件在多个 skill 间的差异，输出不一致报告
# 用法: ./scripts/sync-references.sh
#
# 检查的 references 文件列表:
#   repetition.md, hooks.md, gates.md, state-values.md, service-lifecycle.md, self-review.md

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

# 需要校验的同名 references 文件
REF_FILES=(
  "repetition.md"
  "hooks.md"
  "gates.md"
  "state-values.md"
  "service-lifecycle.md"
  "self-review.md"
)

echo "=== References 一致性校验 ==="
echo ""

HAS_DIFF=0
TOTAL_CHECKS=0

for ref_file in "${REF_FILES[@]}"; do
  # 收集所有包含该 references 文件的 skill
  declare -a skill_dirs=()
  for skill_dir in "$SKILLS_DIR"/kflow-*/; do
    if [ -f "$skill_dir/references/$ref_file" ]; then
      skill_dirs+=("$skill_dir")
    fi
  done

  count=${#skill_dirs[@]}
  if [ "$count" -lt 2 ]; then
    echo "  - $ref_file: 仅 $count 个 skill 持有，跳过（无需对比）"
    continue
  fi

  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
  echo "  $ref_file: $count 个 skill 持有，对比中..."

  # 对比所有 pair
  declare -a mismatches=()
  for ((i=0; i<count; i++)); do
    for ((j=i+1; j<count; j++)); do
      skill_a=$(basename "${skill_dirs[$i]}")
      skill_b=$(basename "${skill_dirs[$j]}")
      file_a="${skill_dirs[$i]}references/$ref_file"
      file_b="${skill_dirs[$j]}references/$ref_file"

      if ! diff -q "$file_a" "$file_b" > /dev/null 2>&1; then
        mismatches+=("$skill_a ↔ $skill_b")
        HAS_DIFF=1
      fi
    done
  done

  if [ ${#mismatches[@]} -eq 0 ]; then
    echo "    ✓ 全部一致"
  else
    echo "    ✗ 不一致 ($count 个 skill):"
    for pair in "${mismatches[@]}"; do
      echo "      - $pair"
    done
  fi
  echo ""
done

echo "=== 结果 ==="
echo "检查项: $TOTAL_CHECKS"
if [ "$HAS_DIFF" -eq 0 ]; then
  echo "状态: ✓ 所有多 skill 共享的 references 文件一致"
else
  echo "状态: ✗ 存在不一致的 references 文件，请手动同步"
fi
