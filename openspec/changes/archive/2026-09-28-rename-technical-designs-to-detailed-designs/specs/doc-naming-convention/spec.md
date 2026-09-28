## RENAMED Requirements

- FROM: ### Requirement: 产品级技术设计文档目录化
- TO: ### Requirement: 产品级详细设计文档目录化

## MODIFIED Requirements

### Requirement: 产品级详细设计文档目录化

系统 SHALL 将产品级详细设计文档组织为 `docs/designs/detailed-designs/` 目录结构，包含 6 个文件。

#### Scenario: 产品级 technical-designs 目录

- **WHEN** 产品级详细设计文档首次创建
- **THEN** 创建 `docs/designs/detailed-designs/` 目录
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md

### Requirement: 旧命名兼容期

系统 SHALL 在过渡期兼容读取旧命名格式的文件。

#### Scenario: 发现旧命名文件（功能设计）

- **WHEN** Skill 读取变更目录时发现 functional-design.md 而非 functional-designs/ 目录
- **THEN** 系统正常读取旧的 functional-design.md 单文件
- **AND** 提示用户文件命名已更新为目录结构，建议迁移

#### Scenario: 发现旧命名文件（测试用例）

- **WHEN** Skill 读取变更目录时发现 api-tests.md / e2e-tests.md / integration-tests.md 单文件
- **THEN** 系统正常读取旧单文件
- **AND** 提示用户文件命名已更新为目录结构，建议迁移

#### Scenario: 新旧文件同时存在

- **WHEN** 变更目录同时存在单文件和新目录结构
- **THEN** 系统优先读取新目录结构
- **AND** 提示用户清理旧的单文件

#### Scenario: 发现旧命名产品级目录（详细设计）

- **WHEN** Skill 读取产品级技术设计文档时发现 `docs/designs/technical-designs/` 而非 `docs/designs/detailed-designs/`
- **THEN** 系统兼容读取旧的 `technical-designs/` 目录
- **AND** 提示用户目录已重命名为 `detailed-designs/`，建议执行 `git mv` 迁移
