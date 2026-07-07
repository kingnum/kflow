# centralized-service-management Specification (Delta)

## MODIFIED Requirements

### Requirement: 变更级 agent 独占服务生命周期管理

系统 SHALL 将服务生命周期管理（启动、停止、编译、重启、健康检查）的职责完全归属于变更级 agent，且必须读取 service-guide.md 获取启动命令和配置。系统 SHALL 在首次读取 service-guide.md 时执行就绪检测，确保配置完整且外部服务依赖连接信息可用。

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
