# 任务清单

> **变更名称**: split-api-e2e-test-and-fix-archive

---

## 阶段 1：新增 kflow-api-test 设计规格

- [x] 1.1 创建 `docs/designs/skills/kflow-api-test.md`
  - 基本信息（name/description/triggers/allowed-tools）
  - 门控检查（前置：代码审查通过、api-tests/ 存在）
  - 项目类型判断（所有项目必须执行）
  - 输入要求（api-tests/、service-guide.md）
  - 输出产物（api/round-{n}.md、api/summary.md）
  - 执行流程（curl/HTTP 测试 + 健康评分）
  - Agent 迭代执行模式（10 轮下限、复杂度评估）
  - 与其他 Skill 的关系

## 阶段 2：修改 kflow-e2e-test 设计规格

- [x] 2.1 更新 `docs/designs/skills/kflow-e2e-test.md`
  - 移除 API 测试相关职责描述
  - 更新 name/description 仅反映 E2E 职责
  - 移除 API 测试产物（api/round-{n}.md、api/summary.md）
  - 更新门控检查（增加前置接口测试完成）
  - 更新与其他 Skill 的关系

## 阶段 3：修复 kflow-archive 归档条件

- [x] 3.1 修复 `docs/designs/skills/kflow-archive.md` 第 37 行：补充"代码审查"
- [x] 3.2 修复 `docs/designs/skills/kflow-archive.md` 第 172 行：补充"代码审查"

## 阶段 4：更新核心机制文档

- [x] 4.1 更新 `core-mechanisms.md` §6.1 前后端流程图（新增 kflow-api-test 节点）
- [x] 4.2 更新 `core-mechanisms.md` §6.1 纯后端流程图（新增 kflow-api-test 节点）
- [x] 4.3 更新 `core-mechanisms.md` §3.4 门控规则（拆分接口测试 + E2E 测试门控）
- [x] 4.4 更新 `core-mechanisms.md` §12.3 调度映射表（拆分两行）
- [x] 4.5 更新 `core-mechanisms.md` §15 执行类阶段列表（新增 kflow-api-test）

## 阶段 5：更新索引文件

- [x] 5.1 更新 `docs/designs/index.md`（新增 kflow-api-test 行，更新 kflow-e2e-test 描述）
- [x] 5.2 更新 `docs/designs/overview.md`（Skills 表、依赖图、实施顺序）
- [x] 5.3 更新 `docs/designs/skills/index.md`（Skills 清单、触发时机、依赖图、流转图）

## 阶段 6：更新关联 Skill 引用

- [x] 6.1 更新 `kflow-guide.md`（流程概览表、关键词映射）
- [x] 6.2 更新 `kflow-resume.md`（调度映射表拆分）
- [x] 6.3 更新 `kflow-code.md`（后续阶段链）
- [x] 6.4 更新 `kflow-code-review.md`（输出给引用）
- [x] 6.5 更新 `kflow-bug-fix.md`（输入来自引用）
- [x] 6.6 更新 `kflow-integration-test.md`（输入来自引用）
- [x] 6.7 更新 `kflow-audit.md`（回退路由）
- [x] 6.8 更新 `kflow-init.md`（工具推荐矩阵）

## 阶段 7：更新模板索引

- [x] 7.1 更新 `templates/index.md`（API 测试模板产出 Skill 归属）

## 阶段 8：一致性验证

- [x] 8.1 全局搜索 `kflow-e2e-test` 引用，确认所有引用点已更新
- [x] 8.2 全局搜索 `接口单元测试` 与 Skill 映射一致性
- [x] 8.3 验证纯后端项目流程闭环（kflow-api-test 覆盖所有项目类型）
- [x] 8.4 验证归档条件三文档一致性（kflow-archive.md、core-mechanisms.md、kflow-guide.md）

## 阶段 9：Skill 实现同步

- [x] 9.1 新建 `.claude/skills/kflow-api-test/SKILL.md`
- [x] 9.2 更新 `.claude/skills/kflow-e2e-test/SKILL.md`（移除 API 测试职责）
