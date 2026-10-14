# kflow-init（环境初始化）

> **版本**: 参见仓库根目录 `VERSION` 文件（统一版本管理，18 个运行时 Skills 共享版本号）
> **阶段**: 环境初始化（按需阶段）

---

## 基本信息

```yaml
name: kflow-init
description: 环境初始化 - 发现当前上下文可用 MCP servers 和 Skills，评估组合可行性，输出工具链推荐方案和 toolchain.md。扫描项目画像（技术栈、目录结构、产品文档状态）注入 CLAUDE.md。支持老项目代码逆向分析生成产品文档草稿。按需阶段，项目启动时调用。
license: MIT
triggers:
  - 初始化
  - 环境配置
  - 工具推荐
  - 设置
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
```

---

## 门控检查

此阶段为可选的入口阶段，无前置门控要求。

输出产物检查：
- toolchain.md 文件在项目根目录 docs/ 下创建
- toolchain.md 包含各阶段推荐工具及优先级
- toolchain.md 包含环境能力扫描结果

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 项目上下文 | ✅ 必须 | 当前项目目录结构和类型 |
| 会话上下文 | ✅ 必须 | 当前会话可用的 MCP 和 Skills |

---

## 输出产物

| 产物 | 文件 | 模板 | 图例 | 内容要求 |
|------|------|------|------|---------|
| 工具链配置 | docs/toolchain.md | [工具链配置](../../templates/docs/toolchain.md) | ✅ 必须 | 各阶段推荐工具（含优先级）、环境能力扫描结果、安装建议 |
| 变更级覆盖（可选） | docs/changes/{change}/toolchain.md | [工具链配置](../../templates/docs/toolchain.md) | 🔶 条件 | 特定变更需要不同工具链时创建，优先级高于项目级 |
| CLAUDE.md 注入（项目画像） | CLAUDE.md | N/A（代码注入） | 🔶 条件 | 向项目根目录 CLAUDE.md 注入「项目画像」section（技术栈、目录结构、产品文档状态），marker 检测幂等。其中「项目类型」行为项目类型项目级记录的**唯一真源**，供变更创建链路（`kflow-guide`、`kflow-explore`）读取，读取优先级高于 `docs/toolchain.md` 头部的同名字段 |
| CLAUDE.md 注入（流程规则） | CLAUDE.md | N/A（代码注入） | 🔶 条件 | 向项目根目录 CLAUDE.md 注入/更新「变更流程强制规则」section（跨 skill 路由约束、用户接口约定与流程概览；SHALL NOT 含 skill 内部执行步骤），marker 检测幂等 |
| CLAUDE.md 注入（skill-suggestion 捕获） | CLAUDE.md | N/A（代码注入） | 🔶 条件 | 向项目根目录 CLAUDE.md 注入/更新「Skill 改进建议自动捕获」section（三种触发模式），marker 检测幂等 |
| CLAUDE.md 注入（项目自定义规则） | CLAUDE.md | N/A（代码注入） | 🔶 条件 | CLAUDE.md 不含 `## 项目自定义规则` marker 时创建该区块并标注由项目自行维护；后续 re-init SHALL NOT 读取、替换或删除其内容 |
| 产品文档草稿（老项目） | docs/CONTEXT.md, docs/designs/*.md, docs/service-guide.md | N/A（逆向分析生成） | 🔶 条件 | 老项目产品文档缺失时，代码逆向扫描生成草稿，用户审核确认后写入 |
| CONTEXT.md 检测 | docs/CONTEXT.md | N/A（环境检测） | ✅ 必须 | 检测 docs/CONTEXT.md 是否存在，存在时加载词汇表，不存在时标记"待构建" |

---

## 环境感知层次

系统分三层感知环境能力：

| 层次 | 感知方式 | 覆盖范围 |
|------|---------|---------|
| 运行时 | 扫描当前会话 MCP 工具前缀（如 mcp__context7__*） | 已连接的 MCP servers |
| 配置 | 读取 settings.json 中配置的 MCP servers | 已配置但可能未连接的 MCP |
| 知识库 | 内置推荐数据库 | 已知的推荐工具（如 /playwright-cli skill） |

---

## 工具推荐矩阵

### 按项目类型和阶段推荐

| 阶段 | 前后端项目 | 纯后端项目 | 优先级 |
|------|-----------|-----------|--------|
| 设计探索 | Read, Glob, Grep, AskUserQuestion | Read, Glob, Grep, AskUserQuestion | 必须 |
| 原型设计 | **多方案**（见下方方案对比） | ⏭️ 跳过 | 推荐 |
| 详细设计 | Read, Write, Edit, Agent | Read, Write, Edit, Agent | 必须 |
| 计划 | Write, Edit | Write, Edit | 必须 |
| 编码 | Bash, Read, Write, Edit, Agent | Bash, Read, Write, Edit, Agent | 必须 |
| 接口单元测试 | `kflow-api-test`、Bash, Read, Edit | `kflow-api-test`、Bash, Read, Edit | 必须 |
| E2E 测试 | `kflow-e2e-test`、**/playwright-cli skill**（首选）, playwright MCP（备选） | ⏭️ 跳过 | 推荐 |
| 集成测试 | Bash, Read, Agent | Bash, Read, Agent | 必须 |
| 缺陷修复 | Bash, Read, Edit, Agent | Bash, Read, Edit, Agent | 按需 |
| 归档 | Bash, Read, Write, Edit | Bash, Read, Write, Edit | 必须 |
| 审计 | Read, Agent | Read, Agent | 归档门控 |

**注意**：`kflow-browser-rules` 不列入推荐列表。

---

## 执行流程

```
环境初始化流程:

┌─────────────────────────────────────────────────────────────┐
│                      INIT WORKFLOW                           │
├─────────────────────────────────────────────────────────────┤
│  1. DETECT    → 确定项目类型（读取优先 + 扫描比对）           │
│  │   ├── 读取项目级记录（CLAUDE.md 项目画像 → toolchain.md 头部）│
│  │   ├── 记录缺失 → 扫描项目根目录检测前端工程标识            │
│  │   └── 记录存在 → 重新扫描，与记录比对                       │
│  1.5 TYPECONFIRM → 项目类型确认（条件触发）                   │
│  │   ├── 记录缺失（首次 init）→ AskUserQuestion 确认一次      │
│  │   ├── 扫描与记录冲突 → AskUserQuestion 请求裁决            │
│  │   └── 扫描与记录一致 → 静默复用，SHALL NOT 询问用户        │
│  2. SCAN      → 扫描环境能力                                 │
│  │   ├── 运行时: 检查 MCP 工具前缀                            │
│  │   │   └── 例: huashu-design Skill 存在 → 原型设计可用       │
│  │   ├── 配置: 读取 settings.json                            │
│  │   │   └── .claude/settings.json, settings.local.json      │
│  │   ├── Skills: 扫描 .claude/skills/ 目录                   │
│  │   │   └── 列出所有已安装 Skills                            │
│  │   └── CONTEXT: 检测 CONTEXT.md 领域词汇表                  │
│  │       ├── 存在 → 读取词汇表，标注"CONTEXT.md 已就绪"       │
│  │       └── 不存在 → 标注"CONTEXT.md 待构建"                 │
│  3. PROFILE   → 扫描项目画像信息（新增）                      │
│  │   ├── 项目类型、语言、框架、数据库、构建工具                │
│  │   ├── 关键目录、入口文件                                   │
│  │   └── 产品文档状态（8 项存在性检测）                       │
│  3.5 PERM_CONFIG → 权限配置（新增）                           │
│  │   ├── 读取 skills/kflow-init/references/permission-model.md 权限声明      │
│  │   ├── 检测 .claude/settings.json 是否存在及权限状态        │
│  │   ├── 不存在 → AskUserQuestion → 创建 settings.json        │
│  │   ├── 已存在但缺少部分权限 → AskUserQuestion → 追加缺失权限│
│  │   ├── 已齐全 → 输出"权限配置齐全"                          │
│  │   └── 用户拒绝 → toolchain.md 标注"权限未配置"             │
│  4. MATCH     → 匹配工具推荐矩阵                              │
│  │   ├── 根据项目类型确定所需阶段                             │
│  │   └── 为每个阶段匹配推荐工具                               │
│  5. GAP       → 检测能力缺口                                  │
│  │   ├── 原型设计需要 prototype-gen 角色 Skill（≥1 个）        │
│  │   │   └── 检测 huashu-design / frontend-design 存在性       │
│  │   │   └── 缺失时提示: "安装 huashu-design 或 frontend-design"│
│  │   └── E2E 测试需要 playwright-cli → 缺失时提示安装         │
│  6. COMPAT    → 组合可行性评估                                │
│  │   ├── 检查工具间已知冲突                                   │
│  │   ├── 检查每个阶段覆盖度                                   │
│  │   └── 标注覆盖度百分比                                     │
│  7. PROPOSE   → 输出多方案（如适用）                          │
│  │   ├── 方案 A: 推荐最佳组合                                 │
│  │   ├── 方案 B: 备选降级方案                                 │
│  │   └── 方案 C: 最小必须方案                                 │
│  │   └── 每方案标注覆盖度和风险                               │
│  8. CONFIRM   → 用户确认方案（AskUserQuestion）               │
│  9. OUTPUT    → 输出 docs/toolchain.md                        │
│ 10. LEGACY    → 老项目逆向分析（条件触发）                    │
│  │   ├── 检测产品文档缺失（docs/CONTEXT.md 或 functional-designs/ 为空） │
│  │   ├── AskUserQuestion: 是否通过代码逆向扫描生成文档草稿？   │
│  │   ├── 确认 → L1 配置文件 → L2 目录结构 → L3 源码语义       │
│  │   ├── 生成草稿（7 类，含 service-guide.md）→ 用户审核确认 → 写入  │
│  │   └── 跳过 → 产品文档标注为 ❌ 不存在                      │
│ 11. INJECT    → 注入 CLAUDE.md（受管 marker 3 个）            │
│  │   ├── 注入「项目画像」section (marker: `## 项目画像`)      │
│  │   │   ├── 不存在 → 在 CLAUDE.md 末尾追加                   │
│  │   │   └── 已存在 → 重新扫描并替换（幂等）                  │
│  │   ├── 注入「变更流程强制规则」section                      │
│  │   │   ├── 不存在 → 追加                                    │
│  │   │   └── 已存在 → 版本相同仅更新时间戳，否则全量替换      │
│  │   ├── 注入「Skill 改进建议自动捕获」section                │
│  │   │   ├── 不存在 → 追加                                    │
│  │   │   └── 已存在 → 幂等更新（不重复追加）                  │
│  │   ├── 创建「项目自定义规则」区块（不受管，不覆盖）         │
│  │   └── CLAUDE.md 不存在 → 跳过注入（可选）                  │
│ 12. GIT INIT  → 检测 Git 仓库并询问是否初始化（条件触发）     │
│  │   ├── 检测当前目录是否为 git 仓库（git rev-parse --git-dir） │
│  │   ├── 已是仓库 → 跳过                                       │
│  │   └── 非仓库 → AskUserQuestion 询问是否 git init            │
│ 13. COMPLETE  → 完成初始化                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 项目类型确定与确认（DETECT + TYPECONFIRM）

> **版本**: 当前变更新增。项目类型是仓库级不变量，其确认动作前移到 init 一次，变更创建链路改为继承。规则权威定义见 [core-mechanisms/01-project-types.md](../core-mechanisms/01-project-types.md#14-项目类型记录与继承)。

init 是项目生命周期中唯一「必然要打断用户一次」的场合（已有权限配置、工具链方案选择确认），且执行时正在做项目画像扫描，上下文最贴合，因此项目类型的用户确认落在本 Skill。

### 步骤 1 DETECT — 确定项目类型（读取优先 + 扫描比对）

```
项目类型确定逻辑:

1. 读取项目级记录（优先级从高到低）:
   ├── CLAUDE.md「## 项目画像」表的「项目类型」行
   └── docs/toolchain.md 头部的「项目类型」字段
2. 记录缺失 → 按检测规则扫描项目根目录:
   ├── 读取 package.json，检查前端框架依赖（react, vue, angular, next, nuxt, svelte 等）
   ├── 扫描前端源文件（.vue, .tsx, .jsx, .svelte）
   ├── 扫描前端构建配置（vite.config, webpack.config 等）
   ├── 任一命中 → 前后端项目
   └── 全部不命中 → 纯后端项目
3. 记录存在 → 重新扫描（用途为与记录比对，非重新判定）
4. 冲突判定:
   ├── 扫描结果 == 记录值 → 一致
   └── 扫描结果 != 记录值 → 冲突
```

### 步骤 1.5 TYPECONFIRM — 项目类型确认（条件触发）

AskUserQuestion 仅在以下两种情形使用，其余情形 SHALL 静默复用，SHALL NOT 询问用户：

| 情形 | 条件 | 动作 |
|------|------|------|
| 首次确认 | 项目级记录不存在 | AskUserQuestion 展示检测结果，用户可确认或手动修正 |
| 冲突复核 | 项目级记录存在，且重新扫描结果与记录冲突 | AskUserQuestion 展示冲突项（扫描结果 vs 记录值），按裁决结果更新项目级记录 |

```
项目类型确认流程:

1. 记录不存在（首次 init / 首次确定项目类型）:
   └── AskUserQuestion 展示检测结果 → 用户确认或修正 → 结果写入项目级记录
2. 记录存在且重新扫描一致:
   └── 静默复用记录值，SHALL NOT 使用 AskUserQuestion 询问项目类型
3. 记录存在且重新扫描冲突:
   └── AskUserQuestion 请求用户裁决 → 按裁决结果更新项目类型行
```

### 项目级记录的写入

项目类型 SHALL 写入两处**项目级真源**，由本 Skill 在同一轮扫描中生成，值保持一致：

| 记录落点 | 位置 | 性质 |
|---------|------|------|
| CLAUDE.md 项目画像 | 「## 项目画像」表的「项目类型」行（步骤 11 INJECT 写入） | 权威来源，会话自动加载进上下文 |
| `docs/toolchain.md` | 头部元信息区的「项目类型」字段（步骤 9 OUTPUT 写入） | 兜底来源，init 的唯一必须产物 |

两处由同一轮扫描写入，不存在天然分叉；CLAUDE.md 为条件产物（文件不存在或用户清理画像区块时缺失），此时由 `docs/toolchain.md` 兜底。

### 静默复用规则

- **记录一致时 SHALL NOT 询问用户**：re-init 且重新扫描结果与项目级记录一致 → 静默复用记录值，不重复询问项目类型
- 仅 `docs/toolchain.md` 一处有值时（CLAUDE.md 画像缺失或被清理）→ 以该值静默复用，不询问
- 静默复用 SHALL NOT 跳过重新扫描——扫描用于漂移比对，是冲突发现的唯一来源

---

## 权限配置步骤（PERM_CONFIG）

### 步骤描述

在 PROFILE 步骤完成后、MATCH 步骤之前，执行权限配置。读取 `skills/kflow-init/references/permission-model.md` §1 全局必需权限清单，检测目标项目 `.claude/settings.json` 状态，按幂等规则配置权限。

### 权限配置流程

```
权限配置:

1. 读取 skills/kflow-init/references/permission-model.md §1 全局必需权限清单
2. 检测目标项目 .claude/settings.json 状态:
   ├── 不存在 → AskUserQuestion 询问是否创建
   │   ├── 用户确认 → 创建 .claude/settings.json，写入全部权限
   │   └── 用户拒绝 → toolchain.md 标注"权限未配置，子代理后台执行可能失败"
   ├── 已存在 → 读取 permissions.allow 列表
   │   ├── 缺少部分权限 → AskUserQuestion 列出缺失权限并询问是否追加
   │   │   ├── 用户确认 → 追加缺失权限（合并不覆盖）
   │   │   └── 用户拒绝 → toolchain.md 标注缺失权限
   │   └── 权限齐全 → 输出"权限配置齐全 ✅"
3. 记录权限配置状态到 toolchain.md 权限配置状态节
```

### 幂等规则

- 仅追加缺失权限到 permissions.allow，不删除或修改已有条目
- 不覆盖 deny 列表
- 重复执行时已包含全部所需权限 → 不重复添加，不重复询问

### 权限配置状态输出

| 字段 | 说明 |
|------|------|
| 配置状态 | ✅ 齐全 / ⚠️ 部分缺失 / ❌ 未配置 |
| 已配置权限数量 | 如 "16/16" |
| 缺失权限列表 | 仅部分缺失时列出 |
| 配置时间 | 本次配置的时间戳 |

---

## 组合可行性评估

```
兼容性检查:
├── 检查 MCP server 间端口/资源冲突
├── 检查 Skill 间功能重叠（择优推荐）
└── 降级策略: 有冲突时推荐不冲突的组合

覆盖度检查:
├── 每个必须阶段 → 至少 1 个工具支撑
├── 每个推荐阶段 → 标注是否有工具可用
└── 覆盖度 = 已覆盖阶段数 / 总阶段数 × 100%
```

---

## toolchain.md 格式

```markdown
# 工具链配置：{project-name}

> **创建时间**: {YYYY-MM-DD HH:MM}
> **项目类型**: {前后端项目 / 纯后端项目}
> **覆盖度**: {percentage}%

---

## 一、环境能力扫描

### MCP Servers

| MCP Server | 状态 | 能力 | 适用阶段 |
|-----------|------|------|---------|
| huashu-design | ✅ 已安装 | HTML 原型设计 | 原型设计 |
| playwright | ❌ 未安装 | 浏览器自动化 | E2E 测试 |

### Skills

| Skill | 状态 | 适用场景 |
|-------|------|---------|
| kflow-guide | ✅ 已安装 | 流程指引 |
| kflow-explore | ✅ 已安装 | 设计探索 |
| /playwright-cli | ❌ 未安装 | E2E 浏览器测试 |

### 领域词汇表

| 项目文件 | 状态 | 说明 |
|---------|------|------|
| CONTEXT.md | ✅ 已就绪 / ⚠️ 待构建 | 项目级领域词汇表，由 kflow-explore 构建和增补 |

### 权限配置状态

| 字段 | 值 |
|------|-----|
| 配置状态 | ✅ 齐全 / ⚠️ 部分缺失 / ❌ 未配置 |
| 已配置权限数量 | {N}/16 |
| 缺失权限列表 | {缺失的权限列表，无则标"—"} |
| 配置时间 | {YYYY-MM-DD HH:MM} |

---

## 二、阶段工具推荐

| 阶段 | 首选工具 | 备选工具 | 状态 |
|------|---------|---------|------|
| 设计探索 | Read, Glob, Grep | — | ✅ 可用 |
| 原型设计 | huashu-design Skill 或 frontend-design | — | ✅ 可用 |
| 详细设计 | Read, Write, Edit, Agent | — | ✅ 可用 |
| 计划 | Write, Edit | — | ✅ 可用 |
| 编码 | Bash, Read, Write, Edit, Agent | — | ✅ 可用 |
| 接口单元测试 | Bash, Read, Edit | — | ✅ 可用 |
| E2E 测试 | /playwright-cli skill | playwright MCP | ⚠️ 需安装 |
| 集成测试 | Bash, Read, Agent | — | ✅ 可用 |
| 缺陷修复 | Bash, Read, Edit, Agent | — | ✅ 可用 |
| 归档 | Bash, Read, Write, Edit | — | ✅ 可用 |
| 审计 | Read, Agent | — | ✅ 可用 |

---

## 三、安装建议

| 工具 | 用途 | 安装方式 | 优先级 |
|------|------|---------|--------|
| /playwright-cli | E2E 浏览器自动化测试 | 安装 skill | 高 |
| playwright MCP | E2E 备选方案 | 配置 MCP server | 低 |

---

## 四、多方案对比

### 方案 A：推荐最佳组合 (覆盖度 100%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | huashu-design Skill（一体化） | 低 |
| E2E 测试 | /playwright-cli skill | 低 |

### 方案 B：降级方案 (覆盖度 100%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | ui-ux-pro-max + huashu-design（设计驱动型） | 低 |
| E2E 测试 | playwright MCP | 中（封装度较低） |

### 方案 C：最小必须方案 (覆盖度 90%)

| 阶段 | 工具 | 风险 |
|------|------|------|
| 原型设计 | ui-ux-pro-max + frontend-design（静态页面型） | 中（无 flow demo） |
| E2E 测试 | ⏭️ 跳过 | 高（无浏览器自动化） |

### 原型设计阶段方案对比

> **铁律**：用户环境中必须至少有 1 个能编写 HTML 原型的 Skill（prototype-gen 角色）。

| 方案 | 包含 Skills | 流程 | 优点 | 缺点 | 适用场景 |
|------|-----------|------|------|------|---------|
| A: 一体化 | huashu-design | 单一引擎完成风格推荐+原型生成 | 内置顾问模式+反 slop+Playwright 验证 | 仅适用于 HTML 原型 | 大多数前端变更（推荐） |
| B: 设计驱动 | ui-ux-pro-max + huashu-design | ui-ux-pro-max 输出 design-system → huashu-design 生成原型 | 更精确的设计系统输出 | 需要两个 Skill 配合 | 对设计系统要求高的场景 |
| C: 静态页面型 | ui-ux-pro-max + frontend-design | ui-ux-pro-max 推荐风格 → frontend-design 生成 HTML | 生产级代码输出 | frontend-design 不做 flow demo | 需要快速出页面的场景 |

---

## 五、变更级覆盖

如需为特定变更使用不同的工具链，在 `docs/changes/{change}/toolchain.md` 创建覆盖配置。变更级配置优先级高于项目级。
```

> **头部「项目类型」字段的性质**：该字段是项目类型项目级记录的**兜底真源**。`docs/toolchain.md` 是 init 的唯一必须输出文件，存在性有保证，因此当 CLAUDE.md 缺失或无「## 项目画像」区块时，变更创建链路回退读取本字段。两处由同一轮扫描写入，值一致；读取优先级见「项目类型确定与确认（DETECT + TYPECONFIRM）」。

---

## 项目画像扫描

### 项目画像字段定义

| 字段 | 类型 | 来源 | 新项目 | 老项目 |
|------|------|------|--------|--------|
| 项目类型 | 枚举（前后端/纯后端） | 项目级记录（CLAUDE.md 项目画像 / `docs/toolchain.md` 头部）；记录缺失时 package.json + 源文件扫描 | ✅ 有值 | ✅ 有值 |
| 语言 | string | 源文件扫描 | ✅ 有值 | ✅ 有值 |
| 框架 | string | package.json | ✅ 有值 | ✅ 有值 |
| 数据库 | string | 配置文件扫描 | ⚠️ 待确定 | ✅ 有值 |
| 构建工具 | string | 配置文件扫描 | ✅ 有值 | ✅ 有值 |
| 关键目录 | list | 目录扫描 | ⚠️ 默认结构 | ✅ 有值 |
| 入口文件 | list | 文件扫描 | ❌ 不存在 | ✅ 有值 |
| 产品文档状态 | 8 项状态表 | 文件存在性检测 | 全 ❌ | 混合 |

### 扫描逻辑

```
项目画像扫描:

1. 项目类型: 读取项目级记录（CLAUDE.md 项目画像 → `docs/toolchain.md` 头部）→ 记录缺失时按前端框架依赖 + 源文件检测判定
2. 技术栈:
   ├── 语言: 扫描源文件扩展名 (.ts, .js, .py, .java, .go, .rs)
   ├── 框架: 从 package.json / pom.xml / requirements.txt 提取
   ├── 数据库: 扫描配置文件中的数据库连接信息
   └── 构建工具: 从构建配置文件中提取
3. 目录结构: 扫描 src/ 子目录，识别关键目录（controllers, models, services, routes）
4. 入口文件: 扫描常用入口文件名（main.*, index.*, app.*, server.*）
5. 产品文档状态: 8 项文件存在性检测
```

### 产品文档状态检测

系统检测以下 8 项产品文档的存在性：

| # | 文件 | 路径 | 状态值 |
|---|------|------|--------|
| 1 | CONTEXT.md | docs/CONTEXT.md | ✅ 已就绪 / ❌ 不存在 |
| 2 | 设计索引入口 | docs/designs/index.md | ✅ 已就绪 / ❌ 不存在 |
| 3 | 功能设计文档 | docs/designs/functional-designs/ | 前后端：✅ N个模块 / ❌ 不存在；纯后端：✅ N篇 / ❌ 不存在 |
| 4 | 架构全景 | docs/designs/detailed-designs/architecture.md | ✅ 已就绪 / ❌ 不存在 |
| 5 | 数据模型 | docs/designs/detailed-designs/data-model.md | ✅ 已就绪 / ❌ 不存在 |
| 6 | API 目录 | docs/designs/detailed-designs/api-catalog.md | ✅ 已就绪 / ❌ 不存在 |
| 7 | NFR 基线 | docs/designs/detailed-designs/nfr-baseline.md | ✅ 已就绪 / ❌ 不存在 |
| 8 | 服务指引 | docs/service-guide.md | ✅ 已就绪 / ❌ 不存在 |

**侧带检测**（不影响主判断）：config-items.md 和 error-handling.md 缺失时标注"⚠️ 建议补充"。

Re-init 时重新扫描并更新状态标记。

---

## 老项目逆向分析流程

### 触发条件

当 `docs/CONTEXT.md` 不存在或 `docs/designs/functional-designs/` 目录为空时，使用 AskUserQuestion 询问用户：

> "检测到产品文档缺失，是否通过代码逆向分析生成产品级文档草稿？"

选项：「生成草稿」「跳过」

### 三层逆向扫描

```
L1: 配置文件扫描
  ├── package.json / pom.xml / build.gradle / requirements.txt / Cargo.toml
  └── 输出: 技术栈、构建工具、依赖列表、配置项

L2: 目录结构扫描
  ├── src/ 子目录、routes/、controllers/、models/、services/
  └── 输出: 模块划分、候选设计域

L2.5: 前端工程扫描（前后端项目条件执行，纯后端跳过）
  ├── 路由配置: Vue Router / React Router / Next.js → path → component 映射、嵌套层级
  ├── 菜单配置: 独立配置文件 / 组件内菜单 → 一级菜单、二级菜单、权限控制
  ├── 页面组件: 页面标题 / 表单字段(name/label/rules) / 操作按钮
  └── 输出: 菜单层级结构、表单字段、操作按钮

L3: 源码语义扫描
  ├── 路由定义、数据模型、API 接口、关键注释、异常处理
  └── 输出: API 目录、数据模型、领域术语、错误码
```

### 生成文档草稿

基于扫描结果生成产品文档草稿（标注 `> 由 AI 逆向分析生成，待人工审核`）：

| 序号 | 文档 | 扫描来源 | 前后端项目 | 纯后端项目 |
|------|------|---------|-----------|-----------|
| 1 | docs/CONTEXT.md | L3 提取 | 领域术语及定义 | 领域术语及定义 |
| 2 | docs/designs/index.md | 综合 | 项目概述、功能模块导航（指向子目录） | 项目概述、功能模块导航（指向平铺文件） |
| 3 | docs/designs/functional-designs/ | L2.5 + L3 | 按菜单子目录: `{menu}/index.md` + `{menu}/part-NN.md` | 按设计域平铺: `{domain}.md` (backend-domain.md) |
| 4 | docs/designs/detailed-designs/architecture.md | L1 + L2 | 系统架构模式推断 + 配置项索引 + 错误处理索引 | 系统架构模式推断 + 配置项索引 + 错误处理索引 |
| 5 | docs/designs/detailed-designs/data-model.md | L3 实体扫描 | 实体及关键字段聚合 | 实体及关键字段聚合 |
| 6 | docs/designs/detailed-designs/api-catalog.md | L3 路由定义 | API 端点目录 | API 端点目录 |
| 7 | docs/designs/detailed-designs/nfr-baseline.md | L3 注解扫描 | NFR 基线 | NFR 基线 |
| 8 | docs/designs/detailed-designs/config-items.md | L1 配置扫描 | 配置项骨架（新增） | 配置项骨架（新增） |
| 9 | docs/designs/detailed-designs/error-handling.md | L3 异常扫描 | 错误码骨架（新增） | 错误码骨架（新增） |
| 10 | docs/service-guide.md | L1 配置扫描 | dev 环境启动命令、端口、数据库 | dev 环境启动命令、端口、数据库 |

### 用户审核确认

生成完成后展示 7 类文档清单和关键内容摘要，使用 AskUserQuestion 请求用户确认：
- 「确认写入」— 将确认的文档写入对应路径，更新项目画像中的产品文档状态
- 「修改后写入」— 用户自行修改后写入
- 「放弃」— 不写入任何文档，标注产品文档为 ❌ 不存在

---

## 首次 init 时 git 仓库检测

首次 init 完成时，检测当前目录是否是 git 仓库：

```
git 仓库检测流程:

1. git rev-parse --git-dir 检测
   ├── 成功（已是 git 仓库）→ 跳过，进入 COMPLETE
   └── 失败（非 git 仓库）→ 进入询问步骤

2. AskUserQuestion 询问:
   └── "当前目录尚未初始化为 git 仓库，是否执行 git init？"
       选项:
       ├──「初始化 git 仓库」→ git init
       └──「跳过」→ 不执行，提示用户可后续手动初始化
```

git init 失败不阻塞 init 流程，提示失败原因。

---

## Re-init 幂等更新策略

重新执行 kflow-init 时：

```
幂等更新逻辑:

1. 项目画像 section:
   ├── 重新扫描所有画像字段
   ├── 更新扫描时间戳
   └── 保留用户手动修改的其他 CLAUDE.md 内容

2. 流程规则 section:
   ├── 读取区块版本行并与本 Skill front matter 的 `version` 比较
   ├── 版本相同 → 仅更新时间戳
   └── 版本不同 / 未读到版本行 / 读到但无法解析 → 全量替换为当前模板内容

3. 项目类型（静默复用）:
   ├── 读取项目级记录（CLAUDE.md 项目画像 → `docs/toolchain.md` 头部）
   ├── 重新扫描项目根目录并与记录比对
   ├── 扫描与记录一致 → 静默复用记录值，SHALL NOT 使用 AskUserQuestion 询问用户
   └── 扫描与记录冲突 → AskUserQuestion 请求用户裁决，按裁决结果更新项目级记录

4. 产品文档状态:
   └── 重新扫描并更新状态标记

5. 变更对齐检查（新增）:
   ├── 扫描 docs/changes/ 目录下所有未归档变更（排除 docs/changes/archive/）
   ├── 读取每个变更的 .status.md 获取当前阶段列表
   ├── 读取 core-mechanisms/01-project-types.md §1.3 中的当前阶段定义
   ├── 对每个变更逐一对比阶段列表与当前阶段定义
   ├── 项目类型匹配：前后端项目使用 11 阶段列表，纯后端项目使用 9 阶段列表
   ├── 缺失阶段检测 → 标记 "⚠️ 变更 {change-name} 缺少阶段: {阶段名}"
   ├── 多余阶段检测 → 标记 "ℹ️ 变更 {change-name} 包含已废弃阶段: {阶段名}"
   ├── 阶段顺序变更检测 → 标记 "ℹ️ 变更 {change-name} 阶段顺序不同: {具体差异}"
   ├── 输出对齐报告摘要：检测到的变更总数、对齐的变更数、存在差异的变更数及清单
   ├── SHALL NOT 自动修改任何 .status.md 文件
   └── 如存在差异，提示用户"是否需要协助修复不一致的变更"

6. 不重复询问:
   ├── 产品文档已存在 → 不询问逆向分析
   ├── 产品文档仍缺失 → 再次询问
   └── 项目类型记录与扫描一致 → 静默复用，不询问项目类型

7. 无未归档变更时:
   └── 跳过对齐检查，不输出任何对齐报告
```

---

## 与其他 Skill 的关系

- **独立 Skill**：可在项目启动时独立调用
- **关联 Skill**：工具推荐结果影响 `kflow-prototype-design`（需要 prototype-gen 角色 Skill ≥1 个：huashu-design / frontend-design）和 `kflow-e2e-test`（需要 playwright-cli）
- **输出给**：所有后续阶段 Skill 可参考 toolchain.md 中的工具推荐
- **前置阶段**：无
- **后续阶段**：`kflow-guide`（流程指引）、`kflow-explore`（设计探索）
- **CLAUDE.md 注入**：注入项目画像、变更流程强制规则（跨 skill 路由约束与用户接口约定）与 Skill 改进建议自动捕获，并为项目创建不受管的「项目自定义规则」区块；流程规则以「新变更由 `kflow-explore` 承接 + 阶段自动衔接 + 恢复/推进双入口 + 变更名模式禁止 Plan Mode 拦截」为骨架，SHALL NOT 要求变更先经 `kflow-guide`，亦 SHALL NOT 禁止直接调用阶段 Skill

---

## CLAUDE.md 注入规范

### marker 注入架构

kflow-init 使用三个受管的 `## ` section marker 分别管理「项目画像」、「变更流程强制规则」和「Skill 改进建议自动捕获」，并额外创建一个不受管的「项目自定义规则」区块：

```
CLAUDE.md 结构（init 注入后）:

  (用户原始内容)
  ...
  ## 项目画像                          ← 受管 marker 1
  > 来源: kflow-init ...
  - 项目类型 / 技术栈 / ...
  
  ## 变更流程强制规则                   ← 受管 marker 2
  > 来源: kflow-init ...
  - guide 流转规则 / 用户接口约定

  ## Skill 改进建议自动捕获             ← 受管 marker 3
  > 来源: kflow-init ...
  - 三种触发模式和处理规则

  ## 项目自定义规则                     ← 不受管区块（创建后不读取、不替换）
  > 来源: kflow-init 创建 | 维护方: 项目自身
```

受管 marker 的区块内容由 kflow-init 按版本判据替换；「项目自定义规则」区块仅在不存在时创建，其内容归属项目，不参与版本比较与替换。

### 注入内容格式 — 项目画像

```markdown
## 项目画像

> **来源**: kflow-init | **扫描时间**: {YYYY-MM-DD HH:MM}

| 字段 | 值 |
|------|-----|
| 项目类型 | {前后端项目 / 纯后端项目} |
| 语言 | {TypeScript / Python / Java / ...} |
| 框架 | {React + Express / FastAPI / Spring Boot / ...} |
| 数据库 | {PostgreSQL / MySQL / MongoDB / 待确定} |
| 构建工具 | {Vite / Webpack / Maven / pip / ...} |
| 关键目录 | {src/controllers, src/models, src/services, ...} |
| 入口文件 | {src/index.ts, src/main.py, ...} |

### 产品文档状态

| 文档 | 状态 |
|------|------|
| CONTEXT.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/index.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/functional-designs/ | 前后端：✅ {N}个模块 / ❌ 不存在；纯后端：✅ {N}篇 / ❌ 不存在 |
| docs/designs/detailed-designs/architecture.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/detailed-designs/data-model.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/detailed-designs/api-catalog.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/detailed-designs/nfr-baseline.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/detailed-designs/config-items.md | ✅ 已就绪 / ⚠️ 建议补充 |
| docs/designs/detailed-designs/error-handling.md | ✅ 已就绪 / ⚠️ 建议补充 |
| docs/service-guide.md | ✅ 已就绪 / ❌ 不存在 |
```

> **「项目类型」行的用途契约**：该行是项目类型项目级记录的**唯一真源**，供变更创建链路（`kflow-guide`、`kflow-explore`）读取，读取优先级高于 `docs/toolchain.md` 头部的同名字段。该区块为受管 marker，re-init 时整体替换——非 kflow-init 的写入方 SHALL NOT 向本区块补写内容（残缺区块会与替换逻辑冲突）。CLAUDE.md 不存在时该区块缺省，读取侧回退 `docs/toolchain.md`。

### 注入内容格式 — 变更流程强制规则

```markdown
## 变更流程强制规则

> **来源**: kflow-init 自动生成
> **模板版本**: {kflow-init 的 version 值}
> **生成时间**: {YYYY-MM-DD HH:MM}

本项目使用 KFlow Skills 体系管理所有变更。以下为强制规则：

1. **新变更由 `kflow-explore` 承接**：变更类型分类、变更命名、档位初判与冲突预检均在该阶段完成，无需先经 `kflow-guide` 做创建前指引
2. **阶段完成后自动衔接下一阶段**：阶段 Skill 的 COMPLETE 步骤完成后直接调度下一阶段 Skill，SHALL NOT 提示用户输入推进指令（如「继续 {change-name}」）；阶段自有的人工评审门控照常执行
3. **中断恢复使用「恢复 {change-name}」**：由 `kflow-resume` 执行完整断点恢复流程
4. **「继续 {change-name}」为轻量推进**：读取变更状态后直接调度当前/下一阶段 Skill，不执行重恢复流程
5. **变更名模式禁止 Plan Mode 拦截**：用户输入匹配「恢复/resume + 变更名」或「继续 + 变更名」时，SHALL NOT 进入 Plan Mode，直接进入 Skill 路由链；此规则优先级高于 Plan Mode 自动触发
6. **流程阶段**: 设计探索 -> 原型设计(可选) -> 详细设计 -> 计划 -> 编码 -> 代码审查 -> 接口单元测试 -> E2E测试(前后端) -> 集成测试 -> 审计 -> 归档
7. **查看状态**: 使用「状态」「进度」关键词触发 `kflow-status` 查看变更状态
```

> **规则条目契约**：条目 1 与 `kflow-explore` 的能力边界一致（变更类型分类、命名、档位初判、冲突预检均在其 INIT/CLASSIFY/TIER/CONTEXT 步骤内完成）；条目 2 与 `phase-auto-transition` 能力一致（自动衔接免除的仅为「提示用户输入推进指令」，阶段自有的人工评审门控照常执行）；条目 3、4 与 `intent-priority-rules` 的推进/恢复分流一致；条目 5 与 `resume-plan-mode-bypass` 能力一致（两条变更名路径均不进入 Plan Mode）。该 section SHALL NOT 出现要求所有变更先经 `kflow-guide` 的规则，亦 SHALL NOT 出现禁止直接调用阶段 Skill 的规则。

**模板版本取值**：`{kflow-init 的 version 值}` 取自本 Skill front matter 的 `version` 字段（消费方为 `.claude/skills/kflow-init/SKILL.md`），该字段由本仓库在归档后运行 `scripts/sync-version.sh` 统一同步；SHALL NOT 引用消费方项目中可能不存在的文件（如仓库根 `VERSION` 文件）。

**作用域边界**：该 section 只承载跨 skill 的路由约束、用户接口约定与流程概览，包括变更名模式的 Plan Mode 绕过禁令（`resume-plan-mode-bypass` 能力要求由 kflow-init 注入）。归档后的 git commit 询问由 `kflow-archive` 的归档流程承载，非 git 仓库时的 git init 询问由本 Skill 的 GIT INIT 步骤承载——二者均为 skill 在自身执行流程中完成的步骤，SHALL NOT 写入该 section。该 section 中 SHALL NOT 出现技能开发仓库特有的脚本、产物目录与文件。

### 注入内容格式 — Skill 改进建议自动捕获

```markdown
## Skill 改进建议自动捕获

> **来源**: kflow-init 自动生成
> **模板版本**: {kflow-init 的 version 值}
> **生成时间**: {YYYY-MM-DD HH:MM}

当 AI 对话中出现以下触发模式时，自动记录到 `docs/skill-suggestion.md`：

1. **阻塞模式「因...无法...」**：如"因服务未启动无法执行测试" → 记录阻塞原因和失败的执行路径
2. **因果链「因...导致...」**：如"因设计错误导致测试全部失败" → 记录因果链和受影响的阶段
3. **用户纠正后 AI 附和**：用户纠正 AI 行为后，AI 回复中包含「你说得对」「你是对的」等附和 → 记录用户的纠正内容（非 AI 附和）

记录格式：触发场景、具体内容、改进建议、时间戳、来源（kflow-init 注入规则）。
注意：业务功能问题记录为缺陷参考，Skill 执行机制问题记录为 skill-suggestion。
```

**模板版本取值**：与「变更流程强制规则」一致，取自本 Skill front matter 的 `version` 字段。

### 注入内容格式 — 项目自定义规则（不受管区块）

```markdown
## 项目自定义规则

> **来源**: kflow-init 创建 | **维护方**: 项目自身
> 本区块由项目自行维护，kflow-init 不读取、不替换、不删除其内容。

（在此填写项目自身的规则约定）
```

该区块仅在 CLAUDE.md 不含 `## 项目自定义规则` marker 时创建，创建位置与既有区块一致（追加到 CLAUDE.md 末尾）。该区块不纳入 kflow-init 的模板替换范围，用户在其中的内容不会被 re-init 覆盖，也不构成 kflow-init 的强制规则。

### marker 检测与幂等策略

```
注入幂等逻辑（受管 marker 3 个 + 不受管区块 1 个）:

Marker 1: `## 项目画像`
  1. 检测:
     ├── Read CLAUDE.md
     ├── Grep: "## 项目画像"
     ├── 未找到 → 追加模式: 在 CLAUDE.md 末尾添加 section
     └── 已找到 → 替换模式: 替换 `## 项目画像` 到下一个 `## ` 之间的内容
  2. 更新策略:
     ├── 重新扫描所有画像字段
     ├── 更新扫描时间戳
     └── 保留其他 section 不变

Marker 2: `## 变更流程强制规则`
  1. 检测:
     ├── Grep: "## 变更流程强制规则"
     ├── 未找到 → 追加模式
     └── 已找到 → 读取区块版本行，与本 Skill front matter 的 `version` 比较
  2. 更新策略:
     ├── 未读到版本行（旧版模板产物 / 用户删改）→ 视为版本不同 → 全量替换
     ├── 读到但无法解析为版本号 → 视为版本不同 → 全量替换
     ├── 读到且等于当前 version → 仅更新生成时间戳
     └── 读到且不等于当前 version → 全量替换

Marker 3: `## Skill 改进建议自动捕获`
  1. 检测:
     ├── Grep: "## Skill 改进建议自动捕获"
     ├── 未找到 → 追加模式: 在 CLAUDE.md 末尾添加 section
     └── 已找到 → 读取区块版本行，与本 Skill front matter 的 `version` 比较
  2. 更新策略:
     ├── 版本相同 → 不更新（此规则稳定后不变化）
     └── 版本不同 / 未读到 / 无法解析 → 全量替换

项目自定义规则区块: `## 项目自定义规则`（不受管）
  1. 检测:
     ├── Grep: "## 项目自定义规则"
     ├── 未找到 → 创建区块（追加到 CLAUDE.md 末尾）
     └── 已找到 → 跳过
  2. 更新策略:
     └── 不读取、不替换、不删除——不参与版本比较，内容始终归属项目

CLAUDE.md 不存在:
   └── 跳过注入（可选操作，不阻塞主流程）
```

### section 边界识别

```
替换时精确识别 section 边界:

- 起始: `## 项目画像` 或 `## 变更流程强制规则` 或 `## Skill 改进建议自动捕获`
- 结束: 下一个 `## ` 开头的行 或 EOF
- 替换: 保持 marker 行，替换 marker 后的内容到下一个 `## ` 之前
- 排除: `## 项目自定义规则` 不在替换范围内——不受管区块，其内容与相邻 marker 的边界判定互不影响
```

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
