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

When a shared file is distributed to multiple skills, each skill's copy SHALL contain only the sections relevant to that skill's phase. This SHALL apply to every shared references file, not only `references/hooks.md`: `gates.md`, `state-values.md`, `repetition.md`, `self-review.md`, `phase-transition.md`, and `service-lifecycle.md` SHALL each be sliced by phase before distribution. A distributed copy SHALL NOT contain sections belonging to phases other than its owning skill's phase.

#### Scenario: Phase-specific hook file

- **WHEN** `kflow-code/references/hooks.md` is read
- **THEN** it SHALL contain only the code phase PRE_HOOK and POST_HOOK content
- **AND** it SHALL NOT contain hook content for other phases like plan or api-test

#### Scenario: Phase-specific gate file

- **WHEN** `kflow-code/references/gates.md` is read
- **THEN** it SHALL contain the gate-annotation conventions and the code phase's forward-gate, fallback-gate, and upstream-issue-decision sections
- **AND** it SHALL NOT contain gate sections belonging to other phases (如代码审查闭环、缺陷修复快车道、HITL 阻塞 plan 入口)

#### Scenario: Phase-specific repetition file

- **WHEN** `kflow-code/references/repetition.md` is read
- **THEN** it SHALL contain the execution model, subagent prompt norms, isolation rules, and inter-round summary mechanism applicable to the code phase
- **AND** it SHALL NOT contain phase-specific sections that apply only to other phases

#### Scenario: Phase-specific state-value and self-review files

- **WHEN** `kflow-code/references/state-values.md` or a design-phase skill's `references/self-review.md` is read
- **THEN** the former SHALL contain only the state values produced or consumed by the code phase
- **AND** the latter SHALL contain only the self-review dimensions of its owning design-phase skill

#### Scenario: 副本切片后不再与同源副本逐字节相同

- **WHEN** 切片完成后对两个不同 skill 目录下的同名 references 文件作比对
- **THEN** 两者的正文内容 SHALL 存在实质差异（各自仅含本阶段章节）
- **AND** SHALL NOT 为逐字节完全相同的副本
### Requirement: with_server.py relocated to kflow-code
The `with_server.py` script from `kflow-shared/scripts/` SHALL be relocated to `skills/kflow-code/scripts/with_server.py`. All skills that reference this script (api-test, e2e-test, integration-test) SHALL update their reference paths accordingly.

#### Scenario: with_server.py path update
- **WHEN** `kflow-e2e-test` needs to start a service
- **THEN** it SHALL reference `skills/kflow-code/scripts/with_server.py` (dev) or `.claude/skills/kflow-code/scripts/with_server.py` (consumer)

### Requirement: 切片副本的单一权威源与生成

共享 references 文件 SHALL 由 `scripts/sync-references.sh` 从各 skill 目录下的切片结果生成与校验，使开发期以单一权威源维护、安装期仍为各 skill 自包含的完整副本。

#### Scenario: 开发期单一权威源

- **WHEN** 需要修改一条被多个 skill 引用的规则
- **THEN** 修改 SHALL 发生在该规则的权威源位置
- **AND** 各 skill 的切片副本 SHALL 由脚本生成，SHALL NOT 逐一手工编辑

#### Scenario: 生成物保持自包含

- **WHEN** `scripts/package-skills.sh` 打包
- **THEN** 每个 skill 的 `references/` SHALL 仍包含其运行所需的全部文件
- **AND** 安装后的 skill SHALL NOT 依赖任何跨 skill 共享目录

#### Scenario: 校验生成物与权威源一致

- **WHEN** `scripts/sync-references.sh` 运行
- **THEN** 它 SHALL 校验各 skill 的切片副本与权威源对应的阶段切片一致
- **AND** 不一致时 SHALL 以非零退出码报告差异位置

#### Scenario: 共享只在开发期发生

- **WHEN** 判定共享边界
- **THEN** 权威源与切片生成 SHALL 仅存在于 KFlow Skills 源码仓库的开发期
- **AND** 消费者项目中安装的 skill 目录 SHALL NOT 出现任何指向仓库内其他位置的共享引用

### Requirement: 引用加载清单不含无效条目

各执行类阶段的子代理 prompt SHALL 只要求加载子代理实际需要且会实际执行的 references 文件；经实测确认执行率为零或显著偏低的引用条目 SHALL 被移除。

#### Scenario: 移除零执行的引用条目

- **WHEN** 子代理 prompt 构造引用加载清单
- **THEN** SHALL NOT 要求子代理读取其自身 skill 的 `SKILL.md`
- **AND** SHALL NOT 要求加载与该子代理职责无关的 references 文件

#### Scenario: 引用条目的有效性验证

- **WHEN** 一条引用加载要求被写入子代理 prompt
- **THEN** 该要求对应的文件内容 SHALL 对子代理完成其任务为必需
- **AND** 若子代理在不读取该文件的情况下仍能完成任务，该条目 SHALL 被重新评估
