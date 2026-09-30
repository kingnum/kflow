# kflow-prototype-design（原型设计阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 原型设计（可选阶段）
> **破坏性变更**: v3.0.0 → v4.0.0 原型阶段重构——TOOLCHAIN 由"每次扫描+询问"改为**默认复用已锁定工具链**；新增 **BUILD 构建门控**（四项静态检查，零子代理，唯一必做验证）与**审查方式二选一**（人工审查 / 子代理自动审查验证）；原型产物由"变更级副本 + 归档合并"改为**直写产品级 `docs/designs/prototypes/`**，变更级只留 `prototype-changes.md`（含改动前哈希）+ `prototype-backup/`；VERIFY 与 SELFREV 由"无条件强制"改为**随审查方式条件触发**

---

## 基本信息

```yaml
name: kflow-prototype-design
description: 原型设计阶段 - 编排层，默认复用 docs/toolchain.md 已锁定的设计工具链，委托生成 HTML 原型并直写产品级 docs/designs/prototypes/。BUILD 四项静态门控必做，通过后由用户选择人工审查或子代理自动审查验证。可选阶段，仅涉及前端/UI 变更时推荐使用。
license: MIT
triggers:
  - 原型设计
  - UI 设计
  - 交互设计
  - HTML 原型
allowed-tools:
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
  - Agent
```

---

## 架构模型：编排层 → 工具链复用 → 子代理执行引擎 → 构建门控 → 审查方式分流

`kflow-prototype-design` 作为编排层，默认复用已锁定的设计工具链，委托子代理生成原型并直写产品级原型目录，随后以静态门控保证产物完整性，最后由用户选择审查深度：

```
kflow-prototype-design (编排层)
├── 阶段门控 + 状态管理 + 用户评审
├── 产品级上下文加载（docs/designs/prototypes/）
├── TOOLCHAIN: 复用判定 → 复用 docs/toolchain.md 已锁定工具链（不询问）
│                └── 例外：无锁定 / Skill 失效 / 用户要求更换 → SCAN → 方案推荐 → AskUserQuestion → 锁定
├── prompt 上下文组装（INPUT：机械提取）
├── prompt 优化（OPTIMIZE：设计转译 + prototype-plan/design-prompt.md 输出 + 用户确认）
├── Agent(subagent) 子代理 → 按有效工具链锁定执行，直写 docs/designs/prototypes/
│   ├── 7.1 STYLE: 子代理推荐 3 个差异化风格方向 → 用户选择 → prototype-plan/style-decision.md
│   └── 7.2 GENERATE: 按 execution_order 调用设计引擎
│       ├── 直写 screens/ + components/ + assets/ + index.html + design-tokens.css + design-system/MASTER.md
│       ├── 改动前副本 → prototype-backup/
│       └── 改动登记 → prototype-changes.md
├── 8. BUILD（唯一必做验证，零子代理）: CDN 扫描 + 交叉引用 + 必检产物存在 + 清单与磁盘一致
├── 9. 审查方式选择（AskUserQuestion 二选一）
│   ├── 人工审查            → 跳过全部自动验证，直接进入 REVIEW
│   └── 子代理自动审查验证  → 10. VERIFY（导航 5 轮 + Playwright 5 轮 + UX 5 轮 + 对比度）+ 11. SELFREV
└── 12. 用户评审循环
```

**设计决策**：

- **工具链复用优先**：`docs/toolchain.md` 是项目级、跨变更稳定的配置（由 `kflow-init` 产出）。每次变更重新扫描环境并询问，等于把工具链当作变更级属性，与配置层级不符。仅在配置缺失、配置失效或用户显式要求更换时才重新选择。
- **原型唯一真相源**：产品级 `docs/designs/prototypes/` 是所有变更共用的原型目录，变更**直写**该目录，不维护副本。变更级以 `prototype-changes.md`（改动清单 + 改动前哈希）与 `prototype-backup/`（改动前快照）提供隔离、审计与回滚能力。
- **必做验证与可选验证分离**：BUILD 是四项纯静态检查，秒级完成、零外部依赖，覆盖"产物不可用"的主要故障模式，构成唯一必做验证。重验证（导航/Playwright/UX/对比度/自审）的价值取决于变更规模与用户对原型的信心，由用户显式选择。

**有效工具链解析顺序**：`docs/changes/{change}/toolchain.md` 的原型设计章节 → 不存在时取 `docs/toolchain.md` 的原型设计章节。

**角色分类**（仅在需要重新选择时使用）：
- `prototype-gen`: 能生成 HTML 交互原型（如 huashu-design、frontend-design）
- `design-system`: 能输出色板/字体/风格决策（如 ui-ux-pro-max）
- `ux-review`: 能做 UX 规则审查（如 ui-ux-pro-max、huashu-design）
- `code-gen`: 能生成生产级前端代码（如 frontend-design）

---

## 门控检查

> **机制说明**：门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则)

进入原型设计阶段前检查：

- .status.md 存在
- 设计探索状态 = ✅ 完成
- functional-designs/index.md 存在
- 存在前端/UI 相关功能点

若无前端变更，自动跳过此阶段，状态标记为 ⏭️ 跳过。

> **变更说明**：`prototype-gen` 角色可用性**不再**作为进入阶段的硬拦截项。复用路径下无需扫描环境，工具链已在 `docs/toolchain.md` 锁定；仅在复用判定结论为"需要重新选择"时才扫描并判定该角色可用性（见 §6）。

---

## 输入要求

| 输入 | 图例 | 说明 |
|------|------|------|
| functional-designs/ | ✅ 必须 | 设计探索阶段输出，提取项目背景和 UI 功能点清单 |
| docs/toolchain.md | 🔶 条件 | 项目级工具链配置，原型设计章节存在且已锁定时直接复用 |
| docs/changes/{change}/toolchain.md | 🔶 条件 | 变更级工具链覆盖（用户显式要求更换时写入），存在时优先于项目级 |
| docs/designs/prototypes/manifest.md | 🔶 条件 | 全产品原型清单，存在时用于加载已有原型上下文 |
| docs/designs/prototypes/design-tokens.css | 🔶 条件 | 已有设计令牌，存在时纳入设计约束 |
| docs/designs/prototypes/screens/ | 🔶 条件 | 已有屏幕清单，存在时作为新屏幕的导航锚点 |
| docs/designs/prototypes/components/ | 🔶 条件 | 已有共享组件清单，存在时纳入设计约束 |
| docs/designs/prototypes/design-system/MASTER.md | 🔶 条件 | 已有设计系统，存在时纳入设计约束 |
| docs/designs/prototypes/index.html | 🔶 条件 | 产品级全貌原型，新屏幕需能挂入其导航 |
| docs/changes/{change}/prototype-changes.md | 🔶 条件 | 本变更已有原型改动记录，修订模式判定与并发检测依据 |
| brand-spec.md | 🔶 条件 | 品牌资产，涉及品牌时纳入 prompt |

---

## 输出产物

### 产品级产物（`docs/designs/prototypes/`）

| 产物 | 文件 | 模板 | 内容要求 |
|------|------|------|---------|
| 全产品导航入口 | `docs/designs/prototypes/index.html` | N/A | 卡片网格按功能模块分组，挂载全部屏幕入口 |
| 产品级原型清单 | `docs/designs/prototypes/manifest.md` | [manifest.md](../../templates/design-templates/prototypes/manifest.md) | 六段落：产物组织方式、原型文件清单（含角色与来源变更）、页面清单、设计系统引用、共享资源清单、修订记录。下游阶段获取全产品原型文件列表的入口。 |
| 屏幕页面 | `docs/designs/prototypes/screens/*.html` | N/A（按工具链锁定生成） | 多文件 HTML 交互原型，所有文件离线自包含 |
| 共享组件与资源 | `docs/designs/prototypes/components/`、`assets/` | N/A | 共享组件脚本、共享样式、静态资源 |
| 设计令牌 | `docs/designs/prototypes/design-tokens.css` | N/A | CSS 变量声明（色板/字号/间距/圆角/阴影）。设计引擎产出，COMPLETE 步骤从原型 HTML 复核提取并更新。 |
| 设计系统 | `docs/designs/prototypes/design-system/MASTER.md` | N/A（设计引擎输出） | 通用必备产物：色彩方案、字体系统、间距规格、组件规范、交互规则。无论选定哪个工具链都必须输出 |

### 变更级产物（`docs/changes/{change}/`）

| 产物 | 文件 | 模板 | 内容要求 |
|------|------|------|---------|
| 工具链选择记录（项目级） | `docs/toolchain.md` | N/A（TOOLCHAIN 步骤输出） | 原型设计阶段锁定的工具链方案，含 skills_used、execution_order、decision_time、status |
| 工具链覆盖记录 | `docs/changes/{change}/toolchain.md` | N/A（TOOLCHAIN 步骤输出） | 仅用户显式要求更换工具链时写入，承载"本变更想换工具链"的场景 |
| 原型改动清单 | `prototype-changes.md` | [prototype-changes.md](../../templates/changes/{change}/prototype-changes.md) | 改动表（`\| 文件路径 \| 类型 \| 改动前哈希 \| 说明 \|`）、改动前快照说明、并发写入裁决记录、回滚记录 |
| 原型改动前快照 | `prototype-backup/` | N/A | 按产品级相对路径镜像存放的改动前副本，供回滚使用 |
| 提示词文件 | `prototype-plan/design-prompt.md` | [design-prompt.md](../../templates/changes/{change}/prototype-plan/design-prompt.md) | 7 章节完整提示词文件，DESIGN 步骤的唯一真相源 |
| 风格选择决策 | `prototype-plan/style-decision.md` | [style-decision.md](../../templates/changes/{change}/prototype-plan/style-decision.md) | 用户选定的风格方向：风格名称、设计哲学、色彩方案、字体系统、布局模式、ASCII 线框图 |
| 元素覆盖树 | `element-coverage-tree.md` | [element-coverage-tree.md](../../templates/changes/{change}/element-coverage-tree.md) | 四层树状结构（📄页面→🏗️区域→🔘元素→🎯状态+操作链），TC-ID 列初始为空，待 design 阶段填充 |
| BUILD 报告 | `self-reviews/prototype/cdn-crossref-check/report.md` | N/A | CDN 扫描 + 交叉引用 + 必检产物 + 清单一致 四项检查综合报告（两种审查方式下均产出） |
| 导航验证报告 | `self-reviews/prototype/nav-check/round-{1..5}.md` | N/A | 5 轮导航合理性验证报告（仅子代理自动审查验证路径） |
| Playwright 验证报告 | `self-reviews/prototype/playwright-check/round-{1..5}.md` | N/A | 5 轮 Playwright 全覆盖验证报告或降级说明（仅子代理自动审查验证路径） |
| UX 规则审查报告 | `self-reviews/prototype/ux-check/round-{1..5}.md` | N/A | 5 轮 UX 规则审查报告（内置 20-30 条精简核心规则）（仅子代理自动审查验证路径） |
| 对比度检测报告 | `self-reviews/prototype/contrast-check/report.md` | N/A | WCAG 相对亮度计算结果，标记 <4.5:1 的颜色对（仅子代理自动审查验证路径） |
| 自审报告 | `self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md` | [review-round.md](../../templates/changes/{change}/self-reviews/review-round.md) | 按变更档位目标轮次产出（轻量档 0 轮不产出；仅子代理自动审查验证路径） |
| 用户评审记录 | `.status.md` | N/A | 原型设计评审状态、审查方式选择结果、时间、备注 |

**产物位置**：产品级产物写入 `docs/designs/prototypes/`；变更级工作记录写入 `docs/changes/{change}/`。变更级 **SHALL NOT** 创建 `index.html`、`screens/`、`components/`、`design-tokens.css` 等原型产物。

**产物形式**：多文件架构，`docs/designs/prototypes/index.html` 为全产品入口，`screens/` 存放独立页面文件，`components/`、`assets/` 存放共享资源。产品级 `manifest.md` 按角色（entry/page/tokens/shared/process）标注各产物文件路径。

**离线自包含**：所有 HTML/CSS/JS/字体/图片必须内联或相对路径引用，禁止 CDN 外部依赖。

---

## 执行流程

```
原型设计阶段流程:

┌──────────────────────────────────────────────────────────────────┐
│                     PROTOTYPE WORKFLOW (v4.0)                     │
├──────────────────────────────────────────────────────────────────┤
│  1. CHECK     → 门控检查                                              │
│             → 修订模式检测（prototype-changes.md 是否存在）           │
│  1.5 PRE_HOOK → 引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                               │
│  │   └── RELOAD → 重读 CONTEXT.md, toolchain.md, functional-designs/, │
│  │              docs/designs/prototypes/manifest.md(条件),            │
│  │              prototype-changes.md(条件), .status.md                │
│  2. ASSESS    → 评估是否需要原型设计（新建模式）+ AskUserQuestion     │
│  3. TOOLCHAIN → 复用判定（默认复用，不询问）                          │
│  │   ├── 已锁定且 Skill 可用 → 复用，SHALL NOT 扫描环境              │
│  │   └── 例外（无锁定 / Skill 失效 / 用户要求更换）→ SCAN + 选择      │
│  4. INPUT     → 机械组装 prompt 上下文（数据收集层）                  │
│  │   ├── 必然存在: functional-designs/ 提取背景+UI功能点              │
│  │   ├── 条件存在: docs/designs/prototypes/ 产品级已有原型            │
│  │   └── 条件存在: brand-spec.md 品牌资产                            │
│  5. OPTIMIZE  → 深度分析设计，产出优化后 prompt + 文件输出            │
│  │   ├── 提取菜单树（一/二/三级 → 对应页面）                          │
│  │   ├── 穷举页面元素（按钮/表单/数据区/弹窗/状态）                    │
│  │   ├── 编写业务流程脚本（逐步用户操作路径）                          │
│  │   ├── 注入硬约束（直写产品级+flow demo+离线自包含）                │
│  │   ├── 注入 design-system/MASTER.md 与 design-tokens.css 输出要求   │
│  │   ├── 输出 prototype-plan/design-prompt.md（7 章节完整模板）       │
│  │   └── AskUserQuestion 用户确认（确认执行/需修订）                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ 修订模式分支 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  R. REVISION  → 修订模式（跳过 INPUT+OPTIMIZE+TOOLCHAIN）             │
│  │   ├── 加载 prototype-changes.md 作为本变更改动记录上下文           │
│  │   ├── 加载 prototype-plan/design-prompt.md 作为已有设计约束        │
│  │   ├── 加载有效工具链作为已有锁定                                   │
│  │   ├── AskUserQuestion 确认修订需求或展示已有原型                   │
│  │   └── 合并修订需求到 prompt → 进入 DESIGN                          │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  6. DESIGN    → 按有效工具链锁定执行                                  │
│  │   ├── 6.0 并发写入检测（哈希比对 → 冲突则 AskUserQuestion 裁决）   │
│  │   ├── 6.1 STYLE: 子代理推荐 3 个差异化风格方向                     │
│  │   │   └── AskUserQuestion 选择 → prototype-plan/style-decision.md  │
│  │   └── 6.2 GENERATE: Agent(subagent) 按工具链执行                   │
│  │       ├── prompt = design-prompt.md + style-decision.md            │
│  │       ├── 直写 docs/designs/prototypes/（screens/components/assets/│
│  │       │   index.html/design-tokens.css/design-system/MASTER.md）   │
│  │       ├── 改动前副本 → prototype-backup/                           │
│  │       └── 改动登记 → prototype-changes.md                          │
│  7. BUILD     → 四项静态检查（唯一必做验证，零子代理）                │
│  │   ├── 7.1 CDN 外部依赖扫描                                        │
│  │   ├── 7.2 交叉引用完整性检查                                      │
│  │   ├── 7.3 必检产物存在性检查                                      │
│  │   └── 7.4 清单与磁盘一致性检查                                    │
│  │   → 不通过则修复重跑全部四项，SHALL NOT 进入后续步骤               │
│  8. 审查方式选择 → AskUserQuestion 二选一（BUILD 通过后）             │
│  ─ ─ ─ ─ ─ ─ ─ ─ 「子代理自动审查验证」路径 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  9. VERIFY    → 9.1 导航验证(5轮) → 9.2 Playwright(5轮)               │
│  │              → 9.3 UX 规则审查(5轮) → 9.4 对比度检测               │
│  10. SELFREV  → 按变更档位自审（重复制：每轮全 4 维度）               │
│  ─ ─ ─ ─ ─ ─ ─ ─ 「人工审查」路径：8 之后直接进入 11 ─ ─ ─ ─ ─ ─    │
│  11. REVIEW   → AskUserQuestion 用户评审                              │
│  │   ├── 确认通过 → COMPLETE                                          │
│  │   └── 需修订   → 收集反馈 → 回到 DESIGN                            │
│  12. COMPLETE → 更新状态文件 + 同步 manifest.md + 提取设计令牌与覆盖树│
│  13. POST_HOOK → 引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 POST_HOOK │
│  │   ├── BROWSER_CLEANUP → playwright-cli kill-all 清理浏览器进程     │
│  │   └── UPDATE_STATE → 更新 .status.md                               │
└──────────────────────────────────────────────────────────────────┘
```

> **注**：§7 BUILD 与 §9 VERIFY 内部编号以 BUILD 的 `7.1–7.4` 与 VERIFY 的 `9.1–9.4` 为准。

---

## 1. CHECK — 门控检查

```
1. Read docs/changes/{change}/.status.md
2. Check: design exploration status = ✅ 完成
3. Check: functional-designs/index.md exists
4. Extract: project type from .status.md
5. If project type = pure backend → auto-skip (update status to ⏭️ 跳过, exit)
6. Scan functional-designs/ for UI-related feature points
7. If no UI FPs found → auto-skip (update status to ⏭️ 跳过, exit)
8. 修订模式检测:
   - Check if 变更级 prototype-changes.md already exists and is non-empty
   - If exists → 标记为修订模式候选，进入 §R 修订模式 分支
   - If not exists → 走新建模式，继续 ASSESS → TOOLCHAIN → INPUT → OPTIMIZE → DESIGN
```

> **变更说明**：修订模式检测对象由变更级 `prototype/index.html` 改为变更级 `prototype-changes.md`（是否存在且非空）。直写模型下，变更级不再持有原型副本，`prototype-changes.md` 是本变更"是否已做过原型工作"的唯一可靠信号。

## 2. ASSESS — 评估是否需要原型设计

Determine whether a prototype adds value:

**推荐创建原型**：
- 新增 UI 页面或显著修改现有页面
- 用户交互流程复杂（多步表单、向导、仪表板）
- 视觉设计决策需要干系人对齐
- 开发人员需要视觉参考以进行实现

**可跳过**：
- 纯后端变更（自动跳过）
- 纯数据/API 变更，无 UI 影响（自动跳过）
- UI 变更极其微小（单个按钮、文字或颜色变更）
- 用户明确拒绝

通过 AskUserQuestion 确认：
```
Question: "此变更有 {n} 个 UI 功能点。是否创建 HTML 原型？"
Options:
  - "确认创建原型" (推荐)
  - "跳过原型设计"
```

## 3. TOOLCHAIN — 工具链复用判定与锁定

TOOLCHAIN 步骤负责解析有效工具链并（在必要时）重新选择。

### 3.1 有效工具链解析顺序

```
1. 读取 docs/changes/{change}/toolchain.md 的原型设计章节
2. 该章节存在 → 以变更级覆盖文件作为有效工具链
   - 系统 SHALL NOT 使用 docs/toolchain.md 中的原型设计章节
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
| 无已锁定工具链 | 变更级与项目级均无原型设计章节，或章节存在但 `status` 未标记为已锁定 | 进入重新选择流程；选定后写入 `docs/toolchain.md` 原型设计章节并标记已锁定。SHALL NOT 标记阶段为 ⚠️ 阻塞 |
| 已锁定但引用的 Skill 不可用 | `skills_used` 中至少一个 Skill 在环境中已不可用 | 输出提示："工具链 X 的 Skill Y 已不可用"；进入重新选择流程；完成后用新方案**覆盖写入**已锁定的工具链章节 |
| 用户显式要求更换 | 用户在 TOOLCHAIN 步骤显式要求更换工具链 | 进入重新选择流程，不受已锁定工具链约束；完成后**覆盖写入**变更级 `docs/changes/{change}/toolchain.md` 的原型设计章节，SHALL NOT 修改 `docs/toolchain.md` |

### 3.4 SCAN — 环境扫描设计 Skills（仅在需重新选择时执行）

```
1. 扫描 .claude/skills/ 目录下所有设计相关 Skills
   - 读取每个 Skill 的 SKILL.md 的 name + description 字段
   - 识别设计相关（description 包含 design/原型/HTML/UI/ux 等关键词）
2. 按能力角色分类:
   ├── prototype-gen: 能生成 HTML 交互原型（如 huashu-design、frontend-design）
   ├── design-system: 能输出色板/字体/风格决策（如 ui-ux-pro-max）
   ├── ux-review: 能做 UX 规则审查（如 ui-ux-pro-max、huashu-design）
   └── code-gen: 能生成生产级前端代码（如 frontend-design）
3. 输出扫描结果（内部使用）:
   ├── available-skills.json: 每个 Skill 的名称、角色分类、description 摘要
   └── 用于后续方案推荐
```

#### 角色可用性判定

- `prototype-gen` 数量 = 0 → ⚠️ 阻塞，提示："未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
- `prototype-gen` 数量 = 1 → 自动生成单一工具链方案，直接使用该方案进入 DESIGN 步骤，不询问用户
- `prototype-gen` 数量 ≥ 2 → 生成 2-3 条工具链方案，每条标注：包含的 Skills、流程描述、优点、缺点、适用场景，通过 AskUserQuestion 展示供用户选择，方案数量 SHALL NOT 超过 3 个

### 3.5 用户选定后锁定

```
1. 用户在 AskUserQuestion 中选择一种工具链方案后:
   - 默认写入 docs/toolchain.md 的原型设计章节
   - 用户显式要求更换时写入变更级 docs/changes/{change}/toolchain.md 的原型设计章节
   - 记录字段：change_name、selected_toolchain、skills_used、execution_order、decision_time、status
   - DESIGN 步骤严格按有效工具链中指定的 Skill 和顺序执行
   - 系统 SHALL NOT 在执行过程中自行切换工具链
```

### 3.6 方案示例

| 方案 | 包含 Skills | 流程 | 优点 | 缺点 | 适用场景 |
|------|-----------|------|------|------|---------|
| A: 一体化 | huashu-design | 单一引擎完成风格推荐+原型生成 | 内置顾问模式+反 slop+Playwright 验证 | 仅适用于 HTML 原型 | 大多数前端变更（推荐） |
| B: 设计驱动 | ui-ux-pro-max + huashu-design | ui-ux-pro-max 输出 design-system → huashu-design 生成原型 | 更精确的设计系统输出 | 需要两个 Skill 配合 | 对设计系统要求高的场景 |
| C: 静态页面型 | ui-ux-pro-max + frontend-design | ui-ux-pro-max 推荐风格 → frontend-design 生成 HTML | 生产级代码输出 | frontend-design 不做 flow demo | 需要快速出页面的场景 |

### 3.7 严格按 execution_order 逐个调用

- 系统 SHALL 按 `execution_order` 数组顺序逐个调用 `skills_used` 中列出的 Skill
- SHALL NOT 跳过 `execution_order` 中定义的任一 Skill
- SHALL NOT 在 `execution_order` 之外调用任何其他设计 Skill
- SHALL NOT 自行调整调用顺序
- DESIGN 步骤执行过程中某个 Skill 调用失败 → 重试该 Skill 一次；重试仍失败则标记阶段为 ⚠️ 阻塞并提示用户；SHALL NOT 自行切换到未列出的其他 Skill

## 4. INPUT — 组装 Prompt 上下文（机械提取层）

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

## 5. OPTIMIZE — 提示词优化与用户确认（设计转译层）

在委托设计引擎之前，编排层 Agent SHALL 深度分析 functional-designs/ 产出优化后的设计 prompt。

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

对每个页面逐项穷举描述：

| 元素类别 | 必须内容 |
|---------|---------|
| 布局分区 | header区 / sidebar区 / 主内容区 / 操作栏 / 列表区 / 详情面板 / footer |
| 可执行操作 | 操作名 → 触发方式 → 预期结果 → 目标页面或弹窗 |
| 按钮清单 | 按钮名 → 位置 → 样式(主要/次要/文字/危险) → 触发动作 → 前置条件 |
| 表单清单 | 表单名 → 字段列表 → 每字段: 名称/类型(input/select/date等)/是否必填/校验规则/默认值/placeholder → 提交按钮 → 提交后行为 |
| 数据展示区 | 表格列定义 / 卡片字段 / 图表类型及数据字段 |
| 状态覆盖 | 加载态 / 空态 / 错误态 / 边界态（边界情况） |
| 弹窗/抽屉 | 触发条件 → 弹窗内容 → 关闭方式 |

### 5.3 业务流程脚本

必须包含至少一个完整的端到端业务流程脚本：

```
流程脚本格式:
├── 流程名称: 如"用户登录→查看列表→进入详情→编辑→提交"
├── 逐步描述: 每步明确"用户在[哪个页面] → 点击[哪个按钮] → 看到[什么变化] → 进入[哪个页面或弹窗]"
├── 覆盖端到端路径: 从入口到最终结果，包含所有中间步骤
└── 如有多条核心流程，逐条编写
```

### 5.4 硬约束注入

优化后的 prompt MUST 包含以下硬约束：

| 约束 | 内容 |
|------|------|
| 直写产品级原型目录 | 输出到 `docs/designs/prototypes/` 目录（SHALL NOT 在变更级创建原型副本目录）；屏幕页面写入 `screens/`，共享组件写入 `components/`，静态资源写入 `assets/`；同步更新 `index.html` 全产品导航与 `design-tokens.css` |
| 改动记录与备份 | 写入前将受影响文件的改动前副本备份到变更级 `docs/changes/{change}/prototype-backup/`，并将本次改动登记到变更级 `docs/changes/{change}/prototype-changes.md` |
| 业务流程驱动 | 使用 flow demo 模式（可交互业务流程，单台设备状态管理器驱动），禁止 overview 静态页面平铺 |
| 离线自包含 | 所有 CSS/JS/字体/图片内联或相对路径引用，禁止 `http://` `https://` 外部 CDN 依赖，字体使用系统默认字体栈 |
| design-system 输出 | 无论选定哪个工具链，设计引擎 SHALL 输出 `docs/designs/prototypes/design-system/MASTER.md`（含色彩方案、字体系统、间距规格、组件规范、交互规则） |
| design-tokens 输出 | 设计引擎 SHALL 输出 `docs/designs/prototypes/design-tokens.css`（CSS 变量：色板/字号/间距/圆角/阴影），所有屏幕通过 `<link rel="stylesheet">` 引用 |

### 5.5 design-prompt.md 文件输出

OPTIMIZE 步骤完成后，编排层 Agent SHALL 将优化后的完整提示词写入 `prototype-plan/design-prompt.md` 文件（7 章节模板），作为 DESIGN 步骤的**唯一真相源**：

### 文件路径

`docs/changes/{change}/prototype-plan/design-prompt.md`

### 7 章节模板

| 章节 | 标题 | 内容要求 |
|------|------|---------|
| 第一章 | 项目背景与设计目标 | 从 functional-designs/index.md 提取产品概述，明确原型范围、目标用户和设计意图 |
| 第二章 | 设计系统（Design System） | 色彩方案（主色/背景色/文字色/边框色/状态色，含颜色值）、字体系统（系统字体栈 + 标题/正文层级规格）、间距与圆角规格（页面/卡片/组件/按钮） |
| 第三章 | 菜单与导航结构 | 菜单树（一/二/三级菜单项及其对应页面）、导航模式（顶部导航/侧边栏/Tab Bar/面包屑）、全局组件（Header/Footer/用户头像/通知铃铛等）、每个页面标注对应的原型文件名 |
| 第四章 | 页面详细规格 | 逐页穷举：布局分区（ASCII 线框图）、按钮清单（名称/位置/样式/触发/前置条件）、表单清单（表单名/字段详情/提交行为）、数据展示区（类型/字段/交互）、状态覆盖（加载/空/错误/边界态）、弹窗/抽屉（触发/内容/关闭方式） |
| 第五章 | 业务流程脚本 | 至少一个完整端到端业务流程脚本，每步明确"用户在[哪个页面] → 点击[哪个按钮] → 看到[什么变化] → 进入[哪个页面]"，覆盖从入口到最终结果的完整路径 |
| 第六章 | 硬约束 | 直写产品级原型目录约束、改动记录与备份约束、flow demo 模式约束（AppPhone 状态管理器驱动，禁止 overview 静态平铺）、离线自包含约束（禁 CDN，系统字体栈） |
| 第七章 | 高保真要求 | 参考资源索引（产品级原型目录/产品级清单/设计令牌/设计系统/品牌资产路径）、交互细节规格（按钮 hover/active 态、输入框 focus 态、弹窗过渡动画、表格行 hover 态、Tab 切换动画）、响应式要求（桌面端优先/移动端基准，如有） |

### 文件元信息

文件头部 SHALL 包含：变更名称、版本号（1.0.0 起始）、生成时间、状态标记（待确认/已确认/已执行）。

## 5.6 用户确认

```
1. 编排层 Agent 完成 design-prompt.md 写入后 → 通过 AskUserQuestion 展示提示词摘要
   Question: "提示词已优化并写入 prototype-plan/design-prompt.md，包含:
     - {n} 个页面的菜单结构
     - {m} 个页面的元素级描述（按钮/表单/数据区/状态覆盖）
     - {k} 个端到端业务流程脚本
     - 硬约束: 直写产品级原型目录 + flow demo 模式 + 离线自包含 + design-system/design-tokens 输出
     是否确认执行？"
   Options:
     - "确认执行" → design-prompt.md 状态更新为"已确认" → 进入 DESIGN 步骤
     - "需要修订" → 收集用户反馈 → 回到 5.1 修订 prompt
```

## 5.7 纯后端项目

当 CHECK 步骤判定原型设计自动跳过（纯后端项目）时，OPTIMIZE 步骤不执行。

---

## R. REVISION — 修订模式

### R.1 触发条件

修订模式有两种入口：

**入口 A: CHECK 步骤检测到已有原型工作**

CHECK 步骤检测到变更级 `prototype-changes.md` 存在且非空时，进入修订模式分支。修订模式下跳过 INPUT（机械提取）和 OPTIMIZE（设计转译）步骤，直接使用已有约束并合并用户修订需求。

**入口 B: code 阶段驱动回退**

当编码阶段发现原型交互/视觉/状态问题时，通过 AskUserQuestion 决策流程回退到 prototype-design REVISION 模式。此入口的特有处理：

```
code 阶段驱动回退 → prototype-design REVISION 模式:

1. 编码阶段发现原型问题（如按钮交互流程不合理、视觉设计问题、状态覆盖缺失）
2. 记录到 skill-suggestion.md
3. AskUserQuestion 确认决策:
   - "确认回退到原型设计" → 进入 R.3 修订模式流程，附编码阶段发现的具体问题
   - "暂缓此功能点（标记 ⏸️）" → 在 code 阶段暂缓该 FP
   - "记录为已知问题继续" → 记录不阻止编码继续
4. 进入 REVISION 模式:
   ├── 加载 prototype-changes.md 作为本变更改动记录上下文
   ├── 加载编码阶段发现的具体问题作为修订需求
   ├── 修订 → 验证 → 用户确认
   └── 完成后回到 design 继续后续流程（plan → code）
```

**两种入口对比**：

| 维度 | 入口 A: 用户驱动 | 入口 B: code 阶段驱动 |
|------|-----------------|---------------------|
| 触发者 | 用户在 REVIEW 中选择「需修订」 | 编码 Agent 发现原型问题 |
| 修订需求来源 | 用户口述反馈 | 编码阶段发现的具体技术问题 |
| 决策流程 | 直接进入修订 | AskUserQuestion 确认后进入 |
| 回退影响 | 仅 prototype-design 阶段 | prototype → design → plan → code 连锁回退 |
| 后续流程 | 修订 → 验证 → 用户评审 | 修订 → 验证 → 用户确认 → design → plan → code |

### R.2 修订模式 AskUserQuestion

本变更已做过原型工作但用户无明确修订需求时，通过 AskUserQuestion 询问：

```
Question: "本变更已做过原型工作（prototype-changes.md 已存在）。是否要调整？"
Options:
  - "要调整，描述修改内容" → 进入 R.3 修订模式流程
  - "查看现有原型" → 展示原型摘要，不修改，退出原型设计阶段
```

当用户输入包含修订需求（如"调整原型"、"修改设计"、"改大按钮"等）时，直接进入 R.3 修订模式流程。

### R.3 修订模式流程

```
1. 加载产品级 docs/designs/prototypes/manifest.md 与 screens/ 清单作为现有原型上下文
2. 加载变更级 prototype-plan/design-prompt.md 作为已有设计约束
3. 加载变更级 prototype-changes.md 获取已有改动清单与改动前哈希
4. 加载有效工具链（docs/changes/{change}/toolchain.md 优先，其次 docs/toolchain.md）作为已有锁定
5. 合并用户修订需求到 prompt 中
6. 进入 DESIGN 步骤，按有效工具链执行
```

修订模式下不重新从 functional-designs/ 提取（跳过 INPUT），不重新生成 design-prompt.md（跳过 OPTIMIZE），不重新执行工具链选择（跳过 TOOLCHAIN）。如 design-prompt.md 不存在，基于现有原型反向生成最小约束文件。如有效工具链未锁定，执行一次最小化 TOOLCHAIN 选择。

### R.4 修订模式后验证

修订模式 DESIGN 步骤完成后：

1. 系统 SHALL 执行 BUILD 步骤的四项静态门控检查（7.1 CDN 扫描、7.2 交叉引用、7.3 必检产物存在、7.4 清单与磁盘一致）
2. 该变更选择「子代理自动审查验证」审查方式时，SHALL 继续执行 VERIFY（9.1 导航验证 → 9.2 Playwright 验证 → 9.3 UX 规则审查 → 9.4 对比度检测）与 SELFREV
3. 该变更选择「人工审查」审查方式时，SHALL 跳过 VERIFY 与 SELFREV，直接进入 REVIEW 用户评审循环
4. BUILD 门控不通过或验证不通过 → 返回 DESIGN 重新修订
5. 全部检查通过 → 进入 REVIEW 用户评审循环

### R.5 修订模式后元素覆盖树重新生成

修订模式 REVIEW 确认通过后，§12.2 自动触发 `element-coverage-tree.md` 的重新提取（使用更新后的产品级屏幕文件），覆盖旧版本树文件。该逻辑与新建模式一致，无需修订模式特殊处理。

---

## 6. DESIGN — 按有效工具链锁定执行

DESIGN 步骤分为 6.0 并发写入检测、6.1 STYLE（风格/布局推荐）与 6.2 GENERATE（按工具链锁定执行）。

### 6.0 并发写入检测（主 Agent 执行）

产品级原型目录是多变更共享的写入热点，主 Agent SHALL 在启动 GENERATE 子代理前完成并发写入检测：

```
1. 读取变更级 prototype-changes.md 的改动清单
2. 对每条"修改"或"删除"条目，计算产品级 docs/designs/prototypes/ 下对应文件的当前哈希
3. 与条目记录的"改动前哈希"比对
   ├── 一致 → 正常写入，该条目的改动前哈希在本轮写入后更新为本次写入前的版本哈希
   └── 不一致 → 提示"该文件已被其他变更修改"，通过 AskUserQuestion 交用户裁决
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
3. 启动子代理执行风格/布局推荐:
   Agent(subagent_type="claude", description="执行风格推荐", prompt="读取 prototype-plan/design-prompt.md 中的项目背景、产品类型、目标用户，推荐 3 个差异化风格方向。每个方向包含：风格名称+设计哲学描述、色彩方案（主色/背景色/文字色/强调色+色值）、字体系统（标题+正文）、布局模式、ASCII 线框图（10 行以内）、适用场景+不适用场景。")
   - 如 docs/designs/prototypes/manifest.md 存在，同时读取以了解已有设计系统与屏幕结构
4. 通过 AskUserQuestion 展示风格选项:
   - 选项 1/2/3: 3 个差异化风格方向（preview 含 ASCII 线框图 + 色彩方案）
   - "需要更多方向": 回到推荐步骤重新生成
   - "自行指定": 用户自由描述期望风格
5. 用户选定后写入 prototype-plan/style-decision.md:
   - selected_style: 风格名称
   - style_description: 设计哲学 + 色彩 + 字体 + 布局
   - ascii_wireframe: ASCII 线框图
   - decision_time: 时间戳
6. style-decision.md 作为 6.2 GENERATE 步骤的输入
```

### 6.2 GENERATE — 按工具链锁定执行

```
1. 确认 prototype-plan/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype-plan/style-decision.md 存在（STYLE 步骤产出）
3. 确认有效工具链已锁定（docs/changes/{change}/toolchain.md 或 docs/toolchain.md）
4. 启动子代理:
   Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype-plan/design-prompt.md + prototype-plan/style-decision.md 中的完整提示词，按有效工具链中 execution_order 指定的设计引擎和顺序生成 HTML 交互原型。产物直接写入产品级 docs/designs/prototypes/：屏幕写入 screens/，共享组件写入 components/，静态资源写入 assets/，同步更新 index.html 全产品导航与 design-tokens.css，并输出 design-system/MASTER.md。写入前将受影响文件的改动前副本备份到 docs/changes/{change}/prototype-backup/，并将本次改动登记到 docs/changes/{change}/prototype-changes.md。")
   - 子代理严格按 execution_order 逐个调用设计引擎
   - 子代理 SHALL NOT 调用 execution_order 之外的设计 Skill
   - 子代理 SHALL NOT 在 docs/changes/{change}/ 下创建原型副本目录
   - 子代理独立上下文，HTML 产物不污染主 Agent
5. 子代理写入规则:
   ├── 屏幕页面 → docs/designs/prototypes/screens/
   ├── 共享组件 → docs/designs/prototypes/components/
   ├── 静态资源 → docs/designs/prototypes/assets/
   ├── 更新 docs/designs/prototypes/index.html（全产品导航）
   ├── 更新 docs/designs/prototypes/design-tokens.css
   ├── 输出 docs/designs/prototypes/design-system/MASTER.md
   ├── 改动前副本 → docs/changes/{change}/prototype-backup/（按产品级相对路径镜像；新增文件不生成快照）
   └── 改动登记 → docs/changes/{change}/prototype-changes.md（| 文件路径 | 类型 | 改动前哈希 | 说明 |）
6. 子代理完成后返回结果摘要（成功/失败、生成页面数、改动文件数）
7. 主 Agent 验证产物:
   - 验证 docs/designs/prototypes/index.html 存在且非空
   - 验证 docs/designs/prototypes/design-system/MASTER.md 存在
   - 验证变更级 prototype-changes.md 已生成，且登记的改动条目覆盖产品级原型目录本次实际变更
   - 验证所有内部文件引用目标文件存在
8. 子代理失败处理:
   - 重试一次子代理调用
   - 重试仍失败 → ⚠️ 阻塞，提示用户
   - SHALL NOT 自行切换到 execution_order 中未列出的其他 Skill
```

**强制要求**：flow demo 模式——设计引擎 SHALL 使用单台设备状态管理器（如 `AppPhone`），用户可通过点击 tab bar / 按钮 / 标注点完成完整业务流程。SHALL NOT 仅提供多屏并排静态展示（overview 平铺）。

`kflow-prototype-design` 不干预设计引擎内部迭代过程。

---

## 7. BUILD — 构建门控（唯一必做验证，零子代理）

BUILD 步骤在原型产物生成（DESIGN）之后、审查方式选择之前执行，依次执行四项纯静态检查。此处的"构建"指静态一致性检查，原型为纯 HTML 产物，SHALL NOT 引入编译或打包步骤。

### 执行顺序与约束

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
2. Grep 检索 https?:// 模式的外部资源引用
   - <link href="http..."> → 违规
   - <script src="http..."> → 违规
   - <img src="http..."> → 违规
   - @import url(http...) → 违规
3. 若发现外部依赖:
   - 在 BUILD 报告中列出违规文件和具体引用
   - 判定不通过 → 返回 DESIGN 步骤修复
4. 若 CDN 扫描通过 → 记录"离线自包含检查通过"
```

### 7.2 多文件交叉引用完整性检查

```
1. 提取 docs/designs/prototypes/ 下所有文件中指向本目录的内部引用目标
   （<a href="...">、<iframe src="..."> 等）
2. 验证每个引用目标文件在 docs/designs/prototypes/ 下真实存在
3. 若发现孤立引用 → 在 BUILD 报告中列出 → 返回 DESIGN 步骤修复
```

### 7.3 必检产物存在性检查

```
1. 验证 docs/designs/prototypes/design-system/MASTER.md 存在且包含以下必需章节:
   - 色彩方案（含色值）
   - 字体系统（标题 + 正文字体）
   - 间距规格
   - 组件规范
   - 交互规则
2. 验证 docs/designs/prototypes/design-tokens.css 存在且含 CSS 变量声明
3. 如任一产物缺失 → ⚠️ 阻塞，返回 DESIGN 步骤补齐
4. 如产物均存在 → 记录"必检产物检查通过"
```

### 7.4 清单与磁盘一致性检查

```
1. 验证 docs/designs/prototypes/manifest.md 存在
2. 双向比对清单声明的文件与实际磁盘文件:
   - 清单声明但磁盘不存在 → 违规
   - 磁盘存在但清单未声明 → 违规
3. 验证清单中至少包含一个角色为 entry 的文件条目
4. 任一项不通过 → 返回 DESIGN 步骤修复
```

### BUILD 报告

主 Agent SHALL 将四项检查结果汇总输出到变更级 `self-reviews/prototype/cdn-crossref-check/report.md`，包含：

- 扫描范围（文件列表）
- 发现的外部引用（文件/引用 URL/类型）
- 引用完整性矩阵（源文件/引用路径/目标文件是否存在）与断链清单
- 必检产物存在性结果
- 清单与磁盘双向比对结果
- 四项检查各自结论（通过/不通过）

CDN 扫描不通过时，其余三项检查 SHALL 继续执行并记录结果，所有问题汇总在同一份 `report.md` 中。

**该报告在两种审查方式下均产出。**

---

## 8. 审查方式选择

BUILD 四项静态检查全部通过后，系统 SHALL 通过 AskUserQuestion 询问用户选择审查方式：

```
Question: "原型已生成并通过 BUILD 门控（CDN 扫描 / 交叉引用 / 必检产物 / 清单一致 四项通过）。
是否执行子代理自动审查验证？
  - 子代理自动审查验证：5 轮导航验证 + 5 轮 Playwright 验证 + 5 轮 UX 规则审查 + 对比度检测 + 档位自审（轻量 0 轮 / 标准 2 轮 / 完整 10 轮）
  - 人工审查：跳过全部自动验证，直接进入用户评审"
Options:
  - "子代理自动审查验证" → 进入 §9 VERIFY 与 §10 SELFREV
  - "人工审查" → 跳过 §9 与 §10，直接进入 §11 REVIEW
```

### 记录与恢复

```
1. 用户选定审查方式后，SHALL 将选择结果记录到变更的 .status.md 原型阶段条目
2. 后续 VERIFY 与 SELFREV 步骤 SHALL 依据该记录决定是否执行
3. 变更从 .status.md 恢复执行且已记录审查方式时:
   - SHALL 读取已记录的审查方式
   - SHALL NOT 重复询问审查方式
4. SHALL NOT 在 BUILD 未通过时发起该询问
```

---

## 9. VERIFY — 子代理自动审查验证（条件执行）

> **前置条件**：本节仅在审查方式为「子代理自动审查验证」时执行。审查方式为「人工审查」时，系统 SHALL 完全跳过本节全部步骤，SHALL NOT 启动任何验证子代理，直接进入 §11 REVIEW。

### 执行顺序

```
9.1 导航验证(5轮) → 9.2 Playwright(5轮) → 9.3 UX 规则审查(5轮) → 9.4 对比度检测
每轮子代理串行: 前一轮完成 → 主 Agent 读取报告 → 修复 → 下一轮
各项验证 SHALL 串行执行，SHALL NOT 并行启动多个子代理
```

### 9.1 导航合理性验证（5 轮子代理串行）

导航合理性验证执行 5 轮，每轮启动一个独立子代理执行全部 5 项检查。

#### 每轮子代理启动

```
主 Agent → Agent(subagent_type="claude", description="导航合理性验证 Round {N}", prompt="...")
每轮子代理执行全部 5 项检查 → 输出报告 → 主 Agent 读取 → 修复 → 下一轮
```

#### 每轮 5 项检查

| # | 检查项 | 内容 |
|---|--------|------|
| 1 | 页面可达性 | 从 `docs/designs/prototypes/index.html` 出发 BFS 遍历所有 `<a href>` 和导航组件引用，生成可达性矩阵，标记孤立页面和死胡同页面 |
| 2 | 返回/取消按钮合理性 | 穷举所有"返回""取消""关闭"按钮，验证目标页面是其语义父页面（详情→列表、表单取消→进入前页面、弹窗关闭→上下文不变），标记语义不合理的返回目标 |
| 3 | 表单切换链 | 验证多步表单的"上一步/下一步"链条完整，提交成功后去向明确且合理，提交失败后留在当前页并保留已填数据，标记断链或去向不明确的表单 |
| 4 | 弹窗/抽屉导航 | 验证每个弹窗/抽屉的触发方式正确、所有关闭方式可用（确认/取消/点击遮罩/Esc）、嵌套层级关系和逐层关闭，标记关闭后上下文错乱的情况 |
| 5 | 跨页面流程闭环 | 按业务流程脚本逐条走通完整导航路径，验证从入口到终点能回到起点（闭环），无"跳进去出不来"的页面序列，标记流程断点 |

#### 验证报告

每轮子代理输出报告到 `self-reviews/prototype/nav-check/round-{N}.md`（N 为轮次 1-5），包含 5 项检查各自的结果、发现问题和建议修复。

#### 强制执行规则

- SHALL 完成全部 5 轮子代理验证
- SHALL NOT 因中间某轮无新问题而提前终止，即使连续多轮无新问题也必须完成全部 5 轮
- 每轮完成后主 Agent SHALL 读取其报告并修复发现问题，修复完成后启动下一轮

### 9.2 Playwright 全覆盖验证（5 轮子代理串行）

导航合理性验证完成后，执行 5 轮 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查。

#### 工作目录约束

子代理工作目录 SHALL 固定为项目根目录。原型 HTML 文件通过 `docs/designs/prototypes/index.html` 相对项目根路径引用。Playwright SHALL 使用 `.kflow-runtime/playwright/` 下的隔离安装。SHALL NOT 在 `docs/designs/prototypes/` 目录下执行 `npm install` 或 `npx playwright`。

#### 每轮子代理启动

```
主 Agent → Agent(
  subagent_type="claude",
  description="Playwright 验证 Round {N}",
  prompt="工作目录固定为项目根目录。使用 /playwright-cli 打开 docs/designs/prototypes/index.html（相对项目根路径），执行全部 5 项检查..."
)
每轮子代理执行全部 5 项检查 → 输出报告 → 主 Agent 读取 → 修复 → 下一轮
```

#### 每轮 5 项检查

| # | 检查项 | 内容 |
|---|--------|------|
| 1 | 页面可达性扫描 | 从 `index.html` 出发 BFS 遍历所有 `<a>` 链接，每个页面验证加载成功且 `pageerror` 数量 = 0，输出可达性矩阵 |
| 2 | 按钮/链接全覆盖点击 | 穷举每个页面的所有 `<button>` 和 `<a>` 元素，逐个点击验证有响应（跳转/弹窗/状态变更/无错误），`disabled` 状态按钮验证不可点击，输出覆盖清单 |
| 3 | 表单全覆盖 | 对每个表单执行空提交验证（校验提示正确显示）、合法数据提交验证（提交行为正确）、取消/重置操作验证，输出覆盖清单 |
| 4 | 弹窗/抽屉全覆盖 | 对每个弹窗/抽屉验证所有打开方式、所有关闭方式（确认/取消/点击遮罩/Esc），弹窗内表单和按钮按上述规则验证，输出覆盖清单 |
| 5 | 端到端业务流程 | 按 `prototype-plan/design-prompt.md` 中定义的业务流程脚本逐条走通，验证无 JS 错误、无交互断点、无死胡同，输出流程通过清单 |

#### Playwright 不可用降级

```
1. 检查 .kflow-runtime/playwright/node_modules/playwright 是否存在
2. 若不存在:
   ├── 优先执行安装引导: cd .kflow-runtime/playwright && npm init -y && npm install playwright && npx playwright install chromium
   ├── 安装成功 → 使用隔离安装继续 Playwright 验证
   └── 安装失败 → 降级为手动文件分析
3. 若 playwright-cli 不可用且无法安装:
   ├── 子代理 prompt 中指示降级为手动文件分析
   ├── 记录降级原因到验证报告
   └── 报告标注 "Playwright 不可用 — 降级为手动检查"
```

#### 验证报告

每轮子代理输出报告到 `self-reviews/prototype/playwright-check/round-{N}.md`（N 为轮次 1-5），包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复。降级报告同样保存到该路径。

#### 运行时隔离

全部 5 轮 Playwright 验证完成后，`docs/designs/prototypes/` 目录 SHALL NOT 包含 `node_modules/`、`package.json`、`package-lock.json`。若发现上述文件，SHALL 在 POST_HOOK BROWSER_CLEANUP 中清理。

#### 强制执行规则

- SHALL 完成全部 5 轮子代理验证
- SHALL NOT 因中间某轮无新问题而提前终止，即使连续多轮无新问题也必须完成全部 5 轮
- 每轮完成后主 Agent SHALL 读取其报告并修复发现问题，修复完成后启动下一轮

### 9.3 UX 规则审查（5 轮子代理串行）

Playwright 验证完成后，执行 5 轮 UX 规则审查，每轮启动一个独立子代理执行精简核心规则集审查。

#### 精简核心规则集（20-30 条）

子代理读取 `docs/designs/prototypes/` 目录下所有 HTML 文件，逐条检查以下核心规则：

| # | 规则 | WCAG 参考 |
|---|------|-----------|
| 1 | 对比度 ≥ 4.5:1（正文文字） | WCAG AA |
| 2 | 触摸目标 ≥ 44×44px | Apple HIG / Material |
| 3 | 表单 label 非 placeholder-only | WCAG |
| 4 | 按钮视觉反馈（hover/active 态） | UX 最佳实践 |
| 5 | 弹窗有明确关闭方式（确认/取消/遮罩/Esc） | Apple HIG |
| 6 | 错误信息有明确恢复路径 | HIG / Material |
| 7 | 必填字段有明确标记 | Material |
| 8 | 空态有引导操作 | UX 最佳实践 |
| 9 | 加载态有 skeleton/spinner 反馈 | Material |
| 10 | 导航层级 ≤ 3 级 | Apple HIG |
| 11 | 表单内联验证（非提交后） | Material |
| 12 | 主操作按钮视觉突出 | Apple HIG |
| 13 | 无水平滚动溢出（移动端） | Responsive |
| 14 | 文字截断使用 ellipsis | Material |
| 15 | 图片有 alt 文本或 aria-label | WCAG |
| 16 | 焦点状态可见 | WCAG AA |
| 17 | 无自动播放音频/视频 | WCAG |
| 18 | 表单字段有正确的 input-type | Material |
| 19 | 破坏性操作有确认对话框 | Apple HIG |
| 20 | Toast 自动消失 3-5s | Material |

#### 验证报告

每轮子代理输出报告到 `self-reviews/prototype/ux-check/round-{N}.md`（N 为轮次 1-5），包含检查项逐条结果、发现问题和建议修复。

#### 强制执行规则

- SHALL 完成全部 5 轮
- 不允许提前终止
- 如果环境中存在 ui-ux-pro-max，其完整 99 条 UX 规则库作为"可选增强"并行执行

### 9.4 对比度检测

UX 规则审查完成后，执行对比度检测：

```
1. 扫描 docs/designs/prototypes/ 目录下所有 .html 文件
2. 提取所有文本颜色对（背景色 + 前景色）
3. 使用 WCAG 相对亮度计算公式:
   - 相对亮度 L = 0.2126 * R + 0.7152 * G + 0.0722 * B（sRGB 线性化）
   - 对比度 = (L1 + 0.05) / (L2 + 0.05)，L1 > L2
4. 标记对比度 < 4.5:1 的颜色对（不满足 WCAG AA）
5. 输出报告到 self-reviews/prototype/contrast-check/report.md:
   - 所有检测到的颜色对及其对比度值
   - 标记 ⚠️ 不达标的颜色对
   - 建议替代色值
```

---

## 10. SELFREV — 自审（按变更档位，条件执行）

> **前置条件**：本节仅在审查方式为「子代理自动审查验证」时执行。审查方式为「人工审查」时，prototype 阶段 SHALL 完全跳过 SELFREV，不启动任何自审子代理、不计算目标轮次、不执行评分底线判定，SHALL NOT 保留兜底轮次，系统直接进入 §11 REVIEW。

> **机制说明**：轮次取值与产物门控规则定义在 `tier-driven-repetition` 能力；本文件 SHALL NOT 自定义「影响范围分数 → 轮次」的数值区间。

### 概述

原型设计阶段在设计引擎委托执行完成、用户评审确认之前，按审查方式决定是否执行自循环审查（SELFREV）。执行时目标轮次由**变更档位**决定，自审启动前 SHALL 读取变更级 `.status.md` 的「变更档位」字段：

| 变更档位 | 目标轮次 | 评分底线 |
|---------|---------|---------|
| 轻量 | 0（跳过 SELFREV） | 不适用 |
| 标准 | 2 | 不适用 |
| 完整 | 10 | 各维度评分均 > 8 方通过 |

> 档位字段缺失时按 `完整` 档处理（10 轮自审），等价于历史行为。

评分底线仅完整档适用：每轮子代理输出各维度评分（0–10 量纲），各维度均 > 8 方通过；任一维度 ≤ 8 继续补审，直至各维度均 > 8 或达到 10 轮上限。标准档按目标轮次执行，不适用评分底线。

自审由子代理（Agent subagent）串行执行，采用重复制——每轮子代理独立执行全部四个维度（覆盖性/一致性/可用性/完整性），覆盖性为第一优先级。子代理意外停止时，主代理 MUST 重新创建子代理，SHALL NOT 接管执行。

### 轻量档：以产物门控替代自审

轻量档（目标轮次 0）SHALL 完全跳过 SELFREV，SHALL NOT 启动任何自审子代理，SHALL NOT 产出自审报告文件。为保证质量，阶段门控以**产物完整性门控**替代：本阶段产物 SHALL 全部存在且不含 TODO、TBD 或未填充占位符；任一产物缺失或含占位符时 SHALL ⚠️ 阻塞该阶段，返回 DESIGN 补齐。

| 产物层级 | 校验产物 |
|---------|---------|
| 变更级 | `prototype-changes.md`、`prototype-plan/design-prompt.md`、`prototype-plan/style-decision.md`、`element-coverage-tree.md` |
| 产品级 | `docs/designs/prototypes/index.html`、`design-tokens.css`、`design-system/MASTER.md`、`manifest.md` |

审计 SHALL NOT 因轻量档缺少自审记录判定为缺项：轻量档不产出自审报告轮次文件（`self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md`）属合法状态。BUILD 门控报告（`self-reviews/prototype/cdn-crossref-check/report.md`）在两种审查方式下均产出，不受本节影响。

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
| 视觉风格 | 组件命名是否一致 |
| 布局模式 | 页面布局模式是否统一 |
| 交互模式 | 交互模式是否一致 |

#### 可用性

| 检查项 | 规则 |
|--------|------|
| 交互流畅性 | 交互流程是否顺畅 |
| 状态覆盖 | 交互状态覆盖是否完整（加载/空/错误/边界） |
| 反馈机制 | 用户操作是否有明确的反馈 |

#### 完整性

| 检查项 | 规则 |
|--------|------|
| 入口可达 | 所有页面入口是否可达 |
| 组件状态 | 组件状态覆盖是否完整 |
| 流程闭环 | 交互流程是否无断点 |

### 自审模式：重复制

| 对比维度 | 分工制（旧） | 重复制（新） |
|---------|------------|------------|
| 每轮范围 | 部分维度 | 全部维度 |
| 发现问题 | 后期才暴露其他维度问题 | 早期就暴露各类问题 |
| 收敛性 | 不明显 | 自然收敛（后期问题越来越少） |
| 独立性 | 维度间串行 | 每轮独立完整审查 |

### 自审流程

```
自审执行流程（重复制，按变更档位决定目标轮次）:

1. 读取变更级 .status.md 的「变更档位」字段（缺失按 完整 档处理）
2. 轻量档（0 轮）→ 跳过自审，执行产物完整性门控后直接进入 REVIEW
3. 记录开始时间（作为时间戳）
4. 按覆盖性、一致性、可用性、完整性四个维度逐项检查（覆盖性为第一优先级）
5. 发现问题 → 立即修复
6. 生成自审报告 → 保存到 self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md
7. 每轮均执行全部四个维度的完整检查
8. 轮次控制：
   ├── 标准档 → 完成全部 2 轮
   └── 完整档 → 完成全部 10 轮，各维度评分均 > 8 即通过；未达标补审至 10 轮上限
9. 全部完成后进入用户评审确认
```

### 自审记录存储

- 根目录：`self-reviews/prototype/`
- 文件名：`{YYYYMMDD}-{HHMMSS}.md`（审查开始时间）
- 每轮一个独立文件，自然排序即时间序
- 报告模板参考：`docs/designs/templates/changes/{change}/self-reviews/review-round.md`

### 自审报告内容

每轮报告包含：
- 审查维度得分表（维度名、本轮得分、上轮得分、变化值）
- 新发现问题清单（序号、问题描述、严重度、状态）
- 上轮问题修复验证（序号、上轮问题、修复结果）
- 本轮改进内容描述
- 仍存在问题（进入下一轮继续跟踪）

### 强制执行规则

- 轻量档 SHALL NOT 执行 SELFREV、SHALL NOT 启动自审子代理、SHALL NOT 产出自审报告；以产物完整性门控替代，门控不通过时阻塞该阶段
- 标准档 SHALL 完成全部 2 轮自审，不允许提前终止
- 完整档 SHALL 完成全部 10 轮自审，且各维度评分均 > 8 方通过；未达标补审至 10 轮上限
- 即使连续多轮无新问题，也须完成全部目标轮次（标准 2 轮 / 完整 10 轮）
- 审查方式为「人工审查」时，SELFREV SHALL NOT 执行，不计算目标轮次、不保留兜底轮次
- 自审全部完成后进入用户评审确认（AskUserQuestion），释放 design 阶段门控
- 子代理意外停止、报错退出或返回要求重做/继续时，主代理 MUST 分析原因后重新创建新的子代理；SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作；新子代理的 prompt 包含上一轮的上下文和未完成的工作说明

---

## 11. REVIEW — 用户评审循环

通过 AskUserQuestion 进行用户评审：

```
Question: "HTML 原型已完成，覆盖 {n} 个屏幕、{m} 个 UI 功能点。
[BUILD 门控: CDN 扫描 {通过/不通过} | 交叉引用 {通过/不通过} | 必检产物 {通过/不通过} | 清单一致 {通过/不通过}]
[审查方式: {人工审查 / 子代理自动审查验证}]
--- 审查方式为「子代理自动审查验证」时追加 ---
[导航合理性验证: 5 轮完成，发现并修复 {x} 个问题]
[Playwright 验证: 5 轮完成 / 降级为手动检查，发现并修复 {y} 个问题]
[UX 规则审查: 5 轮完成，发现并修复 {a} 个问题]
[对比度检测: {通过/不通过}]
[自审: {完成轮次}，发现并修复 {z} 个问题]
是否确认通过？"
Options:
  - "确认通过" → 原型满足需求，进入详细设计
  - "需要修订" → 收集反馈 → 回到 DESIGN 步骤
```

### 循环机制

```
DESIGN(子代理委托，直写产品级) → BUILD(四项静态检查) → 审查方式选择
  ├── 人工审查            → REVIEW
  └── 子代理自动审查验证  → VERIFY(导航5轮+Playwright5轮+UX5轮+对比度) → SELFREV → REVIEW
REVIEW
  ├── 确认通过 → COMPLETE
  └── 需修订 → 收集用户反馈 → 回到 DESIGN（再次启动子代理，附修订要求）
```

### 评审结果处理

| 用户选择 | 阶段状态 | 评审记录 | 后续动作 |
|---------|---------|---------|---------|
| 确认通过 | ✅ 完成 | ✅ 已确认 | 门控释放，可进入详细设计 |
| 需要修订 | ⚠️ 需修订 | ⚠️ 需修订 | 保持原型设计阶段，根据用户反馈修订原型 |

---

## 12. COMPLETE — 更新状态文件 + 同步清单 + 提取设计令牌与元素覆盖树

Update `docs/changes/{change}/.status.md`:

1. Mark prototype design phase: `✅ 完成` (or `⏭️ 跳过`)
2. Record user review result in user review table
3. Set current phase to `详细设计`
4. Record completion time and execution notes

### 12.1 同步产品级原型清单（用户确认通过后执行）

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

### 12.2 原型通过后自动提取设计令牌和元素覆盖树（用户确认通过后执行）

当用户在 REVIEW 步骤中"确认通过"后，系统 SHALL 从实际原型 HTML 文件中提取设计令牌（产品级）和元素覆盖树（变更级）：

#### 提取 design-tokens.css（产品级）

```
1. 扫描产品级 docs/designs/prototypes/ 目录下所有 .html 文件
2. 提取范围 SHALL 限定为本变更涉及的页面（依据变更级 prototype-changes.md 的改动清单）
3. 提取 :root { ... } 中的 CSS 变量声明
4. 提取内联 style 中出现的颜色值、font-size、border-radius、box-shadow 等样式值
5. 去重、排序、归类后输出到产品级 docs/designs/prototypes/design-tokens.css
6. 文件头部标注: 提取来源（原型版本、生成时间、自动提取）
7. 本变更新增的 CSS 变量 SHALL 追加到产品级 design-tokens.css，并注释标注来源变更和追加时间
8. SHALL 在变更级 prototype-changes.md 中登记 design-tokens.css 的改动条目
```

#### 提取 element-coverage-tree.md（变更级）

```
1. 从产品级 docs/designs/prototypes/ 目录下本变更涉及页面的 .html 文件中解析 DOM 树
2. 提取页面导航骨架: 所有 <a href> 和导航组件引用 → 构建 📄 页面节点层
3. 提取交互元素: <button>、<a>、<input>、<select>、<textarea>、<dialog>、[role="dialog"]、<details>
   - 每个元素标注类型、文本内容或 aria-label
   - 按 DOM 层级组织到页面 → 区域 → 元素结构
4. 提取 CSS 伪类状态: 扫描样式表和内联 style 中的 :hover、:active、:focus、:disabled
   - 扫描 class 命名推测状态: is-loading、is-error、is-empty、is-disabled、is-active
   - 每个发现的状态作为 🎯 节点挂载到对应元素下
5. 提取操作链: 扫描 JS 事件绑定（onclick、addEventListener、@click、onClick）
   - 分析事件处理函数中的 DOM 操作（显示/隐藏弹窗、添加/移除 class）
   - 推断操作触发的动态元素（弹窗/下拉/浮窗）并构建 💬 子树
   - 分析页面跳转逻辑构建 🔗 跳转关联
6. 输出变更级 docs/changes/{change}/element-coverage-tree.md（初始版，TC-ID 列为空）
7. 文件位置 SHALL 固定于变更根目录，使 TC-ID 追溯保持在变更级，避免被后续变更覆盖
8. 文件头部标注: 生成时间戳和来源（prototype-design 阶段自动生成）
```

> **说明**: 元素覆盖树承载 TC-ID 映射，是变更级追溯产物，design 阶段会在其上追加填充。设计令牌描述产品整体视觉规范，属产品级资产，被 code 与 code-review 阶段消费。

#### 原型迭代后重新生成

当原型设计阶段用户确认通过后又进入修订循环，新一轮用户确认通过后，重新执行 design-tokens.css 和 element-coverage-tree.md 的提取，覆盖旧版本文件。若 design 阶段已填充 TC-ID，SHALL 通过 AskUserQuestion 确认是否保留已有映射。同时 SHALL 同步更新产品级 manifest.md 中的文件清单和版本号。

#### 用户跳过原型设计时不生成

当原型设计阶段被跳过（⏭️ 跳过）时，系统不生成 `docs/designs/prototypes/design-tokens.css` 和 `element-coverage-tree.md`。后续 code 和 code-review 阶段不执行原型对账。后续 design 阶段按路径 B（playwright-cli 探索）生成元素覆盖树。

---

## 13. POST_HOOK — 浏览器清理与状态更新

引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 POST_HOOK：

```
├── BROWSER_CLEANUP → playwright-cli kill-all 清理浏览器进程
│                     并清理 docs/designs/prototypes/ 下残留的 node_modules/、package.json、package-lock.json
└── UPDATE_STATE → 更新 .status.md
```

> **条件性**：Playwright 验证仅在「子代理自动审查验证」路径执行，因此 BROWSER_CLEANUP 的浏览器进程清理只在需要时产生实际作用；残留产物清理与 UPDATE_STATE 无条件执行。

---

## 原型改动回滚（按需，非流程步骤）

> 对应能力：`prototype-change-tracking`「回滚支持」

当变更被废弃，或用户要求撤销本变更对产品级原型的改动时，系统 SHALL 依据变更级 `prototype-changes.md` 与 `prototype-backup/` 把产品级原型目录恢复到本变更介入之前的状态：

```
1. 读取变更级 prototype-changes.md 的改动清单
2. 向用户展示受影响的文件清单（产品级相对路径 + 改动类型），取得确认
3. 逐条处理:
   ├── 类型为「修改」或「删除」的条目 → 用 prototype-backup/ 中对应产品级相对路径的快照恢复
   └── 类型为「新增」的条目 → 删除产品级 docs/designs/prototypes/ 中的对应文件
4. 回滚完成后在 prototype-changes.md 的改动清单中标记对应条目已回滚，并写入「四、回滚记录」
```

回滚属于原型设计阶段的职责范围。下游阶段（plan、code、code-review、e2e-test、integration-test）SHALL NOT 自行执行原型回滚，须经 REVISION 模式或本流程回退到原型设计阶段处理。

---

## 审查产物存放约束

原型设计阶段的所有审查与验证产物 SHALL 统一存放在变更级 `self-reviews/prototype/` 目录下，SHALL NOT 将验证报告散落在产品级原型目录 `docs/designs/prototypes/` 下。产品级原型目录只承载原型产物本身（`index.html`、`screens/`、`components/`、`assets/`、`design-tokens.css`、`design-system/MASTER.md`、`manifest.md`）。

---

## 跳过条件

| 条件 | 处理 |
|------|------|
| 纯后端项目 | 自动跳过，标记 ⏭️ 跳过 |
| functional-designs/ 中无前端/UI 功能点 | 自动跳过，标记 ⏭️ 跳过 |
| 用户在 AskUserQuestion 中拒绝 | 跳过，标记 ⏭️ 跳过 |
| 需重新选择工具链且 prototype-gen 角色 Skill 数量 = 0 | ⚠️ 阻塞，提示安装 huashu-design 或 frontend-design，不跳过 |

---

## 与其他 Skill 的关系

- **输入来自**：`kflow-explore`（设计探索阶段）
- **输出给**：`kflow-design`（详细设计阶段）
- **前置阶段**：设计探索
- **后续阶段**：详细设计（原型设计完成后或跳过后）
- **委托执行**：按有效工具链锁定的设计引擎（huashu-design / frontend-design / 其他）执行，需重新选择且不可用时阻塞
- **归档登记**：`kflow-archive` 将本变更的原型改动登记到 `docs/designs/prototypes/manifest.md`（原型已在原型设计阶段直写产品级，归档不再执行文件级合并）

---

## 阶段边界约束

### 域内内容（prototype 负责）

| 内容类别 | 说明 |
|---------|------|
| UI 原型页面 | 基于 functional-designs/ 的页面定义生成多文件 HTML 原型，**直写产品级 `docs/designs/prototypes/`**（`index.html` 为全产品入口，屏幕在 `screens/`） |
| 交互流程 | 基于功能设计中的可执行操作和业务流程设计交互，使用 flow demo 模式（完整可交互路径） |
| 视觉风格 | 统一的视觉风格、组件命名、页面布局模式 |
| 交互状态 | 加载态、空态、错误态、边界态等完整状态覆盖 |
| 表单组件 | 基于功能设计中的表单项定义（字段名/类型/校验规则/默认值）生成对应表单组件 |
| 离线自包含 | 所有资源内联或相对路径引用，禁 CDN 外部依赖，系统字体栈 |
| 改动追踪 | 维护变更级 `prototype-changes.md`（改动清单 + 改动前哈希）与 `prototype-backup/`（改动前快照），支持并发检测与回滚 |

### 域外内容（禁止）

| 内容类别 | 说明 | 应由哪个阶段处理 |
|---------|------|----------------|
| 功能决策 | 新增/删除/修改功能点定义 | explore（回退） |
| 业务规则修改 | 修改功能设计中的业务规则 | explore（回退） |
| 技术实现决策 | 技术架构、接口设计、数据模型 | design |
| 代码实现 | 任何代码文件 | code |

### 产品级原型目录的写权限

产品级 `docs/designs/prototypes/` 目录的写权限 SHALL 仅归属于原型设计阶段（kflow-prototype-design）；变更级 `prototype-changes.md` 与 `prototype-backup/` 同样 SHALL 仅由原型设计阶段写入。其他阶段对两者只读。

当下游阶段（plan、code、code-review、e2e-test、integration-test）执行过程中发现原型产物存在问题时：

1. 系统 SHALL 通过回退机制触发原型设计阶段的修订流程（REVISION 模式）
2. SHALL NOT 直接修改 `docs/designs/prototypes/` 目录下的任何文件（含 `manifest.md`、`index.html`、HTML 文件、CSS 文件等）
3. SHALL NOT 直接修改变更级 `prototype-changes.md` 与 `prototype-backup/`
4. 回退修订完成后由原型设计阶段负责更新产品级 `manifest.md` 与变更级 `prototype-changes.md`

### 越界处理

当 prototype 阶段发现功能设计不完整或定义不清晰时：
1. 记录到 `docs/skill-suggestion.md`
2. 在当前能力范围内完成原型（标注已知局限）
3. 提示用户是否需要回退 explore 阶段补充
4. 禁止自行修改 functional-designs/ 内容

**code 阶段回退到 prototype-design 的越界处理**：

当编码阶段发现原型问题并回退到 prototype-design REVISION 模式时：
1. 编码 Agent 记录具体问题到 `docs/skill-suggestion.md`（格式：原型页面路径 + 问题描述 + 建议修订方向）
2. prototype-design 加载编码阶段记录的问题作为修订输入
3. 修订完成后通知 code 阶段重新执行受影响的功能点
4. 修订范围仅限于原型问题，不扩展到功能设计或技术设计领域

---

## 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
