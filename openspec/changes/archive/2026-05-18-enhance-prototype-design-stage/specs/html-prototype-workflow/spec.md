## MODIFIED Requirements

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

系统 SHALL 输出多文件 HTML 原型到 `prototype/` 目录，`index.html` 为访问入口。

#### Scenario: 原型产物输出

- **WHEN** huashu-design 完成设计
- **THEN** 系统将产物写入 `docs/changes/{change}/prototype/` 目录
- **AND** `index.html` 为访问入口，可导航到目录下其他页面文件
- **AND** 允许多文件架构（多个 HTML 文件 + 共享资源目录），不限制为单文件

#### Scenario: 产物验证

- **WHEN** 原型文件写入完成
- **THEN** 系统验证 `prototype/index.html` 文件存在且可打开
- **AND** 验证 `index.html` 中引用的所有内部文件（`<a href>`、`<iframe src>` 等）均存在
- **AND** 文件间引用完整性检查通过后方可进入 VERIFY 步骤

### Requirement: huashu-design 委托调用

系统 SHALL 在用户确认优化后的 prompt 后，委托 huashu-design Skill 执行 HTML 原型设计工作。

#### Scenario: huashu-design 可用

- **WHEN** OPTIMIZE 步骤完成且用户确认通过
- **AND** huashu-design Skill 已安装在项目中
- **THEN** 系统通过 `Skill("huashu-design", prompt)` 委托执行设计
- **AND** prompt 为 OPTIMIZE 步骤产出的优化后 prompt，包含页面元素级描述、业务流程脚本和硬约束

#### Scenario: huashu-design 不可用

- **WHEN** 进入原型设计阶段 CHECK 步骤
- **AND** huashu-design Skill 未安装
- **THEN** 系统提示用户执行 `npx skills add alchaincyf/huashu-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞

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

### Requirement: Playwright 交互验证

系统 SHALL 在原型交付前使用 Playwright 执行最小点击测试，验证交互流程可用。

#### Scenario: 点击测试通过

- **WHEN** Playwright 可用且原型为 flow demo 交互原型
- **THEN** 系统执行点击测试（进入详情、关键点击、页面切换）
- **AND** 验证 pageerror 数量为 0
- **AND** 验证至少一个完整业务流程可走通（无断点、无 JS 错误）

#### Scenario: Playwright 不可用降级

- **WHEN** Playwright 未安装或执行失败
- **THEN** 系统降级为手动视觉检查
- **AND** 在状态文件中记录降级原因

## ADDED Requirements

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
