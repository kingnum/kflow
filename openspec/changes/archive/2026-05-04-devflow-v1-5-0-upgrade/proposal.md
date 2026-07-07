## Why

DevFlow Skills 体系（v1.4.0）在核心流程上已完整，但缺少两个关键闭环——**使用评估**和**环境初始化**。同时现有机制存在三个缺口：集成测试缺少多轮缺陷修复循环、归档未将设计成果合并到产品级、文件命名和大文档管理缺乏规范。本次升级补齐这些缺口，实现从"启动→执行→评估→合并"的完整闭环。

## What Changes

### 新增 Skills
- **`kflow-audit`**：使用情况评估 Skill，在归档前自动触发（归档门控），也支持随时手动调用。评估维度包括流程合规性、产物完整性、审查质量、测试充分性、缺陷管理、效率指标。审计未通过时按问题归属阶段回退。
- **`kflow-init`**：环境初始化 Skill，发现当前上下文可用能力（MCP servers + Skills），评估组合可行性并输出推荐方案（原型阶段首选 pencil MCP，E2E 阶段首选 /playwright-cli skill），输出 `toolchain.md` 到项目级。

### 现有 Skill 增强
- **`kflow-bug-fix`**：扩展为**单 Skill + 两级内部上下文检测**。子变更级保持现有根因三分法；新增变更级根因四分法（接口实现/接口契约/集成测试用例/架构设计），报告路径新增 `test-reports/integration/fix-reports/`。共享根因分类引擎、多 Agent 并行分析、回退门控逻辑。
- **`kflow-archive`**：归档时合并功能设计（`functional-design.md`）和详细设计（`detailed-design.md`）到产品级文档（`docs/designs/domains/{domain}.md` + 全景文档），原型设计保留在变更级不合并。每个章节标注来源变更和归档时间。

### 文件命名优化（**BREAKING**）
- `design-explore.md` → `functional-design.md`
- `design.md` → `detailed-design.md`

### 大文档管理策略
- 产品级文档：从一开始即多文件拆分（`index.md` + `domains/*.md` + 全景文档），`changelog.md` 按年归档
- 变更级文档：功能点 ≤30 单文件，>30 拆分为多文件 + 索引入口

### 目录结构更新
- 新增 `docs/designs/domains/` 存放按设计域拆分的产品级设计文档
- 变更级新增 `test-reports/integration/fix-reports/` 存放集成测试缺陷修复报告
- 回退触发来源新增第 4 种：`kflow-audit` 审计发现

## Capabilities

### New Capabilities
- `devflow-audit`: 使用情况评估——归档前自动触发审计门控，支持手动调用，六维度评估（流程合规性、产物完整性、审查质量、测试充分性、缺陷管理、效率指标），审计未通过按问题归属阶段回退
- `devflow-init`: 环境初始化——发现当前上下文可用 MCP servers 和 Skills，评估组合可行性，输出工具链推荐方案和 toolchain.md
- `change-level-bug-fix`: 变更级缺陷修复——与子变更级共享同一 Skill，内部上下文检测区分级别，变更级根因四分法，集成测试多轮修复循环
- `archive-design-merge`: 归档设计合并——归档时将变更级功能设计和详细设计合并到产品级文档，按设计域组织，标注来源变更和归档时间，支持冲突检测
- `doc-naming-convention`: 文件命名规范——functional-design.md（功能设计）和 detailed-design.md（详细设计）双层命名体系
- `doc-split-strategy`: 大文档拆分策略——产品级从一开始多文件拆分，变更级按功能点数量决定拆分方式

### Modified Capabilities
- `devflow-archive`: 归档流程新增设计合并步骤——从单纯文件移动升级为"合并设计 + 移动文件 + 更新索引"三合一
- `defect-root-cause`: 根因分类从子变更级三分法扩展为支持变更级四分法，新增接口契约错误类型
- `integration-testing`: 集成测试新增多轮缺陷修复循环——集成测试失败后进入变更级 bug-fix，修复后重新集成测试，循环直到通过
- `change-rollback`: 回退触发来源新增第 4 种——`kflow-audit` 审计发现，与现有三种（缺陷修复、代码审查、用户需求变更）并列

## Impact

- **设计文档**：`docs/designs/index.md`（版本号 → 1.5.0）、`overview.md`（Skills 清单更新）、`core-mechanisms.md`（新增审计门控、变更级 bug-fix、设计合并、回退来源、目录结构）、`skills/index.md`（新增 2 个 Skill 条目）、`skills/kflow-bug-fix.md`（扩展为两级）、`skills/kflow-archive.md`（新增合并流程）
- **新增设计文档**：`skills/kflow-audit.md`、`skills/kflow-init.md`
- **新增示例**：审计报告示例、toolchain 示例、集成测试修复报告示例、产品级领域文档示例
- **Breaking**：现有变更目录中的 `design-explore.md` 和 `design.md` 需按新命名规范迁移（提供兼容期处理）
