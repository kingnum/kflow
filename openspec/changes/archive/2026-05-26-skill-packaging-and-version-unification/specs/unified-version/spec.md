## ADDED Requirements

### Requirement: 统一版本号文件

项目 SHALL 在仓库根目录维护 `VERSION` 文件，内容为三段式语义化版本号（`major.minor.patch`），作为整个 KFlow Skills 体系（16 个运行时 Skills）的统一版本标识。

#### Scenario: VERSION 文件初始创建

- **WHEN** 执行变更实现
- **THEN** 系统在仓库根目录创建 `VERSION` 文件
- **AND** 文件内容为 `0.0.1`

#### Scenario: 读取当前版本号

- **WHEN** 需要获取当前 Skills 体系版本号
- **THEN** 系统读取 `VERSION` 文件内容
- **AND** 解析为 `major.minor.patch` 三段整数

### Requirement: 版本自增判定

每次 `/opsx:archive` 归档完成后，系统 SHALL 分析归档的变更内容自动判定版本号递增级别。

#### Scenario: 新增 Skill 或核心机制触发 minor 递增

- **WHEN** 归档的变更包含新增 Skill、新增阶段、或核心运行机制变更
- **THEN** 版本号 minor 位 +1，patch 位归零
- **AND** 如 `0.0.1` → `0.1.0`

#### Scenario: Bug修复或文档更新触发 patch 递增

- **WHEN** 归档的变更包含 Bug修复、文档更新、重构、或 references/ 文件变更
- **AND** 不涉及新增 Skill 或核心机制
- **THEN** 版本号 patch 位 +1
- **AND** 如 `0.0.1` → `0.0.2`

#### Scenario: 无法判定时默认 patch 递增

- **WHEN** 系统无法明确判定变更性质归属
- **THEN** 默认执行 patch 位 +1
- **AND** 提示用户复核版本号

### Requirement: Major 版本手动确认

版本号的 Major 位（最左侧）SHALL 由用户手动决定，系统不得自动递增 Major 位。

#### Scenario: 用户决定升级 Major 版本

- **WHEN** 用户明确要求升级 Major 版本
- **THEN** 系统将 Major 位 +1，minor 和 patch 归零
- **AND** 如 `0.5.3` → `1.0.0`

#### Scenario: 非用户触发时 Major 不变

- **WHEN** 归档完成但用户未要求变更 Major 版本
- **THEN** 系统 SHALL NOT 自动递增 Major 位

### Requirement: SKILL.md 版本字段移除

16 个运行时 kflow-* Skills 的 SKILL.md 文件 SHALL 移除 frontmatter 中的独立 `version:` 字段，版本号由 VERSION 文件统一管理。

#### Scenario: 移除独立版本号

- **WHEN** 执行变更实现
- **THEN** 系统从以下 16 个 SKILL.md 中移除 `version:` 行：
  kflow-guide, kflow-explore, kflow-prototype-design, kflow-design,
  kflow-plan, kflow-code, kflow-code-review, kflow-api-test,
  kflow-e2e-test, kflow-integration-test, kflow-bug-fix, kflow-audit,
  kflow-archive, kflow-status, kflow-init, kflow-resume
- **AND** kflow-skills-auditor 的 `version:` 字段保留不变（不纳入统一版本管理）
- **AND** 非 kflow-* 的 Skills（openspec-*, skill-creator, huashu-design, frontend-design, ui-ux-pro-max）不受影响
