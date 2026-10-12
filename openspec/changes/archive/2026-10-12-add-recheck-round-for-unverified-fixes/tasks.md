# Tasks

> 规格依据：`specs/`（1 个新能力 + 10 个能力的 delta）。实现依据：`design.md`。
> 基准策略（依 design D6、D7、D9）：先改 1 份作为基准文件，其余按字节级 `diff` 同步，避免多份拷贝漂移。

## 1. 复检轮核心机制（执行类重复制权威文件）

- [x] 1.1 在 `skills/kflow-code/references/repetition.md` 落地复检轮：改造 §4 流程图 ACCEPT 分支（新增"终止点判定：累积未复核修复清单是否为空"）、§7 Agent 完成判断、§8 验收标准表（轮次维度加"或存在通过的复检轮"、终止原因取值改为三值）、§9 验收失败处理（新增"清单非空却未追加复检轮 → 拒收并追加"、类型 B 加"不存在通过的复检轮"前置）、§14.5 终止原因（`收敛` / `收敛（复检轮）` / `达上限`）、§14.6 非收敛分支、§15 验证门控（复检轮场景判定）。验证：`grep -n "复检轮" skills/kflow-code/references/repetition.md` 在 §4/§7/§8/§9/§14.5/§14.6/§15 各命中，且 `grep -n "取值 \`收敛\` 或 \`达上限\`" skills/kflow-code/references/repetition.md` 无命中
- [x] 1.2 将 1.1 的改动同步到其余 7 份 `references/repetition.md`（`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`、`kflow-plan`）。验证：`for f in skills/kflow-*/references/repetition.md; do grep -c "复检轮" "$f"; done` 每份 ≥ 1；`grep -ln "收敛（复检轮）" skills/kflow-*/references/repetition.md | wc -l` 为 8；两两 `diff -q` 的差异仅限阶段名与维度名等既有差异
- [x] 1.3 在 8 份 `references/repetition.md` 的轮间摘要章节（§13）加入「累积未复核修复清单」字段与增量规则（累积公式见 design D6），明确该清单由主 Agent 维护、供终止判定与复检轮消费。验证：`grep -n "累积未复核修复清单" skills/kflow-*/references/repetition.md` 每份命中

## 2. 设计自审规则（三份 self-review.md，须内容一致）

- [x] 2.1 重写 `skills/kflow-explore/references/self-review.md`：§4.2 轮次取值表加复检轮行、§4.5 终止条件与复核义务改为"先判清单、再分支"、§5 自审流程图加复检轮环节、§6 自审执行方式加复检轮子代理、§7 自审记录存储加复检轮报告与份数规则、§8 自审报告内容规范加"累积未复核修复清单"与"复检轮判定"章节；同时把轮间摘要格式与注入规则**内联**为本文件的新章节，删除 3 处对 `references/repetition.md` §13 的悬空引用（design D9）。验证：`grep -n "复检轮" skills/kflow-explore/references/self-review.md` 命中 §4/§5/§6/§7/§8；`grep -n "references/repetition.md" skills/kflow-explore/references/self-review.md` 无命中；`grep -n "累积未复核修复清单" skills/kflow-explore/references/self-review.md` 命中
- [x] 2.2 将 2.1 同步到 `skills/kflow-design/references/self-review.md` 与 `skills/kflow-prototype-design/references/self-review.md`。验证：`diff skills/kflow-explore/references/self-review.md skills/kflow-design/references/self-review.md` 与对 prototype-design 的 `diff` 均无输出（`phase-self-review` 要求三份内容一致）
- [x] 2.3 更新 `skills/kflow-explore/references/self-review-dimensions.md` 的见证轮与终止表述以对齐复检轮（补充"见证轮候选与复检轮须复核累积清单内全部修复"）。验证：`grep -n "复检轮\|累积未复核修复清单" skills/kflow-explore/references/self-review-dimensions.md` 命中
- [x] 2.4 在 `skills/kflow-prototype-design/references/self-review.md` 的 §10.2/§10.3/§10.4 为 nav-check、playwright-check、ux-check 三条 VERIFY 流程加入复检轮（不消耗 1–5 轮上限、最多 1 轮），并规定复检轮报告命名为 `round-recheck.md`。验证：`grep -n "round-recheck.md" skills/kflow-prototype-design/references/self-review.md` 至少命中 nav-check 与 playwright-check 两处，且 §10.3 规则表含复检轮行

## 3. 设计类 SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 3.1 设计文档 → SKILL.md 同步：更新 `skills/kflow-explore/SKILL.md` 的 SELFREV 段落、产物表脚注与自审报告份数判定（改为"≤ 档位上限，或 = 档位上限 + 1 当且仅当终止原因含复检轮"）、终止原因与强制执行规则段。验证：`grep -n "复检轮" skills/kflow-explore/SKILL.md` 命中；`grep -n "份数 ≤ 档位轮次上限" skills/kflow-explore/SKILL.md` 的命中行已改写
- [x] 3.2 设计文档 → SKILL.md 同步：按 3.1 同步 `skills/kflow-design/SKILL.md` 与 `skills/kflow-prototype-design/SKILL.md`（含 prototype 的 SELFREV 前置条件段与 VERIFY 轮次说明）。验证：`grep -n "复检轮" skills/kflow-design/SKILL.md skills/kflow-prototype-design/SKILL.md` 各自命中；`grep -n "不计算轮次上限" skills/kflow-prototype-design/SKILL.md` 命中行仍保留"人工审查"路径的跳过语义
- [x] 3.3 设计文档 → SKILL.md 同步：更新 `skills/kflow-plan/SKILL.md` 步骤 9.5（SELFREV）与「重复制执行模型」段的轮次表、终止原因与复检轮规则，保持"口径唯一来源"说明成立。验证：`grep -n "复检轮" skills/kflow-plan/SKILL.md` 在步骤 9.5 与后文"重复制执行模型"各命中；`grep -n "收敛（复检轮）" skills/kflow-plan/SKILL.md` 命中

## 4. 执行类 SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 4.1 设计文档 → SKILL.md 同步：更新 7 个执行类 SKILL.md（`kflow-code`、`kflow-code-review`、`kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`、`kflow-bug-fix`、`kflow-bug-triage`）的终止条件段、验收块、终止原因字段与非收敛分支说明，加入复检轮。验证：`grep -ln "复检轮" skills/kflow-{code,code-review,api-test,e2e-test,integration-test,bug-fix,bug-triage}/SKILL.md | wc -l` 为 7
- [x] 4.2 设计文档 → SKILL.md 同步：更新 `skills/kflow-resume/SKILL.md` 中读取"执行轮次计数器与终止原因字段"的表述，使恢复流程能识别 `收敛（复检轮）` 并正确恢复复检轮环节。验证：`grep -n "终止原因" skills/kflow-resume/SKILL.md` 的命中行含复检轮

## 5. 门控与审计同步

- [x] 5.1 更新 10 份 `skills/kflow-*/references/gates.md` 的自审记录份数判定：由"≤ 档位轮次上限"改为 design D8 的四条规则（含"多出的 1 份须能由终止原因解释"的防滥用条款），并覆盖进入接口单元测试/E2E测试/集成测试/归档等各门控分支中的份数检查。验证：`grep -c "档位上限 + 1\|档位轮次上限 + 1" skills/kflow-explore/references/gates.md` ≥ 1；`grep -rn "份数 ≤ 档位轮次上限\|份数不超过档位轮次上限" skills/kflow-*/references/gates.md` 无命中
- [x] 5.2 更新 `skills/kflow-audit/SKILL.md` 的三处轮次判定（流程与产物合规性、效率与改进、档位基准段）：SHALL NOT 因终止原因 `收敛（复检轮）`、或因份数 = 档位上限 + 1 而判定轮次不足、超额或缺项；`收敛（复检轮）` 与 `达上限`（份数 = 上限 + 1）均须有对应的合法分支。验证：`grep -n "收敛（复检轮）" skills/kflow-audit/SKILL.md` 在三处判定各命中

## 6. 设计文档同步

- [x] 6.1 更新 `docs/designs/core-mechanisms/07-agent-model.md` 的轮次模型段与 §16 自审规范引用，加入复检轮（不消耗档位预算、全局最多 1 轮、三值终止原因）。验证：`grep -n "复检轮" docs/designs/core-mechanisms/07-agent-model.md` 命中
- [x] 6.2 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`（终止原因字段取值）、`04-gates-and-transitions.md`（份数判定）、`08-governance.md`（`self-reviews/{phase}/` 白名单与份数说明）。验证：`grep -rn "复检轮" docs/designs/core-mechanisms/` 在上述文件中命中；`grep -rn "终止原因（取值 \`收敛\` 或 \`达上限\`）\|终止原因（\`收敛\` / \`达上限\`）" docs/designs/core-mechanisms/` 无命中
- [x] 6.3 更新 `docs/designs/skills/kflow-{explore,design,prototype-design,plan,code,code-review,api-test,e2e-test,integration-test,bug-fix,bug-triage,resume,audit}.md` 的轮次表、终止原因与份数判定表述。验证：`grep -rln "复检轮" docs/designs/skills/ | wc -l` ≥ 10
- [x] 6.4 更新 `README.md`：档位行为差异表中的设计自审/执行类轮次行加复检轮说明、FAQ 中执行类重复制条目、版本更新说明条目。验证：`grep -n "复检轮" README.md` 命中档位行为差异表段与 FAQ 段

## 7. 集成验证

- [x] 7.1 运行 `openspec validate add-recheck-round-for-unverified-fixes --strict` 确认无 ERROR/WARNING。验证：命令输出 `Change 'add-recheck-round-for-unverified-fixes' is valid`
- [x] 7.2 交叉核对一致性：三份 `references/self-review.md` 内容一致；8 份 `references/repetition.md` 的终止原因取值集合一致且均为三值。验证：三份 `diff` 无输出；`grep -h "收敛（复检轮）" skills/kflow-*/references/repetition.md | wc -l` 为 8
- [x] 7.3 端到端走查轻量档样例：按更新后的规则推演——第 1 轮零发现 → `收敛`（1 份报告）；第 1 轮含 1 项修复 → 追加复检轮 → 通过则 `收敛（复检轮）`（2 份报告），未通过则 `达上限` + 非收敛分支。确认不存在"发现即非收敛"的路径。验证：走查结论记录到 `openspec/changes/add-recheck-round-for-unverified-fixes/review.md`，且 `grep -n "复检轮" skills/kflow-explore/SKILL.md` 命中
- [x] 7.4 端到端走查完整档样例：确认 5 轮内每轮均含修复时，复检轮逐项复核全部累积修复；复检轮报告份数为 6（上限 5 + 1）且终止原因为 `收敛（复检轮）`；门控与审计均不判违规。验证：走查结论记录到 `openspec/changes/add-recheck-round-for-unverified-fixes/review.md`，并逐条对照 design D3 判读链与 D8 份数规则
- [x] 7.5 端到端走查 prototype 人工审查路径：确认 README 与 SKILL.md 中"人工审查"路径 SHALL NOT 追加复检轮。验证：`grep -n "SHALL NOT 追加复检轮\|不得追加复检轮" skills/kflow-prototype-design/SKILL.md` 命中
