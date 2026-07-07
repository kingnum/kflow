---
name: kflow-prototype-design
version: 0.16.0
description: Use when user needs prototype design/原型设计、UI 设计、交互设计、HTML 原型 for frontend changes. 编排层，动态扫描环境设计 Skills，组合工具链方案供用户选择，选定后锁定执行。可选阶段，仅涉及前端/UI 变更时推荐使用。含用户评审循环、5 轮导航合理性验证、5 轮 Playwright 全覆盖验证、UX 规则审查、对比度检测、CDN 离线扫描、多文件交叉引用检查。含 PRE_HOOK/POST_HOOK 阶段钩子引用。
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

原型设计编排层。采用「编排层 → 子代理执行引擎」架构模型——**不做具体原型制作**（通过子代理委托 huashu-design 执行），只做阶段门控、上下文组装、提示词优化（含 design-prompt.md 文件输出 + 用户确认）、子代理委托调用、验证（CDN 扫描 + 交叉引用 + 5 轮导航验证 + 5 轮 Playwright 全覆盖验证）和用户评审。

> **设计决策**：huashu-design 是一套持续更新的完整 Skill（60KB+ SKILL.md + assets/ + scripts/ + references/），通过子代理委托调用而非在主 Agent 上下文直接调用，避免 HTML 产物污染主 Agent 上下文、内容膨胀和 Token 浪费。

> **v2.2.0 重要变更**：DESIGN 改为子代理委托调用、VERIFY 升级为 5 轮全覆盖验证（导航+Playwright）、OPTIMIZE 新增 design-prompt.md 文件输出、SELFREV 改为重复制。

# 任务

```
门控检查（含 prototype-gen 角色可用性硬拦截）
  → SCAN: 环境扫描设计 Skills → 角色分类（新增）
  → 评估是否需要原型（AskUserQuestion 确认）
  → 机械组装 prompt 上下文（功能设计 + 产品级上下文 + 品牌资产）
  → 提示词优化（菜单树 + 页面元素穷举 + 业务流程脚本 + 硬约束注入）+ 输出 design-prompt.md + 用户确认
  → TOOLCHAIN: 多方案推荐 → AskUserQuestion 选择 → 锁定 docs/toolchain.md（新增）
  → 5.1 STYLE: 子代理推荐 3 个差异化风格方向 → 用户选择 → style-decision.md（新增）
  → 5.2 GENERATE: 子代理按 toolchain.md 锁定执行，生成 HTML 原型 + design-system/MASTER.md
  → CDN 扫描 + 交叉引用检查 + 5 轮导航验证 + 5 轮 Playwright 验证
  → 5 轮 UX 规则审查 + 对比度检测 + design-system 产物必检（新增）
  → 10 轮自审（重复制：每轮全 4 维度）
  → 用户评审循环（AskUserQuestion）
  → 更新状态文件
```

# 架构模型

```
kflow-prototype-design (编排层)
├── 阶段门控 + 状态管理 + 用户评审
├── 产品级上下文加载（docs/prototype/）
├── prompt 上下文组装（INPUT：机械提取层）
├── prompt 优化（OPTIMIZE：设计转译层 + design-prompt.md 文件输出 + 用户确认）
├── Agent(subagent) 子代理 → Skill("huashu-design") 执行引擎
│   └── 子代理独立上下文，读取 design-prompt.md，调用 huashu-design
├── 验证: CDN 扫描 + 交叉引用 + 5轮导航验证(子代理) + 5轮Playwright(子代理)
└── 用户评审循环（确认/修订循环）
```

# 门控检查

进入原型设计阶段前 SHALL 检查：

| 门控项 | 检查方式 | 不满足时的处理 |
|--------|---------|--------------|
| `.status.md` 存在 | Read | 终止，提示需要先执行 kflow-explore |
| 设计探索状态 = ✅ 完成 | 检查 `.status.md` | 终止，提示需要完成设计探索 |
| `functional-designs/index.md` 存在 | Read/Glob | 终止，提示需要完成功能设计 |
| 存在前端/UI 相关功能点 | 扫描 functional-designs/ | 自动跳过，标记 ⏭️ 跳过 |
| 项目类型为纯后端 | 检查 `.status.md` 项目类型 | 自动跳过，标记 ⏭️ 跳过 |
| **prototype-gen 角色 Skill 可用** | 扫描 `.claude/skills/` | ⚠️ 硬阻塞，扫描 huashu-design / frontend-design 等，提示安装命令，退出 |

### prototype-gen 角色可用性检查详情

```
1. 扫描 .claude/skills/ 中所有设计相关 Skills（读取 name + description）
2. 按角色分类: prototype-gen（能生成 HTML 原型，如 huashu-design、frontend-design）/ design-system / ux-review / code-gen
3. prototype-gen 数量 = 0 → ⚠️ 阻塞:
   ├── 提示用户: "未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
   ├── 标记阶段为 ⚠️ 阻塞 in .status.md
   └── 退出（不继续执行）
4. prototype-gen 数量 = 1 → ✅ 单一方案，自动选择
5. prototype-gen 数量 ≥ 2 → ✅ 多方案，进入 TOOLCHAIN 步骤推荐
```

# 输入要求

| 输入 | 图例 | 说明 |
|------|------|------|
| functional-designs/ | ✅ 必须 | 设计探索阶段输出，提取项目背景和 UI 功能点清单 |
| docs/prototype/ | 🔶 条件 | 产品级已有原型目录，存在时作为设计约束加载 |
| docs/prototype/design-tokens.css | 🔶 条件 | 已有设计令牌，存在时纳入设计约束 |
| docs/prototype/screens/ | 🔶 条件 | 已有屏幕清单，存在时作为新屏幕的导航锚点 |
| docs/prototype/index.html | 🔶 条件 | 产品级全貌原型，新屏幕需能挂入其导航 |
| brand-spec.md | 🔶 条件 | 品牌资产文件，涉及品牌感知时纳入 prompt |

> **图例说明**：✅ 必须 ＝ 不可或缺的前置输入；🔶 条件 ＝ 满足特定条件时需要；⏭️ 跳过 ＝ 被跳过的阶段，产物不存在。

# 输出产物

| 产物 | 文件 | 图例 | 内容要求 |
|------|------|------|---------|
| 提示词文件 | `docs/changes/{change}/prototype/design-prompt.md` | ✅ 必须 | 7 章节完整提示词文件（项目背景、设计系统、菜单导航、页面规格、业务流程脚本、硬约束、高保真要求），DESIGN 步骤的唯一真相源，含元信息头部（变更名称/版本号/生成时间/状态标记） |
| 原型索引 | `docs/changes/{change}/prototype/index.md` | ✅ 必须 | 原型产物清单（Prototype Manifest）：产物组织方式、原型文件清单（含角色列：entry/page/tokens/coverage/shared/process）、页面清单（页面-文件映射）、设计系统引用、共享资源清单、修订记录。版本号 1.0.0 起始 |
| 原型文件（多文件） | `docs/changes/{change}/prototype/` 目录（`index.html` 为入口） | ✅ 必须 | 多文件 HTML 交互原型，`index.html` 为访问入口，可包含 `page-*.html` 独立页面文件及 `shared/` 共享资源子目录。所有文件离线自包含 |
| CDN 扫描与交叉引用报告 | `docs/changes/{change}/self-reviews/prototype/cdn-crossref-check/report.md` | ✅ 必须 | CDN 外部依赖扫描结果 + 多文件交叉引用完整性检查合并报告 |
| 导航验证报告 | `docs/changes/{change}/self-reviews/prototype/nav-check/round-{1..5}.md` | ✅ 必须 | 5 轮导航合理性验证报告（页面可达性矩阵、返回/取消按钮语义验证、表单切换链完整性、弹窗/抽屉导航检查、跨页面流程闭环验证） |
| Playwright 验证报告 | `docs/changes/{change}/self-reviews/prototype/playwright-check/round-{1..5}.md` | 🔶 条件 | 5 轮 Playwright 全覆盖验证报告（页面可达性扫描、按钮/链接全覆盖清单、表单全覆盖清单、弹窗/抽屉全覆盖清单、端到端流程通过清单）或降级说明 |
| 自审报告 | `docs/changes/{change}/self-reviews/prototype/` | ✅ 必须 | 10 轮自审报告（重复制），文件名格式：`{YYYYMMDD}-{HHMMSS}.md` |
| 用户评审记录 | `docs/changes/{change}/.status.md`（用户评审记录表） | ✅ 必须 | 原型设计评审状态、评审时间、备注 |

> **产物位置**：`docs/changes/{change}/prototype/` 目录（变更级目录下）。

### 多文件架构示例

```
prototype/
├── index.html              ← 入口：导航/聚合/流程起点
├── page-login.html         ← 登录页
├── page-dashboard.html     ← 仪表盘
├── page-detail.html        ← 详情页
├── page-form.html          ← 表单页
├── shared/
│   ├── styles.css          ← 共享样式
│   ├── components.js       ← 共享组件
│   └── app-phone.js        ← AppPhone 状态管理器
└── verify-report.md
```

# 执行流程

## 总流程

```
原型设计阶段流程:

┌──────────────────────────────────────────────────────────────────┐
│                    PROTOTYPE WORKFLOW (v2.2)                      │
├──────────────────────────────────────────────────────────────────┤
│  1. PRE_HOOK  → 引用 skills/kflow-prototype-design/references/hooks.md prototype-design 阶段 PRE_HOOK │
│  2. CHECK     → 门控检查 + prototype-gen 可用性硬拦截 + 修订模式检测 │
│  │   ├── 检测 prototype/index.md 是否存在（入口 A: 用户驱动修订）    │
│  │   └── 检测是否从 code 阶段回退（入口 B: code 阶段驱动回退）       │
│  3. ASSESS    → 评估是否需要原型设计（AskUserQuestion）           │
│  4. INPUT     → 机械组装 prompt 上下文（分层: 必然/条件）         │
│  │   ├── 必然存在: functional-designs/ 提取背景+UI功能点          │
│  │   ├── 条件存在: docs/prototype/ 产品级已有原型                │
│  │   └── 条件存在: brand-spec.md 品牌资产                        │
│  5. OPTIMIZE  → 深度分析设计 + 文件输出 + 用户确认                │
│  │   ├── 5.1 提取菜单树（一/二/三级菜单 → 对应页面）             │
│  │   ├── 5.2 穷举页面元素（布局/按钮/表单/数据区/弹窗/状态）     │
│  │   ├── 5.3 编写业务流程脚本（逐步用户操作路径）                │
│  │   ├── 5.4 注入硬约束（多文件+flow demo+离线自包含）           │
│  │   ├── 5.5 输出 design-prompt.md（7 章节模板）                │
│  │   └── 5.6 AskUserQuestion 用户确认（确认执行 / 需修订）       │
│  6. DESIGN    → Agent(subagent) 子代理委托调用 huashu-design      │
│  │   └── 子代理读取 prototype/design-prompt.md → 调用 Skill      │
│  │   └── 子代理独立上下文，HTML 不污染主 Agent                    │
│  7. VERIFY    → CDN 扫描 + 交叉引用 + 导航验证 + Playwright       │
│  │   ├── 7.1 CDN 扫描: grep http:// https:// → 不通过           │
│  │   ├── 7.2 交叉引用: 验证所有内部文件引用目标文件存在           │
│  │   ├── 7.3 导航验证: 5 轮子代理串行（每轮全 5 项检查）        │
│  │   ├── 7.4 Playwright: 5 轮子代理串行（每轮全 5 项检查）      │
│  │   ├── 7.5 UX 规则审查: 5 轮子代理串行                         │
│  │   ├── 7.6 对比度检测                                          │
│  │   └── 7.7 design-system 产物必检                              │
│  7.5 BROWSER_CLEANUP → playwright-cli kill-all 清理浏览器进程     │
│  8. SELFREV   → 10 轮自审（子代理串行 + 重复制: 每轮全 4 维度）   │
│  9. REVIEW    → AskUserQuestion 用户评审（确认/修订循环）         │
│  │   ├── 确认通过 → COMPLETE                                     │
│  │   └── 需修订   → 收集反馈 → 回到 DESIGN                       │
│ 10. COMPLETE  → 更新状态文件，记录评审结果                        │
│ 11. POST_HOOK → 引用 skills/kflow-prototype-design/references/hooks.md prototype-design 阶段 POST_HOOK（含 BROWSER_CLEANUP + UPDATE_STATE） │
└──────────────────────────────────────────────────────────────────┘
```

## 步骤 1：PRE_HOOK — 阶段前置钩子

引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 PRE_HOOK（🔶 浏览器类型：CHECK_STATE + RELOAD）。

## 步骤 2：CHECK — 门控检查 + huashu-design 可用性硬拦截

```
1. Read docs/changes/{change}/.status.md
2. 检查: 设计探索状态 = ✅ 完成
3. 检查: functional-designs/index.md 存在
4. 提取 .status.md 中的项目类型
5. 如项目类型 = 纯后端 → 自动跳过（标记 ⏭️ 跳过，退出）
6. 扫描 functional-designs/ 中是否有 UI 功能点
7. 如无 UI 功能点 → 自动跳过（标记 ⏭️ 跳过，退出）
8. 检查 huashu-design 可用性（见上方门控检查详情）
```

## 步骤 3：ASSESS — 评估是否需要原型设计

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

## 步骤 4：INPUT — 机械组装 Prompt 上下文

本步骤为 OPTIMIZE 步骤提供原始数据输入。按存在性分层组装基础 prompt 数据：

```
✅ 必然存在（前置阶段产物）:
  ├── functional-designs/index.md      → 提取产品概述
  ├── functional-designs/part-NN.md    → 提取 UI 功能点清单
  └── 产出路径: docs/changes/{change}/prototype/ 目录

🔶 条件存在（看项目历史 + 变更类型）:
  ├── docs/prototype/design-tokens.css → 已有设计令牌
  ├── docs/prototype/screens/          → 已有屏幕清单
  ├── docs/prototype/index.html        → 产品级全貌原型
  └── brand-spec.md                    → 品牌资产（涉及品牌时）
```

INPUT 产出为基础数据包，传递给 OPTIMIZE 步骤进行设计转译。

## 步骤 5：OPTIMIZE — 提示词优化与用户确认

在委托 huashu-design 之前，编排层 Agent SHALL 深度分析 functional-designs/ 产出优化后的设计 prompt，并通过 AskUserQuestion 展示给用户确认。

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

### 4.3 业务流程脚本

SHALL 包含至少一个完整的端到端业务流程脚本，为 huashu-design 提供 flow demo 的执行路径：

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

### 4.4 硬约束注入

优化后的 prompt SHALL 注入以下硬约束：

| 约束类别 | 具体内容 |
|---------|---------|
| **多文件输出** | 输出到 `docs/changes/{change}/prototype/` 目录，允许多文件结构，`index.html` 为入口，可包含 `page-*.html` 独立页面及 `shared/` 子目录 |
| **业务流程驱动** | 使用 **flow demo 模式**（可交互业务流程，单台设备状态管理器如 `AppPhone` 驱动），SHALL NOT 仅提供 overview 多屏并排静态展示 |
| **离线自包含** | 所有 CSS/JS/字体/图片资源必须内联或相对路径引用；禁止 `http://` `https://` 外部 CDN 依赖；字体使用系统默认字体栈（如 `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`） |

### 4.5 design-prompt.md 文件输出

OPTIMIZE 步骤完成后，编排层 Agent SHALL 将优化后的完整提示词写入 `docs/changes/{change}/prototype/design-prompt.md` 文件（7 章节模板），作为 DESIGN 步骤的**唯一真相源**。

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
| 六 | 硬约束 | 多文件输出（prototype/ 目录，index.html 入口）、flow demo 模式（AppPhone 驱动，禁 overview）、离线自包含（禁 CDN，系统字体栈） |
| 七 | 高保真要求 | 参考资源索引、交互细节规格（hover/active/focus/过渡动画/Tab 切换）、响应式要求 |

### 4.6 用户确认

```
1. 编排层 Agent 完成 design-prompt.md 写入后
2. 通过 AskUserQuestion 向用户展示提示词摘要:
   Question: "提示词已优化并写入 prototype/design-prompt.md，包含:
     - {n} 个页面的菜单结构
     - {m} 个页面的元素级描述（按钮/表单/数据区/状态覆盖）
     - {k} 个端到端业务流程脚本
     - 硬约束: 多文件目录 + flow demo 模式 + 离线自包含
     是否确认执行？"
   Options:
     - "确认执行" → 更新 design-prompt.md 状态为"已确认" → 进入步骤 5（DESIGN）
     - "需要修订" → 收集用户反馈 → 回到 4.1 修订
3. 用户确认后 → 进入 DESIGN 步骤
```

### 4.7 跳过条件

当 CHECK 步骤判定原型设计自动跳过（纯后端项目 / 无 UI 功能点）时，OPTIMIZE 步骤不执行。

## 步骤 6：DESIGN — 按 toolchain.md 锁定执行

> **子代理隔离规则**：子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管原型生成。最多重试 3 次（1 次初始 + 3 次重试），全部失败后标记 ⚠️ 阻塞并提示用户。重新创建的子代理不依赖前上下文。

DESIGN 步骤分为两个子阶段：5.1 STYLE（风格/布局推荐）和 5.2 GENERATE（按 toolchain 锁定执行）。

### 5.1 STYLE — 风格/布局推荐

```
1. 确认 prototype/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype/style-decision.md 不存在（用户未选择过风格）
3. 启动子代理:
   Agent(subagent_type="claude", description="执行风格推荐", prompt="读取 prototype/design-prompt.md 中的项目背景、产品类型、目标用户，推荐 3 个差异化风格方向。每个方向包含：风格名称+设计哲学描述、色彩方案、字体系统、布局模式、ASCII 线框图（10 行以内）。")
4. 通过 AskUserQuestion 展示风格选项（preview 含 ASCII 线框图 + 色彩方案）
5. 用户选定后写入 prototype/style-decision.md
```

### 5.2 GENERATE — 按 toolchain 锁定执行

```
1. 确认 prototype/design-prompt.md 存在且状态为"已确认"
2. 确认 prototype/style-decision.md 存在
3. 确认 docs/toolchain.md 存在
4. 启动子代理:
   Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype/design-prompt.md + prototype/style-decision.md 中的完整提示词，按 docs/toolchain.md 中 execution_order 指定的设计引擎和顺序生成 HTML 交互原型到 prototype/ 目录，并输出 design-system/MASTER.md。")
   - 子代理严格按 toolchain.md execution_order 调用设计引擎
   - 子代理 SHALL NOT 调用 toolchain.md 中未列出的任何设计 Skill
5. 主 Agent 验证产物:
   - 验证 prototype/index.md 存在且清单中包含 entry 角色文件
   - 验证 design-system/MASTER.md 存在
   - 验证所有内部文件引用目标文件存在
6. 子代理失败: 重试一次，仍失败 → ⚠️ 阻塞，不自行切换工具链
```

> **强制要求**：按 toolchain.md 锁定的设计引擎 SHALL 使用 flow demo 模式——单台设备状态管理器（如 `AppPhone`）。SHALL NOT 仅提供 overview 静态平铺。
>
> `kflow-prototype-design` 不干预设计引擎内部迭代过程。

## 步骤 7：VERIFY — CDN 扫描 + 交叉引用 + 导航验证 + Playwright + UX 审查 + 对比度检测 + design-system 产物必检

> **子代理隔离规则**：验证子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管验证执行。最多重试 3 次（1 次初始 + 3 次重试），全部失败后标记 ⚠️ 阻塞并提示用户。

### 验证执行顺序

```
6.1 CDN 扫描（主 Agent 直接执行）
  ↓ (CDN 不通过不继续)
6.2 交叉引用检查（主 Agent 直接执行，与 CDN 合并报告到 self-reviews/prototype/cdn-crossref-check/report.md）
  ↓
6.3 导航合理性验证（5 轮子代理串行，每轮全 5 项）
  │   报告路径: self-reviews/prototype/nav-check/round-{N}.md
  ↓ (全部 5 轮完成后)
6.4 Playwright 全覆盖验证（5 轮子代理串行，每轮全 5 项）
  │   报告路径: self-reviews/prototype/playwright-check/round-{N}.md

轮间修复: 每轮子代理完成 → 主 Agent 读报告 → 直接修复原型文件 → 下一轮
```

### 6.1 CDN 外部依赖扫描（优先执行）

```
1. 扫描 prototype/ 目录下所有 .html 文件
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

### 6.2 多文件交叉引用完整性检查（与 CDN 扫描合并报告）

```
1. 从 index.html 出发，提取所有内部文件引用:
   ├── <a href="page-*.html"> 等超链接目标
   ├── <iframe src="page-*.html"> 等嵌入目标
   └── <script src="shared/*.js"> 等本地脚本引用
2. 验证每个引用目标文件在 prototype/ 目录下实际存在
3. 若发现断链（引用目标文件不存在）→ 在报告中列出 → 返回 DESIGN 步骤修复
4. 若所有引用完整 → 记录"交叉引用检查通过"
5. 合并 CDN 扫描和交叉引用检查结果到同一报告: self-reviews/prototype/cdn-crossref-check/report.md
```

### 6.3 导航合理性验证（新增，5 轮子代理串行）

CDN 扫描和交叉引用检查通过后，执行 5 轮导航合理性验证，每轮启动独立子代理执行全部 5 项检查。

**每轮执行流程**：
```
主 Agent → Agent(
  subagent_type="claude",
  description="导航合理性验证 Round {N}",
  prompt="读取 docs/changes/{change}/prototype/ 下所有 HTML 文件，执行以下全部 5 项导航合理性检查:
    1. 页面可达性: 从 index.html 出发 BFS 遍历所有 <a href> 和导航组件引用，生成可达性矩阵，标记孤立页面和死胡同页面
    2. 返回/取消按钮合理性: 穷举所有返回/取消/关闭按钮，验证目标页面是其语义父页面（详情→列表、表单取消→进入前页面、弹窗关闭→上下文不变）
    3. 表单切换链: 验证多步表单上一步/下一步链条完整，提交成功去向明确，提交失败留在当前页保留数据
    4. 弹窗/抽屉导航: 验证每个弹窗/抽屉触发方式正确、所有关闭方式可用（确认/取消/遮罩/Esc）、嵌套层级逐层关闭
    5. 跨页面流程闭环: 按业务流程脚本逐条走通，验证从入口到终点能回到起点，无'跳进去出不来'的序列
  输出报告到 docs/changes/{change}/self-reviews/prototype/nav-check/round-{N}.md，包含每项检查的结果、发现问题和建议修复。"
)
→ 子代理返回报告
→ 主 Agent 读取 nav-check-round-{N}.md
→ 发现问题 → 直接修复原型文件
→ 修复完成 → 进入下一轮
```

**强制执行规则**：
- SHALL 完成全部 5 轮，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 5 轮

### 6.4 Playwright 全覆盖验证（升级，5 轮子代理串行）

导航合理性验证全部 5 轮完成后，执行 5 轮 Playwright 全覆盖验证，每轮启动独立子代理执行全部 5 项检查。

**每轮执行流程**：
```
主 Agent → Agent(
  subagent_type="claude",
  description="Playwright 验证 Round {N}",
  prompt="工作目录固定为项目根目录。使用 /playwright-cli 打开 docs/changes/{change}/prototype/index.html（相对项目根路径），执行以下全部 5 项 Playwright 验证:
    1. 页面可达性: 从 index.html 出发 BFS 遍历所有 <a> 链接，每个页面验证加载成功且 pageerror=0
    2. 按钮/链接全覆盖: 穷举每个页面所有 <button> 和 <a>，逐个点击验证有响应，disabled 验证不可点击
    3. 表单全覆盖: 每个表单执行空提交（校验提示正确）+ 合法提交（行为正确）+ 取消/重置
    4. 弹窗/抽屉全覆盖: 每个弹窗/抽屉验证所有打开方式和所有关闭方式（确认/取消/遮罩/Esc）
    5. 端到端业务流程: 按 design-prompt.md 中业务流程脚本逐条走通，验证无 JS 错误、无断点、无死胡同
  Playwright 使用 .kflow-runtime/playwright/ 下的隔离安装。SHALL NOT 在 prototype/ 目录下执行 npm install 或 npx playwright。
  输出报告到 docs/changes/{change}/self-reviews/prototype/playwright-check/round-{N}.md，包含每项检查结果、pageerror 统计、发现问题和建议修复。"
)
→ 子代理返回报告
→ 主 Agent 读取 playwright-check-round-{N}.md
→ 发现问题 → 直接修复原型文件
→ 修复完成 → 进入下一轮
```

**Playwright 不可用降级**：
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

**强制执行规则**：
- SHALL 完成全部 5 轮，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 5 轮

### 6.5 UX 规则审查（新增，5 轮子代理串行）

Playwright 验证完成后，执行 5 轮 UX 规则审查，每轮启动独立子代理执行精简核心规则集（20-30 条）：对比度 ≥4.5:1、触摸目标 ≥44px、表单 label 非 placeholder-only、按钮视觉反馈、弹窗关闭方式、错误恢复路径、必填标记、空态引导、加载态 skeleton、导航层级 ≤3、内联验证、主操作突出、无水平滚动溢出、文字 ellipsis 截断、图片 alt/aria-label、焦点状态可见、无自动播放、正确 input-type、破坏性操作确认、Toast 自动消失 3-5s。

报告路径: `self-reviews/prototype/ux-check/round-{N}.md`

### 6.6 对比度检测

```
1. 扫描 prototype/ 目录下所有 .html 文件
2. 提取所有文本颜色对（背景色 + 前景色）
3. 使用 WCAG 相对亮度计算公式: L = 0.2126*R + 0.7152*G + 0.0722*B
4. 对比度 = (L1+0.05)/(L2+0.05)
5. 标记 <4.5:1 的颜色对
6. 输出报告到 self-reviews/prototype/contrast-check.md
```

### 6.7 design-system/MASTER.md 产物必检

```
1. 验证 design-system/MASTER.md 存在
2. 验证包含: 色彩方案、字体系统、间距规格、组件规范、交互规则
3. 缺失 → ⚠️ 阻塞并提示用户
```

## 步骤 7.5：BROWSER_CLEANUP — 清理浏览器进程

在 VERIFY 步骤完成后、SELFREV 步骤开始前，清理浏览器进程：

```
playwright-cli kill-all
```

> 清理 VERIFY 步骤（Playwright 验证）残留的浏览器进程，释放系统资源。

## 步骤 8：SELFREV — 10 轮自审（子代理串行 + 重复制）

### 子代理上下文文件加载（基础层 + 创意层）

自审子代理 prompt 中 SHALL 包含以下 kflow-shared 文件：

- skills/kflow-prototype-design/references/state-values.md（摘要）
- skills/kflow-prototype-design/references/gates.md（当前阶段相关门控）
- skills/kflow-prototype-design/references/self-review.md

> **子代理隔离规则**：自审子代理异常时 MUST 重新创建（新 Agent 调用），主代理 SHALL NOT 接管自审执行。最多重试 3 次，全部失败后标记 ⚠️ 阻塞并提示用户。

在 VERIFY 步骤完成后、用户评审确认之前，强制执行 10 轮自循环审查。自审由子代理（Agent subagent）串行执行，与 VERIFY 子代理模式对齐但审查范围不同（SELFREV 侧重维度级审查+边审边修，VERIFY 侧重具体检查项+出报告）。

> **v2.3.0 变更**: 自审执行方式从"当前 Agent 自身执行"改为"子代理（Agent subagent）串行执行"，每轮启动独立子代理，与 VERIFY 子代理模式对齐。

### 自审模式：子代理串行 + 重复制

> **v2.2.0 变更**: 从"分工制"改为"重复制"——每轮独立执行全部四个维度，10 轮形成自然收敛。

| 对比 | 分工制（旧） | 重复制（新） |
|------|------------|------------|
| 每轮范围 | 部分维度 | **全部四个维度** |
| 发现节奏 | 后期才暴露其他维度问题 | 早期就暴露各类问题 |
| 收敛趋势 | 不明显 | 自然收敛（后期问题越来越少） |

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

### 自审执行流程（子代理串行 + 重复制）

```
10 轮自审执行流程（子代理串行，每轮全维度）:

1. 主 Agent 启动第一轮子代理:
   Agent(
     subagent_type="claude",
     description="Prototype 自审 Round 1",
     prompt="读取 prototype/ 目录下所有 HTML 文件和 design-prompt.md，按覆盖性、一致性、可用性、完整性全部四个维度独立检查。覆盖性为第一优先级。发现问题直接修复原型文件，生成审查报告到 self-reviews/prototype/{YYYYMMDD}-{HHMMSS}.md。仅修复确认的问题，不做重构或额外改进。"
   )
2. 子代理返回审查报告路径
3. 主 Agent 读取报告，确认修复内容
4. 修复不合理 → 主 Agent 补充修复
5. 启动下一轮子代理（Round N+1），步骤同 Round 1
6. SHALL NOT 并行启动多个子代理（串行执行）
7. 重复直至完成全部 10 轮
8. 全部完成后进入用户评审确认
```

### 与 VERIFY 子代理模式的对比

| 维度 | SELFREV（自审） | VERIFY（验证） |
|------|----------------|---------------|
| 执行者 | 独立子代理 (Agent subagent) | 独立子代理 (Agent subagent) |
| 目的 | 自我完善、维度级审查 + 边审边修 | 独立验证、发现遗漏 + 出报告 |
| 范围 | 维度级审查（4 维度全量） | 具体检查项（可达性、按钮、表单、弹窗、流程） |
| 轮次 | 10 轮 | 5 轮（导航）+ 5 轮（Playwright） |

### 自审报告内容

每轮报告包含：审查维度得分表（维度名/本轮得分/上轮得分/变化值）、新发现问题清单、上轮问题修复验证、本轮改进内容描述、仍存在问题。

### 强制执行规则

- SHALL 完成全部 10 轮自审，不允许提前终止
- 即使连续多轮无新问题也必须完成全部 10 轮
- SHALL 每轮启动独立子代理（Agent subagent），不允许主 Agent 自身执行自审
- SHALL NOT 并行启动多个子代理（串行执行，前一轮完成后再启动下一轮）
- 自审全部完成后进入用户评审确认（AskUserQuestion），释放 design 阶段门控

## 步骤 9：REVIEW — 用户评审循环

### 评审交互

通过 AskUserQuestion 向用户展示：

```
Question: "HTML 原型已完成，覆盖 {n} 个屏幕、{m} 个 UI 功能点。
[CDN 离线扫描: {通过 / 不通过}]
[交叉引用检查: {通过 / 不通过}]
[导航合理性验证: 5 轮完成，发现并修复 {x} 个问题]
[Playwright 验证: 5 轮完成，发现并修复 {y} 个问题]
[UX 规则审查: 5 轮完成，发现并修复 {a} 个问题]
[对比度检测: {通过 / 不通过}]
[design-system 产物: {存在 / 缺失}]
[10轮自审（重复制）: 已完成，发现并修复 {z} 个问题]
是否确认通过？"
Options:
  - "确认通过" → 原型满足需求，进入详细设计
  - "需要修订" → 收集用户反馈 → 回到 DESIGN 步骤
```

### 评审循环机制

```
DESIGN(子代理委托) → VERIFY(CDN+交叉引用+导航5轮+Playwright5轮) → SELFREV(10轮重复制) → REVIEW
  ├── 确认通过 → COMPLETE
  └── 需修订 → 收集用户反馈 → 回到 DESIGN（再次调用 huashu-design，附修订要求）
```

### 评审结果处理

| 用户选择 | 阶段状态 | 评审记录 | 后续动作 |
|---------|---------|---------|---------|
| 确认通过 | ✅ 完成 | ✅ 已确认 | 门控释放，可进入详细设计 |
| 需要修订 | ⚠️ 需修订 | ⚠️ 需修订 | 保持原型设计阶段，根据用户反馈修订原型 |

## 步骤 10：COMPLETE — 更新状态文件 + 自动生成元素覆盖树 + 更新 index.md 清单

更新 `docs/changes/{change}/.status.md`：
1. 标记原型设计阶段: `✅ 完成`（或 `⏭️ 跳过`）
2. 记录用户评审结果到「用户评审记录」表
3. 设置当前阶段为「详细设计」
4. 记录完成时间和执行备注

### 10.1 原型通过后自动提取设计令牌和元素覆盖树

当用户在 REVIEW 步骤中"确认通过"后，SHALL 从实际原型 HTML 文件中自动提取：

**提取 design-tokens.css**（保留不变）:

```
1. 扫描 prototype/ 目录下所有 .html 文件
2. 提取 :root { ... } 中的 CSS 变量声明
3. 提取内联 style 中的颜色值、font-size、border-radius、box-shadow 等
4. 去重、排序、归类后输出到 prototype/design-tokens.css
```

**提取 element-coverage-tree.md**（替代 element-spec.md 和 nav-tree.md）:

```
1. 解析 prototype/*.html 的 DOM 树
2. 提取页面导航骨架: 所有 <a href> 和导航组件引用 → 📄 页面节点
3. 提取交互元素: <button>, <a>, <input>, <select>, <textarea>, <dialog>,
   [role="dialog"], <details> → 🔘/📝/📊 元素节点
4. 提取 CSS 伪类状态: :hover, :active, :focus, :disabled
   + class 命名推测: is-loading, is-error, is-empty, is-disabled, is-active
   → 🎯 状态节点
5. 提取操作链: 扫描 JS 事件绑定（onclick, addEventListener, @click, onClick）
   → 分析 DOM 操作推断弹窗/下拉/跳转 → 💬/🔗 子树
6. 输出 prototype/element-coverage-tree.md（初始版，TC-ID 列为空）
7. 文件头部标注: 生成时间戳和来源（prototype-design 阶段自动生成）
```

> **废弃**: element-spec.md 和 nav-tree.md 不再生成，其信息由 element-coverage-tree.md 统一承载。

**原型迭代后重新生成**: 修订模式用户确认通过后，重新执行上述提取，覆盖旧版本。若 design 阶段已填充 TC-ID，通过 AskUserQuestion 确认是否保留已有映射。同时 SHALL 重新扫描 prototype/ 目录，更新 `prototype/index.md` 中的文件清单（含角色标注）和版本号，确保清单反映修订后的产物全貌。

**跳过时不生成**: 原型设计阶段被跳过（⏭️ 跳过）时，不生成 design-tokens.css 和 element-coverage-tree.md。

## 步骤 11：POST_HOOK — 阶段后置钩子

引用 `skills/kflow-prototype-design/references/hooks.md` prototype-design 阶段 POST_HOOK（🔶 浏览器类型：BROWSER_CLEANUP + UPDATE_STATE）。

---

## 跳过条件

| 条件 | 处理方式 |
|------|---------|
| 纯后端项目 | 自动跳过，标记 ⏭️ 跳过 |
| functional-designs/ 中无前端/UI 功能点 | 自动跳过，标记 ⏭️ 跳过 |
| 用户在 AskUserQuestion 中主动拒绝 | 跳过，标记 ⏭️ 跳过 |
| prototype-gen 角色 Skill 数量 = 0 | ⚠️ 硬阻塞，提示安装 huashu-design 或 frontend-design，**不跳过** |

## 修订模式双入口

修订模式有两种入口：

### 入口 A: CHECK 步骤检测到已有原型（用户驱动修订）

`prototype/index.md` 已存在时，跳过 INPUT/OPTIMIZE/TOOLCHAIN，加载已有原型 + 用户修订需求 → 进入 DESIGN。

### 入口 B: code 阶段驱动回退（编码驱动修订）

当编码阶段发现原型交互/视觉/状态问题，通过 AskUserQuestion 决策流程回退到此阶段：

```
code 阶段 → 发现原型问题 → AskUserQuestion → 确认回退 → prototype-design REVISION 模式

1. 编码 Agent 记录问题到 skill-suggestion.md（原型页面路径 + 问题描述 + 建议修订方向）
2. prototype-design 加载已有原型 + 编码阶段记录的问题
3. 修订 → 验证 → 用户确认
4. 完成后回到 design 继续后续流程（plan → code）
5. 修订范围仅限于原型问题，不扩展到功能设计领域
```

---

## 阶段边界约束

### 域内内容（prototype 负责）

| 内容类别 | 说明 |
|---------|------|
| UI 原型页面 | 基于 functional-designs/ 的页面定义生成多文件 HTML 原型（`prototype/` 目录，`index.html` 为入口） |
| 交互流程 | 基于功能设计中的可执行操作和业务流程设计交互，使用 flow demo 模式（完整可交互路径，单台设备状态管理器驱动） |
| 视觉风格 | 统一的视觉风格、组件命名、页面布局模式 |
| 交互状态 | 加载态、空态、错误态、边界态等完整状态覆盖 |
| 表单组件 | 基于功能设计中的表单项定义（字段名/类型/校验规则/默认值/placeholder）生成对应表单组件 |
| 菜单结构 | 基于功能设计中的导航定义生成菜单树（一/二/三级菜单 + 对应页面） |
| 离线自包含 | 所有 CSS/JS/字体/图片内联或相对路径引用，禁止 `http://` `https://` 外部 CDN 依赖，字体使用系统默认字体栈 |

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
4. **禁止**自行修改 functional-designs/ 内容

---

# 与其他 Skill 的关系

```
kflow-explore（设计探索）
  └── 输出 functional-designs/
        └── kflow-prototype-design（本阶段，可选）
              ├── OPTIMIZE 产出 design-prompt.md（7 章节）
              ├── DESIGN: Agent(subagent) 子代理 → Skill("huashu-design")
              └── 输出 prototype/ 目录（多文件，index.html 为入口）
                    └── kflow-design（详细设计）

归档时: kflow-archive 将变更原型合并到产品级 docs/prototype/
```

- **输入来自**：`kflow-explore`（设计探索阶段）
- **输出给**：`kflow-design`（详细设计阶段）
- **前置阶段**：设计探索（必须完成）
- **后续阶段**：详细设计（原型设计完成后或跳过后）
- **委托执行**：按 `docs/toolchain.md` 锁定的设计引擎（huashu-design / frontend-design / 其他），不可用时硬阻塞
- **归档合并**：`kflow-archive` 将变更原型合并到产品级 `docs/prototype/`

---

# 核心提醒

- **编排层非执行层**：本 Skill 不做具体原型制作，所有原型生成通过子代理委托给 huashu-design
- **子代理委托调用**：DESIGN 步骤通过 `Agent(subagent_type="claude")` 子代理调用 huashu-design，子代理独立上下文，HTML 产物不污染主 Agent
- **design-prompt.md 唯一真相源**：OPTIMIZE 完成后输出 `prototype/design-prompt.md`（7 章节），经用户确认后作为 DESIGN 步骤唯一输入
- **OPTIMIZE 必须经用户确认**：提示词优化后 SHALL 通过 AskUserQuestion 展示给用户确认，确认通过后方进入 DESIGN
- **页面元素穷举**：OPTIMIZE 步骤必须穷举每个页面的菜单、按钮、表单（含字段/类型/校验/默认值）、数据展示区、状态覆盖、弹窗/抽屉，不得遗漏
- **业务流程驱动**：默认使用 flow demo 模式（可交互流程，单台设备状态管理器驱动），禁止 overview 静态平铺
- **多文件输出**：原型输出到 `prototype/` 目录（非单文件），`index.html` 为入口，允许 `page-*.html` 独立页面和 `shared/` 共享资源
- **离线自包含硬约束**：禁止 CDN 外部依赖（`http://` `https://`），所有资源内联或相对路径，字体使用系统字体栈
- **prototype-gen 角色不可用是硬阻塞**：标记 ⚠️ 阻塞，提示安装命令：`huashu-design` 或 `frontend-design`
- **5 轮导航合理性验证**：VERIFY 6.3 节执行 5 轮子代理串行验证（页面可达性/返回按钮/表单链/弹窗/闭环），每轮全 5 项，不可提前终止
- **5 轮 Playwright 全覆盖验证**：VERIFY 6.4 节执行 5 轮子代理串行验证（可达性/按钮/表单/弹窗/端到端），每轮全 5 项，不可提前终止
- **10 轮自审强制执行（子代理串行 + 重复制）**：DESIGN 完成后自动进入 SELFREV，每轮启动独立子代理执行全部四个维度（覆盖性+一致性+可用性+完整性），子代理边审边修，串行不可并行，生成独立报告，不允许提前终止
- **用户评审是循环**：通过 AskUserQuestion 确认，需要修订时回到 DESIGN 步骤重新启动子代理委托 huashu-design
- **Playwright 不可用时降级**：记录降级原因，改为手动文件分析并写入报告
- **CDN 扫描优先于后续验证**：CDN 扫描不通过时不继续后续验证步骤
- **禁止自行修改上游产物**：不得修改 functional-designs/ 中的内容

---

# 反馈机制

如果在使用本 Skill 过程中发现问题或有优化建议，请记录到 `docs/skill-suggestion.md` 文件中。
