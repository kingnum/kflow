## Why

当前子代理隔离规则仅存在于 `repetition-model.md` §12（共享文档），各执行类阶段 SKILL.md 中仅描述性提及"启动 Agent 迭代子代理"，缺少显式禁令。主 Agent 在上下文压力大时可能"合理化"直接接手子代理的执行工作，破坏子代理独立性保障。需要将规则从"隐式引用"升级为"双写强制"——集中（共享文档强化）+ 分散（各 SKILL.md 内联规则框），消除执行时的歧义空间。

## What Changes

- **`repetition-model.md` §12 强化**：新增主 Agent 职责硬线声明（调度+验收，SHALL NOT 执行任何阶段主工作，无例外）；细化重试粒度为轮次级（某轮子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试）；适用阶段清单补全全部 7 个执行类阶段
- **7 个执行类阶段 SKILL.md 新增「子代理强制规则」段落**：kflow-plan / kflow-code / kflow-code-review / kflow-api-test / kflow-e2e-test / kflow-integration-test / kflow-bug-fix，每个文件在执行流程前新增独立规则框，包含三条硬规则 + 引用 repetition-model.md §12
- **对应设计文档同步**：`docs/designs/skills/` 下各 Skill 设计文档 + `docs/designs/core-mechanisms/07-agent-model.md`
- **openspec specs 更新**：`subagent-isolation-rule` spec 新增轮次级重试规则和主 Agent 职责硬线；`shared-repetition-model` spec 同步更新

## Capabilities

### New Capabilities

（无新增能力）

### Modified Capabilities

- `subagent-isolation-rule`: 新增主 Agent 职责硬线声明（调度+验收，SHALL NOT 执行阶段主工作）；新增轮次级重试规则（子代理崩溃 → 新建 Agent 重跑该轮，≤3 次）；适用阶段清单扩展至全部 7 个执行类阶段 + 各 SKILL.md 内联规则框要求
- `shared-repetition-model`: §12 子代理隔离规则强化——重试粒度从"任务级"细化为"轮次级"；新增主 Agent 职责边界硬线声明

## Impact

- **共享文档**：`.claude/skills/kflow-shared/repetition-model.md` §12 修改
- **运行时 SKILL.md**（7 个文件）：kflow-plan / kflow-code / kflow-code-review / kflow-api-test / kflow-e2e-test / kflow-integration-test / kflow-bug-fix
- **设计文档**：`docs/designs/skills/` 下对应 7 个 Skill 设计文档 + `docs/designs/core-mechanisms/07-agent-model.md`
- **Specs**：`openspec/specs/subagent-isolation-rule/spec.md` + `openspec/specs/shared-repetition-model/spec.md`
- **无 API / 依赖变更**：本次为纯规则强化，不涉及功能新增或删除
