## ADDED Requirements

### Requirement: Vertical Slice 强制

leadl-code 的 TDD 循环 SHALL 采用垂直切片（vertical slice）方式，每次只实现一个完整的端到端行为切片（schema → logic → API → test），而非按层水平切片。

#### Scenario: Tracer Bullet 先行

- **WHEN** 开始新子变更的 TDD 编码
- **THEN** 第一个 RED→GREEN 循环 SHALL 是一个 tracer bullet——证明端到端路径可用的最简实现
- **AND** tracer bullet 必须横切所有集成层

#### Scenario: 逐切片增量

- **WHEN** tracer bullet 已通过
- **THEN** 每个后续 RED→GREEN 循环 SHALL 基于前一切片的产出增量添加
- **AND** 每次 SHALL 只写一个测试 → 一个实现

### Requirement: 水平切片反模式警告

系统 SHALL 检测并拒绝水平切片（先写所有测试再写所有代码）的 TDD 反模式。

#### Scenario: 检测水平切片

- **WHEN** Agent 尝试一次性编写多个测试（>1）而不进行中间实现
- **THEN** 系统 SHALL 警告："水平切片会导致测试假想行为而非实际行为，重构时这些测试会不可靠"
- **AND** 阻止批量测试编写，引导回到一次一个测试的方式

### Requirement: 测试行为而非实现

所有测试 SHALL 通过公共接口验证系统行为，不耦合实现细节。

#### Scenario: 测试质量检查

- **WHEN** 编写测试用例
- **THEN** 测试 SHALL 描述系统做什么（行为），而非怎么做（实现）
- **AND** 如果内部重构（不改行为）导致测试失败，系统 SHALL 标记为"测试与实现耦合"

#### Scenario: Mock 使用约束

- **WHEN** 需要使用 mock
- **THEN** mock SHALL 仅用于外部边界（数据库、外部服务）
- **AND** 禁止 mock 内部 collaborator 或测试私有方法

### Requirement: 每周期检查清单

每个 TDD 周期完成后，系统 SHALL 自检以下清单：

#### Scenario: RED 阶段检查

- **WHEN** 测试处于 RED 状态（测试已写，待确认失败）
- **THEN** 系统 SHALL 确认：
  - 测试描述行为而非实现
  - 测试使用公共接口
  - 如果内部重构，此测试不应失败

#### Scenario: GREEN 阶段检查

- **WHEN** 实现代码已完成且测试通过
- **THEN** 系统 SHALL 确认：
  - 代码最小——仅满足当前测试
  - 无投机性功能
  - 无提前优化

#### Scenario: REFACTOR 阶段检查

- **WHEN** 所有测试通过后进入 REFACTOR
- **THEN** 系统 SHALL 确认：
  - 消除重复
  - 模块是否可以深化（小接口 + 深实现 = 高 leverage）
  - 每次重构后运行所有测试
  - 禁止在 RED 状态重构

### Requirement: TDD 哲学文档化

leadl-code 的 SKILL.md 或对应设计文档 SHALL 包含 TDD 哲学说明，明确正确和错误的 TDD 模式。

#### Scenario: 哲学内容

- **WHEN** 阅读 kflow-code 的 TDD 章节
- **THEN** 内容 SHALL 包含：
  - 核心原则：测试验证行为通过公共接口
  - 好测试 vs 坏测试的定义和示例
  - 水平切片反模式示意图
  - Vertical slice CORRECT 示意图
  - 每周期检查清单
