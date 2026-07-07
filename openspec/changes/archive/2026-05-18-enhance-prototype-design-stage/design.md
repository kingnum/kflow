## Context

当前 `kflow-prototype-design` 阶段采用编排层委托 huashu-design 的架构模型。流程为 CHECK → ASSESS → INPUT → DESIGN → VERIFY → SELFREV → REVIEW → COMPLETE。其中 INPUT 步骤仅做机械的文本提取（从 functional-designs/ 提取文案填入固定模板），存在以下问题：

1. **Prompt 粒度不足**：机械提取只描述"有哪些页面"，不描述页面内部的菜单层次、按钮、表单、数据展示区、交互行为等细节，huashu-design 缺乏足够的执行指令
2. **输出产物单一**：仅规定 `prototype/index.html` 单文件输出，无法表达复杂应用的页面间关系
3. **交互深度不足**：未强制业务流程驱动的 flow demo 模式，原型可退化为静态页面平铺
4. **离线约束缺失**：未要求自包含，原型可能依赖 CDN 资源导致离线无法查看

## Goals / Non-Goals

**Goals:**
- 在 INPUT 和 DESIGN 之间新增 OPTIMIZE 步骤，编排层 Agent 深度分析 functional-designs/ 后产出细化到页面元素级别的设计 prompt，并通过 AskUserQuestion 展示给用户确认
- 输出产物从单文件改为多文件目录架构，`index.html` 为入口
- 默认强制 flow demo 模式（可交互业务流程），禁止静态页面平铺
- 原型文件必须离线自包含：禁外部 CDN 依赖，内联资源或相对路径，字体使用系统字体栈

**Non-Goals:**
- 不改变 huashu-design 内部工作流（placeholder → show → full pass）
- 不改变委托调用架构模型
- 不改变 10 轮自审机制
- 不改变产品级原型合并逻辑（kflow-archive 负责）

## Decisions

### D1: OPTIMIZE 步骤定位在 INPUT 之后、用户确认之前

**选择**：OPTIMIZE 作为独立步骤，夹在 INPUT（机械组装）和 DESIGN（委托执行）之间。

**理由**：
- INPUT 仍做机械提取（保持确定性），OPTIMIZE 在此基础上做设计转译（需要 Agent 判断力）
- 分离关注点：INPUT = 数据收集，OPTIMIZE = 设计分析 + prompt 编写
- 用户确认点放在 OPTIMIZE 之后：用户看到的是"优化后的完整 prompt"，而非原始数据摘录

**替代方案考虑**：
- 将 OPTIMIZE 合并到 INPUT 中 → 拒绝，因为 INPUT 是机械步骤，合并会让步骤职责不清晰
- 跳过用户确认直接执行 → 拒绝，用户明确要求方案 B（展示后确认）

### D2: 优化后的 prompt 必须穷举页面元素

**选择**：prompt 必须包含以下层级的描述：
- 全局结构：菜单树（一/二/三级 → 对应页面）、导航模式、全局组件
- 页面清单：每个页面的布局分区、可执行操作清单、按钮清单、表单清单（含字段/类型/校验/默认值）、数据展示区、状态覆盖、弹窗/抽屉
- 业务流程脚本：逐步描述用户在哪个页面、点击什么、看到什么
- 设计约束：多文件架构、flow demo 模式、离线自包含

**理由**：huashu-design 作为执行引擎需要像素级指令，功能设计文档的抽象描述（"用户管理页面"）不足以驱动高质量原型生成。

### D3: 输出产物从单文件改为目录

**选择**：输出从 `prototype/index.html`（单文件）改为 `prototype/` 目录（多文件，`index.html` 为入口）。

**理由**：
- huashu-design 已支持多文件架构（deck 的多 HTML + iframe 聚合模式），不需要额外要求单文件
- 多文件适合并行开发（各页面独立 HTML）、更易维护
- `index.html` 作为导航/聚合入口，保持可发现性

**文件结构示例**：
```
prototype/
├── index.html          ← 入口：导航/聚合/流程起点
├── page-{name}.html    ← 各页面独立文件
├── shared/
│   ├── styles.css
│   └── components.js
└── verify-report.md
```

### D4: Flow demo 作为默认模式

**选择**：原型设计默认强制 flow demo 模式（单台设备、完整交互流程），禁止仅提供 overview 静态平铺。

**理由**：用户明确要求"按照业务流程进行原型设计，需要完整接近最终交付形态的体验效果"。overview 平铺仅适合设计审查（多屏并排比较），不符合"业务流程体验"目标。

**huashu-design 对接**：在 prompt 中明确指定使用 `AppPhone` 状态管理器的 flow demo 骨架，包含 tab bar / 按钮 / 标注点的可交互行为。

### D5: 离线自包含作为硬约束

**选择**：原型 HTML 文件必须完全自包含：

| 资源类型 | 要求 |
|---------|------|
| CSS | 内联 `<style>` 或相对路径文件引用，禁止 `<link href="http...">` |
| JavaScript | 内联 `<script>` 或相对路径文件引用，禁止 `<script src="http...">` |
| 字体 | 使用系统默认字体栈（`-apple-system, sans-serif` 等），禁止 Google Fonts / CDN 字体 |
| 图片 | base64 data URI 或本地 assets 目录，禁止 CDN 远程图片引用 |

**验证**：VERIFY 步骤增加 CDN 扫描——grep 所有 HTML 文件检查 `http://` 和 `https://` 外部引用，发现即标记为验证不通过。

## Risks / Trade-offs

- **OPTIMIZE 步骤增加耗时**：深度分析 functional-designs/ 需要额外 Agent 轮次。缓解：分析质量换取下游执行质量，投入产出比为正
- **多文件架构复杂度**：需要 VERIFY 步骤额外检查文件间引用完整性。缓解：增加交叉引用检查（每个 `<a href>` / `<iframe src>` 目标文件必须存在）
- **离线约束限制设计选择**：不能使用 CDN 字体和图标库，视觉丰富度可能略降。缓解：系统字体栈在现代浏览器中已足够好；图标可用内联 SVG 替代
- **用户确认环节增加交互成本**：用户需审核优化后的 prompt。缓解：这是用户明确要求的（方案 B），且 OPTIMIZE 的 AskUserQuestion 只做确认/修订二元选择，不额外增加讨论成本
