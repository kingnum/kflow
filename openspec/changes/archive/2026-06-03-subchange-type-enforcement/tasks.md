# 子变更类型严格二分执行机制 — 任务清单

## 1. FP 类型标记（explore 阶段）

- [x] 1.1 更新 `docs/designs/templates/changes/{change}/functional-designs/index.md` 模板——FP 清单增加「类型」列（位于「简述」和「优先级」之间），统计信息增加后端/前端 FP 数量
- [x] 1.2 更新 `docs/designs/templates/changes/{change}/functional-designs/part-NN.md` 模板——每个功能点增加类型字段
- [x] 1.3 更新 `docs/designs/skills/kflow-explore.md` 设计文档——SPLIT 步骤增加 FP 类型判定规则（后端 FP / 前端 FP 判定标准）、无法归类则强制拆分规则、拆分后关联标注规则
- [x] 1.4 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md`——子变更类型列与 FP 类型列对齐说明
- [x] 1.5 更新 `.claude/skills/kflow-explore/SKILL.md` 运行时 Skill——SPLIT 步骤增加类型标记执行逻辑（设计文档 → SKILL.md 同步）

## 2. 共享关切归属规则（design 阶段 + 核心机制文档）

- [x] 2.1 更新 `docs/designs/core-mechanisms/04-gates-and-transitions.md` §5.3——补充共享关切归属规则表（错误码→后端/错误码提示→前端/配置项→后端/共享 DTO→变更级/Schema 变更→后端/Schema→UI 影响链→关联标注）
- [x] 2.2 更新 `docs/designs/templates/changes/{change}/detailed-design.md` 模板——子变更划分结果表「类型」列改为系统自动推断，「功能点数」列区分后端/前端数量
- [x] 2.3 新增 `docs/designs/templates/changes/{change}/shared-types/README.md` 模板——共享类型目录说明和格式规范
- [x] 2.4 新增 `openspec/specs/shared-type-directory/spec.md`——shared-types/ 目录创建、更新、引用规范

## 3. 子变更类型自动校验（design 阶段）

- [x] 3.1 更新 `docs/designs/skills/kflow-design.md` 设计文档——DIVIDE 步骤增加类型一致性自动校验逻辑（读取 FP 类型→全部一致通过/不一致阻塞）、旧版文档兼容（缺少类型列时警告）
- [x] 3.2 更新 `.claude/skills/kflow-design/SKILL.md` 运行时 Skill——DIVIDE 步骤增加自动校验执行流程（设计文档 → SKILL.md 同步）

## 4. plan 阶段 FP 类型前置校验

- [x] 4.1 更新 `docs/designs/skills/kflow-plan.md` 设计文档——步骤 3 READ 后增加 FP 类型校验逻辑（后端SC 含前端FP → 警告/前端SC 含后端FP → 警告）
- [x] 4.2 更新 `docs/designs/templates/subchanges/{subchange}/subchange-tasks.md` 模板——子变更信息增加「FP 类型一致性」字段
- [x] 4.3 更新 `.claude/skills/kflow-plan/SKILL.md` 运行时 Skill——增加 FP 类型前置校验步骤（设计文档 → SKILL.md 同步）

## 5. code 阶段 FP 类型校验与跳过

- [x] 5.1 更新 `docs/designs/skills/kflow-code.md` 设计文档——步骤 4 编码执行前增加 FP 类型二次校验（前端SC 含后端FP → 跳过该FP/后端SC 含前端FP → 跳过该FP）
- [x] 5.2 更新 `.claude/skills/kflow-code/SKILL.md` 运行时 Skill——增加 FP 类型校验 + 跳过逻辑（设计文档 → SKILL.md 同步）

## 6. verify D3.2 输出越界检查

- [x] 6.1 更新 `docs/designs/skills/kflow-verify.md` 设计文档——D3 维度拆分为 D3.1 输入源检查 + D3.2 输出越界检查，定义 grep 检测模式（后端SC 前端文件检测 / 前端SC 后端代码检测）和误报排除规则
- [x] 6.2 更新 `.claude/skills/kflow-verify/SKILL.md` 运行时 Skill——D3 增加 D3.2 越界检测执行逻辑（设计文档 → SKILL.md 同步）

## 7. code-review 跨层越界检测

- [x] 7.1 更新 `docs/designs/skills/kflow-code-review.md` 设计文档——增加跨层越界检测步骤（在原型对账之前执行），定义后端SC 前端文件检测 / 前端SC 后端逻辑检测规则
- [x] 7.2 更新 `.claude/skills/kflow-code-review/SKILL.md` 运行时 Skill——增加跨层越界检测步骤（设计文档 → SKILL.md 同步）

## 8. 版本与文档收尾

- [x] 8.1 更新 `VERSION` 文件——版本自增（Minor：新增 FP 类型标记 + 子变更类型自动校验 + 越界检测等核心机制）
- [x] 8.2 更新 `docs/designs/index.md`——设计文档版本号和修订记录
- [x] 8.3 更新 `docs/designs/overview.md`——补充 FP 类型标记和子变更类型校验机制说明
- [x] 8.4 执行 `scripts/package-skills.sh subchange-type-enforcement` 打包
