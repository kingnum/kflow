## MODIFIED Requirements

### Requirement: Subagent prompt construction follows layered loading
Subagent prompt construction SHALL follow the layered loading strategy. Each phase SKILL.md SHALL specify which tiers to load.

#### Scenario: Phase SKILL.md documents loading tiers
- **WHEN** an execution-phase SKILL.md constructs a subagent prompt
- **THEN** it SHALL list the specific kflow-shared files to load based on tier classification
