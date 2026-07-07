## 1. OpenSpec 规格迁移

- [x] 1.1 创建新 spec `agent-iteration-execution/spec.md`（已完成 — 在 specs/ 目录下）
- [x] 1.2 创建 delta spec `coverage-traceability/spec.md`（已完成 — MODIFIED: 2 条 requirement 术语更新）
- [x] 1.3 创建 delta spec `hitl-afk-classification/spec.md`（已完成 — MODIFIED: 2 条 requirement 术语更新）
- [x] 1.4 创建 delta spec `ralph-loop-subagent-execution/spec.md`（已完成 — REMOVED: 5 条 requirement 标记废弃）

## 2. 运行时 Skill 更新（.claude/skills/）

- [x] 2.1 更新 `kflow-code/SKILL.md` — "ralph-loop 子代理执行模式" → "Agent 迭代执行模式"，执行流程 3 步（复杂度评估→prompt 构建→启动 Agent）更新，`/ralph-loop` → `Agent(description, prompt, run_in_background)`
- [x] 2.2 更新 `kflow-bug-fix/SKILL.md` — 同上
- [x] 2.3 更新 `kflow-e2e-test/SKILL.md` — 同上
- [x] 2.4 更新 `kflow-integration-test/SKILL.md` — 同上
- [x] 2.5 更新 `kflow-plan/SKILL.md` — "ralph-loop 子代理执行" → "Agent 迭代执行"
- [x] 2.6 更新 `kflow-code-review/SKILL.md` — 同上，description 字段也需更新
- [x] 2.7 更新 `kflow-design/SKILL.md` — HITL/AFK 行为表中的 "ralph-loop" → "Agent"，description 字段保持不变（不含 ralph-loop）

## 3. 设计文档更新（docs/designs/）

- [x] 3.1 更新 `core-mechanisms.md` 第 15 章 — 整章从 "ralph-loop 子代理执行" 重写为 "Agent 迭代执行"（18 处引用），更新章节结构、流程图、复杂度映射表
- [x] 3.2 更新 `overview.md` — 设计决策表 3 处 "ralph-loop 子代理执行" → "Agent 迭代执行"
- [x] 3.3 更新 `skills/kflow-code.md` — 执行模式章节（8 处）+ HITL/AFK 行为表
- [x] 3.4 更新 `skills/kflow-design.md` — HITL/AFK 分类表（4 处）
- [x] 3.5 更新 `skills/kflow-bug-fix.md` — 执行模式章节（4 处）
- [x] 3.6 更新 `skills/kflow-e2e-test.md` — 执行模式章节（4 处）
- [x] 3.7 更新 `skills/kflow-integration-test.md` — 执行模式章节（4 处）
- [x] 3.8 更新 `skills/kflow-plan.md` — 执行模式章节（4 处）
- [x] 3.9 更新 `skills/kflow-code-review.md` — 执行模式章节（4 处）
- [x] 3.10 更新 `examples/skill-suggestion.md` — "ralph-loop 验收" → "Agent 验收"（10 处）

## 4. 删除 ralph-loop 运行时文件

- [x] 4.1 删除 `.claude/skills/ralph-loop/` 全部文件（SKILL.md + hooks/stop-hook.sh + hooks/hooks.json + scripts/setup-ralph-loop.sh + .claude-plugin/plugin.json）
- [x] 4.2 删除 `.claude/commands/ralph-loop/` 全部文件（ralph-loop.md + cancel-ralph.md + help.md）
- [x] 4.3 删除 `references/ralph-loop/` 整个目录（SKILL.md + README.md + hooks/ + scripts/ + commands/ + .claude-plugin/）

## 5. Settings 清理

- [x] 5.1 移除 `settings.local.json` → `hooks.Stop` 中 ralph-loop 条目（第 79-88 行）
- [x] 5.2 移除 `settings.local.json` → `permissions.allow` 中 18 条 ralph-loop 相关权限
- [x] 5.3 移除 `settings.local.json` → `permissions.allow` 中 `ralph-loop-subagent-execution` 相关目录创建权限

## 6. 验证

- [x] 6.1 `.claude/` 和 `docs/designs/` 无 ralph-loop 引用；`openspec/specs/` 中 3 个文件待 sync（delta spec 已在 change 目录中，归档时同步）
- [x] 6.2 `ralph.loop` / `ralph_loop` 备选拼写：零匹配
- [x] 6.3 所有 kflow-* SKILL.md 无 ralph-loop 残留
- [x] 6.4 settings.local.json 无 ralph-loop 残留（Hook 已移除，18 条权限已清理）
