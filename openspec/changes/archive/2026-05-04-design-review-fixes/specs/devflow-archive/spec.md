# devflow-archive

## MODIFIED Requirements

### Requirement: 归档条件检查

系统 SHALL 在归档前检查主变更状态文件，包含变更级服务刷新标记和集成测试通过证明。

#### Scenario: 检查归档条件
- **WHEN** 用户请求归档
- **THEN** 系统读取 `.status.md` 检查所有阶段状态
- **AND** 所有阶段均标记完成或跳过
- **AND** 检查变更级服务刷新已完成（服务就绪标记 ✅）
- **AND** 检查 `test-reports/integration/summary.md` 存在且标记"集成测试通过"
- **AND** 执行 `kflow-audit` 审计检查
- **AND** 任一不满足则阻断归档

#### Scenario: 审计通过后继续归档
- **WHEN** 归档流程中审计通过
- **THEN** 系统继续执行设计合并和文件移动

#### Scenario: 审计不通过阻断归档
- **WHEN** 归档流程中审计发现阻塞级或严重级问题
- **THEN** 系统阻断归档
- **AND** 提示用户按审计报告修复后重新审计

### Requirement: 变更归档执行

系统 SHALL 支持将已完成或未完成的变更进行归档操作，并在归档时合并设计到产品级。

#### Scenario: 归档已完成变更
- **WHEN** 用户请求归档一个所有阶段已完成的变更
- **THEN** 系统执行归档条件检查
- **AND** 通过后合并功能设计和详细设计到产品级文档
- **AND** 清理所有 checkpoint 文件（变更级 + 子变更级）
- **AND** 将变更目录移动到 docs/archive/{YYYY-MM-DD}-{change}/
- **AND** 更新 .status.md 添加归档记录
- **AND** 更新 docs/changes/index.md 归档记录

#### Scenario: 归档未完成变更
- **WHEN** 用户请求归档一个未完成的变更
- **THEN** 系统允许归档并记录归档状态为"未完成"
- **AND** 记录归档原因
- **AND** 不执行设计合并（未完成变更的设计可能不完整）
