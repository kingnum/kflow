---
name: kflow-prototype-design
version: 0.29.0
description: Use when user needs prototype design/原型设计、UI 设计、交互设计、HTML 原型 for frontend changes. 编排层，默认复用 docs/toolchain.md 已锁定的设计工具链，委托子代理生成 HTML 原型并直写产品级 docs/designs/prototypes/。BUILD 四项静态门控必做，通过后由用户选择人工审查或子代理自动审查验证。含用户评审循环、变更级改动追踪（哈希并发检测）、CDN 离线扫描、多文件交叉引用检查。含 PRE_HOOK/POST_HOOK 阶段钩子引用。
license: MIT
triggers:
  - 原型设计
  - UI 设计
  - 交互设计
  - HTML 原型
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Skill
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# 角色

原型设计编排层。采用「编排层 → 工具链复用 → 子代理执行引擎 → 构建门控 → 审查方式分流」架构模型——**不做具体原型制作**（通过子代理委托设计引擎执行），只做阶段门控、工具链复用判定、上下文组装、提示词优化（含 design-prompt.md 文件输出 + 用户确认）、子代理委托调用、BUILD 静态门控、审查方式选择、条件性验证和用户评审。

> **设计决策**：huashu-design 等设计引擎是一套持续更新的完整 Skill（数万字 SKILL.md + assets/ + scripts/ + references/），通过子代理委托调用而非在主 Agent 上下文直接调用，避免 HTML 产物污染主 Agent 上下文、内容膨胀和 Token 浪费。

> **v4.0.0 重要变更**：TOOLCHAIN 由「每次扫描+询问」改为默认复用已锁定工具链；新增 BUILD 构建门控（四项静态检查、零子代理、唯一必做验证）与审查方式二选一（人工审查 / 子代理自动审查验证）；原型产物由「变更级副本 + 归档合并」改为直写产品级 `docs/designs/prototypes/`，变更级只留 `prototype-changes.md`（含改动前哈希）+ `prototype-backup/`；VERIFY 与 SELFREV 由「无条件强制」改为随审查方式条件触发。

# 任务

```
门控检查（修订模式检测对象为变更级 prototype-changes.md）
  → PRE_HOOK: 状态检查 + RELOAD（含产品级 manifest.md 与变更级 prototype-changes.md）
  → 评估是否需要原型（AskUserQuestion 确认）
  → TOOLCHAIN: 复用判定
      ├── 已锁定且 Skill 可用 → 复用 docs/toolchain.md 原型设计章节（不扫描、不询问）
      └── 例外（无锁定 / Skill 失效 / 用户要求更换）→ SCAN + 方案推荐 + 锁定
  → 机械组装 prompt 上下文（功能设计 + 产品级已有原型 + 品牌资产）
  → 提示词优化（菜单树 + 页面元素穷举 + 业务流程脚本 + 硬约束注入）+ 输出 prototype-plan/design-prompt.md + 用户确认
  → DESIGN-0: 并发写入检测（改动前哈希比对，冲突交用户裁决）
  → DESIGN-STYLE: 子代理推荐 3 个差异化风格方向 → 用户选择 → prototype-plan/style-decision.md
  → DESIGN-GENERATE: 子代理按有效工具链执行
      ├── 直写 docs/designs/prototypes/（screens/ + components/ + assets/ + index.html + design-tokens.css + design-system/MASTER.md）
      ├── 改动前副本 → prototype-backup/
      └── 改动登记 → prototype-changes.md
  → BUILD: CDN 扫描 + 交叉引用 + 必检产物存在 + 清单与磁盘一致（零子代理，唯一必做验证）
  → 审查方式选择（AskUserQuestion 二选一）
      ├── 人工审查            → 跳过全部自动验证，直接进入 REVIEW
      └── 子代理自动审查验证  → VERIFY（单轮合并验证：一轮子代理、一份报告，含导航/Playwright/UX/对比度四分区）+ SELFREV（签署清单 + 单轮验证）
  → 用户评审循环（AskUserQuestion）
  → COMPLETE: 更新状态文件 + 同步 manifest.md + 提取设计令牌与元素覆盖树
  → POST_HOOK: 浏览器清理 + 状态更新
```

# 架构模型

```
kflow-prototype-design (编排层)
├── 阶段门控 + 状态管理 + 用户评审
├── 产品级上下文加载（docs/designs/prototypes/）
├── TOOLCHAIN: 复用判定 → 复用已锁定工具链 / 例外时 SCAN + 选择
├── prompt 上下文组装（INPUT：机械提取层）
├── prompt 优化（OPTIMIZE：设计转译层 + prototype-plan/design-prompt.md 文件输出 + 用户确认）
├── Agent(subagent) 子代理 → 按有效工具链 execution_order 执行设计引擎
│   ├── 子代理独立上下文，读取 design-prompt.md + style-decision.md
│   ├── 直写产品级 docs/designs/prototypes/
│   ├── 改动前副本 → prototype-backup/
│   └── 改动登记 → prototype-changes.md
├── BUILD: 四项静态检查（主 Agent 直接执行，零子代理）
├── 审查方式选择 → 人工审查 / 子代理自动审查验证
└── 用户评审循环（确认/修订循环）
```

**有效工具链解析顺序**：`docs/changes/{change}/toolchain.md` 的原型设计章节 → 不存在时取 `docs/toolchain.md` 的原型设计章节。

# 门控检查

进入原型设计阶段前 SHALL 检查：

| 门控项 | 检查方式 | 不满足时的处理 |
|--------|---------|--------------|
| `.status.md` 存在 | Read | 终止，提示需要先执行 kflow-explore |
| 设计探索状态 = ✅ 完成 | 检查 `.status.md` | 终止，提示需要完成设计探索 |
| `functional-designs/index.md` 存在 | Read/Glob | 终止，提示需要完成功能设计 |
| 存在前端/UI 相关功能点 | 扫描 functional-designs/ | 自动跳过，标记 ⏭️ 跳过 |
| 项目类型为纯后端 | 检查 `.status.md` 项目类型 | 自动跳过，标记 ⏭️ 跳过 |

> **变更说明**：`prototype-gen` 角色可用性**不再**作为进入阶段的硬拦截项。复用路径下无需扫描环境（工具链已在 `docs/toolchain.md` 锁定）；仅在 TOOLCHAIN 复用判定结论为「需要重新选择」时才扫描并判定该角色可用性。角色数量 = 0 时标记 ⚠️ 阻塞，**不跳过**。

# 输入要求

| 输入 | 图例 | 说明 |
|------|------|------|
| functional-designs/ | ✅ 必须 | 设计探索阶段输出，提取项目背景和 UI 功能点清单 |
| `docs/toolchain.md` | 🔶 条件 | 项目级工具链配置，原型设计章节存在且已锁定时直接复用 |
| `docs/changes/{change}/toolchain.md` | 🔶 条件 | 变更级工具链覆盖（用户显式要求更换时写入），存在时优先于项目级 |
| `docs/designs/prototypes/manifest.md` | 🔶 条件 | 全产品原型清单，存在时用于加载已有原型上下文 |
| `docs/designs/prototypes/design-tokens.css` | 🔶 条件 | 已有设计令牌，存在时纳入设计约束 |
| `docs/designs/prototypes/screens/` | 🔶 条件 | 已有屏幕清单，存在时作为新屏幕的导航锚点 |
| `docs/designs/prototypes/components/` | 🔶 条件 | 已有共享组件清单，存在时纳入设计约束 |
| `docs/designs/prototypes/design-system/MASTER.md` | 🔶 条件 | 已有设计系统，存在时纳入设计约束 |
| `docs/designs/prototypes/index.html` | 🔶 条件 | 产品级全貌原型，新屏幕需能挂入其导航 |
| `docs/changes/{change}/prototype-changes.md` | 🔶 条件 | 本变更已有原型改动记录，修订模式判定与并发检测依据 |
| brand-spec.md | 🔶 条件 | 品牌资产文件，涉及品牌感知时纳入 prompt |

> **图例说明**：✅ 必须 ＝ 不可或缺的前置输入；🔶 条件 ＝ 满足特定条件时需要；⏭️ 跳过 ＝ 被跳过的阶段，产物不存在。

# 输出产物

## 产品级产物（`docs/designs/prototypes/`）

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 全产品导航入口 | `docs/designs/prototypes/index.html` | ✅ 必须 | 卡片网格按功能模块分组，挂载全部屏幕入口 |
| 产品级原型清单 | `docs/designs/prototypes/manifest.md` | ✅ 必须 | 六段落：产物组织方式、原型文件清单（含角色与来源变更）、页面清单、设计系统引用、共享资源清单、修订记录。下游阶段获取全产品原型文件列表的入口 |
| 屏幕页面 | `docs/designs/prototypes/screens/*.html` | ✅ 必须 | 多文件 HTML 交互原型，所有文件离线自包含 |
| 共享组件与资源 | `docs/designs/prototypes/components/`、`assets/` | 🔶 条件 | 共享组件脚本、共享样式、静态资源 |
| 设计令牌 | `docs/designs/prototypes/design-tokens.css` | ✅ 必须 | CSS 变量声明（色板/字号/间距/圆角/阴影）。设计引擎产出，COMPLETE 步骤从原型 HTML 复核提取并更新 |
| 设计系统 | `docs/designs/prototypes/design-system/MASTER.md` | ✅ 必须 | 通用必备产物：色彩方案、字体系统、间距规格、组件规范、交互规则。无论选定哪个工具链都必须输出 |

## 变更级产物（`docs/changes/{change}/`）

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 工具链选择记录（项目级） | `docs/toolchain.md` | ✅ 必须 | 原型设计阶段锁定的工具链方案，含 skills_used、execution_order、decision_time、status |
| 工具链覆盖记录 | `docs/changes/{change}/toolchain.md` | 🔶 条件 | 仅用户显式要求更换工具链时写入 |
| 原型改动清单 | `prototype-changes.md` | ✅ 必须 | 改动表（`\| 文件路径 \| 类型 \| 改动前哈希 \| 说明 \|`）、改动前快照说明、并发写入裁决记录、回滚记录 |
| 原型改动前快照 | `prototype-backup/` | 🔶 条件 | 按产品级相对路径镜像存放的改动前副本，供回滚使用（新增文件不生成快照） |
| 提示词文件 | `prototype-plan/design-prompt.md` | ✅ 必须 | 7 章节完整提示词文件，DESIGN 步骤的唯一真相源，含元信息头部（变更名称/版本号/生成时间/状态标记） |
| 风格选择决策 | `prototype-plan/style-decision.md` | ✅ 必须 | 用户选定的风格方向：风格名称、设计哲学、色彩方案、字体系统、布局模式、ASCII 线框图 |
| 元素覆盖树 | `element-coverage-tree.md` | ✅ 必须 | 四层树状结构（📄页面→🏗️区域→🔘元素→🎯状态+操作链），TC-ID 列初始为空，待 design 阶段填充 |
| BUILD 报告 | `self-reviews/prototype/cdn-crossref-check/report.md` | ✅ 必须 | CDN 扫描 + 交叉引用 + 必检产物 + 清单一致 四项检查综合报告（两种审查方式下均产出） |
| VERIFY 合并验证报告 | `self-reviews/prototype/verify-report.md` | 🔶 条件 | 单轮合并验证报告（固定路径，不按轮次编号），按「导航合理性 / Playwright 全覆盖 / UX 规则审查 / 对比度检测 / 验证结论」强制分区，每分区独立给出该环节全部检查项的逐项结论（仅子代理自动审查验证路径） |
| 自审报告 | `self-reviews/prototype/report.md` | 🔶 条件 | SELFREV 单轮验证报告（固定路径，不按轮次编号），含签署清单打假结果、独立发现问题清单、范围外观察、全量遍历证明、验证结论（仅子代理自动审查验证路径） |
| 用户评审记录 | `docs/changes/{change}/.status.md`（用户评审记录表） | ✅ 必须 | 原型设计评审状态、审查方式选择结果、评审时间、备注 |

> **产物位置**：产品级产物写入 `docs/designs/prototypes/`；变更级工作记录写入 `docs/changes/{change}/`。变更级 **SHALL NOT** 创建 `index.html`、`screens/`、`components/`、`design-tokens.css` 等原型产物。

### 产品级原型目录示例

```
docs/designs/prototypes/
├── index.html                  ← 全产品导航入口（卡片网格按功能模块分组）
├── manifest.md                 ← 全产品原型清单（下游阶段读取入口）
├── design-tokens.css           ← 设计令牌（CSS 变量）
├── design-system/
│   └── MASTER.md               ← 设计系统主文档
├── screens/
│   ├── login.html              ← 登录页
│   ├── dashboard.html          ← 仪表盘
│   ├── detail.html             ← 详情页
│   └── form.html               ← 表单页
├── components/
│   └── components.js           ← 共享组件
└── assets/
    └── app-phone.js            ← AppPhone 状态管理器
```

## 状态双写规则

阶段完成、回退与重执行时，主 Agent SHALL 同时执行两处写入：

1. **追加历史**：向 `docs/changes/{change}/status-log.md` 追加本次事件——阶段名、轮次、完成时间、耗时、终止结果；回退时另记回退原因与目标阶段
2. **刷新当前**：刷新变更级 `.status.md` 的当前状态字段——当前阶段、阶段状态表对应行、执行轮次、终止结果、未决事项

`.status.md` SHALL 保持在 100 行以内，超出部分改为写入 `status-log.md`。变更目录中不存在 `status-log.md`（历史变更未分层）时按既有单文件口径处理，SHALL NOT 强制回填。

> 读取边界：常规阶段推进与门控判定 SHALL 仅读取 `.status.md`；`status-log.md` 仅在中断恢复与审计场景读取。权威定义见 `status-file-layering` 能力。

# 执行流程

## 总流程

```
原型设计阶段流程:

┌──────────────────────────────────────────────────────────────────┐
│                    PROTOTYPE WORKFLOW (v4.0)                      │
├──────────────────────────────────────────────────────────────────┤
│  1.5 PRE_HOOK → 引用 skills/kflow-prototype-design/references/hooks.md prototype-design 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                          │
│  │   └── RELOAD → 重读 CONTEXT.md, toolchain.md, functional-designs/, │
│  │              docs/designs/prototypes/manifest.md(条件),            │
│  │              prototype-changes.md(条件), .status.md                │
│  1. CHECK     → 门控检查 + 修订模式检测                            │
│  │   ├── 检测变更级 prototype-changes.md 是否存在且非空（入口 A）   │
│  │   └── 检测是否从 code 阶段回退（入口 B）                        │
│  2. ASSESS    → 评估是否需要原型设计（AskUserQuestion）           │
│  3. TOOLCHAIN → 复用判定                                          │
│  │   ├── 已锁定且 Skill 可用 → 复用（不扫描、不询问）              │
│  │   └── 例外 → SCAN + 多方案推荐 + AskUserQuestion 选择 + 锁定    │
│  4. INPUT     → 机械组装 prompt 上下文（分层: 必然/条件）         │
│  │   ├── 必然存在: functional-designs/ 提取背景+UI功能点          │
│  │   ├── 条件存在: docs/designs/prototypes/ 产品级已有原型        │
│  │   └── 条件存在: brand-spec.md 品牌资产                        │
│  5. OPTIMIZE  → 深度分析设计 + 文件输出 + 用户确认                │
│  │   ├── 5.1 提取菜单树（一/二/三级菜单 → 对应页面）             │
│  │   ├── 5.2 穷举页面元素（布局/按钮/表单/数据区/弹窗/状态）     │
│  │   ├── 5.3 编写业务流程脚本（逐步用户操作路径）                │
│  │   ├── 5.4 注入硬约束（直写产品级+flow demo+离线自包含）       │
│  │   ├── 5.5 输出 prototype-plan/design-prompt.md（7 章节模板） │
│  │   └── 5.6 AskUserQuestion 用户确认（确认执行 / 需修订）       │
│  6. DESIGN    → 按有效工具链锁定执行                              │
│  │   ├── 6.0 并发写入检测（哈希比对 → 冲突则 AskUserQuestion 裁决）│
│  │   ├── 6.1 STYLE: 子代理推荐 3 个差异化风格方向                 │
│  │   │   └── AskUserQuestion 选择 → prototype-plan/style-decision.md │
│  │   └── 6.2 GENERATE: Agent(subagent) 按工具链执行               │
│  │       ├── 直写 docs/designs/prototypes/                        │
│  │       ├── 改动前副本 → prototype-backup/                       │
│  │       └── 改动登记 → prototype-changes.md                      │
│  7. BUILD     → 四项静态检查（零子代理）                          │
│  │   ├── 7.1 CDN 外部依赖扫描                                    │
│  │   ├── 7.2 交叉引用完整性检查                                  │
│  │   ├── 7.3 必检产物存在性检查                                  │
│  │   └── 7.4 清单与磁盘一致性检查                                │
│  │   → 不通过则修复重跑全部四项，SHALL NOT 进入后续步骤           │
│  8. 审查方式选择 → AskUserQuestion 二选一（BUILD 通过后）         │
│  ─ ─ ─ ─ ─ ─ ─ ─ 「子代理自动审查验证」路径 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  9. VERIFY    → 单轮合并验证（1 个子代理、1 份报告、无第二轮）   │
│  │   四分区: 导航合理性 / Playwright 全覆盖 / UX 规则审查 /      │
│  │          对比度检测（静态计算）+ 验证结论                     │
│  │   报告: self-reviews/prototype/verify-report.md              │
│  │   主 Agent 统一修复 → 本阶段修复清单                          │
│ 10. SELFREV   → 签署清单 + 单轮验证（报告 self-reviews/prototype/report.md） │
│  ─ ─ ─ ─ ─ ─ ─ ─ 「人工审查」路径：8 之后直接进入 11 ─ ─ ─ ─ ─ ─ │
│  │              （SHALL NOT 执行 VERIFY / SELFREV）              │
│ 11. REVIEW    → AskUserQuestion 用户评审（确认/修订循环）         │
│  │   ├── 确认通过 → COMPLETE                                     │
│  │   └── 需修订   → 收集反馈 → 回到 DESIGN                       │
│ 12. COMPLETE  → 更新状态文件 + 同步 manifest.md + 提取设计令牌与覆盖树 │
│ 13. POST_HOOK → 引用 skills/kflow-prototype-design/references/hooks.md prototype-design 阶段 POST_HOOK（含 BROWSER_CLEANUP + UPDATE_STATE） │
└──────────────────────────────────────────────────────────────────┘
```

## 步骤 1.5：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 PRE_HOOK（🔶 浏览器类型：CHECK_STATE + RELOAD）。

RELOAD 清单包含 `docs/designs/prototypes/manifest.md`（条件）与 `prototype-changes.md`（条件）。

## 步骤 1：CHECK — 门控检查

```
1. Read docs/changes/{change}/.status.md
2. 检查: 设计探索状态 = ✅ 完成
3. 检查: functional-designs/index.md 存在
4. 提取 .status.md 中的项目类型
5. 如项目类型 = 纯后端 → 自动跳过（标记 ⏭️ 跳过，退出）
6. 扫描 functional-designs/ 中是否有 UI 功能点
7. 如无 UI 功能点 → 自动跳过（标记 ⏭️ 跳过，退出）
8. 修订模式检测: 变更级 prototype-changes.md 是否存在且非空
   ├── 存在 → 标记为修订模式候选，进入「修订模式双入口」入口 A 分支
   └── 不存在 → 走新建模式，继续 ASSESS → TOOLCHAIN → INPUT → OPTIMIZE → DESIGN
```

> **变更说明**：修订模式检测对象由变更级 `prototype/index.html` 改为变更级 `prototype-changes.md`（是否存在且非空）。直写模型下变更级不再持有原型副本，`prototype-changes.md` 是「本变更是否已做过原型工作」的唯一可靠信号。

## 步骤 2：ASSESS — 评估是否需要原型设计

### 推荐创建原型

| 场景 | 说明 |
|------|------|
| 新增 UI 页面或显著修改现有页面 | 需要视觉确认新页面的布局和交互 |
| 用户交互流程复杂 | 多步表单、向导、仪表板等需要验证交互合理性 |
| 视觉设计决策需要干系人对齐 | 产品/设计/开发对 UI 方向需要可视化对齐 |
| 开发人员需要视觉参考 | 编码阶段需要明确的 UI 参考进行实现 |

### 可跳过

| 场景 | 说明 |
|------|------|
| 纯后端变更 | 自动跳过 |
| 纯数据/API 变更（无 UI 影响） | 自动跳过 |
| UI 变更极其微小 | 单个按钮、文字或颜色变更 |
| 用户明确拒绝 | 在 AskUserQuestion 中主动选择跳过 |

使用 AskUserQuestion 确认：

```
Question: "此变更有 {n} 个 UI 功能点。是否创建 HTML 原型？"
Options:
  - "确认创建原型"（推荐）
  - "跳过原型设计"
```

## 步骤 3：TOOLCHAIN — 工具链复用判定与锁定

### 3.1 有效工具链解析顺序

```
1. 读取 docs/changes/{change}/toolchain.md 的原型设计章节
2. 该章节存在 → 以变更级覆盖文件作为有效工具链
   - SHALL NOT 使用 docs/toolchain.md 中的原型设计章节
3. 该章节不存在 → 读取 docs/toolchain.md 的原型设计章节作为有效工具链
4. docs/toolchain.md 的路径 SHALL NOT 变更
```

### 3.2 复用判定（默认路径）

```
WHEN TOOLCHAIN 步骤启动
AND 有效工具链已锁定（章节存在且 status 已锁定）
AND 该工具链 skills_used 中列出的所有 Skill 在环境中均可用
THEN:
  1. 直接复用该工具链进入 DESIGN 步骤
  2. SHALL NOT 扫描 .claude/skills/ 目录
  3. SHALL NOT 调用 AskUserQuestion 询问工具链
  4. 输出"复用已有工具链"记录，包含：工具链来源文件、skills_used、execution_order、decision_time
```

### 3.3 需重新选择的三种例外

| 例外 | 判定 | 处理 |
|------|------|------|
| 无已锁定工具链（首次选择） | 变更级与项目级均无原型设计章节，或章节存在但 `status` 未标记为已锁定 | 进入重新选择流程；选定后写入 `docs/toolchain.md` 原型设计章节并标记已锁定。SHALL NOT 标记阶段为 ⚠️ 阻塞 |
| 已锁定但引用的 Skill 不可用 | `skills_used` 中至少一个 Skill 在环境中已不可用 | 输出提示："工具链 X 的 Skill Y 已不可用"；进入重新选择流程；完成后用新方案**覆盖写入**已锁定的工具链章节 |
| 用户显式要求更换 | 用户在 TOOLCHAIN 步骤显式要求更换工具链 | 进入重新选择流程，不受已锁定工具链约束；完成后**覆盖写入**变更级 `docs/changes/{change}/toolchain.md`，SHALL NOT 修改 `docs/toolchain.md` |

### 3.4 SCAN — 环境扫描设计 Skills（仅在需重新选择时执行）

```
1. 扫描 .claude/skills/ 目录下所有设计相关 Skills（读取 name + description）
2. 按角色分类: prototype-gen（能生成 HTML 原型，如 huashu-design、frontend-design）/ design-system / ux-review / code-gen
3. prototype-gen 数量 = 0 → ⚠️ 阻塞:
   ├── 提示用户: "未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
   ├── 标记阶段为 ⚠️ 阻塞 in .status.md
   └── 退出（不继续执行）
4. prototype-gen 数量 = 1 → ✅ 单一方案，自动选择该方案进入 DESIGN 步骤，不询问用户
5. prototype-gen 数量 ≥ 2 → ✅ 多方案，生成 2-3 条工具链方案（含 Skills/流程/优点/缺点/适用场景），AskUserQuestion 展示供用户选择，方案数量 SHALL NOT 超过 3 个
6. 扫描结果 SHALL 输出到 available-skills.json（内部使用，含每个 Skill 的名称、角色分类、description 摘要）
```

### 3.5 用户选定后锁定

```
1. 用户在 AskUserQuestion 中选择一种工具链方案后:
   - 默认写入 docs/toolchain.md 的原型设计章节
   - 用户显式要求更换时写入变更级 docs/changes/{change}/toolchain.md 的原型设计章节
   - 记录字段：change_name、selected_toolchain、skills_used、execution_order、decision_time、status
2. DESIGN 步骤 SHALL 严格按有效工具链中指定的 Skill 和顺序执行
3. 系统 SHALL NOT 在执行过程中自行切换工具链
```

### 3.6 严格按 execution_order 逐个调用

- SHALL 按 `execution_order` 数组顺序逐个调用 `skills_used` 中列出的 Skill
- SHALL NOT 跳过 `execution_order` 中定义的任一 Skill
- SHALL NOT 在 `execution_order` 之外调用任何其他设计 Skill
- SHALL NOT 自行调整调用顺序
- 某个 Skill 调用失败 → 重试一次；重试仍失败 → 标记阶段为 ⚠️ 阻塞并提示用户；SHALL NOT 自行切换到未列出的其他 Skill

## 步骤 4：INPUT — 机械组装 Prompt 上下文

本步骤为 OPTIMIZE 步骤提供原始数据输入。按存在性分层组装基础 prompt 数据：

```
✅ 必然存在（前置阶段产物）:
  ├── functional-designs/index.md      → 提取产品概述
  ├── functional-designs/part-NN.md    → 提取 UI 功能点清单
  └── 产出路径: 产品级 docs/designs/prototypes/ 目录
      变更级工作记录: docs/changes/{change}/prototype-plan/ 目录

🔶 条件存在（看项目历史 + 变更类型）:
  ├── docs/designs/prototypes/design-tokens.css        → 已有设计令牌
  ├── docs/designs/prototypes/screens/                 → 已有屏幕清单
  ├── docs/designs/prototypes/components/              → 已有共享组件清单
  ├── docs/designs/prototypes/design-system/MASTER.md  → 已有设计系统
  ├── docs/designs/prototypes/index.html               → 产品级全貌
  ├── docs/designs/prototypes/manifest.md              → 全产品原型清单
  └── brand-spec.md                                    → 品牌资产（涉及品牌时）
```

`docs/designs/prototypes/` 不存在时（首次原型设计），系统 SHALL 在 prompt 中标注"无已有设计令牌，请建立"，并按首次设计执行。

INPUT 产出为基础数据包，传递给 OPTIMIZE 步骤进行设计转译。

## 步骤 5：OPTIMIZE — 提示词优化与用户确认

在委托设计引擎之前，编排层 Agent SHALL 深度分析 functional-designs/ 产出优化后的设计 prompt，并通过 AskUserQuestion 展示给用户确认。

### 5.1 菜单结构提取

从 functional-designs/ 中提取并显式化为菜单树：

```
必须明确:
├── 一级菜单项及其对应页面
├── 二级菜单项（如有）及其对应页面
├── 三级菜单项（如有）及其对应页面
├── 导航模式: 顶部导航 / 侧边栏 / Tab Bar / 面包屑
└── 全局组件: Header / Footer / 用户头像 / 通知铃铛等
```

### 5.2 页面元素穷举

对每个页面逐项穷举描述，不得遗漏：

#### 布局分区

每个页面 SHALL 明确划分：header区 / sidebar区 / 主内容区 / 操作栏 / 列表区 / 详情面板 / footer 等布局区域。

#### 可执行操作

```
操作名 → 触发方式 → 预期结果 → 目标页面或弹窗
- 每个可执行操作逐条列出
- 明确触发方式（点击/双击/长按/滑动/悬停等）
- 明确结果（页面跳转/弹窗/抽屉/状态变更/数据刷新）
```

#### 按钮清单

```
按钮名 → 位置 → 样式(主要/次要/文字/危险) → 触发动作 → 前置条件
- 主按钮（Primary）：页面主要操作
- 次按钮（Secondary）：辅助操作
- 文字按钮（Text）：低优先级操作
- 危险按钮（Danger）：删除/不可逆操作
- 前置条件示例: "选中至少一条数据后才可点击"、"表单字段全部必填项已填写"
```

#### 表单清单

```
表单名 → 字段列表:
  ├── 字段 1: 名称 / 类型(input/select/textarea/date/switch/radio/checkbox/...) / 是否必填 / 校验规则 / 默认值 / placeholder
  ├── 字段 2: ...
  └── ...
→ 提交按钮: 按钮名称
→ 提交后行为: 页面跳转 / 弹窗关闭 / 列表刷新 / 状态变更
→ 取消/重置行为（如有）
```

#### 数据展示区

```
数据区域类型（表格/卡片列表/图表/指标卡等）→ 数据字段定义:
├── 表格: 列名 / 数据字段 / 可排序 / 可筛选 / 分页设置 / 行操作按钮
├── 卡片: 卡片字段（标题/副标题/描述/标签/状态/操作按钮）
├── 图表: 图表类型（柱状/折线/饼图等）/ 数据维度 / 指标
└── 指标卡: 指标名 / 数值格式 / 对比值 / 趋势方向
```

#### 状态覆盖

每个页面 SHALL 覆盖以下状态：

| 状态 | 说明 |
|------|------|
| 加载态 | 数据加载中（skeleton / spinner / 进度条） |
| 空态 | 无数据时的展示 + 引导操作 |
| 错误态 | 请求失败时的提示 + 重试操作 |
| 边界态 | 极端数据、长文本、权限受限等情况 |

#### 弹窗/抽屉

```
触发条件 → 弹窗/抽屉标题 → 内容（表单/确认信息/详情）→ 确认/取消按钮行为 → 关闭方式
```

### 5.3 业务流程脚本

SHALL 包含至少一个完整的端到端业务流程脚本，为设计引擎提供 flow demo 的执行路径：

```
流程脚本格式:
├── 流程名称: "用户登录→查看列表→进入详情→编辑→提交→返回列表"
├── 逐步描述:
│   ├── 步骤 1: 用户在 [登录页面] → 输入用户名和密码 → 点击 [登录按钮] → 登录成功后进入 [仪表盘页面]
│   ├── 步骤 2: 用户在 [仪表盘页面] → 点击侧边栏 [XX菜单] → 进入 [列表页面]
│   ├── 步骤 3: 用户在 [列表页面] → 看到数据表格 → 点击某行 [查看详情按钮] → 进入 [详情页面]
│   ├── 步骤 4: 用户在 [详情页面] → 点击 [编辑按钮] → 弹出编辑表单弹窗
│   ├── 步骤 5: 用户在弹窗中 → 修改表单字段 → 点击 [提交按钮] → 提交成功 → 弹窗关闭 → 详情刷新
│   └── 步骤 6: 用户点击 [返回按钮] → 回到 [列表页面] → 列表显示已更新数据
├── 覆盖端到端路径: 从登录入口到最终提交成功的完整路径
└── 如有多条核心流程，逐条编写
```

### 5.4 硬约束注入

优化后的 prompt SHALL 注入以下硬约束：

| 约束类别 | 具体内容 |
|---------|---------|
| **直写产品级原型目录** | 输出到 `docs/designs/prototypes/` 目录（SHALL NOT 在变更级创建原型副本目录）；屏幕页面写入 `screens/`，共享组件写入 `components/`，静态资源写入 `assets/`；同步更新 `index.html` 全产品导航与 `design-tokens.css` |
| **改动记录与备份** | 写入前将受影响文件的改动前副本备份到变更级 `docs/changes/{change}/prototype-backup/`（按产品级相对路径镜像；新增文件不生成快照），并将本次改动登记到变更级 `docs/changes/{change}/prototype-changes.md` |
| **业务流程驱动** | 使用 **flow demo 模式**（可交互业务流程，单台设备状态管理器如 `AppPhone` 驱动），SHALL NOT 仅提供 overview 多屏并排静态展示 |
| **离线自包含** | 所有 CSS/JS/字体/图片资源必须内联或相对路径引用；禁止 `http://` `https://` 外部 CDN 依赖；字体使用系统默认字体栈（如 `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`） |
| **design-system 输出** | 无论选定哪个工具链，设计引擎 SHALL 输出 `docs/designs/prototypes/design-system/MASTER.md`（含色彩方案、字体系统、间距规格、组件规范、交互规则） |
| **design-tokens 输出** | 设计引擎 SHALL 输出 `docs/designs/prototypes/design-tokens.css`（CSS 变量：色板/字号/间距/圆角/阴影），所有屏幕通过 `<link rel="stylesheet">` 引用 |

### 5.5 design-prompt.md 文件输出

OPTIMIZE 步骤完成后，编排层 Agent SHALL 将优化后的完整提示词写入 `docs/changes/{change}/prototype-plan/design-prompt.md` 文件（7 章节模板），作为 DESIGN 步骤的**唯一真相源**。

**文件头部元信息**：
```markdown
> **变更名称**: {change-name}
> **版本**: 1.0.0
> **生成时间**: {YYYY-MM-DD HH:MM}
> **状态**: ⏳ 待确认
```

**7 章节模板**：

| 章节 | 标题 | 内容要求 |
|------|------|---------|
| 一 | 项目背景与设计目标 | 从 functional-designs/ 提取产品概述、原型范围、目标用户、设计意图 |
| 二 | 设计系统（Design System） | 色彩方案（主色/背景色/文字色/边框色/状态色 + 颜色值）、字体系统（系统字体栈 + 标题/正文层级）、间距与圆角规格 |
| 三 | 菜单与导航结构 | 菜单树（一/二/三级菜单项+对应页面+原型文件名）、导航模式（顶部/侧边栏/Tab Bar/面包屑）、全局组件 |
| 四 | 页面详细规格 | 逐页穷举：布局分区（ASCII 线框图）、按钮清单（名称/位置/样式/触发/前置条件）、表单清单（表单名/字段详情/提交行为）、数据展示区（类型/字段/交互）、状态覆盖（加载/空/错误/边界态）、弹窗/抽屉（触发/内容/关闭方式） |
| 五 | 业务流程脚本 | 至少一个完整端到端流程，每步"用户在[页面] → 点击[按钮] → 看到[变化] → 进入[页面]" |
| 六 | 硬约束 | 直写产品级原型目录约束、改动记录与备份约束、flow demo 模式（AppPhone 驱动，禁 overview）、离线自包含（禁 CDN，系统字体栈） |
| 七 | 高保真要求 | 参考资源索引（产品级原型目录/产品级清单/设计令牌/设计系统/品牌资产路径）、交互细节规格（hover/active/focus/过渡动画/Tab 切换）、响应式要求 |

### 5.6 用户确认

```
1. 编排层 Agent 完成 design-prompt.md 写入后
2. 通过 AskUserQuestion 向用户展示提示词摘要:
   Question: "提示词已优化并写入 prototype-plan/design-prompt.md，包含:
     - {n} 个页面的菜单结构
     - {m} 个页面的元素级描述（按钮/表单/数据区/状态覆盖）
     - {k} 个端到端业务流程脚本
     - 硬约束: 直写产品级原型目录 + flow demo 模式 + 离线自包含 + design-system/design-tokens 输出
     是否确认执行？"
   Options:
     - "确认执行" → 更新 design-prompt.md 状态为"已确认" → 进入步骤 6（DESIGN）
     - "需要修订" → 收集用户反馈 → 回到 5.1 修订
3. 用户确认后 → 进入 DESIGN 步骤
4. DESIGN 步骤完成后 → design-prompt.md 状态更新为"已执行"
```

## 步骤 6：DESIGN — 按有效工具链锁定执行

> **子代理隔离规则**：子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管原型生成。最多重试 3 次（1 次初始 + 3 次重试），全部失败后标记 ⚠️ 阻塞并提示用户。重新创建的子代理不依赖前上下文。

DESIGN 步骤分为 6.0 并发写入检测、6.1 STYLE（风格/布局推荐）和 6.2 GENERATE（按工具链锁定执行）。

### 6.0 并发写入检测（主 Agent 执行）

产品级原型目录是多变更共享的写入热点，主 Agent SHALL 在启动 GENERATE 子代理前完成并发写入检测：

```
1. 读取变更级 prototype-changes.md 的改动清单
2. 对每条"修改"或"删除"条目，计算产品级 docs/designs/prototypes/ 下对应文件的当前哈希
3. 与条目记录的"改动前哈希"比对
   ├── 一致 → 正常写入；该条目的改动前哈希在本轮写入后更新为本次写入前的版本哈希
   └── 不一致 → 提示"该文件已被其他变更修改"，通过 AskUserQuestion 交用户裁决:
       - "基于新版本改" → 以磁盘当前版本为基线重新应用本变更的改动意图
       - "覆盖" → 以本变更版本覆盖磁盘文件，并将磁盘版本存入 prototype-backup/
       - "人工合并" → 停止自动写入，等待用户提供合并结果
4. SHALL NOT 在用户裁决前覆盖该文件
5. 裁决过程与结果记录到 prototype-changes.md 的「并发写入裁决记录」段落
```

### 6.1 STYLE — 风格/布局推荐

```
1. 确认 prototype-plan/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype-plan/style-decision.md 不存在（用户未选择过风格）
3. 启动子代理:
   Agent(subagent_type="claude", description="执行风格推荐", prompt="读取 prototype-plan/design-prompt.md 中的项目背景、产品类型、目标用户，推荐 3 个差异化风格方向。每个方向包含：风格名称+设计哲学描述、色彩方案（主色/背景色/文字色/强调色+色值）、字体系统（标题+正文）、布局模式、ASCII 线框图（10 行以内）、适用场景+不适用场景。如 docs/designs/prototypes/manifest.md 存在，同时读取以了解已有设计系统与屏幕结构。")
4. 通过 AskUserQuestion 展示风格选项:
   - 选项 1/2/3: 3 个差异化风格方向（preview 含 ASCII 线框图 + 色彩方案）
   - "需要更多方向": 回到推荐步骤重新生成
   - "自行指定": 用户自由描述期望风格
5. 用户选定后写入 prototype-plan/style-decision.md:
   - selected_style / style_description / ascii_wireframe / decision_time
```

### 6.2 GENERATE — 按有效工具链锁定执行

```
1. 确认 prototype-plan/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype-plan/style-decision.md 存在
3. 确认有效工具链已锁定（docs/changes/{change}/toolchain.md 或 docs/toolchain.md）
4. 启动子代理:
   Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype-plan/design-prompt.md + prototype-plan/style-decision.md 中的完整提示词，按有效工具链中 execution_order 指定的设计引擎和顺序生成 HTML 交互原型。产物直接写入产品级 docs/designs/prototypes/：屏幕写入 screens/，共享组件写入 components/，静态资源写入 assets/，同步更新 index.html 全产品导航与 design-tokens.css，并输出 design-system/MASTER.md。写入前将受影响文件的改动前副本备份到 docs/changes/{change}/prototype-backup/，并将本次改动登记到 docs/changes/{change}/prototype-changes.md。")
   - 子代理严格按 execution_order 调用设计引擎
   - 子代理 SHALL NOT 调用 execution_order 之外的设计 Skill
   - 子代理 SHALL NOT 在 docs/changes/{change}/ 下创建原型副本目录
5. 子代理写入规则:
   ├── 屏幕页面 → docs/designs/prototypes/screens/
   ├── 共享组件 → docs/designs/prototypes/components/
   ├── 静态资源 → docs/designs/prototypes/assets/
   ├── 更新 docs/designs/prototypes/index.html（全产品导航）
   ├── 更新 docs/designs/prototypes/design-tokens.css
   ├── 输出 docs/designs/prototypes/design-system/MASTER.md
   ├── 改动前副本 → prototype-backup/（按产品级相对路径镜像；新增文件不生成快照）
   └── 改动登记 → prototype-changes.md（| 文件路径 | 类型 | 改动前哈希 | 说明 |）
6. 子代理完成后 SHALL 返回结果摘要（成功/失败、生成页面数、改动文件数）
7. 主 Agent 验证产物:
   - 验证 docs/designs/prototypes/index.html 存在且非空
   - 验证 docs/designs/prototypes/design-system/MASTER.md 存在
   - 验证变更级 prototype-changes.md 已生成，且登记的改动条目覆盖产品级原型目录本次实际变更
   - 验证所有内部文件引用目标文件存在
8. 子代理失败: 重试一次，仍失败 → ⚠️ 阻塞，不自行切换工具链
```

> **强制要求**：按有效工具链锁定的设计引擎 SHALL 使用 flow demo 模式——单台设备状态管理器（如 `AppPhone`）。SHALL NOT 仅提供 overview 静态平铺。
>
> `kflow-prototype-design` 不干预设计引擎内部迭代过程。

## 步骤 7：BUILD — 构建门控（唯一必做验证，零子代理）

BUILD 在原型产物生成（DESIGN）之后、审查方式选择之前执行，依次执行四项纯静态检查。此处的"构建"指静态一致性检查，原型为纯 HTML 产物，SHALL NOT 引入编译或打包步骤。

```
7.1 CDN 外部依赖扫描 → 7.2 交叉引用完整性 → 7.3 必检产物存在 → 7.4 清单与磁盘一致
- 四项检查 SHALL 全部执行，SHALL NOT 因前一项结论跳过后续检查
- 全部四项由主 Agent 在其上下文内直接完成，SHALL NOT 启动任何子代理
- 任一项不通过 → 修复后重跑 BUILD 的全部四项检查，循环至全部通过
- 不通过时 SHALL NOT 进入后续步骤（审查方式选择、用户评审）
```

### 7.1 CDN 外部依赖扫描

```
1. 扫描 docs/designs/prototypes/ 目录下所有 .html 文件
2. 使用 grep 或文本搜索检测 http:// 或 https:// 模式的外部资源引用:
   ├── <link href="http..."> 或 <link href="https..."> → 违规（外部 CSS）
   ├── <script src="http..."> 或 <script src="https..."> → 违规（外部 JS）
   ├── <img src="http..."> 或 <img src="https..."> → 违规（外部图片）
   ├── @import url(http...) 或 @import url(https...) → 违规（外部 CSS import）
   └── url(http...) 或 url(https...) in inline CSS → 违规（外部字体/背景图）
3. 若发现外部依赖:
   ├── 在报告中列出所有违规文件和具体引用 URL
   ├── 标记 CDN 扫描不通过
   └── 返回 DESIGN 步骤修复
4. 若 CDN 扫描通过（无任何外部引用）→ 记录"离线自包含检查通过"
```

### 7.2 多文件交叉引用完整性检查

```
1. 提取 docs/designs/prototypes/ 下所有文件中指向本目录的内部引用目标:
   ├── <a href="screens/*.html"> 等超链接目标
   ├── <iframe src="screens/*.html"> 等嵌入目标
   └── <script src="components/*.js"> 等本地脚本引用
2. 验证每个引用目标文件在 docs/designs/prototypes/ 目录下实际存在
3. 若发现断链（引用目标文件不存在）→ 在报告中列出 → 返回 DESIGN 步骤修复
4. 若所有引用完整 → 记录"交叉引用检查通过"
```

### 7.3 必检产物存在性检查

```
1. 验证 docs/designs/prototypes/design-system/MASTER.md 存在，且包含:
   ├── 色彩方案（含色值）
   ├── 字体系统（标题 + 正文字体）
   ├── 间距规格
   ├── 组件规范
   └── 交互规则
2. 验证 docs/designs/prototypes/design-tokens.css 存在且含 CSS 变量声明
3. 任一产物缺失 → ⚠️ 阻塞，返回 DESIGN 步骤补齐
4. 产物均存在 → 记录"必检产物检查通过"
```

### 7.4 清单与磁盘一致性检查

```
1. 验证 docs/designs/prototypes/manifest.md 存在
2. 双向比对清单声明的文件与实际磁盘文件:
   ├── 清单声明但磁盘不存在 → 违规
   └── 磁盘存在但清单未声明 → 违规
3. 验证清单中至少包含一个角色为 entry 的文件条目
4. 任一项不通过 → 返回 DESIGN 步骤修复
```

### BUILD 报告

主 Agent SHALL 将四项检查结果汇总输出到 `docs/changes/{change}/self-reviews/prototype/cdn-crossref-check/report.md`，包含：

- 扫描范围（文件列表）、发现的外部引用（文件/引用 URL/类型）
- 引用完整性矩阵（源文件/引用路径/目标文件是否存在）与断链清单
- 必检产物存在性结果
- 清单与磁盘双向比对结果
- 四项检查各自结论（通过/不通过）

CDN 扫描不通过时，其余三项检查 SHALL 继续执行并记录结果，所有问题汇总在同一份 `report.md` 中。**该报告在两种审查方式下均产出。**

## 步骤 8：审查方式选择

BUILD 四项静态检查全部通过后，通过 AskUserQuestion 询问用户选择审查方式：

```
Question: "原型已生成并通过 BUILD 门控（CDN 扫描 / 交叉引用 / 必检产物 / 清单一致 四项通过）。
是否执行子代理自动审查验证？
  - 子代理自动审查验证：VERIFY 单轮合并验证（导航合理性 / Playwright 全覆盖 / UX 规则审查 / 对比度检测 四分区）+ SELFREV 单轮验证
  - 人工审查：跳过全部自动验证，直接进入用户评审"
Options:
  - "子代理自动审查验证" → 进入步骤 9 VERIFY 与步骤 10 SELFREV
  - "人工审查" → 跳过步骤 9 与 10，直接进入步骤 11 REVIEW
```

```
1. 用户选定后 SHALL 将选择结果记录到 .status.md 原型阶段条目
2. 后续 VERIFY 与 SELFREV 步骤 SHALL 依据该记录决定是否执行
3. 变更从 .status.md 恢复执行且已记录审查方式时:
   ├── SHALL 读取已记录的审查方式
   └── SHALL NOT 重复询问审查方式
4. SHALL NOT 在 BUILD 未通过时发起该询问
```

## 步骤 9：VERIFY — 子代理自动审查验证（单轮合并验证，条件执行）

> **前置条件**：本步骤仅在审查方式为「子代理自动审查验证」时执行。审查方式为「人工审查」时，系统 SHALL 完全跳过本步骤全部子步骤，SHALL NOT 启动任何验证子代理，直接进入步骤 11 REVIEW。

> **子代理隔离规则**：验证子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管验证执行。最多重试 3 次（1 次初始 + 3 次重试），全部失败后标记 ⚠️ 阻塞并提示用户。

### 单轮合并验证总览

导航合理性、Playwright 全覆盖与 UX 规则审查三项验证 SHALL 合并为**一轮子代理、一份合并报告**，SHALL NOT 为三项验证分别启动独立子代理、SHALL NOT 执行第二轮。对比度检测为静态计算，不启动独立子代理。BUILD 四项静态门控另在步骤 7 由主 Agent 直接执行（零子代理，两种审查方式下均执行）。

```
主 Agent 启动 1 个验证子代理（Agent(subagent_type="claude")，独立上下文）
  ├── 分区一 导航合理性（5 项检查）
  ├── 分区二 Playwright 全覆盖（5 项检查）
  ├── 分区三 UX 规则审查（逐项结论）
  ├── 分区四 对比度检测（WCAG 相对亮度静态计算）
  ├── 范围外观察小节（为空时记「（空）」）
  └── 验证结论（发现总数 N + 全量遍历证明）
→ 只报告，SHALL NOT 修改产物
→ 报告路径: self-reviews/prototype/verify-report.md
→ 主 Agent 读取报告 → 统一修复原型文件 → 生成「本阶段修复清单」→ 进入步骤 10 SELFREV
```

### 合并验证规则

| 规则 | 说明 |
|------|------|
| 子代理类型 | `Agent(subagent_type="claude")`，独立上下文，仅 1 个 |
| 单轮执行 | 同一轮内完成导航合理性、Playwright 全覆盖与 UX 规则三项验证的全部检查项；SHALL NOT 执行第二轮 |
| 报告分区 | 报告 SHALL 按「导航合理性 / Playwright 全覆盖 / UX 规则审查 / 对比度检测 / 验证结论」强制分区，每分区 SHALL 独立给出该环节全部检查项的逐项结论；缺少任一环节独立结论时报告 SHALL 判定为不完整，主 Agent SHALL 要求子代理补齐后重新提交 |
| 对比度检测 | 静态计算（WCAG 相对亮度），标记对比度 < 4.5:1 的颜色对，SHALL NOT 启动独立子代理 |
| 报告路径 | `self-reviews/prototype/verify-report.md`（固定路径，SHALL NOT 产出按轮次编号的多份报告，SHALL NOT 创建按环节拆分的检查子目录） |
| 只报告不修改 | 合并验证子代理 SHALL NOT 修改任何原型产物；全部发现项由主 Agent 统一修复并生成「本阶段修复清单」，SHALL NOT 追加确认轮 |
| 审查范围冻结与范围外观察 | 审查对象集合由主 Agent 从原型阶段既有产物生成并冻结，审查维度限于导航 5 项、Playwright 5 项、UX 规则与对比度检测四类固定检查项；范围外发现记为「范围外观察」，不改产物、不计入发现数 |
| 子代理异常 | 意外停止、报错退出或返回不完整结果时，主代理 MUST 重新创建新的子代理；SHALL NOT 接管；最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户 |

### 分区一：导航合理性（5 项检查）

合并验证子代理 SHALL 在本轮内执行以下全部 5 项导航合理性检查：

1. 页面可达性：从 `docs/designs/prototypes/index.html` 出发 BFS 遍历所有 `<a href>` 和导航组件引用，生成可达性矩阵，标记孤立页面（无任何入口链接指向）与死胡同页面（无任何出口链接）
2. 返回/取消按钮合理性：穷举所有返回/取消/关闭按钮，验证目标页面是其语义父页面（详情→列表、表单取消→进入前页面、弹窗关闭→上下文不变），标记语义不合理的返回目标
3. 表单切换链：验证多步表单上一步/下一步链条完整，提交成功去向明确且合理，提交失败留在当前页保留数据，标记断链或去向不明确的表单
4. 弹窗/抽屉导航：验证每个弹窗/抽屉触发方式正确、所有关闭方式可用（确认/取消/遮罩/Esc）、嵌套层级逐层关闭，标记关闭后上下文错乱的情况
5. 跨页面流程闭环：按业务流程脚本逐条走通完整导航路径，验证从入口到终点能回到起点（闭环），无「跳进去出不来」的页面序列，标记流程断点

### 分区二：Playwright 全覆盖（5 项检查）

合并验证子代理 SHALL 在本轮内执行以下全部 5 项 Playwright 检查。工作目录 SHALL 固定为项目根目录，原型 HTML 文件 SHALL 通过 `docs/designs/prototypes/index.html` 相对路径引用。

1. 页面可达性：从 index.html 出发 BFS 遍历所有 `<a>` 链接，每个页面验证加载成功（HTTP 200 或无 pageerror）且 `pageerror` 数量 = 0，输出页面可达性矩阵
2. 按钮/链接全覆盖：穷举每个页面所有 `<button>` 和 `<a>`，逐个点击验证有响应（页面跳转/弹窗打开/状态变更/控制台无错误），`disabled` 状态按钮验证其不可点击，输出按钮/链接覆盖清单
3. 表单全覆盖：每个表单执行空提交（校验提示正确显示）+ 合法数据提交（提交行为正确）+ 取消/重置操作，输出表单覆盖清单
4. 弹窗/抽屉全覆盖：每个弹窗/抽屉验证所有打开方式和所有关闭方式（确认/取消/点击遮罩/Esc），弹窗内表单和按钮按上述规则验证，输出弹窗覆盖清单
5. 端到端业务流程：按 `prototype-plan/design-prompt.md` 中业务流程脚本逐条走通，验证每个流程无 JS 错误、无交互断点、无死胡同，输出流程通过清单

Playwright 使用 `.kflow-runtime/playwright/` 下的隔离安装。SHALL NOT 在 `docs/designs/prototypes/` 目录下执行 npm install 或 npx playwright。

**Playwright 不可用降级**：
```
1. 检查 .kflow-runtime/playwright/node_modules/playwright 是否存在
2. 若不存在:
   ├── 优先执行隔离安装引导: cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium
   ├── 安装成功 → 使用隔离安装继续 Playwright 验证
   └── 安装失败 → 降级为手动文件分析
3. 若 playwright-cli 不可用且无法安装:
   ├── 子代理 prompt 中指示降级为手动文件分析
   ├── 在报告「Playwright 全覆盖」分区记录降级原因
   └── 报告标注 "Playwright 不可用 — 降级为手动检查"
```

**运行时隔离**：验证终止后，`docs/designs/prototypes/` 目录 SHALL NOT 包含 `node_modules/`、`package.json`、`package-lock.json`。若发现，SHALL 在 POST_HOOK BROWSER_CLEANUP 中清理。

### 分区三：UX 规则审查（逐项结论）

合并验证子代理 SHALL 在本轮内执行 UX 规则审查并逐项给出结论：按本阶段既有 UX 规则检查项逐项审查 `docs/designs/prototypes/` 目录下所有 HTML 文件，精简核心规则集（20-30 条）：对比度 ≥4.5:1、触摸目标 ≥44px、表单 label 非 placeholder-only、按钮视觉反馈、弹窗关闭方式、错误恢复路径、必填标记、空态引导、加载态 skeleton、导航层级 ≤3、内联验证、主操作突出、无水平滚动溢出、文字 ellipsis 截断、图片 alt/aria-label、焦点状态可见、无自动播放、正确 input-type、破坏性操作确认、Toast 自动消失 3-5s。每项检查 SHALL 给出独立结论，发现的问题 SHALL 记入合并报告的「UX 规则审查」分区。如环境中存在 ui-ux-pro-max，其完整 99 条 UX 规则库作为"可选增强"纳入本分区检查项。

### 分区四：对比度检测（静态计算）

对比度检测 SHALL 作为静态计算执行于合并报告内，SHALL NOT 启动独立子代理。

```
1. 扫描 docs/designs/prototypes/ 目录下所有 .html 文件
2. 提取所有文本颜色对（背景色 + 前景色）
3. 使用 WCAG 相对亮度计算公式: L = 0.2126*R + 0.7152*G + 0.0722*B（sRGB 线性化）
4. 对比度 = (L1+0.05)/(L2+0.05)，L1 > L2
5. 标记 <4.5:1 的颜色对（不满足 WCAG AA）
6. 结果写入合并报告的「对比度检测」分区，含所有颜色对及对比度值、⚠️ 不达标标记、建议替代色值
```

### 验证结论分区与统一修复

「验证结论」分区 SHALL 给出发现总数 N、发现清单与全量遍历证明。主 Agent SHALL 从 `self-reviews/prototype/verify-report.md` 读取报告，对发现的问题统一修复原型文件，并生成「本阶段修复清单」；SHALL NOT 追加确认轮。修复完成后进入步骤 10 SELFREV。

### 审查范围冻结与范围外观察

审查对象集合 SHALL 由主 Agent 从原型阶段既有产物生成并冻结，审查维度 SHALL 限于导航合理性 5 项、Playwright 5 项、UX 规则与对比度检测四类固定检查项。子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增检查维度、SHALL NOT 借验证之名新增功能点/字段/章节/分支。冻结范围之外的发现 SHALL 记为「范围外观察」——SHALL NOT 触发产物修改、SHALL NOT 计入验证发现数，写入合并报告的「范围外观察」小节（为空时记「（空）」），由主 Agent 在阶段终止时汇总全部范围外观察条目并向用户提示。

## 步骤 10：SELFREV — 按变更档位自审（签署清单 + 单轮验证，条件执行）

> **前置条件**：本步骤仅在审查方式为「子代理自动审查验证」时执行。审查方式为「人工审查」时，prototype 阶段 SHALL 完全跳过 SELFREV，不得启动任何验证子代理，SHALL NOT 保留兜底轮次，系统直接进入步骤 11 REVIEW。该跳过属**流程分支**，SHALL NOT 被视为 0 轮豁免。

### 子代理上下文文件加载（基础层 + 创意层）

自审验证子代理 prompt 中 SHALL 包含以下文件：

- `skills/kflow-prototype-design/references/state-values.md`（摘要）
- `skills/kflow-prototype-design/references/gates.md`（当前阶段相关门控）
- `skills/kflow-prototype-design/references/self-review.md`

> **子代理隔离规则**：验证子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管验证执行。最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户。

### 自审模型：签署自证 → 单轮独立验证 → 统一修复

> **v3.0.0 变更（BREAKING）**：自审终止模型由「多轮收敛循环」改为**固定单轮**——删除多轮收敛判据、失败终止判定、跨轮摘要注入与跨轮修复清单。验证子代理改为**只报告不修改产物**（审查者与修复者分离）。自审由三个环节构成：

```
1. 主 Agent 签署自证（零子代理）→ 写作时按 4 维度逐项填写「维度 / 自证结论 / 证据锚点」
2. 单轮独立子代理验证         → 先独立遍历产物（不读签署清单）→ 再逐项打假 → 只报告不修改
3. 主 Agent 统一修复          → 修复全部发现项，产出「本阶段修复清单」随产物交付下游
```

系统 SHALL NOT 预置任何审查轮数、SHALL NOT 执行第二轮、SHALL NOT 存在 0 轮豁免路径。终止结果 SHALL 为 `验证通过` 或 `验证发现问题({N})`，写入变更级 `.status.md`。

> **档位语义**：变更档位只决定**审查形态与产出深度**，SHALL NOT 决定自审轮数（轮数恒为 1）。自审启动前 SHALL 读取变更级 `.status.md` 基本信息的「变更档位」字段；字段缺失或读取到历史遗留的 `完整` 取值时按 `标准` 档处理。

> **独立验证的归属**：本机制只承担「写作质量控制 + 单轮打假」。**真正的独立验证留给用户评审（REVIEW）环节**——主 Agent 统一修复后生成的「本阶段修复清单」随产物一并交付，原型阶段的修复结果由用户评审确认。

### 签署清单

签署清单 SHALL 按本阶段专属的 4 个维度（覆盖性 / 一致性 / 可用性 / 完整性，覆盖性为第一优先级）组织，每个维度 SHALL 包含「维度」「自证结论」「证据锚点」三列：

| 维度 | 自证结论 | 证据锚点 |
|------|---------|---------|
| {维度名} | 通过 / 不通过 | {产物内的具体位置} |

- **证据锚点 SHALL 指向产物内的具体位置**——页面文件名、FP-ID、元素/组件名或 design-prompt.md 章节号之一；SHALL NOT 为「全文」「多处」「见上文」之类的模糊指向
- **签署不成立判定**：锚点为空，或锚点指向的位置在产物中不存在、内容不匹配 → 该维度签署判定为**不成立**；任一维度签署不成立时该阶段 SHALL NOT 判定为签署通过
- 签署区 SHALL 作为阶段产物模板的组成部分存在于产物中（如 `prototype-plan/design-prompt.md`），SHALL NOT 以独立文件形式产出
- 产物初稿完成后主 Agent SHALL 逐个 4 维度完成签署自证，**SHALL NOT 启动子代理**；自证中发现某维度不通过时 SHALL 先修复该产物并重新完成该维度自证

### 单轮验证

主 Agent SHALL 启动**一个**验证子代理（`Agent(subagent_type="claude")`，独立上下文、不共享主 Agent 对话历史），其执行顺序强制为：

```
1. 独立遍历产物 → 形成自己的 4 维度结论      ← 此阶段 SHALL NOT 读取签署清单
2. 逐项对照签署清单 → 打假                   ← 锚点为空 / 指向不存在内容 = 签署不成立
3. 输出 { 独立发现问题 | 签署打假结果 | 全量遍历证明 | 范围外观察 | 验证结论 }
4. SHALL NOT 修改任何产物（只报告）
```

- 执行顺序反转时该轮验证结果 SHALL NOT 被接受，主 Agent SHALL 重新启动验证子代理
- **子代理异常处置**：意外停止、报错退出或返回不完整结果时，主代理 MUST 分析原因后重新创建新的子代理，SHALL NOT 在主 Agent 上下文中接管其未完成的工作；最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户

**审查范围冻结与范围外观察**：主 Agent SHALL 在单轮验证启动前从原型阶段产物既有内容生成**审查对象集合**并冻结，审查维度 SHALL 限于本阶段固定 4 个维度枚举；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点/字段/章节/分支。冻结范围之外的发现降级为「范围外观察」——不改产物、不计入发现数，写入报告的「范围外观察」小节（为空时记「（空）」）。子代理引入冻结范围外新内容时主 Agent SHALL 拒收并要求在冻结范围内重新验证，越界事实记录到 `docs/skill-suggestion.md`。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。

**验证发现分级与终止结果**：

| 终止结果 | 判定口径 |
|---------|---------|
| `验证通过` | 单轮验证零发现 **且** 无签署不成立项 |
| `验证发现问题({N})` | 存在发现项 **或** 存在签署不成立项；N 为该阶段发现总数 |

- 仅存在范围外观察而无范围内发现时，发现数记为 0（其余条件同时满足时终止结果 MAY 为 `验证通过`）
- 读取兼容：读取侧遇到历史变更遗留的 `收敛` 取值 SHALL 归并为 `验证通过`，其余历史取值 SHALL 归并为 `验证发现问题`

**轻量档产物完整性门控**：轻量档 SHALL 执行单轮自审，SHALL NOT 跳过自审。产物完整性门控 SHALL 保留为附加硬门：

- 阶段产物 SHALL 对照本 SKILL.md「输出产物」章节清单逐项存在，且 SHALL NOT 含 `TODO` / `TBD` / 未填充占位符
- `self-reviews/prototype/report.md` SHALL 存在（缺失判缺项）
- 门控不通过 → 标记 ⚠️ 阻塞并修复后重跑；门控通过 → 进入步骤 11 REVIEW

自审维度与检查规则见下节，辅助规则见 [references/self-review.md](references/self-review.md)。

### 审查维度与检查规则

#### 覆盖性（第一优先级）

| 检查项 | 规则 |
|--------|------|
| 页面覆盖 | 是否所有 FP 有对应原型页面 |
| 操作覆盖 | 是否所有可执行操作有对应交互组件 |
| 表单项覆盖 | 是否所有表单项有对应表单组件 |

#### 一致性

| 检查项 | 规则 |
|--------|------|
| 视觉风格 | 组件命名是否一致，颜色/字体/间距是否统一 |
| 布局模式 | 页面布局模式（导航方式、内容区划分）是否统一 |
| 交互模式 | 按钮样式、表单行为、弹窗/抽屉等交互模式是否一致 |

#### 可用性

| 检查项 | 规则 |
|--------|------|
| 交互流畅性 | 交互流程是否顺畅（点击次数、跳转层级合理） |
| 状态覆盖 | 交互状态覆盖是否完整（加载态/空态/错误态/边界态） |
| 反馈机制 | 用户操作是否有明确的即时反馈（成功/失败/进行中） |

#### 完整性

| 检查项 | 规则 |
|--------|------|
| 入口可达 | 所有页面入口是否可从导航到达（无孤立页面） |
| 组件状态 | 组件全部状态是否覆盖（default/hover/active/disabled/focus） |
| 流程闭环 | 交互流程是否形成闭环（可前进可后退/可取消） |

### 验证报告内容

单轮验证子代理 SHALL 生成一份验证报告到 `self-reviews/prototype/report.md`（固定路径，SHALL NOT 按轮次编号、SHALL NOT 产出多份时间戳文件），SHALL 包含：

| 小节 | 内容 |
|------|------|
| 签署清单打假结果 | 逐维度列出：维度名、自证结论、证据锚点、打假结论（属实 / 不成立）、不成立原因 |
| 独立发现问题清单 | 序号、问题描述、严重度、所属维度（来自独立遍历，与签署清单对照结果分开呈现） |
| 范围外观察 | 冻结审查对象集合之外发现的条目；无条目时记「（空）」 |
| 全量遍历证明 | 显式声明全部 4 个审查维度与全部审查对象均已完成遍历 |
| 验证结论 | 发现总数 N；终止结果 `验证通过` 或 `验证发现问题({N})` |

> **反空转条款**：未证明全量遍历的报告 SHALL 判定为不完整，主 Agent SHALL 要求子代理补齐后重新提交。

### 统一修复与流转

验证完成后，主 Agent SHALL 统一修复全部发现项（仅修复报告确认的问题，不做重构或额外改进，SHALL NOT 新增冻结审查对象集合之外的内容），SHALL NOT 追加确认轮，SHALL 生成「本阶段修复清单」随产物交付。修复完成后写入 `.status.md` 终止结果，随后进入步骤 11 用户评审（AskUserQuestion），释放 design 阶段门控。

### 与 VERIFY 子代理模式的对比

| 维度 | SELFREV（自审） | VERIFY（合并验证） |
|------|----------------|---------------|
| 执行者 | 签署自证：主 Agent（零子代理）+ 验证：1 个子代理 | 1 个独立子代理 |
| 目的 | 维度级自证 + 单轮打假 | 导航/Playwright/UX/对比度四环节全覆盖验证 |
| 范围 | 4 维度签署清单 + 独立遍历 | 具体检查项（可达性、按钮、表单、弹窗、流程、UX、对比度） |
| 轮次 | 恒为 1 轮 | 恒为 1 轮（三环节合并） |
| 报告 | `self-reviews/prototype/report.md` | `self-reviews/prototype/verify-report.md`（四分区） |
| 触发条件 | 仅「子代理自动审查验证」路径 | 仅「子代理自动审查验证」路径 |

### 强制执行规则

- 全部档位 SHALL 执行单轮自审，SHALL NOT 存在 0 轮豁免路径；轮数恒为 1，SHALL NOT 执行第二轮
- 档位 SHALL 以变更级 `.status.md` 的「变更档位」字段为准（缺失或历史取值 `完整` 按 `标准` 档处理），SHALL NOT 依据 `docs/CONTEXT.md` 存在性或 `docs/designs/detailed-designs/` 是否为空判定
- 签署自证 SHALL 由主 Agent 执行（零子代理），逐维度填写自证结论与证据锚点；锚点 SHALL 指向产物内具体位置，锚点为空或指向不存在内容判该维度签署不成立
- 验证 SHALL 由 1 个独立子代理执行，先独立遍历（不读签署清单）后逐项打假；子代理 SHALL NOT 修改任何产物，全部修复由主 Agent 统一执行
- 审查对象集合 SHALL 由主 Agent 从阶段产物既有内容生成并冻结，审查维度限于覆盖性/一致性/可用性/完整性四维枚举（覆盖性为第一优先级）；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度
- 冻结范围之外的发现 SHALL 记为「范围外观察」，SHALL NOT 修改产物、SHALL NOT 计入发现数；引入范围外新内容的验证 SHALL 被拒收并要求在冻结范围内重新验证
- 统一修复 SHALL 仅修复报告确认的问题，SHALL NOT 追加确认轮；「本阶段修复清单」SHALL 随产物交付
- 验证报告 SHALL NOT 输出各维度 0–10 评分与不达标项清单（该评分要求原为第三档专属的报告输出深度，已随该取值一并废除）
- 终止结果 SHALL 写入 `.status.md`，取值 `验证通过` / `验证发现问题({N})`
- 子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管验证执行；最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户
- 主 Agent SHALL 在阶段终止时汇总「范围外观察」条目并向用户提示
- 自审终止后进入用户评审确认（AskUserQuestion），释放 design 阶段门控

## 步骤 11：REVIEW — 用户评审循环

### 评审交互

通过 AskUserQuestion 向用户展示：

```
Question: "HTML 原型已完成，覆盖 {n} 个屏幕、{m} 个 UI 功能点。
[BUILD 门控: CDN 扫描 {通过/不通过} | 交叉引用 {通过/不通过} | 必检产物 {通过/不通过} | 清单一致 {通过/不通过}]
[审查方式: {人工审查 / 子代理自动审查验证}]
--- 审查方式为「子代理自动审查验证」时追加 ---
[VERIFY 合并验证（单轮，四分区）: 导航合理性 {通过/不通过} | Playwright 全覆盖 {通过/降级为手动检查} | UX 规则审查 {通过/不通过} | 对比度检测 {通过/不通过}，发现并修复 {x} 个问题]
[自审（签署清单 + 单轮验证）: {档位} 档，终止结果 {验证通过/验证发现问题({N})}，发现并修复 {z} 个问题]
是否确认通过？"
Options:
  - "确认通过" → 原型满足需求，进入详细设计
  - "需要修订" → 收集用户反馈 → 回到 DESIGN 步骤
```

### 评审循环机制

```
DESIGN(子代理委托，直写产品级) → BUILD(四项静态检查) → 审查方式选择
  ├── 人工审查            → REVIEW
  └── 子代理自动审查验证  → VERIFY(单轮合并验证：导航/Playwright/UX/对比度四分区) → SELFREV(单轮验证) → REVIEW
REVIEW
  ├── 确认通过 → COMPLETE
  └── 需修订 → 收集用户反馈 → 回到 DESIGN（再次启动子代理，附修订要求）
```

### 评审结果处理

| 用户选择 | 阶段状态 | 评审记录 | 后续动作 |
|---------|---------|---------|---------|
| 确认通过 | ✅ 完成 | ✅ 已确认 | 门控释放，可进入详细设计 |
| 需要修订 | ⚠️ 需修订 | ⚠️ 需修订 | 保持原型设计阶段，根据用户反馈修订原型 |

## 步骤 12：COMPLETE — 更新状态文件 + 同步清单 + 提取设计令牌与元素覆盖树

更新 `docs/changes/{change}/.status.md`：
1. 标记原型设计阶段: `✅ 完成`（或 `⏭️ 跳过`）
2. 记录用户评审结果到「用户评审记录」表
3. 设置当前阶段为「详细设计」
4. 记录完成时间和执行备注

### 12.1 同步产品级原型清单

```
1. 重新扫描产品级 docs/designs/prototypes/ 目录
2. 按模板生成/更新 docs/designs/prototypes/manifest.md:
   ├── 一、产物组织方式（文件结构类型、入口文件路径、共享资源目录）
   ├── 二、原型文件清单（文件/说明/角色/来源变更/版本）
   ├── 三、页面清单（页面名称/路由路径/对应原型文件/所含区域）
   ├── 四、设计系统引用（色彩/字体/间距/组件库及其在 design-system/MASTER.md 中的来源章节）
   ├── 五、共享资源清单（components/、assets/ 下文件及用途）
   └── 六、修订记录（版本、日期、修订类型、修订内容、影响功能点、触发阶段），修订模式时版本号递增
3. 确保变更级 prototype-changes.md 完整记录本变更对产品级原型目录的全部改动
4. 清单 SHALL 反映全产品原型的最终产物全貌，而非初始模板
```

### 12.2 原型通过后自动提取设计令牌和元素覆盖树

当用户在 REVIEW 步骤中"确认通过"后，SHALL 从实际原型 HTML 文件中提取：

**提取 design-tokens.css（产品级）**：

```
1. 扫描产品级 docs/designs/prototypes/ 目录下所有 .html 文件
2. 提取范围 SHALL 限定为本变更涉及的页面（依据变更级 prototype-changes.md 的改动清单）
3. 提取 :root { ... } 中的 CSS 变量声明
4. 提取内联 style 中的颜色值、font-size、border-radius、box-shadow 等
5. 去重、排序、归类后输出到 docs/designs/prototypes/design-tokens.css
6. 文件头部标注: 提取来源（原型版本、生成时间、自动提取）
7. 本变更新增的 CSS 变量 SHALL 追加到产品级 design-tokens.css，并注释标注来源变更和追加时间
8. SHALL 在变更级 prototype-changes.md 中登记 design-tokens.css 的改动条目
```

**提取 element-coverage-tree.md（变更级）**：

```
1. 从产品级 docs/designs/prototypes/ 目录下本变更涉及页面的 .html 文件中解析 DOM 树
2. 提取页面导航骨架: 所有 <a href> 和导航组件引用 → 📄 页面节点
3. 提取交互元素: <button>, <a>, <input>, <select>, <textarea>, <dialog>,
   [role="dialog"], <details> → 🔘/📝/📊 元素节点
4. 提取 CSS 伪类状态: :hover, :active, :focus, :disabled
   + class 命名推测: is-loading, is-error, is-empty, is-disabled, is-active → 🎯 状态节点
5. 提取操作链: 扫描 JS 事件绑定（onclick, addEventListener, @click, onClick）
   → 分析 DOM 操作推断弹窗/下拉/跳转 → 💬/🔗 子树
6. 输出变更级 docs/changes/{change}/element-coverage-tree.md（初始版，TC-ID 列为空）
7. 文件位置 SHALL 固定于变更根目录，使 TC-ID 追溯保持在变更级，避免被后续变更覆盖
8. 文件头部标注: 生成时间戳和来源（prototype-design 阶段自动生成）
```

> **说明**：元素覆盖树承载 TC-ID 映射，是变更级追溯产物，design 阶段会在其上追加填充；设计令牌描述产品整体视觉规范，属产品级资产，被 code 与 code-review 阶段消费。

**原型迭代后重新生成**: 修订模式用户确认通过后，重新执行上述提取，覆盖旧版本。若 design 阶段已填充 TC-ID，通过 AskUserQuestion 确认是否保留已有映射。同时 SHALL 重新扫描产品级目录，更新 `manifest.md` 中的文件清单和版本号。

**跳过时不生成**: 原型设计阶段被跳过（⏭️ 跳过）时，不生成 `docs/designs/prototypes/design-tokens.css` 和 `element-coverage-tree.md`。后续 code 和 code-review 阶段不执行原型对账。

### 12.3 阶段衔接决策

状态文件、产品级清单与提取产物更新完成后 SHALL 执行阶段衔接决策，规则见 [references/phase-transition.md](references/phase-transition.md)（决策表与调度映射表的单一真源；本步骤只引用，SHALL NOT 内联决策表或调度映射表）。

- **门控先于衔接**：步骤 11 的原型用户评审门控 SHALL 在衔接决策之前完成——评审「确认通过」后进入本步骤；评审「需要修订」时按步骤 11 既有规则回到 DESIGN 修订，不进入衔接决策
- **跳过分支同样衔接**：本阶段因纯后端项目 / 无 UI 功能点 / 用户拒绝而标记 `⏭️ 跳过` 时，SHALL 同样执行衔接决策，按决策表处理目标阶段
- **调度方式**：按决策表判定下一阶段（详细设计）的状态后直接调度 `kflow-design`（`Skill(skill="kflow-design", args="{change-name}")`）
- **SHALL NOT 提示推进指令**：系统 SHALL NOT 将「提示用户输入推进指令（如「继续 {change-name}」）」作为进入下一阶段的必要条件
- **停止衔接时说明原因**：衔接决策停止（目标阶段 `❌ 阻塞` 等）时 SHALL 向用户说明停止原因与可执行的下一步操作

## 步骤 13：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 POST_HOOK（🔶 浏览器类型：BROWSER_CLEANUP + UPDATE_STATE）。

BROWSER_CLEANUP SHALL 同时清理 `docs/designs/prototypes/` 下残留的 `node_modules/`、`package.json`、`package-lock.json`。

---

## 原型改动回滚（按需，非流程步骤）

当变更被废弃，或用户要求撤销本变更对产品级原型的改动时，系统 SHALL 依据变更级 `prototype-changes.md` 与 `prototype-backup/` 把产品级原型目录恢复到本变更介入之前的状态：

```
1. 读取变更级 prototype-changes.md 的改动清单
2. 向用户展示受影响的文件清单（产品级相对路径 + 改动类型），取得确认
3. 逐条处理:
   ├── 类型为「修改」或「删除」的条目 → 用 prototype-backup/ 中对应产品级相对路径的快照恢复
   └── 类型为「新增」的条目 → 删除产品级 docs/designs/prototypes/ 中的对应文件
4. 回滚完成后在 prototype-changes.md 的改动清单中标记对应条目已回滚，并写入「四、回滚记录」
```

回滚属于原型设计阶段的职责范围。下游阶段 SHALL NOT 自行执行原型回滚，须经 REVISION 模式或本流程回退到原型设计阶段处理。

## 审查产物存放约束

原型设计阶段的所有审查与验证产物 SHALL 统一存放在变更级 `self-reviews/prototype/` 目录下，SHALL NOT 将验证报告散落在产品级原型目录 `docs/designs/prototypes/` 下。产品级原型目录只承载原型产物本身（`index.html`、`screens/`、`components/`、`assets/`、`design-tokens.css`、`design-system/MASTER.md`、`manifest.md`）。

---

## 跳过条件

| 条件 | 处理方式 |
|------|---------|
| 纯后端项目 | 自动跳过，标记 ⏭️ 跳过 |
| functional-designs/ 中无前端/UI 功能点 | 自动跳过，标记 ⏭️ 跳过 |
| 用户在 AskUserQuestion 中主动拒绝 | 跳过，标记 ⏭️ 跳过 |
| 需重新选择工具链且 prototype-gen 角色 Skill 数量 = 0 | ⚠️ 阻塞，提示安装 huashu-design 或 frontend-design，**不跳过** |

## 修订模式双入口

修订模式有两种入口。修订模式下 SHALL 跳过 INPUT 与 OPTIMIZE，不重新生成 design-prompt.md，不重新执行工具链选择。

### 入口 A: CHECK 步骤检测到已有原型工作（用户驱动修订）

变更级 `prototype-changes.md` 存在且非空时，进入修订模式分支：

```
1. 加载产品级 docs/designs/prototypes/manifest.md 与 screens/ 清单作为现有原型上下文
2. 加载变更级 prototype-plan/design-prompt.md 作为已有设计约束
3. 加载变更级 prototype-changes.md 获取已有改动清单与改动前哈希
4. 加载有效工具链作为已有锁定
5. 合并用户修订需求到 prompt → 进入 DESIGN
```

现有原型存在但用户无明确修订需求时，通过 AskUserQuestion 询问：「本变更已做过原型工作（prototype-changes.md 已存在）。是否要调整？」→「要调整，描述修改内容」进入修订模式 / 「查看现有原型」展示原型摘要，不修改，退出。

如 design-prompt.md 不存在，基于现有原型反向生成最小约束文件。如有效工具链未锁定，执行一次最小化 TOOLCHAIN 选择。

### 入口 B: code 阶段驱动回退（编码驱动修订）

当编码阶段发现原型交互/视觉/状态问题，通过 AskUserQuestion 决策流程回退到此阶段：

```
code 阶段 → 发现原型问题 → AskUserQuestion → 确认回退 → prototype-design REVISION 模式

1. 编码 Agent 记录问题到 skill-suggestion.md（原型页面路径 + 问题描述 + 建议修订方向）
2. prototype-design 加载已有原型改动记录 + 编码阶段记录的问题
3. 修订 → BUILD → 验证（随审查方式）→ 用户确认
4. 完成后回到 design 继续后续流程（plan → code）
5. 修订范围仅限于原型问题，不扩展到功能设计领域
```

### 修订模式后验证

修订模式 DESIGN 步骤完成后：

1. SHALL 执行 BUILD 步骤的四项静态门控检查（7.1 CDN 扫描、7.2 交叉引用、7.3 必检产物存在、7.4 清单与磁盘一致）
2. 该变更选择「子代理自动审查验证」审查方式时，SHALL 继续执行 VERIFY（步骤 9 单轮合并验证）与 SELFREV（步骤 10 单轮验证）
3. 该变更选择「人工审查」审查方式时，SHALL 跳过 VERIFY 与 SELFREV，直接进入 REVIEW
4. BUILD 门控不通过或验证不通过 → 返回 DESIGN 重新修订
5. 全部检查通过 → 进入 REVIEW 用户评审循环

---

## 阶段边界约束

### 域内内容（prototype 负责）

| 内容类别 | 说明 |
|---------|------|
| UI 原型页面 | 基于 functional-designs/ 的页面定义生成多文件 HTML 原型，直写产品级 `docs/designs/prototypes/`（`index.html` 为全产品入口，屏幕在 `screens/`） |
| 交互流程 | 基于功能设计中的可执行操作和业务流程设计交互，使用 flow demo 模式（完整可交互路径，单台设备状态管理器驱动） |
| 视觉风格 | 统一的视觉风格、组件命名、页面布局模式 |
| 交互状态 | 加载态、空态、错误态、边界态等完整状态覆盖 |
| 表单组件 | 基于功能设计中的表单项定义（字段名/类型/校验规则/默认值/placeholder）生成对应表单组件 |
| 菜单结构 | 基于功能设计中的导航定义生成菜单树（一/二/三级菜单 + 对应页面） |
| 离线自包含 | 所有 CSS/JS/字体/图片内联或相对路径引用，禁止 `http://` `https://` 外部 CDN 依赖，字体使用系统默认字体栈 |
| 改动追踪 | 维护变更级 `prototype-changes.md`（改动清单 + 改动前哈希）与 `prototype-backup/`（改动前快照），支持并发检测与回滚 |

### 域外内容（禁止）

| 内容类别 | 说明 | 应由哪个阶段处理 |
|---------|------|----------------|
| 功能决策 | 新增/删除/修改功能点定义 | explore（回退） |
| 业务规则修改 | 修改功能设计中的业务规则 | explore（回退） |
| 技术实现决策 | 技术架构、接口设计、数据模型 | design |
| 代码实现 | 任何代码文件 | code |

### 产品级原型目录的写权限

产品级 `docs/designs/prototypes/` 目录的写权限 SHALL 仅归属于原型设计阶段；变更级 `prototype-changes.md` 与 `prototype-backup/` 同样 SHALL 仅由原型设计阶段写入。其他阶段对两者只读。

下游阶段（plan、code、code-review、e2e-test、integration-test）发现原型产物问题时：

1. SHALL 通过回退机制触发原型设计阶段的修订流程（REVISION 模式）
2. SHALL NOT 直接修改 `docs/designs/prototypes/` 目录下的任何文件（含 `manifest.md`、`index.html`、HTML 文件、CSS 文件等）
3. SHALL NOT 直接修改变更级 `prototype-changes.md` 与 `prototype-backup/`
4. 回退修订完成后由原型设计阶段负责更新产品级 `manifest.md` 与变更级 `prototype-changes.md`

### 越界处理

当 prototype 阶段发现功能设计不完整或定义不清晰时：
1. 记录到 `docs/skill-suggestion.md`
2. 在当前能力范围内完成原型（标注已知局限）
3. 提示用户是否需要回退 explore 阶段补充
4. **禁止**自行修改 functional-designs/ 内容

---

# 与其他 Skill 的关系

```
kflow-explore（设计探索）
  └── 输出 functional-designs/
        └── kflow-prototype-design（本阶段，可选）
              ├── OPTIMIZE 产出 prototype-plan/design-prompt.md（7 章节）
              ├── DESIGN: Agent(subagent) 子代理 → 按有效工具链 execution_order 执行设计引擎
              └── 输出产品级 docs/designs/prototypes/ + 变更级 prototype-changes.md
                    └── kflow-design（详细设计）

归档时: kflow-archive 将本变更的原型改动登记到 docs/designs/prototypes/manifest.md
```

- **输入来自**：`kflow-explore`（设计探索阶段）
- **输出给**：`kflow-design`（详细设计阶段）
- **前置阶段**：设计探索（必须完成）
- **后续阶段**：详细设计（原型设计完成后或跳过后）
- **委托执行**：按有效工具链锁定的设计引擎（huashu-design / frontend-design / 其他）执行，需重新选择且不可用时阻塞
- **归档登记**：`kflow-archive` 将本变更的原型改动登记到 `docs/designs/prototypes/manifest.md`（原型已直写产品级，归档不再执行文件级合并）

---

# 核心提醒

- **编排层非执行层**：本 Skill 不做具体原型制作，所有原型生成通过子代理委托给设计引擎
- **子代理委托调用**：DESIGN 步骤通过 `Agent(subagent_type="claude")` 子代理调用设计引擎，子代理独立上下文，HTML 产物不污染主 Agent
- **工具链默认复用**：TOOLCHAIN 步骤默认复用 `docs/toolchain.md` 已锁定工具链，不扫描、不询问；仅在无锁定 / Skill 失效 / 用户显式要求更换时重新选择
- **design-prompt.md 唯一真相源**：OPTIMIZE 完成后输出 `prototype-plan/design-prompt.md`（7 章节），经用户确认后作为 DESIGN 步骤唯一输入
- **OPTIMIZE 必须经用户确认**：提示词优化后 SHALL 通过 AskUserQuestion 展示给用户确认，确认通过后方进入 DESIGN
- **页面元素穷举**：OPTIMIZE 步骤必须穷举每个页面的菜单、按钮、表单（含字段/类型/校验/默认值）、数据展示区、状态覆盖、弹窗/抽屉，不得遗漏
- **业务流程驱动**：默认使用 flow demo 模式（可交互流程，单台设备状态管理器驱动），禁止 overview 静态平铺
- **直写产品级原型目录**：原型产物写入 `docs/designs/prototypes/`（变更级 SHALL NOT 创建原型副本目录）；屏幕在 `screens/`，共享组件在 `components/`，静态资源在 `assets/`
- **改动追踪与并发检测**：写入前将改动前副本备份到 `prototype-backup/`，并登记到 `prototype-changes.md`（含改动前哈希）；写入前比对哈希，不一致时交用户裁决（基于新版本改 / 覆盖 / 人工合并）
- **离线自包含硬约束**：禁止 CDN 外部依赖（`http://` `https://`），所有资源内联或相对路径，字体使用系统字体栈
- **BUILD 是唯一必做验证**：四项纯静态检查（CDN 扫描/交叉引用/必检产物/清单一致）由主 Agent 直接执行，零子代理；不通过则修复重跑全部四项，不得进入后续步骤
- **审查方式由用户选择**：BUILD 通过后 AskUserQuestion 二选一——「人工审查」跳过全部自动验证直接进入 REVIEW；「子代理自动审查验证」执行 VERIFY（单轮合并验证：一轮子代理、一份报告，含导航合理性/Playwright 全覆盖/UX 规则审查/对比度检测四分区）与 SELFREV（签署清单 + 单轮验证）
- **条件说明**：VERIFY 单轮合并验证与 SELFREV 单轮验证均仅在「子代理自动审查验证」路径生效；「人工审查」路径下二者完全跳过，不保留兜底轮次，系统 SHALL NOT 执行 SELFREV 与 VERIFY，直接进入用户评审 REVIEW
- **prototype-gen 角色不可用是硬阻塞**：仅在需重新选择工具链时判定，标记 ⚠️ 阻塞，提示安装命令：`huashu-design` 或 `frontend-design`
- **自审（签署清单 + 单轮验证）**：仅「子代理自动审查验证」路径执行；固定单轮、SHALL NOT 执行第二轮、SHALL NOT 存在 0 轮豁免路径（读取变更级 `.status.md` 的「变更档位」字段仅用于确定报告形态与产出深度，缺失或历史取值 完整 按 标准 档）。三环节：主 Agent 签署自证（零子代理，`维度 / 自证结论 / 证据锚点` 三列，锚点 SHALL 指向产物内具体位置）→ 1 个独立子代理单轮验证（先独立遍历产物形成自身 4 维度结论且不读签署清单，再逐项对照签署清单打假，只报告不修改产物）→ 主 Agent 统一修复并生成「本阶段修复清单」，不追加确认轮。审查对象集合由主 Agent 冻结、维度集合封闭为覆盖性/一致性/可用性/完整性四维（覆盖性为第一优先级），范围外发现降级为「范围外观察」；引入范围外新内容的验证 SHALL 被拒收。验证报告 SHALL NOT 输出各维度 0–10 评分与不达标项清单（该评分要求已随第三档取值一并废除）。终止结果取值 `验证通过` / `验证发现问题({N})`
- **用户评审是循环**：通过 AskUserQuestion 确认，需要修订时回到 DESIGN 步骤重新启动子代理委托
- **Playwright 不可用时降级**：优先执行 `.kflow-runtime/playwright/` 隔离安装引导，安装失败后改为手动文件分析并在报告「Playwright 全覆盖」分区记录降级原因
- **禁止自行修改上游产物**：不得修改 functional-designs/ 中的内容；也不得直接修改产品级 `docs/designs/prototypes/`（UI 问题须经 REVISION 模式）

---

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
