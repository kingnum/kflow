# Spec Delta

## MODIFIED Requirements

### Requirement: RELOAD清单 adds module-summary.md for relevant phases

explore/design/plan phase RELOAD清单 SHALL include `module-summary.md` as an optional load item. The RELOAD清单 SHALL be defined in each skill's own `references/hooks.md`.

#### Scenario: RELOAD清单 updated

- **WHEN** the RELOAD清单 is read for the explore, design, or plan phase
- **THEN** it SHALL be read from that phase's own `references/hooks.md` (for example `skills/kflow-explore/references/hooks.md`)
- **AND** explore/design/plan phases SHALL list `module-summary.md` as an optional load
- **AND** the read SHALL NOT depend on a `kflow-shared/phase-hooks.md` file
