# phase-hooks Specification

## Purpose

本能力定义各阶段 PRE_HOOK 与 POST_HOOK 的归属与加载规则，规定钩子规则按阶段分散存放于各 Skill 自身的 `references/` 目录，服务生命周期与端口冲突规则同样以本地引用为唯一来源。

## Requirements

### Requirement: Phase hooks service management deduplication
PRE_HOOK/POST_HOOK step sequences SHALL reside in each skill's `references/hooks.md` file, not in a centralized `kflow-shared/phase-hooks.md`. Each skill's `references/hooks.md` SHALL contain only the hook sections relevant to that skill's phase.

#### Scenario: Port conflict detection single source
- **WHEN** port conflict detection rules are needed for a skill requiring service management
- **THEN** they SHALL be read from the skill's `references/service-lifecycle.md`, not from any centralized file

#### Scenario: Service stop timeout chain single source
- **WHEN** service stop timeout chain is needed for a skill requiring service management
- **THEN** it SHALL be read from the skill's `references/service-lifecycle.md`, not from any centralized file

### Requirement: All phase Skills reference their own references/hooks.md
All phase Skill SKILL.md files SHALL contain PRE_HOOK and POST_HOOK loading instructions pointing to their own `references/hooks.md` file. No skill SHALL reference `kflow-shared/phase-hooks.md`.

#### Scenario: kflow-code SKILL.md contains local hook reference
- **WHEN** `skills/kflow-code/SKILL.md` execution flow is read
- **THEN** it SHALL contain a PRE_HOOK loading instruction for `skills/kflow-code/references/hooks.md` (dev) or `.claude/skills/kflow-code/references/hooks.md` (consumer)
- **AND** it SHALL contain a POST_HOOK loading instruction for the same file

#### Scenario: kflow-design SKILL.md contains local hook reference
- **WHEN** `skills/kflow-design/SKILL.md` execution flow is read
- **THEN** it SHALL contain PRE_HOOK and POST_HOOK loading instructions pointing to its own `references/hooks.md`

### Requirement: RELOAD supports incremental mode
Each skill's `references/hooks.md` RELOAD rules SHALL document the incremental RELOAD option alongside the existing full RELOAD.

#### Scenario: Hooks file documents incremental RELOAD
- **WHEN** a skill's `references/hooks.md` RELOAD section is read
- **THEN** it SHALL document the incremental RELOAD option alongside the existing full RELOAD
