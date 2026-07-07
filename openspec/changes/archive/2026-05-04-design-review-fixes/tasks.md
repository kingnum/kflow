# 设计评审修正：实现任务清单

## 1. 文件命名一致性修复

- [x] 1.1 修复 `docs/designs/skills/kflow-code.md` 中 `functional-detailed-design.md` 笔误 → `functional-design.md`
- [x] 1.2 修复 `docs/designs/examples/change-status.md` 中 2 处 `functional-detailed-design.md` 笔误
- [x] 1.3 修复 `docs/designs/examples/rollback-status.md` 中 2 处 `functional-detailed-design.md` 笔误
- [x] 1.4 修复 `docs/designs/skills/index.md` 中 `design.md` → `detailed-design.md`（2 处）
- [x] 1.5 修复 `docs/designs/skills/kflow-plan.md` 中 `design.md` → `detailed-design.md`（4 处）
- [x] 1.6 修复 `docs/designs/skills/kflow-e2e-qa.md` 中 `design.md` → `detailed-design.md`（2 处）

## 2. 新增 Skill 设计文档

- [x] 2.1 创建 `docs/designs/skills/kflow-integration-test.md` — 集成测试 Skill 完整设计（执行流程 + 四分法修复循环 + 架构评估自动触发）
- [x] 2.2 创建 `docs/designs/skills/kflow-code-review.md` — 代码审查 Skill 完整设计（两视角并行审查 + 闭环验证）

## 3. 现有 Skill 设计文档修改

- [x] 3.1 修改 `docs/designs/skills/kflow-code.md`：移除代码审查子阶段（整个 `### 代码审查子阶段` 章节），在流程图中标注审查后跳过代码审查，改为进入 `kflow-code-review`
- [x] 3.2 修改 `docs/designs/skills/kflow-code.md`：增加多 Agent 并行编码收敛说明（变更级同步收敛 + 共享文件冲突预防）
- [x] 3.3 修改 `docs/designs/skills/kflow-code.md`：版本号更新至 1.6.0，更新与其他 Skill 关系
- [x] 3.4 修改 `docs/designs/skills/kflow-bug-fix.md`：移除变更级四分法全部内容（上下文检测、变更级执行流程、四分法分类标准）
- [x] 3.5 修改 `docs/designs/skills/kflow-bug-fix.md`：保留并简化子变更级三分法，版本号更新至 1.6.0
- [x] 3.6 修改 `docs/designs/skills/kflow-design.md`：版本号更新，文件命名引用确认正确
- [x] 3.7 修改 `docs/designs/skills/kflow-guide.md`：更新阶段数量（7→9 / 5→7），增加意图识别优先级规则
- [x] 3.8 修改 `docs/designs/skills/kflow-audit.md`：效率基准值增加"可按项目配置覆盖"说明
- [x] 3.9 修改 `docs/designs/skills/kflow-prototype-design.md`：版本号 1.3.0 → 1.6.0（内容无变化，同步版本）

## 4. 核心运行机制文档更新

- [x] 4.1 修改 `docs/designs/core-mechanisms.md`：阶段数量修正（17-18行：前后端 9 阶段 / 纯后端 7 阶段）
- [x] 4.2 修改 `docs/designs/core-mechanisms.md`：checkpoint 目录结构改为两级（变更级 + 子变更级），增加过期清理规则
- [x] 4.3 修改 `docs/designs/core-mechanisms.md`：编码→测试门控增加变更级服务刷新同步点（Step 0）
- [x] 4.4 修改 `docs/designs/core-mechanisms.md`：集成测试门控更新为指向 `kflow-integration-test` Skill
- [x] 4.5 修改 `docs/designs/core-mechanisms.md`：设计合并冲突裁决增加结构性冲突判定标准
- [x] 4.6 修改 `docs/designs/core-mechanisms.md`：子变更文件数描述修正（移除"2文件"的不准确描述）
- [x] 4.7 修改 `docs/designs/core-mechanisms.md`：版本号更新至 1.6.0

## 5. 索引入口与总览文档更新

- [x] 5.1 修改 `docs/designs/index.md`：Skill 清单新增 `kflow-integration-test` 和 `kflow-code-review`（含触发时机）
- [x] 5.2 修改 `docs/designs/index.md`：更新 `kflow-code` 和 `kflow-bug-fix` 的核心功能描述
- [x] 5.3 修改 `docs/designs/index.md`：核心设计决策表新增变更级服务刷新、两级 checkpoint、架构评估自动触发
- [x] 5.4 修改 `docs/designs/overview.md`：阶段数量修正（53-54行），Skill 清单更新
- [x] 5.5 修改 `docs/designs/overview.md`：实施计划增加 `kflow-integration-test` 和 `kflow-code-review`
- [x] 5.6 修改 `docs/designs/skills/index.md`：Skill 清单新增 2 个 Skill，触发时机总览新增对应行
- [x] 5.7 修改 `docs/designs/skills/index.md`：阶段依赖关系图更新（插入 code-review、integration-test）

## 6. 示例文档更新

- [x] 6.1 修改 `docs/designs/examples/change-status.md`：文件命名修正 + 新增服务刷新状态行
- [x] 6.2 修改 `docs/designs/examples/rollback-status.md`：文件命名修正
- [x] 6.3 新建 `docs/designs/examples/code-review-report.md`：独立代码审查报告示例
- [x] 6.4 新建 `docs/designs/examples/arch-assessment.md`：架构评估报告示例
- [x] 6.5 修改 `docs/designs/examples/index.md`：新增示例条目

## 7. 最终验证

- [x] 7.1 全局搜索验证：`functional-detailed-design.md` 无残留引用
- [x] 7.2 全局搜索验证：独立出现的 `design.md` 无残留（排除 `detailed-design.md` 和 `functional-design.md`）
- [x] 7.3 所有版本号一致性检查（设计文档全部为 1.6.0）
- [x] 7.4 阶段数量一致性检查（全文无明显 7+1/5+1 残留）
- [x] 7.5 Skill 交叉引用完整性检查（每个 Skill 的"与其他 Skill 的关系"章节）
