## Context

当前体系在编码/测试等下游阶段发现设计需调整时，通过阶段回退机制（change-rollback）将目标阶段标记为 ⚠️需修订、后续阶段重置为 ⏳待开始。但存在三个缺口：

1. **prototype/** 目录无 index.md，缺少版本管理和修订记录
2. **detailed-design.md** 仅有孤立版本号，无修订记录表
3. **回退后下游产物同步缺少逐阶段独立确认机制**——当前仅靠 RELOAD 机制"重读最新文件"，无显式的"哪个阶段已同步、哪个尚未"的追踪

本设计填补上述缺口，同时遵循关注点分离原则：设计目录 index.md 记录 WHAT（修订内容），.status.md 追踪 WHERE（同步状态）。

## Goals / Non-Goals

**Goals:**
- 三个设计目录（functional-designs/、prototype/、detailed-design/）均有 index.md，包含统一格式的"修订记录"表
- .status.md 新增"设计修订同步追踪"区，每受影响阶段独立确认同步状态
- kflow-guide 集中检测用户"XX设计需调整"意图并分流到对应设计 Skill（REVISION 模式）
- 合并 functional-designs/index.md 中现存的"需求变更记录"与"修订记录"为统一的一张表

**Non-Goals:**
- 不改变阶段回退的核心门控规则（change-rollback 已有）
- 不在各阶段 Skill 的 description 中添加其他阶段的触发词
- 不改变 traceability.md 的 FP 覆盖矩阵机制
- 不创建新的 Skill，仅在现有 Skill 中增加触发检测和路由

## Decisions

### 决策 1：设计变更记录放在设计目录 index.md，同步追踪放在 .status.md

**选择**：分离——设计目录的 index.md 记录修订历史（永久保留），.status.md 追踪传播状态（跟随执行推进）。

**理由**：index.md 是设计产物，应保持纯设计属性；同步状态是流程关注点，随阶段执行变化，应放在状态文件中。分离后，设计文档可在变更归档后直接合并到产品级文档而无需修改流程状态信息。

**替代方案**：全放在 index.md 中——被否决，因为混合了设计与流程两个关注点，归档时需剥离流程信息。

### 决策 2：统一"修订记录"表格式，合并"需求变更记录"

**选择**：三个设计目录的 index.md 使用同一张"修订记录"表（版本/日期/修订类型/修订内容/影响功能点/触发阶段），functional-designs/index.md 中原有的"八、需求变更记录"与"九、修订记录"合并。

**理由**：现有两张表高度重叠——需求变更记录是修订记录的子集。合并后减少冗余，用户只需看一张表即可了解设计文档的完整变更历史。"修订类型"列（初始版本/需求变更/接口签名/数据模型/UI布局/交互行为/架构设计/配置项/其他）区分变更性质。

### 决策 3：同步追踪表使用每阶段独立确认列

**选择**：.status.md 的"设计修订同步追踪"表中，每阶段使用独立列（plan/code/review/api-test/e2e-test/integ-test），各阶段完成后独立标记本列状态。

**理由**：单状态位方案（⏳→🔄→✅）在频繁修订时状态会丢失——修订 #2 发生后无法判断修订 #1 在各阶段的同步进度。独立列方案下，新修订产生新行，每行有独立的列状态，各行之间互不干扰。每个阶段完成后自行确认本列，"不适用"的列标记 `—`。

### 决策 4：设计修订意图由 kflow-guide 集中检测和分流

**选择**：kflow-guide 的 description 中添加"设计需调整/功能设计需调整/原型需调整/详细设计需调整/接口设计要改"等触发词，由 kflow-guide PARSE 阶段统一解析目标设计目录并路由到对应设计 Skill（REVISION 模式）。

**理由**：若各阶段 Skill 各自添加其他阶段的触发词，会导致 Claude Code 的 Skill 匹配歧义（AI 无法判断应使用哪个 Skill）。集中到 kflow-guide 后，各阶段 Skill 保持职责单一，跨阶段意图统一由 guide 分发。

**替代方案**：各阶段 Skill 自行检测并处理——被否决，会导致 description 混乱和匹配歧义。

### 决策 5：prototype/index.md 内容范围

**选择**：prototype/index.md 包含四大节——原型文件清单、页面清单、设计系统引用、修订记录。

**理由**：原型是多个文件的集合（index.html、page-*.html、design-tokens.css、design-prompt.md、style-decision.md、验证报告等），需要一个清单文件来建立整体视图。设计系统引用链接到 design-system/MASTER.md，确保原型与设计系统之间可追溯。修订记录与其他两个设计目录保持一致格式。

## Risks / Trade-offs

- **prototype/index.md 信息可能过时**：原型文件可能被直接修改而 index.md 未同步更新 → 在 prototype-design Skill 的 VERIFY 步骤中增加 index.md 与原型文件的一致性检查
- **同步追踪表列数增长**：如果未来新增阶段，需扩展追踪表的列 → 列仅包含受设计修订影响的阶段（plan 之后），新阶段加入时自然追加
- **kflow-guide 负担增加**：集中检测意味着 guide 需维护更多触发词 → 触发词按模式分组管理（DESIGN_REVISION 模式为一组），每月审查触发准确率
