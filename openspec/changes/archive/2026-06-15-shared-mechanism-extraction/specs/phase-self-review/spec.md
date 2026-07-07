## MODIFIED Requirements

### Requirement: Self-review workflow and reporting
The core definition of self-review SHALL reside in `kflow-shared/self-review.md`. `07-agent-model.md` §16 SHALL retain only a brief overview and a reference to the shared file.

#### Scenario: Core mechanism doc simplified
- **WHEN** `07-agent-model.md` §16 is read after the change
- **THEN** it SHALL contain ≤5 lines of overview text plus a reference `> 完整规范参见 kflow-shared/self-review.md`
- **THEN** the full workflow diagram, storage structure, report format, and VERIFY mechanism SHALL NOT appear in `07-agent-model.md`
