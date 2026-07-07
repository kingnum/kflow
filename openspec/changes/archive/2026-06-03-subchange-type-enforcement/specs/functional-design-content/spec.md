# functional-design-content Delta Spec

## ADDED Requirements

### Requirement: 功能点清单包含类型列

functional-designs/index.md 的功能点清单 SHALL 包含「类型」列，标记每个功能点为后端或前端。

#### Scenario: 类型列位置

- **WHEN** functional-designs/index.md 生成功能点清单
- **THEN** 表格 SHALL 在「简述」和「优先级」之间增加「类型」列
- **AND** 「类型」列 SHALL 在「优先级」之前显示
- **AND** 列值为枚举：`后端` | `前端`

#### Scenario: 后端 FP 判定标准

- **WHEN** 功能点涉及 API 实现、服务逻辑、数据模型、数据库操作、业务规则或外部服务集成
- **THEN** SHALL 标记为「后端」

#### Scenario: 前端 FP 判定标准

- **WHEN** 功能点涉及页面、组件、路由、状态管理、样式或 CSS 变量注入
- **THEN** SHALL 标记为「前端」

#### Scenario: 无法归类则拆分

- **WHEN** 功能点同时涉及后端和前端判定标准的内容
- **THEN** SHALL 判定为粒度过粗
- **AND** MUST 拆分为独立的后端 FP 和前端 FP
- **AND** 两个 FP 在「关联功能点」列相互引用

#### Scenario: 统计信息包含类型统计

- **WHEN** functional-designs/index.md 生成统计信息
- **THEN** 统计表 SHALL 增加「后端 FP 数量」和「前端 FP 数量」两行

### Requirement: 功能点标注跨层关联

后端 FP 如影响前端展示或表单字段，SHALL 在「关联功能点」列显式标注受影响的前端 FP-ID。

#### Scenario: Schema→UI 影响标注

- **WHEN** 后端 FP 涉及数据库 Schema 变更
- **AND** 该 Schema 变更影响前端展示
- **THEN** 后端 FP 的「关联功能点」列 SHALL 包含受影响前端 FP-ID
- **AND** 前端 FP 的「依赖功能点」列 SHALL 包含后端 FP-ID
- **AND** 关联关系类型 SHALL 标注为「数据模型变更」
