## Why

`kflow-design` 的设计文档和 SKILL.md 均缺少 `kflow-shared/phase-hooks.md` 的 PRE_HOOK/POST_HOOK 引用。CLAUDE.md 强制规则要求："阶段 Skill 的 SKILL.md 执行流程中 MUST 包含对 `kflow-shared/phase-hooks.md` 的 PRE_HOOK 和 POST_HOOK 引用"。`kflow-design` 是变更级必须阶段，缺少钩子引用是审计违规项。

## What Changes

- `kflow-design` SKILL.md 执行流程中添加 PRE_HOOK（step 1）引用 `kflow-shared/phase-hooks.md` design PRE_HOOK
- `kflow-design` SKILL.md 执行流程中添加 POST_HOOK（最后步骤）引用 `kflow-shared/phase-hooks.md` design POST_HOOK
- `docs/designs/skills/kflow-design.md` 设计文档同步添加 PRE_HOOK/POST_HOOK 引用

## Capabilities

### New Capabilities

### Modified Capabilities
- `phase-hooks`: kflow-design 阶段接入 PRE_HOOK/POST_HOOK 钩子机制

## Impact

- **SKILL.md**: `.claude/skills/kflow-design/SKILL.md` 修改
- **设计文档**: `docs/designs/skills/kflow-design.md` 修改
- 审计阶段（kflow-audit）将检查此合规项——修改后从违规变为合规
