# Spec Delta

## MODIFIED Requirements

### Requirement: 隔离规则适用范围

子代理隔离规则 SHALL 适用于所有阶段的所有子代理调用场景，包括：SELFREV 审查、VERIFY 验证、DESIGN 原型生成、四视角交叉审查、Agent 迭代执行、审计评估与轻量自检。执行类阶段额外适用主 Agent 职责边界硬线（调度+验收，SHALL NOT 执行阶段主工作）和轮次级重试机制。审计阶段适用隔离规则与 3 次重试上限，但不适用轮次级重试粒度（审计为单次执行，无轮次概念）。

#### Scenario: 适用阶段清单

- **WHEN** 以下阶段使用子代理
- **THEN** kflow-explore（SELFREV）SHALL 遵守隔离规则
- **AND** kflow-prototype-design（DESIGN/VERIFY/SELFREV）SHALL 遵守隔离规则
- **AND** kflow-design（SELFREV/四视角审查）SHALL 遵守隔离规则
- **AND** kflow-audit（审计评估/轻量自检）SHALL 遵守隔离规则
- **AND** kflow-plan（重复制/SELFREV）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-code（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-code-review（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-api-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-e2e-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-integration-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-bug-fix（重复制）SHALL 遵守隔离规则 + 子代理强制规则

#### Scenario: 审计阶段的规则适用子集

- **WHEN** 审计子代理意外停止、报错退出或返回不完整结果
- **THEN** 主 Agent MUST 重新创建新的审计子代理执行审计
- **AND** SHALL NOT 在主 Agent 上下文中接管审计工作
- **AND** 重试上限 SHALL 为最多 3 次，全部失败后标记 ⚠️ 阻塞并提示用户
- **AND** SHALL NOT 适用轮次级重试粒度（审计为单次执行，无轮次概念）
- **AND** SHALL NOT 适用主 Agent 职责边界硬线（审计非执行类阶段）
