## ADDED Requirements

### Requirement: 产品级原型目录

系统 SHALL 维护 `docs/prototype/` 作为产品级原型的唯一来源。

#### Scenario: 目录结构初始化
- **WHEN** 首次归档创建产品级原型
- **THEN** 系统创建 `docs/prototype/` 及 `index.html`、`design-tokens.css`、`screens/`、`components/`、`assets/` 目录
- **AND** `index.html` 为卡片网格导航，按功能模块分组

#### Scenario: design-tokens.css 定义
- **WHEN** 产品级原型首次创建
- **THEN** `design-tokens.css` 包含色板、字号、间距、圆角、阴影的 CSS 变量
- **AND** 所有原型屏幕通过 `<link rel="stylesheet">` 引用此文件

### Requirement: 原型合并

系统 SHALL 在归档时将变更级原型合并到产品级原型。

#### Scenario: 新屏幕追加
- **WHEN** 变更包含产品级不存在的屏幕
- **THEN** 系统复制屏幕 HTML 到 `docs/prototype/screens/`
- **AND** 在 `index.html` 中追加导航卡片

#### Scenario: 修改屏幕覆盖
- **WHEN** 变更修改了产品级已存在的屏幕
- **THEN** 系统提示用户确认（覆盖/保留/人工裁决）
- **AND** 确认后替换对应文件

#### Scenario: CSS 变量追加
- **WHEN** 变更引入了新的 CSS 变量
- **THEN** 系统追加到 `design-tokens.css` 末尾
- **AND** 注释标注来源变更和追加时间

#### Scenario: 导航更新
- **WHEN** 原型合并完成
- **THEN** 系统更新 `index.html` 导航链接和最后更新时间戳

### Requirement: 新变更原型引导

系统 SHALL 在新变更进入原型设计时加载产品级上下文。

#### Scenario: 加载已有原型
- **WHEN** 新变更进入原型设计
- **AND** `docs/prototype/` 存在
- **THEN** 系统读取 `design-tokens.css`、`screens/` 清单、`components/` 清单
- **AND** 将已有信息纳入委托 prompt 的设计约束

#### Scenario: 首次原型设计
- **WHEN** 新变更进入原型设计
- **AND** `docs/prototype/` 不存在
- **THEN** 系统在 prompt 中标注"无已有设计令牌，请建立"
- **AND** 按首次设计执行
