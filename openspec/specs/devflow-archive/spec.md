## MODIFIED Requirements

### Requirement: Archive conditions and design merge single source
The core definition of archive conditions and design merge workflow SHALL reside in `kflow-shared/archive-rules.md`. `04-gates-and-transitions.md` §6.3-6.3.1 SHALL be replaced with references.

#### Scenario: Core mechanism doc archive sections simplified
- **WHEN** `04-gates-and-transitions.md` §6.3 is read after the change
- **THEN** it SHALL contain a reference `> 完整规范参见 kflow-shared/archive-rules.md`
- **THEN** the full archive checklist and design merge workflow SHALL NOT appear in `04-gates-and-transitions.md`

## MODIFIED by token-opt-archive-summarization

### Requirement: Archive conditions and design merge single source with summary generation
The core definition of archive conditions and design merge workflow SHALL reside in `kflow-shared/archive-rules.md`. `04-gates-and-transitions.md` §6.3-6.3.1 SHALL be replaced with references. Archive phase SHALL include a summary generation step (step 5.6 SUMMARY) after design merge, outputting `module-summary.md`.

#### Scenario: Core mechanism doc archive sections simplified
- **WHEN** `04-gates-and-transitions.md` §6.3 is read after the change
- **THEN** it SHALL contain a reference `> 完整规范参见 kflow-shared/archive-rules.md`
- **THEN** the full archive checklist and design merge workflow SHALL NOT appear in `04-gates-and-transitions.md`

#### Scenario: Archive includes summary generation step
- **WHEN** `kflow-archive` SKILL.md execution flow is read
- **THEN** it SHALL contain a step 5.6 SUMMARY for generating/updating `module-summary.md` after design merge

#### Scenario: Output artifacts table updated
- **WHEN** archive output artifacts table is read
- **THEN** it SHALL include `module-summary.md` as an output artifact entry
