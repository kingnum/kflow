## ADDED Requirements

### Requirement: 服务启动前端口冲突检测

变更级 agent 在启动服务前 SHALL 检测目标端口是否已被其他进程占用。

#### Scenario: 端口空闲时正常启动

- **WHEN** 变更级 agent 需要启动服务且 `service-guide.md` 中定义的端口未被占用
- **THEN** 变更级 agent SHALL 正常启动服务
- **AND** 记录端口检查结果到日志

#### Scenario: 端口被非预期进程占用

- **WHEN** 变更级 agent 检测到目标端口已被占用且占用进程非当前变更管理的服务
- **THEN** 变更级 agent SHALL 标记当前阶段为 ⚠️ 阻塞
- **AND** SHALL 提示用户端口占用信息（端口号、占用进程 PID、进程名称）
- **AND** SHALL NOT 自动 kill 非预期进程

#### Scenario: 端口被残留的服务进程占用

- **WHEN** 变更级 agent 检测到目标端口被占用且占用进程为当前变更管理的残留服务（`.service-state.json` 中记录的 PID）
- **THEN** 变更级 agent SHALL 先执行 STOP_STALE 步骤
- **AND** 发送 SIGTERM → 等待 30s → SIGKILL → 验证端口释放
- **AND** 端口释放后继续正常启动流程

#### Scenario: 端口检测方式

- **WHEN** 执行端口冲突检测
- **THEN** 变更级 agent SHALL 使用 `scripts/with_server.py` 的端口检测功能或系统命令（如 `netstat`、`lsof`、`ss`）
- **AND** 检测结果 SHALL 包含：端口号、占用状态、占用进程 PID（如被占用）

### Requirement: 端口配置来源强制使用 service-guide.md

服务启动时使用的端口 SHALL 严格使用 `docs/service-guide.md` dev 环境中定义的端口，不得自行推断或使用其他端口。

#### Scenario: 从 service-guide.md 读取端口

- **WHEN** 变更级 agent 需要确定服务端口
- **THEN** 变更级 agent SHALL 从 `docs/service-guide.md` 的 dev 环境配置中读取端口值
- **AND** SHALL NOT 自行推断或从其他来源获取端口

#### Scenario: 端口变更时重新读取

- **WHEN** service-guide.md 中的端口配置发生变更
- **THEN** 下次 PRE_HOOK RELOAD 时 SHALL 使用新端口值
- **AND** SHALL NOT 继续使用旧端口值
