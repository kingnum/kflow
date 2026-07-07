# html-prototype-workflow Delta Specification

## MODIFIED Requirements

### Requirement: huashu-design 委托调用

系统 SHALL 在用户确认 design-prompt.md 后，通过子代理（Agent）委托调用 huashu-design Skill 执行 HTML 原型设计工作。

#### Scenario: 子代理委托调用

- **WHEN** OPTIMIZE 步骤完成且 `prototype/design-prompt.md` 已用户确认
- **AND** huashu-design Skill 已安装在项目中
- **THEN** 系统 SHALL 启动子代理 `Agent(subagent_type="claude")` 执行 huashu-design
- **AND** 子代理 SHALL 从 `prototype/design-prompt.md` 读取完整提示词
- **AND** 子代理 SHALL 调用 `Skill("huashu-design", prompt)` 生成原型
- **AND** SHALL NOT 在主 Agent 上下文中直接调用 `Skill("huashu-design")`

#### Scenario: 子代理完成回主 Agent

- **WHEN** 子代理完成 huashu-design 调用并写入文件
- **THEN** 主 Agent SHALL 验证 `prototype/index.html` 存在且非空
- **AND** 主 Agent SHALL 验证所有内部文件引用目标文件存在
- **AND** 验证通过后 SHALL 进入 VERIFY 步骤

#### Scenario: huashu-design 不可用

- **WHEN** 进入原型设计阶段 CHECK 步骤
- **AND** huashu-design Skill 未安装
- **THEN** 系统提示用户执行 `npx skills add alchaincyf/huashu-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞

### Requirement: Playwright 交互验证

系统 SHALL 在原型交付前使用 Playwright 执行 5 轮全覆盖验证，每轮启动独立子代理执行全部 5 项检查（页面可达性、按钮/链接全覆盖点击、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）。

#### Scenario: 5 轮 Playwright 全覆盖验证

- **WHEN** 导航合理性验证（6.3 节）完成
- **AND** Playwright 可用且原型为 flow demo 交互原型
- **THEN** 系统 SHALL 执行 5 轮子代理串行 Playwright 验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查（页面可达性、按钮/链接全覆盖、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）
- **AND** 每轮验证 pageerror 数量 SHALL 为 0
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

#### Scenario: Playwright 不可用降级

- **WHEN** Playwright 未安装或执行失败
- **THEN** 系统降级为手动文件分析
- **AND** 在验证报告中记录降级原因

## ADDED Requirements

### Requirement: 导航合理性验证

系统 SHALL 在 CDN 扫描和交叉引用检查通过后、Playwright 验证之前，执行 5 轮导航合理性验证（6.3 节），每轮启动独立子代理执行全部 5 项检查。

#### Scenario: 5 轮导航合理性验证

- **WHEN** CDN 扫描（6.1）和交叉引用检查（6.2）通过
- **THEN** 系统 SHALL 执行 5 轮子代理串行导航合理性验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查（页面可达性、返回/取消按钮合理性、表单切换链、弹窗/抽屉导航、跨页面流程闭环）
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

#### Scenario: 导航验证与 Playwright 验证的顺序

- **WHEN** 导航合理性验证（6.3 节）全部 5 轮完成
- **THEN** 系统 SHALL 进入 Playwright 验证（6.4 节）
- **AND** SHALL NOT 在导航验证未全部完成前启动 Playwright 验证

### Requirement: design-prompt.md 文件输出

系统 SHALL 在 OPTIMIZE 步骤完成后，将优化后的完整提示词写入 `prototype/design-prompt.md` 文件（含 7 个章节），经用户确认后作为 DESIGN 步骤的唯一输入。

#### Scenario: OPTIMIZE 产出文件化

- **WHEN** OPTIMIZE 步骤完成（菜单树提取 + 页面元素穷举 + 业务流程脚本 + 硬约束注入）
- **THEN** 系统 SHALL 将完整 prompt 写入 `docs/changes/{change}/prototype/design-prompt.md`
- **AND** 文件 SHALL 包含 7 个章节（项目背景、设计系统、菜单导航、页面规格、业务流程脚本、硬约束、高保真要求）
- **AND** 系统 SHALL NOT 在未生成该文件前进入 DESIGN 步骤

#### Scenario: 用户确认 design-prompt.md

- **WHEN** design-prompt.md 写入完成
- **THEN** 系统 SHALL 通过 AskUserQuestion 展示提示词摘要
- **AND** 文件状态初始为"待确认"
- **AND** 用户确认后文件状态更新为"已确认"并进入 DESIGN 步骤
- **AND** DESIGN 步骤完成后文件状态更新为"已执行"
