# code-review-phase

## MODIFIED Requirements

### Requirement: 代码审查子阶段

系统 SHALL 提供 `kflow-code-review` 作为独立的代码审查 Skill，在编码阶段完成后作为独立阶段执行。

#### Scenario: 代码审查执行时机
- **WHEN** 子变更所有功能点的 TDD 循环完成（全 Green + 已提交）
- **THEN** 系统进入 `kflow-code-review` 阶段
- **AND** 审查通过后子变更编码-审查阶段标记完成

#### Scenario: 代码审查前置门控
- **WHEN** 进入代码审查阶段
- **THEN** 系统检查子变更编码状态 = ✅ 完成
- **AND** 检查 tasks.md 中所有实现任务已完成
- **AND** 不满足则 ❌ 阻塞，提示先完成编码

#### Scenario: 代码审查不通过
- **WHEN** 代码审查发现高严重度问题 ≥ 1 或中严重度问题 ≥ 3
- **THEN** 系统标记子变更编码阶段为 ❌ 阻塞
- **AND** 输出代码审查报告，列出待修复问题
- **AND** 修复完成后重新触发 `kflow-code-review`

### Requirement: 代码审查双视角并行

系统 SHALL 使用两个并行 Agent 执行代码审查，视角分别为安全+规范和质量+性能。

#### Scenario: 安全+规范视角审查
- **WHEN** `kflow-code-review` 启动
- **THEN** Agent 1 检查 SQL注入、XSS、CSRF、敏感信息泄露、编码规范、依赖安全漏洞
- **AND** 输出安全+规范审查结果

#### Scenario: 质量+性能视角审查
- **WHEN** `kflow-code-review` 启动
- **THEN** Agent 2 检查 N+1查询、内存泄漏风险、错误处理完整性、代码复杂度
- **AND** 输出质量+性能审查结果

### Requirement: 代码审查报告格式

系统 SHALL 按标准格式输出代码审查报告到子变更的 test-reports 目录。

#### Scenario: 审查报告输出路径
- **WHEN** 代码审查完成
- **THEN** 报告输出到 `subchanges/{subchange}/test-reports/review/code-review.md`
- **AND** 报告包含审查时间、子变更名、审查文件数
- **AND** 问题清单含编号、所属 Agent、严重度、文件位置、问题描述、修复状态
- **AND** 包含门控结论（通过/阻塞）
