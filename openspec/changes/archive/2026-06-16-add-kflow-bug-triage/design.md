# Design: add-kflow-bug-triage

## Context

当前 Skills 体系的问题处理链路存在结构性缺口：

```
用户反馈问题 ──▶ ???（无结构化流程）
测试失败 ──▶ kflow-bug-fix（三分法：实现/测试/设计）
```

`kflow-bug-fix` 的三分法根因分类将所有上游问题笼统归为"设计错误"，无法区分需求定义、原型设计、详细设计三个不同层级的问题源头。这导致回退目标固定为 design 阶段，但实际问题可能源自 explore（需求）或 prototype-design（原型）阶段。

同时，`kflow-guide` 的 INTENT 关键词表将所有"问题相关"关键词（修复/Bug/缺陷/问题）统一路由到 `kflow-bug-fix`，但 bug-fix 的执行前提是存在测试失败报告——用户反馈场景下 bug-fix 无法有效执行。

现有机制参考：
- `kflow-verify`：独立诊断 Skill，七维度产物诊断，路由到 REVISION 模式。与 triage 互补——verify 检查"产物质量"，triage 诊断"问题源头"
- `kflow-code` 上游问题检测（Section 6.6）：编码阶段发现原型/功能问题时的决策流。与 triage 互补——code 的上游检测是编码过程中的即时发现，triage 是用户反馈的系统诊断
- `change-rollback` spec 已支持六种回退触发来源（缺陷修复设计错误/代码审查/需求变更/审计/编码发现原型问题/编码发现功能点问题），triage 新增第七种

## Goals / Non-Goals

**Goals:**

- 为用户反馈问题提供结构化的四层溯源诊断流程（需求→原型→设计→实现）
- 建立独立的问题登记机制（bugs/ 目录 + 索引 + 分页详情），支持问题全生命周期追踪
- 精确定位问题源头阶段，路由到正确的 REVISION 模式或调用 bug-fix 修复
- 消除 kflow-bug-triage 与 kflow-bug-fix 的业务重叠，明确职责边界
- 修改 kflow-guide 路由表，将用户反馈入口从 bug-fix 切换到 triage

**Non-Goals:**

- 不处理测试阶段自动发现的缺陷（B 路径直接进入 bug-fix）
- 不替代 `kflow-verify` 的产物诊断能力（verify 检查产物质量，triage 诊断问题源头）
- 不修改集成测试的四分法修复循环（`kflow-integration-test` 独立处理）
- 不变更阶段门控机制和状态文件结构（.status.md 的 ⚠️ 需修订 机制保持不变）
- 不新增 REVISION 模式（复用现有 explore/prototype-design/design 的 REVISION 模式）

## Decisions

### D1: 独立 Skill vs 增强 bug-fix

**决策**：创建独立的 `kflow-bug-triage` Skill。

**理由**：
- 职责清晰分离——triage 负责"诊断+登记+路由"，bug-fix 负责"复现+修复+验证"
- triage 的输入（用户自然语言描述）与 bug-fix 的输入（测试失败报告）本质不同
- 避免 bug-fix 过度膨胀（bug-fix 已有 604 行设计规格）

**替代方案**：在 bug-fix 的 DISCOVER 步骤前插入溯源步骤——被否决，因为会让 bug-fix 同时承担诊断和执行两个不同职责，违反单一职责原则。

### D2: 溯源漏斗方向——从上游到下游

**决策**：诊断顺序为 L1 需求 → L2 原型 → L3 设计 → L4 实现，从上往下逐层排除。

**理由**：
- 如果上游有问题，修改下游全是浪费。先排除上游问题避免方向性错误
- 每层有明确的判断依据和证据来源（functional-designs/prototype/detailed-design/code），可系统化执行

**替代方案**：从下游（实现层）开始往上排查——被否决，因为用户反馈的问题往往不是代码层面的，从下往上容易"头痛医头"。

### D3: bug-fix 三分法简化为二分法

**决策**：去掉 bug-fix 的"设计错误"分类和回退路由，仅保留实现错误/测试错误。

**理由**：
- 用户反馈入口已统一到 triage，triage 在调用 bug-fix 之前已确认问题在 L4 实现层
- bug-fix 不再需要判断"设计错误"——如果问题在 L1-L3，triage 会直接路由到对应 REVISION 模式，根本不会调用 bug-fix
- B 路径（测试自动发现）进入 bug-fix 时，测试失败通常明确指向实现/测试层面，不需要上游诊断

**风险**：B 路径进入 bug-fix 时如果实际问题源自设计层，bug-fix 的二分法可能误判。→ 缓解：保留 bug-fix 的"三次尝试后升级用户"机制，用户可选择触发设计回退。

### D4: 问题登记使用独立目录而非融入现有文件

**决策**：在变更目录下创建独立的 `bugs/` 目录，含 `index.md` 索引和分页详情文件（每文件≤20条）。

**理由**：
- 问题登记有独立的生命周期（登记→诊断→确认→修复→验证→关闭），与现有文件（tasks.md、.status.md）的关注点不同
- 分页设计遵循现有大文档拆分规范（参照 `functional-designs/part-NN.md` 模式）
- `index.md` 模式与现有 `functional-designs/index.md`、`api-tests/index.md` 等保持一致

**替代方案**：在 `.status.md` 新增问题追踪节——被否决，因为 .status.md 关注阶段状态，混入问题追踪会职责不清。

### D5: kflow-guide 路由切换策略

**决策**：
- 新增 triage 路由关键词：`反馈`、`报告问题`、`报bug`、`提bug` → `kflow-bug-triage`
- 修改 `修复` 关键词：增加上下文判断（有活跃 bug-fix 子阶段 → bug-fix，否则 → triage）
- bug-fix 不再通过 guide 路由（仅测试阶段自动触发）

**理由**：
- guide 是用户手动入口，用户通过 guide 表达的所有"问题相关"意图本质上都是"我要反馈一个问题"
- "修复"是唯一的特殊关键词——可能表示"继续已有修复工作"，需上下文判断

**风险**：`修复` 关键词的上下文判断增加 guide 的复杂度。→ 缓解：判断逻辑简单（检查活跃变更是否有正在执行的 bug-fix），失败时 fallback 到 AskUserQuestion。

### D6: triage 与现有 Skill 的协作方式

**决策**：
- L1-L3 路由：triage 直接修改 `.status.md` 执行阶段回退，触发对应 Skill 的 REVISION 模式
- L4 路由：triage 调用 `kflow-bug-fix` 执行修复
- triage 不执行任何修复动作（不修代码、不修测试、不修设计文档）

**理由**：
- triage 是"分诊台"角色——只诊断和路由，不执行治疗
- 复用现有 REVISION 模式（explore/prototype-design/design 已有成熟的修订流程）

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 四层溯源诊断可能过度分析简单问题（如明显是代码写错了） | 每层设置快速排除条件——如果证据明确指向某层，无需逐层详细检查。诊断报告中标注快速排除理由 |
| triage 的溯源判断可能不准确（误判源头层级） | 诊断报告展示完整的四层判断过程和证据，用户确认后才执行路由。用户可覆盖诊断结论 |
| bug-fix 简化后 B 路径可能漏判设计层问题 | 保留三次尝试升级机制作为兜底；用户可选择触发设计回退 |
| guide 的 `修复` 关键词上下文判断增加复杂度 | 判断逻辑仅一个条件（是否有活跃 bug-fix），fallback 到 AskUserQuestion |
| bugs/ 目录可能积累大量未关闭问题影响变更归档 | bugs/ 目录中的未关闭问题作为 kflow-audit 审计的输入之一；阻塞级未关闭问题阻断归档 |
