# archive-product-summary Specification

## Requirements

### Requirement: Archive generates module summary after merge
After archive design merge completes, the archive phase SHALL generate/update `docs/designs/functional-designs/module-summary.md` containing a 2-3 line summary per module (module name + core functions + FP-ID range + document location).

#### Scenario: Summary generated after merge
- **WHEN** archive design merge completes
- **THEN** `module-summary.md` SHALL be created or updated with current module information

#### Scenario: Summary format
- **WHEN** `module-summary.md` is read
- **THEN** it SHALL contain a table with columns: 模块 | 核心功能 | FP-ID 范围 | 文档位置

### Requirement: Subsequent changes reference summary first
Subsequent changes' RELOAD SHALL prioritize loading `module-summary.md` over full functional-designs documents. Full module documents SHALL only be loaded when the subchange directly involves that module.

#### Scenario: RELOAD uses summary as entry point
- **WHEN** a new change's explore/design phase executes RELOAD
- **THEN** it SHALL load `module-summary.md` first, then selectively load full module documents only for relevant modules

### Requirement: Archive phase includes summary generation step
`kflow-archive` SHALL include a summary generation step after design merge.

#### Scenario: Archive SKILL.md updated
- **WHEN** `kflow-archive` SKILL.md execution flow is read
- **THEN** it SHALL contain a step for generating/updating `module-summary.md` after design merge

## MODIFIED by token-opt-archive-summarization

### Requirement: RELOAD清单 adds module-summary.md for relevant phases
explore/design/plan phase RELOAD清单 SHALL include `module-summary.md` as an optional load item.

#### Scenario: RELOAD清单 updated
- **WHEN** `kflow-shared/phase-hooks.md` RELOAD清单 is read
- **THEN** explore/design/plan phases SHALL list `module-summary.md` as an optional load
