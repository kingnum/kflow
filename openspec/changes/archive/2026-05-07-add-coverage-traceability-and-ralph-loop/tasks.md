## 1. 核心机制文档更新

- [x] 1.1 在 core-mechanisms.md 新增「十四、覆盖追溯机制」章节（traceability.md 生命周期、格式规范、覆盖率门控规则）
- [x] 1.2 在 core-mechanisms.md 新增「十五、子代理执行模型」章节（阶段分类、ralph-loop 调度、复杂度评估、验收流程）
- [x] 1.3 在 core-mechanisms.md 门控规则（§3.4）中集成覆盖率检查（各阶段门控增加 traceability.md 对应列覆盖率 = 100% 校验）
- [x] 1.4 在 core-mechanisms.md 目录结构规范（§2.1）中增加 traceability.md 文件位置
- [x] 1.5 更新 overview.md 设计决策表（新增 2 条决策：覆盖追溯矩阵、ralph-loop 子代理执行），实施计划增加相关条目

## 2. traceability.md 模板与规格

- [x] 2.1 创建 `docs/designs/templates/change/traceability.md` 模板文件（覆盖总览表 + 阶段覆盖统计 + 缺口追踪表）
- [x] 2.2 在 `docs/designs/templates/index.md` 中注册 traceability.md 模板

## 3. kflow-design 集成（traceability.md 创建）

- [x] 3.1 更新 `docs/designs/skills/kflow-design.md` — 输出产物增加 traceability.md、执行流程增加 traceability.md 创建步骤（基于 functional-designs/index.md FP 清单初始化空白矩阵）
- [x] 3.2 更新 kflow-design 门控检查：设计探索完成后自动创建 traceability.md

## 4. 执行类阶段集成 ralph-loop 子代理

- [x] 4.1 更新 `docs/designs/skills/kflow-plan.md` — 增加 ralph-loop 子代理执行模式（复杂度评估 → 子代理调度 → 验收 → traceability.md 更新）
- [x] 4.2 更新 `docs/designs/skills/kflow-code.md` — 增强 ralph-loop 集成（在现有子代理基础上增加迭代循环 + COMPLETED 承诺 + 验收）
- [x] 4.3 更新 `docs/designs/skills/kflow-code-review.md` — 增加 ralph-loop 子代理模式（复杂度评估 → 两视角审查并行 → 验收）
- [x] 4.4 更新 `docs/designs/skills/kflow-e2e-test.md` — 增强 ralph-loop 集成（测试执行 → 覆盖率验证 → COMPLETED 承诺 → 验收）
- [x] 4.5 更新 `docs/designs/skills/kflow-bug-fix.md` — 增加 ralph-loop 子代理模式（根因分析 → 修复 → 验证循环）
- [x] 4.6 更新 `docs/designs/skills/kflow-integration-test.md` — 增强 ralph-loop 集成（集成测试执行 → 四分法修复 → 覆盖率验证 → 验收）

## 5. skill-suggestion.md 扩展

- [x] 5.1 更新 `docs/designs/examples/skill-suggestion.md` — 新增 ralph-loop 验收不通过记录格式（含阶段、轮次、覆盖率缺口、改进建议字段）
- [x] 5.2 更新 core-mechanisms.md 中 skill-suggestion.md 的触发条件（增加 ralph-loop 验收失败触发）

## 6. 验证与闭合

- [x] 6.1 验证所有受影响的 Skill 文档中「与其他 Skill 的关系」和「反馈机制」章节已更新
- [x] 6.2 验证 core-mechanisms.md 门控规则与 traceability.md 覆盖率检查逻辑一致性
- [x] 6.3 使用 kflow-skills-auditor 对所有更新的 Skill 文档执行规范审查
