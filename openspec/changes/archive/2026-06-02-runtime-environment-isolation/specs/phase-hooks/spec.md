# phase-hooks Specification (Delta)

## MODIFIED Requirements

### Requirement: 阶段前置钩子 PRE_HOOK

每个阶段 Skill 在执行核心流程前，SHALL 执行 PRE_HOOK 步骤。PRE_HOOK 由变更级 agent 执行，内容包括：重读基础信息文件（RELOAD）、验证前置阶段状态（CHECK_STATE）、需要服务时执行 service-guide.md 就绪检测和端口检查与可用性验证、需要浏览器时确保 `.kflow-runtime/playwright/` 就绪。

#### Scenario: 所有阶段执行 RELOAD

- **WHEN** 任何阶段 Skill 被调用并进入执行流程
- **THEN** 变更级 agent SHALL 在核心流程前执行 RELOAD 步骤
- **AND** RELOAD 步骤 SHALL 读取本阶段在钩子配置表中定义的 RELOAD 清单文件
- **AND** RELOAD 步骤 SHALL 以文件 mtime 判断是否需要重新读取，仅在文件已变更或未缓存时重读

#### Scenario: 需要服务的阶段执行服务 PRE_HOOK

- **WHEN** 阶段在钩子配置表中标记为"需要服务"
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中依次执行：READ_SERVICE_GUIDE（含就绪检测）→ CHECK_PORTS → STOP_STALE → START_SERVICE → HEALTH_CHECK
- **AND** READ_SERVICE_GUIDE 子步骤 SHALL 检测 service-guide.md 存在性、内容完整性、外部服务依赖连接信息，缺失时通过 AskUserQuestion 收集并持久化
- **AND** 任一子步骤失败 SHALL 阻塞当前阶段

#### Scenario: 需要浏览器的阶段执行浏览器 PRE_HOOK

- **WHEN** 阶段在钩子配置表中标记为"🔶 浏览器"
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中检测 `.kflow-runtime/playwright/` 是否就绪
- **AND** 若未就绪，SHALL 在 `.kflow-runtime/playwright/` 下执行 `npm install playwright` 和浏览器二进制安装
- **AND** 确保后续 `/playwright-cli` 调用使用该安装路径

### Requirement: 阶段后置钩子 POST_HOOK

每个阶段 Skill 在执行核心流程完毕后，SHALL 执行 POST_HOOK 步骤。POST_HOOK 由变更级 agent 执行，内容包括：停止服务（如需）、清理浏览器进程、更新状态文件。

#### Scenario: 需要服务的阶段执行服务 POST_HOOK

- **WHEN** 阶段在钩子配置表中标记为"需要服务"且阶段核心流程执行完毕
- **THEN** 变更级 agent SHALL 在 POST_HOOK 中依次执行：STOP_SERVICE → VERIFY_STOP → BROWSER_CLEANUP（如有浏览器进程）→ UPDATE_STATE → UPDATE_SERVICE_STATE
- **AND** STOP_SERVICE SHALL 发送 SIGTERM 后等待最多 30s，未终止则发送 SIGKILL，再等待 10s 仍占用则报错阻塞

#### Scenario: 浏览器清理从项目根目录执行

- **WHEN** POST_HOOK 或阶段结束执行 BROWSER_CLEANUP
- **THEN** `playwright-cli kill-all` SHALL 从项目根目录执行
- **AND** SHALL NOT 在 `prototype/` 或其他设计文档目录下产生残留文件

### Requirement: 钩子配置表

系统 SHALL 维护一张钩子配置表，定义每个阶段的"需要服务"属性和"RELOAD 清单"。

#### Scenario: 各阶段钩子配置

- **WHEN** 查询钩子配置表
- **THEN** 各阶段配置 SHALL 如下：

| 阶段 | 需要服务 | RELOAD 清单 |
|------|:------:|------------|
| explore | ❌ | CONTEXT.md, functional-designs/index.md, .status.md |
| prototype-design | 🔶 浏览器 | CONTEXT.md, toolchain.md, functional-designs/, .status.md |
| design | ❌ | CONTEXT.md, functional-designs/, prototype/(条件), .status.md |
| plan | ❌ | detailed-design.md, .status.md |
| code | 🔶 编译验证 | service-guide.md, CONTEXT.md, detailed-design.md, .status.md |
| code-review | ❌ | service-guide.md, CONTEXT.md, detailed-design.md, .status.md |
| api-test | ✅ 后端 | service-guide.md, api-tests/, detailed-design.md, .status.md |
| e2e-test | ✅ 前后端 | service-guide.md, e2e-tests/, detailed-design.md, prototype/(条件), .status.md |
| integration-test | ✅ 前后端 | service-guide.md, integration-tests/, detailed-design.md, .status.md |
| audit | ❌ | 全量产物, cross-reviews/, test-reports/, .status.md |
| bug-fix | 同触发阶段 | service-guide.md, 相关文档, .status.md |
| archive | ❌ | 全量产物, .status.md |
