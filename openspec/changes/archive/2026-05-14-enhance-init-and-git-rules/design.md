## Context

当前 `kflow-init` 的 CLAUDE.md 注入仅包含流程规则，缺少项目特定上下文；`kflow-guide` 和 `kflow-archive` 缺少 git 版本管理机制。本设计在现有技能体系上扩展三项能力：项目画像注入、老项目逆向分析、变更边界 git commit。

现有基础：
- `kflow-init` v1.8.0 已有 marker 注入机制（`## 变更流程强制规则` section），支持幂等更新
- `kflow-guide` 已有活跃变更检测和意图识别能力
- `kflow-archive` 已有归档条件检查、设计合并、索引更新流程
- `CLAUDE.md` 已有手动编写的流程规则（含一条 commit 规则）

## Goals / Non-Goals

**Goals:**
- 扩展 `kflow-init` 向 CLAUDE.md 注入「项目画像」section，含项目类型、技术栈、源码结构、产品文档状态
- 支持 re-init 重新扫描并更新项目画像（幂等）
- 新增老项目代码逆向分析流程，按用户确认生成产品级文档
- 在 `kflow-guide` 新增 pre-change git commit 检查（分析-总结-确认-提交）
- 在 `kflow-archive` 新增 post-archive git commit 步骤
- 首次 init 完成后自动 git commit

**Non-Goals:**
- 不改变现有 toolchain.md 的生成逻辑
- 不改变 `kflow-guide` 的意图识别和路由逻辑（仅增加前置步骤）
- 不改变 `kflow-archive` 的设计合并逻辑（仅在末尾追加步骤）
- 不强制 git commit（用户可选择跳过）
- 不实现自动 push

## Decisions

### Decision 1: CLAUDE.md 双层 marker 注入架构

**选择**: 使用两个独立的 `## ` section marker 分别管理「项目画像」和「变更流程强制规则」，各自独立幂等更新。

```
CLAUDE.md 结构（init 注入后）:

  (用户原始内容)
  ...
  ## 项目画像                          ← marker 1
  > 来源: kflow-init ...
  - 项目类型 / 技术栈 / ...
  
  ## 变更流程强制规则                   ← marker 2
  > 来源: kflow-init ...
  - guide 流转规则 / git commit 规则
```

**理由**:
- 项目画像是项目特定的（不同项目内容完全不同），流程规则是通用的（跨项目一致）
- 两者更新频率不同：项目画像在 re-init 时重新扫描，流程规则只在规则升级时更新
- 独立的 marker 允许单独替换某一个 section，不影响另一个

**备选方案**: 合并为一个 section — 拒绝，因为更新粒度太粗，re-init 时无法区分"需要重新扫描"和"需要保持"的内容。

### Decision 2: 项目画像字段设计

**选择**: 8 个字段，分必填和条件两类：

| 字段 | 类型 | 来源 | 新项目 | 老项目 |
|------|------|------|--------|--------|
| 项目类型 | 枚举（前后端/纯后端） | package.json + 源文件扫描 | ✅ 有值 | ✅ 有值 |
| 语言 | string | 源文件扫描 | ✅ 有值 | ✅ 有值 |
| 框架 | string | package.json | ✅ 有值 | ✅ 有值 |
| 数据库 | string | 配置文件扫描 | ⚠️ 待确定 | ✅ 有值 |
| 构建工具 | string | 配置文件扫描 | ✅ 有值 | ✅ 有值 |
| 关键目录 | list | 目录扫描 | ⚠️ 默认结构 | ✅ 有值 |
| 入口文件 | list | 文件扫描 | ❌ 不存在 | ✅ 有值 |
| 产品文档状态 | 7 项状态表 | 文件存在性检测 | 全 ❌ | 混合 |

**理由**: 新项目技术栈可能未确定，需要接受"未知"状态；老项目可以通过文件扫描获取全部信息。

### Decision 3: 老项目逆向分析范围

**选择**: 按三层深度扫描，生成 6 类产品文档草稿：

```
扫描层次:
  L1: 配置文件扫描
      package.json / pom.xml / build.gradle / requirements.txt / Cargo.toml
      → 技术栈、构建工具、依赖列表
  
  L2: 目录结构扫描
      src/ 子目录、routes/、controllers/、models/、services/
      → 模块划分、领域识别
  
  L3: 源码语义扫描
      路由定义、数据模型、API 接口、关键注释
      → API 目录、数据模型、领域术语

生成文档（草稿状态，待用户审核）:
  1. CONTEXT.md              — 领域术语（L3 提取）
  2. docs/designs/index.md   — 产品设计入口（综合）
  3. docs/designs/domains/{domain}.md — 各领域文档（L2 模块 + L3 路由）
  4. docs/designs/architecture.md     — 系统架构（L1 + L2）
  5. docs/designs/data-model.md       — 数据模型（L3 模型文件）
  6. docs/designs/api-catalog.md      — API 目录（L3 路由定义）
```

**理由**: L1→L3 渐进式深度，不过度分析（不解析完整 AST，仅语义级扫描）。草稿机制保证用户始终拥有最终审核权。

### Decision 4: Pre-change commit 分析策略

**选择**: guide 检测到未提交时，通过 `git diff --stat` + `git diff` 分析变更内容，基于文件路径和 diff 内容推断变更性质，生成一行摘要。

```
检测流程:
  1. git status --porcelain → 判断是否有未提交
  2. 有未提交 → 读取最近一次 commit 信息（用于上下文）
  3. git diff --stat → 了解变更范围
  4. 分析:
     ├── 文件路径推断: docs/archive/ → "归档变更"
     ├── 文件路径推断: docs/changes/ → "变更中"
     ├── 文件路径推断: docs/designs/domains/ → "产品文档更新"
     └── 源码路径 → "代码变更"
  5. 生成一行中文摘要
  6. AskUserQuestion: 展示摘要 + 变更文件概要 → 用户确认/修改/跳过
  7. 用户确认后: git add -A && git commit -m "{摘要}"
```

**提交信息格式**: `{动词}: {一行中文摘要}`，例如：
- `归档变更 add-2fa: 新增双因素认证，更新认证域文档`
- `变更 explore: add-user-auth 设计探索阶段完成`
- `修复: 支付回调签名验证异常`

### Decision 5: Post-archive commit 触发时机

**选择**: 在 `kflow-archive` 流程末尾（索引更新之后）新增 COMMIT 步骤，作为归档流程的第 8 步。

```
kflow-archive 流程变更:

  现有步骤:
    1. CHECK    → 门控检查
    2. CONFIRM  → 用户确认归档
    3. MERGE    → 设计合并到产品级
    3.5 ADR     → ADR 索引更新检查
    4. MOVE     → 移动变更目录到 archive/
    5. UPDATE   → 更新归档状态文件
    6. INDEX    → 更新 docs/changes/index.md
    7. COMPLETE → 输出归档完成信息
    + 8. COMMIT → git add + git commit (新增)
```

### Decision 6: 变更目录自动创建策略

**选择**: 变更级目录（docs/changes/{change}/ 及其子目录）由各阶段 Skill 在需要时自动创建，不集中在 init 阶段创建。

| 目录 | 创建时机 | 创建者 |
|------|---------|--------|
| docs/changes/{change}/ | 变更初始化 | kflow-explore |
| docs/changes/{change}/functional-designs/ | 设计探索 | kflow-explore |
| docs/changes/{change}/self-reviews/ | 自审阶段 | kflow-explore/design/prototype |
| docs/changes/{change}/test-reports/ | 测试阶段 | kflow-e2e-test/integration-test |
| docs/changes/{change}/checkpoints/ | 各阶段 | 各 Skill |

**理由**: 已在现有 core-mechanisms 中定义，无需改变。

## Risks / Trade-offs

- **[R] 老项目逆向分析不准确** → 所有生成文档为草稿状态，必须用户审核确认后才写入；标注"由 AI 逆向分析生成"提示用户审慎验证
- **[R] git diff 分析产出不精准的 commit 摘要** → 展示 diff 概要给用户确认，用户可直接修改提交信息或跳过提交
- **[R] re-init 扫描结果与实际项目演进不同步** → 项目画像 section 标注扫描时间戳，提示用户"如需更新请重新执行 kflow-init"
- **[R] pre-change commit 可能打断用户工作流** → 允许用户选择"跳过本次提交"，但记录到 checkpoint 中作为未提交提醒
