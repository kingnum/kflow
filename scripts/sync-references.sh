#!/bin/bash
# 校验同名 references 文件在多个 skill 间的差异，输出不一致报告
# 用法: ./scripts/sync-references.sh
#
# 检查的 references 文件列表:
#   repetition.md, hooks.md, gates.md, state-values.md, service-lifecycle.md, self-review.md
#
# skill 路径归一化:
#   各 skill 的副本中会引用 skill 目录路径，且引用的是「本副本对应的 skill」——
#   例如 repetition.md 引用本 skill 的 permission-model.md，service-lifecycle.md 引用
#   承载脚本的 kflow-code/scripts/with_server.py。这类路径差异由「副本归属哪个 skill」决定，
#   不构成实质不一致。比对前将各副本中的 skills/<skill 名>/ 路径段统一归一化为 skills/<SKILL>/，
#   再行比对；内容、规则、检查项的实质差异不受归一化影响，仍会正确报告。

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

# 归一化文件内容中的 skill 目录路径段
# 参数: $1=文件路径（$2 保留以兼容调用点，归一化不再依赖副本归属的 skill 名）
normalize_skill_refs() {
  sed 's#skills/kflow-[a-z0-9-]*/#skills/<SKILL>/#g' "$1"
}

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

      if ! diff -q <(normalize_skill_refs "$file_a") <(normalize_skill_refs "$file_b") > /dev/null 2>&1; then
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
