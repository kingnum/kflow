# Proposal: 子变更类型严格二分执行机制

## Why

子变更类型严格二分（后端/前端、禁止混合）的规则已在 `04-gates-and-transitions.md §5.3` 中定义，但仅作为声明性规则存在，从 explore 到 verify 的整条链路中缺少配套的执行机制。实际使用中出现混合子变更，导致编码流程选择错误、门控检查混乱、测试策略不匹配等问题频发。需要在 FP 源头 → 划分校验 → 共享归属 → 事后检测 → 审查兜底五个层面建立完整的执行闭环。

## What Changes

- **FP 类型标记**：explore 阶段功能点清单增加 `类型` 列（后端/前端），无法归类的 FP 强制进一步拆分。**BREAKING**：`functional-designs/index.md` 模板字段变更，旧版本功能设计文档缺少类型列将被 verify D2 标记为警告。
- **子变更划分自动校验**：design 阶段 DIVIDE 步骤输出前增加类型一致性校验——同一子变更包含的 FP 类型必须全部一致，混合则阻塞并提示拆分。**BREAKING**：现有已划分的混合子变更将在下次 design 修订时被拦截。
- **共享关切归属规则**：明确错误码、配置项、共享 DTO、Schema 变更等跨层关切的归属规则，消除"不知道该归哪个子变更"的灰色地带。
- **verify 输出越界检查**：D3 维度新增 D3.2 输出越界检查——后端SC grep 前端组件文件/硬编码样式，前端SC grep 数据库脚本/ORM 模型/服务端路由。
- **code-review 跨层越界检测**：后端SC 审查增加前端代码泄露检测，前端SC 审查增加后端逻辑泄露检测。

## Capabilities

### New Capabilities

- `fp-type-classification`: explore 阶段 FP 拆分时标记每个功能点的类型（后端/前端），无法归类的 FP 判定为粒度过粗并强制继续拆分。
- `subchange-type-validation`: design 阶段子变更划分完成后自动校验类型一致性——同一子变更内所有 FP 的类型必须相同，混合则阻塞流程并提示拆分。
- `shared-concern-ownership`: 明确跨层共享关切（错误码/配置项/共享 DTO/Schema 变更影响前端的追踪）的默认归属规则和跨子变更引用格式。
- `cross-tier-violation-detection`: verify 阶段和 code-review 阶段对子变更源码进行跨层越界检测——后端SC 检测前端代码特征，前端SC 检测后端代码特征。

### Modified Capabilities

- `functional-design-content`: FP 清单模板增加「类型」列，每个 FP 在 explore 阶段即标记为后端或前端。
- `subchange-input-source`: 输入源检查逻辑从「按子变更类型判断」调整为「按 FP 类型列表判断」，校验依据从子变更标签变为 FP 类型标记。
- `phase-artifact-verification`: D3 维度从单一的输入源检查扩展为 D3.1 输入源检查 + D3.2 输出越界检查。
- `prototype-to-code-consistency`: 跨层越界检测纳入代码审查阶段，后端SC 增加前端代码泄露检测规则。
- `frontend-implementation-subchange`: 前端子变更编码子流程增加输入前校验——确认子变更内无后端 FP 混入。

## Impact

- **5 个阶段 Skill**：`kflow-explore`（FP 类型标记）、`kflow-design`（DIVIDE 自动校验 + 共享归属指引）、`kflow-plan`（按 FP 类型生成任务）、`kflow-verify`（D3.2 越界检查）、`kflow-code-review`（跨层越界检测）
- **2 个核心机制文档**：`04-gates-and-transitions.md`（补充共享关切归属规则）、`03-status-and-tasks.md`（子变更类型列与 FP 类型列对齐）
- **3 个模板文件**：`functional-designs/index.md`（FP 清单加类型列）、`functional-designs/part-NN.md`（同上）、`subchange-tasks.md`（子变更信息中 FP 类型一致性声明）
- **相关 specs**：新建 4 个 + 修改 5 个
