# Spec Delta

## REMOVED Requirements

### Requirement: RELOAD 清单由共享钩子文件统一定义

**Reason**: 该需求要求各阶段的 RELOAD 文件清单在 `.claude/skills/kflow-shared/phase-hooks.md` 中统一定义，该目录已不存在。且 `phase-hooks` 能力明确要求「PRE_HOOK/POST_HOOK step sequences SHALL reside in each skill's `references/hooks.md` file, not in a centralized `kflow-shared/phase-hooks.md`」——本需求与该要求直接矛盾，是重构后遗留的过期描述。

**Migration**: RELOAD 清单改由各 skill 自身的 `references/hooks.md` 定义，各 skill 可自行维护其阶段的 RELOAD 清单；跨阶段的 RELOAD 原则由本能力的「RELOAD mechanism aligns with layered loading」约束。

## MODIFIED Requirements

### Requirement: Phase hooks RELOAD清单 adds module-summary.md

The RELOAD 清单 for explore/design/plan phases SHALL add `module-summary.md` as an optional load item. The RELOAD 清单 SHALL be read from each phase's own `references/hooks.md`.

#### Scenario: RELOAD清单 updated

- **WHEN** the RELOAD清单 is read for one of the explore, design, or plan phases
- **THEN** it SHALL be read from that phase's own `references/hooks.md` file
- **AND** explore/design/plan phases SHALL include `module-summary.md` as an optional load item
- **AND** the read SHALL NOT depend on a `kflow-shared/phase-hooks.md` file

### Requirement: RELOAD清单 adds module-summary.md for relevant phases

explore/design/plan phase RELOAD清单 SHALL include `module-summary.md` as an optional load item. (Content identical to token-opt-incremental-reload; retained for traceability to archive-summarization change.)

#### Scenario: RELOAD清单 updated

- **WHEN** the RELOAD清单 is read for one of the explore, design, or plan phases
- **THEN** explore/design/plan phases SHALL list `module-summary.md` as an optional load
- **AND** the RELOAD清单 source SHALL be that phase's own `references/hooks.md`, not a `kflow-shared/phase-hooks.md` file
