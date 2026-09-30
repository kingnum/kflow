# Spec Delta

## ADDED Requirements

### Requirement: 打包范围与排除规则（自包含 Skill 目录）

系统 SHALL 扫描 `.claude/skills/kflow-*` 目录，包含所有运行时 Skills 的完整文件（含 `scripts/` 子目录），排除 `kflow-skills-auditor`。

#### Scenario: 扫描并收集 Skills 文件

- **WHEN** 执行打包流程
- **THEN** 系统扫描 `.claude/skills/kflow-*/` 下所有目录
- **AND** 收集范围为所有 `kflow-*` Skills，每个 Skill 自包含其 `references/` 与 `scripts/`
- **AND** 收集范围 SHALL NOT 包含独立的 `kflow-shared/` 目录
- **AND** 每个 Skill 目录下所有文件均纳入打包（SKILL.md + references/ + scripts/ + 其他附属文件）

#### Scenario: 运行时脚本随 kflow-code 分发

- **WHEN** 打包包含 `kflow-code` 的目录
- **THEN** 系统纳入 `skills/kflow-code/scripts/` 目录下所有文件
- **AND** 包含 `with_server.py` 等服务生命周期管理脚本
- **AND** 保持 `scripts/` 相对该 Skill 目录的位置不变

#### Scenario: 排除 kflow-skills-auditor

- **WHEN** 扫描 Skills 目录
- **THEN** `kflow-skills-auditor` 目录被排除，不纳入打包

#### Scenario: ZIP 包中各 Skill 的自包含结构

- **WHEN** 解压生成的 zip 文件
- **THEN** 每个 `kflow-*/` 目录 SHALL 包含自身的 `references/` 子目录
- **AND** `kflow-code/` SHALL 额外包含 `scripts/` 目录，其中含 `with_server.py`
- **AND** 解压结果 SHALL NOT 包含 `kflow-shared/` 目录

#### Scenario: 安装后脚本可执行

- **WHEN** 用户将 zip 内容解压到目标项目 `.claude/skills/` 目录
- **THEN** 路径 `.claude/skills/kflow-code/scripts/with_server.py` 存在且可执行
- **AND** 执行 `python .claude/skills/kflow-code/scripts/with_server.py --help` 输出帮助信息
- **AND** 各 skill `references/service-lifecycle.md` 中的引用路径与实际文件位置一致

## MODIFIED Requirements

### Requirement: ZIP 包结构与内容

打包产物 SHALL 为位于 `targets/` 目录下的 ZIP 文件，命名格式为 `kflow-devflow-skills-x.x.x.zip`，内部根目录为 `kflow-devflow-skills-x.x.x/`。

#### Scenario: 生成标准 ZIP 结构

- **WHEN** 打包执行
- **THEN** 系统在 `targets/` 目录下生成 `kflow-devflow-skills-x.x.x.zip`
- **AND** zip 内部根目录名为 `kflow-devflow-skills-x.x.x/`
- **AND** 根目录下包含 `VERSION.txt` 文件
- **AND** 根目录下包含所有 Skills 子目录，每个子目录自包含其 `references/`（及 `kflow-code` 的 `scripts/`）

#### Scenario: VERSION.txt 内容

- **WHEN** 生成 VERSION.txt 文件
- **THEN** 文件内容包含版本号（`x.x.x`）
- **AND** 包含构建时间（`YYYY-MM-DD HH:MM` 格式）
- **AND** 包含来源变更名称（如 `skill-packaging-and-version-unification`）

#### Scenario: 目标项目可安装

- **WHEN** 用户解压 zip 文件到目标项目的 `.claude/skills/` 目录
- **THEN** 所有 Skills 的文件结构保持完整
- **AND** 每个 Skill 的 `references/` 文件位于正确位置
- **AND** 运行 `/kflow-init` 可正常扫描并初始化

## REMOVED Requirements

### Requirement: 打包范围与排除规则

**Reason**: 该需求中「收集范围包含所有 kflow-* Skills（含 kflow-shared）」「ZIP 包中 kflow-shared 结构」等场景以已不存在的 `kflow-shared/` 目录为前提，其场景名本身即以该目录命名。`kflow-shared/` 已在 `2026-07-04-skill-self-contained-refactor` 中移除，需求描述与场景命名均已失效。

**Migration**: 由本能力新增的「打包范围与排除规则（自包含 Skill 目录）」取代，打包范围改为各 `kflow-*` Skill 自包含其 `references/`（`kflow-code` 额外含 `scripts/`），并明确排除独立的 `kflow-shared/` 目录。
