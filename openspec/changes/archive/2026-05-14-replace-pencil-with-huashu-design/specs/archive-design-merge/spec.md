## MODIFIED Requirements

### Requirement: 归档时合并功能设计和详细设计

系统 SHALL 在归档时将变更级的功能设计、详细设计和原型设计合并到产品级文档。

#### Scenario: 合并功能设计
- **WHEN** 归档变更
- **THEN** 系统从 functional-design.md 提取功能点清单、需求描述、验收标准
- **AND** 合并到 docs/designs/domains/{domain}.md 的功能设计章节

#### Scenario: 合并详细设计
- **WHEN** 归档变更
- **THEN** 系统从 detailed-design.md 提取设计域章节、数据模型、接口设计
- **AND** 合并到 docs/designs/domains/{domain}.md 的技术设计章节
- **AND** 更新全景文档（architecture.md, data-model.md, api-catalog.md, nfr-baseline.md）

#### Scenario: 合并原型设计
- **WHEN** 归档变更
- **AND** 变更包含 `prototype/` 目录（原型设计阶段非跳过）
- **THEN** 系统将变更原型合并到 `docs/prototype/`
- **AND** 新屏幕复制到 `screens/`，修改屏幕用户确认后覆盖
- **AND** 新组件复制到 `components/`，新 CSS 变量追加到 `design-tokens.css`
- **AND** 更新 `index.html` 导航



