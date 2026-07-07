## ADDED Requirements

### Requirement: 功能设计文档目录化输出

系统 SHALL 将设计探索阶段的输出格式从单文件调整为目录结构。

#### Scenario: 功能设计产物目录化
- **WHEN** kflow-explore 阶段完成
- **THEN** 输出 functional-designs/ 目录（替代原 functional-design.md 单文件）
- **AND** 目录包含 index.md + part-NN.md 分册
- **AND** index.md 包含完整的功能点清单索引（ID、名称、简述、优先级、依赖）

#### Scenario: 功能设计索引可读性
- **WHEN** functional-designs/index.md 被生成
- **THEN** 包含变更概述（问题、目标用户、预期价值）
- **AND** 包含功能点依赖关系图
- **AND** 包含统计信息（总数、分册数、P0/P1/P2 数量）

## MODIFIED Requirements

### Requirement: 设计探索输出调整

系统 SHALL 调整设计探索阶段的输出内容，不包含子变更划分，但输出格式从单文件改为目录结构。

#### Scenario: 功能设计输出内容
- **WHEN** 设计探索阶段完成
- **THEN** functional-designs/ 目录包含需求描述、项目类型、功能点清单、功能点关联关系
- **AND** 每个功能点包含：用户故事、功能行为矩阵（≥1HP+2EP+1EC）、业务规则、交互约束
- **AND** 不包含数据需求、接口需求（这些属于详细设计）
- **AND** 不包含子变更划分方案
- **AND** 版本号和修订记录在 index.md 和每个 part-NN.md 中维护
