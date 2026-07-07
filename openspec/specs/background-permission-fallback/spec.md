## ADDED Requirements

### Requirement: 后台子代理权限失败自动回退前台子代理

当后台子代理因权限问题执行失败时，主 Agent SHALL 自动创建新的前台子代理重新执行同一任务，主 Agent SHALL NOT 直接接管执行。

#### Scenario: 检测权限相关错误

- **WHEN** 后台子代理（run_in_background=true）执行失败
- **AND** 主 Agent 从子代理错误输出中检测到权限相关错误模式
- **THEN** 主 Agent SHALL 匹配以下至少一种错误模式：
  - "permission denied" / "权限不足"
  - "not allowed" / "不允许"
  - "requires approval" / "需要批准"
  - "blocked" / "被阻止"
  - 错误信息包含工具名 + 拒绝语义

#### Scenario: 创建前台子代理回退执行

- **WHEN** 主 Agent 检测到后台子代理因权限问题失败
- **THEN** 主 Agent SHALL 输出提示："检测到子代理因权限问题失败，创建前台子代理重新执行"
- **AND** 主 Agent SHALL 创建新的子代理，参数 `run_in_background=false`
- **AND** 新子代理的 prompt SHALL 包含与原后台子代理相同的任务内容和轮次上下文
- **AND** 主 Agent SHALL NOT 在主 Agent 上下文中直接接管执行

#### Scenario: 前台子代理回退执行成功

- **WHEN** 前台子代理回退执行成功
- **THEN** 主 Agent SHALL 正常继续后续流程
- **AND** SHALL 更新 .status.md 记录回退事件

#### Scenario: 前台子代理回退执行也失败

- **WHEN** 前台子代理回退执行也失败
- **THEN** 主 Agent SHALL 标记该阶段为 ⚠️ 阻塞
- **AND** SHALL 输出提示："子代理前台/后台均失败，请检查权限配置或手动处理"
- **AND** 主 Agent SHALL NOT 在任何情况下直接接管执行

#### Scenario: 非权限错误的失败

- **WHEN** 后台子代理执行失败
- **AND** 主 Agent 未检测到权限相关错误模式
- **THEN** 主 Agent SHALL 按原有轮次级重试机制处理（参见 `kflow-shared/repetition-model.md` §12）
- **AND** SHALL NOT 执行权限回退前台子代理逻辑

### Requirement: 权限回退不计入轮次级重试上限

后台子代理权限失败回退前台子代理的执行 SHALL NOT 计入 `kflow-shared/repetition-model.md` §12 定义的轮次级重试 3 次上限。

#### Scenario: 回退后的重试计数独立

- **WHEN** 后台子代理因权限失败后回退为前台子代理执行
- **THEN** 该回退 SHALL NOT 计入轮次级重试的 3 次上限
- **AND** 轮次级重试计数器 SHALL 保持不变
- **AND** 回退执行是独立于重试机制的不同执行模式切换

#### Scenario: 前台子代理回退后的重试

- **WHEN** 前台子代理回退执行失败后
- **AND** 主 Agent 标记该阶段为阻塞
- **THEN** 后续的重试操作（如用户触发恢复）SHALL 从轮次级重试计数器的当前值继续
- **AND** 回退执行不计入该计数器
