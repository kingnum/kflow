## Context

当前 `kflow-prototype-design` 阶段通过 CHECK 步骤硬编码绑定 `huashu-design` 单一引擎：扫描 `.claude/skills/` 中是否存在 `huashu-design`，不存在则阻塞。用户环境中实际可用的设计 Skill（如 `ui-ux-pro-max`、`frontend-design`）无法被利用。同时编排层的验证门控部分依赖引擎自带能力，缺少自给自足的兜底验证体系。

## Goals / Non-Goals

**Goals:**

- 使 `kflow-prototype-design` 能够动态识别环境中可用的设计相关 Skills，并组合为可行的工具链方案
- 在 DESIGN 步骤前增加风格/布局推荐环节（5.1 STYLE），用户选定风格后锁定执行（5.2 GENERATE）
- 编排层验证门控完全自给自足：新增 UX 规则审查（5 轮）和对比度检测，不依赖任何引擎
- `design-system/MASTER.md` 作为通用必备产物，不限定哪个 Skill 生成
- `kflow-init` 工具推荐矩阵反映多方案现状

**Non-Goals:**

- 不改变 kflow-prototype-design 的核心流程（CHECK → ASSESS → INPUT → OPTIMIZE → DESIGN → VERIFY → SELFREV → REVIEW → COMPLETE）
- 不改变 kflow-prototype-design 作为编排层的职责（不内化任何引擎的实现细节）
- 不引入新的外部依赖或 MCP server
- 不涉及其他阶段的变更

## Decisions

### D1: 在 kflow-prototype-design 内部实现工具链选择，而非新建独立 Skill

**决策**: 工具链扫描、分析、推荐、锁定逻辑内置于 kflow-prototype-design 的 SCAN + TOOLCHAIN 步骤。

**理由**: 工具链选择是原型设计阶段的子流程，不需要独立 Skill。新建 Skill 会增加调用链复杂度和用户认知负担。

**替代方案**: 新建 `kflow-toolchain-selector` Skill — 被否决，因为增加了一层不必要的抽象。

### D2: 风格推荐由编排层子代理执行，不依赖引擎内部能力

**决策**: 5.1 STYLE 步骤由 kflow-prototype-design 的子代理分析 design-prompt.md 后直接推荐 3 个差异化风格方向（含 ASCII 线框图 + 色彩方案）。

**理由**: 风格推荐是信息展示 + 用户决策，不需要生成 HTML。编排层基于已有的项目上下文（产品类型、目标用户、设计约束）即可输出合理的风格建议。如果环境中存在 `ui-ux-pro-max`，可先执行 `--design-system` 查询获取更精确的推荐作为补充。

### D3: UX 规则审查采用精简硬编码规则集（20-30 条），不依赖 ui-ux-pro-max 的 CSV 数据库

**决策**: 编排层内置一个精简的 UX 核心规则清单（对比度 ≥4.5:1、触摸目标 ≥44px、表单 label 非 placeholder-only、按钮视觉反馈、弹窗关闭方式等），子代理读取 HTML 文件做静态分析逐条检查。

**理由**: 编排层的验证必须能在没有 ui-ux-pro-max 的环境中独立运行。如果选了 ui-ux-pro-max，其完整 99 条 UX 规则库作为"可选增强"并行执行，交叉验证更全面。

### D4: design-system/ 作为必备产物，任何引擎都必须输出

**决策**: 无论选定哪个工具链，最终都必须输出 `design-system/MASTER.md`。编排层在 design-prompt.md 的硬约束章节中显式要求输出此文件。如果选了 ui-ux-pro-max，由其 `--design-system --persist` 生成更精确的结果；如果选了其他引擎，由编排层 prompt 约束其输出。

**理由**: design-system 是后续 code 和 code-review 阶段进行"原型对账"的必要输入，不能依赖特定引擎才生成。

### D5: 风格选择决策记录到 prototype/style-decision.md，不新增独立文件类型

**决策**: 新增 `prototype/style-decision.md` 文件记录用户选定的风格方向，作为 5.2 GENERATE 步骤的输入。文件包含风格名称、设计哲学描述、色彩方案、字体系统、布局模式、ASCII 线框图。

**理由**: 此文件是 DESIGN 步骤内部的中间产物，不需要在 toolchain.md 中记录（toolchain.md 记录的是工具链方案选择，不是风格选择）。

## Risks / Trade-offs

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 风格推荐质量不如 huashu-design 内置顾问模式 | 用户选到不合适的风格 | 编排层基于 design-prompt.md 的上下文（产品类型、目标用户）做有根据的推荐；有 ui-ux-pro-max 时先查询其 CSV 数据库增强精确度 |
| 精简 UX 规则集（20-30 条）覆盖不足 | 部分 UX 问题未被发现 | 作为兜底验证，不影响引擎自带的更专业审查（如有） |
| 强制要求所有引擎输出 design-system/ | 部分引擎不擅长结构化输出 | 编排层在 prompt 中提供明确的 Markdown 模板格式，降低引擎实现难度 |
| 工具链方案过多导致用户决策困难 | 选择疲劳 | 限制推荐不超过 3 个方案，标注推荐优先级 |
