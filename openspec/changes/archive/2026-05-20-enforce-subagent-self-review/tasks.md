## 1. Spec 层更新

- [x] 1.1 更新 `openspec/specs/phase-self-review/spec.md`：执行方式 Agent→子代理、design 分工制→重复制、新增串行约束、删除轮次分配
- [x] 1.2 将 `specs/subagent-self-review/spec.md` 合并到 `openspec/specs/subagent-self-review/spec.md`（新建上线）

## 2. 核心机制文档更新

- [x] 2.1 修改 `docs/designs/core-mechanisms.md` §16.4：自审执行方式从"当前阶段 Agent 自己执行"改为"子代理串行执行" + 更新"与自审机制的区别"表（SELFREV vs VERIFY 区分维度从执行者转为目的+范围）
- [x] 2.2 修改 `docs/designs/core-mechanisms.md` §15：设计类阶段自审环节从"主 Agent 直连"改为允许子代理执行
- [x] 2.3 修改 `docs/designs/core-mechanisms.md` §16.3：design 阶段自审模式从"分工制"改为"重复制"

## 3. kflow-explore Skill 改造

- [x] 3.1 修改 `.claude/skills/kflow-explore/SKILL.md` §10 SELFREV：自审执行改为子代理调用模式（启动 Agent subagent → 读取报告 → 修复 → 下一轮）
- [x] 3.2 修改 `.claude/skills/kflow-explore/references/self-review-dimensions.md`：自审执行流程加入子代理调用说明、边审边修说明

## 4. kflow-prototype-design Skill 改造

- [x] 4.1 修改 `.claude/skills/kflow-prototype-design/SKILL.md` §7 SELFREV：自审执行改为子代理调用模式，与 VERIFY 子代理模式对齐但审查范围不同

## 5. kflow-design Skill 改造

- [x] 5.1 修改 `.claude/skills/kflow-design/SKILL.md` §9 SELFREV：自审模式从分工制改为重复制 + 执行方式改为子代理调用
- [x] 5.2 修改 `.claude/skills/kflow-design/references/self-review.md`：删除轮次分配表，改为重复制说明 + 子代理执行说明

## 6. 交叉验证

- [x] 6.1 确认三阶段 SKILL.md 的 SELFREV 步骤描述一致（执行方式、审查模式、串行约束）
- [x] 6.2 确认 spec 层（phase-self-review + subagent-self-review）与 SKILL.md 实现无矛盾
