# Spec Delta

## MODIFIED Requirements

### Requirement: Inter-round summary format

The system SHALL define a standard inter-round summary format used by the execution-phase repetition mode phases only — namely 编码（kflow-code）、代码审查（kflow-code-review）与缺陷修复（kflow-bug-fix）。Design-phase self-review (SELFREV) in kflow-explore, kflow-prototype-design, kflow-design and kflow-plan SHALL NOT use the inter-round summary, and the test phases (接口单元测试 / E2E 测试 / 集成测试) SHALL NOT use it either. After each round, the main Agent SHALL extract a summary containing: fixed issues, unresolved issues, coverage changes, next-round focus suggestions, and an **out-of-scope observation** section (范围外观察).

#### Scenario: Summary generated after each round

- **WHEN** a repetition-mode round completes in kflow-code, kflow-code-review or kflow-bug-fix
- **THEN** the main Agent SHALL generate an inter-round summary in the defined format

#### Scenario: Summary injected into next round prompt

- **WHEN** the next round subagent is constructed for a repetition-mode phase
- **THEN** its prompt SHALL include the inter-round summary from the previous round
- **AND** this SHALL NOT apply to design-phase SELFREV, kflow-plan self-review, or the test phases

#### Scenario: Unverified-fix list accumulates across multiple rounds

- **WHEN** an execution phase has a further round pending
- **THEN** the summary SHALL NOT carry an accumulated unverified-fix list
- **AND** fixes SHALL be tracked by the phase's own execution report, not by the summary

#### Scenario: Verified fixes are removed from the list

- **WHEN** a round completes after fixing issues reported in a prior round
- **THEN** the summary's 「已修复问题」 field SHALL list those fixes as fixed
- **AND** no separate unverified-fix list SHALL be maintained

#### Scenario: Out-of-scope observations carried in the summary

- **WHEN** a round produces out-of-scope observations
- **THEN** the inter-round summary SHALL carry them in the 范围外观察 field
- **AND** subsequent rounds SHALL use them to avoid rediscovering the same out-of-scope content
- **AND** when the field is empty it SHALL be recorded as 「（空）」

### Requirement: Witness-round aligned summary consumption

Subagents receiving an inter-round summary SHALL use it to optimize attention allocation — fast regression check for fixed items, focused analysis for unresolved items, full check for untouched items. The summary SHALL NOT reduce the coverage scope of any work item.

#### Scenario: Later rounds more efficient

- **WHEN** a later-round subagent in a repetition-mode phase receives an inter-round summary
- **THEN** it SHALL allocate more attention to unresolved items and less to confirmed-fixed items
- **AND** SHALL still perform a full check on untouched items
- **AND** the summary SHALL NOT reduce the coverage scope of any work item

#### Scenario: Witness-round candidate consumes the accumulated list

- **WHEN** a subagent receives an inter-round summary
- **THEN** it SHALL NOT be required to verify any accumulated unverified-fix list
- **AND** it SHALL still perform a full traversal of all work items in its round
