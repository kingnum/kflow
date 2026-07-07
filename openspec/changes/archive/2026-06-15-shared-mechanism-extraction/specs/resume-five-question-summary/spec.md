## MODIFIED Requirements

### Requirement: Resume workflow references shared recovery protocol
`kflow-resume.md` design doc SHALL reference `kflow-shared/recovery-protocol.md` for the recovery priority chain and dispatch mapping table instead of inlining them.

#### Scenario: Resume design doc deduplicated
- **WHEN** `docs/designs/skills/kflow-resume.md` is read after the change
- **THEN** the RESUME WORKFLOW section SHALL reference `kflow-shared/recovery-protocol.md` instead of containing the full workflow diagram and priority chain inline
