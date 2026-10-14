# Spec Delta

## MODIFIED Requirements

### Requirement: 两级缺陷修复共享入口

系统 SHALL 通过单一 kflow-bug-fix Skill 入口支持子变更级和变更级两级缺陷修复，并在无测试阶段上下文时支持快车道模式。快车道模式 SHALL 由 `kflow-bug-triage` 的 L4 结论触发（见 `bugfix-fast-lane` 能力），SHALL NOT 提供其他入口。

#### Scenario: 上下文检测为子变更级

- **WHEN** 调用 kflow-bug-fix 且当前阶段为接口单元测试或 E2E 测试
- **THEN** 系统路由到子变更级缺陷修复流程
- **AND** 使用子变更级根因二分法

#### Scenario: 上下文检测为变更级

- **WHEN** 调用 kflow-bug-fix 且当前阶段为集成测试
- **THEN** 系统路由到变更级缺陷修复流程
- **AND** 使用变更级根因四分法

#### Scenario: 上下文无法判断

- **WHEN** 系统无法通过当前阶段判断级别
- **AND** 调用来源为 kflow-bug-triage 的 L4 路由
- **THEN** 系统 SHALL 进入快车道模式
- **AND** SHALL 使用子变更级根因二分法（实现错误 / 测试错误）

#### Scenario: 无 triage 结论时不进入快车道

- **WHEN** 系统无法通过当前阶段判断级别
- **AND** 调用来源不是 kflow-bug-triage 的 L4 路由
- **THEN** 系统 SHALL 询问用户确认调用上下文
- **AND** SHALL NOT 在未确认来源的情况下进入快车道模式

### Requirement: 多轮集成测试修复循环

系统 SHALL 支持集成测试失败后进入修复→重新集成测试的循环，直到全部通过。快车道模式 SHALL NOT 使用本循环——其验证为定向验证，由定向验证的重试上限约束，且有界。

#### Scenario: 单轮修复后重新测试

- **WHEN** 变更级根因分类为接口实现错误或测试用例错误
- **THEN** 修复完成后自动触发新一轮集成测试
- **AND** 产生新的测试轮次报告

#### Scenario: 多轮收敛

- **WHEN** 集成测试经过 N 轮修复后全部用例通过
- **THEN** 系统输出 summary.md 标记「集成测试通过」
- **AND** 记录总轮次数和修复历史

#### Scenario: 快车道模式不进入本循环

- **WHEN** 快车道缺陷完成修复
- **THEN** 系统 SHALL 执行定向验证而非全量集成测试
- **AND** SHALL NOT 触发集成测试轮次
- **AND** 验证结果 SHALL 写入缺陷级状态文件的定向验证区
