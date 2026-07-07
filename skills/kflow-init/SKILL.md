---
name: kflow-init
version: 0.16.0
description: Use when user needs environment initialization/初始化、环境配置、工具推荐、设置, project kickoff/项目启动, or legacy project reverse analysis/老项目逆向分析.
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
---

# 角色

环境初始化器。发现当前上下文可用 MCP servers 和 Skills，评估组合可行性，输出工具链推荐方案和 toolchain.md。扫描项目画像（技术栈、目录结构、产品文档状态）注入 CLAUDE.md。支持老项目代码逆向分析生成产品文档草稿。按需阶段，项目启动时调用。

# 任务

检测项目类型 -> 扫描三层环境能力（运行时MCP/配置settings.json/知识库推荐）-> 扫描项目画像（技术栈、目录结构、8项产品文档状态）-> 权限配置（读取 permission-model.md → 检测 settings.json → 用户确认 → 创建/追加/跳过 → 输出到 toolchain.md）-> 匹配工具推荐矩阵 -> 检测能力缺口 -> 组合可行性评估 -> 输出多方案对比 -> 用户确认方案 -> 输出 toolchain.md -> 老项目逆向分析（条件触发）-> CLAUDE.md 注入（三层 marker + skill-suggestion 自动捕获）-> Re-init 变更对齐检查（条件触发）-> 检测 git 仓库并询问是否 git init（条件触发）。

# 门控检查

此阶段为可选的入口阶段，无前置门控要求。

输出产物检查：
- `docs/toolchain.md` 文件在项目根目录 docs/ 下创建
- toolchain.md 包含各阶段推荐工具及优先级
- toolchain.md 包含环境能力扫描结果

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 项目上下文 | ✅ 必须 | 当前项目目录结构和类型 |
| 会话上下文 | ✅ 必须 | 当前会话可用的 MCP 和 Skills |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 工具链配置 | docs/toolchain.md | ✅ 必须 | 各阶段推荐工具（含优先级）、环境能力扫描结果、权限配置状态、安装建议 |
| 变更级覆盖（可选） | docs/changes/{change}/toolchain.md | 🔶 条件 | 特定变更需要不同工具链时创建，优先级高于项目级 |
| CLAUDE.md 注入（项目画像） | CLAUDE.md | 🔶 条件 | 注入「项目画像」section（技术栈、目录结构、产品文档状态），marker 检测幂等 |
| CLAUDE.md 注入（流程规则） | CLAUDE.md | 🔶 条件 | 注入/更新「变更流程强制规则」section（含 git commit 规则），marker 检测幂等 |
| CLAUDE.md 注入（skill-suggestion 捕获） | CLAUDE.md | 🔶 条件 | 注入/更新「Skill 改进建议自动捕获」section（三种触发模式），marker 检测幂等 |
| 产品文档草稿（老项目） | docs/CONTEXT.md, docs/designs/*.md, docs/service-guide.md | 🔶 条件 | 老项目产品文档缺失时，代码逆向扫描生成草稿，用户审核确认后写入 |
| CONTEXT.md 检测 | docs/CONTEXT.md | ✅ 必须 | 检测 docs/CONTEXT.md 是否存在，存在时加载词汇表，不存在时标记"待构建" |

# 环境感知层次

系统分三层感知环境能力：

| 层次 | 感知方式 | 覆盖范围 |
|------|---------|---------|
| 运行时 | 扫描当前会话 MCP 工具前缀（如 mcp__context7__*） | 已连接的 MCP servers |
| 配置 | 读取 settings.json 中配置的 MCP servers 和权限配置 | 已配置但可能未连接的 MCP、权限配置状态 |
| 知识库 | 内置推荐数据库 | 已知的推荐工具（如 /playwright-cli skill） |

# 工具推荐矩阵

## 按项目类型和阶段推荐

| 阶段 | 前后端项目 | 纯后端项目 | 优先级 |
|------|-----------|-----------|--------|
| 设计探索 | Read, Glob, Grep, AskUserQuestion | Read, Glob, Grep, AskUserQuestion | 必须 |
| 原型设计 | **多方案**（方案 A: huashu-design 一体化，推荐；方案 B: ui-ux-pro-max + huashu-design 设计驱动型；方案 C: ui-ux-pro-max + frontend-design 静态页面型） | ⏭️ 跳过 | 推荐 |
| 详细设计 | Read, Write, Edit, Agent | Read, Write, Edit, Agent | 必须 |
| 计划 | Write, Edit | Write, Edit | 必须 |
| 编码 | Bash, Read, Write, Edit, Agent | Bash, Read, Write, Edit, Agent | 必须 |
| 接口单元测试 | Bash, Read, Edit | Bash, Read, Edit | 必须 |
| E2E 测试 | **/playwright-cli skill**（首选）, playwright MCP（备选） | ⏭️ 跳过 | 推荐 |
| 集成测试 | Bash, Read, Agent | Bash, Read, Agent | 必须 |
| 缺陷修复 | Bash, Read, Edit, Agent | Bash, Read, Edit, Agent | 按需 |
| 归档 | Bash, Read, Write, Edit | Bash, Read, Write, Edit | 必须 |
| 审计 | Read, Agent | Read, Agent | 归档门控 |

**注意**：`kflow-browser-rules` 不列入推荐列表。

# 执行流程

## 总流程

```
DETECT(项目类型) -> SCAN(环境能力) -> PROFILE(项目画像) -> PERM_CONFIG(权限配置) -> MATCH(工具匹配) -> GAP(能力缺口)
    -> COMPAT(可行性评估) -> PROPOSE(多方案) -> CONFIRM(用户确认) -> OUTPUT(toolchain.md)
    -> LEGACY(老项目逆向) -> INJECT(CLAUDE.md注入) -> GITINIT(git仓库检测) -> COMPLETE
```

```
┌─────────────────────────────────────────────────────────────────┐
│                         INIT WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│  1. DETECT     检测项目类型                                      │
│     ├── 前后端项目（存在前端框架依赖）                           │
│     └── 纯后端项目（无前端工程）                                 │
│  2. SCAN       扫描环境能力                                      │
│     ├── 运行时: 检查 MCP 工具前缀                                │
│     ├── 配置: 读取 settings.json                                 │
│     ├── Skills: 扫描 .claude/skills/ 目录                        │
│     └── CONTEXT: 检测 CONTEXT.md 领域词汇表                      │
│  3. PROFILE    扫描项目画像信息                                  │
│     ├── 项目类型、语言、框架、数据库、构建工具                   │
│     ├── 关键目录、入口文件                                      │
│     └── 产品文档状态（8 项存在性检测）                           │
│  3.5 PERM_CONFIG  权限配置（新增）                               │
│     ├── 读取 skills/kflow-init/references/permission-model.md 权限声明          │
│     ├── 检测 .claude/settings.json 是否存在及权限状态            │
│     ├── 不存在 → AskUserQuestion → 创建 settings.json            │
│     ├── 已存在但缺少部分权限 → AskUserQuestion → 追加缺失权限    │
│     ├── 已齐全 → 输出"权限配置齐全 ✅"                          │
│     └── 用户拒绝 → toolchain.md 标注"权限未配置"                 │
│  4. MATCH      匹配工具推荐矩阵                                  │
│  5. GAP        检测能力缺口                                      │
│     ├── 原型设计需要 prototype-gen 角色 Skill（≥1 个：huashu-design / frontend-design）│
│     └── E2E 测试需要 playwright-cli -> 缺失时提示安装            │
│  6. COMPAT     组合可行性评估                                    │
│     ├── 检查工具间已知冲突                                      │
│     ├── 检查每个阶段覆盖度                                      │
│     └── 标注覆盖度百分比                                        │
│  7. PROPOSE    输出多方案（如适用）                              │
│     ├── 方案 A: 推荐最佳组合                                     │
│     ├── 方案 B: 备选降级方案                                    │
│     └── 方案 C: 最小必须方案                                    │
│  8. CONFIRM    用户确认方案（AskUserQuestion）                   │
│  9. OUTPUT     输出 docs/toolchain.md                            │
│ 10. LEGACY     老项目逆向分析（条件触发）                        │
│     ├── 检测产品文档缺失                                        │
│     ├── AskUserQuestion: 是否生成文档草稿？                       │
│     ├── L1 配置文件 -> L2 目录结构 -> L2.5 前端扫描 -> L3 源码语义 │
│     ├── 生成草稿 -> 用户审核确认 -> 写入                         │
│     └── 跳过 -> 标注为 ❌ 不存在                                 │
│ 11. INJECT     注入 CLAUDE.md（三层 marker）                     │
│     ├── 注入「项目画像」section                                 │
│     ├── 注入「变更流程强制规则」section                         │
│     ├── 注入「Skill 改进建议自动捕获」section                    │
│     └── CLAUDE.md 不存在 -> 跳过注入（可选）                     │
│ 12. ALIGN      Re-init 变更对齐检查（条件触发）                   │
│     ├── 扫描未归档变更的阶段列表                                  │
│     ├── 对比当前阶段定义与变更中的阶段列表                        │
│     └── 输出对齐报告（差异/缺失/新增阶段）                        │
│ 13. GIT INIT   检测 Git 仓库并询问是否初始化（条件触发）         │
│ 14. COMPLETE   完成初始化                                        │
└─────────────────────────────────────────────────────────────────┘
```

## 步骤 1：DETECT — 检测项目类型

```
项目类型检测逻辑:

1. 读取 package.json
2. 检查前端框架依赖（react, vue, angular, next, nuxt, svelte 等）
3. 扫描前端源文件（.vue, .tsx, .jsx, .svelte）
4. 扫描前端构建配置（vite.config, webpack.config 等）
5. 判定:
   ├── 任一命中 -> 前后端项目
   └── 全部不命中 -> 纯后端项目
```

## 步骤 2：SCAN — 扫描环境能力

```
环境能力扫描:

运行时感知:
├── 扫描 MCP 工具前缀（mcp__*）
├── 例: huashu-design / frontend-design Skill 存在 -> 原型设计可用
└── 列出所有已连接的 MCP servers

配置感知:
├── 读取 .claude/settings.json
├── 读取 .claude/settings.local.json
└── 提取已配置的 MCP servers

Skills 感知:
├── 扫描 .claude/skills/ 目录
└── 列出所有已安装 Skills

CONTEXT 检测:
├── 检测 docs/CONTEXT.md 是否存在
│   ├── 存在 -> 读取词汇表，标注"CONTEXT.md ✅ 已就绪"
│   └── 不存在 -> 标注"CONTEXT.md ⚠️ 待构建"
```

## 步骤 3：PROFILE — 扫描项目画像

### 项目画像字段定义

| 字段 | 类型 | 来源 | 新项目 | 老项目 |
|------|------|------|--------|--------|
| 项目类型 | 枚举（前后端/纯后端） | package.json + 源文件扫描 | ✅ 有值 | ✅ 有值 |
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

1. 项目类型: 前端框架依赖 + 源文件检测 -> 前后端 / 纯后端
2. 技术栈:
   ├── 语言: 扫描源文件扩展名 (.ts, .js, .py, .java, .go, .rs)
   ├── 框架: 从 package.json / pom.xml / requirements.txt 提取
   ├── 数据库: 扫描配置文件中的数据库连接信息
   └── 构建工具: 从构建配置文件中提取
3. 目录结构: 扫描 src/ 子目录，识别关键目录
4. 入口文件: 扫描常用入口文件名（main.*, index.*, app.*, server.*）
5. 产品文档状态: 8 项文件存在性检测
```

### 产品文档 8 项检测

详见 [references/legacy-analysis.md](references/legacy-analysis.md) — 8 项产品文档检测表及侧带检测规则。

## 步骤 3.5：PERM_CONFIG — 权限配置

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

幂等规则：仅追加缺失权限，不删除或修改已有条目，重复执行不重复添加。

## 步骤 4-6：MATCH + GAP + COMPAT

### 覆盖度计算

```
覆盖度 = 已覆盖阶段数 / 总阶段数 × 100%

兼容性检查:
├── 检查 MCP server 间端口/资源冲突
├── 检查 Skill 间功能重叠（择优推荐）
└── 降级策略: 有冲突时推荐不冲突的组合
```

## 步骤 7-8：PROPOSE + CONFIRM

### 三方案对比

- **方案 A（推荐最佳组合）**：最高覆盖度，首选工具
- **方案 B（降级方案）**：备选工具替代缺失的首选工具
- **方案 C（最小必须方案）**：仅必须阶段，跳过可选阶段

每方案标注覆盖度和风险，使用 AskUserQuestion 确认方案选择。

## 步骤 9：OUTPUT — 输出 toolchain.md

详见 [references/toolchain-template.md](references/toolchain-template.md) — 完整格式模板（环境能力扫描、阶段工具推荐、安装建议、多方案对比、变更级覆盖）。

## 步骤 10：LEGACY — 老项目逆向分析（条件触发）

### 触发条件

当 `docs/CONTEXT.md` 不存在或 `docs/designs/functional-designs/` 目录为空时，使用 AskUserQuestion 询问用户。

详见 [references/legacy-analysis.md](references/legacy-analysis.md) — 三层逆向扫描（L1 配置文件 / L2 目录结构 / L2.5 前端工程 / L3 源码语义）、生成文档草稿（10 项产品文档）、产品文档 8 项检测、用户审核确认。

## 步骤 11：INJECT — 注入 CLAUDE.md（三层 marker）

### Marker 1：项目画像

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
| docs/designs/functional-designs/ | 前后端：✅ N个模块 / ❌ 不存在；纯后端：✅ N篇 / ❌ 不存在 |
| docs/designs/technical-designs/architecture.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/technical-designs/data-model.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/technical-designs/api-catalog.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/technical-designs/nfr-baseline.md | ✅ 已就绪 / ❌ 不存在 |
| docs/designs/technical-designs/config-items.md | ✅ 已就绪 / ⚠️ 建议补充 |
| docs/designs/technical-designs/error-handling.md | ✅ 已就绪 / ⚠️ 建议补充 |
| docs/service-guide.md | ✅ 已就绪 / ❌ 不存在 |
```

### Marker 2：变更流程强制规则

```markdown
## 变更流程强制规则

> **来源**: kflow-init 自动生成
> **版本**: 参见 VERSION 文件（统一版本管理）
> **生成时间**: {YYYY-MM-DD HH:MM}

本项目使用 KFlow Skills 体系管理所有变更。以下为强制规则：

1. **所有用户变更必须首先通过 `kflow-guide` 进行流程指引**，禁止跳过 guide 直接调用阶段 Skill
2. **新变更由 guide 引导后进入 `kflow-explore`**，变更初始化（目录创建、状态文件）在 explore 阶段完成
3. **中断恢复时使用「继续 {change-name}」**，guide 将路由到 `kflow-resume` 进行精确断点恢复
4. **禁止直接调用** `kflow-code`、`kflow-plan`、`kflow-explore`、`kflow-design` 等阶段 Skill 跳过 guide 指引
5. **流程阶段**: 设计探索 -> 原型设计(可选) -> 详细设计 -> 计划 -> 编码 -> 代码审查 -> 接口单元测试 -> E2E测试(前后端) -> 集成测试 -> 审计 -> 归档
6. **查看状态**: 使用「状态」「进度」关键词触发 `kflow-status` 查看变更状态
7. **归档完成后询问是否执行 git commit**，提交信息包含变更名称和归档日期；若确认提交，则先执行版本自增和打包（读取 VERSION → 版本自增判定（Major 手动/Minor 新功能/Patch 修复）→ 更新 VERSION → 打包为 targets/kflow-devflow-skills-x.x.x.zip）再将 VERSION、targets/ 和归档产物一并提交
8. **首次 init 时若目录非 git 仓库，询问是否执行 git init**
```

### Marker 3：Skill 改进建议自动捕获

```markdown
## Skill 改进建议自动捕获

> **来源**: kflow-init 自动生成 | **版本**: 1.0.0

当 AI 对话中出现以下触发模式时，自动记录到 `docs/skill-suggestion.md`：

1. **阻塞模式「因...无法...」**：如"因服务未启动无法执行测试" → 记录阻塞原因和失败的执行路径
2. **因果链「因...导致...」**：如"因设计错误导致测试全部失败" → 记录因果链和受影响的阶段
3. **用户纠正后 AI 附和**：用户纠正 AI 行为后，AI 回复中包含「你说得对」「你是对的」等附和 → 记录用户的纠正内容（非 AI 附和）

记录格式：触发场景、具体内容、改进建议、时间戳、来源（kflow-init 注入规则）。业务功能问题记录为缺陷参考，Skill 执行机制问题记录为 skill-suggestion。
```

### 幂等策略

```
双层注入幂等逻辑:

Marker 1: "## 项目画像"
  1. 检测:
     ├── Read CLAUDE.md
     ├── Grep: "## 项目画像"
     ├── 未找到 -> 追加模式: 在 CLAUDE.md 末尾添加 section
     └── 已找到 -> 替换模式: 替换 "## 项目画像" 到下一个 "## " 之间的内容
  2. 更新策略:
     ├── 重新扫描所有画像字段
     ├── 更新扫描时间戳
     └── 保留其他 section 不变

Marker 2: "## 变更流程强制规则"
  1. 检测:
     ├── Grep: "## 变更流程强制规则"
     ├── 未找到 -> 追加模式
     └── 已找到 -> 替换模式（含版本比较）
  2. 更新策略:
     ├── 版本相同 -> 仅更新时间戳
     └── 版本不同 -> 替换为最新版本（含最新 git 规则）

Marker 3: "## Skill 改进建议自动捕获"
  1. 检测:
     ├── Grep: "## Skill 改进建议自动捕获"
     ├── 未找到 -> 追加模式
     └── 已找到 -> 替换模式
  2. 更新策略:
     ├── 版本相同 -> 不更新（此规则稳定后不变化）
     └── 版本不同 -> 替换为最新版本

3. CLAUDE.md 不存在:
   └── 跳过注入（可选操作，不阻塞主流程）
```

### section 边界识别

```
替换时精确识别 section 边界:

- 起始: "## 项目画像" 或 "## 变更流程强制规则" 或 "## Skill 改进建议自动捕获"
- 结束: 下一个 "## " 开头的行 或 EOF
- 替换: 保持 marker 行，替换 marker 后的内容到下一个 "## " 之前
```

## 步骤 12：ALIGN — Re-init 变更对齐检查（条件触发）

> **来源**: refine-skill-execution-rules 变更。Skill 体系升级后，未归档变更可能停留在旧阶段列表中。Re-init 时输出对齐报告，帮助用户了解需要调整的地方。

```
Re-init 变更对齐检查:

1. 扫描未归档变更:
   ├── Glob: docs/changes/*/
   └── 排除 docs/archive/ 下的变更

2. 对每个未归档变更:
   ├── 读取 .status.md 中的阶段状态表
   ├── 对比当前 Skills 体系定义的阶段列表
   ├── 检测:
   │   ├── 缺失阶段（当前体系有但变更中不存在）
   │   ├── 新增阶段（变更中已标记完成但当前体系已移除）
   │   └── 阶段名称变更（旧名称 vs 新名称）
   └── 输出对齐报告

3. 输出格式:
   ## Re-init 变更对齐报告

   | 变更名称 | 当前阶段 | 缺失阶段 | 状态变更 | 建议操作 |
   |---------|---------|---------|---------|---------|
   | {change} | {stage} | {missing} | {changed} | {action} |

4. 不自动修改任何变更的 .status.md（仅输出报告）
5. 用户可根据报告手动调整或通过 kflow-guide 路由到正确阶段
```

## 步骤 13：GIT INIT — 检测 Git 仓库并询问是否初始化（条件触发）

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

## 步骤 14：COMPLETE — 完成初始化

输出初始化完成摘要，包含：项目类型、工具链覆盖度、产品文档状态、CLAUDE.md 注入状态。

# Re-init 幂等更新策略

重新执行 kflow-init 时：

```
幂等更新逻辑:

1. 项目画像 section:
   ├── 重新扫描所有画像字段
   ├── 更新扫描时间戳
   └── 保留用户手动修改的其他 CLAUDE.md 内容

2. 流程规则 section:
   ├── 检查版本号
   ├── 版本相同 -> 仅更新时间戳
   └── 版本不同 -> 替换为最新版本（含新增 git 规则）

3. 产品文档状态:
   └── 重新扫描并更新状态标记

4. 不重复询问:
   ├── 产品文档已存在 -> 不询问逆向分析
   └── 产品文档仍缺失 -> 再次询问
```

# 与其他 Skill 的关系

- **独立 Skill**：可在项目启动时独立调用
- **关联 Skill**：工具推荐结果影响 `kflow-prototype-design`（需要 prototype-gen 角色 Skill ≥1 个）和 `kflow-e2e-test`（需要 playwright-cli）
- **输出给**：所有后续阶段 Skill 可参考 toolchain.md 中的工具推荐
- **前置阶段**：无
- **后续阶段**：`kflow-guide`（流程指引）、`kflow-explore`（设计探索）
- **CLAUDE.md 注入**：注入项目画像和变更流程强制规则（含 git 规则），引导后续所有变更通过 `kflow-guide` 流转

# 核心提醒

- toolchain.md 是唯一必须输出文件，其他均为条件产物
- 三层环境感知（运行时/配置/知识库）确保工具推荐覆盖全面
- 逆向生成的文档必须标注"由 AI 逆向分析生成，待人工审核"
- 三层 marker 注入确保幂等：同版本不重复写入，仅更新时间戳（项目画像 / 流程规则 / skill-suggestion 捕获）
- Re-init 不重复询问已有产品文档
- git init 失败不阻塞 init 流程
- CLAUDE.md 不存在时跳过注入，不阻塞主流程
- `kflow-browser-rules` 不列入推荐列表

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
