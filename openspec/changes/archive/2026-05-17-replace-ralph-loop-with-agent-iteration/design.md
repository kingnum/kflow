## Context

当前 ralph-loop 通过 Stop Hook（stop-hook.sh）拦截 Claude 退出，读取 transcript 检查 `<promise>COMPLETED</promise>` 标签，未检测到时重喂相同 prompt 实现迭代循环。这依赖外部基础设施：Shell 脚本、jq JSON 解析、perl 正则、状态文件（.claude/ralph-loop.local.md）、hooks.json 配置。

实际上 Claude Code 的 Agent 工具已原生支持内部迭代——当 prompt 包含 "TDD: 写测试→实现→运行→修bug→重复直到全绿" 这样的迭代指令时，Agent 会自然地在一个长会话中反复执行、检查、修复，直到满足完成标准。Stop Hook 机制是多余的中间层。

## Goals / Non-Goals

**Goals:**
- 完全移除 ralph-loop 运行时依赖（Skill 定义、Hook、脚本、命令、参考文档、状态文件）
- 用 Agent 工具原生迭代能力替换所有执行类阶段的 "ralph-loop 子代理执行模式"
- 保持执行模型核心逻辑不变：复杂度评估 → 子代理调度 → 主 Agent 验收
- 保持 HITL/AFK 分类机制不变（仅更新引用名称）
- 清理 settings.local.json 中的 ralph-loop 相关配置

**Non-Goals:**
- 不修改阶段门控机制
- 不修改主 Agent 验收逻辑（产物检查、覆盖率验证、skill-suggestion 记录）
- 不修改阶段流转规则
- 不修改已归档变更
- 不引入新的外部依赖

## Decisions

### Decision 1: 用 Agent 工具原生迭代替代 Stop Hook 循环

**选择**: 执行类阶段直接使用 `Agent(description, prompt, run_in_background)` 启动子代理，prompt 中内嵌迭代指令（TDD 循环、直到满足 DoD）。

**替代方案**:
- ScheduleWakeup 轮询: 每次轮询重新加载上下文，成本高，非连续迭代
- CronCreate 持久轮询: 过度设计，超出单 session 需求
- 保留但简化 ralph-loop: 不解决根本问题，Hook 基础设施仍需维护

**原理**: Agent 收到 "写测试→实现→运行测试→修bug→重复直到全绿→输出验收报告" 这样的 prompt 时，会自然地在单次会话中迭代。不需要外部 Hook 强制重入。

### Decision 2: 完成信号从 "promise 标签" 改为 "Agent 自然返回"

**选择**: Agent 完成任务后自然返回（不再需要 `<promise>COMPLETED</promise>` 标签检测）。主 Agent 验收是真正的质量门。

**原理**: ralph-loop 的完成承诺机制是为了让外部 Hook 能检测完成状态。Agent 原生执行时，Agent 自己判断何时完成并返回。如果 Agent 提前返回但产物不全，主 Agent 验收会捕获（与当前 ralph-loop 验收不通过流程相同）。

### Decision 3: 复杂度评估转为 Agent prompt 中的节奏指引

**选择**: 保留复杂度评估公式（功能点数 × 1 + 接口数 × 1.5 + 场景数 × 2），但其结果从 "ralph-loop --max-iterations" 转为 Agent prompt 中的 pacing guidance。

```
旧: /ralph-loop --max-iterations 7
新: Agent prompt 中嵌入 "复杂度: 中 (预计需 5-8 轮迭代验证)"
```

**原理**: Agent 会根据实际进展自我调节迭代次数，不需要外部硬限制。复杂度评估作为 prompt 中的参考信息帮助 Agent 判断工作量。

### Decision 4: 主 Agent 验收逻辑完全保留

**选择**: 不做任何修改。验收仍检查：产物完整性、覆盖率=100%、无 TODO/TBD 占位符。验收不通过时仍记录 skill-suggestion.md + AskUserQuestion 询问重跑。

### Decision 5: HITL/AFK 分类保留，名称更新

**选择**: 分类逻辑完全不变。仅将文档中的 "ralph-loop 全自动" 改为 "Agent 全自动"，"ralph-loop 暂停" 改为 "Agent 使用 AskUserQuestion 暂停"。

| 类型 | 旧行为 | 新行为 |
|------|--------|--------|
| AFK | ralph-loop 全自动迭代 | Agent 全自动迭代 |
| HITL | ralph-loop 在决策点暂停 | Agent 在决策点使用 AskUserQuestion 暂停 |

### Decision 6: 文件删除策略

**选择**: 完全删除 ralph-loop 相关文件，不保留兼容层或桥接代码。

删除清单:
```
.claude/skills/ralph-loop/          (SKILL.md + hooks/ + scripts/ + .claude-plugin/)
.claude/commands/ralph-loop/        (ralph-loop.md + cancel-ralph.md + help.md)
references/ralph-loop/              (整个目录)
settings.local.json → hooks.Stop    (仅 ralph-loop 条目)
settings.local.json → allow         (18 条 ralph-loop 权限)
```

## Risks / Trade-offs

- **[风险] Agent 可能提前返回（任务未完成）** → 主 Agent 验收会捕获产物缺失，验收不通过 → skill-suggestion.md → AskUserQuestion 重跑，与当前 ralph-loop 流程一致
- **[风险] Agent 可能过度迭代（浪费时间）** → prompt 中嵌入复杂度评估作为节奏指引，Agent 有自然停止判断
- **[风险] 迁移可能遗漏引用** → 已完成全仓库 grep 审计（47 文件），按变更清单逐项执行
- **[取舍] 失去 Stop Hook 的硬性重入保证** → Agent 原生迭代更自然，上下文连续性更好（无需每次重读文件），是一个质量提升

## Migration Plan

1. 创建新 spec (`agent-iteration-execution`)，修改现有 specs (`coverage-traceability`, `hitl-afk-classification`)，废弃旧 spec (`ralph-loop-subagent-execution`)
2. 更新所有运行时 Skill 文件（7 个 SKILL.md）
3. 更新所有设计文档（10 个文件）
4. 删除 ralph-loop 运行时文件
5. 清理 settings.local.json
6. 验证: 检查全仓库无残留 ralph-loop 引用（归档目录除外）

回滚策略: git revert 整个 commit。无数据迁移（仅文本替换）。
