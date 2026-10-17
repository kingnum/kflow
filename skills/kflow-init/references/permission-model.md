# KFlow 权限声明模型

> **版本**: 1.0.0
> **来源**: 变更 portable-permission-propagation
> **加载层级**: 基础层
> **适用阶段**: 全部（权限配置相关）
>
> **v1.0.0**: 初始版本——集中定义 kflow Skills 执行所需权限清单、聚合规则、环境适配指引和幂等配置规则。取代分散在各处的硬编码权限列表，作为权限配置的 source of truth。
>
> **v1.1.0**: 新增 §5「上下文配置」——kflow-init 除权限清单外还须写入上下文压缩阈值与主 Agent 门控 hook 注册项。

## 1. 全局必需权限

所有 kflow Skills 共享的权限清单，确保子代理执行过程中无权限请求中断。

### Bash 工具类

| 权限 | 说明 |
|------|------|
| `Bash(npm *)` | npm 包管理器 |
| `Bash(yarn *)` | yarn 包管理器 |
| `Bash(pnpm *)` | pnpm 包管理器 |
| `Bash(npx *)` | npx 包运行器 |
| `Bash(node *)` | Node.js 运行时 |
| `Bash(git *)` | Git 版本控制 |
| `Bash(curl *)` | HTTP 请求 |
| `Bash(python *)` | Python 脚本 |
| `Bash(python3 *)` | Python3 脚本 |

### 文件操作类

| 权限 | 说明 |
|------|------|
| `Read` | 读取文件 |
| `Write` | 写入文件 |
| `Edit` | 编辑文件 |
| `Glob` | 文件模式搜索 |
| `Grep` | 内容搜索 |

### 子代理调用

| 权限 | 说明 |
|------|------|
| `Agent` | 子代理调用 |

### 文档查询

| 权限 | 说明 |
|------|------|
| `WebFetch` | 文档查询 |

### 完整权限列表

```
Bash(npm *), Bash(yarn *), Bash(pnpm *), Bash(npx *), Bash(node *), Bash(git *), Bash(curl *), Bash(python *), Bash(python3 *), Read, Write, Edit, Glob, Grep, Agent, WebFetch
```

## 2. 权限聚合规则

kflow-init 读取本声明后，按以下规则合并为 `.claude/settings.json`：

1. **读取**：kflow-init 读取 `skills/kflow-init/references/permission-model.md` §1 全局必需权限清单
2. **合并**：将权限清单与目标项目 `.claude/settings.json` 的 `permissions.allow` 列表合并
3. **追加策略**：仅追加目标项目中缺失的权限条目，不删除或修改已有条目
4. **用户确认**：创建或修改 settings.json 前，通过 AskUserQuestion 征求用户同意
5. **输出**：配置结果写入 toolchain.md 权限配置状态节

## 3. 环境适配指引

### Claude Code → `.claude/settings.json` 格式映射

```json
{
  "permissions": {
    "allow": [
      "Bash(npm *)",
      "Bash(yarn *)",
      "Bash(pnpm *)",
      "Bash(npx *)",
      "Bash(node *)",
      "Bash(git *)",
      "Bash(curl *)",
      "Bash(python *)",
      "Bash(python3 *)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Agent",
      "WebFetch"
    ],
    "deny": []
  }
}
```

### 其他工具 → 待定义

当前团队仅使用 Claude Code，其他 AI 工具（Cursor、Copilot CLI 等）的权限适配规则待定义。本节预留结构，未来需要时只需补充具体映射规则。

## 4. 权限配置幂等规则

### 检测已有配置

kflow-init 执行 PERM_CONFIG 步骤时，SHALL 先检测目标项目 `.claude/settings.json` 是否存在及其 `permissions.allow` 列表内容。

### 合并不覆盖

| 场景 | 操作 |
|------|------|
| settings.json 不存在 | AskUserQuestion 询问是否创建 → 用户确认后创建 |
| settings.json 存在但缺少部分权限 | AskUserQuestion 列出缺失权限并询问是否追加 → 用户确认后追加 |
| settings.json 权限已齐全 | 输出"权限配置齐全"，不修改文件 |
| 用户拒绝配置 | 不修改 settings.json，toolchain.md 标注"权限未配置" |

合并时仅追加缺失权限到 `permissions.allow` 列表，SHALL NOT 删除或修改已有条目，SHALL NOT 覆盖 `deny` 列表。

### 重复执行不重复添加

kflow-init 重复执行时：
- settings.json 已包含全部所需权限 → 不重复添加，不重复询问
- settings.json 已包含部分所需权限 → 仅追加缺失项，不重复已有项

## 5. 上下文配置

除权限清单外，kflow-init 的 PERM_CONFIG 步骤 SHALL 向目标项目 `.claude/settings.json` 写入以下两项上下文配置。二者与权限配置同属一个写入动作，校验与幂等规则与 §4 一致。

### 5.1 自动压缩阈值 `autoCompactWindow`

| 项 | 取值 | 写入位置 |
|----|------|---------|
| `autoCompactWindow` | `300000` | `.claude/settings.json` 顶层字段（与 `permissions` 同级） |

使上下文在约 30 万 token 时触发自动压缩，而非等到接近上下文窗口上限。缺省（未配置）时 Claude Code 在接近窗口上限时才压缩，压缩前的高基数轮次会被反复重读，同一份工作被做两遍。

**幂等规则**：字段缺失时补写为 `300000`；已存在且取值更小（即更早压缩）时保持不变——更小的取值意味着更强的节流，不应被抬高。

### 5.2 主 Agent 门控 hook 注册

| 项 | 取值 |
|----|------|
| hook 事件 | `PreToolUse` |
| matcher | `Edit` / `Write` / `Bash` |
| 脚本源文件 | `skills/kflow-init/scripts/kflow-main-agent-gate.py`（随 kflow-init 安装） |
| 脚本落位 | `.claude/hooks/kflow-main-agent-gate.py`（kflow-init 复制到目标项目） |
| 判定来源 | 变更级 `.status.md` 的当前阶段字段 |

**安装动作**：kflow-init 在 PERM_CONFIG 步骤中 SHALL 将脚本源文件复制到目标项目的 `.claude/hooks/kflow-main-agent-gate.py`（目录不存在时创建），再写入下述注册条目。脚本 SHALL 以 Python 3 运行，无需第三方依赖。

注册条目写入 `.claude/settings.json` 的 `hooks.PreToolUse` 数组：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/kflow-main-agent-gate.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

门控的作用与判定规则见 `main-agent-execution-gating` 能力；本节只声明 kflow-init 须写入的配置项与落位。

**幂等规则**：项目自定义的 hook 条目 SHALL 保持不变——仅在 `hooks.PreToolUse` 中查找到本门控脚本的注册条目时更新该条目，不得整体替换 `PreToolUse` 数组，也不得删除或改写项目自有的 hook 条目。

**行为与降级**：

| 情形 | 行为 |
|------|------|
| 无法判定当前阶段（无活跃变更 / `.status.md` 缺失 / 字段不可解析 / 存在多个活跃变更） | 放行——门控的目的是降低上下文消耗，不是安全边界 |
| 设计类阶段（explore / prototype-design / design） | 放行——主 Agent 是这些阶段产物的写作者 |
| 执行类阶段（plan / code / code-review / api-test / e2e-test / integration-test / bug-fix） | 主 Agent 的越界 `Edit`/`Write` 与长输出命令被拒绝；子代理放行 |
| 子代理识别 | 以 stdin 的 `agent_id` / `agent_type` 为主判据——实测 Claude Code 2.1.278 中，子代理的 PreToolUse 输入含该两字段、主 Agent 不含；`transcript_path` 在当前版本为会话级路径、不构成有效判据；字段缺失时按主 Agent 处理 |
| 上游字段变化 | `agent_id` / `agent_type` 为未文档化字段。若升级后子代理不再携带该字段，子代理会被误判为主 Agent（其写入被拒绝）；此时设置 `KFLOW_GATING_DISABLE=1` 临时关闭门控，并按新版本重新探测 |
| 脚本异常 | fail-open 放行，并记录到 `.claude/kflow-gating.log` |
| 需要临时关闭门控 | 设置环境变量 `KFLOW_GATING_DISABLE=1` |

> **白名单**：`.status.md`、`status-log.md`、`docs/skill-suggestion.md`、`docs/doc-optimize-report.md`、`docs/doc-optimize-references.md`。前两者保障状态双写，后者保障 skill 改进建议与独立维护工具的正常写入。

### 5.3 上下文配置状态输出

上下文配置结果与权限配置结果一并写入 `docs/toolchain.md` 的权限配置状态节：

| 字段 | 说明 |
|------|------|
| 自动压缩阈值 | 如 `300000` / `已存在（{值}）` / `未配置` |
| 门控 hook | 如 `已注册` / `已存在（保持）` / `未配置` |

### 5.4 配置校验

kflow-init 在写入完成后 SHALL 运行配置校验脚本，确认配置已实际生效：

```bash
python skills/kflow-init/scripts/verify_project_config.py --root <目标项目>
```

| 校验项 | 通过条件 |
|--------|---------|
| `settings.json` | 存在且可解析 |
| `autoCompactWindow` | 存在且 ≤ 300000 |
| `permissions.allow` | 全局必需权限齐全（缺项仅告警） |
| `hooks.PreToolUse` | 存在指向 `kflow-main-agent-gate.py` 的条目，matcher 覆盖 `Edit` / `Write` / `Bash` |
| `hook.timeout` | 存在（建议 5 秒） |
| 门控脚本 | `.claude/hooks/kflow-main-agent-gate.py` 存在 |

退出码 0 表示必需项全部通过；非 0 时按脚本输出修正缺失项后重跑。仍失败时记录到 `docs/toolchain.md` 并提示手工补救，SHALL NOT 阻塞 init 主流程。
