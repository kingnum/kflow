---
name: kflow-doc-optimize
version: 0.30.0
description: Use when user needs document optimization/文档优化、文档瘦身、拆分文档、清理修订记录、文档体积治理, or wants to trim revision records and split oversized docs in an existing project. 独立维护 Skill（非流程阶段）——扫描产品级与活跃变更级文档，按阈值识别修订记录超量与超大文档，经用户确认后仅搬移、拆分与建索引，并校验引用完整性。不写入变更阶段状态。
license: MIT
triggers:
  - 文档优化
  - 文档瘦身
  - 拆分文档
  - 清理修订记录
  - 文档体积
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - AskUserQuestion
---

# 角色

文档优化器（独立维护工具，非流程阶段）。对项目中已生成的**存量文档**执行修订记录裁剪与大文档拆分，并保证优化后的引用完整、内容不失真。可在任意时刻被调用，不要求存在活跃变更。

# 任务

扫描文档（SCAN）→ 输出优化清单（REPORT）→ 用户确认执行范围（CONFIRM）→ 仅搬移、拆分与建索引（EXECUTE）→ 引用完整性校验并输出报告（VERIFY）。

# 触发时机

| 触发方式 | 说明 |
|---------|------|
| 手动调用 | 用户直接调用 `/kflow-doc-optimize`，或说「文档优化」「文档瘦身」「拆分文档」「清理修订记录」「文档体积」 |
| kflow-guide 路由 | guide 识别上述关键词后路由到此；**无活跃变更时同样可路由** |
| 自动触发 | 无——本 Skill 不由任何阶段自动调用 |

# 定位与边界

| 维度 | 规则 |
|------|------|
| 定位 | **独立维护 Skill（非流程阶段）**，与 `kflow-verify` / `kflow-bug-triage` 同层 |
| 作用域 | **项目级**——`CONTEXT.md`、`docs/designs/**`、`docs/open/**` 与 `docs/changes/` 下的活跃变更产物 |
| 阶段状态 | SHALL NOT 写入任何变更的阶段状态；`.status.md` 阶段状态表 SHALL NOT 被修改 |
| 产出 | 以独立优化报告承载，SHALL NOT 登记进变更产物清单 |
| 适用边界 | 作为项目级文档维护工具，**不受**「KFlow Skills 仅适用于功能变更与缺陷修复」这一变更流程适用边界的排除 |
| 阅读前提 | 不依赖 `.status.md` 阶段状态，也不修改它 |

> **为什么是独立 Skill 而非扩展 `kflow-verify`**：`kflow-verify` 是变更级、依赖活跃变更、修复目标是路由到阶段 REVISION；本 Skill 是项目级、可无活跃变更、修复方式是就地搬移与拆分。二者作用域与产物边界不同。

# 流程

```
SCAN → REPORT → CONFIRM → EXECUTE → VERIFY
```

```
┌─────────────────────────────────────────────────────────────┐
│                 DOC OPTIMIZE WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│  1. SCAN     → 扫描产品级与活跃变更级文档，按阈值识别       │
│  2. REPORT   → 输出优化清单（路径/类型/体积/方式/预计体积/引用）│
│  3. CONFIRM  → AskUserQuestion：全部执行 / 部分执行 / 不执行 │
│  │             └── 无优化项 → 报告「无需优化」并终止          │
│  4. EXECUTE  → 仅搬移、拆分与建索引（不改写正文）            │
│  │   ├── 执行前产出受影响引用清单并留档                      │
│   │   ├── 修订记录裁剪 → 历史承载位置                        │
│  │   └── 大文档拆分 → 目录化结构 + index.md                  │
│  5. VERIFY   → 更新并校验全部受影响引用                      │
│  │   ├── 存在无法解析的引用 → 报告并停止，不得静默通过       │
│   │   └── 通过 → 输出优化报告                                │
└─────────────────────────────────────────────────────────────┘
```

## 步骤 1：SCAN — 扫描与识别

**扫描范围**：

| 范围 | 说明 |
|------|------|
| 产品级文档 | `CONTEXT.md`、`docs/designs/**`、`docs/open/**` |
| 变更级文档 | `docs/changes/` 下的活跃变更产物（`.status.md` 与 `status-log.md` 除外） |
| 排除 | 已归档变更目录（`docs/changes/archive/**`） |

**识别规则**：

| 问题类型 | 判定 |
|---------|------|
| 修订记录超量 | 文档头部修订记录条数 > **3** |
| 超出分片阈值 | 单文件体积 > **80 KB** |
| 缺少章节索引 | 单文件体积 > **30 KB** 且未提供章节索引 |

**术语表例外**：`CONTEXT.md` 不拆分——保持单文件，提供按模块或按首字母的术语索引，读取侧按索引定位到目标术语所在区间。

**已符合边界**：扫描识别出的文档若已满足留存边界与体积规则，SHALL 被排除且不产生副作用；重复执行时已优化的文档不再进入清单。

**执行助手**（推荐用脚本完成扫描，避免人工遗漏）：

```bash
python skills/kflow-doc-optimize/scripts/scan_docs.py --root <项目根>
```

脚本按上述范围与阈值输出 Markdown 优化清单；加 `--json` 可输出结构化结果供后续步骤消费。

详见 [references/scan-rules.md](references/scan-rules.md) — 阈值判定细则与问题类型识别表。

## 步骤 2：REPORT — 输出优化清单

清单每一项 SHALL 包含：文档路径、问题类型、当前体积、优化方式、预计优化后体积、受影响的引用位置。

| 字段 | 说明 |
|------|------|
| 文档路径 | 相对项目根的路径 |
| 问题类型 | 修订记录超量 / 超出分片阈值 / 缺少章节索引 |
| 当前体积 | 单文件大小（KB）或修订记录条数 |
| 优化方式 | 裁剪修订记录 / 拆分目录化 / 建立章节索引 / 建立术语索引 |
| 预计优化后体积 | 按留存边界或拆分规则估算 |
| 受影响的引用位置 | 引用该文档的项目文档、Skill 规则与脚本位置 |

## 步骤 3：CONFIRM — 执行前确认

> **强制门控**：本 Skill SHALL 在任何写入动作前将优化清单提交用户确认，禁止未经确认直接执行。

AskUserQuestion 选项：

| 选项 | 行为 |
|------|------|
| 全部执行 | 执行清单中全部项 |
| 部分执行 | 仅执行用户所选项；未选项 SHALL NOT 被修改 |
| 不执行 | 终止，不产生任何写入 |

**无优化项时**：报告「无需优化」并终止，SHALL NOT 发起确认询问。

## 步骤 4：EXECUTE — 执行与内容保真

> **核心约束**：本 Skill 执行优化时 SHALL 仅搬移、拆分与建立索引，**SHALL NOT 改写、删减或合并文档的实质内容**。

**执行前留档**：执行前 SHALL 产出受影响引用清单并写入 `docs/doc-optimize-references.md`，记录全部受影响引用及其原路径，以备反向还原（存量优化不可自动回滚）。

```bash
# 逐项留档（对清单中每个待优化文档执行一次）
python skills/kflow-doc-optimize/scripts/check_refs.py find --root <项目根> --target <被优化文档路径> \
  --write docs/doc-optimize-references.md
```

拆分完成后更新引用（先 dry-run 确认范围，再 `--apply`）：

```bash
python skills/kflow-doc-optimize/scripts/check_refs.py replace --root <项目根> \
  --old docs/open/guide.md --new docs/open/guide/index.md
python skills/kflow-doc-optimize/scripts/check_refs.py replace --root <项目根> \
  --old docs/open/guide.md --new docs/open/guide/index.md --apply
```

| 动作 | 保真约束 |
|------|---------|
| 修订记录裁剪 | 被移出的记录原样进入历史承载位置；保留在头部的记录 SHALL NOT 被改写 |
| 大文档拆分 | 各分册内容为原文件对应章节的原文；SHALL NOT 因拆分改写表述、调整章节顺序或合并章节 |
| 拆分后建立索引 | 在同级建立 `index.md` 承载章节导航，使读取侧能按章节定位到目标分册 |
| 术语表处理 | 保持单文件，提供按模块/首字母的术语索引 |

**历史承载位置**：

| 文档层级 | 历史承载位置 |
|---------|-------------|
| 变更级产物 | `docs/changes/{change}/revision-history.md`（按产物文件分组） |
| 产品级文档 | `docs/designs/changelog.md`（保留原属文档标识） |

详见 [references/execute-rules.md](references/execute-rules.md) — 裁剪、搬移与拆分的具体步骤。

## 步骤 5：VERIFY — 引用完整性校验

优化执行完毕后 SHALL 校验全部受影响引用的完整性，SHALL NOT 留下断链或失效路径：

| 场景 | 动作 |
|------|------|
| 拆分后的引用更新 | 定位引用被拆分文档的位置，更新为拆分后的目标路径；更新范围 SHALL 包含项目文档、Skill 规则文件与脚本 |
| 引用校验 | 校验全部受影响引用均能解析到存在的文件；存在无法解析的引用时 SHALL 报告并停止，不得静默通过 |
| 校验通过后输出报告 | 优化报告含实际执行的项、体积变化、更新过的引用清单 |

**执行助手**：

```bash
# 校验执行前留档的引用清单（退出码 0 = 全部可解析；1 = 存在断链）
python skills/kflow-doc-optimize/scripts/check_refs.py verify --root <项目根> --list docs/doc-optimize-references.md
```

详见 [references/verify-rules.md](references/verify-rules.md) — 引用扫描、更新与校验步骤；报告格式见 [references/report-template.md](references/report-template.md)。

# 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 项目文档树 | ✅ 必须 | `CONTEXT.md`、`docs/designs/**`、`docs/open/**`、`docs/changes/**` |
| 用户确认 | ✅ 必须 | 执行范围的选择 |
| `.status.md` 阶段状态 | ⏭️ 不读取 | 本 Skill 不依赖也不修改变更阶段状态 |

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 优化报告 | `docs/doc-optimize-report.md` | ✅ 必须 | 按 [references/report-template.md](references/report-template.md) 输出：扫描范围、实际执行项、体积变化前后对比、更新过的引用清单、引用校验结论、未执行项、反向还原说明 |
| 受影响引用清单（执行前留档） | `docs/doc-optimize-references.md` | ✅ 必须 | 执行前产出，记录全部受影响引用及其原路径，供反向还原 |
| 历史承载位置 | `docs/changes/{change}/revision-history.md`、`docs/designs/changelog.md` | 🔶 条件 | 发生修订记录裁剪时创建或追加 |
| 章节索引 / 拆分目录 | 与被优化文档同级 | 🔶 条件 | 体积跨越 30 / 80 KB 阈值时创建 |

# 执行约束

- SHALL NOT 修改任何变更的 `.status.md` 阶段状态表
- SHALL NOT 改写入、删减或合并文档的实质内容——仅搬移、拆分与建索引
- SHALL NOT 在用户确认前执行任何写入
- SHALL NOT 静默通过引用校验失败——存在断链时报告并停止
- SHALL NOT 扫描已归档变更目录
- 重复执行时已符合边界的文档被排除，清单为空即报告「无需优化」，不发起确认询问

# 与其他 Skill 的关系

- **独立 Skill**：可随时调用，不要求活跃变更
- **与 `kflow-init`**：kflow-init 在目标项目写入门控配置并注入本 Skill 的适用边界例外声明；本 Skill 负责存量文档优化
- **与 `kflow-archive`**：归档设计合并步骤自动执行新文档的留存边界；本 Skill 处理存量
- **与 `kflow-guide`**：guide 支持关键词路由，无活跃变更时同样可路由
- **前置阶段**：无
- **后续阶段**：无（非流程阶段）

# 核心提醒

- 执行前必须产出受影响引用清单并留档，存量优化不可自动回滚
- 只搬移、拆分与建索引，不改写正文
- 无优化项时直接报告并终止，不打扰用户
- 引用校验失败即停止，不静默通过
- 不写入、不依赖变更阶段状态

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
