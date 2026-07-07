## Why

当前 `kflow-prototype-design` 阶段硬编码绑定 `huashu-design` 单一引擎，无法适配用户环境中实际可用的其他设计 Skill（如 `ui-ux-pro-max`、`frontend-design`）。同时编排层的验证门控部分依赖引擎自带能力（如 Playwright 验证），缺少自给自足的兜底验证。DESIGN 步骤缺少风格/布局推荐环节，用户无法在生成前选择设计方向。

## What Changes

- DESIGN 步骤拆分为 **5.1 STYLE（风格/布局推荐）** 和 **5.2 GENERATE（按选定风格生成）** 两个子阶段，推荐 3 个差异化方向供用户选择
- 编排层新增 UX 规则审查（5 轮）和对比度检测，验证门控不再依赖任何特定引擎
- `design-system/` 作为通用必备产物，不限定哪个 Skill 生成
- `kflow-init` 工具推荐矩阵从硬编码 `huashu-design` 改为多方案描述
- 新增 `prototype/style-decision.md` 产物记录风格选择决策
- 修订模式（REVISION）对齐上述变更

## Capabilities

### New Capabilities

- `prototype-design-toolchain`: 原型设计阶段工具链灵活性——环境扫描、多方案推荐、用户选择锁定、引擎无关验证门控

### Modified Capabilities

- `kflow-init-toolchain`: kflow-init 工具推荐矩阵中原型设计阶段从硬编码改为多方案描述
- `kflow-prototype-design-verify`: 编排层验证门控增强（UX 规则审查 + 对比度检测 + design-system 产物检查）

## Impact

- **修改的设计文档**: `docs/designs/skills/kflow-prototype-design.md`（DESIGN/VERIFY 步骤重写）、`docs/designs/skills/kflow-init.md`（工具推荐矩阵更新）
- **新增的产物文件**: `prototype/style-decision.md`（风格选择记录）、`design-system/MASTER.md`（设计系统，通用必备）
- **受影响的阶段**: 原型设计阶段（前端/UI 变更）
- **不受影响的阶段**: 纯后端项目（跳过原型设计）、其他所有阶段
