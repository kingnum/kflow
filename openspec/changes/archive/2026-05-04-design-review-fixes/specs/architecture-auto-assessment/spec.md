# architecture-auto-assessment

## ADDED Requirements

### Requirement: 架构评估自动触发

系统 SHALL 在集成测试中连续 3 轮同一测试用例 ID 失败时自动触发架构评估。

#### Scenario: 自动触发条件
- **WHEN** 同一测试用例 ID 在连续 3 轮集成测试中均标记为失败
- **THEN** 系统自动启动架构评估 Agent
- **AND** 暂停当前修复循环
- **AND** 无需用户手动干预即可启动评估

#### Scenario: 失败计数追踪
- **WHEN** 集成测试轮次报告输出
- **THEN** 系统按测试用例 ID 追踪失败次数
- **AND** 同一用例 ID 连续失败次数记录在测试轮次报告中

#### Scenario: 失败计数重置
- **WHEN** 任一条件满足：该用例 ID 在某轮通过、或 `detailed-design.md` 中相关接口契约被修订、或用户手动重置
- **THEN** 该用例 ID 的失败计数器归零

### Requirement: 架构评估证据收集

系统 SHALL 自动收集架构评估所需的所有证据。

#### Scenario: 证据收集范围
- **WHEN** 架构评估启动
- **THEN** 系统收集以下证据：
  - 3 轮失败用例的完整详情（预期 vs 实际、错误日志、堆栈追踪）
  - 关联的接口契约定义（从 `detailed-design.md` 中提取）
  - 受影响的子变更列表及其依赖关系
  - 已尝试的修复方案及每次修复的结果

### Requirement: 架构评估分析输出

系统 SHALL 自动完成分析并输出多方案报告。

#### Scenario: 根因深挖
- **WHEN** 证据收集完成
- **THEN** 系统判断问题定性为以下之一：架构层面设计缺陷、接口契约根本性矛盾、技术选型不当、其他
- **AND** 给出判断依据

#### Scenario: 多方案输出
- **WHEN** 根因分析完成
- **THEN** 系统输出 ≥2 个可选改造方案：
  - 方案 A（推荐方案）：完整改造方案 + 改动量估算 + 风险评估
  - 方案 B（最小改动方案）：局部修复方案 + 局限性说明 + 风险
- **AND** 每个方案包含：改动涉及的设计域、受影响子变更、预期工作量、建议实施顺序

#### Scenario: 报告输出格式
- **WHEN** 方案生成完成
- **THEN** 系统输出 `test-reports/integration/fix-reports/arch-assessment-{timestamp}.md`
- **AND** 报告包含：问题定性、影响范围、方案对比、推荐建议

### Requirement: 用户决策交互

系统 SHALL 在输出架构评估报告后等待用户决策，不自动执行改造。

#### Scenario: 用户选择方案
- **WHEN** 架构评估报告输出完成
- **THEN** 系统使用 AskUserQuestion 展示方案选项
- **AND** 用户可选择方案 A、方案 B 或自定义方案
- **AND** 用户确认后系统执行选定方案

#### Scenario: 用户拒绝改造
- **WHEN** 用户认为不需要架构级改造
- **THEN** 系统记录用户决策
- **AND** 用户提供替代方向
- **AND** 按替代方向继续

#### Scenario: 架构评估误报
- **WHEN** 用户判断为误报（非架构问题）
- **THEN** 系统记录误报原因
- **AND** 重置失败计数器
- **AND** 返回正常修复循环
