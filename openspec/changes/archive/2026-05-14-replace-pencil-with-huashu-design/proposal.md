## Why

Pencil 的 `.pen` 是加密封闭格式，不可 diff/merge/复用，原型在每个变更中从零画起、归档后即废弃。Huashu-Design 是一套完整可用的 HTML 原型 Skill，产出纯文本、可交互、可组合。替换后不仅产出质量提升，更关键的是原型从一次性消费品变为可跨变更累积的产品资产。

## What Changes

- **BREAKING**: 移除 Pencil MCP 依赖，`mcp__pencil__*` 工具调用全部废弃
- **BREAKING**: 变更级原型产物从 `prototype.pen` 改为 `prototype/index.html`
- `kflow-prototype-design` 改为委托调用 huashu-design Skill 执行设计工作
- 新增产品级原型目录 `docs/prototype/`，含 `design-tokens.css`、`screens/`、`components/`、总导航 `index.html`
- `kflow-init` 新增 huashu-design 可用性检测，未安装时提示安装
- `kflow-archive` 归档时自动合并变更原型到产品级原型
- 新变更原型设计时，自动加载产品级已有原型作为上下文，基于已有设计扩展
- 新增 Playwright 最小点击测试作为原型交付前验证
- 删除 `references/rules/pencil-design-style.md`

## Capabilities

### New Capabilities

- `html-prototype-workflow`: HTML 原型工作流 — huashu-design 委托调用、prompt 上下文组装、用户评审循环（确认通过/需修订回到 DESIGN）、Playwright 交互验证
- `product-prototype-system`: 产品级原型累积体系 — `docs/prototype/` 目录结构、design-tokens.css 共享令牌、原型合并算法（新增/修改/不变三种处理）、新变更基于已有原型的扩展机制

### Modified Capabilities

- `archive-design-merge`: 归档合并范围从"功能设计+详细设计"扩展为"功能设计+详细设计+原型"，新增原型文件合并逻辑，移除"原型设计不合并"的旧规则（Pencil 时代产物）

## Impact

| 层面 | 影响 |
|------|------|
| Skill 实现 | `kflow-prototype-design` SKILL.md 完全重写（编排层，委托调用 huashu-design）；`kflow-archive` 扩展原型合并步骤；`kflow-init` 新增 huashu-design 检测 |
| 设计文档 | `docs/designs/skills/kflow-prototype-design.md` 重写 (v2.0.0)；`docs/designs/core-mechanisms.md` 产物路径更新；`docs/designs/index.md` Skill 描述更新；`docs/designs/skills/kflow-design.md` 输入来源更新 |
| 目录结构 | 新增 `docs/prototype/`；变更目录下 `prototype.pen` → `prototype/` |
| 工具链 | 移除 `mcp__pencil__*`；新增 `Skill("huashu-design", ...)` 委托调用 |
| 规则文件 | 删除 `references/rules/pencil-design-style.md` |
| 外部依赖 | huashu-design Skill (`npx skills add alchaincyf/huashu-design`) |
