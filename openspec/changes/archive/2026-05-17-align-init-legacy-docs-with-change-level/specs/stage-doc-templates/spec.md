## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: 产品级 functional-designs/{module}.md 需要模板

- **WHEN** 产品级功能设计模块文档需要生成
- **THEN** 该产物必须有对应模板
- **AND** 前后端项目使用 index.md + part-NN.md 目录化模板，章节结构与变更级 functional-designs/part-NN.md 一致
- **AND** 纯后端项目使用 backend-domain.md 简化模板
- **AND** 额外包含来源标注字段（来源变更 + 归档时间）

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

## REMOVED Requirements

### Requirement: functional-designs 分册模板扩展

**Reason**: 该需求已合并到产品级 functional-designs 目录化模板体系中，章节扩展属于模板本身的结构定义

**Migration**: 使用新的 `templates/design-templates/functional-designs/part-NN.md` 模板（产品级），已包含所有扩展章节
