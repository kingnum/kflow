## 1. 核心机制文档更新——轮次计数器 (§3.1, §3.2)

- [x] 1.1 core-mechanisms.md §3.1 变更级 .status.md 模板 `## 基本信息` 区增加 `**执行轮次**: {N} / 10` 字段
- [x] 1.2 core-mechanisms.md §3.2 子变更级 .status.md 模板 `## 基本信息` 区增加 `**执行轮次**: {N} / 10` 字段
- [x] 1.3 core-mechanisms.md §3.2 模板更新——阶段状态表中备注列示例更新（如"第1轮执行中" → "第3/10轮"）

## 2. 核心机制文档更新——Agent 迭代流程 (§15)

- [x] 2.1 §15.3 Agent 迭代执行流程图增加步骤 1.5（INIT：主 Agent 写入执行轮次 1/10）和步骤 5 ACCEPT 增加轮次检查
- [x] 2.2 §15.6 Agent 完成判断增加"满10轮"条件——Agent 须在第10轮完成后才可返回验收报告
- [x] 2.3 §15.7 主 Agent 验收标准表增加轮次检查行：检查 .status.md 执行轮次 = 10/10
- [x] 2.4 §15.9 Agent prompt 规范表增加轮次迭代指令行：「每完成一轮，更新执行轮次计数器，满10轮后返回」
- [x] 2.5 §15.4 复杂度评估机制的节奏指引更新——低/中/高复杂度对应不同的轮次阶段分布（重点执行→细节优化→验证边界），但不改变10轮下限

## 3. 核心机制文档更新——缺陷修复与10轮层级 (§6.2)

- [x] 3.1 §6.2 缺陷修复尝试上限章节增加与10轮迭代的层级关系说明（上限约束单用例修复次数/下限约束整体轮次，独立共存）

## 4. 示例文件同步

- [x] 4.1 docs/designs/examples/change-status.md 变更级 .status.md 示例 `## 基本信息` 区增加 `**执行轮次**: 3 / 10`
- [x] 4.2 docs/designs/examples/subchange-status.md 子变更级 .status.md 示例 `## 基本信息` 区增加 `**执行轮次**: 3 / 10`

## 5. 执行类 Skill 设计文档更新——prompt 模板增加轮次指令

- [x] 5.1 kflow-plan.md 设计文档——Agent prompt 模板增加轮次迭代指令和计数器写入指令
- [x] 5.2 kflow-code.md 设计文档——Agent prompt 模板增加轮次迭代指令和 TDD 10轮循环要求
- [x] 5.3 kflow-code-review.md 设计文档——Agent prompt 模板增加轮次迭代指令（多轮审查后返回）
- [x] 5.4 kflow-e2e-test.md 设计文档——Agent prompt 模板增加轮次迭代指令
- [x] 5.5 kflow-integration-test.md 设计文档——Agent prompt 模板增加轮次迭代指令
- [x] 5.6 kflow-bug-fix.md 设计文档——Agent prompt 模板增加轮次迭代指令，并澄清3次修复上限与10轮迭代的层级关系

## 6. 版本记录

- [x] 6.1 core-mechanisms.md 文件头版本号升级并记录本次变更
