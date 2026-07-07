## MODIFIED Requirements

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

### Requirement: 模板覆盖范围

系统 SHALL 为所有独立文件产物提供模板，新增 product/functional-designs/{module}.md 模板。

#### Scenario: 需要模板的产物

- **WHEN** 阶段产出是一个独立的 Markdown 文件
- **THEN** 该产物必须有对应模板
- **AND** 以下产物除外：prototype.pen（Pencil 工具生成）、迁移 SQL 脚本（内容为 DDL/DML）、代码文件（无固定模板结构）

#### Scenario: 产品级 functional-designs/{module}.md 需要模板

- **WHEN** 产品级功能设计模块文档需要生成
- **THEN** 该产物必须有对应模板
- **AND** 模板章节结构与变更级 functional-designs/part-NN.md 一致
- **AND** 额外包含来源标注字段（来源变更 + 归档时间）

### Requirement: 模板维护规则

当 Skill spec 变更影响产物格式时，SHALL 同步更新关联模板。

#### Scenario: 产物格式变更时更新模板

- **WHEN** Skill 的产物输出格式发生变更
- **THEN** 对应模板文件的版本号递增
- **AND** 模板文件的修订记录区记录变更内容
- **AND** 若产物路径变更，模板文件路径同步更新

## ADDED Requirements

### Requirement: 模板路径与产物路径镜像

模板目录的子目录结构 SHALL 镜像实际 `docs/` 输出结构。

#### Scenario: 查找模板

- **WHEN** 需要查找某产物对应的模板
- **THEN** 模板路径为：`templates/{产物路径}`
- **AND** 目录型产物的模板使用相同目录名（如 `templates/changes/{change}/functional-designs/`）
- **AND** 文件型产物的模板直接对应（如 `templates/docs/service-guide.md`）

#### Scenario: 模板重组迁移

- **WHEN** 模板目录结构从抽象分层迁移到镜像结构
- **THEN** 系统保留旧模板目录作为迁移参考
- **AND** 更新 templates/index.md 中的模板路径
