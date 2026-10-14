# prototype-navigation-verification Specification

## Purpose

定义原型设计阶段 VERIFY 步骤中的导航合理性验证（9.1 节），子代理串行验证，轮次下限 1、**不预设轮数上限**（纯收敛驱动），以见证轮四项判据收敛终止，每轮子代理完整执行全部 5 项检查；适用审查范围冻结与范围外观察降级。该验证仅在审查方式为「子代理自动审查验证」时执行。

## Requirements

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
