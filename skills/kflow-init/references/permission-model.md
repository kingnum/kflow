# KFlow 权限声明模型

> **版本**: 1.0.0
> **来源**: 变更 portable-permission-propagation
> **加载层级**: 基础层
> **适用阶段**: 全部（权限配置相关）
>
> **v1.0.0**: 初始版本——集中定义 kflow Skills 执行所需权限清单、聚合规则、环境适配指引和幂等配置规则。取代分散在各处的硬编码权限列表，作为权限配置的 source of truth。

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
