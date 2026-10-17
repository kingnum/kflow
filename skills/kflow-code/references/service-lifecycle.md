# 服务生命周期操作指令（运行时）

> **版本**: 1.0.0
> **类型**: 运行时共享文件（被 `skills/kflow-code/references/hooks.md` 引用）
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
