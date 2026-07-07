## Why

ralph-loop 通过 Stop Hook 拦截退出 + 重喂 prompt 实现迭代循环，依赖外部 Shell 脚本（stop-hook.sh、setup-ralph-loop.sh）、状态文件（ralph-loop.local.md）、jq/perl 等运行时工具。实际上 Agent 工具原生支持内部迭代——给 Agent 一个 TDD 流程 prompt，它会自然地写测试→实现→运行→修bug→重复直到完成。用 Stop Hook 强制重入不仅增加了 15+ 个额外文件的维护负担，还割裂了上下文连续性（每次迭代重新读文件而非持续累积）。用 Agent 原生迭代能力替换这条依赖链，是消除不必要的架构复杂度。

## What Changes

- **BREAKING**: 移除 ralph-loop 插件全部运行时文件（SKILL.md、hooks/、scripts/、.claude-plugin/、commands/）
- **BREAKING**: 移除 `references/ralph-loop/` 参考目录
- **BREAKING**: 移除 `settings.local.json` 中的 Stop Hook 配置及 18 条 ralph-loop 相关 allow 权限
- 7 个执行类阶段 Skill 的 "ralph-loop 子代理执行模式" 改为 "Agent 迭代执行模式"，执行流程改为直接使用 Agent 工具
- 设计文档 core-mechanisms.md 第15章从 "ralph-loop 子代理执行" 重写为 "Agent 迭代执行"
- 6 个 skill 设计规格（kflow-plan/code/code-review/e2e-test/bug-fix/integration-test）的执行模式章节更新
- kflow-design 设计规格中的 HITL/AFK 行为表更新
- skill-suggestion.md 示例中的验收记录表更新
- OpenSpec 规格：新增 `agent-iteration-execution`，修改 `coverage-traceability`、`hitl-afk-classification`，废弃 `ralph-loop-subagent-execution`
- 主 Agent 验收闭环逻辑保持不变

## Capabilities

### New Capabilities

- `agent-iteration-execution`: Agent 原生迭代执行模式。执行类阶段使用 Agent 工具内置迭代能力，替代 ralph-loop Stop Hook 循环。核心机制：复杂度评估确定迭代策略 → 构建阶段专属 prompt（含迭代指令）→ Agent(background) 执行 → Agent 自然返回 → 主 Agent 验收

### Modified Capabilities

- `ralph-loop-subagent-execution`: 废弃，功能由 `agent-iteration-execution` 取代
- `coverage-traceability`: "通过 ralph-loop 子代理完成" 改为 "通过 Agent 迭代执行完成"
- `hitl-afk-classification`: "ralph-loop 全自动/暂停" 改为 "Agent 全自动/暂停（使用 AskUserQuestion）"

## Impact

- 删除 ~15 个文件（.claude/skills/ralph-loop/、.claude/commands/ralph-loop/、references/ralph-loop/）
- 修改 ~20 个文件（7 个运行时 SKILL.md + 10 个设计文档 + 3 个 OpenSpec 规格）
- 修改 `settings.local.json`（移除 Stop Hook、移除 18 条 ralph-loop 权限）
- 运行时 `.claude/ralph-loop.local.md` 状态文件不再创建
- 对用户不可见：执行类阶段行为无变化（仍然先评估复杂度、再启动子代理迭代、最后主 Agent 验收）
