# Spec Delta

## MODIFIED Requirements

### Requirement: 主 Agent 职责边界硬线声明

所有执行类阶段 SHALL 遵守主 Agent 职责边界硬线：主 Agent 的职责限定为调度（构建 prompt、启动子代理）和验收（检查产物、决定通过/拒收），SHALL NOT 直接执行任何阶段主工作（编码/修复/测试/审查/计划等），无例外。此规则适用于所有入口场景，包括直接触发、triage 路由和其他 Skill 调用。该硬线 SHALL 由 `main-agent-execution-gating` 能力提供的工具级门控强制实施，SHALL NOT 仅依赖 SKILL.md 中的声明性约束。

#### Scenario: 主 Agent 直接执行阶段主工作

- **WHEN** 执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）的主工作需要执行
- **THEN** 主 Agent MUST 通过 Agent 子代理执行
- **AND** 主 Agent SHALL NOT 在主 Agent 上下文中直接编写代码、修复缺陷、运行测试、执行审查、生成计划等
- **AND** 此规则无例外——即使子代理多次失败，主 Agent 也不得接管执行

#### Scenario: 主 Agent 允许的工作

- **WHEN** 主 Agent 在执行类阶段中工作
- **THEN** 主 Agent MAY 执行以下调度和验收工作：构建子代理 prompt、启动 Agent 子代理、读取产物文件检查验收标准、更新 .status.md 状态、使用 AskUserQuestion 与用户交互
- **AND** 主 Agent SHALL NOT 将上述允许工作延伸为执行阶段主工作

#### Scenario: Triage 路由场景下的硬线适用

- **WHEN** kflow-bug-triage 路由到 kflow-bug-fix（L4 路由）
- **THEN** kflow-bug-fix 的主 Agent SHALL 遵守职责边界硬线
- **AND** SHALL NOT 因 triage 上下文而直接执行修复工作
- **AND** MUST 通过子代理执行修复主工作

#### Scenario: 硬线由工具级门控强制实施

- **WHEN** 执行类阶段的主 Agent 尝试调用 `Edit` / `Write` 写入非白名单路径，或调用长输出构建与测试命令
- **THEN** 该调用 SHALL 被工具级门控拒绝
- **AND** 门控拒绝 SHALL NOT 被视为流程阻塞，主 Agent SHALL 转而创建子代理执行

#### Scenario: 硬线遵守情况可审计

- **WHEN** 审计阶段核验执行类阶段的主 Agent 职责边界遵守情况
- **THEN** 审计 SHALL 以门控拒绝记录与主 Agent 的工具调用分布为依据
- **AND** 发现主 Agent 承担了阶段主工作时 SHALL 记录为发现项

#### Scenario: 设计类阶段不适用本硬线

- **WHEN** 阶段为 explore / prototype-design / design
- **THEN** 主 Agent 的产物写作职责 SHALL 不受本硬线约束
- **AND** 这些阶段的自审机制 SHALL 按既有规定执行
