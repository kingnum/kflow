# 阶段钩子执行规范（运行时）

> **版本**: 1.0.0
> **类型**: 运行时共享文件（被各阶段 SKILL.md 引用）
> **创建时间**: 2026-05-28

> **加载层级**: 服务层
> **适用阶段**: api-test/e2e-test/integration-test

本文档是各阶段 PRE_HOOK 和 POST_HOOK 的运行时执行规范。阶段 Skill 的 SKILL.md 在执行流程中通过引用本文档接入钩子机制，不在自身 SKILL.md 中内联复制钩子逻辑。

---

## 一、12 阶段钩子配置表

| 阶段 | 需要服务 | RELOAD 清单 |
|------|:------:|------------|
| explore | ❌ | CONTEXT.md, functional-designs/index.md, module-summary.md(条件), .status.md |
| prototype-design | 🔶 浏览器 | CONTEXT.md, toolchain.md, functional-designs/, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| design | ❌ | CONTEXT.md, functional-designs/, functional-designs/index.md, module-summary.md(条件), docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| plan | ❌ | detailed-design.md, functional-designs/index.md, functional-designs/part-NN.md, module-summary.md(条件), api-tests/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| code | 🔶 编译验证 | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| code-review | ❌ | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| api-test | ✅ 后端 | service-guide.md, api-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| e2e-test | ✅ 前后端 | service-guide.md, e2e-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件,前端SC), prototype-changes.md(条件,前端SC), .status.md |
| integration-test | ✅ 前后端 | service-guide.md, integration-tests/, detailed-design.md, functional-designs/index.md, docs/designs/prototypes/manifest.md(条件), prototype-changes.md(条件), .status.md |
| audit | ❌ | 全量产物, cross-reviews/, test-reports/, .status.md |
| bug-fix | 同触发阶段 | service-guide.md, 相关文档, .status.md |
| archive | ❌ | 全量产物, .status.md |

### 图例

| 图例 | 含义 |
|------|------|
| ❌ | 不需要服务，仅执行 CHECK_STATE + RELOAD |
| 🔶 浏览器 | 需要浏览器进程（Playwright），阶段结束后清理 |
| 🔶 编译验证 | 仅编译验证（不启动持久服务） |
| ✅ 后端 | 需要后端服务持久运行 |
| ✅ 前后端 | 需要前后端服务同时运行 |
| 同触发阶段 | 继承触发阶段的钩子配置 |

### 裁剪阶段的钩子豁免

变更档位为 `轻量` 且某阶段被阶段适用性声明判定为 `⏭️ 不适用` 时，该阶段的钩子 SHALL NOT 执行：

| 阶段 | 裁减时跳过的钩子步骤 | 说明 |
|------|-------------------|------|
| api-test | PRE_HOOK 全部步骤（含 READ_SERVICE_GUIDE/COMPILE/MIGRATE/START_SERVICE/HEALTH_CHECK）与 POST_HOOK 全部步骤 | SHALL NOT 启动服务，SHALL NOT 重启或停止服务 |
| e2e-test | 同上（含 COMPILE_BE/COMPILE_FE/START_FE/HEALTH_FE） | SHALL NOT 启动浏览器进程 |
| integration-test | 同上 | SHALL NOT 执行变更级服务刷新与集成测试收尾 |

> 裁剪阶段的豁免仅适用于上述三个阶段，且 MUST 以变更级 `.status.md` 的阶段适用性声明依据为前提。无声明依据的 `⏭️` SHALL NOT 触发豁免，按门控规则阻塞。裁剪判定见 [gates.md](gates.md) §1.2，声明字段定义见 [state-values.md](state-values.md) §5。
>
> **豁免范围**: PRE_HOOK 与 POST_HOOK 整体跳过，包括 `CHECK_STATE`、`RELOAD`、服务生命周期操作与 `UPDATE_STATE`。阶段状态由 kflow-design 在写入适用性声明时一次性标记为 `⏭️ 不适用`，不由被裁剪阶段自身更新。

---

## 二、PRE_HOOK 执行步骤

### 2.1 不需要服务的阶段（❌）

```
PRE_HOOK（轻量）:
  1. CHECK_STATE → 验证前置阶段状态为 ✅ 完成
  2. RELOAD      → 按 RELOAD 清单重读基础信息文件
```

### 2.2 需要浏览器进程的阶段（🔶 浏览器）

```
PRE_HOOK:
  1. CHECK_STATE         → 验证前置阶段状态为 ✅ 完成
  2. RELOAD              → 按 RELOAD 清单重读文件
  3. PLAYWRIGHT_READY    → 检测 .kflow-runtime/playwright/ 就绪
                            ├── 检测 .kflow-runtime/playwright/node_modules/playwright 是否存在
                            ├── 不存在 → mkdir -p .kflow-runtime/playwright
                            │           && cd .kflow-runtime/playwright
                            │           && npm init -y && npm install playwright
                            │           && npx playwright install chromium
                            └── 已存在 → 跳过安装，直接使用
```

### 2.3 需要编译验证的阶段（🔶 编译验证）

```
PRE_HOOK（编码阶段）:
  1. CHECK_STATE         → 验证前置阶段状态为 ✅ 完成
  2. RELOAD              → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE  → 读取 service-guide.md 获取编译命令
```

### 2.4 需要后端服务的阶段（✅ 后端）

```
PRE_HOOK（API 测试阶段）:
  1. CHECK_STATE         → 验证前置阶段状态为 ✅ 完成
  2. RELOAD              → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE  → 四阶段就绪检测流程:
    PHASE 1: DETECT（检测存在性）
      ├── docs/service-guide.md 存在？
      │   ├── NO  → 进入 PHASE 3（COLLECT）全量收集
      │   └── YES → 进入 PHASE 2（VALIDATE）
    PHASE 2: VALIDATE（验证完整性）
      ├── dev 环境启动命令 ≠ 模板占位符（{命令}、{端口}、{框架名称}）？
      ├── dev 环境端口值实际存在且为有效数字？
      ├── 「服务依赖」章节存在且每项外部服务连接信息完整？
      ├── 配置状态标记 = ✅ 已就绪？
      │   ├── ALL PASS → 直接使用，跳过 PHASE 3
      │   └── FAIL    → 进入 PHASE 3（仅询问缺失项）
    PHASE 3: COLLECT（收集用户输入）
      ├── AskUserQuestion: "检测到以下配置缺失，请提供:"
      │   ├── [缺失项 1] 后端启动命令和端口
      │   ├── [缺失项 2] 数据库连接信息（类型/主机/端口/数据库名）
      │   ├── [缺失项 3] Redis 连接信息（主机/端口）
      │   └── [缺失项 N] ...
      ├── 用户提供信息 → 写入 service-guide.md
      └── 用户选择「稍后配置」→ ❌ 阻塞当前阶段
    PHASE 4: PERSIST（持久化）
      ├── 将用户输入写入 service-guide.md 对应章节
      ├── 记录配置完成标记: > **配置状态**: ✅ 已就绪 ({确认日期})
      ├── 记录检测时间戳: > **上次检测**: {ISO 8601 时间戳}
      └── 后续会话 PHASE 2 检测到标记后自动跳过询问
  4. CHECK_PORTS         → 检测目标端口是否被占用
  5. STOP_STALE          → 停止残留的旧服务进程
  6. COMPILE             → 执行后端编译
  7. MIGRATE             → 执行未执行的数据库迁移脚本
  8. START_SERVICE       → 启动后端服务（skills/kflow-code/scripts/with_server.py --daemon）
  9. HEALTH_CHECK        → /health + /db-health 验证服务就绪
```

### 2.5 需要前后端服务的阶段（✅ 前后端）

```
PRE_HOOK（E2E/集成测试阶段）:
  1. CHECK_STATE         → 验证前置阶段状态为 ✅ 完成
  2. RELOAD              → 按 RELOAD 清单重读文件
  3. READ_SERVICE_GUIDE  → 四阶段就绪检测流程（同 §2.4）:
    PHASE 1 DETECT → PHASE 2 VALIDATE → PHASE 3 COLLECT → PHASE 4 PERSIST
  4. CHECK_PORTS         → 检测前后端目标端口是否被占用
  5. STOP_STALE          → 停止残留的旧服务进程
  6. COMPILE_BE          → 执行后端编译
  7. COMPILE_FE          → 执行前端编译
  8. MIGRATE             → 执行未执行的数据库迁移脚本
  9. START_BE            → 启动后端服务（skills/kflow-code/scripts/with_server.py --daemon）
  10. START_FE           → 启动前端服务（skills/kflow-code/scripts/with_server.py --daemon）
  11. HEALTH_BE          → /health 验证后端就绪
  12. HEALTH_DB          → /db-health 验证数据库就绪
  13. HEALTH_FE          → /health 验证前端就绪
```

### 2.6 PRE_HOOK 阻塞规则

| 子步骤 | 失败后果 |
|--------|---------|
| CHECK_STATE | ❌ 阻塞，提示缺失的前置阶段 |
| RELOAD（文件不存在） | ❌ 阻塞，提示缺失的文件路径 |
| CHECK_PORTS（非预期进程占用） | ⚠️ 阻塞，提示占用信息（端口号、PID、进程名） |
| COMPILE | ❌ 阻塞，修复后重新编译 |
| HEALTH_CHECK | ❌ 阻塞，分析日志定位原因 |

---

## 三、POST_HOOK 执行步骤

### 3.1 不需要服务的阶段（❌）

```
POST_HOOK（轻量）:
  1. UPDATE_STATE → 更新 .status.md（阶段状态、完成时间）
```

### 3.2 需要浏览器进程的阶段（🔶 浏览器）

```
POST_HOOK（原型设计阶段）:
  1. BROWSER_CLEANUP → 从项目根目录执行 playwright-cli kill-all 清理浏览器进程
                       并清理 docs/designs/prototypes/ 下残留的 node_modules/、package.json、package-lock.json
                       SHALL NOT 在 docs/designs/prototypes/ 目录下产生残留文件
  2. UPDATE_STATE    → 更新 .status.md
```

> **条件性**：Playwright 验证仅在审查方式为「子代理自动审查验证」时执行，因此 BROWSER_CLEANUP 的浏览器进程清理只在需要时产生实际作用；残留产物清理与 UPDATE_STATE 无条件执行。审查方式记录字段见 [state-values.md](state-values.md) §3。

### 3.3 需要编译验证的阶段（🔶 编译验证）

```
POST_HOOK（编码阶段）:
  1. UPDATE_STATE → 更新 .status.md
```

### 3.4 需要服务的阶段（✅ 后端 / ✅ 前后端）

```
POST_HOOK（测试阶段）:
  1. STOP_SERVICE        → 停止所有运行中的服务（skills/kflow-code/scripts/with_server.py --stop-all）
  2. VERIFY_STOP         → 验证所有服务端口已释放
  3. BROWSER_CLEANUP     → 从项目根目录执行 playwright-cli kill-all（如有浏览器进程）
                            SHALL NOT 在 docs/designs/prototypes/ 目录下产生残留文件
  4. UPDATE_STATE        → 更新 .status.md
  5. UPDATE_SERVICE_STATE → 更新/清理 .service-state.json
```

### 3.5 POST_HOOK 阻塞规则

| 子步骤 | 失败后果 |
|--------|---------|
| STOP_SERVICE 超时（SIGTERM 30s + SIGKILL 10s） | ❌ 阻塞，提示僵尸进程信息 |
| VERIFY_STOP 端口未释放 | ❌ 阻塞 |

---

## 四、RELOAD 清单详情

### 4.1 各阶段 RELOAD 文件列表

| 阶段 | 必须重读文件 | 条件重读文件 |
|------|------------|------------|
| explore | CONTEXT.md, functional-designs/index.md, .status.md | module-summary.md（如存在） |
| prototype-design | CONTEXT.md, toolchain.md, functional-designs/, .status.md | docs/designs/prototypes/manifest.md（如存在），prototype-changes.md（如存在） |
| design | CONTEXT.md, functional-designs/, functional-designs/index.md, .status.md | module-summary.md（如存在），docs/designs/prototypes/manifest.md（如存在），prototype-changes.md（如存在） |
| plan | detailed-design.md, functional-designs/index.md, functional-designs/part-NN.md, api-tests/index.md, .status.md | module-summary.md（如存在），docs/designs/prototypes/manifest.md（条件，前端SC），prototype-changes.md（条件，前端SC） |
| code | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, .status.md | docs/designs/prototypes/manifest.md（条件，前端SC），prototype-changes.md（条件，前端SC） |
| code-review | service-guide.md, CONTEXT.md, detailed-design.md, functional-designs/index.md, .status.md | docs/designs/prototypes/manifest.md（条件，前端SC），prototype-changes.md（条件，前端SC） |
| api-test | service-guide.md, api-tests/, detailed-design.md, functional-designs/index.md, .status.md | docs/designs/prototypes/manifest.md（如存在），prototype-changes.md（如存在） |
| e2e-test | service-guide.md, e2e-tests/, detailed-design.md, functional-designs/index.md, .status.md | docs/designs/prototypes/manifest.md（条件，前端SC），prototype-changes.md（条件，前端SC） |
| integration-test | service-guide.md, integration-tests/, detailed-design.md, functional-designs/index.md, .status.md | docs/designs/prototypes/manifest.md（如存在），prototype-changes.md（如存在） |
| audit | 全量产物, cross-reviews/, test-reports/, .status.md | — |
| bug-fix | service-guide.md, 失败测试报告, 相关设计文档, .status.md | — |
| archive | 全量产物, .status.md | — |

### 4.2 RELOAD 执行规则

1. 仅重读 RELOAD 清单中列出的文件
2. 文件 mtime 未变化且已在当前会话中读取过，可跳过重读
3. 文件 mtime 发生变化或首次读取时 SHALL 完整重读
4. RELOAD 清单中文件不存在时 ❌ 阻塞，不继续执行

### 4.3 RELOAD 增量模式

子代理是全新上下文，每次冷启动必须完整重读所有 RELOAD 文件。对于大型变更（detailed-design.md 多文件、functional-designs/ 多文件），RELOAD 的 Token 开销显著。增量模式允许主 Agent 为已读取且未变化的文件生成"已验证标记"，子代理收到标记后可跳过完整读取。

#### 4.3.1 已验证文件标记格式

主 Agent 在子代理 prompt 中注入以下格式的标记块：

```markdown
## RELOAD 已验证文件 (mtime 未变, 本会话已读取)
以下文件自上次读取后未发生变化，你可以信任主 Agent 提供的摘要信息：
- CONTEXT.md (术语表): {2 行摘要}
- functional-designs/index.md: {1 行摘要}
- detailed-design.md: {3 行摘要, 仅当前子变更相关域}
```

每条标记包含：
- **文件路径**：RELOAD 清单中的文件路径
- **文件角色**：括号内标注文件用途（如"术语表"）
- **摘要信息**：1-3 行关键内容摘要，足以覆盖子代理常规引用需求

#### 4.3.2 主 Agent 生成标记的时机和规则

| 规则 | 说明 |
|------|------|
| 生成时机 | 每次调度子代理前，对 RELOAD 清单中的文件逐一检查 |
| mtime 检查 | 文件 mtime 未变化且主 Agent 在当前会话中已读取过该文件时，方可生成标记 |
| 摘要生成 | 主 Agent 从已读取的文件内容中提取 1-3 行关键摘要写入标记 |
| mtime 已变 | 文件 mtime 发生变化时 SHALL 不生成标记，子代理须完整重读 |
| 首次读取 | 主 Agent 在当前会话中未读取过的文件 SHALL 不生成标记 |
| 标记有效期 | 仅在当前子代理调用内有效，下一个子代理调用时须重新检测 mtime |

#### 4.3.3 子代理收到标记后的行为规则

| 规则 | 说明 |
|------|------|
| 跳过完整读取 | 收到已验证标记的文件，子代理 SHALL NOT 重新完整读取 |
| 使用摘要 | 引用标记文件内容时，使用主 Agent 提供的摘要信息 |
| 保留自行读取权 | 执行过程中如发现摘要信息不足（超出摘要范围），子代理 SHALL 自行读取完整文件 |
| 标记不可传递 | 子代理不得将标记转发给其他子代理或假设标记在其他上下文中有效 |

---

## 五、服务生命周期操作步骤

服务生命周期具体操作指令定义在 `skills/kflow-e2e-test/references/service-lifecycle.md` 中。本文档仅列出各阶段各服务类型需要执行的操作步骤。执行时参考 `service-lifecycle.md` 获取每条指令的具体调用方式。

### 5.1 各服务类型操作映射

| 操作 | ❌ 不需要服务 | 🔶 编译验证 | ✅ 后端 | ✅ 前后端 |
|------|:---------:|:--------:|:-----:|:------:|
| CHECK_STATE | ✅ | ✅ | ✅ | ✅ |
| RELOAD | ✅ | ✅ | ✅ | ✅ |
| CHECK_PORTS | — | — | ✅ | ✅ |
| STOP_STALE | — | — | ✅ | ✅ |
| COMPILE | — | ✅（仅编译） | ✅ | ✅（前后端） |
| MIGRATE | — | — | ✅ | ✅ |
| START_SERVICE | — | — | ✅（后端） | ✅（前后端） |
| HEALTH_CHECK | — | — | ✅（/health, /db-health） | ✅（/health BE+FE, /db-health） |
| STOP_SERVICE | — | — | ✅ | ✅ |
| VERIFY_STOP | — | — | ✅ | ✅ |
| BROWSER_CLEANUP | — | 🔶（如有） | — | ✅（如有） |
| UPDATE_STATE | ✅ | ✅ | ✅ | ✅ |
