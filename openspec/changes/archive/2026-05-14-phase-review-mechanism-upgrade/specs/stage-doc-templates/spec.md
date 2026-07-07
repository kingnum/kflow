# stage-doc-templates (Delta)

## ADDED Requirements

### Requirement: functional-designs 分册模板扩展

functional-designs/part-NN.md 模板 SHALL 新增页面导航、可执行操作、表单项定义、业务规则章节。

#### Scenario: 分册模板新章节
- **WHEN** 读取 functional-designs/part-NN.md 模板
- **THEN** 模板包含"所属页面与菜单"章节（页面名、菜单路径、入口条件）
- **AND** 包含"可执行操作"章节（操作名、触发方式、可见条件）
- **AND** 包含"表单项定义"章节（字段名、类型、校验规则、默认值、提示文本）
- **AND** 包含"业务规则"章节（前置条件、校验规则、触发条件、后置结果）
- **AND** 包含"业务流程上下文"章节（在流程中的位置、上下游操作）

#### Scenario: 功能点 ID 作为锚点
- **WHEN** 分册模板定义功能点结构
- **THEN** 每个功能点使用固定的章节结构
- **AND** 功能点 ID 作为主锚点，所有子信息围绕功能点 ID 组织

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

## MODIFIED Requirements

### Requirement: 模板覆盖范围

系统 SHALL 为所有独立文件产物提供模板，新增自审轮次报告模板。

#### Scenario: 需要模板的产物
- **WHEN** 阶段产出是一个独立的 Markdown 文件
- **THEN** 该产物必须有对应模板
- **AND** 以下产物除外：prototype.pen（Pencil 工具生成）、迁移 SQL 脚本（内容为 DDL/DML）、代码文件（无固定模板结构）

#### Scenario: 自审报告需要模板
- **WHEN** 阶段产出包含 self-reviews/{phase}/{timestamp}.md
- **THEN** 该产物必须有对应的自审报告模板
- **AND** 模板按阶段提供维度差异版本
