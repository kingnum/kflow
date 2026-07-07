## MODIFIED Requirements

### Requirement: Layered context loading strategy
The system SHALL define a layered context loading strategy for subagent invocations. The sources for each loading tier SHALL reside in the skill's own `references/` subdirectory. Subagent prompts SHALL load only the tiers relevant to the current phase.

#### Scenario: Loading tier annotation
- **WHEN** any references file is loaded for a subagent
- **THEN** the file SHALL be loaded from `.claude/skills/<skill-name>/references/` (consumer) or `skills/<skill-name>/references/` (dev)
- **AND** the loading instruction in SKILL.md SHALL list the specific references files and their tiers

#### Scenario: Execution phase subagent loads only relevant tiers
- **WHEN** a code phase subagent is constructed
- **THEN** its prompt SHALL instruct loading of 基础层 + 执行层 from the skill's own `references/` directory
- **AND** SHALL NOT load files from any external shared directory

#### Scenario: No reference to kflow-shared in loading instructions
- **WHEN** any KFlow Skill constructs a subagent prompt
- **THEN** the loading instructions SHALL NOT reference `kflow-shared/`
- **AND** all file paths SHALL point to the skill's own `references/` directory

## REMOVED Requirements

### Requirement: Shared file loading tier annotation in kflow-shared headers
**Reason**: `kflow-shared/` directory is removed. Loading tier annotations are now implicit based on which `references/` files a skill includes.
**Migration**: Each skill's SKILL.md SHALL document which `references/` files belong to which loading tier in its subagent construction instructions.
