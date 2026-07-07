## Why

手动测试 `/kflow-init` 过程中发现产品级文档体系存在三处缺陷：CONTEXT.md 路径与核心机制定义不一致、产品级文档结构与变更级不对齐导致归档合并困难、老项目初始化缺少 service-guide.md。这些问题阻碍了文档驱动的阶段门控机制正常运转，需要系统修复。

## What Changes

- **BREAKING** CONTEXT.md 路径：从项目根目录修正为 `docs/CONTEXT.md`，与 `core-mechanisms.md` 权威定义一致
- **BREAKING** 产品级设计文档结构重组：`docs/designs/domains/{domain}.md` → `docs/designs/functional-designs/{module}.md`，按功能模块拆分，与变更级 `functional-designs/part-NN.md` 章节结构保持一致
- **BREAKING** 新增 `docs/designs/technical-designs/` 目录，收纳 `architecture.md`、`data-model.md`、`api-catalog.md`、`nfr-baseline.md`，与变更级 `detailed-design.md` 内容维度对齐
- kflow-init LEGACY 步骤新增 `docs/service-guide.md` 为第 7 类输出，产品文档检测从 7 项扩展为 8 项
- kflow-archive MERGE 步骤定义去草稿规则：首次合并时替换「由 AI 逆向分析生成」→ 正式来源标注
- 模板目录重组：`templates/change/`、`templates/product/` 等抽象分层 → 镜像实际 `docs/` 输出结构

## Capabilities

### New Capabilities
<!-- No new capabilities — this change fixes existing ones -->

### Modified Capabilities
- `devflow-init`: CONTEXT.md 路径修正、LEGACY 输出扩展为 7 类（含 service-guide.md）、产品文档检测 7→8 项、生成文档结构对齐新模板
- `archive-design-merge`: 合并目标路径 domains/{domain}.md → functional-designs/{module}.md、新增去草稿规则
- `stage-doc-templates`: 模板目录结构重组为镜像 docs/ 结构
- `doc-naming-convention`: domains/ 目录命名 → functional-designs/ + technical-designs/，domain 概念 → module 概念
- `domain-glossary`: CONTEXT.md 路径引用从项目根目录 → docs/
- `service-guide-generation`: init 可预生成初步 service-guide.md（标记草稿），kflow-code 为其补充多环境配置
- `multi-environment-config`: service-guide.md 产出 Skill 从仅 kflow-code 扩展为 kflow-init（预生成）+ kflow-code（补充完善）

## Impact

- 受影响设计文档：`core-mechanisms.md`、`kflow-init.md`、`kflow-archive.md`、`kflow-code.md`、`overview.md`、`templates/index.md`
- 受影响 SKILL 实现：`kflow-init/SKILL.md`、`kflow-archive/SKILL.md`
- 受影响模板文件：`product/domain-doc.md` 重命名/重构、`product/` 目录重组
- 已有产品文档需从 `docs/designs/domains/` 迁移到 `docs/designs/functional-designs/`
- 已有 CONTEXT.md 需从项目根目录迁移到 `docs/CONTEXT.md`
