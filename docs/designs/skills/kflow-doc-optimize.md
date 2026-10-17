# kflow-doc-optimize（文档优化 Skill）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **类型**: 独立维护 Skill（非流程阶段）
> **创建时间**: 2026-10-17

---

## 基本信息

```yaml
name: kflow-doc-optimize
description: 文档优化 - 存量文档的修订记录裁剪、大文档拆分与章节索引建立，含引用完整性校验。独立维护 Skill（非流程阶段），可随时手动调用，不写入变更阶段状态。
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
```

---

## 定位

`kflow-doc-optimize` 是**独立维护 Skill（非流程阶段）**，与 `kflow-verify` / `kflow-bug-triage` 同层：

| 维度 | 说明 |
|------|------|
| 作用域 | **项目级**——`CONTEXT.md`、`docs/designs/**`、`docs/open/**` 与 `docs/changes/` 下的活跃变更产物 |
| 触发 | 随时手动调用（`/kflow-doc-optimize` 或「文档优化」等关键词），或经 `kflow-guide` 路由；**不要求存在活跃变更** |
| 阶段状态 | SHALL NOT 写入任何变更的阶段状态（`.status.md` 阶段状态表不被修改） |
| 产出 | 以独立**优化报告**承载，SHALL NOT 登记进变更产物清单 |
| 与变更流程的关系 | SHALL NOT 被视为任何阶段的产物；其调用 SHALL NOT 改变任何变更的阶段状态 |

### 三层分工

```
  ① 规范层   —— 定义「该写什么、保留多少」        docs/designs/ 机制文档与各模板
                          ↓
  ② 自动层   —— 归档设计合并步骤自动裁剪、      archive-design-merge 能力（用户零操作）
                维护索引并触发拆分
                          ↓
  ③ 存量层   —— 对已生成的文档执行一次性优化    kflow-doc-optimize（本 Skill）
                扫描 → 清单 → 用户确认 → 执行 → 引用校验 → 报告
```

规范层与自动层只作用于**新变更产生的文档**；存量文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`、活跃变更目录）需要本 Skill 这一显式入口。

### 为什么是独立 Skill 而非扩展 `kflow-verify`

| 维度 | `kflow-verify` | `kflow-doc-optimize` |
|------|---------------|---------------------|
| 作用域 | **变更级**——读 `.status.md`，七维度针对该变更的产物 | **项目级**——产品级文档与活跃变更目录 |
| 修复目标 | 路由到对应阶段的 REVISION 模式 | 就地搬移与拆分，不触发阶段 |
| 触发前提 | 存在变更 | 可无活跃变更 |

### 不受变更流程适用边界约束

`kflow-doc-optimize` 是**项目级文档维护工具**，SHALL NOT 受「KFlow Skills 仅适用于功能变更与缺陷修复」这一适用边界的排除。项目在其 `CLAUDE.md`「项目自定义规则」区块中声明该类边界时，SHALL 将本 Skill 列为例外；`kflow-init` 注入的流程规则 SHALL 声明该例外，便于项目侧同步。

---

## 流程

```
SCAN → REPORT → CONFIRM → EXECUTE → VERIFY
```

| 步骤 | 动作 | 产出 |
|------|------|------|
| SCAN | 扫描产品级与活跃变更级文档，按阈值识别需要优化的文档 | 待优化文档的内部清单 |
| REPORT | 输出用户可读的优化清单（文档路径、问题类型、当前体积、优化方式、预计优化后体积、受影响的引用位置） | 优化清单 |
| CONFIRM | 提交用户确认执行范围（全部 / 部分 / 不执行） | 用户选择 |
| EXECUTE | 仅搬移、拆分与建索引，不改变正文 | 优化后的文档 |
| VERIFY | 校验全部受影响引用可解析；通过后输出优化报告 | 优化报告 |

**无优化项时**：扫描未识别出任何需要优化的文档时，报告「无需优化」并终止，SHALL NOT 发起确认询问。重复执行时已符合边界的文档被排除，不产生副作用。

---

## 执行助手脚本

Skill 随包提供三个 Python 脚本（无第三方依赖，Python 3），使扫描、引用留档与校验可重复执行、可机器判定：

| 脚本 | 步骤 | 职责 | 退出码 |
|------|------|------|--------|
| `skills/kflow-doc-optimize/scripts/scan_docs.py` | SCAN | 按扫描范围与阈值（3 条 / 30 KB / 80 KB）输出 Markdown 优化清单；`--json` 输出结构化结果 | 0 |
| `skills/kflow-doc-optimize/scripts/check_refs.py find` | EXECUTE 前 | 扫描项目中对目标文档的全部引用；`--write` 写入 `docs/doc-optimize-references.md` 留档 | 0 |
| `skills/kflow-doc-optimize/scripts/check_refs.py replace` | EXECUTE | 批量替换引用；默认 dry-run，`--apply` 才写入 | 1（dry-run 有待替换项） |
| `skills/kflow-doc-optimize/scripts/check_refs.py verify` | VERIFY | 逐条校验引用可解析；存在断链时报告并返回非零 | 0 通过 / 1 断链 |
| `references/report-template.md` | VERIFY | 优化报告的固定格式 |

> 脚本仅作用于被调用的目标项目，SHALL NOT 修改任何变更的阶段状态。

## SCAN — 扫描与识别

### 扫描范围

| 范围 | 说明 |
|------|------|
| 产品级文档 | `CONTEXT.md`、`docs/designs/**`、`docs/open/**` |
| 变更级文档 | `docs/changes/` 下的活跃变更产物（`.status.md` 除外——状态文件按 `status-file-layering` 分层，不适用修订记录规则） |
| 排除 | 已归档变更目录（`docs/changes/archive/**`） |

### 识别规则

| 问题类型 | 判定 |
|---------|------|
| 修订记录超量 | 文档头部修订记录条数 > **3** |
| 超出分片阈值 | 单文件体积 > **80 KB** |
| 缺少章节索引 | 单文件体积 > **30 KB** 且未提供章节索引 |

> 阈值权威定义见 `artifact-revision-record-retention`（保留条数）与 `large-doc-splitting`（30 / 80 KB 两档）。`CONTEXT.md` 术语表例外——不拆分，改为提供按模块/首字母的术语索引。

### 清单内容

每一项 SHALL 包含：文档路径、问题类型、当前体积、优化方式、预计优化后体积、受影响的引用位置。

---

## EXECUTE — 执行与内容保真

本 Skill 执行优化时 SHALL 仅搬移、拆分与建立索引，**SHALL NOT 改写、删减或合并文档的实质内容**。

| 动作 | 保真约束 |
|------|---------|
| 修订记录裁剪 | 被移出的记录原样进入历史承载位置；保留在头部的记录 SHALL NOT 被改写 |
| 大文档拆分 | 各分册内容为原文件对应章节的原文；SHALL NOT 因拆分改写表述、调整章节顺序或合并章节 |
| 拆分后建立索引 | 在同级建立 `index.md` 承载章节导航，使读取侧能按章节定位到目标分册 |
| 术语表处理 | `CONTEXT.md` 保持单文件，提供按模块/首字母的术语索引 |

历史承载位置按层级划分：变更级产物 → `docs/changes/{change}/revision-history.md`；产品级文档 → `docs/designs/changelog.md`。

**执行前留档**：执行前 SHALL 产出受影响引用清单并留档，以备反向还原（存量优化不可自动回滚）。

---

## VERIFY — 引用完整性校验

优化执行完毕后，本 Skill SHALL 校验全部受影响引用的完整性，SHALL NOT 留下断链或失效路径：

| 场景 | 动作 |
|------|------|
| 拆分后的引用更新 | 定位引用被拆分文档的位置，更新为拆分后的目标路径；更新范围 SHALL 包含项目文档、Skill 规则文件与脚本 |
| 引用校验 | 校验全部受影响引用均能解析到存在的文件；存在无法解析的引用时 SHALL 报告并停止，不得静默通过 |
| 校验通过后输出报告 | 优化报告含实际执行的项、体积变化、更新过的引用清单 |

---

## 输入要求

| 产物 | 图例 | 说明 |
|------|------|------|
| 项目文档树 | ✅ 必须 | `CONTEXT.md`、`docs/designs/**`、`docs/open/**`、`docs/changes/**` |
| 用户确认 | ✅ 必须 | 执行范围的选择 |
| 变更阶段状态 | ⏭️ 不读取 | 本 Skill 不依赖 `.status.md` 阶段状态，也不修改它 |

## 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 优化报告 | `docs/doc-optimize-report.md` | ✅ 必须 | 扫描范围、实际执行项、体积变化前后对比、更新过的引用清单、引用校验结论 |
| 受影响引用清单（执行前留档） | `docs/doc-optimize-references.md` | ✅ 必须 | 执行前产出，记录全部受影响引用及其原路径，供反向还原 |
| 历史承载位置 | `docs/changes/{change}/revision-history.md`、`docs/designs/changelog.md` | 🔶 条件 | 发生修订记录裁剪时创建或追加 |
| 章节索引 / 拆分目录 | 与被优化文档同级 | 🔶 条件 | 体积跨越 30 / 80 KB 阈值时创建 |

---

## 与其他 Skill 的关系

- **独立 Skill**：可随时调用，不要求活跃变更
- **与 `kflow-init`**：`kflow-init` 负责在目标项目写入项目级配置（`autoCompactWindow`、门控 hook）并注入本 Skill 的适用边界例外声明；本 Skill 负责存量文档的一次性优化
- **与 `kflow-archive`**：归档的设计合并步骤自动执行新文档的留存边界；本 Skill 处理存量
- **与 `kflow-guide`**：guide 支持本 Skill 的关键词路由，且无活跃变更时同样可路由
- **与 `kflow-verify`**：作用域与修复目标不同（见「定位」）
