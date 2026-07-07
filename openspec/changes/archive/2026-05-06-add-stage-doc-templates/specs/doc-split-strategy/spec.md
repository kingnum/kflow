## ADDED Requirements

### Requirement: 按条目数量拆分

系统 SHALL 对 4 组大型文档引入按条目数量拆分策略。

#### Scenario: 功能设计文档按功能点数拆分
- **WHEN** functional-designs 的功能点数 > 30
- **THEN** 系统拆分为多个 part-NN.md 分册
- **AND** 每个分册功能点数 ≤ 30

#### Scenario: 测试用例文档按用例数拆分
- **WHEN** api-tests、e2e-tests、integration-tests 的条目数 > 30
- **THEN** 系统拆分为多个 part-NN.md 分册
- **AND** 每个分册条目数 ≤ 30

#### Scenario: 条目数不超过阈值
- **WHEN** 上述任一组文档的条目数 ≤ 30
- **THEN** 仅包含一个 part-01.md
- **AND** 目录结构（index.md + part-01.md）保持与拆分后的结构一致

## MODIFIED Requirements

### Requirement: 变更级文档条件拆分

系统 SHALL 按功能点数量决定变更级文档是否拆分，拆分策略分为条件拆分和数量拆分两种。

#### Scenario: 功能点不超过 30 个
- **WHEN** 变更功能点 ≤ 30
- **THEN** detailed-design.md 保持为单文件
- **AND** 内部分设计域章节组织
- **AND** functional-designs/ 包含 index.md + part-01.md（单分册结构）

#### Scenario: 功能点超过 30 个
- **WHEN** 变更功能点 > 30
- **THEN** 系统对 functional-designs/ 执行按数量拆分（≤30/分册）
- **AND** 系统评估 detailed-design.md 是否需要按域拆分（>30 时拆分为 detailed-design/{domain}.md）
- **AND** detailed-design.md 保留为 detailed-design/index.md 索引入口
