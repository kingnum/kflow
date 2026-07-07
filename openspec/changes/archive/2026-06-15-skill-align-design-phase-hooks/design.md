## Context

`kflow-design` 是变更级必须阶段，但 SKILL.md 和设计文档均缺少 PRE_HOOK/POST_HOOK 引用。这是 CLAUDE.md 强制规则的违规项。design 阶段不需要服务（❌ 类型），PRE_HOOK 仅需 CHECK_STATE + RELOAD，POST_HOOK 仅需 UPDATE_STATE。

## Goals / Non-Goals

**Goals:**
- kflow-design SKILL.md 添加 PRE_HOOK/POST_HOOK 引用
- 设计文档同步更新

**Non-Goals:**
- 不修改钩子执行逻辑本身
- 不修改其他 Skill

## Decisions

### D1: 引用位置

执行流程中添加：
- Step 1: PRE_HOOK — 引用 `kflow-shared/phase-hooks.md` design PRE_HOOK
- 最后 Step: POST_HOOK — 引用 `kflow-shared/phase-hooks.md` design POST_HOOK
- 原有步骤编号顺移

### D2: phase-hooks.md 更新

`kflow-shared/phase-hooks.md` 和 `09-phase-hooks.md` 的 RELOAD 清单中 design 阶段配置已存在（line 17），无需额外修改。仅需确认引用路径正确。

## Risks / Trade-offs

无显著风险。pure additive change。
