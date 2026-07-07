## MODIFIED Requirements

### Requirement: 产品级功能设计文档目录化

系统 SHALL 将产品级功能设计文档组织为 `docs/designs/functional-designs/` 目录结构，前后端项目按一级菜单划分子目录，纯后端项目按设计域创建简化文件。

#### Scenario: 产品级 functional-designs 目录（前后端项目）

- **WHEN** 产品级功能设计文档首次创建且项目为前后端
- **THEN** 输出目录为 `docs/designs/functional-designs/`
- **AND** 目录内按一级菜单组织：`{一级菜单}/index.md` + `{一级菜单}/part-NN.md`
- **AND** 一级菜单名使用 kebab-case 格式

#### Scenario: 产品级 functional-designs 目录（纯后端项目）

- **WHEN** 产品级功能设计文档首次创建且项目为纯后端
- **THEN** 输出目录为 `docs/designs/functional-designs/`
- **AND** 目录内按设计域组织：`{domain}.md` 平铺文件
- **AND** 使用 backend-domain-template 简化模板

#### Scenario: 功能模块命名（前后端项目）

- **WHEN** 归档时需要确定功能模块归属
- **THEN** 目录名 SHALL 使用对应的一级菜单项 kebab-case 名称
- **AND** 如菜单项为中文，转换为 kebab-case 拼音或英文翻译（如"系统管理"→`system-admin`）

#### Scenario: 功能模块命名（纯后端项目）

- **WHEN** 归档时需要确定功能模块归属
- **THEN** 文件名 SHALL 使用设计域的 kebab-case 名称
- **AND** 避免使用抽象的 domain 名称

### Requirement: 产品级技术设计文档目录化

系统 SHALL 将产品级技术设计文档组织为 `docs/designs/technical-designs/` 目录结构，包含 6 个文件。

#### Scenario: 产品级 technical-designs 目录

- **WHEN** 产品级技术设计文档首次创建
- **THEN** 创建 `docs/designs/technical-designs/` 目录
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md
