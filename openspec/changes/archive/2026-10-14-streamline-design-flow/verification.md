# 集成验证记录

> 本文件承载 `tasks.md` 第 7 组（集成验证）的走查与遥测验证记录。范围说明：本文件是变更的验证证据，不属于归档、版本自增、打包等元工作流范畴。

## 1. 端到端流程走查（任务 7.3）

**样例**：`标准档 功能需求`（前后端项目，功能点数 8 → 影响范围分数落在 4~15 区间 → `标准` 档）。

**阶段流转**：设计探索 → 原型设计（前后端项目必须）→ 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试 → 集成测试 → 审计 → 归档。

| # | 阶段 | 输入产物 | 执行方式 | 输出产物 | 门控判据 |
|---|------|---------|---------|---------|---------|
| 1 | 设计探索 | 用户需求、产品级 `functional-designs/`、`CONTEXT.md` | 主 Agent 直连（CLARIFY 收敛门 → SPLIT → TIER 初判 → RELATE）+ SELFREV：签署自证（主 Agent，零子代理）→ 1 轮独立子代理验证 | 变更级 `functional-designs/`（index.md + part-NN.md，含「完成前签署」区）、`.status.md`（含变更档位与两遥测区） | 产物齐全 + `self-reviews/explore/report.md` 存在 + 终止结果 ∈ {`验证通过`, `验证发现问题({N})`} |
| 2 | 原型设计 | `functional-designs/`、`element-coverage-tree.md` | DESIGN（子代理委托）→ BUILD 四项静态门控（主 Agent 直接执行，零子代理）→ 审查方式选择 → VERIFY 单轮合并验证（1 个子代理、1 份报告）+ SELFREV 单轮验证 | `docs/designs/prototypes/`、`prototype-changes.md`、`self-reviews/prototype/cdn-crossref-check/report.md`、`self-reviews/prototype/report.md`、`self-reviews/prototype/verify-report.md` | BUILD 四项全部通过 + 用户评审确认 + `report.md` 与 `verify-report.md` 存在（审查方式 = 子代理自动审查验证 时） |
| 3 | 详细设计 | `functional-designs/`、原型产物 | 主 Agent 直连（DETAIL → TIER_RECHECK 复核升档 → DIVIDE → 测试用例设计）+ SELFREV 单轮验证 + REVIEW 交叉审查（`标准` 档两视角并行） | `detailed-design.md`（含签署区）、`api-tests/`、`e2e-tests/`、`traceability.md`、`cross-reviews/{ts}/business-technical-review.md` + `security-quality-review.md` + `synthesis.md`、`self-reviews/design/report.md` | Gate 2：详细设计 ✅ 完成 + `report.md` 存在 + 两视角报告与 `synthesis.md` 通过 + NFR 章节达标 + 用户评审确认 |
| 4 | 计划 | `detailed-design.md`、`api-tests/`、`e2e-tests/` | 主 Agent 直连（任务划分 + DoD）+ SELFREV 单轮验证（步骤 8.5） | `subchanges/*/tasks.md`（含签署区：任务覆盖完整性 / DoD 验收标准正确性 / HITL 标注准确性 / 任务粒度合理性）、`self-reviews/plan/report.md` | 各子变更 `tasks.md` 存在且格式合规 + `report.md` 存在 + 终止结果合法 |
| 5 | 编码 | `subchanges/*/tasks.md` | 重复制循环（子代理迭代执行 TDD 垂直切片；每轮全量遍历全部功能点） | 代码变更、`migration-log.md`、`.status.md` 执行轮次与两遥测区更新 | 验收 = 执行报告完整（含全量遍历证明）+ 产物齐全 + `traceability.md` 编码列 = 100% + 无占位符；终止结果 `执行完成` |
| 6 | 代码审查 | 代码变更、`tasks.md` | 重复制循环（`标准` 档两视角并行；每轮全量遍历全部待审查子变更） | `subchanges/*/test-reports/review/code-review.md` | 审查通过标记 + 终止结果 `执行完成` |
| 7 | 接口单元测试 | `api-tests/`、接口实现 | 单轮全面执行 + 定向重验（仅重跑失败用例） | `subchanges/*/test-reports/api/round-{n}.md`、`summary.md` | `summary.md` 健康评分达标 + `traceability.md`「接口测试(ID)」列 = 100% + 定向重验全部通过；终止结果 `执行完成` |
| 8 | E2E测试 | `e2e-tests/`、前端实现 | 单轮全面执行 + 定向重验 | `subchanges/*/test-reports/e2e/round-{n}.md`、`summary.md` | `summary.md` 达标 + `traceability.md`「E2E测试」列 = 100% + 定向重验全部通过；终止结果 `执行完成` |
| 9 | 集成测试 | 变更级集成产物、各子变更完成状态 | 单轮全面执行 + 定向重验；变更级服务刷新（编译 → 迁移 → 重启 → 健康检查） | `test-reports/integration/summary.md`、`integration/arch-assessment.md`（按需） | 集成测试通过 + 终止结果 ∈ {`执行完成`, `定向重验失败`（须有升级记录）} |
| 10 | 审计 | 全部阶段产物、`.status.md` | 单一子代理执行四项记账职责（门控校验 / 覆盖率与产物校验 / 耗时汇总 / 阻塞兜底） | `audit-report.md`（记账记录形态：四项职责结论 + 耗时效率摘要 + 分级问题清单 + 改进建议） | 无阻塞级问题 → 放行归档；存在阻塞级问题 → 阻断归档并要求修复后重新审计 |
| 11 | 归档 | `audit-report.md`、各阶段产物 | `kflow-archive`（产品级合并 + 计时摘要回流） | 产品级 `docs/designs/` 合并结果、`docs/changes/index.md`、`docs/skill-suggestion.md` 计时摘要条目 | 审计无阻塞 + 用户验收确认 ✅ + traceability 全部适用列 = 100% |

**走查结论**：11 个阶段的输入产物、执行方式、输出产物与门控判据均可对应到本次变更后的规范，无断链、无引用已废除机制的判据。阶段流转可跑通。

**关键变更点在走查中的体现**：

- 设计探索 / 详细设计 / 计划：SELFREV 由多轮循环变为「签署自证（零子代理）+ 1 轮独立子代理验证 + 统一修复」，轮数固定为 1。
- 原型设计：VERIFY 三环节（导航 / Playwright / UX）合并为单轮单报告 `verify-report.md`，对比度检测为静态计算；BUILD 门控不受影响。
- 编码 / 代码审查：重复制循环与轮间摘要保持不变，仅验收判据与终止结果取值同步。
- 接口单元测试 / E2E测试 / 集成测试：由多轮循环改为单轮全面执行 + 定向重验。
- 审计：由四维度加权评分改为四项记账职责，保留阻塞级拦截权。

## 2. 计时遥测验证（任务 7.4）

### 2.1 两个遥测区可被各阶段写入

`.status.md` 的两个遥测区（「阶段耗时与轮次统计」与「阶段内事件计时」）的字段定义见 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.1，字段语义见 `skills/kflow-*/references/state-values.md` §6。走查样例的写入结果如下（样例数据）：

```markdown
## 阶段耗时与轮次统计

| 阶段 | 开始时间 | 结束时间 | 耗时 | 子代理轮次 | 执行方式 |
|------|---------|---------|------|-----------|---------|
| 设计探索 | 2026-10-14 09:00 | 2026-10-14 10:40 | 1h40m | 1 | 单轮验证 |
| 原型设计 | 2026-10-14 11:00 | 2026-10-14 14:30 | 3h30m | 1 | 单轮验证 |
| 详细设计 | 2026-10-14 15:00 | 2026-10-14 19:20 | 4h20m | 1 | 单轮验证 + 多视角审查 |
| 计划 | 2026-10-15 09:00 | 2026-10-15 10:30 | 1h30m | 1 | 单轮验证 |
| 编码 | 2026-10-15 11:00 | 2026-10-15 19:00 | 8h00m | 3 | 重复制循环 |
| 代码审查 | 2026-10-16 09:00 | 2026-10-16 11:30 | 2h30m | 2 | 重复制循环 |
| 接口单元测试 | 2026-10-16 13:00 | 2026-10-16 15:10 | 2h10m | 2 | 定向重验 |
| E2E测试 | 2026-10-16 15:30 | 2026-10-16 18:00 | 2h30m | 1 | 单轮执行 |
| 集成测试 | 2026-10-17 09:00 | 2026-10-17 12:00 | 3h00m | 1 | 单轮执行 |
| 审计 | 2026-10-17 13:00 | 2026-10-17 14:00 | 1h00m | 1 | 单代理执行 |
| 归档 | 2026-10-17 14:10 | 2026-10-17 14:40 | 30m | -- | 主 Agent 直接执行 |

## 阶段内事件计时

| 阶段 | 事件 | 开始时间 | 结束时间 | 耗时 |
|------|------|---------|---------|------|
| 编码 | 子代理轮次 1 | 2026-10-15 11:00 | 2026-10-15 14:00 | 3h00m |
| 编码 | 子代理轮次 2 | 2026-10-15 14:10 | 2026-10-15 16:50 | 2h40m |
| 编码 | 子代理轮次 3 | 2026-10-15 17:00 | 2026-10-15 18:40 | 1h40m |
| 编码 | 门控校验 | 2026-10-15 18:50 | 2026-10-15 19:00 | 10m |
| 详细设计 | 签署自证 | 2026-10-14 15:00 | 2026-10-14 16:00 | 1h00m |
| 详细设计 | 单轮验证 | 2026-10-14 16:10 | 2026-10-14 17:20 | 1h10m |
| 详细设计 | 统一修复 | 2026-10-14 17:30 | 2026-10-14 18:00 | 30m |
| 详细设计 | 交叉审查 | 2026-10-14 18:10 | 2026-10-14 19:20 | 1h10m |
```

**展开判定**：编码阶段耗时 8h00m 占变更总耗时约 27%，未超过 40% 阈值；但其子代理轮次为 3，命中轮次阈值，故展开该阶段的内部事件计时并标注为最耗时阶段（耗时绝对值最高）。详细设计阶段耗时占比约 15%，未命中耗时阈值，但其事件计时一并列出以演示四类事件（签署自证 / 单轮验证 / 统一修复 / 交叉审查）的落点。

> 注：触发阈值（耗时占比 40% / 子代理轮次阈值）的具体数值可在收集前 3~5 个变更的真实数据后校准，不影响字段结构定义。

### 2.2 归档时计时摘要回流 `docs/skill-suggestion.md`

归档阶段按 `phase-time-telemetry` 能力的「计时摘要回流改进建议记录」Requirement 追加如下条目（样例）：

```markdown
## 计时摘要：streamline-design-flow-sample

- **变更名**: streamline-design-flow-sample
- **总耗时**: 约 29h30m（跨 4 个工作日）
- **各阶段耗时与轮次**:
  | 阶段 | 耗时 | 子代理轮次 | 执行方式 |
  |------|------|-----------|---------|
  | 设计探索 | 1h40m | 1 | 单轮验证 |
  | 原型设计 | 3h30m | 1 | 单轮验证 |
  | 详细设计 | 4h20m | 1 | 单轮验证 + 多视角审查 |
  | 计划 | 1h30m | 1 | 单轮验证 |
  | 编码 | 8h00m | 3 | 重复制循环 |
  | 代码审查 | 2h30m | 2 | 重复制循环 |
  | 接口单元测试 | 2h10m | 2 | 定向重验 |
  | E2E测试 | 2h30m | 1 | 单轮执行 |
  | 集成测试 | 3h00m | 1 | 单轮执行 |
  | 审计 | 1h00m | 1 | 单代理执行 |
  | 归档 | 30m | -- | 主 Agent 直接执行 |
- **最耗时阶段**: 编码（8h00m，占 27%；子代理轮次 3，命中轮次阈值）
- **改进建议**: 编码阶段的 3 轮重复制循环耗时集中，可在后续变更中观察其轮次分布是否随工作项粒度变化。
```

**累积趋势可读性**：该条目与既有条目按同一字段结构排列，支持按阶段横向比较耗时与子代理轮次的变化趋势（例如对比多个变更的「编码」阶段耗时与轮次）。

**回流失败不阻塞归档**：计时摘要回流失败时归档流程 SHALL 继续执行，并向用户提示失败原因与手工补救方式。

## 3. 验证结论

- 任务 7.3（端到端流程走查）：11 个阶段的输入产物、执行方式、输出产物与门控判据均可对应到本次变更后的规范，无断链、无已废除机制的判据残留。
- 任务 7.4（计时遥测验证）：两个遥测区的字段结构可被各阶段写入；归档时计时摘要回流规则可执行，回流失败不阻塞归档。

## 4. 工具校验结果（任务 7.1）

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `python scripts/validate-frontmatter.py` | 0 | 通过 40，失败 0；所有 front matter 与设计规格 yaml 代码块合法 |
| `bash scripts/sync-references.sh` | 0 | 检查项 6，6 个多 skill 共享 references 文件（repetition.md / hooks.md / gates.md / state-values.md / service-lifecycle.md / self-review.md）**全部一致**，无跨 skill 引用告警 |

## 5. 全仓检索一致性（任务 7.2）

```bash
grep -rn "见证轮\|不收敛\|收敛驱动\|安全丝\|累积未复核" skills/kflow-*/SKILL.md skills/kflow-*/references/*.md
# exit=1（零命中）
```

`docs/designs/` 与 `README.md` 同样零命中；保留的命中仅为以下两类**有意保留**项：

| 位置 | 内容 | 保留理由 |
|------|------|---------|
| 各阶段 SKILL.md 与 `docs/designs/` 的终止结果判读段 | 历史取值 `收敛` / `未收敛` 的归并规则 | spec 明文要求的读取兼容规则（`收敛` → `验证通过`，其余 → `验证发现问题`） |
| `docs/designs/core-mechanisms/07-agent-model.md` 与 `repetition.md` | 与已移除的 `recheck-round` 的命名区分说明 | design.md 约束 2 要求显式区分「定向重验」与 `recheck-round` |
| `README.md` 版本更新说明区（v0.18.0 及更早） | 历史版本条目 | 记录既往变更事实，不改写 |
| `skills/kflow-explore/references/clarify-convergence.md` | 需求澄清收敛门（CLARIFY） | 独立机制，不在本次改造范围；术语与自审单轮化无冲突 |

## 6. 设计规格 → SKILL.md 逐阶段一致性（任务 8.1）

| 阶段 | 设计规格 | SKILL.md | 核对项与结果 |
|------|---------|---------|-------------|
| explore | `docs/designs/skills/kflow-explore.md` | `skills/kflow-explore/SKILL.md` | 签署清单/证据锚点 ✓；终止结果 `验证通过`/`验证发现问题({N})` ✓；档位无「产品需求 → 完整」映射 ✓；报告 `self-reviews/explore/report.md` ✓ |
| design | `kflow-design.md` | `skills/kflow-design/SKILL.md` | 同上（report 路径为 `self-reviews/design/report.md`）✓；REVIEW 档位映射未变 ✓ |
| prototype-design | `kflow-prototype-design.md` | `skills/kflow-prototype-design/SKILL.md` | 签署清单 ✓；VERIFY 单轮合并报告 `self-reviews/prototype/verify-report.md`（四分区 + 验证结论）✓；BUILD 四项静态门控保留 ✓ |
| plan | `kflow-plan.md` | `skills/kflow-plan/SKILL.md` | 签署清单 ✓；4 维度含 HITL 标注准确性 ✓；报告 `self-reviews/plan/report.md` ✓；步骤编号 SELFREV=8.5 ✓；主工作由子代理执行 ✓ |
| api-test | `kflow-api-test.md` | `skills/kflow-api-test/SKILL.md` | 单轮全面执行 + 定向重验 ✓；终止结果 `执行完成`/`定向重验失败` ✓；产物 `round-{n}.md` + `summary.md` 与模板一致 ✓ |
| e2e-test | `kflow-e2e-test.md` | `skills/kflow-e2e-test/SKILL.md` | 同上 ✓ |
| integration-test | `kflow-integration-test.md` | `skills/kflow-integration-test/SKILL.md` | 同上 ✓ |
| audit | `kflow-audit.md` | `skills/kflow-audit/SKILL.md` | 四项记账职责 ✓；无加权评分表 ✓；阻塞级拦截权与归档门控地位保留 ✓ |

**结论**：本次变更涉及的全部 8 个阶段的规格与 SKILL.md 关键口径逐项对应，无未同步项。

## 7. 自包含性（任务 8.2）

`scripts/sync-references.sh` 退出码 0，无跨 skill 引用告警；各 skill 的辅助规则（`references/` 下的门控、自审规范、重复制规范、状态值定义、阶段钩子）均位于自身目录内，安装后零外部依赖。

## 8. 版本字段一致性（任务 8.3）

仓库根 `VERSION` = `0.23.0`；18 个 `skills/kflow-*/SKILL.md` 的 `version` 字段全部为 `0.23.0`，逐一比对一致（`scripts/sync-version.sh` 执行前的准备条件已满足）。本次变更的版本自增由 CLAUDE.md「归档后规则」驱动。
