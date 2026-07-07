## Why

当前体系在原型设计和详细设计两个关键阶段完成后，仅有 AI Agent 自动审查，缺少用户（人）的最终评审确认环节。原型设计和详细设计是变更级最重要的决策阶段——原型决定了用户体验方向，详细设计决定了架构、数据模型、接口契约和子变更划分——这些决策不应由 AI 独立裁决后直接进入执行阶段。需要在 AI 审查的基础上，增加用户评审门控，确保人对关键设计决策有最终确认权。

## What Changes

- 原型设计阶段执行流程新增用户评审步骤：原型输出后，展示给用户确认，评审通过才标记阶段完成
- 详细设计阶段执行流程新增用户评审步骤：AI 四视角审查通过后，展示设计给用户最终确认，评审通过才标记阶段完成
- `.status.md` 新增「用户评审记录」表格，记录各阶段用户评审状态、时间和备注
- 门控规则新增两条：原型设计→详细设计之间增加用户评审门控（仅前后端项目且原型未跳过时）；详细设计→计划之间增加用户评审门控（所有项目类型）
- `kflow-prototype-design` Skill 文档更新执行流程和输出产物
- `kflow-design` Skill 文档更新执行流程和输出产物
- `core-mechanisms.md` 更新门控规则、状态文件格式、阶段流转图
- `overview.md` 核心设计决策表新增用户评审项

## Capabilities

### New Capabilities

- `user-review-gate`: 用户评审门控机制——在关键设计阶段（原型设计、详细设计）完成后，通过 AskUserQuestion 要求用户确认设计产出，评审结果记录在 .status.md 中，下一阶段门控检查用户评审状态

### Modified Capabilities

<!-- 本次为新增机制，不修改已有 spec 级行为 -->

## Impact

- 影响的文档：`docs/designs/core-mechanisms.md`、`docs/designs/overview.md`
- 影响的 Skill 设计：`docs/designs/skills/kflow-prototype-design.md`、`docs/designs/skills/kflow-design.md`
- 影响的 Skill 实现：`kflow-prototype-design`、`kflow-design`（`.claude/skills/` 下的对应 Skill 文件）
- 不影响纯后端项目流程（原型设计跳过时，对应门控自动跳过）
- 不影响已有变更的 .status.md 格式兼容性（新增表格为可选区块，缺少时门控提示而非阻塞）
