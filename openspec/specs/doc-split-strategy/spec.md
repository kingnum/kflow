## Requirements

### Requirement: 产品级文档多文件拆分

系统 SHALL 从一开始即对产品级设计文档采用多文件拆分策略。

#### Scenario: 首次创建产品级文档
- **WHEN** 首次归档触发产品级文档创建
- **THEN** 系统创建 index.md 索引入口
- **AND** 创建 domains/ 目录存放设计域文档
- **AND** 创建 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md 全景文档

#### Scenario: 索引入口格式
- **WHEN** 产品级索引入口被创建或更新
- **THEN** index.md 包含设计域列表（链接 + 最后更新时间 + 来源变更）
- **AND** 包含全景文档链接

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

### Requirement: 全景文档增量更新

系统 SHALL 在归档合并时增量更新全景文档。

#### Scenario: 技术栈变化时更新架构
- **WHEN** 归档变更引入了技术栈变化
- **THEN** architecture.md 更新对应技术选型章节
- **AND** 保留旧版本记录

#### Scenario: 新增数据实体时更新
- **WHEN** 归档变更引入了新数据实体
- **THEN** data-model.md 追加新实体定义
- **AND** 保持已有实体内容不变

#### Scenario: 新增接口时更新
- **WHEN** 归档变更引入了新 API 接口
- **THEN** api-catalog.md 追加新接口条目
- **AND** 按设计域分组排列

### Requirement: changelog 按年归档

系统 SHALL 在 changelog.md 超过阈值或年末时执行归档。

#### Scenario: 超过行数阈值
- **WHEN** changelog.md 超过 500 行
- **THEN** 系统将旧记录移至 changelog-{year}.md
- **AND** changelog.md 保留当前年记录

#### Scenario: 年末强制归档
- **WHEN** 到达每年 12 月 31 日
- **THEN** 系统将当年所有记录归档到 changelog-{year}.md
- **AND** 新年的 changelog.md 从零开始
