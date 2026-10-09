# Tasks

> 规格依据：`specs/`（13 个能力的 delta）。实现依据：`design.md`。

## 1. 核心轮次模型（执行类重复制权威文件）

- [x] 1.1 更新 `skills/kflow-code/references/repetition.md`：§7 移除「禁止在目标轮次前返回」与「无实际工作仍须递增至 N/N」，改为收敛驱动（见证轮）；§10 重复制遍历指令改为新增的正向表述；§14 档位基线改为「轮次上限」（轻量 1 / 标准 3 / 完整 5），回退叠加改为 `上限 = max(档位上限, 映射)`，映射 `>15 → 5`；§15 验证门控阈值改为「执行轮次 < 轮次上限」。验证：`grep -n "轮次上限" skills/kflow-code/references/repetition.md` 命中 §14，且 `grep -n "禁止在目标轮次前返回"` 无命中
- [x] 1.2 将 1.1 的改动同步到其余 7 份 `references/repetition.md`（`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-plan`）。验证：`for f in skills/kflow-*/references/repetition.md; do grep -c "轮次上限" "$f"; done` 每份 ≥ 1，且全部无「禁止在目标轮次前返回」
- [x] 1.3 在每份 `references/repetition.md` §14 补充「终止原因写入 `.status.md`」与「非收敛分支」条款，并确认 §13 轮间摘要标注其适用范围已扩展到设计自审。验证：`grep -n "终止原因\|非收敛分支" skills/kflow-*/references/repetition.md` 每份命中

## 2. 设计自审规则（三技能一致）

- [x] 2.1 重写 `skills/kflow-explore/references/self-review.md` §4/§5：轮次表改为「下限 1 / 上限 轻量 1·标准 2·完整 5」，删除「轻量档 0 轮跳过自审」与「即使连续多轮无新问题，也须完成全部目标轮次」，新增见证轮终止条件与失败分支。验证：`grep -n "见证轮" skills/kflow-explore/references/self-review.md` 命中，且 `grep -n "即使连续多轮无新问题"` 无命中
- [x] 2.2 将 2.1 的改动同步到 `skills/kflow-design/references/self-review.md` 与 `skills/kflow-prototype-design/references/self-review.md`，使三者内容一致。验证：`diff` 三份文件 §4/§5 段落无差异（`phase-self-review` 能力要求内容一致）
- [x] 2.3 更新 `skills/kflow-explore/references/self-review-dimensions.md`：删除「即使连续多轮无新问题，也须完成全部目标轮次」，改为见证轮终止；补充「见证轮须复核前轮摘要中的全部修复」。验证：`grep -n "见证轮" skills/kflow-explore/references/self-review-dimensions.md` 命中，无「即使连续多轮无新问题」

## 3. 设计类阶段 SKILL.md 同步（设计自审口径）

- [x] 3.1 设计文档 → SKILL.md 同步：更新 `skills/kflow-explore/SKILL.md` 步骤 8e/11 的档位轮次表（轻量 1 / 标准 2 / 完整 5）、轻量档产物门控表述、以及「强制执行规则」段落。验证：`grep -n "轻量 0 轮\|完整 10 轮" skills/kflow-explore/SKILL.md` 无命中
- [x] 3.2 设计文档 → SKILL.md 同步：按 3.1 同步 `skills/kflow-design/SKILL.md` 与 `skills/kflow-prototype-design/SKILL.md` 的自审轮次与轻量档表述。验证：`grep -rn "轻量 0 轮\|完整 10 轮" skills/kflow-design/SKILL.md skills/kflow-prototype-design/SKILL.md` 无命中
- [x] 3.3 设计文档 → SKILL.md 同步：更新 `skills/kflow-plan/SKILL.md` 步骤 9.5 自审轮次（轻量 1 / 标准 2 / 完整 5），删除「即使连续多轮无新问题也必须完成全部目标轮次」。验证：`grep -n "即使连续多轮无新问题" skills/kflow-plan/SKILL.md` 无命中

## 4. 执行类阶段 SKILL.md 同步（执行类口径）

- [x] 4.1 设计文档 → SKILL.md 同步：把 7 个执行类 SKILL.md（`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`）的重复制遍历指令由「必须完成全部目标轮次迭代后才可返回验收报告，禁止在目标轮次前返回」改为收敛驱动表述；档位轮次数值由 `完整 10` 改为 `完整 5`。验证：`grep -rn "禁止在目标轮次前返回" skills/kflow-*/SKILL.md` 无命中
- [x] 4.2 更新上述 7 个 SKILL.md 的验收块：`执行轮次 = N / N` 改为 `执行轮次 >= 1 且（见证轮 ∨ = 轮次上限）`，「轮次不足（< 目标轮次 N）拒收」改为「无见证轮且未达上限时拒收」，并补「达上限仍无见证轮 → 非收敛分支」。验证：`grep -rn "执行轮次 = N / N" skills/kflow-*/SKILL.md` 无命中
- [x] 4.3 更新 `skills/kflow-resume/SKILL.md` 中「执行轮次 = N / N（N 由弹性轮次决策确定）」的验收表述以匹配新判据。验证：`grep -n "执行轮次" skills/kflow-resume/SKILL.md` 的命中行不再表述为 `= N / N`

## 5. 原型阶段 VERIFY 同步

- [x] 5.1 设计文档 → SKILL.md 同步：更新 `skills/kflow-prototype-design/SKILL.md` 的导航验证与 Playwright 验证段落，把「SHALL NOT 因中间某轮无新问题而提前终止，即使连续多轮无新问题也必须完成全部 5 轮」改为「下限 1、上限 5、见证轮收敛终止」。验证：`grep -n "必须完成全部 5 轮" skills/kflow-prototype-design/SKILL.md` 无命中
- [x] 5.2 更新 `skills/kflow-prototype-design/references/self-review.md` 中 BUILD/VERIFY 的轮次与「不允许因无新问题而提前终止」表述。验证：`grep -n "不允许因无新问题而提前终止" skills/kflow-prototype-design/references/self-review.md` 无命中

## 6. 设计文档同步

- [x] 6.1 更新 `docs/designs/skills/kflow-explore.md`、`kflow-design.md`、`kflow-prototype-design.md`、`kflow-plan.md` 的自审轮次表与「不允许提前终止」表述。验证：`grep -rn "完整 10 轮\|轻量 0 轮" docs/designs/skills/` 无命中
- [x] 6.2 更新 `docs/designs/skills/kflow-code.md`、`kflow-bug-fix.md` 及其他执行类设计文档的重复制遍历指令与轮次数值。验证：`grep -rn "禁止在目标轮次前返回" docs/designs/` 无命中
- [x] 6.3 若 `docs/designs/core-mechanisms/03-status-and-tasks.md` 或 `07-agent-model.md` 含轮次下限/上限或 `{N}/10` 表述，同步更新。验证：`grep -rn "10 轮\|/ 10" docs/designs/core-mechanisms/` 的命中行均已按「档位上限」改写
   - 执行说明：除任务列名的 03/07 外，一并同步了 `04-gates-and-transitions.md`、`08-governance.md`、`index.md`、`overview.md`，以及 `skills/kflow-*/references/gates.md`（10 份）、`skills/kflow-audit/SKILL.md`、`skills/kflow-explore/SKILL.md` 与全部档位驱动模板（audit-report / review-round / code-review）——均为本变更模型变更的直接下游消费者

## 7. 规格漂移修正（Purpose 段与能力文本）

- [x] 7.1 修正 `openspec/specs/agent-iteration-execution/spec.md` 与 `openspec/specs/plan-self-review/spec.md` 的 Purpose 段（现分别写「强制 10 轮迭代机制」「强制执行的 10 轮子代理串行自审」）。验证：`grep -n "10 轮" openspec/specs/agent-iteration-execution/spec.md openspec/specs/plan-self-review/spec.md` 无命中
- [x] 7.2 修正 `openspec/specs/prototype-navigation-verification/spec.md`、`prototype-playwright-5round-verification/spec.md`、`html-prototype-workflow/spec.md`、`inter-round-summary/spec.md`、`tier-driven-repetition/spec.md` 的 Purpose 段以反映收敛驱动与设计自审纳入。验证：`grep -ln "5 轮子代理串行\|不允许提前终止\|目标轮次" openspec/specs/*/spec.md` 的命中文件均已修正
   - 注：5 份 Purpose 段均已修正；`grep` 仍命中 9 行，全部位于**标题**且受归档工具约束不得改动（`tier-driven-repetition` 的 `目标轮次写入状态文件` / `轮次计数器呈现目标轮次` 被本变更 delta 的 MODIFIED 块按名称引用，必须逐字保留；其余位于 delta 的 REMOVED 目标之内，归档时随能力一并删除）。详见本变更 review 记录。
- [x] 7.3 全仓清理残留表述：`完成全部 5 轮`、`完成全部 10 轮`、`不允许提前终止`、`必须完成全部目标轮次`、`{N} / 10`。验证：`grep -rn "完成全部 10 轮\|完成全部 5 轮\|不允许提前终止\|必须完成全部目标轮次\|{N} / 10" skills/ docs/designs/ openspec/specs/` 无命中（归档目录 `openspec/changes/archive/` 除外）
   - 执行说明（归档同步时补记）：`openspec/specs/triage-impact-assessment/spec.md` 的 `Score > 15: 10 rounds` 与 `max(tier baseline, impact mapping)` 未被本任务的检索式覆盖而遗漏，归档同步时一并修正为 `5 rounds` 与 `max(tier upper bound, impact mapping)`，与 `tier-driven-repetition` 的统一映射（`>15 → 5`、`上限 = max(档位上限, 映射)`）对齐

## 8. 集成验证

- [x] 8.1 运行 `openspec validate converge-review-rounds --strict` 并确认无 ERROR/WARNING
   - 结果：`Change 'converge-review-rounds' is valid`（exit 0）
- [x] 8.2 交叉核对一致性：`skills/kflow-{explore,design,prototype-design}/references/self-review.md` 三份内容一致；8 份 `references/repetition.md` 的 §14 数值一致。验证：`diff` 三份 self-review.md 无输出；`grep -h "完整 5" skills/kflow-*/references/repetition.md | sort -u` 仅一行
   - 结果：三份 self-review.md `diff` 无输出；8 份 repetition.md 两两 `diff -q` 无差异（字节级一致），§14 档位上限表为 `| 轻量 | 1 |` / `| 标准 | 3 |` / `| 完整 | 5 |`
   - 说明：`grep -h "完整 5" ... | sort -u` 实测返回 6 行而非 1 行——因单份文件内「完整 5」出现在 6 个不同语句（v1.6.0 变更注记、§14.2 档位表、§14.2 plan 例外、§14.4 示例、§17.3、§16.1 字段说明）。任务意图为「8 份数值一致」，已由字节级 `diff` 更强地验证。
- [x] 8.3 端到端走查一个轻量档样例：按更新后的 `kflow-explore/SKILL.md` 推演，确认轻量档执行 1 轮自审 + 产物门控，且 `.status.md` 记录终止原因。验证：走查结论记录到本变更的 review 记录中，无「跳过自审」路径
   - 结果：记录于 `openspec/changes/converge-review-rounds/review.md` §2；`grep -n "跳过自审\|跳过 SELFREV" skills/kflow-explore/SKILL.md` 无命中
- [x] 8.4 端到端走查一个完整档样例：确认轮次上限 5、达上限仍无见证轮时触发非收敛分支（skill-suggestion + AskUserQuestion + ⚠️ 阻塞）。验证：走查结论记录到本变更的 review 记录中
   - 结果：记录于 `openspec/changes/converge-review-rounds/review.md` §3
