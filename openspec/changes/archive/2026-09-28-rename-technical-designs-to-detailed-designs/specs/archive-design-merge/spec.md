## RENAMED Requirements

- FROM: ### Requirement: 技术设计全景文档组织
- TO: ### Requirement: 详细设计全景文档组织

## MODIFIED Requirements

### Requirement: 归档时合并功能设计和详细设计

系统 SHALL 在归档时将变更级的功能设计、详细设计和原型设计合并到产品级文档。

#### Scenario: 合并功能设计

- **WHEN** 归档变更
- **THEN** 系统从 functional-designs/ 提取功能点清单、需求描述、验收标准
- **AND** 按功能点的"所属页面与菜单"信息定位目标产品级目录 `docs/designs/functional-designs/{一级菜单}/`
- **AND** 按 FP-ID 匹配：已存在则替换更新对应 part-NN.md 中的功能点章节，不存在则追加
- **AND** 更新目标目录的 index.md 分册总览

#### Scenario: 合并详细设计

- **WHEN** 归档变更
- **THEN** 系统从 detailed-design.md 提取各章节内容
- **AND** 合并到 docs/designs/detailed-designs/ 下对应 6 个文档（architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md）

#### Scenario: 合并原型设计

- **WHEN** 归档变更
- **AND** 变更包含 `prototype/` 目录（原型设计阶段非跳过）
- **THEN** 系统将变更原型合并到 `docs/prototype/`
- **AND** 新屏幕复制到 `screens/`，修改屏幕用户确认后覆盖
- **AND** 新组件复制到 `components/`，新 CSS 变量追加到 `design-tokens.css`
- **AND** 更新 `index.html` 导航

### Requirement: 详细设计全景文档组织

系统 SHALL 将详细设计全景文档放入 docs/designs/detailed-designs/ 目录，包含 6 个文件。

#### Scenario: 技术设计文档创建

- **WHEN** 归档时需要创建详细设计文档
- **THEN** 系统在 docs/designs/detailed-designs/ 下创建
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md
