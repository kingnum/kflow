# skill-self-contained Specification

## Purpose

本能力定义 KFlow Skill 的自包含结构，规定每个 Skill 均含 `references/` 子目录以承载原集中于 `kflow-shared/` 的辅助规则，安装后不依赖任何外部目录，并规定共享文件按引用数量分发且内容按阶段裁剪。

## Requirements

### Requirement: Skill directory structure includes references subdirectory
Each KFlow Skill SHALL contain a `references/` subdirectory within its skill directory. The `references/` directory SHALL contain all supporting rules that were previously stored in the centralized `kflow-shared/` directory.

#### Scenario: Skill directory layout after refactor
- **WHEN** a KFlow Skill is installed via `npx skills add`
- **THEN** the skill directory SHALL contain both `SKILL.md` and `references/`
- **AND** `references/` SHALL contain only the files required by that specific skill

#### Scenario: Zero external dependency after installation
- **WHEN** a KFlow Skill is loaded in a consumer project
- **THEN** the skill SHALL NOT depend on the existence of a `kflow-shared/` directory at the project root
- **AND** rule files under the skill's own `references/` SHALL be self-contained within that skill
- **AND** a cross-skill reference SHALL be permitted only for (a) a shared executable script, such as `.claude/skills/kflow-code/scripts/with_server.py`, or (b) a rule file owned by a single skill and referenced by name from other skills, such as `.claude/skills/kflow-init/references/permission-model.md`
- **AND** every cross-skill reference path SHALL resolve to a file that exists in the installed layout

### Requirement: Shared file distribution by reference count
Each shared file from the former `kflow-shared/` directory SHALL be distributed to the `references/` subdirectory of every skill that references it. Files referenced by only one skill SHALL be placed solely in that skill's `references/`.

#### Scenario: Multi-reference file distribution
- **WHEN** `repetition-model.md` is referenced by 8 execution-phase skills
- **THEN** each of the 8 skills SHALL have its own copy at `references/repetition.md`

#### Scenario: Single-reference file distribution
- **WHEN** `recovery-protocol.md` is referenced only by `kflow-resume`
- **THEN** only `kflow-resume/references/recovery-protocol.md` SHALL exist

### Requirement: references content is phase-specific
When a shared file is distributed to multiple skills, each skill's copy SHALL contain only the sections relevant to that skill's phase. For example, `references/hooks.md` in `kflow-code` SHALL contain only the `code` phase PRE_HOOK and POST_HOOK sections, not hooks for other phases.

#### Scenario: Phase-specific hook file
- **WHEN** `kflow-code/references/hooks.md` is read
- **THEN** it SHALL contain only the code phase PRE_HOOK and POST_HOOK content
- **AND** it SHALL NOT contain hook content for other phases like plan or api-test

### Requirement: with_server.py relocated to kflow-code
The `with_server.py` script from `kflow-shared/scripts/` SHALL be relocated to `skills/kflow-code/scripts/with_server.py`. All skills that reference this script (api-test, e2e-test, integration-test) SHALL update their reference paths accordingly.

#### Scenario: with_server.py path update
- **WHEN** `kflow-e2e-test` needs to start a service
- **THEN** it SHALL reference `skills/kflow-code/scripts/with_server.py` (dev) or `.claude/skills/kflow-code/scripts/with_server.py` (consumer)
