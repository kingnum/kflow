# inter-round-summary Specification

## Purpose

定义全部多轮审查机制（执行类重复制**与**设计自审 SELFREV）的轮次间摘要格式与使用方式，使主 Agent 在每轮结束后归纳已修复问题、未解决问题、覆盖率变化与下轮重点建议，并将其注入下一轮子代理提示，从而优化后续轮次的注意力分配；设计自审 SHALL NOT 被排除在轮间摘要注入之外。摘要同时提供见证轮候选须复核的前轮修复清单。

## Requirements

### Requirement: Inter-round summary format
The system SHALL define a standard inter-round summary format used by **all multi-round review mechanisms**: execution-phase repetition mode and design-phase self-review (SELFREV) in kflow-explore, kflow-prototype-design, kflow-design, and kflow-plan. After each round, the main Agent SHALL extract a summary containing: fixed issues, unresolved issues, coverage changes, and next-round focus suggestions. Design-phase self-review SHALL NOT be excluded from inter-round summary injection.

#### Scenario: Summary generated after each round
- **WHEN** any repetition mode or design self-review round completes
- **THEN** the main Agent SHALL generate an inter-round summary in the defined format

#### Scenario: Summary injected into next round prompt
- **WHEN** the next round subagent is constructed
- **THEN** its prompt SHALL include the inter-round summary from the previous round
- **AND** this SHALL apply to design-phase SELFREV rounds from round 2 onward, not only to execution-phase repetition mode

### Requirement: Subagent uses summary for attention optimization
Subagents receiving an inter-round summary SHALL use it to optimize attention allocation — fast regression check for fixed items, focused analysis for unresolved items, full check for untouched items. The summary SHALL NOT reduce the coverage scope of any work item, and SHALL supply the list of prior-round fixes that a witness-round candidate must verify.

#### Scenario: Later rounds more efficient
- **WHEN** a later-round subagent receives an inter-round summary
- **THEN** it SHALL allocate more attention to unresolved items and less to confirmed-fixed items
- **AND** SHALL still perform a full check on untouched items
- **AND** when the round is a witness-round candidate (zero new findings and zero modifications), it SHALL verify every prior-round fix listed in the summary, and SHALL NOT be judged a witness round if any such fix fails verification
