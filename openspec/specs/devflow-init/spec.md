## MODIFIED Requirements

### Requirement: 变更流程强制规则 section 扩展

kflow-init SHALL 在「变更流程强制规则」section 中包含 git 相关规则和 Skill 改进建议自动捕获规则。使用现有 marker `## 变更流程强制规则` 和新增 marker `## Skill 改进建议自动捕获` 幂等更新。

#### Scenario: 注入扩展的流程规则

- **WHEN** 执行 kflow-init
- **THEN** 系统在「变更流程强制规则」section 中包含以下 git 规则：
  - 首次 init 时，若目录非 git 仓库，询问是否执行 git init
  - 归档完成后，询问是否将当前变更及相关文件提交 git

#### Scenario: 注入 Skill 改进建议自动捕获规则

- **WHEN** 执行 kflow-init
- **AND** CLAUDE.md 不存在 `## Skill 改进建议自动捕获` marker
- **THEN** 系统在 CLAUDE.md 末尾追加 `## Skill 改进建议自动捕获` section
- **AND** section 内容 SHALL 定义三种触发模式和处理规则：
  - 「因...无法...」→ 记录阻塞原因和失败的执行路径
  - 「因...导致...」→ 记录因果链和受影响的阶段
  - 用户纠正后 AI 回复中的「你说得对」等附和 → 记录用户的纠正内容
- **AND** 标注来源为 kflow-init 和注入时间戳

#### Scenario: 已有流程规则的增量更新

- **WHEN** CLAUDE.md 已有「变更流程强制规则」section 但不含 git 规则
- **THEN** 系统替换为包含 git 规则的最新版本
- **AND** 保留原有非 git 规则的内容结构

#### Scenario: 自动捕获规则已存在的幂等更新

- **WHEN** CLAUDE.md 已包含 `## Skill 改进建议自动捕获` marker
- **THEN** 系统 SHALL 不重复追加该 section
- **AND** 可选择更新 section 内容以反映最新的触发模式定义

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
