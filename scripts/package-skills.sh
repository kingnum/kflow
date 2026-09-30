#!/bin/bash
# 打包 KFlow Skills 为可分发的 zip 包
# 用法: ./scripts/package-skills.sh <change-name>
# 示例: ./scripts/package-skills.sh skill-packaging-and-version-unification

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# Skills 源目录：KFlow Skills 的实现产物位于 skills/，
# .claude/skills/ 存放的是运行时注册的工具链 Skill（skill-creator 等），不是打包对象
SKILLS_DIR="$REPO_ROOT/skills"
TARGETS_DIR="$REPO_ROOT/targets"
VERSION_FILE="$REPO_ROOT/VERSION"
CHANGE_NAME="${1:-unknown-change}"

# 从 VERSION 文件读取版本
if [ ! -f "$VERSION_FILE" ]; then
  echo "错误: 未找到 VERSION 文件 ($VERSION_FILE)"
  exit 1
fi

VERSION=$(head -1 "$VERSION_FILE" | tr -d '[:space:]')
if [ -z "$VERSION" ]; then
  echo "错误: 无法从 VERSION 文件读取版本号"
  exit 1
fi
BUILD_TIME=$(date '+%Y-%m-%d %H:%M')
PACKAGE_NAME="kflow-devflow-skills-$VERSION"
ZIP_FILE="$TARGETS_DIR/$PACKAGE_NAME.zip"
WORK_DIR="$TARGETS_DIR/.work-$PACKAGE_NAME-$$"

echo "=== KFlow Skills 打包 ==="
echo "版本: $VERSION"
echo "构建时间: $BUILD_TIME"
echo "变更: $CHANGE_NAME"
echo ""

# Front matter 校验（阻断式）
# 非法 front matter 会导致 `npx skills add` 静默跳过对应 Skill（不报错、不提示），
# 使安装数量少于实际 Skill 数量，故必须在打包前拦截。
echo "=== Front Matter 校验 ==="
if command -v python &> /dev/null; then
  PYTHON_BIN="python"
elif command -v python3 &> /dev/null; then
  PYTHON_BIN="python3"
else
  echo "错误: 未找到 python，无法执行 front matter 校验"
  exit 1
fi
if ! "$PYTHON_BIN" "$REPO_ROOT/scripts/validate-frontmatter.py"; then
  echo ""
  echo "错误: front matter 校验未通过，终止打包"
  exit 1
fi
echo ""

# 清理可能的残留工作目录
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR/$PACKAGE_NAME"
mkdir -p "$TARGETS_DIR"

# 生成 VERSION.txt
cat > "$WORK_DIR/$PACKAGE_NAME/VERSION.txt" <<EOF
version: $VERSION
build_time: $BUILD_TIME
change: $CHANGE_NAME
EOF

# 路径替换表达式: skills/kflow-*/ → .claude/skills/kflow-*/
# 替换目标为任意 kflow-* 名称而非仅当前 Skill，以覆盖跨 Skill 引用
# （如 kflow-api-test 的 references 引用 kflow-code 的脚本路径）；
# 前置字符断言 [^./] 避免对已带 .claude/ 前缀的路径重复加前缀。
REWRITE_EXPR="s|^skills/\(kflow-[a-z0-9-]*\)/|.claude/skills/\1/|g; s|\([^./]\)skills/\(kflow-[a-z0-9-]*\)/|\1.claude/skills/\2/|g"

# 扫描并复制 Skills
SKILL_COUNT=0
echo "扫描 $SKILLS_DIR/kflow-* ..."
for skill_dir in "$SKILLS_DIR"/kflow-*/; do
  skill_name=$(basename "$skill_dir")
  # 通配符未匹配时会展开为字面量 "kflow-*"，须跳过，
  # 否则它会被计入 SKILL_COUNT 并产出空包（且使版本校验守卫失准）
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    continue
  fi
  echo "  打包: $skill_name"

  # 创建目标目录
  mkdir -p "$WORK_DIR/$PACKAGE_NAME/$skill_name/references"

  # 复制 SKILL.md
  if [ -f "$skill_dir/SKILL.md" ]; then
    cp "$skill_dir/SKILL.md" "$WORK_DIR/$PACKAGE_NAME/$skill_name/SKILL.md"
  fi

  # 复制 references/ 目录
  if [ -d "$skill_dir/references" ] && [ "$(ls -A "$skill_dir/references" 2>/dev/null)" ]; then
    cp -r "$skill_dir/references/"* "$WORK_DIR/$PACKAGE_NAME/$skill_name/references/"
  fi

  # 复制 scripts/ 目录（如有）
  if [ -d "$skill_dir/scripts" ] && [ "$(ls -A "$skill_dir/scripts" 2>/dev/null)" ]; then
    mkdir -p "$WORK_DIR/$PACKAGE_NAME/$skill_name/scripts"
    cp -r "$skill_dir/scripts/"* "$WORK_DIR/$PACKAGE_NAME/$skill_name/scripts/"
  fi

  # 路径替换: skills/kflow-*/ → .claude/skills/kflow-*/
  # Markdown 与脚本文件（*.py）中的示例路径一并处理
  find "$WORK_DIR/$PACKAGE_NAME/$skill_name" \( -name "*.md" -o -name "*.py" \) | while read -r doc_file; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "$REWRITE_EXPR" "$doc_file"
    else
      sed -i "$REWRITE_EXPR" "$doc_file"
    fi
  done

  SKILL_COUNT=$((SKILL_COUNT + 1))
done

echo ""
echo "共打包 $SKILL_COUNT 个 Skills"

# 防空包：源目录不存在或路径写错时，kflow-*/ 通配符不展开，脚本会静默产出
# 只含字面量目录名 "kflow-*" 的空包，故必须显式拦截
if [ "$SKILL_COUNT" -eq 0 ]; then
  echo "错误: 未扫描到任何 Skills（$SKILLS_DIR 下无 kflow-*/SKILL.md）"
  rm -rf "$WORK_DIR"
  exit 1
fi

# 版本一致性校验
echo ""
echo "=== 版本一致性校验 ==="
VERSION_MISMATCH=0
VERSION_CHECKED=0
for skill_md in "$WORK_DIR/$PACKAGE_NAME"/kflow-*/SKILL.md; do
  if [ ! -f "$skill_md" ]; then
    continue
  fi
  VERSION_CHECKED=$((VERSION_CHECKED + 1))
  skill_name=$(basename "$(dirname "$skill_md")")
  md_version=$(grep '^version:' "$skill_md" | head -1 | sed 's/^version:[[:space:]]*//' | tr -d '[:space:]')
  if [ "$md_version" != "$VERSION" ]; then
    echo "  ✗ $skill_name: version=$md_version (期望 $VERSION)"
    VERSION_MISMATCH=$((VERSION_MISMATCH + 1))
  fi
done
if [ "$VERSION_MISMATCH" -gt 0 ]; then
  echo "错误: $VERSION_MISMATCH 个 SKILL.md version 与 VERSION 不一致"
  rm -rf "$WORK_DIR"
  exit 1
fi
# 防空跑：通配符未匹配时循环体不执行，会得出「全部一致」的假结论
if [ "$VERSION_CHECKED" -ne "$SKILL_COUNT" ]; then
  echo "错误: 仅校验到 $VERSION_CHECKED 个 SKILL.md，与打包数 $SKILL_COUNT 不符"
  rm -rf "$WORK_DIR"
  exit 1
fi
echo "  ✓ $VERSION_CHECKED 个 SKILL.md version 与 VERSION ($VERSION) 一致"

# 打包为 zip
echo ""
echo "生成 $ZIP_FILE ..."
cd "$WORK_DIR"

# 检测可用打包工具
if command -v tar &> /dev/null; then
  # tar 方式（Git Bash / Linux / macOS 通用）
  tar -czf "$ZIP_FILE" "$PACKAGE_NAME/" 2>/dev/null || {
    # tar.gz 备选方案
    echo "tar -czf 失败，尝试 tar -cf + gzip ..."
    tar -cf "$ZIP_FILE.tar" "$PACKAGE_NAME/"
    gzip -f "$ZIP_FILE.tar"
    mv "$ZIP_FILE.tar.gz" "$ZIP_FILE" 2>/dev/null || true
  }
elif command -v zip &> /dev/null; then
  zip -r "$ZIP_FILE" "$PACKAGE_NAME/"
elif command -v powershell.exe &> /dev/null; then
  # Windows PowerShell 备选
  powershell.exe -NoProfile -Command "Compress-Archive -Path '$PACKAGE_NAME' -DestinationPath '$ZIP_FILE' -Force"
else
  echo "错误: 未找到可用的打包工具（tar/zip/Compress-Archive）"
  rm -rf "$WORK_DIR"
  exit 1
fi

# 清理工作目录
rm -rf "$WORK_DIR"

echo ""
echo "=== 打包完成 ==="
echo "产物: $ZIP_FILE"
echo "版本: $VERSION"
ls -lh "$ZIP_FILE" 2>/dev/null || echo "文件大小: $(stat -f%z "$ZIP_FILE" 2>/dev/null || stat -c%s "$ZIP_FILE" 2>/dev/null || echo 'unknown') bytes"
