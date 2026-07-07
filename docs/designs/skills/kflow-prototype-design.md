# kflow-prototype-design（原型设计阶段）

> **版本**: 参见仓库根目录 `VERSION` 文件
> **阶段**: 原型设计（可选阶段）
> **破坏性变更**: v2.3.0 → v3.0.0 工具链灵活性——CHECK 从硬编码 huashu-design 改为动态扫描环境设计 Skills；新增 SCAN+TOOLCHAIN 步骤；DESIGN 拆分为 5.1 STYLE（风格推荐）+ 5.2 GENERATE（按 toolchain 锁定执行）；VERIFY 增强（UX 规则审查+对比度检测+design-system 产物必检）；新增 prototype/style-decision.md、design-system/MASTER.md 产物

---

## 基本信息

```yaml
name: kflow-prototype-design
description: 原型设计阶段 - 编排层，动态扫描环境设计 Skills，组合工具链方案供用户选择，选定后锁定执行。可选阶段，仅涉及前端/UI 变更时推荐使用。
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

## 架构模型：编排层 → 工具链选择 → 子代理执行引擎

`kflow-prototype-design` 作为编排层，动态扫描环境中可用的设计 Skills，组合为可行工具链方案供用户选择，选定后锁定执行：

```
kflow-prototype-design (编排层)
├── 阶段门控 + 状态管理 + 用户评审
├── 产品级上下文加载（docs/prototype/）
├── SCAN: 环境扫描设计 Skills → 角色分类（prototype-gen/design-system/ux-review/code-gen）
├── TOOLCHAIN: 多方案推荐 → AskUserQuestion 选择 → 写入 docs/toolchain.md 锁定
├── prompt 上下文组装（INPUT：机械提取）
├── prompt 优化（OPTIMIZE：设计转译 + design-prompt.md 输出 + 用户确认）
├── Agent(subagent) 子代理 → 按 toolchain.md 锁定执行
│   ├── 5.1 STYLE: 子代理推荐 3 个差异化风格方向 → 用户选择 → style-decision.md
│   └── 5.2 GENERATE: 按 toolchain.md execution_order 调用设计引擎 → HTML 原型 + design-system/MASTER.md
├── 验证: CDN 扫描 + 交叉引用 + 导航验证(5轮子代理) + Playwright(5轮子代理)
│       + UX 规则审查(5轮子代理) + 对比度检测 + design-system 产物必检
└── 用户评审循环
```

**设计决策**：工具链动态选择，非硬编码绑定。环境中可能有 huashu-design、ui-ux-pro-max、frontend-design 等多种设计 Skill，编排层扫描后按角色组合为方案供用户选择。选定后写入 docs/toolchain.md 作为 DESIGN 步骤唯一执行依据，禁止运行时自行切换。

**角色分类**：
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
- **prototype-gen 角色 Skill 可用**（硬拦截：扫描 `.claude/skills/` 中 prototype-gen 角色的 Skill 数量，=0 时标记 ⚠️ 阻塞，提示安装 huashu-design 或 frontend-design）

若无前端变更，自动跳过此阶段，状态标记为 ⏭️ 跳过。

---

## 输入要求

| 输入 | 图例 | 说明 |
|------|------|------|
| functional-designs/ | ✅ 必须 | 设计探索阶段输出，提取项目背景和 UI 功能点清单 |
| docs/prototype/ | 🔶 条件 | 产品级已有原型，存在时作为设计约束加载 |
| docs/prototype/design-tokens.css | 🔶 条件 | 已有设计令牌，存在时纳入设计约束 |
| brand-spec.md | 🔶 条件 | 品牌资产，涉及品牌时纳入 prompt |

---

## 输出产物

| 产物 | 文件 | 模板 | 内容要求 |
|------|------|------|---------|
| 工具链选择记录 | docs/toolchain.md（项目级） | N/A（TOOLCHAIN 步骤输出） | 原型设计阶段选定的工具链方案，含 skills_used、execution_order、decision_time |
| 原型清单（Manifest） | prototype/index.md | [原型索引](../../templates/changes/{change}/prototype/index.md) | 原型清单入口（必须）。含原型文件清单（文件/说明/版本表，标注角色：page/design-tokens/coverage）、页面清单（页面/路由/原型文件/所含区域表）、设计系统引用（色彩/字体/间距/组件库及其在 design-system/MASTER.md 中的来源章节）、修订记录（统一格式）。版本号 1.0.0 起始。下游阶段通过此清单获取原型产物路径。 |
| 风格选择决策 | prototype/style-decision.md | N/A（STYLE 步骤输出） | 用户选定的风格方向：风格名称、设计哲学、色彩方案、字体系统、布局模式、ASCII 线框图 |
| 提示词文件 | prototype/design-prompt.md | [design-prompt.md](../../templates/changes/{change}/prototype/design-prompt.md) | 7 章节完整提示词文件（项目背景、设计系统、菜单导航、页面规格、业务流程脚本、硬约束、高保真要求），DESIGN 步骤的唯一真相源 |
| 原型文件（多文件） | prototype/ 目录（index.md 为清单入口） | N/A（按 toolchain 锁定生成） | 多文件 HTML 交互原型，index.md 为清单入口记录各文件路径与角色，所有文件离线自包含 |
| 设计令牌 | prototype/design-tokens.css | N/A（自动提取） | 从原型 HTML 中提取的 CSS 变量声明、颜色值、间距、圆角等样式值，供 code/code-review 阶段对账 |
| 元素覆盖树 | prototype/element-coverage-tree.md | N/A（自动生成） | 四层树状结构（📄页面→🏗️区域→🔘元素→🎯状态+操作链），TC-ID 列初始为空，替代 element-spec.md 和 nav-tree.md |
| 设计系统 | design-system/MASTER.md | N/A（设计引擎输出） | 通用必备产物：色彩方案、字体系统、间距规格、组件规范、交互规则。无论选定哪个工具链都必须输出 |
| 导航验证报告 | prototype/nav-check-round-{1..5}.md | N/A（自动生成） | 5 轮导航合理性验证报告（页面可达性、返回/取消按钮、表单切换链、弹窗/抽屉、跨页面流程闭环） |
| Playwright 验证报告 | prototype/playwright-check-round-{1..5}.md | N/A（自动生成） | 5 轮 Playwright 全覆盖验证报告（页面可达性、按钮/链接全覆盖、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）或降级说明 |
| UX 规则审查报告 | prototype/ux-check-round-{1..5}.md | N/A（自动生成） | 5 轮 UX 规则审查报告（内置 20-30 条精简核心规则：对比度/触摸目标/表单 label/按钮反馈/弹窗关闭等） |
| 对比度检测报告 | prototype/contrast-check.md | N/A（自动生成） | WCAG 相对亮度计算结果，标记 <4.5:1 的颜色对 |
| 用户评审记录 | .status.md | N/A（自动生成） | 原型设计评审状态、时间、备注 |

**产物位置**：`docs/changes/{change}/prototype/` 目录。

**产物形式**：多文件架构，`index.md` 为清单入口，可包含 `page-*.html` 独立页面文件及 `shared/` 共享资源子目录。清单中按角色（page/design-tokens/coverage）标注各产物文件路径。

**离线自包含**：所有 HTML/CSS/JS/字体/图片必须内联或相对路径引用，禁止 CDN 外部依赖。

---

## 执行流程

```
原型设计阶段流程:

┌─────────────────────────────────────────────────────────────┐
│                   PROTOTYPE WORKFLOW (v3.0)                  │
├─────────────────────────────────────────────────────────────┤
│  1. CHECK     → 门控检查 + prototype-gen 角色可用性硬拦截    │
│             → 修订模式检测（prototype/index.md 是否存在）   │
│  1.5 PRE_HOOK → 引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 PRE_HOOK │
│  │   ├── CHECK_STATE → 验证前置阶段状态                       │
│  │   └── RELOAD → 重读 CONTEXT.md, toolchain.md, functional-designs/, .status.md │
│  2. SCAN      → 环境扫描设计 Skills → 角色分类               │
│  3. ASSESS    → 评估是否需要原型设计（新建模式）              │
│  4. INPUT     → 机械组装 prompt 上下文（数据收集层）          │
│  │   ├── 必然存在: functional-designs/ 提取背景+UI功能点      │
│  │   ├── 条件存在: docs/prototype/ 产品级已有原型             │
│  │   └── 条件存在: brand-spec.md 品牌资产                    │
│  5. OPTIMIZE  → 深度分析设计，产出优化后 prompt + 文件输出    │
│  │   ├── 提取菜单树（一/二/三级 → 对应页面）                  │
│  │   ├── 穷举页面元素（按钮/表单/数据区/弹窗/状态）            │
│  │   ├── 编写业务流程脚本（逐步用户操作路径）                  │
│  │   ├── 注入硬约束（多文件+flow demo+离线自包含）            │
│  │   ├── 注入 design-system/MASTER.md 输出要求              │
│  │   ├── 输出 design-prompt.md（7 章节完整模板）             │
│  │   └── AskUserQuestion 用户确认（确认执行/需修订）          │
│  6. TOOLCHAIN → 多方案推荐 → AskUserQuestion 选择 → 锁定     │
│  │   ├── 零 prototype-gen → ⚠️ 阻塞                           │
│  │   ├── 单一 prototype-gen → 自动选择该方案                  │
│  │   └── 多个 prototype-gen → 2-3 方案 → AskUserQuestion     │
│  ─ ─ ─ ─ ─ ─ ─ ─ 修订模式分支 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│  R. REVISION  → 修订模式（跳过 INPUT+OPTIMIZE+TOOLCHAIN）     │
│  │   ├── 加载 prototype/index.md 作为现有原型清单上下文       │
│  │   ├── 加载 prototype/design-prompt.md 作为已有设计约束     │
│  │   ├── 加载 docs/toolchain.md 作为已有工具链锁定            │
│  │   ├── AskUserQuestion 确认修订需求或展示已有原型           │
│  │   └── 合并修订需求到 prompt → 进入 DESIGN                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│  7. DESIGN    → 按 toolchain.md 锁定执行                      │
│  │   ├── 7.1 STYLE: 子代理推荐 3 个差异化风格方向             │
│  │   │   └── AskUserQuestion 选择 → style-decision.md        │
│  │   └── 7.2 GENERATE: Agent(subagent) 按 toolchain 执行      │
│  │       └── prompt = design-prompt.md + style-decision.md   │
│  8. VERIFY    → CDN + 交叉引用 + 导航 + Playwright            │
│  │   ├── 8.1 CDN 扫描: grep http:// https:// → 不通过       │
│  │   ├── 8.2 交叉引用: 验证所有内部文件引用存在              │
│  │   ├── 8.3 导航验证: 5 轮子代理串行（每轮全 5 项检查）    │
│  │   ├── 8.4 Playwright: 5 轮子代理串行（每轮全 5 项检查）  │
│  │   ├── 8.5 UX 规则审查: 5 轮子代理串行（内置 20-30 条）   │
│  │   ├── 8.6 对比度检测: WCAG 相对亮度计算，标记 <4.5:1      │
│  │   └── 8.7 design-system/MASTER.md 产物必检               │
│  9. SELFREV   → 10 轮自审（重复制：每轮全 4 维度）           │
│ 10. REVIEW    → AskUserQuestion 用户评审                     │
│  │   ├── 确认通过 → COMPLETE                                │
│  │   └── 需修订   → 收集反馈 → 回到 DESIGN                  │
│ 11. POST_HOOK → 引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 POST_HOOK │
│  │   ├── BROWSER_CLEANUP → playwright-cli kill-all 清理浏览器进程 │
│  │   └── UPDATE_STATE → 更新 .status.md                       │
│ 12. COMPLETE  → 更新状态文件，记录评审结果                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. CHECK — 门控检查 + prototype-gen 角色可用性

```
1. Read docs/changes/{change}/.status.md
2. Check: design exploration status = ✅ 完成
3. Check: functional-designs/index.md exists
4. Extract: project type from .status.md
5. If project type = pure backend → auto-skip (update status to ⏭️ 跳过, exit)
6. Scan functional-designs/ for UI-related feature points
7. If no UI FPs found → auto-skip (update status to ⏭️ 跳过, exit)
8. 修订模式检测:
   - Check if prototype/index.md already exists in change directory
   - If exists → 标记为修订模式候选，进入 §修订模式 分支
   - If not exists → 走新建模式，继续 SCAN → ASSESS → INPUT → OPTIMIZE → TOOLCHAIN → DESIGN
```

## 2. SCAN — 环境扫描设计 Skills

CHECK 步骤通过后，扫描环境中可用的设计相关 Skills：

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
   └── 用于 TOOLCHAIN 步骤的多方案推荐
```

### 角色可用性判定

- `prototype-gen` 数量 = 0 → ⚠️ 阻塞，提示："未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
- `prototype-gen` 数量 = 1 → 标记为单一方案，TOOLCHAIN 步骤自动选择
- `prototype-gen` 数量 ≥ 2 → 标记为多方案，TOOLCHAIN 步骤推荐 2-3 条工具链方案

## 3. ASSESS — 评估是否需要原型设计

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

## 3. INPUT — 组装 Prompt 上下文（机械提取层）

本步骤为 OPTIMIZE 步骤提供原始数据输入。按存在性分层组装基础 prompt 数据：

```
✅ 必然存在（前置阶段产物）:
  ├── functional-designs/index.md      → 提取产品概述
  ├── functional-designs/part-NN.md    → 提取 UI 功能点清单
  └── 产出路径: docs/changes/{change}/prototype/ 目录

🔶 条件存在（看项目历史 + 变更类型）:
  ├── docs/prototype/design-tokens.css → 已有设计令牌
  ├── docs/prototype/screens/          → 已有屏幕清单
  ├── docs/prototype/index.html        → 产品级全貌
  └── brand-spec.md                    → 品牌资产（涉及品牌时）
```

INPUT 产出为基础数据包，传递给 OPTIMIZE 步骤进行设计转译。

## 4. OPTIMIZE — 提示词优化与用户确认（设计转译层）

在委托 huashu-design 之前，编排层 Agent SHALL 深度分析 functional-designs/ 产出优化后的设计 prompt。

### 4.1 菜单结构提取

从 functional-designs/ 中提取并显式化为菜单树：

```
必须明确:
├── 一级菜单项及其对应页面
├── 二级菜单项（如有）及其对应页面
├── 三级菜单项（如有）及其对应页面
├── 导航模式: 顶部导航 / 侧边栏 / Tab Bar / 面包屑
└── 全局组件: Header / Footer / 用户头像 / 通知铃铛等
```

### 4.2 页面元素穷举

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

### 4.3 业务流程脚本

必须包含至少一个完整的端到端业务流程脚本：

```
流程脚本格式:
├── 流程名称: 如"用户登录→查看列表→进入详情→编辑→提交"
├── 逐步描述: 每步明确"用户在[哪个页面] → 点击[哪个按钮] → 看到[什么变化] → 进入[哪个页面或弹窗]"
├── 覆盖端到端路径: 从入口到最终结果，包含所有中间步骤
└── 如有多条核心流程，逐条编写
```

### 4.4 硬约束注入

优化后的 prompt MUST 包含以下硬约束：

| 约束 | 内容 |
|------|------|
| 多文件输出 | 输出到 `prototype/` 目录，允许多文件结构，`index.html` 为入口 |
| 业务流程驱动 | 使用 flow demo 模式（可交互业务流程，单台设备状态管理器驱动），禁止 overview 静态页面平铺 |
| 离线自包含 | 所有 CSS/JS/字体/图片内联或相对路径引用，禁止 `http://` `https://` 外部 CDN 依赖，字体使用系统默认字体栈 |
| design-system 输出 | 无论选定哪个工具链，设计引擎 SHALL 输出 `design-system/MASTER.md`（含色彩方案、字体系统、间距规格、组件规范、交互规则） |

### 4.5 design-prompt.md 文件输出

OPTIMIZE 步骤完成后，编排层 Agent SHALL 将优化后的完整提示词写入 `prototype/design-prompt.md` 文件（7 章节模板），作为 DESIGN 步骤的**唯一真相源**：

### 文件路径

`docs/changes/{change}/prototype/design-prompt.md`

### 7 章节模板

| 章节 | 标题 | 内容要求 |
|------|------|---------|
| 第一章 | 项目背景与设计目标 | 从 functional-designs/index.md 提取产品概述，明确原型范围、目标用户和设计意图 |
| 第二章 | 设计系统（Design System） | 色彩方案（主色/背景色/文字色/边框色/状态色，含颜色值）、字体系统（系统字体栈 + 标题/正文层级规格）、间距与圆角规格（页面/卡片/组件/按钮） |
| 第三章 | 菜单与导航结构 | 菜单树（一/二/三级菜单项及其对应页面）、导航模式（顶部导航/侧边栏/Tab Bar/面包屑）、全局组件（Header/Footer/用户头像/通知铃铛等）、每个页面标注对应的原型文件名 |
| 第四章 | 页面详细规格 | 逐页穷举：布局分区（ASCII 线框图）、按钮清单（名称/位置/样式/触发/前置条件）、表单清单（表单名/字段详情/提交行为）、数据展示区（类型/字段/交互）、状态覆盖（加载/空/错误/边界态）、弹窗/抽屉（触发/内容/关闭方式） |
| 第五章 | 业务流程脚本 | 至少一个完整端到端业务流程脚本，每步明确"用户在[哪个页面] → 点击[哪个按钮] → 看到[什么变化] → 进入[哪个页面]"，覆盖从入口到最终结果的完整路径 |
| 第六章 | 硬约束 | 多文件输出约束（输出到 prototype/ 目录，index.html 为入口）、flow demo 模式约束（AppPhone 状态管理器驱动，禁止 overview 静态平铺）、离线自包含约束（禁 CDN，系统字体栈） |
| 第七章 | 高保真要求 | 参考资源索引（产品级原型/设计令牌/品牌资产路径）、交互细节规格（按钮 hover/active 态、输入框 focus 态、弹窗过渡动画、表格行 hover 态、Tab 切换动画）、响应式要求（桌面端优先/移动端基准，如有） |

### 文件元信息

文件头部 SHALL 包含：变更名称、版本号（1.0.0 起始）、生成时间、状态标记（待确认/已确认/已执行）。

## 4.6 用户确认

```
1. 编排层 Agent 完成 design-prompt.md 写入后 → 通过 AskUserQuestion 展示提示词摘要
   Question: "提示词已优化并写入 prototype/design-prompt.md，包含:
     - {n} 个页面的菜单结构
     - {m} 个页面的元素级描述（按钮/表单/数据区/状态覆盖）
     - {k} 个端到端业务流程脚本
     - 硬约束: 多文件目录 + flow demo 模式 + 离线自包含 + design-system 输出
     是否确认执行？"
   Options:
     - "确认执行" → design-prompt.md 状态更新为"已确认" → 进入 TOOLCHAIN 步骤
     - "需要修订" → 收集用户反馈 → 回到 4.1 修订 prompt
2. 用户确认后 → 进入 TOOLCHAIN 步骤
```

## 4.7 纯后端项目

当 CHECK 步骤判定原型设计自动跳过（纯后端项目）时，OPTIMIZE 步骤不执行。

---

## 6. TOOLCHAIN — 工具链选择与锁定

TOOLCHAIN 步骤负责根据 SCAN 结果组合可行工具链方案，供用户选择后锁定执行。

### 6.1 零 prototype-gen 能力阻塞

```
1. 如 SCAN 结果中 prototype-gen 角色 Skill 数量 = 0:
   - 标记阶段为 ⚠️ 阻塞
   - 输出: "未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
   - 更新 .status.md，退出
```

### 6.2 单一 prototype-gen 自动选择

```
1. 如 prototype-gen 数量 = 1:
   - 自动生成单一工具链方案
   - 直接使用该方案进入 DESIGN 步骤，不询问用户
```

### 6.3 多个 prototype-gen 推荐方案

```
1. 如 prototype-gen 数量 ≥ 2:
   - 根据扫描到的 Skill 及其角色组合生成 2-3 条工具链方案
   - 每条方案标注：包含的 Skills、流程描述、优点、缺点、适用场景
   - 通过 AskUserQuestion 展示方案供用户选择
   - 方案数量 SHALL NOT 超过 3 个
```

### 6.4 用户选定后锁定

```
1. 用户在 AskUserQuestion 中选择一种工具链方案后:
   - 将选定方案写入 docs/toolchain.md 的原型设计章节
   - 记录字段：change_name、selected_toolchain、skills_used、execution_order、decision_time、status
   - DESIGN 步骤严格按 toolchain.md 中指定的 Skill 和顺序执行
   - 系统 SHALL NOT 在执行过程中自行切换工具链
```

### 6.5 方案示例

| 方案 | 包含 Skills | 流程 | 优点 | 缺点 | 适用场景 |
|------|-----------|------|------|------|---------|
| A: 一体化 | huashu-design | 单一引擎完成风格推荐+原型生成 | 内置顾问模式+反 slop+Playwright 验证 | 仅适用于 HTML 原型 | 大多数前端变更（推荐） |
| B: 设计驱动 | ui-ux-pro-max + huashu-design | ui-ux-pro-max 输出 design-system → huashu-design 生成原型 | 更精确的设计系统输出 | 需要两个 Skill 配合 | 对设计系统要求高的场景 |
| C: 静态页面型 | ui-ux-pro-max + frontend-design | ui-ux-pro-max 推荐风格 → frontend-design 生成 HTML | 生产级代码输出 | frontend-design 不做 flow demo | 需要快速出页面的场景 |

---

## R. REVISION — 修订模式

> **版本**: 2.3.0 新增

### R.1 触发条件

修订模式有两种入口：

**入口 A: CHECK 步骤检测到已有原型**（现有机制）

CHECK 步骤检测到 `prototype/index.md` 已存在时，进入修订模式分支。修订模式下跳过 INPUT（机械提取）和 OPTIMIZE（设计转译）步骤，直接使用已有约束并合并用户修订需求。

**入口 B: code 阶段驱动回退**（新增）

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
   ├── 加载 prototype/index.md 作为现有原型清单上下文
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

现有原型存在但用户无明确修订需求时，通过 AskUserQuestion 询问：

```
Question: "原型已存在（prototype/index.md）。是否要调整？"
Options:
  - "要调整，描述修改内容" → 进入 R.3 修订模式流程
  - "查看现有原型" → 展示原型摘要，不修改，退出原型设计阶段
```

当用户输入包含修订需求（如"调整原型"、"修改设计"、"改大按钮"等）时，直接进入 R.3 修订模式流程。

### R.3 修订模式流程

```
1. 加载 prototype/index.md 作为现有原型清单上下文
2. 加载 prototype/design-prompt.md 作为已有设计约束（如存在）
3. 加载 docs/toolchain.md 作为已有工具链锁定（如存在）
4. 合并用户修订需求到 prompt 中
5. 进入 DESIGN 步骤，按已有 toolchain.md 执行
```

修订模式下不重新从 functional-designs/ 提取（跳过 INPUT），不重新生成 design-prompt.md（跳过 OPTIMIZE），不重新执行工具链选择（跳过 TOOLCHAIN）。如 design-prompt.md 不存在，基于现有原型反向生成最小约束文件。如 toolchain.md 不存在，执行一次最小化 TOOLCHAIN 扫描+选择。

### R.4 修订模式后验证

修订模式 DESIGN 步骤完成后，执行完整的 VERIFY 流程（8.1 CDN 扫描 → 8.2 交叉引用 → 8.3 导航验证 → 8.4 Playwright 验证 → 8.5 UX 规则审查 → 8.6 对比度检测 → 8.7 design-system 产物必检），与新建模式一致。验证不通过返回 DESIGN 重新修订，验证通过进入 REVIEW 用户评审循环。

修订模式用户确认通过后，§8.1 COMPLETE 步骤重新执行以下操作：
1. 更新 prototype/index.md 修订记录（版本号递增 + 追加修订行）
2. 重新提取 design-tokens.css 和 element-coverage-tree.md，覆盖旧版本
3. 若 design 阶段已填充 TC-ID，SHALL 通过 AskUserQuestion 确认是否保留已有映射

### R.5 修订模式后元素覆盖树重新生成

修订模式 REVIEW 确认通过后，§8.1 自动触发 element-coverage-tree.md 的重新提取（使用更新后的 prototype/*.html），覆盖旧版本树文件。该逻辑与新建模式一致，无需修订模式特殊处理。

---

## 7. DESIGN — 按 toolchain.md 锁定执行

DESIGN 步骤分为两个子阶段：7.1 STYLE（风格/布局推荐）和 7.2 GENERATE（按 toolchain 锁定执行）。

### 7.1 STYLE — 风格/布局推荐

```
1. 确认 prototype/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype/style-decision.md 不存在（用户未选择过风格）
3. 启动子代理执行风格/布局推荐:
   Agent(subagent_type="claude", description="执行风格推荐", prompt="读取 prototype/design-prompt.md 中的项目背景、产品类型、目标用户，推荐 3 个差异化风格方向。每个方向包含：风格名称+设计哲学描述、色彩方案（主色/背景色/文字色/强调色+色值）、字体系统（标题+正文）、布局模式、ASCII 线框图（10 行以内）、适用场景+不适用场景。")
4. 通过 AskUserQuestion 展示风格选项:
   - 选项 1/2/3: 3 个差异化风格方向（preview 含 ASCII 线框图 + 色彩方案）
   - "需要更多方向": 回到推荐步骤重新生成
   - "自行指定": 用户自由描述期望风格
5. 用户选定后写入 prototype/style-decision.md:
   - selected_style: 风格名称
   - style_description: 设计哲学 + 色彩 + 字体 + 布局
   - ascii_wireframe: ASCII 线框图
   - decision_time: 时间戳
6. style-decision.md 作为 7.2 GENERATE 步骤的输入
```

### 7.2 GENERATE — 按 toolchain 锁定执行

```
1. 确认 prototype/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype/style-decision.md 存在（STYLE 步骤产出）
3. 确认 docs/toolchain.md 存在（TOOLCHAIN 步骤产出）
4. 启动子代理:
   Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype/design-prompt.md + prototype/style-decision.md 中的完整提示词，按 docs/toolchain.md 中 execution_order 指定的设计引擎和顺序生成 HTML 交互原型到 prototype/ 目录，并输出 design-system/MASTER.md。")
   - 子代理严格按 toolchain.md execution_order 逐个调用设计引擎
   - 子代理 SHALL NOT 调用 toolchain.md 中未列出的任何设计 Skill
   - 子代理独立上下文，HTML 产物不污染主 Agent
5. 子代理完成后返回结果摘要（成功/失败、生成页面数）
6. 主 Agent 验证产物:
   - 验证 prototype/index.md 存在且包含 entry 角色文件声明
   - 验证清单中声明的所有文件路径对应的实际文件存在且非空
   - 验证所有内部文件引用目标文件存在
   - 验证 design-system/MASTER.md 存在
7. 子代理失败处理:
   - 重试一次子代理调用
   - 重试仍失败 → ⚠️ 阻塞，提示用户
   - SHALL NOT 自行切换到 toolchain.md 中未列出的其他 Skill
```

**强制要求**：flow demo 模式——设计引擎 SHALL 使用单台设备状态管理器（如 `AppPhone`），用户可通过点击 tab bar / 按钮 / 标注点完成完整业务流程。SHALL NOT 仅提供多屏并排静态展示（overview 平铺）。

`kflow-prototype-design` 不干预设计引擎内部迭代过程。

---

## 8. VERIFY — CDN 扫描 + 交叉引用 + 导航验证 + Playwright + UX 审查 + 对比度检测 + design-system 产物必检

### 执行顺序

```
8.1 CDN 扫描 → 8.2 交叉引用 → 8.3 导航验证(5轮) → 8.4 Playwright(5轮) → 8.5 UX 规则审查(5轮) → 8.6 对比度检测 → 8.7 design-system 产物必检
前置依赖: CDN 扫描不通过不继续后续步骤
每轮子代理串行: 前一轮完成 → 主 Agent 读取报告 → 修复 → 下一轮
```

### 6.1 CDN 外部依赖扫描

```
1. 扫描 prototype/ 目录下所有 .html 文件
2. Grep 检测 http:// 或 https:// 模式的外部资源引用
   - <link href="http..."> → 违规
   - <script src="http..."> → 违规
   - <img src="http..."> → 违规
   - @import url(http...) → 违规
3. 若发现外部依赖:
   - 在验证报告中列出违规文件和具体引用
   - 标记验证不通过 → 返回 DESIGN 步骤修复
4. 若 CDN 扫描通过 → 记录"离线自包含检查通过"
```

### 6.2 多文件交叉引用完整性检查

```
1. 提取 index.html 中所有内部引用目标（<a href="page-*.html">、<iframe src="page-*.html"> 等）
2. 验证每个引用目标文件在 prototype/ 目录下存在
3. 若发现孤立引用 → 在验证报告中列出 → 返回 DESIGN 步骤修复
```

### 6.3 导航合理性验证（新增，5 轮子代理串行）

CDN 扫描和交叉引用检查通过后，执行 5 轮导航合理性验证，每轮启动一个独立子代理执行全部 5 项检查。

#### 每轮子代理启动

```
主 Agent → Agent(subagent_type="claude", description="导航合理性验证 Round {N}", prompt="...")
每轮子代理执行全部 5 项检查 → 输出报告 → 主 Agent 读取 → 修复 → 下一轮
```

#### 每轮 5 项检查

| # | 检查项 | 内容 |
|---|--------|------|
| 1 | 页面可达性 | 从 `index.html` 出发 BFS 遍历所有 `<a href>` 和导航组件引用，生成可达性矩阵，标记孤立页面和死胡同页面 |
| 2 | 返回/取消按钮合理性 | 穷举所有"返回""取消""关闭"按钮，验证目标页面是其语义父页面（详情→列表、表单取消→进入前页面、弹窗关闭→上下文不变），标记语义不合理的返回目标 |
| 3 | 表单切换链 | 验证多步表单的"上一步/下一步"链条完整，提交成功后去向明确且合理，提交失败后留在当前页并保留已填数据，标记断链或去向不明确的表单 |
| 4 | 弹窗/抽屉导航 | 验证每个弹窗/抽屉的触发方式正确、所有关闭方式可用（确认/取消/点击遮罩/Esc）、嵌套层级关系和逐层关闭，标记关闭后上下文错乱的情况 |
| 5 | 跨页面流程闭环 | 按业务流程脚本逐条走通完整导航路径，验证从入口到终点能回到起点（闭环），无"跳进去出不来"的页面序列，标记流程断点 |

#### 验证报告

每轮子代理输出报告到 `prototype/nav-check-round-{N}.md`（N 为轮次 1-5），包含 5 项检查各自的结果、发现问题和建议修复。

#### 强制执行规则

- SHALL 完成全部 5 轮，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 5 轮

### 6.4 Playwright 全覆盖验证（升级，5 轮子代理串行）

导航合理性验证完成后，执行 5 轮 Playwright 全覆盖验证，每轮启动一个独立子代理执行全部 5 项检查。

#### 工作目录约束

子代理工作目录 SHALL 固定为项目根目录。原型 HTML 文件通过 `docs/changes/{change}/prototype/index.html` 相对项目根路径引用。Playwright SHALL 使用 `.kflow-runtime/playwright/` 下的隔离安装。SHALL NOT 在 `prototype/` 目录下执行 `npm install` 或 `npx playwright`。

#### 每轮子代理启动

```
主 Agent → Agent(
  subagent_type="claude",
  description="Playwright 验证 Round {N}",
  prompt="工作目录固定为项目根目录。使用 /playwright-cli 打开 docs/changes/{change}/prototype/index.html（相对项目根路径），执行全部 5 项检查..."
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
| 5 | 端到端业务流程 | 按 `prototype/design-prompt.md` 中定义的业务流程脚本逐条走通，验证无 JS 错误、无交互断点、无死胡同，输出流程通过清单 |

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

每轮子代理输出报告到 `prototype/playwright-check-round-{N}.md`（N 为轮次 1-5），包含 5 项检查各自的结果、pageerror 统计、发现问题和建议修复。

#### 强制执行规则

- SHALL 完成全部 5 轮，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 5 轮

### 8.5 UX 规则审查（新增，5 轮子代理串行）

Playwright 验证完成后，执行 5 轮 UX 规则审查，每轮启动一个独立子代理执行精简核心规则集审查。

#### 精简核心规则集（20-30 条）

子代理读取 prototype/ 目录下所有 HTML 文件，逐条检查以下核心规则：

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

每轮子代理输出报告到 `prototype/ux-check-round-{N}.md`（N 为轮次 1-5），包含检查项逐条结果、发现问题和建议修复。

#### 强制执行规则

- SHALL 完成全部 5 轮，不允许提前终止
- 如果环境中存在 ui-ux-pro-max，其完整 99 条 UX 规则库作为"可选增强"并行执行

### 8.6 对比度检测

UX 规则审查完成后，执行对比度检测：

```
1. 扫描 prototype/ 目录下所有 .html 文件
2. 提取所有文本颜色对（背景色 + 前景色）
3. 使用 WCAG 相对亮度计算公式:
   - 相对亮度 L = 0.2126 * R + 0.7152 * G + 0.0722 * B（sRGB 线性化）
   - 对比度 = (L1 + 0.05) / (L2 + 0.05)，L1 > L2
4. 标记对比度 < 4.5:1 的颜色对（不满足 WCAG AA）
5. 输出报告到 prototype/contrast-check.md:
   - 所有检测到的颜色对及其对比度值
   - 标记 ⚠️ 不达标的颜色对
   - 建议替代色值
```

### 8.7 design-system/MASTER.md 产物必检

```
1. 验证 design-system/MASTER.md 文件存在
2. 验证文件包含以下必需章节:
   - 色彩方案（含色值）
   - 字体系统（标题 + 正文字体）
   - 间距规格
   - 组件规范
   - 交互规则
3. 如产物缺失 → ⚠️ 阻塞并提示用户
4. 如产物存在 → 记录"design-system 检查通过"
```

---

## 9. REVIEW — 用户评审循环

通过 AskUserQuestion 进行用户评审：

```
Question: "HTML 原型已完成，覆盖 {n} 个屏幕、{m} 个 UI 功能点。
[CDN 扫描: {通过/不通过}]
[交叉引用: {通过/不通过}]
[导航合理性验证: 5 轮完成，发现并修复 {x} 个问题]
[Playwright 验证: 5 轮完成 / 降级为手动检查，发现并修复 {y} 个问题]
[UX 规则审查: 5 轮完成，发现并修复 {a} 个问题]
[对比度检测: {通过/不通过}]
[design-system 产物: {存在/缺失}]
[10轮自审: 已完成（重复制），发现并修复 {z} 个问题]
是否确认通过？"
Options:
  - "确认通过" → 原型满足需求，进入详细设计
  - "需要修订" → 收集反馈 → 回到 DESIGN 步骤
```

### 循环机制

```
DESIGN(子代理委托) → VERIFY(CDN+交叉引用+导航5轮+Playwright5轮) → SELFREV(10轮) → REVIEW
  ├── 确认通过 → COMPLETE
  └── 需修订 → 收集用户反馈 → 回到 DESIGN（再次启动子代理调用 huashu-design，附修订要求）
```

### 评审结果处理

| 用户选择 | 阶段状态 | 评审记录 | 后续动作 |
|---------|---------|---------|---------|
| 确认通过 | ✅ 完成 | ✅ 已确认 | 门控释放，可进入详细设计 |
| 需要修订 | ⚠️ 需修订 | ⚠️ 需修订 | 保持原型设计阶段，根据用户反馈修订原型 |

---

## 8. COMPLETE — 更新状态文件 + 创建 index.md + 自动生成元素覆盖树

Update `docs/changes/{change}/.status.md`:

1. Mark prototype design phase: `✅ 完成` (or `⏭️ 跳过`)
2. Record user review result in user review table
3. Set current phase to `详细设计`
4. Record completion time and execution notes

### 8.0 创建/更新 prototype/index.md（用户确认通过后执行）

```
1. 检查 prototype/index.md 是否存在
2. 若不存在 → 按模板创建（含原型文件清单、页面清单、设计系统引用、修订记录）
3. 若已存在（修订模式）→ 更新修订记录：
   ├── 版本号递增（semver）
   └── 追加修订记录行
4. 更新原型文件清单和页面清单以反映当前原型状态
```

### 8.1 原型通过后自动提取设计令牌和元素覆盖树（用户确认通过后执行）

当用户在 REVIEW 步骤中"确认通过"后，系统 SHALL 从实际原型 HTML 文件中自动提取设计令牌和元素覆盖树：

#### 提取 design-tokens.css

```
1. 扫描 prototype/ 目录下所有 .html 文件
2. 提取 :root { ... } 中的 CSS 变量声明
3. 提取内联 style 中出现的颜色值、font-size、border-radius、box-shadow 等样式值
4. 去重、排序、归类后输出到 prototype/design-tokens.css
5. 文件头部标注: 提取来源（原型版本、生成时间、自动提取）
```

#### 提取 element-coverage-tree.md

```
1. 从 prototype/ 目录下所有 .html 文件中解析 DOM 树
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
6. 输出 prototype/element-coverage-tree.md（初始版，TC-ID 列为空）
7. 文件头部标注: 生成时间戳和来源（prototype-design 阶段自动生成）
```

> **说明**: 废弃 `prototype/element-spec.md` 和 `prototype/nav-tree.md`，其信息由 `element-coverage-tree.md` 统一承载。页面导航结构合并到树的 📄 页面节点层，元素清单合并到树的 🔘/📝/📊 元素节点层。

#### 原型迭代后重新生成

当原型设计阶段用户确认通过后又进入修订循环，新一轮用户确认通过后，重新执行 design-tokens.css 和 element-coverage-tree.md 的提取，覆盖旧版本文件。若 design 阶段已填充 TC-ID，SHALL 通过 AskUserQuestion 确认是否保留已有映射。

#### 用户跳过原型设计时不生成

当原型设计阶段被跳过（⏭️ 跳过）时，系统不生成 design-tokens.css 和 element-coverage-tree.md。后续 code 和 code-review 阶段不执行原型对账。后续 design 阶段按路径 B（playwright-cli 探索）生成元素覆盖树。

---

## 跳过条件

| 条件 | 处理 |
|------|------|
| 纯后端项目 | 自动跳过，标记 ⏭️ 跳过 |
| functional-designs/ 中无前端/UI 功能点 | 自动跳过，标记 ⏭️ 跳过 |
| 用户在 AskUserQuestion 中拒绝 | 跳过，标记 ⏭️ 跳过 |
| prototype-gen 角色 Skill 数量 = 0 | ⚠️ 阻塞，提示安装 huashu-design 或 frontend-design，不跳过 |

---

## 10 轮自审

> **版本**: 2.0.0 新增

### 概述

原型设计阶段在 huashu-design 委托执行完成后、用户评审确认之前，强制执行 10 轮自循环审查。自审由当前 Agent 执行，不启动独立审查 Agent。

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

> **v2.2.0 变更**: 从"分工制"（每轮只审查部分维度）改为"重复制"——每轮独立执行全部四个维度（覆盖性+一致性+可用性+完整性），10 轮形成自然收敛。

| 对比维度 | 分工制（旧） | 重复制（新） |
|---------|------------|------------|
| 每轮范围 | 部分维度 | 全部维度 |
| 发现问题 | 后期才暴露其他维度问题 | 早期就暴露各类问题 |
| 收敛性 | 不明显 | 自然收敛（后期问题越来越少） |
| 独立性 | 维度间串行 | 每轮独立完整审查 |

### 自审流程

```
10 轮自审执行流程（重复制）:

1. 记录开始时间（作为时间戳）
2. 按覆盖性、一致性、可用性、完整性四个维度逐项检查（覆盖性为第一优先级）
3. 发现问题 → 立即修复
4. 生成自审报告 → 保存到 self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md
5. 进入下一轮
6. 每轮均执行全部四个维度的完整检查
7. 重复直至完成全部 10 轮
8. 全部完成后进入用户评审确认
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

- SHALL 完成全部 10 轮自审，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 10 轮
- 自审全部完成后进入用户评审确认（AskUserQuestion），释放 design 阶段门控

---

## 与其他 Skill 的关系

- **输入来自**：`kflow-explore`（设计探索阶段）
- **输出给**：`kflow-design`（详细设计阶段）
- **前置阶段**：设计探索
- **后续阶段**：详细设计（原型设计完成后或跳过后）
- **委托执行**：按 `docs/toolchain.md` 锁定的设计引擎（huashu-design / frontend-design / 其他），不可用时硬阻塞
- **归档合并**：`kflow-archive` 将变更原型合并到 `docs/prototype/`

---

## 阶段边界约束

### 域内内容（prototype 负责）

| 内容类别 | 说明 |
|---------|------|
| UI 原型页面 | 基于 functional-designs/ 的页面定义生成多文件 HTML 原型（`prototype/` 目录，`index.html` 为入口） |
| 交互流程 | 基于功能设计中的可执行操作和业务流程设计交互，使用 flow demo 模式（完整可交互路径） |
| 视觉风格 | 统一的视觉风格、组件命名、页面布局模式 |
| 交互状态 | 加载态、空态、错误态、边界态等完整状态覆盖 |
| 表单组件 | 基于功能设计中的表单项定义（字段名/类型/校验规则/默认值）生成对应表单组件 |
| 离线自包含 | 所有资源内联或相对路径引用，禁 CDN 外部依赖，系统字体栈 |

### 域外内容（禁止）

| 内容类别 | 说明 | 应由哪个阶段处理 |
|---------|------|----------------|
| 功能决策 | 新增/删除/修改功能点定义 | explore（回退） |
| 业务规则修改 | 修改功能设计中的业务规则 | explore（回退） |
| 技术实现决策 | 技术架构、接口设计、数据模型 | design |
| 代码实现 | 任何代码文件 | code |

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
