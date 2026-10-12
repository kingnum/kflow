# prototype-navigation-verification Specification

## Purpose

定义原型设计阶段 VERIFY 步骤中的导航合理性验证（9.1 节），子代理串行验证，轮次下限 1、上限 5，以见证轮收敛终止，每轮子代理完整执行全部 5 项检查；该验证仅在审查方式为「子代理自动审查验证」时执行。

## Requirements

### Requirement: 导航合理性验证轮次（收敛驱动）

系统 SHALL 在审查方式为「子代理自动审查验证」且 BUILD 四项静态检查全部通过后，执行**不少于 1 轮、不超过 5 轮**的导航合理性验证，每轮启动一个独立子代理执行全部 5 项检查；达成收敛终止条件（最近一轮为见证轮）时 SHALL 提前结束。到达终止点且累积未复核修复清单非空时，系统 SHALL 追加 1 轮复检轮，该轮 SHALL NOT 消耗 1–5 轮的轮次上限，且 SHALL 最多追加 1 轮。审查方式为「人工审查」时，系统 SHALL NOT 执行导航合理性验证，SHALL NOT 追加复检轮。

#### Scenario: 前置条件满足时进入导航验证

- **WHEN** BUILD 四项静态检查全部通过且用户选择的审查方式为「子代理自动审查验证」
- **THEN** 系统 SHALL 进入导航合理性验证（9.1 节）
- **AND** 系统 SHALL 启动串行子代理验证，轮次不少于 1 轮、不超过 5 轮

#### Scenario: 人工审查路径跳过导航验证

- **WHEN** 用户选择的审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 执行导航合理性验证
- **AND** SHALL NOT 启动导航验证子代理
- **AND** SHALL NOT 追加复检轮
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）

#### Scenario: 每轮子代理启动

- **WHEN** 进入导航合理性验证（9.1 节）
- **THEN** 系统 SHALL 串行启动子代理，每轮子代理类型为 `Agent(subagent_type="claude")`
- **AND** 每个子代理 SHALL 使用 Playwright 或文件分析执行全部 5 项导航合理性检查
- **AND** 每轮子代理完成后，主 Agent SHALL 读取其报告并修复发现问题
- **AND** 修复完成后 SHALL 启动下一轮子代理

#### Scenario: 收敛或达上限终止

- **WHEN** 导航验证执行中（审查方式为「子代理自动审查验证」）
- **THEN** 最近一轮为零新发现、零修复且报告证明 5 项检查已全量执行的见证轮时，系统 SHALL 终止验证
- **AND** 否则 SHALL 继续下一轮，直至达到轮次上限 5 轮
- **AND** SHALL NOT 因「必须完成全部 5 轮」而继续执行无增量价值的轮次

#### Scenario: 终止点清单非空时追加复检轮

- **WHEN** 导航验证到达终止点（最近一轮为见证轮，或已达到轮次上限 5 轮）
- **AND** 累积未复核修复清单非空
- **THEN** 系统 SHALL 追加 1 轮复检轮
- **AND** 该轮 SHALL NOT 计入 1–5 轮的轮次上限
- **AND** 该轮 SHALL 逐项复核清单内全部修复，并证明 5 项检查已完成全量遍历

#### Scenario: 复检轮通过后终止

- **WHEN** 复检轮零新发现、零修复、证明 5 项检查全量遍历且清单内全部修复逐项复核通过
- **THEN** 系统 SHALL 终止导航验证
- **AND** 终止原因 SHALL 记录为 `收敛（复检轮）`

#### Scenario: 复检轮未通过后终止

- **WHEN** 复检轮未满足通过判据
- **THEN** 系统 SHALL 终止导航验证
- **AND** 终止原因 SHALL 记录为 `达上限`
- **AND** 系统 SHALL 进入非收敛分支

### Requirement: 每轮导航验证检查项

每轮导航验证子代理 SHALL 执行以下全部 5 项检查。

#### Scenario: 页面可达性检查

- **WHEN** 子代理执行导航验证
- **THEN** 子代理 SHALL 从 `docs/designs/prototypes/index.html` 出发进行 BFS 遍历
- **AND** 遍历所有 `<a href>` 和导航组件引用
- **AND** 生成页面可达性矩阵
- **AND** 标记孤立页面（无任何入口链接指向）
- **AND** 标记死胡同页面（无任何出口链接）

#### Scenario: 返回/取消按钮合理性检查

- **WHEN** 子代理执行导航验证
- **THEN** 子代理 SHALL 穷举所有"返回""取消""关闭"按钮
- **AND** 验证每个按钮的目标页面是其语义父页面
- **AND** 验证详情页"返回"目标为列表页（非无意义的 history.back()）
- **AND** 验证表单"取消"目标为进入表单前的页面
- **AND** 验证弹窗"关闭"后上下文不变
- **AND** 标记语义不合理的返回目标

#### Scenario: 表单切换链检查

- **WHEN** 子代理执行导航验证
- **THEN** 子代理 SHALL 验证多步表单的"上一步/下一步"链条完整
- **AND** 验证表单提交成功后的去向明确（列表页/详情页/新页面）且合理
- **AND** 验证表单提交失败后留在当前页并保留已填数据
- **AND** 标记断链或去向不明确的表单

#### Scenario: 弹窗/抽屉导航检查

- **WHEN** 子代理执行导航验证
- **THEN** 子代理 SHALL 验证每个弹窗/抽屉的触发方式正确
- **AND** 验证所有关闭方式可用（确认按钮/取消按钮/点击遮罩/Esc）
- **AND** 验证弹窗嵌套的层级关系和逐层关闭
- **AND** 标记关闭后上下文错乱的情况

#### Scenario: 跨页面流程闭环检查

- **WHEN** 子代理执行导航验证
- **THEN** 子代理 SHALL 按业务流程脚本逐条走通完整导航路径
- **AND** 验证从入口到终点能回到起点（闭环）
- **AND** 验证无"跳进去出不来"的页面序列
- **AND** 标记流程断点

### Requirement: 导航验证报告

每轮子代理 SHALL 输出验证报告到指定路径。

#### Scenario: 报告输出

- **WHEN** 子代理完成一轮导航验证
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/nav-check/round-{N}.md`（N 为轮次 1-5）
- **AND** 报告 SHALL 包含 5 项检查各自的结果、发现问题和建议修复

#### Scenario: 复检轮报告输出

- **WHEN** 子代理完成复检轮
- **THEN** 子代理 SHALL 保存报告到 `self-reviews/prototype/nav-check/round-recheck.md`
- **AND** 该报告 SHALL 明确标注其为复检轮
- **AND** 该报告 SHALL 包含清单内每一项修复的逐项复核结果与全量遍历证明

#### Scenario: 主 Agent 读取和处理

- **WHEN** 子代理报告写入完成
- **THEN** 主 Agent SHALL 从 `self-reviews/prototype/nav-check/round-{N}.md` 读取报告
- **AND** 对发现的问题 SHALL 直接修复原型文件
- **AND** 修复完成后 SHALL 进入下一轮
