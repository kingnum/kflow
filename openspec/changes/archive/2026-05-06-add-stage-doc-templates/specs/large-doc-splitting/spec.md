## ADDED Requirements

### Requirement: 按数量拆分触发条件

系统 SHALL 对 4 组文档引入按数量拆分机制，每个分册不超过 30 个条目。

#### Scenario: 条目数不超过 30
- **WHEN** functional-designs、api-tests、e2e-tests、integration-tests 中任一组文档的条目数 ≤ 30
- **THEN** 该组仅包含 index.md + 一个 part-01.md
- **AND** part-01.md 包含全部条目

#### Scenario: 条目数超过 30
- **WHEN** 上述任一组文档的条目数 > 30
- **THEN** 系统拆分为 index.md + 多个 part-NN.md 分册
- **AND** 每个分册条目数 ≤ 30
- **AND** 最后一个分册条目数可能少于 30

### Requirement: 拆分适用文档范围

拆分机制 SHALL 仅适用于以下 4 组文档。

#### Scenario: 适用拆分的文档组
- **WHEN** 以下文档的条目数 > 30
- **THEN** functional-designs 按功能点数拆分
- **AND** api-tests 按接口数拆分
- **AND** e2e-tests 按场景数拆分
- **AND** integration-tests 按场景数拆分

#### Scenario: 其他文档不适用拆分
- **WHEN** detailed-design.md、audit-report.md 等其他文档
- **THEN** 保持单文件模式
- **AND** 其拆分规则由 doc-split-strategy spec 中的条件拆分规则决定

### Requirement: 分册文件命名规范

分册文件 SHALL 统一使用 `part-NN.md` 格式命名。

#### Scenario: 分册命名
- **WHEN** 创建分册文件
- **THEN** 文件名格式为 `part-01.md`、`part-02.md` ... 使用两位数字序号
- **AND** 每组文档的索引入口统一命名为 `index.md`

### Requirement: 分册模板格式

每个分册 SHALL 使用独立模板，包含本册条目的完整覆盖信息。

#### Scenario: 分册 frontmatter 字段
- **WHEN** 分册文件被创建
- **THEN** frontmatter 包含 part（分册号）、range（条目范围）、count（条目数）、covered_fp（覆盖的功能点范围）

#### Scenario: 分册正文结构
- **WHEN** 分册正文被渲染
- **THEN** 开头包含"本册覆盖范围"摘要
- **AND** 随后为条目的详细定义（与不分拆时的格式一致）
- **AND** 末尾包含本册修订记录

### Requirement: 索引文件规范

索引文件 SHALL 统一命名为 index.md，SHALL 具备逐条可读性。

#### Scenario: 索引文件结构
- **WHEN** 索引文件被创建
- **THEN** 包含分册总览表（分册号、文件链接、条目范围、条目数、内容简述）
- **AND** 包含逐条清单（每个条目的 ID、名称、简述、关键属性）

#### Scenario: e2e-tests 索引逐条清单
- **WHEN** e2e-tests/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、功能点简述、覆盖场景（场景ID列表）、验证类型、所在分册

#### Scenario: api-tests 索引逐条清单
- **WHEN** api-tests/index.md 被创建
- **THEN** 逐条清单包含：接口ID、方法、路径、简述、用例数、所在分册

#### Scenario: functional-designs 索引逐条清单
- **WHEN** functional-designs/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、名称、简述、优先级、依赖功能点、所在分册

#### Scenario: integration-tests 索引逐条清单
- **WHEN** integration-tests/index.md 被创建
- **THEN** 逐条清单包含：功能点ID、功能点简述、所属子变更、子变更级测试状态、集成场景（场景ID列表）、集成验证要点、所在分册

### Requirement: 门控检查适配拆分

阶段门控检查 SHALL 适配目录化结构，检查 index.md 存在即可。

#### Scenario: 功能设计门控检查
- **WHEN** 门控检查 functional-design.md 是否存在
- **THEN** 改为检查 functional-designs/index.md 是否存在
- **AND** index.md 存在即视为功能设计阶段产物已输出

#### Scenario: 测试用例门控检查
- **WHEN** 门控检查 api-tests.md / e2e-tests.md / integration-tests.md
- **THEN** 改为检查对应目录的 index.md 是否存在
