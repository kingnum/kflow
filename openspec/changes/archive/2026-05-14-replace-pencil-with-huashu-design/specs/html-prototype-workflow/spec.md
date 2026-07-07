## ADDED Requirements

### Requirement: huashu-design 委托调用

系统 SHALL 委托 huashu-design Skill 执行 HTML 原型设计工作。

#### Scenario: huashu-design 可用
- **WHEN** 进入原型设计阶段
- **AND** huashu-design Skill 已安装在项目中
- **THEN** 系统通过 `Skill("huashu-design", prompt)` 委托执行设计
- **AND** prompt 包含项目背景、UI 功能点清单、设计约束、品牌资产、产出要求

#### Scenario: huashu-design 不可用
- **WHEN** 进入原型设计阶段
- **AND** huashu-design Skill 未安装
- **THEN** 系统提示用户执行 `npx skills add alchaincyf/huashu-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞

### Requirement: prompt 上下文组装

系统 SHALL 在委托调用前组装完整的上下文 prompt。

#### Scenario: 组装必然存在的前置产物
- **WHEN** 组装 prompt 上下文
- **THEN** 系统从 `functional-designs/` 提取项目背景和 UI 功能点清单
- **AND** 指定产出路径为 `docs/changes/{change}/prototype/index.html`

#### Scenario: 组装条件存在的产品级原型
- **WHEN** `docs/prototype/design-tokens.css` 存在
- **THEN** 系统将其 CSS 变量内容纳入设计约束
- **AND** 将 `docs/prototype/screens/` 下已有屏幕清单纳入上下文

#### Scenario: 组装条件存在的品牌资产
- **WHEN** 变更涉及具体品牌且有 brand-spec.md
- **THEN** 系统将品牌资产纳入 prompt

### Requirement: HTML 原型产物

系统 SHALL 输出 HTML 文件作为原型产物，替代 Pencil .pen 格式。

#### Scenario: 原型产物输出
- **WHEN** huashu-design 完成设计
- **THEN** 系统将产物写入 `docs/changes/{change}/prototype/` 目录
- **AND** `index.html` 为可浏览器直接打开的自包含文件

#### Scenario: 产物验证
- **WHEN** 原型文件写入完成
- **THEN** 系统验证 `prototype/index.html` 文件存在且可打开

### Requirement: 用户评审循环

系统 SHALL 在原型完成后通过 AskUserQuestion 进行用户评审。

#### Scenario: 确认通过
- **WHEN** 用户选择"确认通过"
- **THEN** 系统将原型设计阶段状态更新为 ✅ 完成
- **AND** kflow-guide 引导用户进入下一阶段

#### Scenario: 需要修订
- **WHEN** 用户选择"需要修订"
- **THEN** 系统收集用户反馈
- **AND** 将反馈作为修订要求重新调用 huashu-design
- **AND** 修订完成后再次进入评审

### Requirement: Playwright 交互验证

系统 SHALL 在原型交付前使用 Playwright 执行最小点击测试。

#### Scenario: 点击测试通过
- **WHEN** Playwright 可用且原型为交互原型
- **THEN** 系统执行点击测试（进入详情、关键点击、页面切换）
- **AND** 验证 pageerror 数量为 0

#### Scenario: Playwright 不可用降级
- **WHEN** Playwright 未安装或执行失败
- **THEN** 系统降级为手动视觉检查
- **AND** 在状态文件中记录降级原因

### Requirement: 移除 Pencil 依赖

系统 SHALL 完全移除 Pencil MCP 相关依赖。

#### Scenario: allowed-tools 更新
- **WHEN** kflow-prototype-design SKILL.md 定义 allowed-tools
- **THEN** 不包含 `mcp__pencil__*`
- **AND** 包含 `Skill`、`WebSearch`、`WebFetch`

#### Scenario: 设计规范文件移除
- **WHEN** 本变更实施完成
- **THEN** `references/rules/pencil-design-style.md` 已删除
