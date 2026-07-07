## 1. 核心机制文档：.status.md 表格扩展

- [x] 1.1 在 core-mechanisms.md 的 3.1 变更级状态文件格式中，于「审查记录」后增加「关键决策记录」表格模板（7 列：序号/决策点/候选方案/选择/理由/决策时间/决策阶段）
- [x] 1.2 在 core-mechanisms.md 的 4.1 任务清单格式中，于「执行记录」前增加「错误日志」表格模板（8 列：序号/时间/阶段/子变更/错误描述/尝试次数/解决方案/状态），替代原有简单阻碍记录

## 2. 核心机制文档：缺陷修复循环增加上限

- [x] 2.1 在 core-mechanisms.md 的 6.2 子变更级缺陷修复循环中增加「修复尝试上限」规则：同一失败 ≤ 3 次自动尝试，第 3 次失败后 AskUserQuestion 升级用户
- [x] 2.2 在 core-mechanisms.md 的 6.2 中增加尝试计数规则说明：不同测试用例独立计数、根因变更重置计数

## 3. kflow-bug-fix 设计文档更新

- [x] 3.1 在 docs/designs/skills/kflow-bug-fix.md 中增加「修复尝试上限」规则章节，描述 3 次尝试的递进策略（直接修复 → 替代方案 → 重新思考 → 升级用户）
- [x] 3.2 更新 kflow-bug-fix.md 的缺陷修复循环流程图，增加尝试次数判断分支

## 4. kflow-explore 设计文档更新

- [x] 4.1 在 docs/designs/skills/kflow-explore.md 中增加「两动作规则」行为准则：每 2 次信息收集操作后将发现写入产出文件
- [x] 4.2 明确两动作规则的适用范围（WebFetch/WebSearch/Read外部资源/图片/PDF）和不适用范围（项目内源代码读取不计数）

## 5. kflow-resume 设计文档更新

- [x] 5.1 在 docs/designs/skills/kflow-resume.md 的 SUMMARIZE 步骤中增加「五问题快速摘要」输出格式
- [x] 5.2 定义摘要的 5 个字段：当前位置、剩余路径、变更目标、设计依据、已完成

## 6. openspec 规格文档同步

- [x] 6.1 将 changes 目录下的 defect-root-cause delta spec（三次尝试上限场景）合并到 openspec/specs/defect-root-cause/spec.md
- [x] 6.2 将 changes 目录下的 two-level-checkpoint delta spec（五问题摘要场景）合并到 openspec/specs/two-level-checkpoint/spec.md
- [x] 6.3 将新的 defect-strike-limit spec 归档到 openspec/specs/defect-strike-limit/
- [x] 6.4 将新的 explore-two-action-rule spec 归档到 openspec/specs/explore-two-action-rule/
- [x] 6.5 将新的 status-decision-error-tracking spec 归档到 openspec/specs/status-decision-error-tracking/
- [x] 6.6 将新的 resume-five-question-summary spec 归档到 openspec/specs/resume-five-question-summary/
