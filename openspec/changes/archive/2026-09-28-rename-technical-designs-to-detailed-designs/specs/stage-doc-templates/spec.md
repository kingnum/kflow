## RENAMED Requirements

- FROM: ### Requirement: 新增技术设计模板
- TO: ### Requirement: 新增详细设计模板

## MODIFIED Requirements

### Requirement: 新增详细设计模板

系统 SHALL 为 config-items.md 和 error-handling.md 提供模板。

#### Scenario: 配置项设计模板

- **WHEN** config-items.md 需要生成
- **THEN** 提供 `templates/design-templates/detailed-designs/config-items.md` 模板
- **AND** 模板格式与 detailed-design.md §五配置项设计一致

#### Scenario: 错误处理设计模板

- **WHEN** error-handling.md 需要生成
- **THEN** 提供 `templates/design-templates/detailed-designs/error-handling.md` 模板
- **AND** 模板格式与 detailed-design.md §六错误处理设计一致
