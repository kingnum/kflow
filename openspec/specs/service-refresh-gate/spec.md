# service-refresh-gate Specification

## Purpose
Defines the per-round service compilation and restart gate that must be passed before each round of E2E testing or integration testing.

## Requirements
### Requirement: 变更级服务编译刷新同步点

系统 SHALL 在每轮测试开始前强制执行一次变更级服务编译刷新，由变更级 agent 执行。服务刷新不再是「编码完成后一次性」门控，而是「每轮测试前」的重复执行步骤。

#### Scenario: 同步点触发条件
- **WHEN** 进入新的 E2E 测试轮次或集成测试轮次（含首轮）
- **THEN** 变更级 agent 触发服务编译刷新
- **AND** 在任一子变更进入该轮测试前必须完成

#### Scenario: 同步点每轮执行
- **WHEN** 所有子变更完成当前轮次测试和修复后需要进入下一轮
- **THEN** 变更级 agent 重新执行服务编译刷新
- **AND** 编译通过且健康检查通过后释放下一轮测试门控

#### Scenario: 本轮全部通过则不执行下一轮刷新
- **WHEN** 当前轮次所有测试用例全部通过
- **THEN** 变更级 agent 不执行下一轮服务刷新
- **AND** 直接进入测试完成流程

### Requirement: 服务编译与启动

系统 SHALL 在每轮刷新时编译并启动前后端服务。

#### Scenario: 后端编译与启动
- **WHEN** 每轮服务刷新触发
- **THEN** 变更级 agent 读取 `docs/service-guide.md` 获取后端编译命令
- **AND** 停止当前运行的服务
- **AND** 执行编译
- **AND** 编译成功后使用 with_server.py 启动后端服务
- **AND** 编译失败则 ❌ 阻塞，修复后重新编译

#### Scenario: 前端编译与启动（前后端项目）
- **WHEN** 项目类型为前后端项目且后端启动成功
- **THEN** 变更级 agent 读取 `service-guide.md` 获取前端编译命令
- **AND** 执行编译
- **AND** 编译成功后使用 with_server.py 启动前端服务

#### Scenario: 纯后端项目跳过前端
- **WHEN** 项目类型为纯后端项目
- **THEN** 变更级 agent 仅编译和启动后端服务
- **AND** 不执行前端相关操作

### Requirement: 服务健康检查

系统 SHALL 在每轮服务启动后执行健康检查。

#### Scenario: 健康检查通过
- **WHEN** 每轮服务启动完成
- **THEN** 变更级 agent 调用 `/health` 端点验证服务可用
- **AND** 调用 `/db-health` 端点验证数据库连接正常
- **AND** (前后端项目) 调用前端 `/health` 端点
- **AND** 全部返回 200 后标记本轮服务就绪 ✅

#### Scenario: 健康检查失败
- **WHEN** 任一健康检查端点返回非 200
- **THEN** 变更级 agent 标记当前轮次服务刷新为 ❌ 阻塞
- **AND** 分析日志定位失败原因
- **AND** 修复后重新执行启动和健康检查
- **AND** 遵循障碍自解原则，禁止跳过

### Requirement: 服务就绪门控释放

系统 SHALL 在每轮服务刷新通过后释放该轮测试的门控。

#### Scenario: 门控释放
- **WHEN** 每轮健康检查全部通过
- **THEN** 变更级 agent 通知所有子变更 agent 「服务就绪，开始 Round N」
- **AND** 子变更 agent 开始本轮测试

### Requirement: 迁移脚本合并与执行

系统 SHALL 在每轮服务刷新时按序号排序并执行所有未执行迁移脚本。

#### Scenario: 迁移脚本收集
- **WHEN** 每轮服务刷新启动
- **THEN** 变更级 agent 扫描所有子变更关联的迁移脚本（`migrations/{序号}_*.sql`）
- **AND** 按序号排序
- **AND** 排除已在 `migration-log.md` 中记录为「已执行」的脚本

#### Scenario: 迁移执行
- **WHEN** 迁移脚本收集完成
- **THEN** 变更级 agent 按序号依次执行迁移脚本
- **AND** 每执行完一个即在 `migration-log.md` 中记录

#### Scenario: 迁移失败回滚
- **WHEN** 迁移脚本执行失败
- **THEN** 变更级 agent 执行对应的 `_rollback.sql` 回滚脚本
- **AND** 标记当前轮次服务刷新为 ❌ 阻塞
- **AND** 分析失败原因并修复后重新执行
