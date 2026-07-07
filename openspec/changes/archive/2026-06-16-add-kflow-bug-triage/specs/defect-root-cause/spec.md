## MODIFIED Requirements

### Requirement: 缺陷根因二分法分类

系统 SHALL 在子变更级缺陷修复阶段对测试失败进行二分法根因分类（实现错误/测试错误），并在修复循环中遵循三次尝试上限。分类执行前 SHALL 完成系统化 feedback loop 构建和可证伪多假设生成。

> **变更说明**：原三分法（实现错误/测试错误/设计错误）简化为二分法。"设计错误"分类及回退路由职责上移到 `kflow-bug-triage`。bug-fix 的入口仅限测试阶段自动发现（B 路径），不再接受用户直接反馈（用户反馈统一走 triage 的 A 路径）。

#### Scenario: 根因分类判断
- **WHEN** 子变更接口单元测试或 E2E 测试失败进入缺陷修复阶段
- **THEN** 系统分类根因为以下两类之一：实现错误、测试错误
- **AND** 分类结果决定后续处理路由
- **AND** 不再需要检测上下文级别（入口 Skill 已确定上下文）
- **AND** 分类前 SHALL 已完成 feedback loop 构建和缺陷复现（参考 `diagnose-feedback-loop` spec）

#### Scenario: 实现错误路由
- **WHEN** 根因判定为"代码实现不符合预期"
- **THEN** 进入标准修复流程：修复代码 → 本地验证 → 返回测试阶段
- **AND** 若此前已对同一失败尝试 2 次实现错误修复且均失败，SHALL 升级到第三次尝试（替代方案）

#### Scenario: 测试错误路由
- **WHEN** 根因判定为"测试用例或测试代码有误"
- **THEN** 修正测试用例或测试代码 → 本地验证 → 返回测试阶段
- **AND** 不修改任何实现代码
- **AND** 若此前已对同一失败尝试 2 次测试修正且均失败，SHALL 升级到第三次尝试（重新思考）

#### Scenario: 三次尝试后升级
- **WHEN** 同一测试用例三次修复尝试均失败
- **THEN** 系统 SHALL 停止自动修复循环
- **AND** SHALL 使用 AskUserQuestion 升级用户，提供三个选项：保留当前状态（人工介入）/ 跳过该功能点（标记为已知问题）/ 触发设计阶段回退
- **AND** 若用户选择触发设计回退，SHALL 建议用户通过 kflow-bug-triage 进行正式诊断

### Requirement: 根因分类决策树

系统 SHALL 使用二分法决策树辅助子变更级根因分类，并结合可证伪假设的测试结果进行判定。

#### Scenario: 决策树判断逻辑
- **WHEN** 根因不明确
- **THEN** 依次检查：代码实现是否符合预期 → 否 → 实现错误
- **AND** 测试用例与设计是否一致 → 否 → 测试错误
- **AND** 以上均否 → 实现错误（默认分类）
- **AND** 结合 Phase 3 假设测试结果辅助判定

### Requirement: 缺陷修复入口门控

系统 SHALL 将缺陷修复阶段的入口限定为测试阶段自动触发。

#### Scenario: 入口检查
- **WHEN** 缺陷修复阶段被触发
- **THEN** 系统 SHALL 验证存在以下入口条件之一：
  - 子变更接口单元测试的失败轮次报告（round-{n}.md）
  - 子变更 E2E 测试的失败轮次报告（round-{n}.md）
- **AND** SHALL NOT 接受"用户描述的缺陷信息"作为入口条件（用户反馈统一由 kflow-bug-triage 处理）

## REMOVED Requirements

### Requirement: 设计错误回退报告

**Reason**: "设计错误"分类及回退路由职责已上移到 kflow-bug-triage。bug-fix 不再需要判定设计错误或输出设计错误报告。当三次尝试后升级用户且用户选择设计回退时，引导用户通过 kflow-bug-triage 进行正式诊断。

**Migration**: 使用 kflow-bug-triage Skill 进行问题源头诊断，triage 会路由到对应阶段的 REVISION 模式。
