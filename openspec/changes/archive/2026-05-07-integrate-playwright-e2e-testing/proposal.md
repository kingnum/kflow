# Proposal: Integrate Playwright E2E Testing

## Why

当前 `kflow-e2e-qa` 的测试执行方法过于笼统——「启动浏览器自动化工具 → 执行所有测试用例」——缺少具体的方法论指导：元素选择器从哪来？不同测试场景如何选择路径？健康评分如何采集数据？服务生命周期由谁管理？这些问题导致 agent 测试行为不可预测，测试质量和效率不稳定。

`references/playwright-cli` 提供了 snapshot+ref 元素定位、自动测试代码生成、DevTools 集成等能力，`references/webapp-testing` 提供了决策树、侦查-行动模式等服务生命周期管理方法。将这些整合进 KFlow E2E 测试阶段，可以显著提升测试执行的标准化程度和可复现性。

## What Changes

- **BREAKING**: 重命名 `kflow-e2e-qa` → `kflow-e2e-test`（Skill 名称和文件全部更新）
- 引入 playwright-cli snapshot+ref 模式作为主要元素定位方法，替代手工编写 CSS 选择器
- 引入测试决策树（静态 HTML / 动态应用 / 服务器状态分支）
- 健康评分维度映射到 playwright-cli 具体命令（console、eval performance.timing、screenshot）
- 测试代码自动生成作为新产物（generated-test.spec.ts，子变更级保留）
- 网络 Mock 用于错误场景测试（route 命令）
- 服务管理集中到变更级 agent，子变更 agent 为纯消费者
- 每个测试轮次开始前变更级 agent 重新编译+重启服务
- 所有子变更完成一轮测试+修复后，统一等待变更级 agent 重启服务再进入下一轮
- 服务崩溃恢复和中断恢复统一走变更级 agent
- 新增常见陷阱文档和上下文管理原则

## Capabilities

### New Capabilities
- `playwright-cli-e2e-workflow`: 基于 playwright-cli 的 E2E 测试执行工作流，包含 snapshot+ref 元素定位、决策树、命令与健康评分映射
- `centralized-service-management`: 变更级 agent 统一管理服务生命周期，with_server.py 作为工具，子变更 agent 为纯消费者
- `per-round-service-refresh`: 每轮测试前变更级 agent 重新编译+重启服务，确保环境清洁

### Modified Capabilities
- `service-refresh-gate`: 服务刷新从「编码完成后一次性」改为「每轮测试前执行」。触发条件、频率、职责归属变更
- `subchange-phase-unification`: 子变更测试阶段增加「等待变更级同步」状态，批量推进替代独立推进
- `project-type-detection`: E2E 测试阶段引用 playwright-cli 作为指定浏览器工具

## Impact

- 设计文档: `docs/designs/skills/kflow-e2e-qa.md` → `kflow-e2e-test.md`（重写）
- 核心机制: `docs/designs/core-mechanisms.md`（服务刷新机制从一次性改为轮次级）
- 设计概述: `docs/designs/overview.md`（Skill 名称、流程更新）
- 索引: `docs/designs/index.md`（Skill 名称更新）
- 导航: `docs/designs/skills/index.md`（Skill 名称更新）
- 关联 Skill: `kflow-code`（服务循环引用 with_server.py）、`kflow-integration-test`（服务管理+每轮刷新）
- 工具脚本: 引入 `scripts/with_server.py`
- 已实现 Skills: `.claude/skills/kflow-e2e-qa` → `.claude/skills/kflow-e2e-test`（如有）
