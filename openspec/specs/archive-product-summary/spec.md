# archive-product-summary Specification

## Purpose

定义归档阶段生成与维护产品模块摘要（module-summary.md）的规则，使后续变更的 RELOAD 能以模块摘要作为入口、按需选择性加载完整功能设计文档，从而降低上下文开销。

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

### Requirement: RELOAD清单 adds module-summary.md for relevant phases

explore/design/plan phase RELOAD清单 SHALL include `module-summary.md` as an optional load item. The RELOAD清单 SHALL be defined in each skill's own `references/hooks.md`.

#### Scenario: RELOAD清单 updated

- **WHEN** the RELOAD清单 is read for the explore, design, or plan phase
- **THEN** it SHALL be read from that phase's own `references/hooks.md` (for example `skills/kflow-explore/references/hooks.md`)
- **AND** explore/design/plan phases SHALL list `module-summary.md` as an optional load
- **AND** the read SHALL NOT depend on a `kflow-shared/phase-hooks.md` file
