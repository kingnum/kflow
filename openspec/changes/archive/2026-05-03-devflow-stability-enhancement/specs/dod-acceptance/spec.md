## ADDED Requirements

### Requirement: 每功能点定义 DoD 验收标准

系统 SHALL 在计划阶段为每功能点的任务清单增加 Definition of Done (DoD) 验收标准区块。

#### Scenario: DoD 区块格式
- **WHEN** kflow-plan 生成子变更 tasks.md
- **THEN** 每个功能点的任务章节顶部包含 DoD 验收标准检查清单
- **AND** 验收标准涵盖正常路径、异常路径、边界条件、质量标准四个维度

#### Scenario: 四维验收标准
- **WHEN** 定义验收标准
- **THEN** Happy Path (正常路径) ≥ 1 条
- **AND** Error Path (异常路径) ≥ 2 条
- **AND** Edge Case (边界条件) ≥ 1 条
- **AND** Quality (质量标准) ≥ 1 条

#### Scenario: DoD 检查清单
- **WHEN** 功能点实现完成
- **THEN** 检查功能代码已实现、单元测试已通过、边界条件有覆盖、代码审查通过、验收标准全部满足、代码已提交

### Requirement: 验收标准编写规则

系统 SHALL 在计划阶段指导验收标准的编写。

#### Scenario: 验收标准示例格式
- **WHEN** 为功能点"用户登录"编写验收标准
- **THEN** Happy Path: "用户名+密码正确 → 返回 JWT token"
- **AND** Error Path 1: "密码错误 → 返回 401"
- **AND** Error Path 2: "用户不存在 → 返回 401（不泄露用户存在性）"
- **AND** Edge Case: "连续 5 次失败 → 账号锁定 15 分钟"
- **AND** Quality: "登录接口响应时间 P95 < 200ms"
