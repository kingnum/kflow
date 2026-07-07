## MODIFIED Requirements

### Requirement: Self-review workflow and reporting uses per-skill references
The specification of self-review SHALL reside in each design-phase skill's `references/self-review.md` (kflow-explore, kflow-prototype-design, kflow-design). No centralized `kflow-shared/self-review.md` SHALL exist.

#### Scenario: Design skill SKILL.md references local self-review
- **WHEN** `kflow-design/SKILL.md` constructs a self-review subagent prompt
- **THEN** it SHALL instruct loading `skills/kflow-design/references/self-review.md` (dev) or `.claude/skills/kflow-design/references/self-review.md` (consumer)

#### Scenario: Self-review content is identical across design skills
- **WHEN** comparing `references/self-review.md` across kflow-explore, kflow-prototype-design, and kflow-design
- **THEN** the content SHALL be identical (same self-review rules apply to all design phases)

## REMOVED Requirements

### Requirement: Shared self-review in kflow-shared
**Reason**: `kflow-shared/self-review.md` is removed. Each design-phase skill maintains its own copy in `references/self-review.md`.
**Migration**: Self-review rules are copied to each design-phase skill's `references/self-review.md`. Consumer projects should delete `kflow-shared/self-review.md`.
