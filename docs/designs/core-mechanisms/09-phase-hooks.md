# 阶段钩子与服务生命周期

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-05-28
> **父文档**: [index.md](index.md)

> **加载层级**: 服务层
> **适用阶段**: api-test/e2e-test/integration-test

本文档定义 KFlow Skills 体系中各阶段的 PRE_HOOK（前置钩子）和 POST_HOOK（后置钩子）标准化执行规范，包括钩子配置表、RELOAD 清单、服务生命周期规则和服务停止超时链。

---

## 一、钩子架构概述

每个阶段 Skill 在执行核心流程前后，由变更级 agent 执行标准化的 PRE_HOOK 和 POST_HOOK 步骤。钩子的具体执行规范定义在 `.claude/skills/各 skill 的 references/hooks.md`（运行时共享文件）中，各阶段 SKILL.md 通过引用该文件接入钩子机制，不在自身 SKILL.md 中内联复制钩子逻辑。

```
阶段执行流程:

  PRE_HOOK                      CORE_WORKFLOW                    POST_HOOK
  ┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
  │ 1. CHECK_STATE    │    │ 阶段核心执行逻辑       │    │ 1. STOP_SERVICE   │
  │ 2. RELOAD         │───▶│ (各阶段差异化)         │───▶│ 2. VERIFY_STOP    │
  │ 3. CHECK_PORTS    │    │                      │    │ 3. BROWSER_CLEANUP│
  │ 4. STOP_STALE     │    │                      │    │ 4. UPDATE_STATE   │
  │ 5. START_SERVICE  │    │                      │    │ 5. UPDATE_SERVICE │
  │ 6. HEALTH_CHECK   │    │                      │    │                   │
  └──────────────────┘    └──────────────────────┘    └──────────────────┘
```

### 1.1 钩子职责归属

钩子执行职责完全归属于变更级 agent。子变更 agent 不执行任何钩子步骤。

### 1.2 钩子共享引用机制

各阶段 SKILL.md 在执行流程章节中通过引用 `各 skill 的 references/hooks.md` 接入钩子，格式为：

```markdown
## 执行流程

### PRE_HOOK
引用 `各 skill 的 references/hooks.md` 中 [阶段名] 的 PRE_HOOK 节。

### 核心流程
...

### POST_HOOK
引用 `各 skill 的 references/hooks.md` 中 [阶段名] 的 POST_HOOK 节。
```

---

## 二、钩子配置表

### 2.1 12 阶段钩子配置

| 阶段 | 需要服务 | RELOAD 清单 |
|------|:------:|------------|
| explore | ❌ | CONTEXT.md, functional-designs/index.md, module-summary.md(条件), .status.md |
| prototype-design | 🔶 浏览器 | CONTEXT.md, toolchain.md, functional-designs/, prototype/index.md, .status.md |
| design | ❌ | CONTEXT.md, functional-designs/, functional-designs/index.md, module-summary.md(条件), prototype/index.md(条件), .status.md |
| plan | ❌ | detailed-design.md, functional-designs/index.md, module-summary.md(条件), prototype/index.md(条件), .status.md |
| code | 🔶 编译验证 | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, prototype/index.md(条件), .status.md |
| code-review | ❌ | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, prototype/index.md(条件), .status.md |
| api-test | ✅ 后端 | service-guide.md, api-tests/, detailed-design.md, functional-designs/index.md, prototype/index.md(条件), .status.md |
| e2e-test | ✅ 前后端 | service-guide.md, e2e-tests/, detailed-design.md, functional-designs/index.md, prototype/index.md(条件), prototype/(条件), .status.md |
| integration-test | ✅ 前后端 | service-guide.md, integration-tests/, detailed-design.md, functional-designs/index.md, prototype/index.md(条件), .status.md |
| audit | ❌ | 全量产物, cross-reviews/, test-reports/, .status.md |
| bug-fix | 同触发阶段 | service-guide.md, 相关文档, .status.md |
| archive | ❌ | 全量产物, .status.md |

### 2.2 服务需求图例

| 图例 | 含义 | 说明 |
|------|------|------|
| ❌ | 不需要服务 | 仅执行 RELOAD + CHECK_STATE |
| 🔶 浏览器 | 需要浏览器进程 | 原型设计阶段使用 Playwright 浏览器，阶段结束后清理 |
| 🔶 编译验证 | 仅编译验证 | 编码阶段末尾验证代码可编译，不启动持久服务 |
| ✅ 后端 | 需要后端服务 | 测试阶段需要持久运行的后端服务 |
| ✅ 前后端 | 需要前后端服务 | E2E/集成测试阶段需要前后端服务同时运行 |
| 同触发阶段 | 继承触发阶段的配置 | bug-fix 阶段继承触发它的测试阶段的钩子配置 |

---

## 三、PRE_HOOK 规范

### 3.1 PRE_HOOK 步骤序列

#### 不需要服务的阶段（❌）

```
PRE_HOOK（轻量）:
  1. CHECK_STATE → 验证前置阶段状态为 ✅ 完成
  2. RELOAD      → 按 RELOAD 清单重读基础信息文件
```

#### 需要浏览器进程的阶段（🔶 浏览器）

```
PRE_HOOK:
  1. CHECK_STATE → 验证前置阶段状态为 ✅ 完成
  2. RELOAD      → 按 RELOAD 清单重读文件
```

#### 需要编译验证的阶段（🔶 编译验证）

```
PRE_HOOK（编码阶段）:
  1. CHECK_STATE    → 验证前置阶段状态为 ✅ 完成
  2. RELOAD         → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE → 读取 service-guide.md 获取编译命令
```

#### 需要后端服务的阶段（✅ 后端）

```
PRE_HOOK（API 测试阶段）:
  1. CHECK_STATE        → 验证前置阶段状态为 ✅ 完成
  2. RELOAD             → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE → 读取 service-guide.md 获取启动命令和端口
  4. CHECK_PORTS        → 检测目标端口是否被占用
  5. STOP_STALE         → 停止残留的旧服务进程
  6. COMPILE            → 执行后端编译
  7. MIGRATE            → 执行未执行的数据库迁移脚本
  8. START_SERVICE      → 启动后端服务（with_server.py --daemon）
  9. HEALTH_CHECK       → /health + /db-health 验证服务就绪
```

#### 需要前后端服务的阶段（✅ 前后端）

```
PRE_HOOK（E2E/集成测试阶段）:
  1. CHECK_STATE        → 验证前置阶段状态为 ✅ 完成
  2. RELOAD             → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE → 读取 service-guide.md 获取启动命令和端口
  4. CHECK_PORTS        → 检测前后端目标端口是否被占用
  5. STOP_STALE         → 停止残留的旧服务进程
  6. COMPILE_BE         → 执行后端编译
  7. COMPILE_FE         → 执行前端编译
  8. MIGRATE            → 执行未执行的数据库迁移脚本
  9. START_BE           → 启动后端服务（with_server.py --daemon）
  10. START_FE          → 启动前端服务（with_server.py --daemon）
  11. HEALTH_BE         → /health 验证后端就绪
  12. HEALTH_DB         → /db-health 验证数据库就绪
  13. HEALTH_FE         → /health 验证前端就绪
```

### 3.2 PRE_HOOK 阻塞规则

任一子步骤失败 SHALL 阻塞当前阶段：
- CHECK_STATE 失败 → ❌ 阻塞，提示缺失的前置阶段
- RELOAD 文件不存在 → ❌ 阻塞，提示缺失的文件路径
- CHECK_PORTS 被非预期进程占用 → ⚠️ 阻塞，提示占用信息
- COMPILE 失败 → ❌ 阻塞，修复后重新编译
- HEALTH_CHECK 失败 → ❌ 阻塞，分析日志定位原因

---

## 四、POST_HOOK 规范

### 4.1 POST_HOOK 步骤序列

#### 不需要服务的阶段（❌）

```
POST_HOOK（轻量）:
  1. UPDATE_STATE → 更新 .status.md（阶段状态、完成时间）
```

#### 需要浏览器进程的阶段（🔶 浏览器）

```
POST_HOOK（原型设计阶段）:
  1. BROWSER_CLEANUP → playwright-cli kill-all 清理浏览器进程
  2. UPDATE_STATE    → 更新 .status.md
```

#### 需要编译验证的阶段（🔶 编译验证）

```
POST_HOOK（编码阶段）:
  1. UPDATE_STATE → 更新 .status.md（编码完成，释放代码审查门控）
```

#### 需要服务的阶段（✅ 后端 / ✅ 前后端）

```
POST_HOOK（测试阶段）:
  1. STOP_SERVICE       → 停止所有运行中的服务（with_server.py --stop-all）
  2. VERIFY_STOP         → 验证所有服务端口已释放
  3. BROWSER_CLEANUP     → playwright-cli kill-all（如有浏览器进程）
  4. UPDATE_STATE        → 更新 .status.md
  5. UPDATE_SERVICE_STATE → 更新/清理 .service-state.json
```

### 4.2 POST_HOOK 阻塞规则

- STOP_SERVICE 超时（SIGTERM 30s + SIGKILL 10s 后端口仍占用）→ ❌ 阻塞，提示僵尸进程信息
- VERIFY_STOP 端口未释放 → ❌ 阻塞

---

## 五、RELOAD 机制

### 5.1 RELOAD 目的

RELOAD 步骤确保阶段执行基于最新的文件内容，不使用对话上下文缓存中的旧版本。

### 5.2 RELOAD 执行规则

| 规则 | 说明 |
|------|------|
| 按清单重读 | 仅重读钩子配置表中该阶段定义的 RELOAD 清单文件 |
| mtime 判断 | 文件 mtime 未变化且已在当前会话中读取过，可跳过重读 |
| 不得跳过 | mtime 发生变化或首次读取时 SHALL 完整重读 |
| 不存在时阻塞 | RELOAD 清单中文件不存在时 ❌ 阻塞，不继续执行 |
| 增量模式 | 子代理可通过"已验证文件标记"跳过完整读取（见 §5.4） |

### 5.3 各阶段 RELOAD 重点

| 阶段 | RELOAD 重点 |
|------|-----------|
| explore | 重读 CONTEXT.md 进行术语对齐，重读 functional-designs/ 了解功能上下文，条件加载 module-summary.md 获取模块概况 |
| prototype-design | 重读 CONTEXT.md 和 toolchain.md，确认工具链锁定方案，重读 prototype/index.md 获取原型索引 |
| design | 重读 CONTEXT.md 确保术语一致性，重读 functional-designs/index.md 获取最新修订记录，条件加载 module-summary.md 获取模块概况，条件读取 prototype/index.md 作为设计参考 |
| plan | 重读 detailed-design.md（仅提取当前子变更相关的设计域章节），重读 functional-designs/index.md 和 module-summary.md（条件）获取最新修订和模块概况，重读 prototype/index.md（条件）获取最新修订 |
| code | 重读 service-guide.md 获取编译命令，重读 detailed-design.md 确认接口和数据模型，重读 functional-designs/index.md 和 prototype/index.md（条件）检查设计修订 |
| code-review | 重读 service-guide.md 检查配置安全性，重读 detailed-design.md 对照检查，重读 functional-designs/index.md 和 prototype/index.md（条件）获取最新设计 |
| api-test | 重读 service-guide.md 获取端口和启动命令，重读 api-tests/ 和 detailed-design.md，重读 functional-designs/index.md 和 prototype/index.md（条件） |
| e2e-test | 重读 service-guide.md 获取前后端端口，重读 e2e-tests/，重读 functional-designs/index.md 和 prototype/index.md（条件），条件读取 prototype/ |
| integration-test | 重读 service-guide.md 确认服务配置，重读 integration-tests/ 和 detailed-design.md，重读 functional-designs/index.md 和 prototype/index.md（条件） |
| audit | 重读全量产物进行完整性审计，重读 cross-reviews/ 和 test-reports/ |
| bug-fix | 重读 service-guide.md 获取当前环境配置，重读失败测试报告和相关设计文档 |
| archive | 重读全量产物确认所有门控已通过，重读 .status.md 确认阶段状态 |

### 5.4 RELOAD 增量模式

子代理是全新上下文，每次冷启动必须完整重读所有 RELOAD 文件。对于大型变更（detailed-design.md 多文件、functional-designs/ 多文件），RELOAD 的 Token 开销显著。增量模式允许主 Agent 为已读取且未变化的文件生成"已验证标记"，子代理收到标记后可跳过完整读取，预估收益 Token 减少 40-60%。

#### 5.4.1 已验证文件标记格式

主 Agent 在子代理 prompt 中注入标记块：

```markdown
## RELOAD 已验证文件 (mtime 未变, 本会话已读取)
以下文件自上次读取后未发生变化，你可以信任主 Agent 提供的摘要信息：
- CONTEXT.md (术语表): {2 行摘要}
- functional-designs/index.md: {1 行摘要}
- detailed-design.md: {3 行摘要, 仅当前子变更相关域}
```

每条标记包含：文件路径、文件角色（括号标注用途）、1-3 行关键内容摘要。

#### 5.4.2 主 Agent 生成标记规则

| 规则 | 说明 |
|------|------|
| 生成时机 | 每次调度子代理前，对 RELOAD 清单中的文件逐一检查 |
| mtime 检查 | 文件 mtime 未变化且主 Agent 在当前会话中已读取过该文件时，方可生成标记 |
| mtime 已变 | 文件 mtime 发生变化时 SHALL 不生成标记，子代理须完整重读 |
| 首次读取 | 主 Agent 在当前会话中未读取过的文件 SHALL 不生成标记 |
| 标记有效期 | 仅在当前子代理调用内有效，下一个子代理调用时须重新检测 mtime |

#### 5.4.3 子代理行为规则

| 规则 | 说明 |
|------|------|
| 跳过完整读取 | 收到已验证标记的文件，子代理 SHALL NOT 重新完整读取 |
| 使用摘要 | 引用标记文件内容时，使用主 Agent 提供的摘要信息 |
| 保留自行读取权 | 执行过程中如发现摘要信息不足，子代理 SHALL 自行读取完整文件 |
| 标记不可传递 | 子代理不得将标记转发给其他子代理 |

---

## 六、服务生命周期规则

### 6.1 服务启动规则

| 规则 | 说明 |
|------|------|
| 配置来源 | 启动命令和端口 SHALL 从 `docs/service-guide.md` dev 环境读取，不得自行推断 |
| 端口冲突检测 | 启动前 SHALL 检测目标端口是否被占用 |
| 持久化模式 | 测试阶段使用 `with_server.py --daemon` 持久化模式 |
| 状态追踪 | 服务信息写入 `.service-state.json`（PID、端口、启动时间、健康状态） |
| 就绪检测 | 轮询 localhost:{port} 直到端口可连接，超时 60s（daemon 模式） |
| 健康检查 | 启动后执行 /health 端点验证，测试阶段额外执行 /db-health |

### 6.2 服务停止规则

| 规则 | 说明 |
|------|------|
| 停止时机 | 测试阶段每轮完成后 SHALL 停止服务 |
| 停止方式 | 使用 `with_server.py --stop-all --state-file {path}` |
| 超时机制 | 见 §七「服务停止超时链」 |
| 端口验证 | 停止后 SHALL 验证所有服务端口已释放 |
| 状态清理 | 所有服务停止后删除 `.service-state.json` |

### 6.3 编译验证规则（编码阶段专用）

| 规则 | 说明 |
|------|------|
| 编译时机 | 所有子代理完成编码后执行一次性编译验证 |
| 编译内容 | 仅编译验证（如 `mvn compile`、`npm run build`），不启动服务 |
| 不含服务 | 编译验证 SHALL NOT 包含服务启动、数据库迁移、健康检查 |
| 失败阻塞 | 编译失败 → ❌ 阻塞编码阶段，修复后重新编译 |

### 6.4 服务刷新规则（测试阶段专用）

| 规则 | 说明 |
|------|------|
| 刷新时机 | 每轮测试开始前执行完整服务刷新 |
| 刷新流程 | STOP → COMPILE → MIGRATE → START → HEALTH_CHECK |
| 每轮停止 | 每轮测试完成后 SHALL 停止所有服务 |
| 全部通过 | 所有测试通过后 SHALL 停止服务，不执行下一轮刷新 |

---

## 七、服务停止超时链

### 7.1 超时链定义

服务停止采用强制终止链，由 `with_server.py --stop-all` 执行：

```
服务停止超时链:

  1. SIGTERM → 发送优雅终止信号
     └── 等待最多 30 秒
         ├── 进程终止 → ✅ 停止成功
         └── 进程未终止 → 进入步骤 2

  2. SIGKILL → 发送强制终止信号
     └── 等待最多 10 秒
         ├── 进程终止 → ⚠️ 停止成功（强制终止）
         └── 进程未终止 → 进入步骤 3

  3. ERROR → ❌ 阻塞
     └── 提示僵尸进程信息（PID、端口、进程名称）
     └── 建议用户手动处理
```

### 7.2 超时链设计决策

| 决策 | 理由 |
|------|------|
| SIGTERM 优先于 SIGKILL | 给服务执行优雅关闭的机会（释放连接池、刷新缓冲区） |
| 30s 等待时间 | 覆盖绝大多数正常关闭场景（数据库连接关闭、事务回滚） |
| SIGKILL 兜底 | 处理无响应的僵尸进程 |
| 10s SIGKILL 后的最终阻塞 | 极端情况（内核态挂起）需要人工介入，不自动反复重试 |

---

## 八、端口冲突检测

### 8.1 检测时机

服务启动前（PRE_HOOK 的 CHECK_PORTS 步骤）执行端口冲突检测。

### 8.2 检测规则

| 场景 | 处理方式 |
|------|---------|
| 端口空闲 | 正常启动服务 |
| 端口被当前变更管理的残留服务占用 | 先执行 STOP_STALE 停止残留进程 |
| 端口被非预期进程占用 | ⚠️ 阻塞，提示占用信息（端口号、PID、进程名称），不自动 kill |

### 8.3 端口配置来源

端口 SHALL 从 `docs/service-guide.md` dev 环境配置中读取，不得自行推断或从其他来源获取。

---

## 九、浏览器进程管理

### 9.1 浏览器生命周期

| 阶段 | 浏览器使用 | 清理规则 |
|------|----------|---------|
| prototype-design | VERIFY 步骤使用 Playwright | POST_HOOK 执行 `playwright-cli kill-all` |
| e2e-test | 整个测试过程使用 Playwright | POST_HOOK 执行 `playwright-cli kill-all` |
| integration-test | 前后端项目使用浏览器 | POST_HOOK 执行 `playwright-cli kill-all` |

### 9.2 浏览器清理命令

```bash
# 清理所有残留浏览器进程
playwright-cli kill-all
```

---

## 十、与共享文件的关系

### 10.1 共享文件架构

```
.claude/skills/skills/<skill>/references/
├── phase-hooks.md        # PRE_HOOK/POST_HOOK 执行规范（运行时）
└── service-lifecycle.md  # 服务启动/停止/健康检查的具体操作指令（运行时）
```

- `phase-hooks.md`：包含 12 阶段钩子配置表、RELOAD 清单、服务生命周期操作步骤
- `service-lifecycle.md`：包含 `with_server.py` 调用规范、端口冲突检测命令、服务停止超时链的具体操作

### 10.2 设计文档与运行时文件的关系

本文档（`09-phase-hooks.md`）定义设计规范，`.claude/skills/skills/<skill>/references/` 下的文件为运行时执行文件。设计文档变更时应同步更新运行时文件。

---

## 十一、违反钩子规范的后果

| 违反项 | 后果 |
|--------|------|
| SKILL.md 缺失 PRE_HOOK 引用 | 审计阶段判定为不合规 |
| SKILL.md 缺失 POST_HOOK 引用 | 审计阶段判定为不合规 |
| SKILL.md 内联复制钩子逻辑 | 维护一致性风险，审计阶段建议修改 |
| PRE_HOOK 中服务启动失败后继续执行 | 后续步骤依赖服务时全部失败 |
| POST_HOOK 未停止服务 | 进程残留堆积，端口持续被占用 |
