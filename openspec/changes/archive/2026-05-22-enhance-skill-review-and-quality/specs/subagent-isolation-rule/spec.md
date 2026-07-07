## ADDED Requirements

### Requirement: 子代理异常时主代理禁止接管

系统 SHALL 在 core-mechanisms.md 中定义全局强制规则：对于所有使用子代理（Agent subagent）开展工作的任务，如果子代理意外停止、报错退出、返回要求重做或继续做，主代理 MUST 重新创建新的子代理继续执行，SHALL NOT 接管子代理的工作直接开始执行。

#### Scenario: 子代理报错退出

- **WHEN** 子代理在执行过程中报错退出
- **THEN** 主代理 MUST 分析错误原因
- **AND** 调整子代理 prompt（如需要）后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作

#### Scenario: 子代理返回要求重做

- **WHEN** 子代理返回结果要求 "需要重新执行" 或 "请继续完成"
- **THEN** 主代理 MUST 创建新的子代理（新的独立上下文）
- **AND** 新子代理的 prompt 包含上一轮子代理的上下文和未完成的工作说明
- **AND** SHALL NOT 在主 Agent 上下文中直接继续

#### Scenario: 子代理要求继续做

- **WHEN** 子代理因上下文限制返回 "已完成部分工作，需继续"
- **THEN** 主代理 MUST 创建新的子代理继续剩余工作
- **AND** 新子代理应获得之前完成的工作摘要作为起点
- **AND** SHALL NOT 在主 Agent 上下文中从断点继续

### Requirement: 隔离规则适用范围

子代理隔离规则 SHALL 适用于所有阶段的所有子代理调用场景，包括：SELFREV 审查、VERIFY 验证、DESIGN 原型生成、四视角交叉审查、Agent 迭代执行。

#### Scenario: 适用阶段清单

- **WHEN** 以下阶段使用子代理
- **THEN** kflow-explore（SELFREV）SHALL 遵守
- **AND** kflow-prototype-design（DESIGN/VERIFY/SELFREV）SHALL 遵守
- **AND** kflow-design（SELFREV/四视角审查）SHALL 遵守
- **AND** kflow-plan（Agent 迭代/SELFREV）SHALL 遵守
- **AND** kflow-code（多 Agent 并行编码）SHALL 遵守

### Requirement: 各 Skill SKILL.md 中标注引用

所有使用子代理的 Skill SHALL 在其 SKILL.md 的相关步骤中标注引用子代理隔离规则。

#### Scenario: 步骤级标注

- **WHEN** Skill 的某步骤使用子代理
- **THEN** 该步骤的描述中 SHALL 包含对 core-mechanisms.md 隔离规则的引用
- **AND** 标注形式为 "SHALL 遵守 core-mechanisms.md 子代理隔离规则：异常时重新创建子代理，主代理不得接管"
