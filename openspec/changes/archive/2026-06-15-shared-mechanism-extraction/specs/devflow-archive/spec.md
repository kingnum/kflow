## MODIFIED Requirements

### Requirement: Archive conditions and design merge single source
The core definition of archive conditions and design merge workflow SHALL reside in `kflow-shared/archive-rules.md`. `04-gates-and-transitions.md` §6.3-6.3.1 SHALL be replaced with references.

#### Scenario: Core mechanism doc archive sections simplified
- **WHEN** `04-gates-and-transitions.md` §6.3 is read after the change
- **THEN** it SHALL contain a reference `> 完整规范参见 kflow-shared/archive-rules.md`
- **THEN** the full archive checklist and design merge workflow SHALL NOT appear in `04-gates-and-transitions.md`
