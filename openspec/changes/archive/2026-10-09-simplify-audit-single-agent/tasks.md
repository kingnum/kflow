# Tasks

## 1. 审计 Skill 主体改写（`skills/kflow-audit/SKILL.md`）

- [x] 1.1 设计文档 → SKILL.md 同步：改写 front matter 的 `description`——权重串由七维度改为四维度（流程与产物合规性 45% / 审查与缺陷闭环 30% / 测试充分性 15% / 效率与改进 10%），并补入「审计由单一子代理执行」。验证：`python scripts/validate-frontmatter.py` 对 `skills/kflow-audit/SKILL.md` 无报错，且 `grep -n "22%\|23%\|Post-mortem5%" skills/kflow-audit/SKILL.md` 无命中
- [x] 1.2 设计文档 → SKILL.md 同步：改写「审计路径分流」表及其后两条 SHALL/SHALL NOT——执行者列统一为「审计子代理（1 个）」，轻量档不再写「主 Agent（SHALL NOT 启动子代理）」，标准/完整档由「4 个 Agent」改为 1 个。验证：`grep -n "4 个 Agent\|主 Agent（SHALL NOT 启动子代理）" skills/kflow-audit/SKILL.md` 无命中，且分流表与 delta 的 ADDED 需求「审计由单一子代理执行」的 `全部档位由单一子代理执行` 场景一致
- [x] 1.3 设计文档 → SKILL.md 同步：改写「角色」「任务」段落与执行流程图（步骤 4 EVALUATE、步骤 5 SCORE）——删除 4 个 Agent 分工框与「七维度并行评估」，改为单子代理取证后统一评分。验证：`grep -n "并行 Agent 评估\|Agent 1: 流程合规性" skills/kflow-audit/SKILL.md` 无命中
- [x] 1.4 设计文档 → SKILL.md 同步：改写「审计维度」章节——「七维度评估体系」改为「四维度评估体系」，维度表由 7 行改为 4 行并注明各维度的合并来源。验证：表中权重合计为 100%，四行维度名与 `design.md` D1 表格逐字一致
- [x] 1.5 设计文档 → SKILL.md 同步：改写「各维度按变更档位给分与不误扣规则」表——按新四维度重组，原七行中每条 SHALL NOT 误扣声明均须在新表中找到归属。验证：以 `git diff` 逐条比对改写前后的 SHALL NOT 声明，无一条丢失
- [x] 1.6 设计文档 → SKILL.md 同步：补入「证据先于评分」执行约束（先完成四维度事实采集并逐维度呈现证据，再统一评分）与「子代理隔离规则」内联声明（异常时新建子代理、禁止主 Agent 接管、重试上限 3 次、不适用轮次级重试粒度；以相对本 skill 的路径引用形式标注）。验证：与 delta 的 `证据先于评分` 场景及 `subagent-isolation-rule` delta 的 `审计阶段的规则适用子集` 场景逐条对应
- [x] 1.7 设计文档 → SKILL.md 同步：改写「审计报告格式（标准 / 完整 档）」——评分表由 7 行改为 4 行并标注总分为健康度参考、不参与门控；同步改写「简化审计记录格式（轻量 档）」中的七维度措辞。验证：两处格式与 `docs/designs/templates/changes/{change}/audit-report.md` 的形态 A / 形态 B 一致
- [x] 1.8 设计文档 → SKILL.md 同步：改写「核心提醒」清单与「与其他 Skill 的关系」段落；「轻量档轻量自检路径」中「降为主 Agent 轻量自检」改为「降为轻量自检（由审计子代理执行）」。验证：`grep -n "七维度\|六维度\|主 Agent 轻量自检" skills/kflow-audit/SKILL.md` 无命中

## 2. 下游 Skill 与 references 措辞同步

- [x] 2.1 设计文档 → SKILL.md 同步：`skills/kflow-archive/SKILL.md` 的门控检查段与归档前检查清单，把「kflow-audit 七维度评估（通过）」改为「kflow-audit 四维度评估（通过）」。验证：`grep -n "七维度" skills/kflow-archive/SKILL.md` 无命中
- [x] 2.2 设计文档 → SKILL.md 同步：`skills/kflow-archive/references/archive-rules.md` 归档检查清单首项同步为四维度。验证：`grep -n "七维度" skills/kflow-archive/references/archive-rules.md` 无命中
- [x] 2.3 设计文档 → SKILL.md 同步：`skills/kflow-guide/SKILL.md` Skill 路由表「审计」行的「七维度评估」改为「四维度评估」。验证：`grep -n "七维度" skills/kflow-guide/SKILL.md` 仅剩 kflow-verify 所在行

## 3. 设计文档镜像同步（`docs/designs/`）

- [x] 3.1 `docs/designs/skills/kflow-audit.md` 全文同步至与 `skills/kflow-audit/SKILL.md` 同口径（description、审计路径分流表、四维度表、按档位给分规则、报告格式、核心提醒）。验证：逐节比对两份文件，无口径差异
- [x] 3.2 `docs/designs/skills/kflow-archive.md` 与 `docs/designs/skills/kflow-guide.md` 的审计描述行同步为四维度。验证：两文件 `grep -n "七维度"` 无命中
- [x] 3.3 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：流程图中 `审计(轻量自检，门控)` 节点与档位分支说明段改为「单子代理 + 四维度」。验证：`grep -n "七维度"` 无命中
- [x] 3.4 `docs/designs/index.md`、`docs/designs/overview.md`、`docs/designs/skills/index.md` 的维度描述与权重同步（含 `index.md` 档位表的「审计形态」列、`overview.md` 的阶段职责表与设计要点表、`skills/index.md` 的 Skill 表与审计门控要点）。验证：三文件 `grep -n "七维度\|六维度"` 无命中
- [x] 3.5 `docs/designs/templates/changes/{change}/audit-report.md`：形态 B 评分表改 4 行、front matter 的 `template_description` 同步、`version` 递增、修订记录区追加条目。验证：满足 `stage-doc-templates` 的 `产物格式变更时更新模板` 场景（版本号递增 + 修订记录）
- [x] 3.6 `docs/designs/examples/audit-report.md` 改写为四维度示例，`docs/designs/examples/index.md` 的描述行同步。验证：示例含 4 行评分表且加权合计算术正确

## 4. README 同步

- [x] 4.1 README 档位对照表的「审计形态」行改为「单一子代理轻量自检（三项检查项）」/「单一子代理四维度加权评分」；kflow-audit 描述行的权重串与「七维度审计」同步为四维度。验证：`grep -n "七维度" README.md` 仅剩 kflow-verify 相关行
- [x] 4.2 README 中「审计降级为主 Agent 轻量自检」的表述改为「审计由单一子代理执行」。验证：该表述与 `skills/kflow-audit/SKILL.md` 的分流表逐字一致

## 5. 规格残留收口（主规格与 delta 配对修改）

- [x] 5.1 修正 `openspec/specs/devflow-audit/spec.md` 的 Purpose：「六维度评估」改为四维度口径（既有 capability 的 Purpose 无法由 delta 表达，须直改主规格）。验证：`openspec validate simplify-audit-single-agent` 通过
- [x] 5.2 更正 scenario 标题：把 `openspec/specs/devflow-audit/spec.md` 与 delta 中的 `标准档与完整档维持七维度审计` **同时**改为 `标准档与完整档维持四维度审计`，并删除 delta 中解释标题保留原因的非规范性说明。验证：`openspec validate simplify-audit-single-agent` 与 `openspec validate simplify-audit-single-agent --strict` 均通过

## 6. 集成验证

- [x] 6.1 全仓残留扫描：`grep -rn "七维度\|六维度" skills/ docs/ README.md openspec/specs/`。验证：命中的每一行均归属 kflow-verify 的七维度产物诊断（`skills/kflow-verify/`、`docs/designs/skills/kflow-verify.md`、`docs/designs/skills/kflow-bug-triage.md`、`openspec/specs/phase-artifact-verification/`）或 `skills/kflow-guide/SKILL.md` 的产物诊断行，无一行属审计
- [x] 6.2 门控链路走查：按改写后的 `skills/kflow-audit/SKILL.md` 逐步走查 EVALUATE → SCORE → REPORT，确认「单一子代理」「四维度」「证据先于评分」「总分为健康度参考」四项与 delta 逐条对应。验证：产出走查记录，每条结论标注其对应的 delta requirement / scenario
- [x] 6.3 校验闭环：`python scripts/validate-frontmatter.py` 与 `openspec validate simplify-audit-single-agent --strict`。验证：两条命令均无 ERROR

> **本组验证记录**：走查结论、残留分类与校验输出见同目录 `review.md`。
>
> **6.1 的主规格残留收口**：`skills/`、`docs/`、`README.md` 的审计域旧口径已零残留；`openspec/specs/devflow-audit/spec.md` 中剩余的审计旧口径全部由本变更 delta 在归档时替换。按本仓库既有做法（`openspec/changes/archive/2026-09-29-sync-legacy-prototype-specs/tasks.md` 任务 6.2）以临时副本模拟 `openspec archive` 后复扫：审计域命中数为 0，`openspec validate --specs` 129 通过 / 0 失败。详见 `review.md` §3.2。
