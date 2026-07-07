## MODIFIED Requirements

### Requirement: Repetition mode execution workflow
The core definition of repetition mode SHALL reside in `kflow-shared/repetition-model.md`. `07-agent-model.md` §15 SHALL retain only a brief overview and a reference to the shared file.

#### Scenario: Core mechanism doc simplified
- **WHEN** `07-agent-model.md` §15 is read after the change
- **THEN** it SHALL contain ≤5 lines of overview text plus a reference `> 完整规范参见 kflow-shared/repetition-model.md`
- **THEN** the full complexity formula, round enforcement rules, acceptance criteria, and prompt specifications SHALL NOT appear in `07-agent-model.md`
