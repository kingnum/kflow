# Spec Delta

## MODIFIED Requirements

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

**Reason**: 原场景要求「the skill SHALL NOT reference any file outside `.claude/skills/<skill-name>/`」，与该能力自身的「with_server.py relocated to kflow-code」需求直接冲突——后者明文要求 api-test / e2e-test / integration-test 引用 `kflow-code/scripts/with_server.py`。现实中已存在两类跨 Skill 引用：共享可执行脚本，以及单一所有者持有、被其他 Skill 说明性引用的规则文件（如 `permission-model.md` 由 kflow-init 持有，其他 Skill 的 `repetition.md` 说明「kflow-init 依据该文件配置权限」）。原场景把这些一并判为违规，使正确实现无法通过规格自检。

**Migration**: 跨 Skill 引用收敛为两类白名单（共享脚本、单一所有者规则文件），并新增「引用路径须在安装布局中真实存在」的断言。各 Skill 独占的规则文件仍受「自包含」约束，不受本次放宽影响。
