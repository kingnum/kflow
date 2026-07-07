## Requirements

### Requirement: 两级缺陷修复共享入口

系统 SHALL 通过单一 kflow-bug-fix Skill 入口支持子变更级和变更级两级缺陷修复。

#### Scenario: 上下文检测为子变更级
- **WHEN** 调用 kflow-bug-fix 且当前阶段为接口单元测试或 E2E 测试
- **THEN** 系统路由到子变更级缺陷修复流程
- **AND** 使用子变更级根因二分法

#### Scenario: 上下文检测为变更级
- **WHEN** 调用 kflow-bug-fix 且当前阶段为集成测试
- **THEN** 系统路由到变更级缺陷修复流程
- **AND** 使用变更级根因四分法

#### Scenario: 上下文无法判断
- **WHEN** 系统无法通过当前阶段判断级别
- **THEN** 系统询问用户确认调用上下文

### Requirement: 变更级根因四分法

系统 SHALL 在变更级集成测试失败时使用根因四分法进行分类。

#### Scenario: 接口实现错误
- **WHEN** 集成测试失败且单个子变更实现不满足接口契约
- **THEN** 系统分类为接口实现错误
- **AND** 定位到具体子变更并修复代码
- **AND** 子变更级重新测试后重新执行集成测试

#### Scenario: 接口契约错误
- **WHEN** 集成测试失败且接口契约定义本身有问题
- **THEN** 系统分类为接口契约错误
- **AND** 更新 detailed-design.md 中的跨子变更接口契约
- **AND** 评估联动影响范围（哪些子变更受影响）
- **AND** 受影响子变更修订并重测后重新执行集成测试

#### Scenario: 集成测试用例错误
- **WHEN** 集成测试失败且集成测试用例本身有问题
- **THEN** 系统分类为集成测试用例错误
- **AND** 修正 integration-tests.md 中对应测试用例
- **AND** 重新执行集成测试

#### Scenario: 架构设计错误
- **WHEN** 集成测试失败且架构层面设计有问题
- **THEN** 系统分类为架构设计错误
- **AND** 标记变更级详细设计为 ⚠️ 需修订
- **AND** 重置所有子变更状态为 ⏳ 待开始
- **AND** 修订 detailed-design.md 后重新执行四视角审查
- **AND** 所有子变更重新执行计划→编码→测试→集成测试

### Requirement: 变更级修复报告

系统 SHALL 在变更级缺陷修复时输出修复报告到变更级目录。

#### Scenario: 变更级修复报告路径
- **WHEN** 执行变更级缺陷修复
- **THEN** 修复报告输出到 test-reports/integration/fix-reports/fix-{timestamp}.md
- **AND** 契约错误时额外输出 contract-error-{timestamp}.md 分析报告

#### Scenario: 变更级修复报告内容
- **WHEN** 输出变更级修复报告
- **THEN** 报告包含根因分类结论和决策路径
- **AND** 报告包含受影响子变更列表
- **AND** 报告包含接口契约变更的联动影响评估

### Requirement: 多轮集成测试修复循环

系统 SHALL 支持集成测试失败后进入修复→重新集成测试的循环，直到全部通过。

#### Scenario: 单轮修复后重新测试
- **WHEN** 变更级根因分类为接口实现错误或测试用例错误
- **THEN** 修复完成后自动触发新一轮集成测试
- **AND** 产生新的测试轮次报告

#### Scenario: 多轮收敛
- **WHEN** 集成测试经过 N 轮修复后全部用例通过
- **THEN** 系统输出 summary.md 标记"集成测试通过"
- **AND** 记录总轮次数和修复历史
