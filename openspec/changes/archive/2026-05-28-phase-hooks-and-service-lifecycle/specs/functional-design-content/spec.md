## ADDED Requirements

### Requirement: 功能点包含关联配置项信息

每个功能点 SHALL 标注其关联的配置项，描述配置项与功能行为的关联关系。

#### Scenario: 功能点关联配置项定义

- **WHEN** functional-designs/part-NN.md 中定义功能点
- **THEN** 每个功能点 SHALL 包含"关联配置项"章节
- **AND** 该章节 SHALL 包含一个表格，字段为：配置项名称、关联功能点ID、关联类型、配置值变化→功能行为变化描述
- **AND** 关联类型 SHALL 从以下枚举中选择：控制可见性、控制数据范围、控制校验规则、控制流程分支、控制权限

#### Scenario: 功能点无关联配置项

- **WHEN** 功能点不依赖任何配置项
- **THEN** "关联配置项"章节 SHALL 标注"本功能点无关联配置项"
- **AND** SHALL NOT 省略该章节

### Requirement: 功能设计索引包含全局配置项影响矩阵

functional-designs/index.md SHALL 包含一个汇总所有功能点配置项关联的全局矩阵。

#### Scenario: 全局配置项影响矩阵格式

- **WHEN** functional-designs/index.md 生成或更新
- **THEN** SHALL 包含"配置项影响矩阵"章节
- **AND** 矩阵 SHALL 包含字段：配置项名称、类型、默认值、受影响功能点ID列表、影响类型汇总
- **AND** 矩阵内容 SHALL 与各分册中功能点定义的"关联配置项"章节保持一致
