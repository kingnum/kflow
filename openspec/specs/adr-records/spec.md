## Requirements

### Requirement: ADR 三条件过滤

系统 SHALL 在 kflow-design 阶段对架构决策进行评估，仅当三项条件全部满足时创建 ADR。

#### Scenario: 三条件全部满足

- **WHEN** kflow-design 阶段产生架构决策且满足：1) 难以逆转（改变决策的成本有意义），2) 缺少上下文会奇怪（未来读者会问"为什么这么做？"），3) 真正做了权衡（存在真实替代方案，选了其中一个有具体理由）
- **THEN** 系统 SHALL 创建 ADR 文件到 `docs/adr/{序号}-{标题}.md`

#### Scenario: 条件不满足

- **WHEN** 架构决策不满足三条件中任一条件
- **THEN** 系统 SHALL 跳过 ADR 创建
- **AND** 决策记录在设计文档 `detailed-design.md` 中即可

### Requirement: ADR 文件格式

每个 ADR SHALL 遵循 grill-with-docs 的 ADR-FORMAT.md 格式，包含过期条件标注。

#### Scenario: ADR 文件结构

- **WHEN** 系统创建 ADR 文件
- **THEN** ADR SHALL 包含：日期、状态、**过期条件**、背景、决策、后果、替代方案
- **AND** 过期条件 SHALL 明确说明何时应重新评估此决策（如"数据量 < 10GB 持续 6 个月 → 重新评估"或"团队规模 > 20 人 → 重新评估微服务拆分"）

### Requirement: ADR 每变更上限

系统 SHALL 按变更粒度控制 ADR 创建数量上限。

#### Scenario: 上限控制

- **WHEN** kflow-design 阶段创建 ADR
- **THEN** 功能需求级变更 SHALL 不超过 2 个 ADR
- **AND** 产品级变更 SHALL 不超过 5 个 ADR
- **AND** 功能缺陷级变更通常不创建 ADR
- **AND** 超出上限时 SHALL 提示用户变更粒度过大，建议拆分

### Requirement: ADR 序号管理

系统 SHALL 按项目级递增序号管理 ADR 文件。

#### Scenario: ADR 序号分配

- **WHEN** 创建新 ADR 文件
- **THEN** 文件名 SHALL 为 `{4位递增序号}-{kebab-case标题}.md`（如 `0003-choose-redis-cluster.md`）
- **AND** 序号 SHALL 从 `docs/adr/` 目录现有最大序号 +1 计算

### Requirement: ADR 索引文件

系统 SHALL 维护 `docs/adr/index.md` 作为所有 ADR 的索引。

#### Scenario: 索引自动更新

- **WHEN** ADR 被创建、状态变更或废弃
- **THEN** 系统 SHALL 更新 `docs/adr/index.md`
- **AND** 索引 SHALL 包含：ADR 序号、标题、创建日期、状态、涉及变更
