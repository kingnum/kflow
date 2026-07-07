# phase-self-review

## Purpose

定义 explore/prototype/design 三个设计阶段的 10 轮自循环审查机制，包括每阶段的自审维度定义、自审流程、自审记录存储和内容规范、强制执行规则，以及自审完成后的流转路径。

## ADDED Requirements

### Requirement: 三阶段 10 轮自审强制执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design 三个阶段各强制执行 10 轮自循环审查，不允许提前终止。

#### Scenario: explore 阶段自审
- **WHEN** kflow-explore 完成 functional-designs/ 初稿
- **THEN** 系统执行 10 轮自审
- **AND** 每轮按完整性、闭环性、必要性、清晰性四个维度检查
- **AND** 必须完成全部 10 轮后方可标记阶段完成

#### Scenario: prototype 阶段自审
- **WHEN** kflow-prototype-design 完成 prototype.pen 初稿
- **THEN** 系统执行 10 轮自审
- **AND** 每轮按覆盖性、一致性、可用性、完整性四个维度检查
- **AND** 覆盖性为第一优先级：确保所有 FP 有对应原型页面
- **AND** 必须完成全部 10 轮后方可进入用户评审

#### Scenario: design 阶段自审
- **WHEN** kflow-design 完成 detailed-design.md 初稿
- **THEN** 系统执行 10 轮自审
- **AND** 每轮按一致性、完备性、可行性、可测性四个维度检查
- **AND** 必须完成全部 10 轮后方可进入四视角交叉审查

### Requirement: 自审由当前阶段 Agent 执行

系统 SHALL 由当前阶段 Agent 自行执行自审，不启动独立审查 Agent。

#### Scenario: Agent 自审流程
- **WHEN** 阶段产物初稿生成完毕
- **THEN** 当前 Agent 进入自审循环
- **AND** Agent 读取自身产出，按维度逐项检查
- **AND** 发现问题后自行修复并记录

#### Scenario: 自审不需外部 Agent
- **WHEN** 自审过程中
- **THEN** 不启动额外的审查 Agent
- **AND** 独立验证由后续四视角交叉审查负责

### Requirement: 自审记录按时间戳命名

系统 SHALL 将每轮自审结果保存为以开始时间命名的独立文件。

#### Scenario: 自审文件命名
- **WHEN** 一轮自审开始
- **THEN** 记录当前本地时间作为轮次标识
- **AND** 文件名格式为 `{YYYYMMDD}-{HHMMSS}.md`
- **AND** 保存路径为 `self-reviews/{phase}/{YYYYMMDD}-{HHMMSS}.md`

#### Scenario: 自然排序即时间序
- **WHEN** 读取 self-reviews/{phase}/ 目录
- **THEN** 文件按名称自然排序即为执行顺序
- **AND** 无需额外的轮次编号字段

### Requirement: 自审记录内容规范

每轮自审报告 SHALL 包含审查维度得分、新发现问题、上轮问题修复验证、本轮改进内容、仍存在问题。

#### Scenario: 自审报告结构
- **WHEN** 一轮自审完成
- **THEN** 报告包含审查维度得分表（维度名、本轮得分、上轮得分、变化值）
- **AND** 包含新发现问题清单（序号、问题描述、严重度、状态）
- **AND** 包含上轮问题修复验证（序号、上轮问题、修复结果）
- **AND** 包含本轮改进内容描述
- **AND** 包含仍存在的问题（进入下一轮继续跟踪）

#### Scenario: 第 1 轮无上轮对比
- **WHEN** 第 1 轮自审报告生成
- **THEN** "上轮得分"列填写 N/A
- **AND** "上轮问题修复验证"章节标注为"首轮，无上轮问题"

### Requirement: explore 阶段自审维度

kflow-explore 自审 SHALL 覆盖完整性、闭环性、必要性、清晰性四个维度。

#### Scenario: 完整性检查
- **WHEN** explore 自审执行完整性维度
- **THEN** 检查是否所有页面/菜单/操作/表单项均已覆盖
- **AND** 检查是否所有用户可执行操作均有对应功能点

#### Scenario: 闭环性检查
- **WHEN** explore 自审执行闭环性维度
- **THEN** 检查业务流程是否无断点
- **AND** 检查每个业务流程是否从触发到结果形成完整闭环

#### Scenario: 必要性检查
- **WHEN** explore 自审执行必要性维度
- **THEN** 检查是否存在多余/冗余功能点
- **AND** 检查每个功能点是否有明确的用户价值

#### Scenario: 清晰性检查
- **WHEN** explore 自审执行清晰性维度
- **THEN** 检查每个功能点描述是否无歧义
- **AND** 检查每个功能点的边界是否明确

### Requirement: prototype 阶段自审维度

kflow-prototype-design 自审 SHALL 覆盖覆盖性、一致性、可用性、完整性四个维度，覆盖性为第一优先级。

#### Scenario: 覆盖性检查（第一优先级）
- **WHEN** prototype 自审执行覆盖性维度
- **THEN** 检查是否所有 FP 有对应原型页面
- **AND** 检查是否所有页面可执行操作有对应交互组件
- **AND** 检查是否所有表单项有对应表单组件

#### Scenario: 一致性检查
- **WHEN** prototype 自审执行一致性维度
- **THEN** 检查视觉风格是否统一
- **AND** 检查组件命名是否一致

#### Scenario: 可用性检查
- **WHEN** prototype 自审执行可用性维度
- **THEN** 检查交互流程是否顺畅
- **AND** 检查交互状态覆盖是否完整（加载/空/错误/边界）

#### Scenario: 完整性检查
- **WHEN** prototype 自审执行完整性维度
- **THEN** 检查组件状态覆盖（加载态、空态、错误态、边界态）
- **AND** 检查所有页面入口是否可达

### Requirement: design 阶段自审维度

kflow-design 自审 SHALL 覆盖一致性、完备性、可行性、可测性四个维度。

#### Scenario: 一致性检查
- **WHEN** design 自审执行一致性维度
- **THEN** 检查 detailed-design.md 是否与 functional-designs/ 对齐
- **AND** 检查数据模型是否与功能设计中的业务规则一致
- **AND** 检查接口设计是否覆盖功能设计中的可执行操作

#### Scenario: 完备性检查
- **WHEN** design 自审执行完备性维度
- **THEN** 检查是否所有 FP 有对应技术设计
- **AND** 检查 NFR 是否覆盖性能/安全/可用性/可维护性

#### Scenario: 可行性检查
- **WHEN** design 自审执行可行性维度
- **THEN** 检查技术方案是否可落地
- **AND** 检查是否使用了团队不支持的依赖

#### Scenario: 可测性检查
- **WHEN** design 自审执行可测性维度
- **THEN** 检查 test-reports/ 下测试用例是否可执行
- **AND** 检查测试用例是否覆盖所有接口和 E2E 场景

### Requirement: 自审后进入交叉审查或用户评审

系统 SHALL 在自审完成后按阶段类型进入下一步：explore 进入完成态，prototype 进入用户评审，design 进入四视角交叉审查。

#### Scenario: explore 自审完成后
- **WHEN** explore 完成 10 轮自审
- **THEN** 标记阶段完成
- **AND** 释放 prototype 或 design 阶段门控

#### Scenario: prototype 自审完成后进入用户评审
- **WHEN** prototype 完成 10 轮自审
- **THEN** 自审记录全部保存完毕
- **AND** 进入用户评审流程（AskUserQuestion）
- **AND** 用户确认后标记阶段完成

#### Scenario: design 自审完成后进入四视角审查
- **WHEN** design 完成 10 轮自审
- **THEN** 自审记录全部保存完毕
- **AND** 进入四视角交叉审查流程
