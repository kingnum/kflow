## MODIFIED Requirements

### Requirement: 变更级 agent 独占服务生命周期管理

系统 SHALL 将服务生命周期管理（启动、停止、编译、重启、健康检查）的职责完全归属于变更级 agent，且必须读取 service-guide.md 获取启动命令和配置。

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

### Requirement: with_server.py 作为变更级 agent 的服务管理工具（MODIFIED）

系统 SHALL 使用 `scripts/with_server.py` 作为变更级 agent 执行服务启停操作的工具脚本，且启动命令必须从 `docs/service-guide.md` 读取。

#### Scenario: 使用 with_server.py 启动服务

- **WHEN** 变更级 agent 需要启动服务
- **THEN** 变更级 agent 必须读取 `docs/service-guide.md` 获取 dev 环境的启动命令和端口
- **AND** 执行 `python scripts/with_server.py --server "{service-guide 中的启动命令}" --port {service-guide 中的端口} -- {后续命令}`
- **AND** with_server.py 在 {后续命令} 执行完毕后自动停止服务并清理进程

#### Scenario: 多服务同时启动

- **WHEN** 变更级 agent 需要同时启动后端和前端服务
- **THEN** 变更级 agent 从 service-guide.md 读取后端和前端的启动命令和端口
- **AND** 使用多个 `--server` 和 `--port` 参数
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
