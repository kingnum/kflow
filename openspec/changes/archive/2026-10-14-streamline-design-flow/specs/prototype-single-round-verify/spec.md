# Spec Delta

## Purpose

定义原型设计阶段 VERIFY 步骤的单轮合并验证机制：将原本各自独立、各为收敛循环的导航合理性验证、Playwright 全覆盖验证与 UX 规则审查合并为**一轮子代理验证、一份合并报告**，报告按环节强制分区以保证各环节检查深度不被合并稀释；对比度检测仍为静态计算。该验证仅在审查方式为「子代理自动审查验证」时执行。

## ADDED Requirements

### Requirement: 原型 VERIFY 单轮合并验证

系统 SHALL 在审查方式为「子代理自动审查验证」且 BUILD 四项静态检查全部通过后，启动**一轮**独立子代理执行导航合理性、Playwright 全覆盖与 UX 规则三项验证，并输出**一份合并验证报告**。系统 SHALL NOT 为三项验证分别启动独立子代理，SHALL NOT 执行第二轮验证。审查方式为「人工审查」时系统 SHALL NOT 执行本验证环节。

#### Scenario: 前置条件满足时进入合并验证

- **WHEN** BUILD 四项静态检查全部通过且审查方式为「子代理自动审查验证」
- **THEN** 系统 SHALL 启动一轮子代理执行三项验证
- **AND** 该子代理类型 SHALL 为 `Agent(subagent_type="claude")`，拥有独立上下文

#### Scenario: 单轮执行

- **WHEN** 合并验证子代理启动
- **THEN** 其 SHALL 在同一轮内完成导航合理性、Playwright 全覆盖与 UX 规则三项验证的全部检查项
- **AND** 系统 SHALL NOT 执行第二轮验证

#### Scenario: 人工审查路径跳过合并验证

- **WHEN** 审查方式为「人工审查」
- **THEN** 系统 SHALL NOT 执行合并验证
- **AND** SHALL NOT 启动任何验证子代理
- **AND** 系统 SHALL 直接进入用户评审（REVIEW）

#### Scenario: 子代理异常时的处置

- **WHEN** 合并验证子代理意外停止、报错退出或返回不完整结果
- **THEN** 主代理 MUST 重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管验证工作
- **AND** 最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户

### Requirement: 合并报告按环节强制分区

合并验证报告 SHALL 按环节分区组织，每个环节 SHALL 输出独立的检查结论。报告 SHALL 包含至少以下分区：导航合理性、Playwright 全覆盖、UX 规则审查、对比度检测、验证结论。任一环节缺失独立结论时该报告 SHALL 判定为不完整。

#### Scenario: 报告包含四个环节分区

- **WHEN** 合并验证报告生成
- **THEN** 报告 SHALL 包含「导航合理性」「Playwright 全覆盖」「UX 规则审查」「对比度检测」四个分区
- **AND** 每个分区 SHALL 独立给出该环节全部检查项的逐项结论

#### Scenario: 环境缺少结论时判定不完整

- **WHEN** 合并验证报告缺少任一环节的独立检查结论
- **THEN** 该报告 SHALL 判定为不完整
- **AND** 主 Agent SHALL 要求子代理补齐该环节后重新提交

#### Scenario: 验证结论分区

- **WHEN** 合并验证报告生成
- **THEN** 报告 SHALL 包含「验证结论」分区
- **AND** 该分区 SHALL 给出发现总数、发现清单与全量遍历证明

### Requirement: 导航合理性检查项（合并报告环节一）

合并验证子代理 SHALL 在本轮内执行以下全部 5 项导航合理性检查。

#### Scenario: 页面可达性检查

- **WHEN** 子代理执行导航合理性检查
- **THEN** 子代理 SHALL 从 `docs/designs/prototypes/index.html` 出发进行 BFS 遍历
- **AND** 遍历所有 `<a href>` 和导航组件引用
- **AND** 生成页面可达性矩阵
- **AND** 标记孤立页面（无任何入口链接指向）
- **AND** 标记死胡同页面（无任何出口链接）

#### Scenario: 返回/取消按钮合理性检查

- **WHEN** 子代理执行导航合理性检查
- **THEN** 子代理 SHALL 穷举所有「返回」「取消」「关闭」按钮
- **AND** 验证每个按钮的目标页面是其语义父页面
- **AND** 验证详情页「返回」目标为列表页（非无意义的 history.back()）
- **AND** 验证表单「取消」目标为进入表单前的页面
- **AND** 验证弹窗「关闭」后上下文不变
- **AND** 标记语义不合理的返回目标

#### Scenario: 表单切换链检查

- **WHEN** 子代理执行导航合理性检查
- **THEN** 子代理 SHALL 验证多步表单的「上一步/下一步」链条完整
- **AND** 验证表单提交成功后的去向明确（列表页/详情页/新页面）且合理
- **AND** 验证表单提交失败后留在当前页并保留已填数据
- **AND** 标记断链或去向不明确的表单

#### Scenario: 弹窗/抽屉导航检查

- **WHEN** 子代理执行导航合理性检查
- **THEN** 子代理 SHALL 验证每个弹窗/抽屉的触发方式正确
- **AND** 验证所有关闭方式可用（确认按钮/取消按钮/点击遮罩/Esc）
- **AND** 验证弹窗嵌套的层级关系和逐层关闭
- **AND** 标记关闭后上下文错乱的情况

#### Scenario: 跨页面流程闭环检查

- **WHEN** 子代理执行导航合理性检查
- **THEN** 子代理 SHALL 按业务流程脚本逐条走通完整导航路径
- **AND** 验证从入口到终点能回到起点（闭环）
- **AND** 验证无「跳进去出不来」的页面序列
- **AND** 标记流程断点

### Requirement: Playwright 全覆盖检查项（合并报告环节二）

合并验证子代理 SHALL 在本轮内执行以下全部 5 项 Playwright 检查，工作目录 SHALL 固定为项目根目录，原型 HTML 文件 SHALL 通过 `docs/designs/prototypes/index.html` 相对路径引用。

#### Scenario: 页面可达性扫描

- **WHEN** 子代理执行 Playwright 检查
- **THEN** 子代理 SHALL 从 `docs/designs/prototypes/index.html` 出发 BFS 遍历所有 `<a>` 链接
- **AND** 对每个页面验证加载成功（HTTP 200 或无 pageerror）
- **AND** 验证每个页面 `pageerror` 数量 = 0
- **AND** 输出页面可达性矩阵

#### Scenario: 按钮/链接全覆盖点击

- **WHEN** 子代理执行 Playwright 检查
- **THEN** 子代理 SHALL 穷举每个页面的所有 `<button>` 和 `<a>` 元素
- **AND** 逐个点击每个元素，验证有响应（页面跳转/弹窗打开/状态变更/控制台无错误）
- **AND** 对 `disabled` 状态按钮验证其不可点击
- **AND** 输出按钮/链接覆盖清单

#### Scenario: 表单全覆盖

- **WHEN** 子代理执行 Playwright 检查
- **THEN** 子代理 SHALL 对每个表单执行空提交验证（校验提示是否正确显示）
- **AND** 对每个表单执行合法数据提交验证（提交行为是否正确）
- **AND** 对每个表单执行取消/重置操作验证
- **AND** 输出表单覆盖清单

#### Scenario: 弹窗/抽屉全覆盖

- **WHEN** 子代理执行 Playwright 检查
- **THEN** 子代理 SHALL 对每个弹窗/抽屉验证所有打开方式
- **AND** 对每个弹窗/抽屉验证所有关闭方式（确认/取消/点击遮罩/Esc）
- **AND** 对弹窗内的表单和按钮按上述规则验证
- **AND** 输出弹窗覆盖清单

#### Scenario: 端到端业务流程

- **WHEN** 子代理执行 Playwright 检查
- **THEN** 子代理 SHALL 按变更级 `prototype-plan/design-prompt.md` 中定义的业务流程脚本逐条走通
- **AND** 验证每个流程无 JS 错误、无交互断点、无死胡同
- **AND** 输出流程通过清单

### Requirement: UX 规则检查项（合并报告环节三）

合并验证子代理 SHALL 在本轮内执行 UX 规则审查，逐项给出结论。

#### Scenario: UX 规则逐项审查

- **WHEN** 子代理执行 UX 规则审查
- **THEN** 子代理 SHALL 按本阶段既有的 UX 规则检查项逐项审查原型
- **AND** 每项检查 SHALL 给出独立结论
- **AND** 发现的问题 SHALL 记入合并报告的 UX 规则审查分区

### Requirement: 对比度检测（合并报告环节四）

对比度检测 SHALL 作为静态计算执行于合并报告内，SHALL NOT 启动独立子代理。

#### Scenario: 对比度静态计算

- **WHEN** 合并验证执行
- **THEN** 系统 SHALL 通过 WCAG 相对亮度计算检测原型中的颜色对
- **AND** 标记对比度低于 4.5:1 的颜色对
- **AND** 结果 SHALL 记入合并报告的对比度检测分区

### Requirement: 合并验证报告存放与读取

合并验证报告 SHALL 固定存放于 `self-reviews/prototype/verify-report.md`。主 Agent SHALL 从该路径读取报告。

#### Scenario: 报告固定路径

- **WHEN** 合并验证子代理完成验证
- **THEN** 报告 SHALL 保存到 `self-reviews/prototype/verify-report.md`
- **AND** SHALL NOT 产出按轮次编号的多份报告

#### Scenario: 主 Agent 读取与处理

- **WHEN** 报告写入完成
- **THEN** 主 Agent SHALL 从 `self-reviews/prototype/verify-report.md` 读取报告
- **AND** 对发现的问题 SHALL 统一修复原型文件
- **AND** SHALL 生成「本阶段修复清单」
- **AND** SHALL NOT 追加确认轮

### Requirement: 合并验证的审查范围冻结与范围外观察

合并验证 SHALL 适用审查范围冻结：审查对象集合 SHALL 由主 Agent 从原型阶段既有产物生成并冻结，审查维度 SHALL 限于导航合理性 5 项、Playwright 5 项、UX 规则与对比度检测四类固定检查项。子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增检查维度、SHALL NOT 借验证之名新增功能点、字段、章节或分支。冻结范围之外的发现 SHALL 记为「范围外观察」——SHALL NOT 触发产物修改、SHALL NOT 计入验证发现数，写入合并报告的「范围外观察」小节，由主 Agent 在阶段终止时汇总提示。

#### Scenario: 审查对象集合冻结

- **WHEN** 主 Agent 构建合并验证子代理的 prompt
- **THEN** prompt SHALL 包含由原型阶段既有产物生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件、代码或内容
- **AND** 子代理 SHALL NOT 新增检查维度

#### Scenario: 范围外发现不计入发现数

- **WHEN** 子代理仅在冻结范围之外发现问题
- **THEN** 该阶段的验证发现数 SHALL 记为 0
- **AND** 系统 SHALL NOT 修改任何原型产物

#### Scenario: 范围外观察写入报告

- **WHEN** 子代理产生范围外观察条目
- **THEN** 合并报告 SHALL 在「范围外观察」小节记录这些条目
- **AND** 该小节为空时 SHALL 记为「（空）」
- **AND** 主 Agent SHALL 在阶段终止时汇总全部范围外观察条目并向用户提示

### Requirement: Playwright 不可用降级

当 Playwright 不可用时，系统 SHALL 优先尝试 `.kflow-runtime/playwright/` 安装引导，安装失败后再降级为手动文件分析，并在报告的 Playwright 分区记录降级原因。

#### Scenario: 优先隔离安装

- **WHEN** `.kflow-runtime/playwright/node_modules/playwright` 不存在
- **THEN** 系统 SHALL 优先执行安装引导：`cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium`
- **AND** 安装成功时 SHALL 使用隔离安装继续验证

#### Scenario: 降级处理

- **WHEN** Playwright CLI 不可用且 `.kflow-runtime/playwright/` 安装失败
- **THEN** 主 Agent SHALL 在子代理 prompt 中指示降级为手动文件分析
- **AND** 报告 SHALL 在 Playwright 分区记录降级原因并标注「Playwright 不可用 — 降级为手动检查」

## REMOVED Requirements

### Requirement: 导航合理性验证轮次（纯收敛驱动）

**Reason**: 收敛驱动循环在本能力所属的原型验证中被单轮合并验证取代——三项验证合并为一轮，不再存在各自独立的轮次循环，见证轮四项判据随之失去载体。

**Migration**: 导航合理性的 5 项检查项迁移至 `prototype-single-round-verify` 能力的「导航合理性检查项（合并报告环节一）」Requirement，在合并验证的单轮内执行。

### Requirement: 每轮导航验证检查项

**Reason**: 该 Requirement 以「每轮」为组织单位，单轮合并验证下不存在轮次概念。

**Migration**: 5 项检查项内容逐条迁移至 `prototype-single-round-verify` 能力的「导航合理性检查项（合并报告环节一）」Requirement，内容不变。

### Requirement: 导航验证报告内容与存放

**Reason**: 报告路径 `self-reviews/prototype/nav-check/round-{N}.md` 以轮次编号命名，单轮合并验证下由单一合并报告取代。

**Migration**: 报告路径改为 `self-reviews/prototype/verify-report.md`，导航检查结果作为合并报告的「导航合理性」分区，见 `prototype-single-round-verify` 能力的「合并报告按环节强制分区」与「合并验证报告存放与读取」Requirement。

### Requirement: Playwright 全覆盖验证轮次（纯收敛驱动）

**Reason**: 同「导航合理性验证轮次（纯收敛驱动）」——收敛驱动循环被单轮合并验证取代。

**Migration**: Playwright 的 5 项检查项、不可用降级与运行时隔离规则分别迁移至 `prototype-single-round-verify` 能力的对应 Requirement；运行时隔离规则同时由原能力的「playwright 运行时隔离」Requirement 继续承载。

### Requirement: 每轮 Playwright 验证检查项

**Reason**: 同「每轮导航验证检查项」——以「每轮」为组织单位，单轮合并验证下不存在轮次概念。

**Migration**: 5 项检查项内容逐条迁移至 `prototype-single-round-verify` 能力的「Playwright 全覆盖检查项（合并报告环节二）」Requirement，内容不变。

### Requirement: Playwright 验证报告内容与存放

**Reason**: 报告路径 `self-reviews/prototype/playwright-check/round-{N}.md` 以轮次编号命名，由单一合并报告取代。

**Migration**: 报告路径改为 `self-reviews/prototype/verify-report.md`，Playwright 结果作为合并报告的「Playwright 全覆盖」分区。

### Requirement: 导航验证适用审查范围冻结与范围外观察

**Reason**: 该 Requirement 以「每轮审查对象集合」「不阻断收敛」为组织口径，属多轮循环语义。

**Migration**: 审查范围冻结与范围外观察规则合并上收至 `prototype-single-round-verify` 能力的「合并验证的审查范围冻结与范围外观察」Requirement，单轮下统一适用于四类检查。

### Requirement: Playwright 验证适用审查范围冻结与范围外观察

**Reason**: 同「导航验证适用审查范围冻结与范围外观察」。

**Migration**: 同「导航验证适用审查范围冻结与范围外观察」的迁移路径。
