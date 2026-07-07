## 1. 核心机制文档更新

- [x] 1.1 更新 `04-gates-and-transitions.md`：回退触发来源从 4 种扩展为 6 种（新增编码发现原型交互流程问题 → prototype-design、编码发现功能设计需调整 → explore/design）；回退目标增加 prototype-design；新增「编码阶段发现上游问题的标准化决策流程」；阶段流转规则增加「Archive 禁止自动流转」规则
- [x] 1.2 更新 `03-status-and-tasks.md`：回退门控规则新增回退到 prototype-design 的场景；回退完成时规则新增原型修订后的后续流程；新增「暂缓功能点（⏸️）」状态值
- [x] 1.3 更新 `08-governance.md`：越界处理场景表中新增「code 发现原型交互/视觉问题 → prototype-design 回退」「code 发现功能设计问题 → explore/design 回退」两项；新增前端子变更的阶段边界约束（与后端子变更的共享文件隔离）

## 2. 设计文档更新

- [x] 2.1 更新 `kflow-plan.md` 设计文档：§任务细化规则 新增后端 FP / 前端 FP 区分，前端 FP 使用「原型转译」任务模板（输入源 + 5 步实现步骤）；§子变更任务清单格式 新增前端子变更的任务结构示例；§HITL 子变更决策点标注 新增前端子变更的依赖标注规则（依赖 API 契约而非后端实现）
- [x] 2.2 更新 `kflow-code.md` 设计文档：§执行流程 新增「前端子变更专属子流程」（工程骨架 → 逐页转译 → API 对接 → 状态覆盖）；§3.5 PROTO_CONSTRAINTS 升级为 §前端实现子流程，原型产物从提示性约束升级为执行输入；§多 Agent 并行编码策略 新增前端子变更独立并行策略；§共享文件冲突预防 新增前后端子变更间的文件隔离规则
- [x] 2.3 更新 `kflow-archive.md` 设计文档：§门控检查 新增「用户显式确认进入归档」硬门控（审计通过后 AskUserQuestion）；§执行流程 标注 Archive 为唯一禁止自动流转的阶段
- [x] 2.4 更新 `kflow-prototype-design.md` 设计文档：§R REVISION 模式 新增「code 阶段驱动回退」入口场景（编码阶段发现原型问题 → 进入 REVISION 模式的处理流程）；§越界处理 更新场景描述

## 3. 运行时 SKILL.md 同步

- [x] 3.1 使用 `/skill-creator` 更新 `kflow-plan` SKILL.md：设计文档 → SKILL.md 同步——区分后端 FP / 前端 FP 任务模板，前端 FP 归属独立子变更，前端子变更依赖 API 契约
- [x] 3.2 使用 `/skill-creator` 更新 `kflow-code` SKILL.md：设计文档 → SKILL.md 同步——新增前端实现子流程（工程骨架 → 逐页转译 → API 对接 → 状态覆盖），原型产物作为执行输入
- [x] 3.3 使用 `/skill-creator` 更新 `kflow-archive` SKILL.md：设计文档 → SKILL.md 同步——禁止自动进入，MUST 用户显式确认，审计通过后 AskUserQuestion
- [x] 3.4 使用 `/skill-creator` 更新 `kflow-prototype-design` SKILL.md：设计文档 → SKILL.md 同步——REVISION 模式增加 code 阶段驱动回退入口

## 4. 模板文件更新

- [x] 4.1 更新 `docs/designs/templates/subchanges/{subchange}/subchange-tasks.md`：新增前端 FP 任务模板区块（输入源 + 5 步实现步骤）

## 5. 验证

- [x] 5.1 使用 `kflow-skills-auditor` 审查所有更新的运行时 Skill（kflow-plan、kflow-code、kflow-archive、kflow-prototype-design）
- [x] 5.2 检查所有更新的设计文档无 TODO/TBD/{待填写} 等占位符
- [x] 5.3 检查 skill-suggestion.md 中是否有与本变更相关的历史建议需要关联处理
