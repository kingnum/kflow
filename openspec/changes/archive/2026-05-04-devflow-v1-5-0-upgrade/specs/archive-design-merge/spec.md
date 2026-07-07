## ADDED Requirements

### Requirement: 归档时合并功能设计和详细设计

系统 SHALL 在归档时将变更级的功能设计和详细设计合并到产品级文档。

#### Scenario: 合并功能设计
- **WHEN** 归档变更
- **THEN** 系统从 functional-design.md 提取功能点清单、需求描述、验收标准
- **AND** 合并到 docs/designs/domains/{domain}.md 的功能设计章节

#### Scenario: 合并详细设计
- **WHEN** 归档变更
- **THEN** 系统从 detailed-design.md 提取设计域章节、数据模型、接口设计
- **AND** 合并到 docs/designs/domains/{domain}.md 的技术设计章节
- **AND** 更新全景文档（architecture.md, data-model.md, api-catalog.md, nfr-baseline.md）

#### Scenario: 原型设计不合并
- **WHEN** 归档变更
- **THEN** 原型设计文件 prototype.pen 保留在变更级归档目录中
- **AND** 不合并到产品级 prototypes/ 目录

### Requirement: 产品级文档按设计域组织

系统 SHALL 将产品级设计文档按设计域拆分为独立文件。

#### Scenario: 创建索引入口
- **WHEN** 首次归档创建产品级文档
- **THEN** 系统创建 docs/designs/index.md 作为索引入口
- **AND** 索引文件列出所有设计域文档链接和最后更新时间

#### Scenario: 新增设计域文档
- **WHEN** 归档变更涉及新的设计域
- **THEN** 系统创建 docs/designs/domains/{domain}.md
- **AND** 文件包含功能设计章节和技术设计章节

#### Scenario: 更新已有设计域文档
- **WHEN** 归档变更涉及已有设计域
- **THEN** 系统更新对应 domains/{domain}.md
- **AND** 默认采用替换更新策略

### Requirement: 变更溯源标注

系统 SHALL 在每个合并章节标注来源变更和归档时间。

#### Scenario: 标注来源变更
- **WHEN** 内容合并到产品级文档
- **THEN** 每个章节头部包含来源变更链接
- **AND** 包含归档时间和最后更新时间
- **AND** 格式为：来源变更 + 归档时间 + 最后更新

### Requirement: 合并冲突检测

系统 SHALL 在归档合并时检测设计域冲突。

#### Scenario: 同设计域已有内容
- **WHEN** 新归档变更涉及已有设计域
- **THEN** 系统检测到冲突并提示用户
- **AND** 提供替换更新、增量追加、人工裁决三种处理选项

#### Scenario: 结构性冲突
- **WHEN** 新旧设计存在结构性冲突（如数据模型不兼容）
- **THEN** 系统标记为需人工裁决
- **AND** 详细展示冲突点

### Requirement: 变更记录维护

系统 SHALL 在归档时更新 changelog.md。

#### Scenario: 追加变更记录
- **WHEN** 归档完成
- **THEN** changelog.md 追加一条记录
- **AND** 记录包含归档日期、变更名称、涉及设计域、主要变更摘要

#### Scenario: changelog 按年归档
- **WHEN** changelog.md 超过 500 行或年末
- **THEN** 系统将旧记录归档到 changelog-{year}.md
- **AND** changelog.md 仅保留当前年记录
