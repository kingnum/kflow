# design-doc-directory Specification

## Purpose
TBD - created by archiving change enhance-skill-review-and-quality. Update Purpose after archive.
## Requirements
### Requirement: FP 阈值触发目录化拆分

系统 SHALL 在变更功能点总数 > 20 时，将 detailed-design.md 单文件强制拆分为 `detailed-design/` 目录结构。

#### Scenario: FP > 20 强制拆分

- **WHEN** kflow-design 阶段开始时，FP 总数 > 20
- **THEN** 系统 SHALL 创建 `detailed-design/` 目录（替代 detailed-design.md 单文件）
- **AND** 目录包含 6 个组成部分：index.md + architecture.md + domains/*.md + nfr.md + config-and-errors.md + subchange-division.md

#### Scenario: FP ≤ 20 保持单文件

- **WHEN** FP 总数 ≤ 20
- **THEN** 系统 SHALL 保持 detailed-design.md 单文件模式
- **AND** 单文件内容结构与目录结构等效（所有章节在同一文件中）

### Requirement: 目录结构规范

`detailed-design/` 目录 SHALL 包含以下 6 部分文件。

#### Scenario: 目录文件清单

- **WHEN** `detailed-design/` 目录被创建
- **THEN** 必须包含 `index.md`（索引入口、设计概述、目录索引、FP 覆盖表、复杂度分布表）
- **AND** 必须包含 `architecture.md`（系统架构、技术选型、模块划分、ADR 索引）
- **AND** 必须包含 `domains/` 子目录（按设计域命名的 .md 文件）
- **AND** 必须包含 `nfr.md`（非功能需求：性能/安全/可用性/可维护性）
- **AND** 必须包含 `config-and-errors.md`（配置项设计 + 错误处理设计）
- **AND** 必须包含 `subchange-division.md`（子变更划分方案、HITL/AFK 分类、实现顺序）

#### Scenario: 设计域文件命名

- **WHEN** 设计域文件被创建
- **THEN** 文件存放于 `domains/` 子目录下
- **AND** 文件名使用设计域英文名（kebab-case），如 `auth.md`、`business.md`、`infrastructure.md`
- **AND** 每个设计域文件包含该域的功能点设计表、数据模型、接口设计、跨子变更契约

### Requirement: index.md 索引模板

当 detailed-design.md 拆分为目录结构时，index.md SHALL 使用以下模板格式。

#### Scenario: index.md 标准结构

- **WHEN** `detailed-design/index.md` 被创建
- **THEN** 必须包含文件头部元信息（版本号、生成时间、变更名称）
- **AND** 必须包含 "设计文档目录" 表格（文档名、文件链接、说明）
- **AND** 必须包含 "设计域清单" 表格（设计域、文件链接、功能点数、涉及子变更）
- **AND** 必须包含 "功能点 → 设计文档映射" 表格（FP ID、名称、所属设计域、设计文档章节链接）
- **AND** 必须包含 "复杂度分布" 表格（复杂度等级、数量、涉及 FP 列表）

#### Scenario: index.md 格式示例

- **WHEN** kflow-design 生成 index.md
- **THEN** 格式如下：
  - `# 详细设计索引：{change-name}`
  - 元信息区（版本/时间/变更名称）
  - 设计文档目录表（| 文档 | 文件 | 说明 |）
  - 设计域清单表（| 设计域 | 文件 | 功能点数 | 涉及子变更 |）
  - FP 映射表（| 功能点ID | 功能点名称 | 所属设计域 | 设计文档章节 |）
  - 复杂度分布表（| 复杂度 | 数量 | 涉及 FP |）

### Requirement: 门控检查适配目录结构

阶段门控和下游阶段读取 SHALL 适配 `detailed-design/` 目录结构。

#### Scenario: 门控检查适配

- **WHEN** kflow-plan 门控检查 "detailed-design.md 存在"
- **THEN** 改为检查 `detailed-design/index.md` 或 `detailed-design.md` 任一存在
- **AND** 优先检查 `detailed-design/index.md`（目录结构），其次 `detailed-design.md`（单文件）

#### Scenario: kflow-plan 读取设计文档

- **WHEN** kflow-plan 读取详细设计文档
- **THEN** 若存在 `detailed-design/index.md` → 通过索引定位到对应的 domains/*.md
- **AND** 若存在 `detailed-design.md` → 直接读取单文件
- **AND** 读取行为对两种结构透明，不影响任务拆分逻辑

