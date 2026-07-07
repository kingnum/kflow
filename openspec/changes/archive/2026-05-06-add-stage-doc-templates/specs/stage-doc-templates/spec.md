## ADDED Requirements

### Requirement: 模板目录结构

系统 SHALL 在 `docs/designs/templates/` 目录下按产物层级组织模板文件。

#### Scenario: 模板目录创建
- **WHEN** 模板体系首次初始化
- **THEN** 系统创建 `docs/designs/templates/index.md` 作为模板目录索引入口
- **AND** 创建 change/、subchange/、integration/、product/、infra/ 五子目录

#### Scenario: 索引入口格式
- **WHEN** templates/index.md 被创建或更新
- **THEN** 文件列出五子目录及其覆盖的产物类型
- **AND** 列出完整模板清单（模板文件路径 + 对应产物 + 产出 Skill）

### Requirement: 模板文件格式

每个模板文件 SHALL 使用 YAML frontmatter + Markdown body 格式。

#### Scenario: 模板文件 frontmatter 字段
- **WHEN** 模板文件被创建
- **THEN** frontmatter 至少包含：产出阶段（stage）、产出 Skill（skill）、版本（version）、创建时间（created_at）
- **AND** 对于分册模板，额外包含分册标识（part）和条目范围（range）

#### Scenario: 模板正文占位符
- **WHEN** 模板正文需要指示待填写内容
- **THEN** 使用 `{placeholder}` 格式标注占位符
- **AND** 每个占位符旁包含注释说明其含义和类型（如 `{change-name}` — 变更名称，kebab-case）

### Requirement: 模板与 Skill spec 的引用关系

每个产出独立文件的 Skill spec SHALL 在"输出产物"表格中引用对应模板路径。

#### Scenario: 输出产物表格包含模板列
- **WHEN** Skill spec 定义输出产物
- **THEN** 输出产物表格包含"模板"列
- **AND** 模板列值为指向 `templates/` 目录的相对路径链接

#### Scenario: 模板文件与产物的对应关系
- **WHEN** 一个产物文件有对应的模板
- **THEN** 该关系为 1:1 映射（一个产物文件对应一个模板文件）
- **AND** 多个 Skill 可能输出相同格式的文件时共享同一模板（如 .status.md 被多个阶段更新）

### Requirement: 模板覆盖范围

系统 SHALL 为所有独立文件产物提供模板。

#### Scenario: 需要模板的产物
- **WHEN** 阶段产出是一个独立的 Markdown 文件
- **THEN** 该产物必须有对应模板
- **AND** 以下产物除外：prototype.pen（Pencil 工具生成）、迁移 SQL 脚本（内容为 DDL/DML）、代码文件（无固定模板结构）

#### Scenario: 非文件产物不需要模板
- **WHEN** 阶段产出仅为会话输出（如 kflow-status 的状态汇总）
- **THEN** 该产出不需要独立模板文件
- **AND** 其输出格式在 Skill spec 中直接定义

### Requirement: 模板维护规则

当 Skill spec 变更影响产物格式时，SHALL 同步更新关联模板。

#### Scenario: 产物格式变更时更新模板
- **WHEN** Skill 的产物输出格式发生变更
- **THEN** 对应模板文件的版本号递增
- **AND** 模板文件的修订记录区记录变更内容
