# Proposal

## Why

在实战项目 `software-dev-agent` 上实测 100 个真实会话（980 MB transcript、659 个子代理）后，KFlow 的单变更 token 消耗达 **1.85 亿**（主会话 9.70 B cache_read + 子代理 8.58 B cache_read，合计 **18.28 B**），**输入侧与输出侧之比为 292:1**——成本几乎全部来自「上下文被反复重读」，而非产出。

进一步归因发现：**绝大部分消耗并非缺少设计，而是设计要求未落实**。

```
  设计已写明的规则                          实测执行情况
  ──────────────────────────────────────────────────────────────────
  §15.3 主 Agent 职责边界硬线：             ✗ 主 Agent 自己 Edit 生产代码
    「主 Agent = 调度 + 验收，                （frontend/src/pages/embed-workbench/
     SHALL NOT 直接执行编码/测试/审查」          index.tsx）、自己跑 8 轮 pytest
                                            → 单会话 169~254 次 Bash、66~215 次 Edit

  skill-self-contained:                     ✗ 95 个技能文件中 600,010 字符
    「references content is phase-specific    （55.1%）是逐字节完全相同的副本；
     —— 每个 skill 的副本 SHALL 只含              10 份 gates.md、8 份 repetition.md
     本阶段的章节」                              内容完全一致

  phase-file-reload:                        ✗ 主 Agent 读 detailed-design.md
    「SHALL 仅提取当前阶段相关章节」              全文（全库 468 次、7.35 MB 注入）
```

实测消耗结构：

```
  主会话 9.70 B  ← 15 个大会话占 60.5%；上下文从 28k 单调涨到 877k~1,046k，
                   到 900k+ 才触发压缩，压缩后又涨回（同一工作做两遍）
  子代理 8.58 B  ← 652 个子代理平均 122 轮/个（最长 532 轮）；单个最贵 1.41 亿
  大文档重读      ← detailed-design.md/index.md/.status.md/backend-services.md
                   等 6 个文件被注入 1,619 次，放大后约 0.82~1.2 B tokens
  references 加载 ← 46,734 字符/子代理，其中约 85% 与本阶段无关，约 0.16 B tokens
```

这四类消耗共同的根因是：**体系缺少「上下文预算」这一维度**——没有阈值、没有节流、没有「主 Agent 退场」的可强制机制，也缺少「只加载本阶段所需」的可验证落实。因此先把已写明的要求落地，再补齐缺失的强制机制。

## What Changes

### 一、主 Agent 禁手硬门控（NEW `main-agent-execution-gating`）

- 新增**阶段感知的 `PreToolUse` deny 机制**：从 `.status.md` 读取当前阶段，**执行类阶段**（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）下主 Agent 的 `Edit`/`Write` 与长输出命令（pytest/tsc/eslint/npm run\*）SHALL 被拒绝
- **设计类阶段**（explore/prototype-design/design/plan）主 Agent 是写作者，不受此门控约束
- 白名单：`.status.md`、`docs/skill-suggestion.md`；主 Agent 保留只读查询能力（Read 小文件 / Grep / Bash 只读）
- 把 `subagent-isolation-rule` 的「职责边界硬线」由**声明**升级为**可强制、可验证**的机制

### 二、子代理任务粒度上限（MOD `agent-iteration-execution`）

- 新增**按工作量分片**约束：单个子代理 SHALL NOT 承担超过 **3 个功能点**或 **10 个 TDD 步骤**；超限即返回并落盘，由主 Agent 开启新子代理续做
- 与既有「prompt SHALL NOT 包含轮数上限数值」的口径**显式区分**——约束对象是**工作量**而非轮次，原条款的意图（禁止为凑轮次而跑）保持不变

### 三、references 按阶段切片（MOD `skill-self-contained`、`layered-context-loading`）

- 把 `skill-self-contained` 已有的「references content is phase-specific」从 **仅 hooks.md** 扩展到**全部共享 references 文件**（gates.md / state-values.md / repetition.md / self-review.md / phase-transition.md / service-lifecycle.md）
- `layered-context-loading` 的加载粒度由「阶段类型」（基础层/执行层/服务层/创意层）**下沉到「具体阶段 + 子代理职责」**
- 切片后各 skill 的副本自然分化，**55% 的逐字节副本大部分消失**
- 删除两条实测未执行的无效要求：子代理读自身 `SKILL.md`（点名 40 次、执行 0 次）、`tdd-checklist.md`（执行率 50%）

### 四、产物读取纪律（MOD `large-doc-splitting`、`incremental-reload`，NEW `status-file-layering`）

- `large-doc-splitting` 新增**按需分片读取**要求：SHALL NOT 对 4 组拆分文档整体 Read，SHALL 按索引定位后读取目标分册或行区间
- `incremental-reload` 的「已验证文件标记 + 跳过全文读取」由**仅 RELOAD 清单**扩展到**全部阶段产物读取**（实测 1,429 次 Read 中 73.2% 是重复读取）
- 新增 `.status.md` **分层结构**：`.status.md` 仅承载当前状态（目标 < 100 行），历史阶段记录移入 `status-log.md`，仅在恢复场景读取

### 五、上下文预算与压缩阈值（NEW `context-budget-management`）

- kflow-init SHALL 在目标项目 `.claude/settings.json` 写入 `autoCompactWindow: 300000`，使自动压缩在 300k 触发而非等到近 1M
- 新增**阶段边界节流规则**：阶段收尾时 SHALL 主动将当前阶段结论落盘为交接摘要，使下一阶段以子代理/新上下文承接（不要求用户执行任何命令）——**零用户负担**

### 六、修订记录留存边界（NEW `artifact-revision-record-retention`）

实测发现规范的一处**不匹配**——`02-directory-structure.md:359` 强制「每次增补必须更新版本号和修订记录」，`09-phase-hooks.md:227` 读取侧只要「最新修订记录」，而**全设计文档中没有任何留存边界规定**。结果：文档头部挂着从 v1.0.0 起的全量历史。

```
 文件                                        总量        修订/历史部分     占比
 docs/designs/functional-designs/index.md   117.7 KB      64.2 KB        54.6%
 CONTEXT.md                                  64.0 KB      29.9 KB        46.7%
 docs/changes/index.md                       47.9 KB      20.3 KB        42.4%
 .status.md（活跃变更）                      64.7 KB      10 个阶段状态追加块
```

- 文档头部修订记录 SHALL 仅保留最近 **3 条**，超出部分移入历史承载位置（变更级 `revision-history.md` / 产品级 `docs/designs/changelog.md`）
- 历史承载位置 SHALL NOT 参与常规读取
- 归档的设计合并步骤 SHALL 自动执行该边界——**新变更产生的文档从此不再膨胀，用户无需任何操作**

### 七、产品级文档纳入拆分范围（MOD `large-doc-splitting`）

现有拆分机制只覆盖**变更级 4 组文档**；产品级 `docs/designs/**`、`docs/open/**` 不在范围内，也没有章节索引。

```
 软件开发数字人开放集成指南.md   182.0 KB   实测被读 100 次、901 KB 注入
 design-prompt.md              152.9 KB
 nfr-baseline.md                88.1 KB
 data-model.md                  81.4 KB
 error-handling.md              72.7 KB
 api-catalog.md                 65.1 KB
```

- 产品级文档 **> 30 KB** SHALL 提供章节索引；**> 80 KB** SHALL 拆分为目录化结构
- 拆分 SHALL 在同一步完成引用更新（项目文档 / Skill 规则 / 脚本），不留断链
- 术语表（`CONTEXT.md`）例外：保持单文件，提供按模块/首字母的术语索引

### 八、存量文档优化入口（NEW `doc-optimize-skill`）

第六、七两条定义的是**规则与自动机制**——它们只作用于新变更产生的文档。存量文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`、活跃变更目录）需要一个显式入口。

- 新增 `kflow-doc-optimize`——**独立维护 Skill（非流程阶段）**，与 `kflow-verify` / `kflow-bug-triage` 同层
- 流程：扫描 → 识别 → 输出优化清单 → 用户确认执行范围 → 执行 → 引用完整性校验 → 报告
- 只搬移、拆分与建索引，**SHALL NOT 改写文档实质内容**
- 触发：`/kflow-doc-optimize`，或说「文档优化」「文档瘦身」「拆分文档」「清理修订记录」，或经 `kflow-guide` 路由
- `kflow-guide` SHALL 在没有活跃变更时同样能路由到该 Skill

## Capabilities

### New Capabilities

- `main-agent-execution-gating`: 执行类阶段主 Agent 工具禁用的阶段感知硬门控——门控判定来源（`.status.md` 当前阶段）、白名单、黑名单命令模式、强制机制、与职责边界硬线的衔接
- `context-budget-management`: 上下文预算与节流——项目级压缩阈值配置、阶段边界主动节流规则、上下文基线的度量口径
- `status-file-layering`: `.status.md` 分层结构——当前状态文件与历史日志文件的字段划分、写入时机、读取场景边界
- `artifact-revision-record-retention`: 修订记录留存边界——头部保留条数、历史承载位置的分层划分、读取侧只消费最新修订、归档合并时的自动执行
- `doc-optimize-skill`: 存量文档优化 Skill——定位与触发、扫描识别与清单输出、执行前确认、内容保真的搬移与拆分、引用完整性校验

### Modified Capabilities

- `skill-self-contained`: 「references content is phase-specific」的适用范围由 hooks.md 扩展到全部共享 references 文件，并明确切片规则（按阶段划分章节归属，副本为切片后的结果）
- `layered-context-loading`: 加载粒度由「阶段类型」下沉到「具体阶段 + 子代理职责」，加载清单精确到章节级别
- `incremental-reload`: 「已验证文件标记 + 跳过全文读取」的适用范围由 RELOAD 清单文件扩展到全部阶段产物读取，新增同一会话内读取去重规则
- `large-doc-splitting`: 新增按需分片读取规则（禁止整体读取已拆分文档）；适用范围扩展到产品级文档，新增章节索引与体积分片两档阈值
- `agent-iteration-execution`: 新增子代理任务粒度上限（功能点数 / TDD 步数）要求，并在重复制 prompt 规范中显式区分「工作量上限」与「轮数上限」
- `subagent-isolation-rule`: 主 Agent 职责边界硬线新增强制机制引用（由 `main-agent-execution-gating` 承载）与验证口径
- `devflow-guide`: 新增 `kflow-doc-optimize` 的路由入口与流程概览条目
- `archive-design-merge`: 变更记录维护新增「合并时裁剪产品级文档修订记录」与「同步维护章节索引并触发拆分」两项职责

## Impact

### 规范文档（`docs/designs/`）

- `core-mechanisms/07-agent-model.md`：§15.3 主 Agent 职责边界硬线补强制机制；§17 子代理上下文分层加载的粒度下沉与切片规则
- `core-mechanisms/09-phase-hooks.md`：阶段边界节流与 RELOAD 清单的切片对齐
- `core-mechanisms/03-status-and-tasks.md`：`.status.md` 分层结构定义
- `core-mechanisms/02-directory-structure.md`：`status-log.md` 与 `revision-history.md` 落位；补入修订记录留存边界
- `core-mechanisms/04-gates-and-transitions.md`：归档设计合并步骤补入裁剪、索引维护与拆分触发
- `skills/kflow-*.md`：7 个执行类阶段的主 Agent 禁手声明、读取纪律声明；新增 `kflow-doc-optimize` 设计规格
- 全部产出文档模板（`templates/`）：修订记录章节补入留存边界说明
- `overview.md`、`index.md`：新增「上下文预算」「文档留存边界」设计决策行

### 可运行 Skills（`skills/`）

- **新增** `kflow-doc-optimize`（SKILL.md + references）
- `kflow-code`/`kflow-code-review`/`kflow-api-test`/`kflow-e2e-test`/`kflow-integration-test`/`kflow-plan`/`kflow-bug-fix` 的 `SKILL.md`：禁手声明与子代理粒度上限
- 上述 7 个 skill 的 `references/repetition.md`：prompt 规范新增工作量分片条款
- 10 个 skill 的 `references/gates.md`、8 个的 `references/repetition.md`、10 个的 `references/state-values.md`、3 个的 `references/self-review.md`、11 个的 `references/phase-transition.md`：**按阶段切片**
- 6 个下游 skill 的 `references/hooks.md`：RELOAD 清单与切片对齐
- `kflow-guide/SKILL.md`：新增 `kflow-doc-optimize` 路由与流程概览条目
- `kflow-archive/SKILL.md`：设计合并步骤补入裁剪、索引维护与拆分触发
- 全部 18+1 个 `SKILL.md`：`version` 字段由 `scripts/sync-version.sh` 同步

### 脚本（`scripts/`）

- `sync-references.sh`：由「校验副本一致性」升级为「**从切片源生成副本 + 校验**」——开发期单一权威源，生成物仍是各 skill 自包含的 `references/`，安装后零外部依赖不变
- `package-skills.sh`：无需改动（仍逐个复制 `references/`）

### 消费者（`software-dev-agent`）

- `.claude/settings.json`：新增 `autoCompactWindow`
- **`CLAUDE.md` 的项目自定义规则区块需增加例外**：该项目当前以「项目自定义规则」区块自维护一条适用边界——「kflow 系列 Skills 仅在本项目的功能变更与缺陷修复场景调用，其余工作（含规则/文档维护）一律不调用」。该规则会把 `kflow-doc-optimize` 一并挡在门外，故须在该区块中为它增加例外声明。**该区块由项目自行维护、kflow-init 不覆盖**，因此这是一处项目侧改动，不在 Skill 体系可自动生效的范围内
- `docs/changes/{change}/.status.md` → 分层为 `.status.md` + `status-log.md`（历史变更保持不变，新变更按新结构）
- **存量文档优化**（由 `kflow-doc-optimize` 执行，一次性）：
  - `CONTEXT.md` 64.0 → 约 34 KB（含术语索引）
  - `docs/designs/functional-designs/index.md` 117.7 → 约 53 KB
  - `docs/changes/index.md` 47.9 → 约 28 KB
  - `docs/open/软件开发数字人开放集成指南.md` 182.0 KB → 目录化拆分
  - `docs/designs/detailed-designs/{nfr-baseline,data-model,error-handling,api-catalog}.md`（65~88 KB）→ 章节索引，跨阈值的拆分
  - 活跃变更目录的 `.status.md` 与产物修订记录

### 依赖与验证

- **前置**：无。本变更不依赖其他未归档变更
- **验证方式**：① 在 `software-dev-agent` 上执行一次存量文档优化，校验引用完整性；② 跑一个中等规模真实变更，用本次实测脚本（`scan.py` / `split.py` / `refcost.py`）对比 `cache_read` 总量，以 18.28 B 为基线做前后对比
- **预期**：18.28 B → 约 4.3 B（≈ 4.2x）；叠加文档留存边界与产品级拆分的读取收益后进一步下降

### 不在本次范围

- 手动 `/clear` 或任何需要用户执行命令的上下文重置方式（按用户裁决排除，全部走子代理自动隔离）
- `kflow-guide` / `kflow-resume` 的反复调用频次问题（属路由层，另案处理）
- 无效注入（`.orca/agent-hooks` 的 PreToolUse/PostToolUse）——属项目侧配置，不在 Skill 体系范围
- **归档产物未冷热分离**（归档区 31 MB / 10 个变更）：归档区不参与常规读取，仅影响目录整洁，不影响读取成本
