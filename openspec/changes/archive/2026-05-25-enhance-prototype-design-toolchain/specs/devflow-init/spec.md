## MODIFIED Requirements

### Requirement: 工具推荐矩阵 — 原型设计阶段多方案

kflow-init 的工具推荐矩阵中，原型设计阶段 SHALL 描述多方案现状而非硬编码单一 Skill。

#### Scenario: 工具推荐矩阵中原型设计阶段

- **WHEN** kflow-init 执行 MATCH 步骤匹配工具推荐矩阵
- **THEN** 原型设计阶段的推荐 SHALL 描述为多方案而非硬编码 `huashu-design`
- **AND** 方案描述 SHALL 包含：
  - 方案 A: huashu-design 一体化（推荐）
  - 方案 B: ui-ux-pro-max + huashu-design 设计驱动型
  - 方案 C: ui-ux-pro-max + frontend-design 静态页面型
- **AND** 每种方案标注优缺点和适用场景
- **AND** 铁律标注：用户环境中必须至少有 1 个能编写 HTML 的原型设计 Skill（prototype-gen 角色）

#### Scenario: GAP 检测更新

- **WHEN** kflow-init 执行 GAP 步骤检测能力缺口
- **THEN** 原型设计阶段缺口检测 SHALL 检查是否存在至少 1 个 prototype-gen 角色的 Skill
- **AND** 不存在时输出："⚠️ 未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
- **AND** 存在但仅有 1 个时标注："✅ 检测到 {skill_name}，可支持原型设计"
- **AND** 存在多个时标注："✅ 检测到多个设计 Skill，kflow-prototype-design 将推荐方案供用户选择"
