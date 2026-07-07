## Why

设计文档存在四处不一致和冗余问题：

1. **CLAUDE.md 阶段数错误**：标注"前后端 7 阶段 / 纯后端 5 阶段"，实际设计文档和所有 Skill 均定义为"前后端 11 阶段 / 纯后端 9 阶段"。这是外部读者看到的第一个信息，传播错误数据。
2. **CLAUDE.md 工作流链缺失 4 个阶段**：省略了 `kflow-code-review`、`kflow-api-test`、`kflow-integration-test`、`kflow-audit`，导致工作流描述不完整。
3. **`core-mechanisms.md` 过长**：单文件 2235 行，包含大量模板级示例代码，远超舒适阅读上限。
4. **设计文档版本号不同步**：kflow-explore/design/code 的设计文档版本低于运行时 SKILL.md 版本。
5. **运行时 Skill 引用设计态文档**：5 个运行时 Skill（9 处引用）通过外链引用 `core-mechanisms.md` 的规则内容，运行时不应依赖设计态文档。
6. **`references/` 目录冗余**：100MB 的历史参考资料（gstack/huashu-design/ui-ux-pro 等 15 个子目录），设计文档无引用，仅 CLAUDE.md 中引用了 3 个子目录（kflow-skills/superpowers-extracted/rules），其余均为初始化时的参考项目，设计已完成不再需要。
7. **临时工作区未清理**：`.claude/worktrees/` 1.1GB（8 个 locked agent worktree）、`evals-workspace/` 248K、`mattpocock-skills-main/` 300K，均为 agent 历史遗留，无当前用途。

本次变更仅做文档整理和一致性修复，不引入新功能。

## What Changes

- 修复 CLAUDE.md 中的阶段数（7/5 → 11/9）和工作流链（补全缺失 4 个阶段）
- 将 `core-mechanisms.md`（2235 行）拆分为 8 个文件，原文件改为 index.md 导航
- 5 个运行时 Skill（9 处引用）内联规则，删除对设计态文档的外链（方案 B：运行时自包含）
- 同步 kflow-explore/design/code 设计文档版本号与运行时 SKILL.md 一致
- 检查并同步这 3 个 Skill 的设计文档内容与运行时 SKILL.md 的差异
- 删除 `references/` 目录（全部 15 个子目录，~100MB），同步清理 CLAUDE.md 中的引用
- 删除 `evals-workspace/`、`mattpocock-skills-main/`、`.claude/worktrees/`（~1.1GB）

## Capabilities

### New Capabilities
<!-- 无新能力，纯文档整理 -->

### Modified Capabilities
<!-- 无规格级行为变更，仅文档一致性修复 -->

## Impact

- `CLAUDE.md`：阶段数和工作流链修正
- `docs/designs/core-mechanisms.md`：拆分为 `core-mechanisms/` 目录（8 文件）
- `docs/designs/core-mechanisms.md`：改为 `core-mechanisms/index.md` 导航页
- `docs/designs/skills/kflow-explore.md`：版本号同步 + 内容对齐
- `docs/designs/skills/kflow-design.md`：版本号同步 + 内容对齐
- `docs/designs/skills/kflow-code.md`：版本号同步 + 内容对齐
- `.claude/skills/` 下 5 个 Skill 的 `core-mechanisms.md` 引用改为内联规则（不再外链）
- `references/`：整个目录删除（~100MB，15 个子目录）
- `CLAUDE.md`：删除 `references/` 项目结构描述（第 39-47 行）和"当前运营中的 Skills"段落（第 52-63 行）
- `evals-workspace/`、`mattpocock-skills-main/`、`.claude/worktrees/`：删除临时工作区（~1.1GB）
