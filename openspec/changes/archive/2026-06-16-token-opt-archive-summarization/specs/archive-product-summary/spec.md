## ADDED Requirements

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
