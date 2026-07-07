## ADDED Requirements

### Requirement: Subagent enforcement notice in SKILL.md header

All 7 execution-phase SKILL.md files SHALL include a prominent subagent enforcement notice immediately after the "Role" section, before any other content.

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

The project `.claude/settings.json` SHALL pre-configure permissions required by kflow Skills to prevent subagent execution failures due to missing permissions.

#### Scenario: Settings.json contains kflow permissions

- **WHEN** `.claude/settings.json` is read
- **THEN** it SHALL include an `allow` list containing:
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
