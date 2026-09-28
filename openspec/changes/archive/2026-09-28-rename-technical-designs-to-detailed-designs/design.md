# Design

## Context

本仓库是 KFlow Skills 的**开发仓库**，`docs/designs/` 描述的是 KFlow 在目标项目运行时生成的产物结构，而非本仓库自身的业务文档。因此本次重命名的对象分两类：

- **本仓库内需直接改动的文件**：模板目录 `docs/designs/templates/design-templates/technical-designs/`、`skills/kflow-archive/SKILL.md`、`skills/kflow-init/SKILL.md`、`docs/designs/` 下各设计文档、`openspec/specs/` 下 6 个现行规格。
- **目标项目的产物路径约定**：KFlow 在目标项目生成 `docs/designs/technical-designs/`，重命名后应生成 `docs/designs/detailed-designs/`。

当前术语状态：变更级产物为 `detailed-design.md`（单数），产品级对应目录为 `technical-designs/`（复数），二者指向同一类产物但命名分裂。

## Goals / Non-Goals

**Goals:**
- 统一「详细设计」术语：产品级目录 `technical-designs/` → `detailed-designs/`，中文术语「技术设计」同步归一为「详细设计」。
- 模板目录同步重命名，保持「模板路径 = 产物路径」的镜像关系。
- 对已安装 KFlow 的目标项目提供旧目录 `technical-designs/` 的兼容读取与迁移提示。

**Non-Goals:**
- 不改动 6 个文件的内部结构（architecture、data-model、api-catalog、nfr-baseline、config-items、error-handling 的章节内容不变）。
- 不改动归档历史 `openspec/changes/archive/` 中的任何文件。
- 不涉及变更级 `detailed-design.md` / `detailed-design/` 目录自身的命名（保持单数不变）。

## Decisions

### 决策 1：术语归一范围 —— 目录名与中文术语一并归一

将目录名 `technical-designs` 改为 `detailed-designs`，同时将规格与文档中的中文「技术设计」描述性术语改为「详细设计」。涉及 requirement 标题的（如「产品级技术设计文档目录化」）用 RENAMED + MODIFIED 表达，纯路径替换的用 MODIFIED。

- 边界：`#### Scenario:` 名是 openspec 的稳定标识，MODIFIED 中必须与现有 spec 精确匹配，不能随术语一并改名（改动会被判为「删旧增新」并拒绝归档）。因此 Scenario 名中的 `technical-designs`（如「产品级 technical-designs 目录」）保留为历史标识，仅其 WHEN/THEN/AND 内容归一。这已在 delta 中落实并通过 `openspec validate`。
- 备选：仅改目录名、保留「技术设计」中文术语 → 目录名与术语自相矛盾，弃用。

### 决策 2：复数命名 `detailed-designs`（而非单数 `detailed-design`）

产品级目录用复数 `detailed-designs`，与 `functional-designs` 对称，并表达「一个目录聚合多个详细设计文档」。变更级 `detailed-design.md` 是单文件故保持单数，单复数差异是自然的。

- 备选：单数 `detailed-design` 精确对齐变更级 → 但与产品级目录既有复数惯例不一致，弃用。

### 决策 3：旧目录兼容策略 —— 兼容读取 + 迁移提示，不自动重命名

对已安装 KFlow 的目标项目，`kflow-archive` / `kflow-init` 读取产品级详细设计文档时，若发现旧的 `docs/designs/technical-designs/` 而非 `detailed-designs/`，兼容读取旧目录并提示用户执行 `git mv` 迁移。不自动执行 `git mv`，避免在用户未确认时改动目标项目的目录结构。

- 备选 A：不兼容，仅认新目录 → 旧项目丢失产品级技术设计文档，破坏性大，弃用。
- 备选 B：自动 `git mv` 迁移 → 归档/init 是读多写少的阶段，自动改动目录有风险，弃用。

### 决策 4：实现方式 —— git mv + 全量文本替换

模板目录用 `git mv` 重命名，其余文件用精确文本替换 `technical-designs` → `detailed-designs`（以及中文「技术设计」→「详细设计」按上下文替换）。归档历史不动。

## Risks / Trade-offs

- [旧项目若无人执行 `git mv` 迁移，会长期停留在兼容读取态] → 兼容读取路径始终可用，迁移提示重复出现，不影响正确性。
- [全量文本替换可能误伤归档历史或无关引用] → 明确限定替换范围：现行 `skills/`、`docs/designs/`、`openspec/specs/`，排除 `openspec/changes/archive/`。
- [中文「技术设计」一词在其他无关语义中出现时被误改] → 只替换与产品级目录/文档直接关联的描述，上下文无关处保留。

## Migration Plan

1. `git mv docs/designs/templates/design-templates/technical-designs docs/designs/templates/design-templates/detailed-designs`。
2. 文本替换 `skills/`、`docs/designs/`、`openspec/specs/` 中的 `technical-designs` → `detailed-designs`，及关联中文术语。
3. 目标项目侧：skill 升级后，旧 `docs/designs/technical-designs/` 目录由兼容读取路径承接，提示用户 `git mv technical-designs detailed-designs`。
4. 回滚：反向 `git mv` + 反向文本替换即可，无数据丢失风险。

## Open Questions

无。
