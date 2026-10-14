# Spec Delta

## ADDED Requirements

### Requirement: Witness-round aligned summary consumption

Subagents receiving an inter-round summary SHALL use it to optimize attention allocation — fast regression check for fixed items, focused analysis for unresolved items, full check for untouched items. The summary SHALL NOT reduce the coverage scope of any work item, and SHALL supply the accumulated list of unverified fixes that a witness-round candidate must verify (the witness-round condition (d)). The summary SHALL NOT be consumed by any recheck round.

#### Scenario: Later rounds more efficient

- **WHEN** a later-round subagent receives an inter-round summary
- **THEN** it SHALL allocate more attention to unresolved items and less to confirmed-fixed items
- **AND** SHALL still perform a full check on untouched items
- **AND** when the round is a witness-round candidate (zero new findings and zero modifications), it SHALL verify every unverified fix listed in the summary, and SHALL NOT be judged a witness round if any such fix fails verification

#### Scenario: Witness-round candidate consumes the accumulated list

- **WHEN** a witness-round candidate is constructed
- **THEN** its prompt SHALL include the accumulated unverified-fix list
- **AND** it SHALL verify every entry on that list
- **AND** SHALL NOT verify only the fixes from the immediately preceding round

## MODIFIED Requirements

### Requirement: Inter-round summary format

The system SHALL define a standard inter-round summary format used by **all multi-round review mechanisms**: execution-phase repetition mode and design-phase self-review (SELFREV) in kflow-explore, kflow-prototype-design, kflow-design, and kflow-plan. After each round, the main Agent SHALL extract a summary containing: fixed issues, unresolved issues, coverage changes, next-round focus suggestions, and an **out-of-scope observation** section (范围外观察). Design-phase self-review SHALL NOT be excluded from inter-round summary injection.

The summary SHALL additionally carry an **accumulated unverified-fix list**: every fix made by any round that has not yet been independently re-verified. A fix SHALL be removed from the list only when a round actually performs the re-verification of that fix. The list SHALL NOT be limited to the immediately preceding round, and SHALL NOT be limited to witness-round candidates — it SHALL be maintained across the whole review cycle and SHALL be consumed by the witness-round verification obligation (condition (d)).

#### Scenario: Summary generated after each round

- **WHEN** any repetition mode or design self-review round completes
- **THEN** the main Agent SHALL generate an inter-round summary in the defined format
- **AND** the summary SHALL include the accumulated unverified-fix list as of the end of that round

#### Scenario: Summary injected into next round prompt

- **WHEN** the next round subagent is constructed
- **THEN** its prompt SHALL include the inter-round summary from the previous round
- **AND** this SHALL apply to design-phase SELFREV rounds from round 2 onward, not only to execution-phase repetition mode

#### Scenario: Unverified-fix list accumulates across multiple rounds

- **WHEN** rounds 1 through N each produce fixes
- **AND** no round in that span performed re-verification (no round was a witness-round candidate)
- **THEN** the accumulated unverified-fix list SHALL contain the fixes from all rounds 1 through N
- **AND** the list SHALL NOT be truncated to the last round's fixes

#### Scenario: Verified fixes are removed from the list

- **WHEN** a round performs re-verification of some fixes in the list
- **THEN** those fixes SHALL be removed from the accumulated unverified-fix list
- **AND** the remaining entries SHALL stay on the list

#### Scenario: Out-of-scope observations carried in the summary

- **WHEN** a round produces out-of-scope observations
- **THEN** the inter-round summary SHALL carry them in the 范围外观察 field
- **AND** subsequent rounds SHALL use them to avoid rediscovering the same out-of-scope content
- **AND** when the field is empty it SHALL be recorded as 「（空）」

## REMOVED Requirements

### Requirement: Subagent uses summary for attention optimization

**Reason**: 该需求的「Recheck round consumes the accumulated list」场景以复检轮为前提；复检轮机制删除后该场景失去对象，其余注意力优化规则实质有效。

**Migration**: 迁移至本能力新增的 `Witness-round aligned summary consumption`——累积未复核修复清单的消费方由「终止判定 + 复检轮」改为见证轮第 (d) 项复核义务；见证轮判据的权威定义见 `convergence-driven-repetition` 能力。
