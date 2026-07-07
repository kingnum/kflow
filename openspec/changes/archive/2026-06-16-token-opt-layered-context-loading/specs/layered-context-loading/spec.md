## ADDED Requirements

### Requirement: Layered context loading strategy
The system SHALL define a layered context loading strategy for subagent invocations. Each core mechanism document and kflow-shared file SHALL be annotated with a loading tier. Subagent prompts SHALL load only the tiers relevant to the current phase.

#### Scenario: Loading tier annotation
- **WHEN** any core mechanism or kflow-shared file is read
- **THEN** its header SHALL contain a "加载层级" annotation (基础层/执行层/服务层/创意层)

#### Scenario: Execution phase subagent loads only relevant tiers
- **WHEN** a code phase subagent is constructed
- **THEN** its prompt SHALL load 基础层 + 执行层, but NOT 服务层 or 创意层
