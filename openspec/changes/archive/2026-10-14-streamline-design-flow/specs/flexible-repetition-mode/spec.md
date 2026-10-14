# Spec Delta

## MODIFIED Requirements

### Requirement: Convergence-aligned flexible repetition verification gate

When an execution phase completes, the system SHALL enforce the following verification criteria: affected items 100% coverage (every affected functional point/interface fully checked) and product integrity (all required outputs exist and are format-compliant). All criteria MUST pass for acceptance. The system SHALL NOT require a fixed full-sweep floor round as a separate criterion, and SHALL NOT make the number of rounds a criterion for acceptance or rejection.

#### Scenario: Verification gate at convergence

- **WHEN** an execution phase completes
- **THEN** the verification criteria SHALL include:
  - Affected items: 100% coverage verification
  - Product integrity: all required outputs exist and are format-compliant
- **AND** all criteria MUST pass for acceptance
- **AND** no fixed full-sweep floor round SHALL be required

#### Scenario: Verification gate on rollback re-execution

- **WHEN** a phase re-executes after a phase rollback and .status.md carries an affected items list
- **THEN** every affected item SHALL receive complete phase-specific verification
- **AND** the affected items 100% coverage criterion MUST pass

#### Scenario: Affected items verification

- **WHEN** verifying affected items
- **THEN** the system SHALL cross-reference the affected items list from .status.md "Recent Revision Info"
- **AND** each affected item SHALL receive complete phase-specific verification (not abbreviated)
- **AND** verification results SHALL be recorded in the phase output
- **AND** the number of execution rounds SHALL NOT be an acceptance criterion

### Requirement: Phase execution history tracking

The system SHALL track phase execution history in .status.md to distinguish first execution from re-execution.

#### Scenario: Execution history table in status file

- **WHEN** .status.md is created or updated
- **THEN** it SHALL include a "Phase Execution History" table with columns:
  - Phase name
  - Execution count (1st, 2nd, etc.)
  - Last execution type (First Execution / REVISION / Rollback Re-execution)
  - Rounds completed (e.g., `1`, `2`)
  - Impact scope score (if applicable)
  - Notes

#### Scenario: History updated on phase completion

- **WHEN** an execution phase completes
- **THEN** the system SHALL update the execution history table
- **AND** increment the execution count for that phase
- **AND** record the execution type and rounds completed
