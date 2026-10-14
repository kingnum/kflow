# Proposal

## Why

KFlow 执行一个需求开发或缺陷修复任务，耗时显著长于 openspec 等轻量 Skills 体系。根因不在单个阶段执行慢，而在**审查循环的无界性**：2026-10-14 归档的 `converge-review-termination` 变更把多轮审查的终止模型反转为「以收敛为唯一成功终止条件」并删除轮数上限，其代价是任何一轮只要发现一个问题就必须再来一轮，而「零新发现」的判据在「全量遍历 4 维度、主动找问题」的审查语义下结构性倾向于永不满足。

按当前规范推演，一个标准档变更在设计链路上要跑 8 个独立的收敛循环（explore / prototype×3 / design / plan / 测试×3），每轮都要冷启动子代理、全量读产物、写报告文件；同一份 `detailed-design.md` 被自审、交叉审查、审计读了三遍。子代理轮次在 16~24 之间且**不可预测**——同样的文档质量可能跑 3 轮也可能跑 8 轮。

需要在**保留全部设计文档产出**的前提下，把审查从「无界循环发现」改为「写作时保证质量 + 单轮验证」，让流程贴近敏捷开发的快速设计-开发-测试-交付节奏，并记录各阶段耗时数据以支撑后续持续优化。

## What Changes

### 一、自审（SELFREV）单轮化 + 签署清单 **BREAKING**

- 删除「见证轮四项判据」「不收敛判定（无进展 / 振荡 / 安全丝）」「累积未复核修复清单」「轮间摘要注入」全套无界循环机制
- 设计类阶段（explore / prototype-design / design / plan）自审改为**固定单轮验证**：主 Agent 写作时按 4 维度**签署清单**逐项自证（零子代理），随后 1 轮独立子代理验证
- 验证子代理执行契约强制为：**先独立遍历产物形成自身结论（此阶段不读签署清单，防锚定）→ 再逐项打假签署清单 → 只报告不修改产物**
- 签署清单含**证据锚点列**（必须指向产物内的具体位置），锚点为空或指向不存在内容时签署不成立
- 主 Agent 按验证结论统一修复，生成「本阶段修复清单」随产物交付下游（审查者与修复者分离，消除「边审边修又改出新问题」的振荡源）
- 自审报告由「每轮一份、份数 = 轮数」改为固定一份 `report.md`
- `.status.md` 终止结果字段取值由 `收敛` / `未收敛` 改为 `验证通过` / `验证发现问题(N)`

### 二、审计（AUDIT）降级为记账员 **BREAKING**

- 删除四维度加权评分（流程与产物合规性 45%、审查与缺陷闭环 30%、测试充分性 15%、效率与改进 10%）
- 改为四项记账职责：校验各阶段门控是否全部通过、汇总阶段耗时数据、校验 traceability 覆盖率与产物存在性、兜底扫出未被前序环节关闭的阻塞级问题
- 保留「阻塞级问题」拦截权；评分与健康度评估不再产出

### 三、原型 VERIFY 三环节合并为单轮

- 导航合理性验证、Playwright 全覆盖验证、UX 规则审查三个独立收敛循环**合并为单轮单报告**
- 报告强制分区（导航 / Playwright / UX / 对比度四节独立结论 + 全量遍历证明），防止合并后某一环节被弱化
- BUILD 四项静态门控保持不变（主 Agent 直接执行、零子代理）
- 报告路径由 `nav-check/`、`playwright-check/`、`ux-check/` 三个目录改为单一合并报告

### 四、变更档位统一按影响范围分数判定 **BREAKING**

- 删除「变更类型为 `产品需求` 的变更档位 SHALL 抬升为 `完整`」的硬映射
- 产品需求档位改由影响范围分数（`功能点数 × 1 + 接口数 × 1.5 + 数据模型变更数 × 2`）与既有阈值（≤3 轻量 / 4~15 标准 / >15 完整）决定
- kflow-explore 初判规则同步调整

### 五、测试三阶段单轮化

- 接口单元测试、E2E 测试、集成测试由收敛驱动循环改为**单轮全面执行 + 定向重验**
- 定向重验仅重跑失败用例，不重跑全量；属**有界**重试，不构成收敛循环
- 编码与代码审查的重复制循环**保留不变**（多轮遍历工作项是真实价值）

### 六、阶段耗时遥测 `phase-time-telemetry`（新增）

- `.status.md` 新增「阶段耗时与轮次统计」区：阶段 × 开始 / 结束 / 耗时 / 子代理轮次 / 执行方式
- 新增「阶段内事件计时」区：对最耗时阶段展开内部事件（自审 / 交叉审查 / 修复）的起止与耗时
- 自动标注最耗时阶段（耗时占比 > 40% 或子代理轮次超阈值时展开事件计时）
- 归档时将计时摘要回流至 `docs/skill-suggestion.md`，形成跨变更的趋势数据

## Capabilities

### New Capabilities

- `signed-checklist-verification`: 签署清单自证与打假验证机制——定义 4 维度签署清单的结构（维度 / 自证结论 / 证据锚点）、主 Agent 写作时自证义务、验证子代理的先独立遍历后打假的执行契约、签署不成立的判定口径，以及单轮验证的终止与流转规则
- `phase-time-telemetry`: 阶段耗时与轮次遥测——定义 `.status.md` 阶段耗时统计区与阶段内事件计时区的字段结构、最耗时阶段的自动标注触发阈值，以及归档时计时摘要回流 `docs/skill-suggestion.md` 的格式与义务
- `prototype-single-round-verify`: 原型 VERIFY 单轮合并验证——定义导航合理性、Playwright 全覆盖与 UX 规则三项验证合并为单轮单报告的执行方式、合并报告的分区结构与全量遍历证明要求、对比度静态计算、审查范围冻结与范围外观察、Playwright 不可用降级

### Modified Capabilities

- `convergence-driven-repetition`: 终止模型由「见证轮为唯一成功终止条件、无轮数上限」改为「单轮验证、固定一轮」；删除见证轮四判据、不收敛判定、累积未复核修复清单；保留审查范围冻结与范围外观察在单轮下的适用形态
- `change-tier-classification`: 删除「产品需求 → 完整档」硬映射，改为统一按影响范围分数定档；kflow-explore 初判规则同步调整
- `devflow-audit`: 四维度加权评分改为记账员四项职责（门控校验 / 计时汇总 / 覆盖率校验 / 阻塞级兜底）；审计报告模板由评分表改为记账记录
- `agent-iteration-execution`: 执行类阶段的收敛驱动迭代在测试三阶段改为单轮执行 + 定向重验；主 Agent 验收从「最近一轮为见证轮」改为「单轮执行报告完整 + 定向重验通过」；编码与代码审查的重复制保留
- `subagent-self-review`: 子代理自审由「串行执行至收敛」改为单轮验证；「边审边修」改为「只报告不修改产物」；自审报告由每轮一份改为固定一份
- `plan-self-review`: kflow-plan 的收敛驱动自审改为单轮验证模型，4 个定制维度保留
- `flexible-repetition-mode`: 验证门控由「按收敛终止对齐」改为「按单轮验证 + 定向重验对齐」；受影响项 100% 覆盖与产物完整性门控保留
- `phase-self-review`: 自审规则仍位于各设计阶段 Skill 自身的 `references/self-review.md`；补充签署清单模板位于各阶段产物模板的存放规则
- `round-counter`: `执行轮次` 字段语义由「收敛实际发生的轮次」改为「单轮执行为 1 或定向重验后累计轮次」；删除「最近一轮为见证轮」的验收判据
- `inter-round-summary`: 适用范围由「全部多轮审查机制」收窄为「保留重复制的执行类阶段（编码、代码审查、缺陷修复）」；设计类自审、计划阶段与测试三阶段不再适用；删除累积未复核修复清单字段
- `prototype-navigation-verification`: 导航合理性验证的收敛驱动循环移除，5 项检查项迁移至 `prototype-single-round-verify` 的合并报告环节
- `prototype-playwright-5round-verification`: Playwright 验证的收敛驱动循环与 5 项检查项迁移至 `prototype-single-round-verify` 的合并报告环节；playwright 运行时隔离 Requirement 保留
- `prototype-review-artifacts`: 审查产物路径由 `nav-check/`、`playwright-check/`、`ux-check/`、`contrast-check/` 四个轮次目录改为单一合并报告 `verify-report.md`

## Impact

### 规范文档（`docs/designs/`）

- `core-mechanisms/03-status-and-tasks.md`（档位判定 §3.1.1、状态文件字段）
- `core-mechanisms/07-agent-model.md` §16 自审机制、§15 子代理执行模型
- `skills/kflow-{explore,design,prototype-design,plan,audit}.md`
- `skills/kflow-{api-test,e2e-test,integration-test}.md`
- `examples/change-status.md`

### 可运行 Skills（`skills/`）

- `kflow-explore/references/self-review.md`、`kflow-design/references/self-review.md`、`kflow-prototype-design/references/self-review.md`（全量重写，v2.0.0 → v3.0.0）
- `kflow-plan/references/repetition.md`（SELFREV 部分改写）
- `kflow-{api-test,e2e-test,integration-test}/references/repetition.md`（循环改单轮）
- `kflow-{explore,design,prototype-design,plan,audit}/SKILL.md`（流程框图与阶段章节）
- `kflow-{explore,design}/SKILL.md`（档位判定步骤）

### 模板（`docs/designs/templates/`）

- `changes/{change}/functional-designs/part-NN.md`、`detailed-design.md`、`api-tests/part-NN.md`、`e2e-tests/part-NN.md`（追加签署清单区）
- `changes/{change}/change-status.md`（新增耗时统计区与事件计时区）
- `changes/{change}/audit-report.md`（评分表改为记账记录）
- `subchanges/{subchange}/subchange-tasks.md`（追加签署清单区）

### 兼容性

- **BREAKING**：历史变更遗留的 `.status.md` 终止结果字段取值 `收敛` / `未收敛` 需按读取侧归并规则处理（`收敛` 读作 `验证通过`，其余读作 `验证发现问题`）；`self-reviews/{phase}/` 下多份时间戳报告的历史变更不做迁移，读取侧按「至少一份存在」判定
- **BREAKING**：历史变更 `.status.md` 不含量化档位字段时仍按 `完整` 档处理的既有兼容规则不变

### 不在本次范围

- 缺陷修复快车道（kflow-bug-triage L4 路由 + kflow-bug-fix 精简状态文件）作为后续独立变更交付，复用本次确立的单轮验证规范
- 代码审查「闭环重审」（高严重度双视角重审 / 中严重度原视角重审 / 低严重度抽查）不在本次调整范围；待本次计时遥测积累数据后据实评估
