# Tasks

## 1. 设计文档同步（docs/designs/）

- [x] 1.1 改写 `docs/designs/core-mechanisms/07-agent-model.md` §15（子代理执行模型）与 §16（自审机制）：删除档位轮次上限表与回退叠加规则，改为收敛终止模型（见证轮 4 项）、审查范围冻结、不收敛判定与升级、终止结果二值。验证：`grep -n "轮次上限\|复检轮\|达上限\|max(档位" docs/designs/core-mechanisms/07-agent-model.md` 无匹配
- [x] 1.2 改写 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：§3「3次修复上限与轮次上限的层级关系」改为「3次修复上限与收敛终止的层级关系」，门控判读链（份数 = 档位上限 + 1）改为「份数 ≥ 1」，验证门控章节按新触发条件改写。验证：`grep -n "轮次上限\|档位上限 + 1\|复检轮" docs/designs/core-mechanisms/04-gates-and-transitions.md` 无匹配
- [x] 1.3 同步 `docs/designs/core-mechanisms/03-status-and-tasks.md` 的 `执行轮次` 字段格式（`{N} 轮`）与「终止原因」→「终止结果」，并同步 `docs/designs/index.md` 的档位行为差异表。验证：`grep -rn "{N} / {上限}\|终止原因" docs/designs/core-mechanisms/03-status-and-tasks.md docs/designs/index.md` 无匹配
- [x] 1.4 同步 `docs/designs/skills/kflow-*.md` 中涉及轮次与终止的段落（explore / design / prototype-design / plan / code / code-review / api-test / e2e-test / integration-test / bug-fix）。验证：`grep -rln "轮次上限\|达上限\|复检轮" docs/designs/skills/` 返回空

## 2. 执行类重复制实现层（8 份 repetition.md + 10 份 gates.md）

- [x] 2.1 改写 8 份 `skills/kflow-*/references/repetition.md` 的 §2 核心特征、§4 重复制执行流程图、§7 Agent 完成判断、§8 验收标准表、§9 验收失败分流、§10 子代理 prompt 规范、§11 skill-suggestion 触发条件：删除档位轮次上限与「或达到轮次上限」路径，收敛（见证轮 4 项）为唯一成功终止条件，验收失败分流新增「引入范围外新内容」类型。验证：`./scripts/sync-references.sh` 报告 8 份 `repetition.md` 内容一致且无差异
- [x] 2.2 改写 8 份 `repetition.md` §13 轮间摘要：新增「范围外观察」字段；§13.5 的复核义务改为引用见证轮第 (d) 项条件（不再作为独立判据）。验证：`grep -n "范围外观察" skills/kflow-code/references/repetition.md` 有匹配，且 `./scripts/sync-references.sh` 通过
- [x] 2.3 重写 8 份 `repetition.md` §14（轮次决策 → 收敛终止模型与不收敛判定）、删除 §14.5.1 复检轮、改写 §14.6 非收敛分支。验证：`grep -rn "复检轮\|档位上限\|影响范围分数映射\|Recommended Rounds" skills/*/references/repetition.md` 无匹配
- [x] 2.4 退化 8 份 `repetition.md` §15 验证门控（删除「全量至少 1 轮兜底」，受影响项 100% 覆盖挂到回退重执行场景）；§16 执行历史表 Rounds 列改 `{N} 轮`；§17 删除分数→轮次映射（保留分数读取用于受影响项清单）。验证：与 §15/§16/§17 相关的旧措辞在 8 份中均无残留，`./scripts/sync-references.sh` 通过
- [x] 2.5 同步 10 份 `skills/kflow-*/references/gates.md` §1.3：四条份数判定规则塌为「自审报告份数 ≥ 1」，删除「份数 = 档位上限 + 1」例外与防滥用条款；归档门控与中断恢复产物完整性验证门控同步。验证：`./scripts/sync-references.sh` 报告 10 份 `gates.md` 内容一致，且 `grep -rn "档位上限 + 1" skills/*/references/gates.md` 无匹配

## 3. 设计自审实现层（3 份 self-review.md + self-review-dimensions.md）

- [x] 3.1 改写 `skills/kflow-explore/references/self-review.md`、`skills/kflow-design/references/self-review.md`、`skills/kflow-prototype-design/references/self-review.md`：删除档位轮次上限表与复检轮约定，改为收敛驱动（见证轮 4 项）、审查范围冻结、范围外观察降级、不收敛判定与升级、终止结果二值。验证：`./scripts/sync-references.sh` 报告三份 `self-review.md` 内容一致（`phase-self-review` 要求）
- [x] 3.2 同步 `skills/kflow-explore/references/self-review-dimensions.md` 中的见证轮与范围冻结表述。验证：`grep -n "轮次上限\|复检轮" skills/kflow-explore/references/self-review-dimensions.md` 无匹配

## 4. 技能 SKILL.md 同步（设计文档 → SKILL.md 同步）

- [x] 4.1 **设计文档 → SKILL.md 同步**：同步 14 份 `skills/kflow-*/SKILL.md`（explore / design / prototype-design / plan / code / code-review / api-test / e2e-test / integration-test / bug-fix / bug-triage / audit / resume / archive）的验收块、SELFREV 步骤描述、门控描述与审计判据——删除轮次上限与复检轮表述，改为收敛终止模型、审查范围冻结与终止结果二值。验证：`grep -rn "轮次上限\|达上限\|复检轮" skills/kflow-*/SKILL.md` 无匹配
- [x] 4.2 校验 4.1 未破坏 front matter 与版本字段。验证：`python scripts/validate-frontmatter.py` 通过
- [x] 4.3 确认 `.claude/skills/` 下三个通用运行时技能（`grilling`、`skill-creator`、`to-spec`）不含本变更涉及的轮次规则，无需同步；如发现对应规则则一并同步。验证：`grep -rn "轮次上限\|复检轮" .claude/skills/` 无匹配

## 5. 主 spec Purpose 同步与引用一致性

- [x] 5.1 同步受影响主 spec 的 `## Purpose` 段（delta 无 Purpose 通道，需在 `openspec/specs/<capability>/spec.md` 内直接改）：`agent-iteration-execution`、`round-counter`、`subagent-self-review`、`plan-self-review`、`execution-repetition-mode`、`flexible-repetition-mode`、`prototype-navigation-verification`、`prototype-playwright-5round-verification`、`devflow-audit` 等。验证：`grep -rn "档位.*轮次上限\|轮次上限由变更档位" openspec/specs/*/spec.md` 无匹配
- [x] 5.2 全仓扫描并修正对已改名能力与已改名需求标题的引用：`tier-driven-repetition` → `convergence-driven-repetition`；「导航合理性验证轮次（收敛驱动）」→「（纯收敛驱动）」；「Playwright 全覆盖验证轮次（收敛驱动）」→「（纯收敛驱动）」。验证：`grep -rn "tier-driven-repetition\|recheck-round" openspec/specs/ skills/ docs/ README.md` 无匹配
- [x] 5.3 运行 `openspec validate converge-review-termination --strict` 并确认变更可被归档消费。验证：命令输出 `is valid`

## 6. README 同步

- [x] 6.1 改写 `README.md` 的档位行为差异表：删除「执行类阶段轮次上限」「设计自审轮次上限」「复检轮」三行，档位语义改为「每轮审查强度 + 产出深度」，并同步设计自审与执行类重复制的轮次说明行。验证：`grep -n "轮次上限" README.md` 无匹配
- [x] 6.2 删除「复检轮是什么？为什么轻量档会执行 2 轮？」问答，并改写「执行类阶段的重复制模式是什么？」中的收敛与轮次表述、以及版本更新说明中的档位与轮次描述。验证：`grep -n "复检轮" README.md` 无匹配
- [x] 6.3 同步 `README.md` 技能总览表中各 skill 的轮次相关描述（`kflow-plan` 等含「按变更档位轮次上限」的行）。验证：`grep -rn "轮次上限\|档位上限" README.md` 无匹配

## 7. 集成校验

- [x] 7.1 全仓残留术语扫描：`grep -rn "轮次上限\|档位上限\|达上限\|收敛（复检轮）\|recheck-round\|tier-driven-repetition" openspec/specs/ skills/ docs/ README.md`——预期仅命中 `openspec/changes/archive/` 下的历史变更（历史产物不改），其余为空。验证：命令输出中除 `archive/` 路径外无匹配行
- [x] 7.2 走查一条轻量档执行类阶段的终止路径，确认新模型自洽：第 1 轮有修复 → 不构成见证轮 → 继续第 2 轮 → 零新发现零修改且清单复核通过 → 终止，终止结果 `收敛`，全程无复检轮、无 `达上限`。验证：以 `skills/kflow-code/SKILL.md` 与 `skills/kflow-code/references/repetition.md` 为文本依据逐条比对流程图与验收表，无矛盾项
