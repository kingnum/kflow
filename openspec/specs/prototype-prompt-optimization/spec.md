# prototype-prompt-optimization Specification

## Purpose
定义原型设计阶段中 OPTIMIZE 步骤的需求规格：编排层 Agent 深度分析 functional-designs/ 产出细化到页面元素级别的设计 prompt，并通过 AskUserQuestion 展示给用户确认。

## Requirements

### Requirement: 原型提示词优化步骤

系统 SHALL 在 INPUT 步骤和 DESIGN 步骤之间执行 OPTIMIZE 步骤，深度分析 functional-designs/ 产出优化后的设计 prompt，并通过 AskUserQuestion 展示给用户确认后方可进入 DESIGN。

#### Scenario: 编排层 Agent 深度分析 functional-designs/
- **WHEN** OPTIMIZE 步骤启动
- **AND** `docs/changes/{change}/functional-designs/` 包含 index.md 和 part-NN.md 文件
- **THEN** 编排层 Agent SHALL 读取 functional-designs/ 全部文件
- **AND** 提取并转译出以下设计信息：
  - 全局菜单结构（一级菜单 → 二级菜单 → 三级菜单，每个菜单项对应的页面）
  - 导航模式（顶部导航 / 侧边栏 / Tab Bar / 面包屑）
  - 全局组件清单（Header / Footer / 用户头像 / 通知铃铛等）

#### Scenario: 优化后的 prompt 包含每个页面的元素级描述
- **WHEN** 编排层 Agent 完成设计信息提取
- **THEN** 优化后的 prompt SHALL 对每个页面穷举描述：
  - 页面名称与路由/锚点
  - 布局分区（header区 / sidebar区 / 主内容区 / 操作栏 / 列表区 / 详情面板 / footer）
  - 可执行操作清单（操作名 → 触发方式 → 预期结果 → 目标页面或弹窗）
  - 按钮清单（按钮名 → 位置 → 样式(主要/次要/文字/危险) → 触发动作 → 前置条件）
  - 表单清单（表单名 → 字段列表 → 每个字段的: 名称/类型/是否必填/校验规则/默认值/placeholder → 提交按钮 → 提交后行为）
  - 数据展示区（表格/卡片/图表的字段定义）
  - 状态覆盖（加载态 / 空态 / 错误态 / 边界态）
  - 弹窗/抽屉（触发条件 → 内容 → 关闭方式）

#### Scenario: 优化后的 prompt 包含业务流程脚本
- **WHEN** 编排层 Agent 组装优化后的 prompt
- **THEN** prompt SHALL 包含至少一个完整的业务流程脚本
- **AND** 每个流程脚本逐步描述：用户在哪个页面 → 点击什么 → 看到什么变化 → 进入哪个页面或弹窗
- **AND** 流程脚本覆盖端到端用户路径（如：登录 → 查看列表 → 进入详情 → 编辑 → 提交 → 返回列表）

#### Scenario: 优化后的 prompt 注入硬约束
- **WHEN** 编排层 Agent 组装优化后的 prompt
- **THEN** prompt SHALL 包含以下硬约束：
  - 输出到 `docs/changes/{change}/prototype/` 目录，允许多文件结构，`index.html` 为入口
  - 使用 flow demo 模式（可交互业务流程，单台设备状态管理器驱动），禁止 overview 静态平铺
  - 所有资源必须自包含（禁 CDN 外部引用，内联或相对路径，系统字体栈）

#### Scenario: 用户确认优化后的 prompt
- **WHEN** 编排层 Agent 完成 prompt 优化
- **THEN** 系统 SHALL 通过 AskUserQuestion 向用户展示优化后的 prompt 摘要
- **AND** 提供「确认执行」和「需要修订」两个选项
- **AND** 用户选择「确认执行」后，系统进入 DESIGN 步骤（委托 huashu-design）
- **AND** 用户选择「需要修订」后，系统收集用户反馈，回到优化步骤修订 prompt

#### Scenario: OPTIMIZE 步骤在纯后端项目中跳过
- **WHEN** 项目类型为纯后端
- **AND** CHECK 步骤判定原型设计自动跳过
- **THEN** OPTIMIZE 步骤 SHALL 不执行
- **AND** 阶段状态标记为 ⏭️ 跳过
