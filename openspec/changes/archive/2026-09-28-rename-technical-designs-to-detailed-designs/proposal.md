# Proposal

## Why

KFlow 体系中「技术设计（technical-design）」与「详细设计（detailed-design）」两个术语指向同一类产物，造成术语分裂：变更级产物名为 `detailed-design.md`（单文件）或 `detailed-design/`（功能点 >20 时拆分），而产品级对应目录却叫 `technical-designs/`。归档时变更级 `detailed-design.md` 的内容正是被合并到产品级 `technical-designs/` 的 6 个文件，二者本质是同一事物的变更级/产品级两个称呼。重命名产品级目录为 `detailed-designs/`，统一术语、与变更级 `detailed-design` 概念对应，并与产品级既有的 `functional-designs/` 命名风格对称。

## What Changes

- 将产品级技术设计文档目录 `docs/designs/technical-designs/` 重命名为 `docs/designs/detailed-designs/`（6 文件：architecture、data-model、api-catalog、nfr-baseline、config-items、error-handling）。
- 将模板目录 `templates/design-templates/technical-designs/` 重命名为 `templates/design-templates/detailed-designs/`。
- 同步更新 `kflow-archive`、`kflow-init` 两个运行时 SKILL.md 中所有对 `technical-designs` 的引用。
- 同步更新设计文档（docs/designs/ 下 index、overview、core-mechanisms、skills、examples、templates）中的路径与术语引用。
- 为已安装运行的目标项目提供旧目录 `technical-designs/` 的兼容读取（见 design.md 决策），避免 skill 升级后旧项目丢失产品级技术设计文档。
- **BREAKING**：现有目标项目中已存在的 `docs/designs/technical-designs/` 目录路径失效，需迁移为 `detailed-designs/`。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `doc-naming-convention`: 「产品级技术设计文档目录化」Requirement 中目录名由 `technical-designs` 改为 `detailed-designs`，术语同步归一。
- `archive-design-merge`: 归档设计合并的目标目录路径由 `docs/designs/technical-designs/` 改为 `docs/designs/detailed-designs/`。
- `init-legacy-reverse-analysis`: 老项目逆向分析生成的 6 个技术设计草稿的写入路径由 `technical-designs/` 改为 `detailed-designs/`。
- `stage-doc-templates`: 技术设计模板的引用路径由 `templates/design-templates/technical-designs/` 改为 `templates/design-templates/detailed-designs/`。
- `product-config-items-doc`: 产品级配置项文档路径由 `technical-designs/config-items.md` 改为 `detailed-designs/config-items.md`。
- `product-error-handling-doc`: 产品级错误处理文档路径由 `technical-designs/error-handling.md` 改为 `detailed-designs/error-handling.md`。

## Impact

- 运行时 Skills：`skills/kflow-archive/SKILL.md`（10 处）、`skills/kflow-init/SKILL.md`（6 处）。
- 设计文档：`docs/designs/` 下 index.md、overview.md、core-mechanisms/02-directory-structure.md、skills/kflow-init.md、skills/kflow-archive.md、examples/product-design-index.md、templates/index.md。
- 模板目录：`docs/designs/templates/design-templates/technical-designs/`（6 个模板文件，目录整体重命名）。
- OpenSpec specs：上述 6 个现行 capability 的 spec 文件。
- 归档历史（`openspec/changes/archive/`）：不改动，保持历史记录原样。
