## Why

当前 KFlow Skills 体系中约 35 种阶段产物文件，其中 48% 完全缺失模板定义，12% 仅有部分模板。阶段产出的格式全靠 Skill 执行时自由发挥，导致同类产物的结构、深度、完整性严重不一致。特别是 `functional-design.md`（每个变更的入口文档）核心骨架缺失，在实施过程中因功能定义不清晰引发大量返工。需要建立统一的模板体系，确保所有阶段产物有明确、详细、可执行的结构定义。

## What Changes

- **新建模板目录 `docs/designs/templates/`**：按 change / subchange / integration / product / infra 五级组织，每个独立文件产物对应一个模板文件，从各 Skill spec 中抽出现有内联模板
- **补全 17 个完全缺失的模板**（api-tests.md、e2e-tests.md、四视角独立审查报告、design-error 报告、contract-error 报告、全景文档等）
- **补全 functional-design.md 核心骨架**（功能行为矩阵、业务规则表、交互约束表）— 纯功能视角，不包含数据需求/接口需求
- **4 组大型文档引入按量拆分机制**（≤30/分册）：functional-designs/、api-tests/、e2e-tests/、integration-tests/，每组分册 + 统一 index.md 索引文件
- **索引文件标准化**：index.md 具备可读性，列出关键信息不丢失（如 e2e-tests/index 列出每个功能点的覆盖场景和验证类型）
- **Skill spec 引用更新**：14 个 Skill spec 中将内联模板替换为模板文件引用，消除重复定义
- **目录结构调整**：functional-design.md → functional-designs/；api-tests.md → api-tests/；e2e-tests.md → e2e-tests/；integration-tests.md → integration-tests/

## Capabilities

### New Capabilities
- `stage-doc-templates`: 模板目录组织结构（templates/index.md）、模板命名规范、模板与 Skill spec 的引用关系、模板维护规则
- `large-doc-splitting`: 4 组文档按量拆分机制（≤30/分册）、分册模板格式、index.md 索引模板格式、拆分触发条件

### Modified Capabilities
- `doc-naming-convention`: functional-design.md 改为 functional-designs/ 目录；api-tests.md、e2e-tests.md、integration-tests.md 均改为独立目录结构
- `doc-split-strategy`: 新增按数量拆分策略（≤30 规则），作为现有按功能点拆分（≤30）的补充
- `design-level-restructure`: 功能设计文档目录化（functional-designs/），索引文件列出全部功能点及依赖关系

## Impact

- **新建文件**：`docs/designs/templates/` 目录及 35+ 模板文件（含 4 组拆分文档的 index.md + part-NN.md 模板）
- **修改文件**：14 个 Skill spec（`docs/designs/skills/kflow-*.md`）— 内联模板替换为模板引用
- **更新文件**：`docs/designs/core-mechanisms.md` — 目录结构章节更新、命名规范更新、拆分策略章节补充
- **更新文件**：`docs/designs/index.md` — 新增模板目录索引入口
- **运行态影响**：后续变更的产物目录结构变化（如 functional-designs/ 替代 functional-design.md）
