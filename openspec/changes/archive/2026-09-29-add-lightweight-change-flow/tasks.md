# Tasks

## 1. 核心机制文档

- [x] 1.1 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`：在变更级 `.status.md` 中加入「阶段适用性声明」区（逐阶段记录 适用 / `⏭️ 不适用` 及判定依据），并说明阶段状态表以 `⏭️` 表示裁剪、缺失声明时按全部适用处理。验证：该文件含适用性声明区定义与缺省规则表述。
- [x] 1.2 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md`：在门控规则中加入裁剪分支——声明不适用且产物不存在为通过、按变更档位的裁剪仅适用于轻量档、归档门控接受有声明依据的裁剪。验证：该文件的门控章节含四种产物状态的判定表与轻量档限定表述。
- [x] 1.3 更新 `docs/designs/core-mechanisms/08-governance.md`：将阶段裁剪与覆盖率分母排除的口径纳入治理说明，明确「无声明依据的 `⏭️` 一律阻塞」。验证：该文件含裁剪合法性的判定原则。
- [x] 1.4 更新 `docs/designs/index.md` 与 `docs/designs/overview.md`：新增「轻量档阶段裁剪」决策项，并修订阶段流转示意中轻量档的阶段集合。验证：两文件的决策表含裁剪条目，阶段流转示意中轻量档的接口单元测试与 E2E 测试标注为条件适用。

## 2. 设计文档 → Skill 规格同步

- [x] 2.1 更新 `docs/designs/skills/kflow-design.md`：DIVIDE 步骤新增「轻量档跳过划分，直接产出单一子变更」分支与「FP 类型混合时升档为标准」处理；新增「阶段适用性声明」步骤（DIVIDE 之后），含三项判定条件、保守回退规则与写入位置。验证：文件含单一子变更分支、升档分支与适用性声明步骤，且判定条件与保守回退有明确表述。
- [x] 2.2 更新 `docs/designs/skills/kflow-explore.md`：档位初判后提示该档位的阶段集合；轻量档不改动探索流程本身。验证：文件含按档位的阶段集合提示。
- [x] 2.3 更新 `docs/designs/skills/kflow-api-test.md` 与 `kflow-e2e-test.md`：新增阶段适用性入口门控（读取声明、四态判定、裁准时跳过并标记 `⏭️`）；说明标准档与完整档不受影响。验证：两文件含适用性门控与四态判定，且含「仅轻量档」限定。
- [x] 2.4 更新 `docs/designs/skills/kflow-integration-test.md`：新增适用性入口门控；裁准时直接进入审计阶段；归档门控视裁剪为满足。验证：文件含裁剪分支与「直接进入审计」表述。
- [x] 2.5 更新 `docs/designs/skills/kflow-audit.md`：新增轻量档轻量自检路径（三项检查项、简化记录形态、保留归档门控地位），并说明标准档与完整档维持七维度加权评分。验证：文件含轻量自检检查项与门控地位说明。
- [x] 2.6 更新 `docs/designs/skills/kflow-archive.md`：归档条件接受有声明依据的裁剪阶段，无依据的 `⏭️` 阻塞归档并提示缺失裁剪依据。验证：文件的归档条件清单含裁剪处理条目。
- [x] 2.7 更新 `docs/designs/skills/kflow-guide.md`：流程概览按变更档位显示实际阶段集合，轻量档标注不适用阶段；未生成适用性声明时显示完整集合并附提示。验证：文件的流程概览章节含档位分支与两种状态的展示规则。
- [x] 2.8 更新 `docs/designs/skills/kflow-verify.md`：产物诊断将「有声明依据的裁剪产物缺失」判为正常，不报缺项；将「无声明依据的 `⏭️`」判为问题。验证：文件的诊断规则含裁剪判定分支。
- [x] 2.9 更新 `docs/designs/skills/kflow-plan.md` 与 `docs/designs/skills/kflow-code.md`：任务清单与编码遍历对单子变更（轻量档）的表述做一致性核对，确认无「遍历全部子变更」对单子变更产生的错误提示。验证：两文件对单子变更场景的表述无冲突。

## 3. Skill 实现同步（设计文档 → SKILL.md 同步）

- [x] 3.1 同步 `skills/kflow-design/SKILL.md` 与 `references/gates.md`、`references/state-values.md`：实现轻量档 DIVIDE 简化分支、FP 类型混合升档、阶段适用性声明步骤与写入。验证：SKILL.md 的执行流程含适用性声明步骤与两个分支，gates.md 含裁剪判定，state-values.md 含适用性声明字段透传。
- [x] 3.2 同步 `skills/kflow-api-test/SKILL.md` 与 `references/gates.md`、`references/hooks.md`：入口门控读取适用性声明，裁准时跳过且不启动子代理、不执行服务刷新钩子。验证：SKILL.md 含裁剪分支，hooks.md 说明裁准时钩子不执行。
- [x] 3.3 同步 `skills/kflow-e2e-test/SKILL.md` 与 `references/gates.md`、`references/hooks.md`：同 3.2 口径。验证：两 skill 的裁剪分支表述一致。
- [x] 3.4 同步 `skills/kflow-integration-test/SKILL.md` 与 `references/gates.md`、`references/hooks.md`：入口门控读取适用性声明，裁准时跳过并直接进入审计。验证：SKILL.md 含裁剪分支与「直接进入审计」流程。
- [x] 3.5 同步 `skills/kflow-audit/SKILL.md`：实现轻量档轻量自检路径（三项检查项、简化记录输出、保留归档门控），标准档与完整档维持七维度评分。验证：SKILL.md 含两条审计路径的分支与各自的产物形态。
- [x] 3.6 同步 `skills/kflow-archive/SKILL.md` 与 `references/archive-rules.md`：归档条件清单接受有声明依据的裁剪，无依据的 `⏭️` 阻塞。验证：archive-rules.md 的归档条件清单含裁剪处理条目。
- [x] 3.7 同步 `skills/kflow-guide/SKILL.md`：流程概览按档位显示阶段集合与不适用标注。验证：SKILL.md 的流程概览章节含档位分支。
- [x] 3.8 同步 `skills/kflow-verify/SKILL.md` 与 `references/`：诊断规则接受有依据的裁剪、检出无依据的 `⏭️`。验证：诊断规则含裁剪分支。
- [x] 3.9 同步 `skills/kflow-explore/SKILL.md`、`skills/kflow-plan/SKILL.md`、`skills/kflow-code/SKILL.md` 与各自 `references/state-values.md`：透传并读取阶段适用性声明；核对单子变更场景的遍历表述。验证：三份 state-values.md 含适用性声明字段，单子变更表述无冲突。
- [x] 3.10 运行 `scripts/sync-references.sh`，修复因本轮改动引入的同名 references 文件不一致。验证：脚本通过且无新增不一致报告。

## 4. 模板与项目文档

- [x] 4.1 更新 `docs/designs/templates/changes/{change}/change-status.md`：新增「阶段适用性声明」区（逐阶段结论与判定依据）。验证：模板含该区与字段说明。
- [x] 4.2 更新 `docs/designs/templates/changes/{change}/traceability.md`：覆盖总览表支持 `⏭️` 列填充与 `N/A` 状态，阶段覆盖统计表含分母排除说明。验证：模板含 `⏭️` 列示例与覆盖率分母定义。
- [x] 4.3 更新 `docs/designs/templates/changes/{change}/audit-report.md`：支持轻量自检形态（三项检查项结论 + 问题清单），保留七维度评分表为另一形态。验证：模板同时覆盖两种形态且标注适用档位。
- [x] 4.4 更新 `README.md`：补充轻量档阶段裁剪机制说明，明确标准档与完整档不受影响。验证：README 含裁剪机制说明与档位适用范围。

## 5. 全链路一致性校验

- [x] 5.1 覆盖率语义校验：以一份含裁剪阶段的虚构 `traceability.md` 为输入，核对覆盖率分母排除后的计算与门控结论。验证：分母不含 `⏭️` 列；裁剪列不参与 100% 判定；无声明依据的 `⏭️` 使归档阻塞。
- [x] 5.2 四态判定校验：构造四种「声明 × 产物」组合（不适用/不存在、不适用/存在、适用/存在、适用/不存在），逐一核对门控结论。验证：分别为通过、阻塞、通过、阻塞，且阻塞提示区分两种情况。
- [x] 5.3 档位隔离校验：grep 确认阶段裁剪的判定与分支仅出现在轻量档条件下，标准档与完整档的路径无裁剪逻辑。验证：相关文件中的裁剪分支均带轻量档限定，纯后端项目跳过 E2E 的既有规则未被改写。
- [x] 5.4 端到端路径走查：以轻量档单子变更（1 个前端 FP、0 接口）与轻量档后端变更（1 个后端 FP、1 个接口）为输入，沿 explore → design（含 DIVIDE 与适用性声明）→ plan → code → code-review → 测试阶段 → 审计 → 归档 的路径核对跳过分支与门控落点。验证：前端路径跳过接口单元测试与集成测试、保留 E2E；后端路径跳过 E2E、保留接口单元测试与集成测试；两条路径的审计均走轻量自检。
- [x] 5.5 类型混合升档校验：以轻量档同时含后端与前端 FP 的变更走查 DIVIDE，确认升档为标准档、经用户确认、产出两个子变更且不生成适用性声明。验证：走查结论与规格一致。
- [x] 5.6 运行 `openspec validate add-lightweight-change-flow` 与 `openspec validate add-change-tier`，确认两个变更的规格增量均通过校验。验证：两条命令均输出 valid。
