# Spec Delta

## MODIFIED Requirements

### Requirement: 自审由子代理串行执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段的 SELFREV 步骤强制使用子代理（Agent subagent）执行自审，每轮启动独立子代理，N 轮顺序执行（N 由 design-review-tiering 决定：explore/prototype/design 三阶段首次创建固定 10 轮、非首次创建弹性轮次下限 1 轮；kflow-plan 维持 10 轮）。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。

#### Scenario: 子代理启动
- **WHEN** 阶段产物初稿生成完毕，进入 SELFREV 步骤
- **THEN** 主 Agent 启动第一轮子代理（Agent subagent）
- **AND** 子代理接收该阶段的产物文件路径和审查维度规则作为输入
- **AND** 子代理拥有独立上下文，不共享主 Agent 的对话历史

#### Scenario: 串行执行 10 轮
- **WHEN** 第 N 轮子代理完成并返回审查报告
- **THEN** 主 Agent 读取审查报告和修复后的产物
- **AND** 主 Agent 确认修复内容后启动第 N+1 轮子代理
- **AND** SHALL NOT 同时启动多个子代理（禁止并行）
- **AND** 必须完成全部目标轮次（首次创建 10 轮、非首次创建弹性轮次）后方可进入下一流程

#### Scenario: 子代理异常时主代理禁止接管（新增）
- **WHEN** 子代理意外停止、报错退出或返回要求重做/继续
- **THEN** 主代理 MUST 分析原因后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 新子代理的 prompt 包含上一轮的上下文和未完成的工作说明
