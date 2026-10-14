# Spec Delta

## ADDED Requirements

### Requirement: 导航合理性验证轮次（纯收敛驱动）

系统 SHALL 在审查方式为「子代理自动审查验证」且 BUILD 四项静态检查全部通过后，执行**不预设轮数、纯收敛驱动**的导航合理性验证，每轮启动一个独立子代理执行全部 5 项检查；达成收敛终止条件（最近一轮为满足全部四项判据的见证轮）时 SHALL 终止，SHALL NOT 预置轮数上限。审查方式为「人工审查」时，系统 SHALL NOT 执行导航合理性验证。

#### Scenario: 前置条件满足时进入导航验证

- **WHEN** BUILD 四项静态检查全部通过且用户选择的审查方式为「子代理自动审查验证」
- **THEN** 系统 SHALL 进入导航合理性验证（9.1 节）
- **AND** 系统 SHALL 启动串行子代理验证，轮数由收敛决定，SHALL NOT 预置轮数上限

#### Scenario: 人工审查路径跳过导航验证

- **WHEN** 用户选择的审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 执行导航合理性验证
- **AND** SHALL NOT 启动导航验证子代理
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）

#### Scenario: 每轮子代理启动

- **WHEN** 进入导航合理性验证（9.1 节）
- **THEN** 系统 SHALL 串行启动子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 Playwright 或文件分析执行全部 5 项导航合理性检查
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题
- **AND** 修复完成后 SHALL 启动下一轮子代理

#### Scenario: 见证轮达成即终止为收敛

- **WHEN** 导航验证执行中，最近一轮同时满足零新发现、零修复、报告证明 5 项检查已完成全量遍历、且累积未复核修复清单内全部条目逐项复核通过
- **THEN** 系统 SHALL 终止导航验证
- **AND** 终止结果 SHALL 记录为 `收敛`

#### Scenario: 未达成见证轮则继续下一轮

- **WHEN** 最近一轮存在新发现、或存在修复、或未证明 5 项检查全量遍历、或累积未复核修复清单内存在未通过复核的条目
- **THEN** 系统 SHALL 继续下一轮
- **AND** SHALL NOT 因轮次数量而终止
- **AND** SHALL NOT 以任何轮数上限作为终止依据

#### Scenario: 不收敛时终止为未收敛

- **WHEN** 导航验证命中不收敛判定（无进展 / 振荡 / 安全丝）
- **THEN** 系统 SHALL 终止导航验证
- **AND** 终止结果 SHALL 记录为 `未收敛`
- **AND** 系统 SHALL 进入非收敛分支升级用户

### Requirement: 导航验证报告内容与存放

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出

- **WHEN** 子代理完成一轮导航验证
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/nav-check/round-{N}.md`（N 为收敛实际轮次）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、发现问题和建议修复

#### Scenario: 主 Agent 读取和处理

- **WHEN** 子代理报告写入完成
- **THEN** 主 Agent SHALL 从 `self-reviews/prototype/nav-check/round-{N}.md` 读取报告
- **AND** 对发现的问题 SHALL 直接修复原型文件
- **AND** 修复完成后 SHALL 进入下一轮

### Requirement: 导航验证适用审查范围冻结与范围外观察

导航合理性验证 SHALL 适用审查范围冻结：每轮审查对象集合 SHALL 由主 Agent 在该轮开始时从原型阶段既有产物生成并冻结，审查维度 SHALL 限于该轮固定的 5 项导航合理性检查。子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增检查维度、SHALL NOT 借审查之名新增功能点、字段、章节或分支。子代理在冻结范围之外发现的问题 SHALL 降级为「**范围外观察**」——SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛，并 SHALL 写入该轮审查报告的「范围外观察」小节，由主 Agent 在阶段终止时汇总提示。某轮引入范围外新内容时该轮 SHALL NOT 被判定为见证轮。

#### Scenario: 审查对象集合按轮冻结

- **WHEN** 主 Agent 构建某轮导航验证子代理的 prompt
- **THEN** prompt SHALL 包含由原型阶段既有产物生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件、代码或内容
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 范围外发现降级为范围外观察

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** 系统 SHALL NOT 修改任何原型产物
- **AND** SHALL NOT 将该问题计入本轮新发现数
- **AND** SHALL NOT 阻断收敛
- **AND** SHALL 将其写入该轮审查报告的「范围外观察」小节

#### Scenario: 范围外发现不计入发现数

- **WHEN** 某轮仅存在范围外发现而无范围内新发现
- **THEN** 本轮的新发现数 SHALL 记为 0
- **AND** 该轮 MAY 构成见证轮（其余三项条件同时满足时）

#### Scenario: 引入范围外新内容的轮次不得判为见证轮

- **WHEN** 某轮的新发现或修改落在冻结的审查对象集合之外
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 主 Agent SHALL 拒收该轮
- **AND** SHALL 要求子代理在冻结范围内重新审查该轮

## REMOVED Requirements

### Requirement: 导航合理性验证轮次（收敛驱动）

**Reason**: 原需求以「不少于 1 轮、不超过 5 轮」的轮次上限与终止点复检轮为终止依据；轮次上限与复检轮废除后，该上限与复检轮相关场景（收敛或达上限终止 / 终止点清单非空时追加复检轮 / 复检轮通过后终止 / 复检轮未通过后终止）均不可达。

**Migration**: 迁移至同能力新增的「导航合理性验证轮次（纯收敛驱动）」Requirement——不预设轮数，收敛（见证轮）为唯一成功终止条件，不收敛时按 `convergence-driven-repetition` 的不收敛判定升级用户。每轮执行全部 5 项检查、子代理串行、人工审查时跳过等规定原样保留。

### Requirement: 导航验证报告

**Reason**: 原需求含「复检轮报告输出」场景，复检轮废除后该场景不可达。

**Migration**: 迁移至同能力新增的「导航验证报告内容与存放」Requirement——`round-{N}.md` 的 N 为收敛实际轮次（不再限于 1–5），不再产出复检轮报告。
