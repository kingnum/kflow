## Why

当前三阶段（explore/prototype/design）自审由当前阶段 Agent 自身执行，存在"作者盲点"——同一 Agent 撰写产物后自审，难以发现自身遗漏。prototype 阶段的 VERIFY 已验证"子代理串行审查"模式有效，但 SELFREV 步骤仍由主 Agent 执行，模式不统一。同时 design 阶段仍使用"分工制"（轮次分组维度），与其他两阶段的"重复制"不一致。

## What Changes

- **BREAKING**: 自审执行方式从"当前阶段 Agent 自身执行"改为"子代理（Agent subagent）串行执行"，每轮启动独立子代理，10 轮顺序执行
- 自审过程中子代理发现的问题直接修复（边审边修），不限于出报告
- **BREAKING**: design 阶段自审模式从"分工制"（Round 1-3 结构性、4-7 细节、8-10 边界）改为"重复制"（每轮全四维度独立检查），与 explore/prototype 统一
- 每个子代理审查维度、要求、范围完全一致（重复制），不允许按维度分工
- 非必要不增加新功能，仅做核心改造

## Capabilities

### New Capabilities

- `subagent-self-review`: 子代理自审执行机制——三阶段（explore/prototype/design）的 SELFREV 步骤强制使用子代理（Agent subagent）串行执行 10 轮自审，每轮子代理独立上下文、相同审查范围、边审边修。

### Modified Capabilities

- `phase-self-review`: 自审执行方式从"当前阶段 Agent 自身执行"改为"子代理串行执行"；design 阶段自审模式从"分工制"改为"重复制"（与 explore/prototype 统一）。

## Impact

- `openspec/specs/phase-self-review/spec.md` — 修改执行方式（Agent→子代理）+ design 模式（分工制→重复制）+ 新增串行/边审边修约束
- `openspec/specs/subagent-self-review/spec.md` — 新建，子代理自审执行机制规格
- `docs/designs/core-mechanisms.md` §15 + §16.3 + §16.4 — 修改子代理执行模型分类 + design 自审模式分工制→重复制 + 执行方式 Agent→子代理 + 更新"与自审机制的区别"表
- `.claude/skills/kflow-explore/SKILL.md` §10 SELFREV — 修改为子代理调用
- `.claude/skills/kflow-prototype-design/SKILL.md` §7 SELFREV — 修改为子代理调用
- `.claude/skills/kflow-design/SKILL.md` §9 SELFREV — 分工制→重复制 + 子代理调用
- `.claude/skills/kflow-design/references/self-review.md` — 删除轮次分配，改为重复制
- `.claude/skills/kflow-explore/references/self-review-dimensions.md` — 加入子代理执行说明
