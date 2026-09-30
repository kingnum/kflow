# Spec Delta

## MODIFIED Requirements

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
- **THEN** 变更级 agent SHALL 使用 `skills/kflow-code/scripts/with_server.py` 的端口检测功能或系统命令（如 `netstat`、`lsof`、`ss`）
- **AND** 检测结果 SHALL 包含：端口号、占用状态、占用进程 PID（如被占用）
- **AND** SHALL NOT 引用 `kflow-shared/` 下的任何脚本路径
