# Spec Delta

## MODIFIED Requirements

### Requirement: Impact score to round mapping

The system SHALL provide a mapping from impact scope score to recommended repetition rounds for downstream phases. This mapping SHALL be defined once in the tier-driven-repetition capability, and kflow-bug-triage SHALL reference it rather than defining its own numeric ranges.

#### Scenario: Round recommendation table

- **WHEN** impact scope score is calculated
- **THEN** the triage report SHALL include round recommendations taken from the tier-driven-repetition mapping:
  - Score <= 3: 1 round
  - Score 4-15: 3 rounds
  - Score > 15: 10 rounds
- **AND** the recommendation SHALL be presented as the impact mapping component of `max(tier baseline, impact mapping)`, not as an absolute round count

#### Scenario: No locally defined round ranges

- **WHEN** kflow-bug-triage and its `references/` files describe round recommendations
- **THEN** they SHALL reference the tier-driven-repetition mapping
- **AND** SHALL NOT define their own score ranges or round counts
