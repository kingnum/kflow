# Spec Delta

## MODIFIED Requirements

### Requirement: Triage impact assessment on diagnosis

kflow-bug-triage SHALL perform impact assessment as part of the diagnostic process, producing an impact scope evaluation that includes affected functional points, interfaces, data model changes, and an impact scope score. The impact scope score SHALL NOT be mapped to repetition rounds, and SHALL NOT be used as the change tier score.

#### Scenario: Impact assessment included in diagnostic report

- **WHEN** kflow-bug-triage completes four-layer root cause diagnosis
- **THEN** the diagnostic report (`{缺陷工作区}/bug-NNN-NNN.md`) SHALL include an "Impact Assessment" section containing:
  - Affected functional points list (e.g., FP-001, FP-003)
  - Affected interfaces list (e.g., `/api/orders/export`)
  - Data model changes (none / description of changes)
  - Impact scope score (calculated value)
  - Verification targets list
- **AND** the impact assessment SHALL be performed before route confirmation

#### Scenario: Impact score calculation

- **WHEN** the system calculates the impact scope score
- **THEN** the score SHALL be computed as: `score = functional_points × 1 + interfaces × 1.5 + data_model_changes × 2`
- **AND** functional_points count = number of affected functional points
- **AND** interfaces count = number of affected API endpoints
- **AND** data_model_changes = 1 if any data model modification exists, 0 otherwise

#### Scenario: Impact assessment for L1/L2/L3 routes

- **WHEN** triage routes to L1 (explore REVISION), L2 (prototype-design REVISION), or L3 (design REVISION)
- **THEN** the impact assessment SHALL be passed to the target phase via the change-level `.status.md` "Recent Revision Info" section
- **AND** downstream phases SHALL use the affected items list for the verification gate and the rollback decision
- **AND** downstream phases SHALL NOT use the impact scope score to determine repetition rounds or the change tier

#### Scenario: Impact assessment for the fast lane

- **WHEN** triage routes to the defect fast lane
- **THEN** the affected items list SHALL be written to `bugfix-status.md` as the sole verification scope
- **AND** the verification targets SHALL include existing tests, new regression tests, or manual verification steps
- **AND** the impact scope score SHALL NOT affect tier selection because the fast lane does not use a change tier

### Requirement: Impact assessment evidence sources

The impact assessment SHALL use specific evidence sources to identify affected scope, selected by the defect workspace.

#### Scenario: Evidence-based assessment

- **WHEN** performing impact assessment for a change-scoped defect
- **THEN** the system SHALL identify affected functional points by cross-referencing the diagnostic conclusion with the change-level `functional-designs/`
- **AND** SHALL identify affected interfaces by checking the change-level `detailed-design.md` API definitions
- **AND** SHALL identify data model changes by examining the diagnostic evidence for schema/storage modifications

#### Scenario: Evidence-based assessment without an active change

- **WHEN** performing impact assessment for a project-scoped defect
- **THEN** the system SHALL identify affected functional points by cross-referencing the diagnostic conclusion with `docs/designs/functional-designs/`
- **AND** SHALL identify affected interfaces by checking `docs/designs/detailed-designs/`
- **AND** SHALL identify data model changes by examining the diagnostic evidence for schema/storage modifications
- **AND** when product-level design artifacts are missing, the assessment SHALL mark the affected items list as incomplete and SHALL NOT route to the fast lane without user confirmation
