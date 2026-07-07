# html-prototype-workflow Specification

## Purpose
定义原型设计阶段中 HTML 原型的子代理委托生成、design-prompt.md 文件化、prompt 上下文组装、导航合理性验证、Playwright 5 轮全覆盖验证、输出产物和流程编排的需求规格。

## Requirements

### Requirement: huashu-design 子代理委托调用

系统 SHALL 在用户确认 design-prompt.md 后，通过子代理（Agent）委托调用 huashu-design Skill 执行 HTML 原型设计工作。

#### Scenario: 子代理委托调用
- **WHEN** OPTIMIZE 步骤完成且 `prototype/design-prompt.md` 已用户确认
- **AND** huashu-design Skill 已安装在项目中
- **THEN** 系统 SHALL 启动子代理 `Agent(subagent_type="claude")` 执行 huashu-design
- **AND** 子代理 SHALL 从 `prototype/design-prompt.md` 读取完整提示词
- **AND** 子代理 SHALL 调用 `Skill("huashu-design")` 生成原型
- **AND** SHALL NOT 在主 Agent 上下文中直接调用 `Skill("huashu-design")`

#### Scenario: 子代理完成回主 Agent
- **WHEN** 子代理完成 huashu-design 调用并写入文件
- **THEN** 主 Agent SHALL 验证 `prototype/index.md` 存在且清单中包含角色为 entry 的文件
- **AND** 主 Agent SHALL 验证入口文件中引用的所有内部文件均存在
- **AND** 验证通过后 SHALL 进入 VERIFY 步骤

#### Scenario: huashu-design 不可用
- **WHEN** 进入原型设计阶段 CHECK 步骤
- **AND** huashu-design Skill 未安装
- **THEN** 系统提示用户执行 `npx skills add alchaincyf/huashu-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞

### Requirement: prompt 上下文组装

系统 SHALL 在委托调用前完成 prompt 上下文机械组装，作为 OPTIMIZE 步骤的输入基础。

#### Scenario: 组装必然存在的前置产物
- **WHEN** 组装 prompt 上下文
- **THEN** 系统从 `functional-designs/` 提取项目背景和 UI 功能点清单
- **AND** 指定产出路径为 `docs/changes/{change}/prototype/` 目录

#### Scenario: 组装条件存在的产品级原型
- **WHEN** `docs/prototype/design-tokens.css` 存在
- **THEN** 系统将其 CSS 变量内容纳入设计约束
- **AND** 将 `docs/prototype/screens/` 下已有屏幕清单纳入上下文

#### Scenario: 组装条件存在的品牌资产
- **WHEN** 变更涉及具体品牌且有 brand-spec.md
- **THEN** 系统将品牌资产纳入 prompt

### Requirement: HTML 原型产物

系统 SHALL 输出 HTML 原型到 `prototype/` 目录，并在原型产物清单（`prototype/index.md`）中声明实际生成的文件结构。

#### Scenario: 原型产物输出
- **WHEN** huashu-design 完成设计
- **THEN** 系统将产物写入 `docs/changes/{change}/prototype/` 目录
- **AND** `prototype/index.md` 中的入口文件 SHALL 指向实际入口（默认为 `index.html`，允许其他入口）
- **AND** 允许多文件架构（多个 HTML 文件 + 共享资源目录），不限制为单文件

#### Scenario: 产物验证
- **WHEN** 原型文件写入完成
- **THEN** 系统验证 `prototype/index.md` 已生成且包含「原型文件清单」
- **AND** 清单中至少包含一个角色为 entry 的文件
- **AND** 验证入口文件中引用的所有内部文件（`<a href>`、`<iframe src>` 等）均存在
- **AND** 文件间引用完整性检查通过后方可进入 VERIFY 步骤

### Requirement: 业务流程驱动

系统 SHALL 默认使用 flow demo 模式生成可交互的业务流程原型，禁止仅提供 overview 静态页面平铺。

#### Scenario: flow demo 模式作为默认
- **WHEN** 原型设计进入 DESIGN 步骤
- **THEN** 系统 SHALL 要求 huashu-design 使用 flow demo 模式
- **AND** flow demo 模式使用单台设备状态管理器（如 `AppPhone`），驱动页面切换和交互行为
- **AND** 用户可通过点击 tab bar / 按钮 / 标注点完成完整业务流程
- **AND** SHALL NOT 仅提供所有页面并排静态展示的 overview 平铺

#### Scenario: overview 平铺被禁止
- **WHEN** 原型输出为多屏并排静态展示（overview 平铺）
- **AND** 用户无法通过点击完成业务流程交互
- **THEN** 该原型 SHALL 被视为不满足要求
- **AND** 需返回 DESIGN 步骤重新生成

### Requirement: 用户评审循环

系统 SHALL 在原型完成后通过 AskUserQuestion 进行用户评审。

#### Scenario: 确认通过
- **WHEN** 用户选择"确认通过"
- **THEN** 系统将原型设计阶段状态更新为 ✅ 完成
- **AND** SHALL 自动生成/更新 `prototype/index.md` 反映最终产物全貌
- **AND** kflow-guide 引导用户进入下一阶段

#### Scenario: 需要修订
- **WHEN** 用户选择"需要修订"
- **THEN** 系统收集用户反馈
- **AND** 将反馈作为修订要求重新调用 huashu-design
- **AND** 修订完成后再次进入评审
- **AND** 修订确认后 SHALL 重新更新 `prototype/index.md`

### Requirement: Playwright 5 轮全覆盖验证

系统 SHALL 在原型交付前使用 Playwright 执行 5 轮全覆盖验证，每轮启动独立子代理执行全部 5 项检查（页面可达性、按钮/链接全覆盖点击、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）。

#### Scenario: 5 轮 Playwright 全覆盖验证
- **WHEN** 导航合理性验证（6.3 节）完成
- **AND** Playwright 可用且原型为 flow demo 交互原型
- **THEN** 系统 SHALL 执行 5 轮子代理串行 Playwright 验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查
- **AND** 每轮验证 pageerror 数量 SHALL 为 0
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

#### Scenario: Playwright 不可用降级
- **WHEN** Playwright 未安装或执行失败
- **THEN** 系统降级为手动文件分析
- **AND** 在验证报告中记录降级原因

### Requirement: 导航合理性验证

系统 SHALL 在 CDN 扫描和交叉引用检查通过后、Playwright 验证之前，执行 5 轮导航合理性验证（6.3 节），每轮启动独立子代理执行全部 5 项检查。

#### Scenario: 5 轮导航合理性验证
- **WHEN** CDN 扫描（6.1）和交叉引用检查（6.2）通过
- **THEN** 系统 SHALL 执行 5 轮子代理串行导航合理性验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查（页面可达性、返回/取消按钮合理性、表单切换链、弹窗/抽屉导航、跨页面流程闭环）
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

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

### Requirement: 移除 Pencil 依赖

系统 SHALL 完全移除 Pencil MCP 相关依赖。

#### Scenario: allowed-tools 更新
- **WHEN** kflow-prototype-design SKILL.md 定义 allowed-tools
- **THEN** 不包含 `mcp__pencil__*`
- **AND** 包含 `Skill`、`WebSearch`、`WebFetch`

#### Scenario: 设计规范文件移除
- **WHEN** 本变更实施完成
- **THEN** `references/rules/pencil-design-style.md` 已删除

### Requirement: OPTIMIZE 步骤在流程中的位置

系统 SHALL 在 CHECK → ASSESS → INPUT 之后、DESIGN 之前插入 OPTIMIZE 步骤。

#### Scenario: OPTIMIZE 步骤触发
- **WHEN** INPUT 步骤完成（prompt 上下文机械组装完毕）
- **AND** 原型设计未被跳过（项目类型为前后端且存在 UI 功能点）
- **THEN** 系统 SHALL 进入 OPTIMIZE 步骤
- **AND** 编排层 Agent SHALL 深度阅读 functional-designs/ 全部内容

#### Scenario: OPTIMIZE 步骤完成后进入 DESIGN
- **WHEN** OPTIMIZE 步骤完成且用户确认通过
- **THEN** 系统 SHALL 进入 DESIGN 步骤
- **AND** 使用优化后的 prompt 委托调用 huashu-design
