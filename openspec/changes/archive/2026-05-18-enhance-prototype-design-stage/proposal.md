## Why

当前 `kflow-prototype-design` 阶段在委托 huashu-design 时，prompt 只是从 `functional-designs/` 机械提取文本填入模板，缺乏对 UI 元素（菜单树、页面分区、按钮、表单、交互行为）的穷举级描述，导致原型产出质量不稳定。同时存在三个缺口：输出仅限单文件 `index.html`、未强制业务流程驱动的 flow demo 模式、未要求离线自包含。这四个问题共同导致原型无法达到"接近最终交付形态"的体验标准。

## What Changes

- **新增 OPTIMIZE 步骤**：编排层 Agent 深度阅读 functional-designs/ 后产出优化后的设计 prompt，通过 AskUserQuestion 展示给用户确认后再执行。优化后的 prompt 必须穷举描述每个页面的菜单层级、布局分区、按钮清单、表单清单（含字段类型/校验/默认值）、数据展示区、状态覆盖、弹窗/抽屉，以及完整的业务流程脚本
- **多文件输出**：原型产物从单文件 `prototype/index.html` 扩展为多文件架构（`prototype/` 目录，`index.html` 为入口），去除对单文件的限制
- **业务流程驱动**：默认使用 flow demo 模式（可交互流程），禁止仅提供 overview 平铺的静态页面展示。prompt 必须包含业务流程脚本（逐步描述用户在哪个页面、点击什么、看到什么）
- **离线自包含**：原型页面禁止外部 CDN 依赖（CSS/JS/字体/图片），所有资源内联或使用相对路径，字体使用系统默认字体栈。**BREAKING**: 对验证步骤增加 CDN 扫描，发现外部依赖视为验证不通过

## Capabilities

### New Capabilities
- `prototype-prompt-optimization`: 编排层在委托 huashu-design 前，深度分析 functional-designs/ 并产出细化到菜单树、页面分区、按钮/表单/数据展示区级别的设计 prompt，通过 AskUserQuestion 展示给用户确认后执行
- `prototype-offline-constraint`: 原型 HTML 文件必须离线自包含——禁止外部 CDN 依赖，所有资源内联或相对路径，字体使用系统字体栈。验证步骤增加 CDN 扫描检查

### Modified Capabilities
- `html-prototype-workflow`: 输出产物从单文件 `index.html` 改为多文件目录架构（`prototype/` 目录，`index.html` 为入口）；默认强制 flow demo 模式（业务流程驱动的可交互原型），禁止 overview 静态平铺；插入 OPTIMIZE 步骤到 INPUT 和 DESIGN 之间

## Impact

- `docs/designs/skills/kflow-prototype-design.md` — 设计规格文档：执行流程、输出产物定义、prompt 模板、验证步骤均需更新
- `.claude/skills/kflow-prototype-design/SKILL.md` — 运行时 Skill 定义：步骤编号、OPTIMIZE 步骤详情、约束规则更新
- `openspec/specs/html-prototype-workflow/spec.md` — 需求规格更新
