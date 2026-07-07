## Purpose

定义阶段产物模板体系，包括模板目录结构、模板文件格式规范、模板与 Skill spec 的引用关系、模板覆盖范围和维护规则，以及自审轮次报告模板。
## Requirements
### Requirement: 模板目录结构

系统 SHALL 在 `docs/designs/templates/` 目录下镜像实际 `docs/` 输出结构组织模板文件。

#### Scenario: 模板目录创建
- **WHEN** 模板体系首次初始化
- **THEN** 系统创建 `docs/designs/templates/index.md` 作为模板目录索引入口
- **AND** 按实际产物路径组织子目录，而非抽象分层（change/product/subchange/integration/infra）
- **AND** 模板路径与产物路径形成直接映射（如产物 `docs/service-guide.md` → 模板 `templates/docs/service-guide.md`）

#### Scenario: 索引入口格式
- **WHEN** templates/index.md 被创建或更新
- **THEN** 文件列出各模板子目录及其覆盖的产物类型
- **AND** 列出完整模板清单（模板文件路径 + 对应产物路径 + 产出 Skill）

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

系统 SHALL 为所有独立文件产物提供模板，新增自审轮次报告模板。

#### Scenario: 需要模板的产物
- **WHEN** 阶段产出是一个独立的 Markdown 文件
- **THEN** 该产物必须有对应模板
- **AND** 以下产物除外：prototype.pen（Pencil 工具生成）、迁移 SQL 脚本（内容为 DDL/DML）、代码文件（无固定模板结构）
- **AND** 新增 config-items.md、error-handling.md、backend-domain.md 必须有对应模板

#### Scenario: 自审报告需要模板
- **WHEN** 阶段产出包含 self-reviews/{phase}/{timestamp}.md
- **THEN** 该产物必须有对应的自审报告模板
- **AND** 模板按阶段提供维度差异版本

### Requirement: 产品级 functional-designs 目录化模板

系统 SHALL 为产品级 functional-designs 的目录结构提供完整模板。

#### Scenario: 菜单索引模板
- **WHEN** 产品级 functional-designs 按菜单目录组织
- **THEN** 提供 `templates/design-templates/functional-designs/index.md` 模板
- **AND** 模板包含本模块功能点清单、分册总览、修订记录

#### Scenario: 产品级分册模板
- **WHEN** 产品级 functional-designs 需要分册文件
- **THEN** 提供 `templates/design-templates/functional-designs/part-NN.md` 模板
- **AND** 模板章节结构与变更级 part-NN.md 一致，额外增加来源标注字段

#### Scenario: 纯后端简化模板
- **WHEN** 纯后端项目需要功能设计文档模板
- **THEN** 提供 `templates/design-templates/functional-designs/backend-domain.md` 模板
- **AND** 模板使用简化章节结构（设计域替代页面菜单、接口参数定义替代表单项、调用约束替代交互约束）

### Requirement: 新增技术设计模板

系统 SHALL 为 config-items.md 和 error-handling.md 提供模板。

#### Scenario: 配置项设计模板
- **WHEN** config-items.md 需要生成
- **THEN** 提供 `templates/design-templates/technical-designs/config-items.md` 模板
- **AND** 模板格式与 detailed-design.md §五配置项设计一致

#### Scenario: 错误处理设计模板
- **WHEN** error-handling.md 需要生成
- **THEN** 提供 `templates/design-templates/technical-designs/error-handling.md` 模板
- **AND** 模板格式与 detailed-design.md §六错误处理设计一致

### Requirement: 模板路径与产物路径镜像

模板目录的子目录结构 SHALL 镜像实际 `docs/` 输出结构。

#### Scenario: 查找模板
- **WHEN** 需要查找某产物对应的模板
- **THEN** 模板路径为：`templates/{产物路径}`
- **AND** 目录型产物的模板使用相同目录名（如 `templates/changes/{change}/functional-designs/`）
- **AND** 文件型产物的模板直接对应（如 `templates/docs/service-guide.md`）

### Requirement: 模板维护规则

当 Skill spec 变更影响产物格式时，SHALL 同步更新关联模板。

#### Scenario: 产物格式变更时更新模板
- **WHEN** Skill 的产物输出格式发生变更
- **THEN** 对应模板文件的版本号递增
- **AND** 模板文件的修订记录区记录变更内容
- **AND** 若产物路径变更，模板文件路径同步更新

### Requirement: 自审轮次报告模板

系统 SHALL 为 self-reviews/ 下的自审记录提供轮次报告模板。

#### Scenario: 自审报告模板结构
- **WHEN** 创建自审报告模板
- **THEN** 模板包含审查维度得分表（维度名、本轮得分、上轮得分、变化）
- **AND** 包含新发现问题清单（序号、问题描述、严重度、状态）
- **AND** 包含上轮问题修复验证（序号、上轮问题、修复结果）
- **AND** 包含本轮改进内容章节
- **AND** 包含仍存在问题章节
- **AND** frontmatter 包含 stage、phase、timestamp、dimensions 字段

#### Scenario: 不同阶段的自审报告维度差异
- **WHEN** 模板用于不同阶段
- **THEN** explores 阶段使用完整性/闭环性/必要性/清晰性维度
- **AND** prototype 阶段使用覆盖性/一致性/可用性/完整性维度
- **AND** design 阶段使用一致性/完备性/可行性/可测性维度

