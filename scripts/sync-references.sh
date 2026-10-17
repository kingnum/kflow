#!/bin/bash
# 从权威源生成切片副本 + 校验一致性
# 用法: ./scripts/sync-references.sh
#
# ── 职责（两段式）──────────────────────────────────────────────────
#   ① 生成段 从 references-src/ 下的权威源，按 references-src/slice-manifest.tsv
#            的切片规则，为每个 skill 生成 skills/<skill>/references/<文件>
#   ② 校验段 归一化比对生成物与权威源对应的阶段切片，不一致时非零退出并定位差异
#
# 实现在 scripts/sync_references.py（本脚本为入口包装）。切片引擎用 Python 而非 awk：
# gawk 在部分 locale 下对多字节字符的正则匹配与数组下标语义不可靠（章节标题含中文顿号、
# 全数字章节号与 strnum 作数值等价），Python 可稳定处理。
#
# ── 权威源与切片清单 ──────────────────────────────────────────────
#   references-src/<文件>                   权威源（开发期单一维护点）
#   references-src/slice-manifest.tsv       切片清单：<源文件><TAB><skill><TAB><sections>
#
#   清单由 scripts/gen-slice-manifest.py 生成。清单中的 `~N:LO-HI` 行区间取自权威源的绝对
#   行号；修改权威源后 SHALL 重新运行生成器刷新行号，再运行本脚本生成切片。
#
# ── 切片语义 ─────────────────────────────────────────────────────
#   文件头部（首个一级章节标题之前的内容）为全局元信息，任何切片均保留。
#   一级章节以行首的 `## <编号>. ` 或 `## <中文序号>、` 起始（如 `## 13. 轮间摘要传递机制`、
#   `## 一、with_server.py`）。该模式有意排除代码块内的二级标题（如 repetition.md 的
#   `## 轮间摘要 (Round {N-1} 完成后)`），使其留在所属章节内。中文序号在匹配时归一为
#   阿拉伯数字，故清单与模式统一使用后者。
#
# ── sections 指令语法（逗号分隔，按出现顺序处理）──────────────────
#     N            保留整节 N
#     -N           排除整节 N（在基础集合之上剔除）
#     N:a:b        在节 N 内仅保留子节 a 与 b（节标题与节首引言保留）
#     ~N:LO-HI[+LO-HI]  用权威源的行区间（1-based，含端点；多段以 + 连接）替换节 N 的正文
#     ^N:KEY       在节 N 的表格内仅保留含文本 KEY 的数据行（表头与分隔行保留）
#
# ── skill 路径处理 ────────────────────────────────────────────────
#   权威源中以 `skills/<SKILL>/` 占位符承载「指向本 skill 自身目录」的路径；生成时按目标
#   skill 替换为具体名称。跨 skill 的固定引用（如 repetition.md 引用 kflow-init 的
#   permission-model.md）在各副本中本就一致，不构成实质差异，故校验前将两侧的
#   skills/<skill 名>/ 路径段统一归一化为 skills/<SKILL>/ 再比对。
#
# ── 退出状态 ─────────────────────────────────────────────────────
#   0  生成完成且全部一致
#   1  存在与权威源不一致的副本
#   2  清单或权威源缺失

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if command -v python &> /dev/null; then
  PYTHON_BIN="python"
elif command -v python3 &> /dev/null; then
  PYTHON_BIN="python3"
else
  echo "错误: 未找到 python，无法执行 references 切片"
  exit 2
fi

exec "$PYTHON_BIN" "$REPO_ROOT/scripts/sync_references.py" "$@"
