# prototype-design-prompt-template Specification

## Purpose

定义原型设计阶段 OPTIMIZE 步骤完成后输出的 `prototype/design-prompt.md` 提示词文件模板结构和内容要求。

## Requirements

### Requirement: design-prompt.md 文件输出

系统 SHALL 在 OPTIMIZE 步骤完成后，将优化后的完整提示词写入 `prototype/design-prompt.md` 文件，经用户确认后作为 DESIGN 步骤的唯一输入。

#### Scenario: 文件输出时机

- **WHEN** OPTIMIZE 步骤完成（4.1 菜单树提取 + 4.2 页面元素穷举 + 4.3 业务流程脚本 + 4.4 硬约束注入）
- **THEN** 系统 SHALL 将完整提示词写入 `docs/changes/{change}/prototype/design-prompt.md`
- **AND** 文件 SHALL 包含全部 7 个章节
- **AND** 系统 SHALL NOT 在未生成该文件前进入 DESIGN 步骤

#### Scenario: 用户确认

- **WHEN** design-prompt.md 写入完成
- **THEN** 系统 SHALL 通过 AskUserQuestion 向用户展示提示词摘要
- **AND** 用户确认后 SHALL 进入 DESIGN 步骤
- **AND** 用户需要修订时 SHALL 收集反馈并回到 4.1 修订

#### Scenario: 文件作为 DESIGN 步骤输入

- **WHEN** DESIGN 步骤开始
- **THEN** 系统 SHALL 从 `prototype/design-prompt.md` 读取完整提示词
- **AND** SHALL NOT 使用 OPTIMIZE 步骤内存中的 prompt 摘要

### Requirement: 7 章节模板结构

design-prompt.md SHALL 包含以下 7 个章节。

#### Scenario: 第一章 — 项目背景与设计目标

- **WHEN** design-prompt.md 生成
- **THEN** 第一章 SHALL 从 functional-designs/index.md 提取产品概述
- **AND** 明确本次原型的范围、目标用户和设计意图

#### Scenario: 第二章 — 设计系统

- **WHEN** design-prompt.md 生成
- **THEN** 第二章 SHALL 包含色彩方案（主色/背景色/文字色/边框色/状态色，含颜色值）
- **AND** 包含字体系统（系统字体栈 + 标题/正文层级规格）
- **AND** 包含间距与圆角规格（页面/卡片/组件/按钮）

#### Scenario: 第三章 — 菜单与导航结构

- **WHEN** design-prompt.md 生成
- **THEN** 第三章 SHALL 以菜单树展示一/二/三级菜单项及其对应页面
- **AND** 明确导航模式（顶部导航/侧边栏/Tab Bar/面包屑）
- **AND** 列出全局组件（Header/Footer/用户头像/通知铃铛等）
- **AND** 每个页面标注对应的原型文件名

#### Scenario: 第四章 — 页面详细规格

- **WHEN** design-prompt.md 生成
- **THEN** 第四章 SHALL 对每个页面逐项穷举：布局分区（ASCII 线框图）、按钮清单（名称/位置/样式/触发/前置条件）、表单清单（表单名/字段详情/提交行为）、数据展示区（类型/字段/交互）、状态覆盖（加载/空/错误/边界态）、弹窗/抽屉（触发/内容/关闭方式）
- **AND** SHALL NOT 遗漏任何功能点对应的页面元素

#### Scenario: 第五章 — 业务流程脚本

- **WHEN** design-prompt.md 生成
- **THEN** 第五章 SHALL 包含至少一个完整的端到端业务流程脚本
- **AND** 每步明确"用户在[哪个页面] → 点击[哪个按钮] → 看到[什么变化] → 进入[哪个页面]"
- **AND** 覆盖从入口到最终结果的完整路径

#### Scenario: 第六章 — 硬约束

- **WHEN** design-prompt.md 生成
- **THEN** 第六章 SHALL 注入多文件输出约束（输出到 prototype/ 目录，index.html 为入口）
- **AND** 注入 flow demo 模式约束（AppPhone 状态管理器驱动，禁止 overview 静态平铺）
- **AND** 注入离线自包含约束（禁 CDN，系统字体栈）

#### Scenario: 第七章 — 高保真要求

- **WHEN** design-prompt.md 生成
- **THEN** 第七章 SHALL 列出参考资源索引（产品级原型/设计令牌/品牌资产路径）
- **AND** 包含交互细节规格（按钮 hover/active 态、输入框 focus 态、弹窗过渡动画、表格行 hover 态、Tab 切换动画）
- **AND** 包含响应式要求（桌面端优先/移动端基准，如有）

### Requirement: 文件元信息

design-prompt.md SHALL 包含文件级元信息头部。

#### Scenario: 元信息头部

- **WHEN** design-prompt.md 生成
- **THEN** 文件头部 SHALL 包含：变更名称、版本号（1.0.0 起始）、生成时间、状态标记（待确认/已确认/已执行）
- **AND** 状态初始为"待确认"，用户确认后更新为"已确认"，DESIGN 步骤完成后更新为"已执行"
