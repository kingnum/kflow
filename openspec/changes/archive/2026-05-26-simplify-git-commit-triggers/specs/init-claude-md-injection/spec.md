## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 在「变更流程强制规则」section 中新增 git commit 相关规则。使用现有 marker `## 变更流程强制规则` 幂等更新。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下 git 规则：
  - 首次 init 时，若目录非 git 仓库，询问是否执行 git init
  - 归档完成后，询问是否将当前变更及相关文件提交 git

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但不含 git 规则或 git 规则过时
- **THEN** 系统替换为包含最新 git 规则（2 条询问式）的版本
- **AND** 保留原有非 git 规则的内容结构

## REMOVED Requirements

### Requirement: 首次 init 后自动 git commit

**Reason**: init 阶段改为询问 git init，不再涉及 git commit。

**Migration**: 见 `devflow-init` spec 中对应的 init 规则修改。
