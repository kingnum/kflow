## MODIFIED Requirements

### Requirement: Detailed design split threshold
The split threshold for detailed design documents SHALL be 20 function points. FP ≤ 20 → single file `detailed-design.md`; FP > 20 → directory `detailed-design/` (6-file structure).

#### Scenario: Threshold corrected in core mechanism doc
- **WHEN** `02-directory-structure.md` §2.4 is read
- **THEN** the threshold SHALL be 20 (not 30)
