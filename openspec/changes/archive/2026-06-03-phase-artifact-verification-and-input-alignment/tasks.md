## 1. 门控规则补全 (03-status-and-tasks.md §3.4)

- [x] 1.1 plan 入口门控：增加 CONTEXT.md 存在性检查 [全部]
- [x] 1.2 plan 入口门控：增加 functional-designs/index.md 存在性检查 [全部]
- [x] 1.3 plan 入口门控：增加 api-tests/index.md 存在性检查 [全部]
- [x] 1.4 plan 入口门控：增加 e2e-tests/index.md 条件存在性检查 [前端SC + 前后端项目]
- [x] 1.5 code 入口门控：增加子变更类型判断分支逻辑
- [x] 1.6 code 入口门控：增加前端SC prototype/index.html + design-tokens.css + element-coverage-tree.md 强制检查
- [x] 1.7 code 入口门控：增加 CONTEXT.md 存在性检查 [全部]
- [x] 1.8 e2e-test 入口门控：增加 element-coverage-tree.md 存在性检查 [前端项目]
- [x] 1.9 integration-test 入口门控：增加设计产物回溯验证（functional-designs/index.md + detailed-design.md + prototype/index.html 条件）
- [x] 1.10 所有门控规则显式标注 [全部]/[后端子变更]/[前端子变更]/[前端项目]/[纯后端项目]

## 2. 子变更类型与输入源规范化

- [x] 2.1 核心机制文档 `04-gates-and-transitions.md`：新增子变更类型严格二分规则（后端SC/前端SC，禁止混合）
- [x] 2.2 核心机制文档 `03-status-and-tasks.md`：子变更进度矩阵增加「子变更类型」列
- [x] 2.3 kflow-plan 设计文档：输入要求表增加「适用SC类型」列，区分后端SC/前端SC输入源
- [x] 2.4 kflow-plan 设计文档：前端子变更 plan 输入增加 prototype/* 核心产物
- [x] 2.5 kflow-code 设计文档：输入要求表增加「适用SC类型」列，区分后端SC/前端SC输入源
- [x] 2.6 kflow-code 设计文档：前端子变更 code 输入限定为核心原型产物（排除 design-prompt.md 和 design-system/*）
- [x] 2.7 kflow-design 设计文档：子变更划分章节增加「依赖API契约」声明格式规范
- [x] 2.8 kflow-design 设计文档：前端子变更「依赖API契约」列表格式定义
- [x] 2.9 Plan 阶段 tasks.md 模板：前端子变更「输入源」区增加 API 契约引用
- [x] 2.10 设计文档模板 `traceability.md`：无需修改，确认现有格式满足需求

## 3. HITL 重新定义为设计阶段标记

- [x] 3.1 核心机制文档 `04-gates-and-transitions.md`：HITL 定义从「执行类型」改为「设计不完整标记」
- [x] 3.2 核心机制文档 `04-gates-and-transitions.md`：增加 HITL 阻塞 plan 入口的规则
- [x] 3.3 核心机制文档 `04-gates-and-transitions.md`：AFK 判定标准移除「UI/UX 方向决策」条件
- [x] 3.4 kflow-design 设计文档：子变更划分 HITL/AFK 分类章节更新语义
- [x] 3.5 kflow-design 设计文档：移除 HITL 决策点说明要求（已不需要在 code 阶段触发）
- [x] 3.6 kflow-code 设计文档：移除 HITL 子变更执行规则和决策点暂停机制

## 4. 新增 kflow-verify 独立诊断 Skill

- [x] 4.1 新增设计文档 `docs/designs/skills/kflow-verify.md`：七维度诊断体系、严重度分级、修复路由、诊断报告格式
- [x] 4.2 新增模板 `docs/designs/templates/changes/{change}/verify-report.md`：诊断报告模板
- [x] 4.3 使用 skill-creator 创建运行时 Skill `.claude/skills/kflow-verify/SKILL.md`（含 description 中英混合触发词：`诊断/验证产物/检查产物/产物完整性/输入源检查/verify`）
- [x] 4.4 kflow-guide SKILL.md：新增 kflow-verify 路由入口和触发词
- [x] 4.5 kflow-guide 设计文档：流程概览显示 kflow-verify

## 5. Phase Hooks 与 RELOAD 清单更新

- [x] 5.1 `kflow-shared/phase-hooks.md`：plan 阶段 RELOAD 增加 functional-designs/index.md、functional-designs/part-NN.md、api-tests/index.md
- [x] 5.2 `kflow-shared/phase-hooks.md`：plan 阶段 RELOAD 增加 prototype/* 核心产物（条件，前端SC）
- [x] 5.3 `kflow-shared/phase-hooks.md`：code 阶段 RELOAD 增加 CONTEXT.md
- [x] 5.4 `kflow-shared/phase-hooks.md`：code 阶段 RELOAD 增加 prototype/design-tokens.css、prototype/element-coverage-tree.md（条件，前端SC）
- [x] 5.5 `kflow-shared/phase-hooks.md`：e2e-test 阶段 RELOAD 增加 element-coverage-tree.md（条件，前端项目）

## 6. 运行时 SKILL.md 同步（设计文档 → SKILL.md 同步）

> **CLA.md 强制要求**：创建提案时，任务清单中必须包含此项——在执行 `openspec-apply-change` 阶段同步使用 `/skill-creator` 根据变更后的设计文档更新对应的运行时 Skill。

- [x] 6.1 `/skill-creator` 更新 kflow-plan SKILL.md：输入要求表增加「适用SC类型」列，前端SC 输入源增加 prototype/* 核心产物
- [x] 6.2 `/skill-creator` 更新 kflow-code SKILL.md：输入要求表增加「适用SC类型」列，前端SC 输入限定为核心原型产物，移除 HITL 执行规则
- [x] 6.3 `/skill-creator` 更新 kflow-design SKILL.md：子变更划分增加「依赖API契约」声明，HITL 语义更新
- [x] 6.4 `/skill-creator` 更新 kflow-explore SKILL.md：阶段边界约束更新（如涉及）
- [x] 6.5 `/skill-creator` 更新 kflow-guide SKILL.md：新增 kflow-verify 路由入口
- [x] 6.6 `/skill-creator` 使用 `kflow-skills-auditor` 审查所有更新后的 Skill

## 7. 验证与收尾

- [x] 7.1 对现有设计文档执行一致性检查：对照 proposal 中的 Capabilities 列表，验证所有 spec 文件已创建
- [ ] 7.2 更新 README.md 版本号与更新说明（归档后执行）
