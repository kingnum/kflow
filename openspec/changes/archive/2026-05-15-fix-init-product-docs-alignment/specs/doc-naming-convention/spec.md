## ADDED Requirements

### Requirement: 产品级功能设计文档目录化

系统 SHALL 将产品级功能设计文档组织为 `docs/designs/functional-designs/` 目录结构。

#### Scenario: 产品级 functional-designs 目录

- **WHEN** 产品级功能设计文档首次创建
- **THEN** 输出目录为 `docs/designs/functional-designs/`
- **AND** 目录内包含 index.md（模块导航索引）+ 至少一个 {module}.md
- **AND** {module}.md 按功能模块以 kebab-case 命名

#### Scenario: 功能模块命名

- **WHEN** 归档时需要确定功能模块归属
- **THEN** 模块名 SHALL 与产品菜单项/功能分组对齐
- **AND** 使用 kebab-case 格式（如 `user-registration-login`、`order-management`）
- **AND** 避免使用抽象的 domain 名称

### Requirement: 产品级技术设计文档目录化

系统 SHALL 将产品级技术设计文档组织为 `docs/designs/technical-designs/` 目录结构。

#### Scenario: 产品级 technical-designs 目录

- **WHEN** 产品级技术设计文档首次创建
- **THEN** 创建 `docs/designs/technical-designs/` 目录
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md

### Requirement: 产品级文档与变更级命名一致

产品级文档命名和内部章节结构 SHALL 与变更级保持一致。

#### Scenario: 功能设计章节一致

- **WHEN** 产品级 {module}.md 生成或合并
- **THEN** 内部章节结构与变更级 functional-designs/part-NN.md 一致
- **AND** 包含：功能点列表、功能点详细定义（优先级、用户故事、所属页面与菜单、可执行操作、表单项定义、业务规则、业务流程上下文、功能行为矩阵、交互约束）
- **AND** 合并时无需转换，按 FP-ID 直接追加

#### Scenario: 技术设计章节一致

- **WHEN** 产品级 technical-designs/ 文档更新
- **THEN** 内容章节与变更级 detailed-design.md 对应的技术设计章节一致
