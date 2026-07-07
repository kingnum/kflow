# subchange-phase-unification Specification

## Purpose
Defines the subchange phase unification (5 phases) with per-round batch sync and the E2E test skill rename.

## Requirements
### Requirement: 子变更阶段统一为 5 阶段

系统 SHALL 将子变更的阶段列表统一为 5 个阶段：计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试（kflow-e2e-test）。前后端项目执行全部 5 阶段，纯后端项目跳过 E2E测试。测试阶段包含「等待变更级同步」状态，确保子变更在每轮测试间批量同步。

#### Scenario: 前后端项目子变更阶段
- **WHEN** 项目类型为前后端项目
- **THEN** 子变更阶段依次为：计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试（kflow-e2e-test）
- **AND** 所有 5 个阶段均需执行

#### Scenario: 纯后端项目子变更阶段
- **WHEN** 项目类型为纯后端项目
- **THEN** 子变更阶段依次为：计划 → 编码 → 代码审查 → 接口单元测试
- **AND** E2E测试阶段标记为 ⏭️ 跳过

#### Scenario: 子变更测试阶段的批量同步状态
- **WHEN** 子变更完成当前轮次 E2E 测试或接口单元测试
- **THEN** 如其他子变更仍在执行或修复中，该子变更进入「等待变更级同步」状态
- **AND** 状态标记为 ⏸️ 等待同步
- **AND** 不自行推进到下一轮

#### Scenario: 等待同步后进入下一轮
- **WHEN** 变更级 agent 完成服务编译重启并通知进入下一轮
- **THEN** 子变更从「⏸️ 等待同步」转为「🔄 进行中」
- **AND** 开始执行 Round N+1 测试

### Requirement: 子变更状态文件格式更新

系统 SHALL 在子变更 .status.md 中支持「⏸️ 等待同步」状态值，并在 `## 基本信息` 区维护 `**执行轮次**` 字段。

#### Scenario: 子变更状态表格
- **WHEN** 子变更 .status.md 创建或更新
- **THEN** 阶段状态表格按项目类型包含对应阶段行
- **AND** 状态值支持：✅ 完成 / 🔄 进行中 / ⏳ 待开始 / ⏭️ 跳过 / ❌ 阻塞 / ⚠️ 需修订 / ⏸️ 等待同步

#### Scenario: 基本信息区包含执行轮次
- **WHEN** 子变更 .status.md 进入执行类阶段
- **THEN** `## 基本信息` 区 MUST 包含 `**执行轮次**: {N} / 10` 字段
- **AND** 该字段位于 `**当前阶段**` 之后、`**执行类型**` 同级区域

#### Scenario: 等待同步状态的使用场景
- **WHEN** 子变更完成当前测试轮次且通过，但其他子变更尚未完成
- **THEN** 该子变更的测试阶段状态标记为「⏸️ 等待同步」
- **AND** 执行记录中注明「等待变更级 Round N+1 同步启动」

### Requirement: 变更级子变更进度矩阵

系统 SHALL 在变更级 .status.md 中使用阶段完成矩阵展示子变更的各阶段状态，支持⏸️等待同步状态。

#### Scenario: 子变更进度矩阵格式
- **WHEN** 变更级 .status.md 显示子变更进度
- **THEN** 使用矩阵格式展示每个子变更在各阶段的完成状态
- **AND** 每个子变更一行，每个阶段一列（✅ 🔄 ⏳ ⏭️ ❌ ⚠️ ⏸️）
- **AND** E2E测试列标题显示为「kflow-e2e-test」

### Requirement: E2E 测试 Skill 名称重命名

系统 SHALL 将 E2E 测试阶段 Skill 名称从 `kflow-e2e-qa` 重命名为 `kflow-e2e-test`。

#### Scenario: Skill 名称使用新名称
- **WHEN** E2E 测试阶段被调度
- **THEN** 系统使用 `kflow-e2e-test` 作为 Skill 名称
- **AND** 不再使用 `kflow-e2e-qa`

#### Scenario: 状态文件中引用新名称
- **WHEN** 变更级或子变更级 .status.md 引用 E2E 测试阶段
- **THEN** 阶段名称显示为「E2E测试」或「kflow-e2e-test」
