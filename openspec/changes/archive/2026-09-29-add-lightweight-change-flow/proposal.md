# Proposal

## Why

变更 `add-change-tier` 让轮次随变更规模变化，但仍要求每个阶段都执行。一个 1 个功能点的缺陷依然要走完 接口单元测试 → E2E测试 → 集成测试 → 七维度审计 的阶段链，其中多数阶段对该变更是空转：没有接口变更却执行接口测试，没有 UI 变更却执行浏览器测试，变更只有单一子变更却执行跨子变更集成测试。**剩余成本的主要来源是阶段数量，而非轮次数量。**

同时，`traceability.md` 的覆盖率门控要求所有适用列 100%，阶段被裁剪时该列必然为空，会把合法裁剪判成覆盖率缺口并阻塞归档。现有规范只定义了「按项目类型跳过」（纯后端跳 E2E），没有定义「按变更规模跳过」——`conditional-product-refs` 的三种处理情况（跳过、完成有文件、待开始）缺少「因变更为轻量档而不适用」这一种。

## What Changes

**新增「轻量档阶段适用性声明」**

- kflow-design 在 DIVIDE 之后扫描 `detailed-design.md`，为本变更逐阶段判定适用性，写入变更级 `.status.md`。
- 判定条件：接口单元测试——本变更含新增或修改接口；E2E测试——前后端项目且本变更含 UI 变更；集成测试——本变更含新增或修改接口，或存在跨模块契约变更。
- 适用性声明为**显式可审**的记录，使「因不适用而跳过」与「遗漏产物」可区分。

**产物存在性与声明双重校验**

- 声明为不适用的阶段不产出对应阶段产物（`api-tests/`、`e2e-tests/`）。
- 下游阶段按声明与产物的一致判定：声明不适用且产物不存在为合法跳过；声明适用但产物缺失为阻塞；声明不适用但产物存在为不一致，阻塞并提示。

**轻量档跳过子变更划分**

- 轻量档恒为单一子变更，跳过 DIVIDE 步骤的依赖关系分析与划分表（单一子变更的类型由 FP 类型一致性校验直接得出）。
- FP 类型混合时轻量档不成立（子变更类型严格二分，混合必须拆分为多个子变更），系统 SHALL 升档为 `标准`，复用 `add-change-tier` 的单向升档机制，SHALL NOT 直接阻塞。

**覆盖追溯矩阵适配裁剪**

- `traceability.md` 中被裁剪的阶段对应列以 `⏭️` 填充，且**不计入覆盖率分母**。覆盖率 = 已填充格数 / (总格数 - 不适用格数)。
- 覆盖率门控对裁剪阶段分支：不适用列不参与 100% 判定，不因裁剪而阻塞。

**审计降为轻量自检**

- 轻量档审计由七维度加权评分子代理审计降为主 Agent 轻量自检，检查项为：阶段完整性（无越界跳阶段）、产物存在性与无占位符、裁剪合法性（每个 `⏭️` 阶段有适用性声明依据）。
- 轻量自检**保留归档门控地位**，不通过仍阻塞归档；输出简化审计记录而非七维度评分报告。

**归档与门控接受合法裁剪**

- 归档前最终覆盖检查、集成测试门控、进入集成测试前的前置覆盖检查，均将合法的 `⏭️` 不适用状态视为满足。
- 流程概览按档位展示实际阶段集合，轻量档的不适用阶段标记为 `⏭️`。

**范围边界**

- 上述裁剪**仅适用于轻量档**。标准档与完整档的阶段集合维持现状（纯后端项目跳过 E2E 的既有规则不变）。

## Capabilities

### New Capabilities

- `lightweight-flow-trimming`: 定义轻量档的阶段适用性声明机制（判定条件、写入位置、产物存在性双重校验）、轻量档跳过子变更划分的规则与 FP 类型混合时的升档处理。

### Modified Capabilities

- `coverage-traceability`: 覆盖总览表新增 `⏭️` 不适用格与覆盖率分母排除规则；覆盖率门控对裁剪阶段分支；归档前最终覆盖检查接受合法裁剪。
- `conditional-product-refs`: 条件产物引用的跳过处理新增「因轻量档不适用而跳过」这一情况，与既有的「按项目类型跳过」并列。
- `subchange-phase-unification`: 子变更 5 阶段在轻量档下条件适用——接口单元测试与 E2E 测试可标记为 `⏭️` 不适用。
- `integration-testing`: 集成测试阶段的触发与门控增加轻量档裁剪分支；轻量档无接口变更且无跨模块契约变更时阶段标记为 `⏭️` 不适用，归档门控视其为满足。
- `subchange-type-validation`: FP 类型混合时的处理由「阻塞流程」改为「变更档位为轻量时升档为标准后重新划分，其余档位维持阻塞」。
- `devflow-audit`: 新增轻量档轻量自检形态，保留归档门控地位，不适用七维度加权评分。
- `devflow-guide`: 流程概览显示按变更档位输出实际阶段集合，标记不适用阶段。

## Impact

**规格层**：新增 1 个能力，修改 7 个既有能力。

**实现层**：`skills/kflow-design`（新增适用性声明步骤与 DIVIDE 简化分支）、`skills/kflow-explore/SKILL.md`（档位初判后的阶段集合提示）、`skills/kflow-code-review`（无需改动，裁剪不涉及）、`skills/kflow-api-test`、`kflow-e2e-test`、`kflow-integration-test`（阶段的适用性判断与跳过分支）、`skills/kflow-audit`（轻量自检路径）、`skills/kflow-archive`（归档门控接受裁剪）、`skills/kflow-guide`（流程概览）、`skills/kflow-verify`（产物诊断接受裁剪）。相关 `references/gates.md`、`references/state-values.md`、`references/hooks.md` 需同步透传适用性声明。

**设计文档层**：`docs/designs/core-mechanisms/` 的 `03-status-and-tasks.md`（阶段状态表的不适用表示与适用性声明字段）、`04-gates-and-transitions.md`（门控分支）、`08-governance.md`；`docs/designs/skills/` 的相关 Skill 规格；`docs/designs/templates/changes/{change}/change-status.md` 与 `traceability.md` 模板、`audit-report.md` 模板；`README.md`。

**依赖**：本变更依赖 `add-change-tier` 提供的「变更档位」字段与单向升档机制。若 `add-change-tier` 未落地，本变更的适用性声明无档位依据，无法实现。

**与 `add-change-tier` 的规格重叠**：`devflow-audit` 的能力被两个变更同时修改。`add-change-tier` 改其「审计六维度评估」的档位给分口径，本变更在同一需求上追加裁剪豁免（合法裁剪的测试阶段不判缺项），并新增「轻量档审计降级为轻量自检」。为保证归档可依序进行，本变更的 `devflow-audit` 增量内容为 `add-change-tier` 编辑结果的**超集**（沿用同一需求名与全部原场景名，同时包含两轮编辑）。因此本变更的 `devflow-audit` 增量在 `add-change-tier` 归档前后均可正确应用，但两变更 MUST 按 `add-change-tier` 在前的顺序归档，以使实现层改动与规格一致。

**兼容性**：适用性声明为新增字段，历史变更缺失时按「全部阶段适用」处理，等价于现状，不改变进行中变更的行为。

**非目标**：

- 不调整轮次与审查分级（属 `add-change-tier`）。
- 不改变标准档与完整档的阶段集合。
- 不新增或合并产物文件路径，不新增 skill。
- 不处理 `shared-repetition-model`、`shared-self-review`、`devflow-archive`、`shared-archive-rules` 四个指向已不存在的 `.claude/skills/kflow-shared/` 的过期规格（需单独清理，`devflow-archive` 与 `shared-archive-rules` 为本轮新识别）。
