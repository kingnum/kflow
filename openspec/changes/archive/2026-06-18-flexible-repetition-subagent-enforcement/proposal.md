## Why

当前重复制机制和子代理执行存在三个核心问题：

1. **10轮强制迭代效率低下**：kflow-bug-fix 等执行类阶段强制10轮下限，即使问题在第2轮已全部修复，仍需继续"空转"至第10轮，造成大量无效 Token 消耗。

2. **子代理执行规则未被遵守**：kflow-bug-triage 路由到 kflow-bug-fix 时，主 Agent 经常直接执行修复工作而未使用子代理。根本原因是子代理强制规则在 SKILL.md 中位置不突出，且路由时未传递执行模式上下文。

3. **阶段回退后重复制过于僵化**：用户反馈或设计修订导致阶段回退后，重新执行该阶段仍需完整10轮重复制，但实际影响范围可能只涉及1-2个功能点，造成严重的效率浪费。

## What Changes

### 1. 子代理执行规则强化
- 所有执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）SKILL.md 开头添加醒目的子代理强制规则框
- 规则明确适用所有入口场景（直接触发 + triage路由 + 其他Skill调用）
- 移除"禁止后台运行"硬规则，改为推荐使用前台模式，允许后台运行但需确保权限已配置
- 项目 settings.json 预设 kflow 所需权限，避免子代理因权限不足而降级执行

### 2. kflow-bug-triage 增强
- 诊断报告新增「影响范围评估」节：涉及功能点清单、涉及接口清单、涉及数据模型变更、影响范围分数
- 路由输出新增「执行模式声明」（EXECUTION_MODE = SUBAGENT_REQUIRED）
- 影响范围分数计算规则：功能点数×1 + 接口数×1.5 + 数据模型变更×2

### 3. 重复制机制调整（所有执行类阶段）
- **首次执行**：完整10轮重复制（保持现有行为）
- **回退重执行**：按影响范围分数决定轮次
  - 1-5分：1-3轮 + 受影响项100%验证 + 全量1轮兜底
  - 6-15分：3-5轮 + 受影响项100%验证 + 全量1轮兜底
  - >15分：完整10轮
- 验证门控强化：受影响项100%覆盖 + 全量至少1轮兜底

### 4. 状态文件新增字段
- 阶段执行历史表：执行次数、最近执行类型（首次执行/REVISION/回退重执行）、轮次、影响范围分数
- 最近修订信息：修订触发来源、修订源头阶段、内容摘要、涉及功能点/接口/数据模型变更、影响范围分数

## Capabilities

### New Capabilities

- `triage-impact-assessment`: triage 诊断时一并执行的影响范围评估能力，输出涉及功能点/接口/数据模型变更清单及影响范围分数，传递给回退目标阶段用于重复制轮次决策
- `flexible-repetition-mode`: 弹性重复制机制，根据阶段执行历史和影响范围分数动态决定重复制轮次，首次执行10轮，回退重执行按影响范围缩减，配套验证门控确保质量
- `subagent-enforcement-notice`: 子代理强制规则前置声明机制，在执行类阶段 SKILL.md 开头添加醒目规则框，明确适用所有入口场景，配套权限预配置确保子代理可正常执行

### Modified Capabilities

- `shared-repetition-model`: 新增弹性重复制轮次决策规则、阶段执行历史追踪、影响范围分数读取机制；调整验证门控以支持非严格重复制场景
- `subagent-isolation-rule`: 移除"禁止后台运行"硬规则，改为推荐使用前台模式；新增权限预配置要求
- `bug-triage-skill`: 新增影响范围评估节、执行模式声明、影响范围分数计算规则
- `execution-repetition-mode`: 新增轮次决策逻辑、验证门控调整

## Impact

### 影响的 Skill（8个）
- `.claude/skills/kflow-plan/SKILL.md`
- `.claude/skills/kflow-code/SKILL.md`
- `.claude/skills/kflow-code-review/SKILL.md`
- `.claude/skills/kflow-api-test/SKILL.md`
- `.claude/skills/kflow-e2e-test/SKILL.md`
- `.claude/skills/kflow-integration-test/SKILL.md`
- `.claude/skills/kflow-bug-fix/SKILL.md`
- `.claude/skills/kflow-bug-triage/SKILL.md`

### 影响的核心机制文档（2个）
- `.claude/skills/kflow-shared/repetition-model.md`
- `docs/designs/core-mechanisms/07-agent-model.md`

### 影响的设计文档（2个）
- `docs/designs/skills/kflow-bug-fix.md`
- `docs/designs/skills/kflow-bug-triage.md`

### 影响的模板文件
- `docs/designs/templates/changes/{change}/.status.md`（新增阶段执行历史表和最近修订信息）
- `docs/designs/templates/changes/{change}/bugs/bug-NNN-NNN.md`（新增影响范围评估节）

### 配置变更
- `.claude/settings.json`（新增 kflow 所需权限预设）

### 版本影响
- Minor 版本自增（核心机制变更）
