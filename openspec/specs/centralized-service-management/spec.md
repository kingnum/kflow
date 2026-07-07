# centralized-service-management Specification

## Purpose
定义集中式服务生命周期管理的规范，明确变更级 agent 和子变更 agent 在服务管理中的职责边界，规范 with_server.py 工具脚本的两种运行模式（一次性模式与持久化模式），以及运行时服务状态追踪机制。

## Requirements

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

#### Scenario: 首次读取 service-guide.md 时执行就绪检测

- **WHEN** 变更级 agent 在 READ_SERVICE_GUIDE 步骤中读取 `docs/service-guide.md`
- **THEN** 系统 SHALL 检测文件存在性、内容完整性（dev 环境启动命令和端口非模板占位符）和外部服务依赖连接信息
- **AND** 缺失信息时 SHALL 通过 AskUserQuestion 收集用户输入并持久化

### Requirement: with_server.py 作为变更级 agent 的服务管理工具

系统 SHALL 使用 `kflow-shared/scripts/with_server.py` 作为变更级 agent 执行服务启停操作的工具脚本，支持一次性模式和持久化模式两种运行方式，且启动命令必须从 `docs/service-guide.md` 读取。

#### Scenario: 使用 with_server.py 一次性模式（保持现有行为）

- **WHEN** 变更级 agent 需要在执行某命令期间临时启动服务
- **THEN** 变更级 agent 必须读取 `docs/service-guide.md` 获取 dev 环境的启动命令和端口
- **AND** 执行 `python kflow-shared/scripts/with_server.py --server "{启动命令}" --port {端口} -- {后续命令}`
- **AND** with_server.py 在 {后续命令} 执行完毕后自动停止服务并清理进程

#### Scenario: 使用 with_server.py 持久化模式

- **WHEN** 变更级 agent 需要启动服务并保持运行（如测试阶段的服务刷新）
- **THEN** 变更级 agent SHALL 使用 `--daemon` 参数启动持久化模式
- **AND** 使用 `--state-file` 参数指定状态文件路径（`docs/changes/{change}/.service-state.json`）
- **AND** 执行 `python kflow-shared/scripts/with_server.py --server "{启动命令}" --port {端口} --daemon --state-file {path}`
- **AND** 脚本 SHALL 将服务的 PID、端口、启动命令、启动时间写入指定的状态文件
- **AND** 脚本 SHALL 在后台保持服务运行，不自动停止

#### Scenario: 查询持久化服务状态

- **WHEN** 变更级 agent 需要查询当前运行的服务状态
- **THEN** 变更级 agent SHALL 执行 `python kflow-shared/scripts/with_server.py --status --state-file {path}`
- **AND** 脚本 SHALL 读取状态文件并输出服务运行状态（运行中/已停止/健康状态）

#### Scenario: 停止所有持久化服务

- **WHEN** 变更级 agent 需要停止所有持久化服务
- **THEN** 变更级 agent SHALL 执行 `python kflow-shared/scripts/with_server.py --stop-all --state-file {path}`
- **AND** 脚本 SHALL 读取状态文件中的 PID 列表
- **AND** 逐一发送 SIGTERM → 等待最多 30s → SIGKILL → 等待 10s
- **AND** 验证所有端口已释放
- **AND** 清理状态文件

#### Scenario: 健康检查

- **WHEN** 变更级 agent 需要检查持久化服务的健康状态
- **THEN** 变更级 agent SHALL 执行 `python kflow-shared/scripts/with_server.py --health --port {端口}`
- **AND** 脚本 SHALL curl `/health` 端点并返回 HTTP 状态码

#### Scenario: 多服务同时启动（持久化模式）

- **WHEN** 变更级 agent 需要同时启动后端和前端服务（持久化模式）
- **THEN** 使用多个 `--server` 和 `--port` 参数
- **AND** 脚本按参数顺序依次启动服务并等待就绪
- **AND** 所有服务 PID 写入同一个状态文件

#### Scenario: 服务就绪检测

- **WHEN** with_server.py 启动服务（一次性或持久化模式）
- **THEN** 脚本轮询 localhost:{port} 直到端口可连接
- **AND** 超时（默认 60s for daemon mode, 30s for one-shot mode）后报告启动失败
- **AND** 启动失败时自动清理已启动的其他服务进程

#### Scenario: 服务异常退出清理

- **WHEN** 一次性模式中后续命令执行完毕或因异常退出
- **THEN** with_server.py 的 finally 块自动 terminate 所有服务进程
- **AND** 超时 5s 未终止则 kill
- **AND** 持久化模式不受此规则影响（不自动停止）

### Requirement: 运行时服务状态文件

系统 SHALL 使用 `.service-state.json` 文件追踪持久化服务的运行时状态。

#### Scenario: 状态文件格式

- **WHEN** 持久化服务被启动
- **THEN** with_server.py SHALL 写入如下 JSON 结构的状态文件：
```json
{
  "services": [
    {
      "name": "backend",
      "port": 8080,
      "pid": 12345,
      "start_command": "mvn spring-boot:run -Dspring-boot.run.profiles=dev",
      "started_at": "2026-05-28T10:30:00",
      "last_health_check": "2026-05-28T10:35:00",
      "health_status": "ok"
    }
  ],
  "browser_sessions": []
}
```

#### Scenario: 状态文件位置

- **WHEN** 变更级 agent 使用持久化模式
- **THEN** 状态文件 SHALL 存储在 `docs/changes/{change}/.service-state.json`
- **AND** 状态文件与变更的 `.status.md` 处于同一目录

#### Scenario: 服务停止后状态文件清理

- **WHEN** 所有持久化服务被成功停止
- **THEN** SHALL 删除 `.service-state.json` 或标记所有服务为已停止
