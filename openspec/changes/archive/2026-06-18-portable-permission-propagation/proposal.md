## Why

上一个变更 `flexible-repetition-subagent-enforcement` 引入了权限预配置机制——在项目 `.claude/settings.json` 中预设 kflow 所需的 16 条权限，确保子代理后台运行时不会因权限缺失而降级执行。

该机制存在两个根本问题：

1. **作用域错误**：`.claude/settings.json` 是项目级配置，仅对当前开发项目（kflow-devflow-skills）生效。Skills 通过 `package-skills.sh` 打包分发到其他项目时，只包含 `.claude/skills/kflow-*/` 目录，不包含 `settings.json`。目标项目没有权限配置，子代理"无权限"问题依然复现——等于在这个项目里修了 bug，但 bug 跟着 Skills 去了别的项目照样存在。

2. **环境绑定**：`.claude/settings.json` 是 Claude Code 专有的权限配置机制。如果团队未来使用其他 AI 编码工具（Cursor、Copilot CLI 等），整套权限模型失效。权限的 source of truth 不应绑定在特定工具的配置文件上。

## What Changes

### 1. 权限声明内嵌到 Skill（Skill 自身成为 source of truth）

在 `kflow-shared/` 中新增 `permission-model.md`，定义 kflow 全局权限声明清单：

```
kflow-shared/permission-model.md
├── 全局必需权限（所有 Skill 共享）
│   ├── Bash 工具类：npm/yarn/pnpm/npx/node/git/curl/python/python3
│   ├── 文件操作类：Read/Write/Edit/Glob/Grep
│   ├── 子代理调用：Agent
│   └── 文档查询：WebFetch
├── 权限聚合规则（kflow-init 读取所有 Skill 声明后合并）
└── 环境适配指引（各 AI 工具的权限配置方式）
```

同步更新 `kflow-shared/repetition-model.md §12.5`——移除硬编码的权限列表，改为引用 `kflow-shared/permission-model.md`。

### 2. kflow-init 增加权限配置步骤

kflow-init 在目标项目首次执行时，增加一个新步骤：

```
kflow-init 执行流程（新增步骤）

  扫描项目类型 → 扫描 MCP → 扫描项目画像
      │
      ▼
  【新增】读取 kflow-shared/permission-model.md 权限声明
      │
      ▼
  【新增】检测目标项目是否已有 .claude/settings.json
      │
      ├── 不存在 → 自动创建，写入 kflow 所需权限
      ├── 已存在 → 检测是否包含 kflow 所需权限
      │     ├── 缺少部分 → 追加缺失权限（合并，不覆盖）
      │     └── 齐全 → 跳过，无需操作
      ▼
  【新增】输出权限配置状态到 toolchain.md
```

关键设计原则：
- **幂等**：重复执行不会重复添加
- **合并不覆盖**：目标项目已有的权限配置保留，只追加缺失项
- **用户确认**：创建或修改 settings.json 前，通过 AskUserQuestion 征求用户同意

### 3. 后台子代理权限失败自动回退前台机制

即使 kflow-init 正确配置了权限，仍可能出现以下情况导致后台子代理因权限问题失败：
- 用户手动删除或修改了 settings.json
- 目标项目使用不同版本的 Claude Code，权限机制有差异
- 新增的工具调用未在权限清单中

因此增加**后台失败自动回退前台子代理**的韧性机制：

```
子代理以 run_in_background=true 启动
    │
    ├── 执行成功 → 正常继续
    │
    └── 执行失败（主 Agent 检测到异常）
        │
        ▼
  【新增】主 Agent 检测失败原因
        │
        ├── 匹配权限相关错误模式：
        │   ├── "permission denied" / "权限不足"
        │   ├── "not allowed" / "不允许"
        │   ├── "requires approval" / "需要批准"
        │   └── 错误信息包含工具名（Bash/Write/Edit 等）
        │
        ├── 是权限问题 → 记录失败原因，输出提示：
        │   "检测到子代理因权限问题失败，自动切换为前台子代理模式重新执行"
        │   │
        │   ▼
        │   以 run_in_background=false 创建新的子代理重新执行
        │   （相同 prompt、相同任务、继承轮次计数器）
        │   ⚠ 主 Agent SHALL NOT 直接接管执行
        │   │
        │   ├── 前台子代理执行成功 → 正常继续，更新 .status.md 记录
        │   │
        │   └── 前台子代理也失败 → 标记 ⚠️ 阻塞，提示用户：
        │       "子代理前台/后台均失败，请检查权限配置或手动处理"
        │
        └── 非权限问题 → 按原有重试机制处理（参见 §12 轮次级重试）
```

关键设计原则：
- **严格子代理执行**：回退前台时，MUST 创建新的子代理（run_in_background=false），主 Agent SHALL NOT 直接接管执行
- **自动检测**：主 Agent 从子代理错误输出中识别权限相关错误模式
- **透明回退**：回退前台子代理执行时，保留轮次计数器和任务上下文
- **用户提示**：回退时输出明确提示，让用户知道发生了什么
- **不掩盖问题**：如果前台子代理也失败，标记阻塞而非无限重试
- **计数规则**：权限回退不计入轮次级重试的 3 次上限（因为是不同执行模式）

实现位置：
- `kflow-shared/repetition-model.md` 新增 §12.7「后台权限失败回退前台子代理机制」
- 7 个执行类阶段 SKILL.md 的「⚠ 子代理强制规则」框中新增第 5 条规则：「后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管」

### 4. 移除本项目中的硬编码 settings.json

当前项目（kflow-devflow-skills）的 `.claude/settings.json` 是手动创建的硬编码文件。变更完成后：
- 删除本项目手动创建的 `.claude/settings.json`
- 通过 kflow-init 重新生成（验证新流程的端到端正确性）

### 5. Specs 和共享文档更新

- `subagent-enforcement-notice` spec：移除"项目 SHALL 预配置 `.claude/settings.json`"条款，改为"kflow-init SHALL 在目标项目中配置 kflow 所需权限（参见 `kflow-shared/permission-model.md`）"；新增"后台子代理权限失败 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管"
- `subagent-isolation-rule` spec：同上调整；重试机制新增权限回退场景（创建新前台子代理，不计入 3 次上限）
- `kflow-shared/repetition-model.md §12.5`：移除硬编码权限列表，改为引用 `kflow-shared/permission-model.md`
- `kflow-shared/repetition-model.md` 新增 §12.7：后台权限失败回退前台子代理机制

## Capabilities

### New Capabilities

- `kflow-permission-model`：kflow 全局权限声明与目标项目权限自动配置能力。权限清单定义在 `kflow-shared/permission-model.md`（跟随 Skill 分发），kflow-init 在目标项目中自动读取声明并生成对应权限配置，支持幂等合并不覆盖
- `background-permission-fallback`：后台子代理权限失败自动回退前台子代理执行机制。主 Agent 从子代理错误输出中识别权限相关错误模式，自动创建新的前台子代理（run_in_background=false）重新执行同一任务，主 Agent SHALL NOT 直接接管执行，保留轮次计数器和任务上下文，回退不计入轮次级重试的 3 次上限

### Modified Capabilities

- `subagent-enforcement-notice`：权限预配置要求从"项目 SHALL 手动配置 settings.json"改为"kflow-init SHALL 自动配置"；新增后台权限失败回退前台子代理规则（主 Agent SHALL NOT 直接接管）
- `subagent-isolation-rule`：同上调整；重试机制新增权限回退场景（创建新前台子代理）
- `shared-repetition-model`：§12.5 移除硬编码权限列表，改为引用 `kflow-shared/permission-model.md`；新增 §12.7 后台权限失败回退前台子代理机制

## Impact

### 影响的 Skill（8 个）
- `.claude/skills/kflow-init/SKILL.md`（新增权限配置步骤）
- `.claude/skills/kflow-plan/SKILL.md`（子代理强制规则框新增第 5 条：权限失败回退）
- `.claude/skills/kflow-code/SKILL.md`（同上）
- `.claude/skills/kflow-code-review/SKILL.md`（同上）
- `.claude/skills/kflow-api-test/SKILL.md`（同上）
- `.claude/skills/kflow-e2e-test/SKILL.md`（同上）
- `.claude/skills/kflow-integration-test/SKILL.md`（同上）
- `.claude/skills/kflow-bug-fix/SKILL.md`（同上）

### 新增的核心共享文档（1 个）
- `.claude/skills/kflow-shared/permission-model.md`（权限声明清单 + 环境适配指引）

### 影响的核心机制文档（1 个）
- `.claude/skills/kflow-shared/repetition-model.md`（§12.5 权限列表改为引用 + 新增 §12.7 后台权限失败回退机制）

### 影响的设计文档（1 个）
- `docs/designs/skills/kflow-init.md`（新增权限配置步骤设计）

### 影响的 specs（2 个）
- `openspec/specs/subagent-enforcement-notice/spec.md`
- `openspec/specs/subagent-isolation-rule/spec.md`

### 配置变更
- 删除 `.claude/settings.json`（改为 kflow-init 自动生成）

### 影响的模板文件
- `docs/designs/templates/docs/toolchain.md`（新增权限配置状态节）

### 版本影响
- Minor 版本自增（新增能力 + 核心机制调整）
