# 服务生命周期操作指令（运行时）

> **版本**: 1.0.0
> **类型**: 运行时共享文件（被 `skills/kflow-e2e-test/references/hooks.md` 引用）
> **创建时间**: 2026-05-28

> **加载层级**: 服务层
> **适用阶段**: api-test/e2e-test/integration-test

本文档定义服务启动、停止、健康检查等生命周期操作的具体调用指令，供各阶段 PRE_HOOK 和 POST_HOOK 执行时参考。

---

## 一、with_server.py 调用规范

### 1.1 双模式概述

`skills/kflow-code/scripts/with_server.py` 支持两种运行模式：

| 模式 | 适用阶段 | 服务生命周期 | 进程管理 |
|------|---------|------------|---------|
| **One-shot** | 手动调试、一次性任务 | 命令执行期间 | 命令结束自动清理 |
| **Daemon** | 测试阶段（api/e2e/integration） | 跨多轮测试持久运行 | 显式 `--stop-all` 停止 |

### 1.2 One-shot 模式（原有模式）

```bash
# 基本用法：在服务运行期间执行命令
python skills/kflow-code/scripts/with_server.py --command "<测试命令>"

# 指定自定义启动命令
python skills/kflow-code/scripts/with_server.py --start-cmd "mvn spring-boot:run" --command "<命令>"

# 指定端口
python skills/kflow-code/scripts/with_server.py --port 8080 --command "<命令>"
```

参数：
- `--command` / `-c`：要在服务就绪后执行的命令（必需）
- `--start-cmd`：服务启动命令（默认从 service-guide.md 读取；首次运行时触发 READ_SERVICE_GUIDE 四阶段就绪检测：DETECT→VALIDATE→COLLECT→PERSIST）
- `--port`：服务端口（默认从 service-guide.md 读取）
- `--health-endpoint`：健康检查端点（默认 `/health`）
- `--timeout`：启动超时秒数（默认 60）

### 1.3 Daemon 模式（新增）

```bash
# 启动持久化服务
python skills/kflow-code/scripts/with_server.py --daemon --state-file .service-state.json

# 指定启动命令和端口
python skills/kflow-code/scripts/with_server.py --daemon --start-cmd "mvn spring-boot:run" --port 8080 --state-file .service-state.json

# 同时启动前后端
python skills/kflow-code/scripts/with_server.py --daemon --start-cmd "mvn spring-boot:run" --port 8080 --state-file .service-state.json
python skills/kflow-code/scripts/with_server.py --daemon --start-cmd "npm run dev" --port 5173 --state-file .service-state.json
```

参数：
- `--daemon`：启用持久化模式
- `--state-file`：服务状态文件路径（默认 `.service-state.json`）
- `--start-cmd`：服务启动命令
- `--port`：服务端口
- `--health-endpoint`：健康检查端点（默认 `/health`）
- `--db-health-endpoint`：数据库健康检查端点（默认 `/db-health`）
- `--timeout`：启动超时秒数（默认 60）
- `--health-retries`：健康检查重试次数（默认 30）
- `--health-interval`：健康检查重试间隔秒数（默认 2）

### 1.4 状态查询

```bash
# 查询所有服务状态
python skills/kflow-code/scripts/with_server.py --status --state-file .service-state.json

# 输出示例:
# PID      PORT      STATUS     START_TIME           HEALTH
# 12345    8080      running    2026-05-28T10:00:00  healthy
# 12346    5173      running    2026-05-28T10:00:01  healthy
```

### 1.5 健康检查

```bash
# 对所有已记录服务执行健康检查
python skills/kflow-code/scripts/with_server.py --health --state-file .service-state.json

# 退出码: 0 = 全部健康, 1 = 部分/全部不健康
```

### 1.6 停止所有服务

```bash
# 停止所有由 daemon 模式启动的服务
python skills/kflow-code/scripts/with_server.py --stop-all --state-file .service-state.json

# 停止流程:
# 1. 读取 .service-state.json 获取所有 PID
# 2. 逐个发送 SIGTERM
# 3. 等待 30s
# 4. 未终止的进程发送 SIGKILL
# 5. 等待 10s
# 6. 仍未终止 → 输出僵尸进程信息，退出码 1
```

---

## 二、端口冲突检测

### 2.1 检测命令

```bash
# Windows (PowerShell)
netstat -ano | findstr :<port>

# Linux/macOS
lsof -i :<port>
# 或
ss -tlnp | grep :<port>
```

### 2.2 检测流程

```
1. 从 service-guide.md dev 环境读取目标端口列表
2. 逐端口检测是否被占用
3. 判断占用进程身份:
   ├── 空闲 → 正常启动
   ├── .service-state.json 中记录的 PID → 执行 STOP_STALE
   └── 非预期进程 → ⚠️ 阻塞，输出占用信息
```

### 2.3 检测结果处理

| 场景 | 命令 | 后续操作 |
|------|------|---------|
| 端口空闲 | — | 正常启动服务 |
| 残留服务占用 | `taskkill /PID <pid>` (Win) / `kill <pid>` (Unix) | STOP_STALE 后启动 |
| 非预期进程占用 | — | ❌ 阻塞，提示用户处理 |

### 2.4 端口配置来源

端口 SHALL 从 `docs/service-guide.md` dev 环境配置中读取。service-guide.md 中端口配置格式：

```markdown
## 服务端口

| 服务 | 开发端口 | 生产端口 |
|------|---------|---------|
| 后端 API | 8080 | 8080 |
| 前端 DevServer | 5173 | — |
| 数据库 | 5432 | 5432 |
```

---

## 三、服务停止超时链

### 3.1 超时链操作

```
1. SIGTERM → 优雅终止
   ├── Windows: taskkill /PID <pid>
   ├── Unix: kill -15 <pid>
   └── 等待 ≤ 30s，每 2s 检查一次进程是否存活

2. SIGKILL → 强制终止（仅当步骤 1 超时时执行）
   ├── Windows: taskkill /F /PID <pid>
   ├── Unix: kill -9 <pid>
   └── 等待 ≤ 10s，每 2s 检查一次进程是否存活

3. ERROR → 阻塞（仅当步骤 1+2 均失败时）
   └── 输出: PID、端口、进程名称、建议手动处理
```

### 3.2 进程存活检测

```bash
# Windows
tasklist /FI "PID eq <pid>" 2>nul | findstr <pid>

# Linux/macOS
kill -0 <pid> 2>/dev/null && echo "alive" || echo "dead"
```

### 3.3 stop-all 完整流程

```bash
python skills/kflow-code/scripts/with_server.py --stop-all --state-file .service-state.json
```

内部执行：
1. 读取 `.service-state.json` → 获取 services 数组
2. 对每个 service 按 PID 倒序（后启动的先停止）执行超时链
3. 验证所有端口已释放（netstat/lsof 检测）
4. 全部释放 → 删除 `.service-state.json`，退出码 0
5. 有端口未释放 → 保留 `.service-state.json`，输出僵尸进程信息，退出码 1

---

## 四、健康检查

### 4.1 健康检查端点

| 检查项 | 端点 | 预期响应 | 适用阶段 |
|--------|------|---------|---------|
| 服务就绪 | `GET http://localhost:{port}/health` | HTTP 200 | 所有需要服务的阶段 |
| 数据库就绪 | `GET http://localhost:{port}/db-health` | HTTP 200 | 测试阶段 |
| 前端就绪 | `GET http://localhost:{port}/health` | HTTP 200 | E2E/集成测试 |

### 4.2 健康检查命令

```bash
# 单端点检查
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health

# with_server.py 内置健康检查
python skills/kflow-code/scripts/with_server.py --health --state-file .service-state.json
```

### 4.3 健康检查轮询参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 启动超时 | 60s | 服务启动的总等待时间 |
| 重试间隔 | 2s | 每次健康检查之间的等待时间 |
| 最大重试次数 | 30 | 超时前最多重试次数（30 × 2s = 60s） |

### 4.4 健康检查失败处理

1. 输出失败端点 URL 和 HTTP 状态码
2. 输出服务最后 20 行日志（stdout + stderr）
3. ❌ 阻塞当前阶段，等待用户修复

---

## 五、.service-state.json 格式

### 5.1 完整格式

```json
{
  "version": "1.0.0",
  "created_at": "2026-05-28T10:00:00+08:00",
  "updated_at": "2026-05-28T10:30:00+08:00",
  "services": [
    {
      "id": "backend-api",
      "type": "backend",
      "pid": 12345,
      "port": 8080,
      "start_command": "mvn spring-boot:run -Dspring-boot.run.profiles=dev",
      "start_time": "2026-05-28T10:00:00+08:00",
      "health_endpoint": "/health",
      "db_health_endpoint": "/db-health",
      "health_status": "healthy",
      "last_health_check": "2026-05-28T10:30:00+08:00"
    },
    {
      "id": "frontend-dev",
      "type": "frontend",
      "pid": 12346,
      "port": 5173,
      "start_command": "npm run dev",
      "start_time": "2026-05-28T10:00:01+08:00",
      "health_endpoint": "/health",
      "health_status": "healthy",
      "last_health_check": "2026-05-28T10:30:00+08:00"
    }
  ]
}
```

### 5.2 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 状态文件格式版本 |
| `created_at` | ISO 8601 | 文件创建时间 |
| `updated_at` | ISO 8601 | 最后更新时间 |
| `services[].id` | string | 服务唯一标识 |
| `services[].type` | enum | `backend` / `frontend` |
| `services[].pid` | int | 进程 ID |
| `services[].port` | int | 监听端口 |
| `services[].start_command` | string | 启动命令 |
| `services[].start_time` | ISO 8601 | 服务启动时间 |
| `services[].health_endpoint` | string | 健康检查端点路径 |
| `services[].db_health_endpoint` | string | 数据库健康检查端点（仅后端） |
| `services[].health_status` | enum | `starting` / `healthy` / `unhealthy` / `stopped` |
| `services[].last_health_check` | ISO 8601 | 最后一次健康检查时间 |

---

## 六、浏览器进程清理

Playwright 运行时环境隔离在 `.kflow-runtime/playwright/` 下。安装和二进制由 🔶 浏览器 阶段 PRE_HOOK 按需初始化（`cd .kflow-runtime/playwright && npm install playwright && npx playwright install chromium`）。

```bash
# 清理所有残留 Playwright 浏览器进程（从项目根目录执行）
playwright-cli kill-all
```

清理场景：
- prototype-design 阶段 VERIFY 步骤完成后
- e2e-test 阶段每轮测试完成后（POST_HOOK）
- integration-test 阶段完成后（POST_HOOK，仅前后端项目）

**路径约束**：
- `playwright-cli kill-all` SHALL 从项目根目录执行，SHALL NOT 在 `docs/designs/prototypes/` 目录下产生残留文件
- Playwright 安装、使用均通过 `.kflow-runtime/playwright/` 下的隔离环境

---

## 七、数据库迁移

### 7.1 迁移执行规则

测试阶段 PRE_HOOK 中 SHALL 检测并执行未执行的迁移脚本。

```bash
# 检测迁移状态（具体命令由 service-guide.md 定义）
# 示例（Flyway）:
mvn flyway:migrate -Dflyway.locations=filesystem:docs/changes/{change}/migrations

# 示例（自定义迁移工具）:
# （由具体项目的 service-guide.md 定义）
```

### 7.2 迁移失败处理

- 迁移执行失败 → ❌ 阻塞，输出失败脚本和错误信息
- 不跳过失败迁移，需人工修复后重新执行
