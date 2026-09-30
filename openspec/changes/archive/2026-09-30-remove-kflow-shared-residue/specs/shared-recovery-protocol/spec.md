# Spec Delta

## REMOVED Requirements

### Requirement: Shared recovery protocol definition file

**Reason**: 该能力要求 `.claude/skills/kflow-shared/recovery-protocol.md` 作为恢复协议的单一权威文件，但 `kflow-shared/` 集中式目录已在 `2026-07-04-skill-self-contained-refactor` 中移除。恢复协议现存放于 `skills/kflow-resume/references/recovery-protocol.md`，由 `skill-self-contained` 的「Single-reference file distribution」需求明确指定为该 skill 独占。

**Migration**: 恢复协议改由 `skills/kflow-resume/references/recovery-protocol.md` 定义；引用该协议的需求（`resume-five-question-summary`、`two-level-checkpoint`）的引用目标同步修正。

### Requirement: Core mechanism doc recovery section replaced

**Reason**: 该需求要求 `06-recovery.md` 的恢复章节替换为对 `kflow-shared/recovery-protocol.md` 的引用。目标文件已不存在，引用无法成立。

**Migration**: 同一需求改由 `two-level-checkpoint` 承担，引用目标改为 `skills/kflow-resume/references/recovery-protocol.md`。
