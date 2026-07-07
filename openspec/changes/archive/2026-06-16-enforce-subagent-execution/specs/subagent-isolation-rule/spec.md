## ADDED Requirements

### Requirement: 主 Agent 职责边界硬线声明

所有执行类阶段 SHALL 遵守主 Agent 职责边界硬线：主 Agent 的职责限定为调度（构建 prompt、启动子代理）和验收（检查产物、决定通过/拒收），SHALL NOT 直接执行任何阶段主工作（编码/修复/测试/审查/计划等），无例外。

#### Scenario: 主 Agent 直接执行阶段主工作

- **WHEN** 执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）的主工作需要执行
- **THEN** 主 Agent MUST 通过 Agent 子代理执行
- **AND** 主 Agent SHALL NOT 在主 Agent 上下文中直接编写代码、修复缺陷、运行测试、执行审查、生成计划等
- **AND** 此规则无例外——即使子代理多次失败，主 Agent 也不得接管执行

#### Scenario: 主 Agent 允许的工作

- **WHEN** 主 Agent 在执行类阶段中工作
- **THEN** 主 Agent MAY 执行以下调度和验收工作：构建子代理 prompt、启动 Agent 子代理、读取产物文件检查验收标准、更新 .status.md 状态、使用 AskUserQuestion 与用户交互
- **AND** 主 Agent SHALL NOT 将上述允许工作延伸为执行阶段主工作

### Requirement: 轮次级重试机制

子代理重试粒度 SHALL 为轮次级：当某轮子代理异常崩溃时，主 Agent SHALL 新建 Agent 重跑该轮（从当前轮次号继续），而非重启整个阶段或让主 Agent 接管。

#### Scenario: 子代理某轮崩溃

- **WHEN** 某轮（第 N 轮）的 Agent 子代理意外停止、报错退出、或返回不完整结果
- **THEN** 主 Agent MUST 重新创建新的 Agent 子代理
- **AND** 新子代理的 prompt 包含前 N-1 轮的轮间摘要（如有）
- **AND** 新子代理从第 N 轮继续执行（.status.md 执行轮次计数器保持为 N）
- **AND** 主 Agent SHALL NOT 在主 Agent 上下文中接管该轮工作

#### Scenario: 轮次级重试上限

- **WHEN** 同一轮次的子代理连续崩溃
- **THEN** 主 Agent MAY 最多重试 3 次（即最多创建 4 个子代理：1 次初始 + 3 次重试）
- **AND** 3 次重试均失败后，主 Agent MUST 标记该阶段为 ⚠️ 阻塞并提示用户
- **AND** 主 Agent SHALL NOT 在重试次数耗尽后接管执行

### Requirement: 各 SKILL.md 内联子代理强制规则框

所有 7 个执行类阶段的 SKILL.md SHALL 在重复制执行流程章节前新增独立的「子代理强制规则」引用框，确保规则在执行时直接可见。

#### Scenario: SKILL.md 规则框内容

- **WHEN** 读取执行类阶段的 SKILL.md
- **THEN** SHALL 在重复制执行流程章节前包含引用框
- **AND** 引用框包含以下三条规则：(1) 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收；(2) 主 Agent SHALL NOT 直接执行本阶段主工作，无例外；(3) 子代理崩溃 → 新建 Agent 重跑该轮（≤3 次重试），全部失败标记 ⚠️ 阻塞
- **AND** 引用框注明"参见 kflow-shared/repetition-model.md §12"

#### Scenario: 适用阶段清单

- **WHEN** 以下执行类阶段的 SKILL.md 被更新
- **THEN** kflow-plan SHALL 包含规则框
- **AND** kflow-code SHALL 包含规则框
- **AND** kflow-code-review SHALL 包含规则框
- **AND** kflow-api-test SHALL 包含规则框
- **AND** kflow-e2e-test SHALL 包含规则框
- **AND** kflow-integration-test SHALL 包含规则框
- **AND** kflow-bug-fix SHALL 包含规则框

## MODIFIED Requirements

### Requirement: 子代理异常时主代理禁止接管

系统 SHALL 在 `kflow-shared/repetition-model.md` §12 中定义全局强制规则：对于所有使用子代理（Agent subagent）开展工作的任务，如果子代理意外停止、报错退出、返回要求重做或继续做，主代理 MUST 重新创建新的子代理继续执行，SHALL NOT 接管子代理的工作直接开始执行。对于执行类阶段，重试粒度为轮次级——新建 Agent 重跑崩溃轮次，最多重试 3 次，全部失败标记阻塞。

#### Scenario: 子代理报错退出

- **WHEN** 子代理在执行过程中报错退出
- **THEN** 主代理 MUST 分析错误原因
- **AND** 调整子代理 prompt（如需要）后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 对于执行类阶段，新子代理从崩溃轮次继续执行

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

子代理隔离规则 SHALL 适用于所有阶段的所有子代理调用场景，包括：SELFREV 审查、VERIFY 验证、DESIGN 原型生成、四视角交叉审查、Agent 迭代执行。执行类阶段额外适用主 Agent 职责边界硬线（调度+验收，SHALL NOT 执行阶段主工作）和轮次级重试机制。

#### Scenario: 适用阶段清单

- **WHEN** 以下阶段使用子代理
- **THEN** kflow-explore（SELFREV）SHALL 遵守隔离规则
- **AND** kflow-prototype-design（DESIGN/VERIFY/SELFREV）SHALL 遵守隔离规则
- **AND** kflow-design（SELFREV/四视角审查）SHALL 遵守隔离规则
- **AND** kflow-plan（重复制/SELFREV）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-code（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-code-review（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-api-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-e2e-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-integration-test（重复制）SHALL 遵守隔离规则 + 子代理强制规则
- **AND** kflow-bug-fix（重复制）SHALL 遵守隔离规则 + 子代理强制规则
