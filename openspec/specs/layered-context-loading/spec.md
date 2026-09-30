# layered-context-loading Specification

## Purpose

本能力定义子代理调用的分层上下文加载策略，规定各加载层级的来源文件位于各 Skill 自身的 `references/` 目录内，子代理 prompt 仅加载当前阶段相关的层级，且不得依赖任何外部共享目录。

## Requirements

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
