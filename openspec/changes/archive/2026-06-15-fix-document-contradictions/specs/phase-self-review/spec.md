## MODIFIED Requirements

### Requirement: Design phase self-review uses repetition mode
The `kflow-design.md` design document SHALL describe self-review using "重复制" (repetition) mode — each round independently executes all four dimensions (一致性+完备性+可行性+可测性). The old "分工制" round grouping (Round 1-3 structural / 4-7 detail / 8-10 boundary) SHALL be removed.

#### Scenario: Design doc self-review flow corrected
- **WHEN** `kflow-design.md` execution flow diagram is read
- **THEN** SELFREV step SHALL describe "子代理串行 + 重复制" without round-grouping
