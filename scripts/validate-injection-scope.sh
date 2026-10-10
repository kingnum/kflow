#!/bin/bash
# 校验 kflow-init 注入消费方 CLAUDE.md 的模板内容的作用域
# 用法: ./scripts/validate-injection-scope.sh
#
# 校验对象:
#   skills/kflow-init/SKILL.md 步骤 11（INJECT）中标注为 ```markdown 的注入模板块
#
# 黑名单词汇（技能开发仓库特有，消费方项目中不存在或不可执行）:
#   scripts/sync-version.sh, scripts/package-skills.sh, targets/, VERSION 文件, README 版本条目
#
# 退出状态:
#   0  校验通过
#   1  命中黑名单词汇
#   2  未提取到任何注入模板块（空集判为失败，避免"无输入即通过"的假阴性）

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$REPO_ROOT/skills/kflow-init/SKILL.md"

BLACKLIST=(
  'scripts/sync-version\.sh'
  'scripts/package-skills\.sh'
  'targets/'
  'VERSION 文件'
  'README.*版本'
)

if [ ! -f "$SKILL_FILE" ]; then
  echo "错误: 未找到注入模板载体 $SKILL_FILE"
  exit 2
fi

# 提取步骤 11 中的 ```markdown 代码块，输出格式: 模板块序号<TAB>SKILL.md 行号<TAB>行内容
# 末尾附加 TOTAL 记录，用于空集保护
# 注: 模板块内部含 ```markdown 的 `## ` 标题行（如 `## 项目画像`），故二级标题只在
#     「不在模板块内」时才作为 section 边界
EXTRACT="$(mktemp)"
trap 'rm -f "$EXTRACT"' EXIT

awk '
  !in_block && /^## / {
    if ($0 ~ /^## 步骤 11/) in_section = 1
    else in_section = 0
    next
  }
  in_section && !in_block && $0 ~ /^```markdown[[:space:]]*$/ { in_block = 1; blocks++; next }
  in_section && in_block && $0 ~ /^```[[:space:]]*$/ { in_block = 0; next }
  in_section && in_block { print blocks "\t" NR "\t" $0 }
  END { print "TOTAL\t" blocks + 0 }
' "$SKILL_FILE" > "$EXTRACT"

BLOCK_COUNT=$(awk -F'\t' '$1 == "TOTAL" { print $2 }' "$EXTRACT")

echo "=== 注入模板作用域校验 ==="
echo ""
echo "校验对象: skills/kflow-init/SKILL.md（步骤 11 INJECT 的注入模板块）"
echo "校验模板块数: $BLOCK_COUNT"
echo ""

# 空集保护: 未提取到任何模板块时不判为通过
if [ "$BLOCK_COUNT" -eq 0 ]; then
  echo "=== 结果 ==="
  echo "状态: ✗ 未提取到任何注入模板块，校验对象为空集，判为失败"
  echo "提示: 确认 $SKILL_FILE 的步骤 11 中注入模板仍以 \`\`\`markdown 代码块承载"
  exit 2
fi

HITS=0
while IFS=$'\t' read -r block lineno text; do
  [ "$block" = "TOTAL" ] && continue
  for pattern in "${BLACKLIST[@]}"; do
    if printf '%s\n' "$text" | grep -qE -- "$pattern"; then
      echo "  ✗ 命中开发态词汇 [${pattern}] — SKILL.md:${lineno}（模板块 ${block}）"
      echo "      | ${text}"
      HITS=$((HITS + 1))
      break
    fi
  done
done < "$EXTRACT"

echo ""
echo "=== 结果 ==="
echo "命中数: $HITS"
if [ "$HITS" -eq 0 ]; then
  echo "状态: ✓ 注入模板仅含消费态规则，未出现技能开发仓库特有词汇"
  exit 0
fi
echo "状态: ✗ 注入模板出现技能开发仓库特有的路径、脚本或流程词汇，请移除后再提交"
exit 1
