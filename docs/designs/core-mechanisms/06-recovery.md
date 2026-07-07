# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17

> **加载层级**: 恢复层
> **适用阶段**: 仅恢复场景

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 十二、中断恢复机制

> **借鉴**：gstack context-save checkpoint 机制

### 12.1 checkpoint 文件格式

checkpoint 文件使用 YAML frontmatter 格式：

```yaml
---
status: in_progress
branch: feature/add-user-auth
timestamp: 2026-04-30T14:30:00
files_modified:
  - docs/changes/add-user-auth/.status.md
  - docs/changes/add-user-auth/subchanges/auth-login/tasks.md
checkpoint_type: manual
---
```

| 字段 | 说明 |
|------|------|
| status | 当前阶段状态：in_progress / paused / blocked |
| branch | 当前 git 分支名 |
| timestamp | checkpoint 创建时间（ISO-8601） |
| files_modified | 本次会话修改的文件列表 |
| checkpoint_type | manual（用户触发）或 auto（系统自动） |

### 12.2 checkpoint 文件存储（两级）与恢复流程

> 完整规范参见 `kflow-resume 的 references/recovery-protocol.md`

checkpoint 按操作级别分为变更级（`docs/changes/{change}/checkpoints/`）和子变更级（`docs/changes/{change}/subchanges/{subchange}/checkpoints/`）两层存储。恢复时按 5 级优先级链查找：子变更 checkpoint → 变更级 checkpoint → 子变更 .status.md → 变更级 .status.md → tasks.md checkbox 反推。

### 12.4 checkpoint 创建时机

| 触发方式 | 时机 | 说明 |
|------|------|------|
| 手动触发 | 用户请求保存进度 | `/kflow-save` 或类似命令 |
| 自动触发 | 阶段切换时 | 进入下一阶段前自动保存 |
| 自动触发 | 长时间运行任务 | 每 30 分钟自动保存 |

---
