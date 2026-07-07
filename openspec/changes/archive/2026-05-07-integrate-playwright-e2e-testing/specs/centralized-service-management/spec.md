## ADDED Requirements

### Requirement: 变更级 agent 独占服务生命周期管理

系统 SHALL 将服务生命周期管理（启动、停止、编译、重启、健康检查）的职责完全归属于变更级 agent。

#### Scenario: 变更级 agent 管理服务启停
- **WHEN** 服务需要启动、停止或重启
- **THEN** 仅变更级 agent 执行这些操作
- **AND** 子变更 agent 不得自行启动、停止或重启服务

#### Scenario: 子变更 agent 为纯消费者
- **WHEN** 子变更 agent 需要执行 E2E 测试或接口测试
- **THEN** 子变更 agent 接收变更级 agent 发出的「服务就绪」信号
- **AND** 子变更 agent 直接连接已知端口使用服务
- **AND** 子变更 agent 不管理服务的生命周期

#### Scenario: 子变更 agent 发现服务不可用
- **WHEN** 子变更 agent 在测试过程中发现服务端口无响应
- **THEN** 子变更 agent 将服务不可用状态上报变更级 agent
- **AND** 子变更 agent 不自行尝试重启服务
- **AND** 等待变更级 agent 恢复服务后继续

### Requirement: with_server.py 作为变更级 agent 的服务管理工具

系统 SHALL 使用 `scripts/with_server.py` 作为变更级 agent 执行服务启停操作的工具脚本。

#### Scenario: 使用 with_server.py 启动服务
- **WHEN** 变更级 agent 需要启动服务
- **THEN** 变更级 agent 从 `docs/service-guide.md` 的 dev 环境获取启动命令和端口
- **AND** 执行 `python scripts/with_server.py --server "{启动命令}" --port {端口} -- {后续命令}`
- **AND** with_server.py 在 {后续命令} 执行完毕后自动停止服务并清理进程

#### Scenario: 多服务同时启动
- **WHEN** 变更级 agent 需要同时启动后端和前端服务
- **THEN** 变更级 agent 使用多个 `--server` 和 `--port` 参数
- **AND** with_server.py 按参数顺序依次启动服务并等待就绪
- **AND** 全部就绪后执行后续命令

#### Scenario: 服务就绪检测
- **WHEN** with_server.py 启动服务
- **THEN** 脚本轮询 localhost:{port} 直到端口可连接
- **AND** 超时（默认 30s）后报告启动失败
- **AND** 启动失败时自动清理已启动的其他服务进程

#### Scenario: 服务异常退出清理
- **WHEN** 后续命令执行完毕或因异常退出
- **THEN** with_server.py 的 finally 块自动 terminate 所有服务进程
- **AND** 超时 5s 未终止则 kill

### Requirement: 服务崩溃恢复统一走变更级 agent

系统 SHALL 在服务崩溃时通过变更级 agent 统一恢复，不由于变更 agent 自行处理。

#### Scenario: 崩溃检测与上报
- **WHEN** 子变更 agent 发现 `curl localhost:{port}` 返回 Connection Refused
- **THEN** 子变更 agent 立即上报变更级 agent
- **AND** 子变更 agent 标记当前测试用例为「阻塞等待服务恢复」

#### Scenario: 变更级 agent 崩溃恢复
- **WHEN** 变更级 agent 收到服务崩溃上报
- **THEN** 变更级 agent 执行 `playwright-cli kill-all` 清理残留浏览器进程
- **AND** 执行 with_server.py 重新编译并启动服务
- **AND** 健康检查通过后通知所有受影响的子变更 agent 继续

### Requirement: 中断恢复统一走变更级 agent

系统 SHALL 在中断恢复时通过变更级 agent 恢复服务状态。

#### Scenario: 从 checkpoint 恢复
- **WHEN** `kflow-resume` 从 checkpoint 恢复到 E2E 测试或集成测试阶段
- **THEN** 变更级 agent 检测服务是否在运行
- **AND** 如服务未运行，变更级 agent 使用 with_server.py 启动服务
- **AND** 健康检查通过后调度对应阶段的测试继续

#### Scenario: 恢复时跳过已执行迁移
- **WHEN** 从 checkpoint 恢复且需要重新编译启动
- **THEN** 变更级 agent 仅编译和启动服务
- **AND** 跳过已在 `migration-log.md` 中标记为「已执行」的迁移脚本
