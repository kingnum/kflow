## MODIFIED Requirements

### Requirement: RELOAD supports incremental mode
`kflow-shared/phase-hooks.md` RELOAD rules SHALL add an "incremental mode" option where verified files can be skipped with summary injection.

#### Scenario: Phase hooks doc updated
- **WHEN** `kflow-shared/phase-hooks.md` RELOAD section is read
- **THEN** it SHALL document the incremental RELOAD option alongside the existing full RELOAD
