# fp-type-classification Specification

## Purpose

定义 explore 阶段功能点类型标记规范——每个 FP 在拆分时即标记为后端或前端，无法归类的 FP 判定为粒度过粗并强制继续拆分。

## ADDED Requirements

### Requirement: FP 清单包含类型列

functional-designs/index.md 的功能点清单 SHALL 包含「类型」列，取值为「后端」或「前端」。

#### Scenario: FP 类型列格式

- **WHEN** explore 阶段输出 functional-designs/index.md
- **THEN** 功能点清单表格 SHALL 在「简述」和「优先级」之间增加「类型」列
- **AND** 列顺序为：功能点ID | 名称 | 简述 | 类型 | 优先级 | 关联功能点 | 依赖功能点 | 所在分册
- **AND** 「类型」取值为枚举：`后端` | `前端`

#### Scenario: 统计信息补充类型统计

- **WHEN** explore 阶段输出 functional-designs/index.md 统计信息
- **THEN** 统计表 SHALL 增加一行「后端 FP 数量」和「前端 FP 数量」
- **AND** 纯后端项目 SHALL 全部标记为后端且前端 FP 数量为 0

### Requirement: 后端 FP 判定标准

功能点涉及以下任一内容时，SHALL 标记为「后端」：

- API 实现（REST 接口/GraphQL/gRPC）
- 服务逻辑（业务规则处理/工作流编排）
- 数据模型定义（ORM 实体/数据库表结构）
- 数据库操作（CRUD/查询/事务）
- 业务规则引擎（规则校验/计算逻辑）
- 外部服务集成（第三方 API 调用/消息队列）

#### Scenario: 后端 FP 标记

- **WHEN** 功能点涉及 API 实现、服务逻辑、数据模型、数据库操作、业务规则或外部服务集成
- **THEN** SHALL 标记为「后端」
- **AND** SHALL NOT 标记为「前端」

### Requirement: 前端 FP 判定标准

功能点涉及以下任一内容时，SHALL 标记为「前端」：

- 页面组件（页面布局/模板结构）
- UI 组件（按钮/表单/表格/弹窗等可复用组件）
- 路由配置（页面路径/导航守卫）
- 状态管理（store/context/reactive state）
- 样式实现（CSS/SCSS/CSS-in-JS/Tailwind）
- CSS 变量注入（design-tokens 应用）

#### Scenario: 前端 FP 标记

- **WHEN** 功能点涉及页面、组件、路由、状态管理、样式或 CSS 变量注入
- **THEN** SHALL 标记为「前端」
- **AND** SHALL NOT 标记为「后端」

### Requirement: 无法归类则强制拆分

当功能点同时涉及后端判定标准和前端判定标准的内容，SHALL 判定为粒度过粗，MUST 继续拆分为独立的子功能点。

#### Scenario: 混合 FP 拒绝

- **WHEN** 一个 FP 同时涉及后端判定标准（如"实现注册 API"）和前端判定标准（如"展示注册表单"）
- **THEN** SHALL 判定为粒度过粗
- **AND** MUST 拆分为：一个后端 FP（注册 API 实现）+ 一个前端 FP（注册页面）
- **AND** SHALL NOT 以混合形式写入 functional-designs/

#### Scenario: 拆分后关联标注

- **WHEN** 一个原始 FP 被拆分为后端 FP 和前端 FP
- **THEN** 两个新 FP SHALL 在「关联功能点」列相互引用
- **AND** 前端 FP SHALL 在功能点描述中标注「关联后端 FP: {FP-ID}」

### Requirement: 类型标记作为后续阶段校验依据

FP 类型标记 SHALL 作为 design 阶段子变更划分类型校验、plan 阶段任务模板选择、verify 阶段输入源检查的依据。

#### Scenario: 下游消费 FP 类型

- **WHEN** functional-designs/index.md 包含 FP 类型列
- **THEN** design 阶段 SHALL 以 FP 类型为基础进行子变更类型一致性校验
- **AND** plan 阶段 SHALL 按 FP 类型选择任务模板
- **AND** verify 阶段 SHALL 按 FP 类型进行输入源正确性检查
