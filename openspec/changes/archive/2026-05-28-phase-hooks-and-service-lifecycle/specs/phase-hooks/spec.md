## ADDED Requirements

### Requirement: 阶段前置钩子 PRE_HOOK

每个阶段 Skill 在执行核心流程前，SHALL 执行 PRE_HOOK 步骤。PRE_HOOK 由变更级 agent 执行，内容包括：重读基础信息文件（RELOAD）、验证前置阶段状态（CHECK_STATE）、以及需要服务时执行端口检查和可用性验证。

#### Scenario: 所有阶段执行 RELOAD

- **WHEN** 任何阶段 Skill 被调用并进入执行流程
- **THEN** 变更级 agent SHALL 在核心流程前执行 RELOAD 步骤
- **AND** RELOAD 步骤 SHALL 读取本阶段在钩子配置表中定义的 RELOAD 清单文件
- **AND** RELOAD 步骤 SHALL 以文件 mtime 判断是否需要重新读取，仅在文件已变更或未缓存时重读

#### Scenario: 需要服务的阶段执行服务 PRE_HOOK

- **WHEN** 阶段在钩子配置表中标记为"需要服务"
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中依次执行：READ_SERVICE_GUIDE → CHECK_PORTS → STOP_STALE → START_SERVICE → HEALTH_CHECK
- **AND** 任一子步骤失败 SHALL 阻塞当前阶段

#### Scenario: 不需要服务的阶段跳过服务 PRE_HOOK

- **WHEN** 阶段在钩子配置表中标记为"不需要服务"
- **THEN** 变更级 agent SHALL 仅执行 RELOAD 和 CHECK_STATE
- **AND** SHALL NOT 执行服务启动相关步骤

### Requirement: 阶段后置钩子 POST_HOOK

每个阶段 Skill 在执行核心流程完毕后，SHALL 执行 POST_HOOK 步骤。POST_HOOK 由变更级 agent 执行，内容包括：停止服务（如需）、清理浏览器进程、更新状态文件。

#### Scenario: 需要服务的阶段执行服务 POST_HOOK

- **WHEN** 阶段在钩子配置表中标记为"需要服务"且阶段核心流程执行完毕
- **THEN** 变更级 agent SHALL 在 POST_HOOK 中依次执行：STOP_SERVICE → VERIFY_STOP → BROWSER_CLEANUP（如有浏览器进程）→ UPDATE_STATE → UPDATE_SERVICE_STATE
- **AND** STOP_SERVICE SHALL 发送 SIGTERM 后等待最多 30s，未终止则发送 SIGKILL，再等待 10s 仍占用则报错阻塞

#### Scenario: 不需要服务的阶段执行轻量 POST_HOOK

- **WHEN** 阶段在钩子配置表中标记为"不需要服务"且阶段核心流程执行完毕
- **THEN** 变更级 agent SHALL 仅执行 UPDATE_STATE
- **AND** SHALL NOT 执行服务停止相关步骤

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

### Requirement: 阶段 Skill 引用共享钩子文件

每个阶段 Skill 的 SKILL.md SHALL 在其执行流程中引用 `.claude/skills/kflow-shared/phase-hooks.md` 作为 PRE_HOOK 和 POST_HOOK 的执行规范。

#### Scenario: SKILL.md 包含钩子引用

- **WHEN** 阶段 Skill 的 SKILL.md 被编写或更新
- **THEN** SKILL.md 的"执行流程"章节 SHALL 包含明确的 PRE_HOOK 和 POST_HOOK 步骤
- **AND** PRE_HOOK 步骤 SHALL 引用 `kflow-shared/phase-hooks.md` 中对应阶段的节
- **AND** POST_HOOK 步骤 SHALL 引用 `kflow-shared/phase-hooks.md` 中对应阶段的节
- **AND** SHALL NOT 在 SKILL.md 中内联复制钩子的具体执行步骤

#### Scenario: 审计检查钩子引用

- **WHEN** 阶段 Skill 的 SKILL.md 被审查
- **THEN** 审查者 SHALL 检查执行流程中是否包含对 `kflow-shared/phase-hooks.md` 的引用
- **AND** 缺失 PRE_HOOK 或 POST_HOOK 引用 SHALL 判定为不合规
