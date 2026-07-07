## MODIFIED Requirements

### Requirement: RELOAD mechanism aligns with layered loading
RELOAD mechanism SHALL integrate with layered loading — subagent RELOAD steps SHALL only reload files from the loaded tiers.

#### Scenario: RELOAD respects tier boundaries
- **WHEN** a subagent executes RELOAD
- **THEN** it SHALL only reload files that belong to its loaded tiers
