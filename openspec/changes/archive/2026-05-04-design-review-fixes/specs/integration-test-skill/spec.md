# integration-test-skill

## ADDED Requirements

### Requirement: 集成测试独立 Skill

系统 SHALL 提供 `kflow-integration-test` Skill 作为变更级集成测试的独立执行入口。

#### Scenario: Skill 触发
- **WHEN** 用户输入包含"集成测试"、"跨子变更测试"等关键词，或所有子变更测试通过后自动进入
- **THEN** 系统启动 `kflow-integration-test` Skill 执行变更级集成测试

#### Scenario: 前置门控检查
- **WHEN** Skill 启动
- **THEN** 系统检查所有子变更的接口单元测试和 E2E 测试（前后端项目）均已通过
- **AND** 检查 integration-tests.md 文件存在
- **AND** 检查变更级服务刷新已完成
- **AND** 任一不满足则提示先完成前置条件

#### Scenario: 项目类型适配
- **WHEN** 项目类型为纯后端项目
- **THEN** Skill 仍执行集成测试（纯后端项目也需执行集成测试）
- **AND** 仅跳过浏览器相关测试，使用接口调用方式执行

### Requirement: 集成测试执行

系统 SHALL 基于 `integration-tests.md` 执行全部集成测试用例。

#### Scenario: 全用例通过
- **WHEN** 集成测试全部用例通过
- **THEN** 系统输出 `test-reports/integration/summary.md` 标记"集成测试通过"
- **AND** 变更可以进入审计和归档阶段

#### Scenario: 部分用例失败
- **WHEN** 集成测试有失败用例
- **THEN** 系统记录失败详情到 `test-reports/integration/round-{n}.md`
- **AND** 进入内聚的四分法缺陷修复循环

### Requirement: 内聚变更级缺陷修复

系统 SHALL 在集成测试失败时内聚执行四分法根因分类和修复，不跳转到外部 Skill。

#### Scenario: 接口实现错误修复
- **WHEN** 根因判定为单子变更实现不满足接口契约（占比约 60%）
- **THEN** 系统定位具体子变更
- **AND** 修复子变更代码
- **AND** 子变更级重新测试通过后重新执行集成测试

#### Scenario: 接口契约错误修复
- **WHEN** 根因判定为接口契约定义本身有问题（占比约 20%）
- **THEN** 系统更新 `detailed-design.md` 中的接口契约定义
- **AND** 评估受影响子变更的联动范围
- **AND** 标记受影响子变更状态为 ⚠️ 需修订
- **AND** 联动修复后重新执行集成测试
- **AND** 输出契约错误分析报告到 `test-reports/integration/fix-reports/contract-error-{timestamp}.md`

#### Scenario: 集成测试用例错误修复
- **WHEN** 根因判定为集成测试用例预期与设计不符（占比约 15%）
- **THEN** 系统修正 `integration-tests.md` 中对应用例
- **AND** 验证测试用例正确性后重新执行集成测试

#### Scenario: 架构设计错误处理
- **WHEN** 根因判定为架构层面设计有缺陷（占比约 5%）
- **THEN** 系统标记集成测试阶段为 ❌ 阻塞
- **AND** 标记详细设计阶段为 ⚠️ 需修订
- **AND** 重置所有子变更状态为 ⏳ 待开始
- **AND** 输出架构错误分析报告到 `test-reports/integration/fix-reports/arch-error-{timestamp}.md`
- **AND** 触发架构评估流程

### Requirement: 多轮循环收敛

系统 SHALL 支持集成测试的多轮修复-重测循环，直到全部通过。

#### Scenario: 修复后重新集成测试
- **WHEN** 任一类型修复完成
- **THEN** 系统自动触发新一轮集成测试
- **AND** 输出新的测试轮次报告

#### Scenario: 全部通过后收敛
- **WHEN** 集成测试全部用例通过
- **THEN** 系统输出 `test-reports/integration/summary.md` 标记"集成测试通过"
- **AND** 记录总轮次数和各轮修复历史

#### Scenario: 连续 3 轮同一用例失败
- **WHEN** 同一测试用例 ID 在连续 3 轮测试中均失败
- **THEN** 系统自动触发架构评估流程
- **AND** 暂停修复循环，等待用户对架构评估方案的决策
