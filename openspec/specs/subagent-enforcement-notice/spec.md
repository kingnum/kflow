## ADDED Requirements

### Requirement: Subagent enforcement notice in SKILL.md header

All 7 execution-phase SKILL.md files SHALL include a prominent subagent enforcement notice immediately after the "Role" section, before any other content. The notice SHALL include a 5th rule for background permission failure fallback.

#### Scenario: Notice placement and visibility

- **WHEN** any execution-phase SKILL.md is read
- **THEN** immediately after the "# Role" section (or equivalent)
- **AND** before "# Tasks" or "# Gate Check" sections
- **THEN** there SHALL be a prominently formatted notice block (using blockquote with warning symbol)

#### Scenario: Notice content for all entry scenarios

- **WHEN** the subagent enforcement notice is read
- **THEN** it SHALL contain the following rules:
  1. Main work of this phase MUST be executed through Agent subagent; main Agent is responsible only for dispatch and acceptance
  2. Main Agent SHALL NOT directly execute phase main work, no exceptions
  3. Subagent SHOULD run in foreground mode (run_in_background=false recommended); background mode allowed only when permissions are pre-configured
  4. Applicable scenarios: direct trigger + triage route + other Skill invocation
  5. When background subagent fails due to permission issues, main Agent SHALL create a new foreground subagent to re-execute; main Agent SHALL NOT directly take over
- **AND** it SHALL reference `kflow-shared/repetition-model.md` §12

### Requirement: Notice applies to all entry scenarios

The subagent enforcement notice SHALL explicitly state that the rules apply regardless of how the Skill was invoked.

#### Scenario: Direct trigger scenario

- **WHEN** the Skill is triggered directly by user (e.g., /kflow-code)
- **THEN** the subagent enforcement rules SHALL apply

#### Scenario: Triage route scenario

- **WHEN** the Skill is invoked via kflow-bug-triage route (e.g., L4 route to kflow-bug-fix)
- **THEN** the subagent enforcement rules SHALL apply
- **AND** the main Agent SHALL NOT bypass subagent requirement due to triage context

#### Scenario: Other Skill invocation scenario

- **WHEN** the Skill is invoked by another Skill (e.g., kflow-resume triggering a phase)
- **THEN** the subagent enforcement rules SHALL apply

### Requirement: Permission pre-configuration

kflow-init SHALL 在目标项目中自动配置 kflow Skills 执行所需的权限（参见 `kflow-shared/permission-model.md`），取代之前要求项目手动预配置 `.claude/settings.json` 的方式。后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管。

#### Scenario: Settings.json contains kflow permissions

- **WHEN** `.claude/settings.json` is read after kflow-init has configured permissions
- **THEN** it SHALL include an `allow` list containing the permissions defined in `kflow-shared/permission-model.md`:
  - Bash commands for package managers (npm, yarn, pnpm, npx)
  - Bash commands for runtime (node)
  - Bash commands for version control (git)
  - Bash commands for HTTP requests (curl)
  - Bash commands for scripting (python, python3)
  - Read, Write, Edit (file operations)
  - Glob, Grep (code search)
  - Agent (subagent invocation)
  - WebFetch (documentation lookup)

#### Scenario: Subagent inherits pre-configured permissions

- **WHEN** a subagent is spawned during execution phase
- **THEN** the subagent SHALL inherit the pre-configured permissions from settings.json
- **AND** SHALL NOT require per-tool user approval during execution

#### Scenario: Permission configuration by kflow-init

- **WHEN** kflow-init executes the PERM_CONFIG step
- **THEN** kflow-init SHALL read `kflow-shared/permission-model.md` for the permission list
- **AND** SHALL configure `.claude/settings.json` according to the rules defined in `kflow-permission-model` capability
- **AND** the project SHALL NOT be required to manually pre-configure permissions

#### Scenario: Background subagent permission failure fallback

- **WHEN** a background subagent fails due to permission issues
- **THEN** the main Agent SHALL create a new foreground subagent (run_in_background=false) to re-execute the same task
- **AND** the main Agent SHALL NOT directly take over execution in the main Agent context
- **AND** the fallback SHALL NOT count toward the 3-retry limit for round-level retries

### Requirement: Foreground mode recommendation

The system SHALL recommend foreground mode for subagent execution while allowing background mode when permissions are confirmed.

#### Scenario: Default foreground mode

- **WHEN** an execution phase spawns a subagent
- **THEN** the default SHALL be foreground mode (run_in_background=false)
- **AND** this allows main Agent to perform round-by-round acceptance and inter-round summary extraction

#### Scenario: Background mode with pre-configured permissions

- **WHEN** permissions are pre-configured in settings.json
- **AND** the execution is long-running with no need for inter-round interaction
- **THEN** background mode (run_in_background=true) MAY be used
- **AND** the subagent SHALL still follow all execution rules

#### Scenario: No hard prohibition on background mode

- **WHEN** evaluating subagent execution rules
- **THEN** there SHALL NOT be a hard rule prohibiting background mode
- **AND** the choice between foreground/background SHALL be based on permission configuration and use case
