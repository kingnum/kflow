# inter-round-summary Specification

## Purpose

定义重复执行模式（repetition mode）的轮次间摘要格式与使用方式，使主 Agent 在每轮结束后归纳已修复问题、未解决问题、覆盖率变化与下轮重点建议，并将其注入下一轮子代理提示，从而优化后续轮次的注意力分配。

## Requirements

### Requirement: Inter-round summary format
The system SHALL define a standard inter-round summary format for repetition mode. After each round, the main Agent SHALL extract a summary containing: fixed issues, unresolved issues, coverage changes, and next-round focus suggestions.

#### Scenario: Summary generated after each round
- **WHEN** a repetition mode round completes
- **THEN** the main Agent SHALL generate an inter-round summary in the defined format

#### Scenario: Summary injected into next round prompt
- **WHEN** the next round subagent is constructed
- **THEN** its prompt SHALL include the inter-round summary from the previous round

### Requirement: Subagent uses summary for attention optimization
Subagents receiving an inter-round summary SHALL use it to optimize attention allocation — fast regression check for fixed items, focused analysis for unresolved items, full check for untouched items.

#### Scenario: Later rounds more efficient
- **WHEN** round 5+ subagent receives inter-round summary
- **THEN** it SHALL allocate more attention to unresolved items and less to confirmed-fixed items
