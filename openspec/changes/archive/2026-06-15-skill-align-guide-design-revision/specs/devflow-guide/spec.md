## MODIFIED Requirements

### Requirement: Guide design doc documents DESIGN_REVISION routing
`docs/designs/skills/kflow-guide.md` SHALL document the DESIGN_REVISION routing mode, post-revision processing flow, and Plan Mode bypass rule.

#### Scenario: Design doc contains DESIGN_REVISION section
- **WHEN** `docs/designs/skills/kflow-guide.md` is read
- **THEN** it SHALL contain a DESIGN_REVISION routing section with keyword mapping and分流 logic
