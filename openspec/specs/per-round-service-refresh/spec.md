# per-round-service-refresh Specification

## Purpose
定义每轮测试前服务的编译、重启、健康检查与每轮测试后停止服务的规范，以及编码阶段的编译验证流程，确保每轮测试在干净的服务状态下执行。

## Requirements

### Requirement: 每轮测试前重新编译重启服务

系统 SHALL 在每轮 API 测试、E2E 测试和集成测试开始前，由变更级 agent 执行完整的 STOP→编译→迁移→启动→健康检查流程。每轮测试完成后 SHALL 停止服务。

#### Scenario: API 测试 Round N 开始前编译重启

- **WHEN** API 测试进入新的轮次（Round N）
- **THEN** 变更级 agent 停止当前服务
- **AND** 执行后端编译
- **AND** 执行未执行的数据库迁移脚本
- **AND** 启动后端服务
- **AND** 执行健康检查（/health + /db-health）
- **AND** 健康检查全部通过后通知子变更 agent「服务就绪，开始 Round N」

#### Scenario: E2E 测试 Round N 开始前编译重启

- **WHEN** E2E 测试进入新的轮次（Round N）
- **THEN** 变更级 agent 停止当前服务
- **AND** 执行后端编译
- **AND** 执行前端编译
- **AND** 执行未执行的数据库迁移脚本
- **AND** 启动后端服务
- **AND** 启动前端服务
- **AND** 执行健康检查（/health + /db-health + 前端 /health）
- **AND** 健康检查全部通过后通知子变更 agent「服务就绪，开始 Round N」

#### Scenario: 集成测试 Round N 开始前编译重启

- **WHEN** 集成测试进入新的轮次
- **THEN** 变更级 agent 执行与 E2E 测试相同的编译重启流程
- **AND** 健康检查通过后开始执行集成测试用例

#### Scenario: 每轮测试完成后停止服务

- **WHEN** 当前轮次（Round N）所有子变更测试执行完毕
- **THEN** 变更级 agent SHALL 停止所有运行中的服务（后端+前端）
- **AND** SHALL 执行 `playwright-cli kill-all` 清理残留浏览器进程（如有）
- **AND** SHALL 验证所有服务端口已释放

#### Scenario: 首轮测试前的编译重启

- **WHEN** 所有子变更编码和代码审查完成后首次进入测试阶段
- **THEN** 变更级 agent 执行完整的编译重启流程（与后续轮次相同）
- **AND** 此轮即为 Round 1 的开始条件

#### Scenario: 上一轮全部通过无需下一轮

- **WHEN** 当前轮次所有测试用例全部通过
- **THEN** 变更级 agent SHALL 停止服务
- **AND** SHALL NOT 执行下一轮编译重启
- **AND** 直接输出 summary.md 标记测试完成

### Requirement: 批量同步推进

系统 SHALL 要求所有子变更完成当前轮次测试和缺陷修复后，统一进入下一轮。

#### Scenario: 等待本轮所有子变更完成
- **WHEN** 部分子变更已完成 Round N 测试但其他子变更仍在执行或修复中
- **THEN** 已完成的子变更进入「等待变更级同步」状态
- **AND** 不自行推进到 Round N+1

#### Scenario: 本轮全部完成触发同步
- **WHEN** 所有子变更 Round N 测试完成且本轮发现的缺陷均已修复（或无需修复）
- **THEN** 变更级 agent 执行编译重启进入 Round N+1
- **AND** 通知所有子变更 agent 开始 Round N+1 测试

#### Scenario: 无失败子变更时跳过等待
- **WHEN** 当前轮次所有子变更测试全部通过且无任何失败
- **THEN** 变更级 agent 输出 summary.md 标记测试完成
- **AND** 所有子变更直接进入完成状态，无需批量同步

#### Scenario: 仅部分子变更失败时批量推进
- **WHEN** 当前轮次仅部分子变更测试失败
- **THEN** 仅失败的子变更进入缺陷修复流程
- **AND** 通过的子变更等待失败子变更修复完成
- **AND** 全部修复完成后变更级 agent 编译重启进入下一轮
- **AND** 已通过的子变更在下一轮中重新测试以验证无回归

### Requirement: 服务编译重启的迁移保护

系统 SHALL 在每轮编译重启时仅执行未执行的迁移脚本，已执行迁移不重复执行。

#### Scenario: 后续轮次跳过已执行迁移
- **WHEN** Round N 编译重启包含迁移执行步骤（N > 1）
- **THEN** 变更级 agent 扫描 `migration-log.md` 排除已标记为「已执行」的迁移
- **AND** 仅执行自上次同步以来新增的迁移脚本

#### Scenario: 首轮执行所有迁移
- **WHEN** Round 1 编译重启（首次进入测试阶段）
- **THEN** 变更级 agent 执行所有未在 `migration-log.md` 中标记为已执行的迁移

### Requirement: 编码阶段仅执行编译验证

编码阶段 SHALL 在所有子代理完成编码后，执行一次性的编译验证（验证代码可编译），不启动持久服务。

#### Scenario: 编码完成后的编译验证

- **WHEN** 所有子变更的子代理完成 TDD 编码
- **THEN** 变更级 agent SHALL 执行统一编译验证
- **AND** 后端编译：执行 service-guide.md 中定义的编译命令（如 `mvn compile`）
- **AND** 前端编译：执行 service-guide.md 中定义的前端编译命令（如 `npm run build` 或 `tsc --noEmit`）
- **AND** 编译验证 SHALL NOT 包含服务启动、数据库迁移、健康检查等步骤
- **AND** 编译验证通过后释放代码审查阶段门控

#### Scenario: 编译验证失败

- **WHEN** 统一编译验证失败
- **THEN** 变更级 agent SHALL 标记编码阶段为 ❌ 阻塞
- **AND** SHALL 分析编译错误并修复后重新编译
- **AND** SHALL NOT 跳过编译验证直接进入代码审查
