# Proposal

## Why

多轮审查机制（设计自审 SELFREV、执行类重复制、prototype VERIFY）以「必须完成全部目标轮次」为终止条件，即**预算制**而非**收敛制**。这带来四个问题：

1. **轮次与轮次之间无状态传递**：设计自审每轮冷启动子代理，前轮的修复与遗留问题不注入下一轮（轮间摘要机制已为执行类定义，但被分层加载规则排除在设计类之外）。因此「自然收敛」没有任何机制保障，只是关于 LLM 行为的假设。
2. **评分底线被架空**：完整档同时规定「必须完成全部 10 轮」与「各维度评分 > 8 方通过」——第 3 轮就 >8 仍须做满 10 轮，第 10 轮才 ≤8 已无处补审。评分底线两头够不着，是装饰性的。
3. **达上限未收敛时静默放行**：完整档 10 轮上限处无失败分支，未达标也直接标记阶段完成。相比之下执行类阶段有完整的「未收敛处理路径」（skill-suggestion + AskUserQuestion + ⚠️ 阻塞）。
4. **表述自相矛盾**：`tier-driven-repetition` 规格自己把 `1/3/10` 定义为「档位基线（目标轮次的下限）」，而各 SKILL 与 references 却把它抬成「强制完成数」。同一概念两套语义。

上述终止规则在三套口径中重复出现，且 `round-counter` 仍硬编码 `{N} / 10`、`agent-iteration-execution` 的 Purpose 段仍写「强制 10 轮迭代机制」，与档位化规格冲突。

## What Changes

- **移除**「即使连续多轮无新问题，也须完成全部目标轮次」「禁止在目标轮次前返回」「SHALL NOT 因中间某轮无新问题而提前终止」等规则，覆盖**全部三套口径**（设计自审 / 执行类重复制 / prototype VERIFY）
- **轮次模型反转为收敛驱动**：下限统一为 **1 轮**（无例外）；上限 = 变更档位基线（轻量 1 / 标准 2 设计·3 执行 / 完整 **5**）。**BREAKING**：档位语义由「强制完成数」翻转为「轮次上限」，`.status.md` 执行轮次字段格式由 `{N} / 10` 变为 `{N} / {上限}`
- **引入收敛终止判据**：**见证轮** = 一轮同时满足「零新发现问题 + 零修改 + 报告证明全维度全量遍历」。终止条件 = 下限达成 **且** 最近一轮为见证轮；或执行轮次达上限
- **轮间摘要注入扩展到设计自审**：原仅执行类阶段的 `references/repetition.md` §13 机制，扩展到 explore / design / prototype-design / plan 的 SELFREV（与上一条原子绑定——无状态传递的「零发现」不可信）
- **完整档评分底线由装饰变为有效终止条件**：`>8 且收敛` 即止，`≤8` 续审至上限（5 轮）
- **回退重执行叠加规则反向**：由 `目标轮次 = max(档位基线, 影响范围映射)` 改为 `上限 = max(档位上限, 影响范围映射)`，保留「返工验证不因低档而放松」原意
- **影响范围分数映射更新**：`>15 → 5`（原 10）；`≤3 → 1` / `4~15 → 3` 不变
- **新增非收敛分支**：达上限仍无见证轮 → 记录 `skill-suggestion.md` + AskUserQuestion → 可标记 ⚠️ 阻塞
- **验收标准改写**：`执行轮次 = N / N` 改为 `执行轮次 >= 1 且（达成收敛 ∨ 执行轮次 = 上限）`；`.status.md` 新增**终止原因**字段（`收敛` / `达上限`）供审计判读
- **BREAKING**：轻量档设计自审由 **0 轮**改为 **1 轮**，不再豁免 SELFREV；产物完整性门控保留为附加硬门
- **修正既有规格漂移**：`round-counter` 的 `{N} / 10` 硬编码与「轮次不足 10/10 拒收」场景；`agent-iteration-execution` 的 Purpose 段「强制 10 轮」

## Capabilities

### New Capabilities

（无新增能力。收敛终止语义并入既有轮次决策能力 `tier-driven-repetition`。）

### Modified Capabilities

- `tier-driven-repetition`: 档位定义由「下限/目标轮次」反转为「轮次上限」；下限统一 1；完整档 10→5；新增收敛终止条件（见证轮）；影响范围映射 `>15 → 5`；回退叠加反向
- `execution-repetition-mode`: 标准重复的档位基线数值与语义更新；灵活重复的 `max()` 叠加反向；验证门控阈值由「目标轮次 < 10」改为「执行轮次 < 上限」
- `flexible-repetition-mode`: 轮次决策 requirement 的数值与 `max()` 语义更新；plan 阶段口径 0/2/10 → 1/2/5；影响范围映射 `>15 → 10` 改为 `→ 5`
- `round-counter`: 计数器格式 `{N} / 10` → `{N} / {上限}`；「轮次不足 10/10 视为验收不通过」改为新验收判据；移除「无实际工作可执行时轮次仍递增」场景
- `agent-iteration-execution`: Purpose 段「强制 10 轮迭代机制」修正；「无实际工作时仍完成轮次」场景改为按上限/收敛判定；重复制遍历指令由「必须完成全部目标轮次后才可返回」改为收敛驱动
- `subagent-self-review`: SELFREV 轮次 0/2/10 → 1/2/5；「轻量档跳过自审」场景改为「轻量档执行 1 轮」；「必须完成全部目标轮次」改为收敛终止；新增轮间摘要注入要求
- `plan-self-review`: 轮次 0/2/10 → 1/2/5；移除「SHALL NOT 因中间某轮无新问题而提前终止」「即使连续多轮无新问题也必须完成全部目标轮次」
- `inter-round-summary`: 适用范围由「重复执行模式（执行类）」扩展到设计自审 SELFREV
- `auto-subchange-traversal`: 提示词强制指令「必须完成全部目标轮次迭代后才可返回验收报告，禁止在目标轮次前返回」改为收敛驱动表述
- `defect-strike-limit`: 「10 轮迭代（外层循环下限）」改为档位上限；移除「不因无工作而跳过轮次——10 轮计数器仍须递增至 10/10」
- `prototype-navigation-verification`: 导航验证由「5 轮强制执行」改为 `[1,5]` 收敛驱动
- `prototype-playwright-5round-verification`: Playwright 验证由「5 轮强制执行」改为 `[1,5]` 收敛驱动
- `html-prototype-workflow`: 「Playwright 5 轮全覆盖验证」与「导航合理性验证」两处 requirement 的「SHALL 完成全部 5 轮，不允许提前终止」改为 `[1,5]` 收敛驱动

## Impact

**受影响实现**：

- `skills/kflow-*/SKILL.md`：explore、design、prototype-design、plan（设计自审口径）+ code、code-review、api-test、e2e-test、integration-test、bug-fix、bug-triage（执行类口径），共 11 个 SKILL 的遍历指令、验收块与强制执行规则
- `skills/kflow-{explore,design,prototype-design}/references/self-review.md`（内容须一致）、`skills/kflow-explore/references/self-review-dimensions.md`
- `skills/kflow-*/references/repetition.md`：8 份（code / code-review / api-test / e2e-test / integration-test / bug-fix / bug-triage / plan）§7、§10、§14、§15
- `docs/designs/skills/kflow-*.md`：设计文档同步
- `openspec/specs/`：上述 13 个能力

**行为影响**：

- Token 与子代理数量显著下降：完整档上限由 10 降至 5，且典型在 3~4 轮收敛即止；设计自审每轮因轮间摘要而更具焦点
- 轻量档新增 1 轮语义自审（原 0 轮，仅有占位符形式检查）
- 无代码、API、依赖或运行时契约变更；变更限于 KFlow Skill 规格与实现文档
