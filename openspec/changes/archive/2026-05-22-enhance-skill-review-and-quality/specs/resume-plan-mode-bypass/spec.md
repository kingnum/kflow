## ADDED Requirements

### Requirement: RESUME 输入禁止进入 Plan Mode

系统 SHALL 在 CLAUDE.md 和 kflow-guide SKILL.md 中强制要求：当用户输入匹配「继续/恢复/resume + 变更名」模式时，直接进入 Skill 路由链（kflow-guide → kflow-resume → 目标阶段 Skill），SHALL NOT 先进入 Claude Code Plan Mode 等待用户审批计划。

#### Scenario: RESUME 路由不被 Plan Mode 拦截

- **WHEN** 用户输入 "继续 add-user-auth" 或 "恢复 add-user-auth" 或 "resume add-user-auth"
- **THEN** Claude Code MUST 直接触发 kflow-guide Skill
- **AND** kflow-guide 正则解析命中 RESUME 模式后路由到 kflow-resume
- **AND** 全程不进入 Plan Mode，不展示计划审批界面
- **AND** kflow-resume 定位断点后直接调度对应阶段 Skill

#### Scenario: 非 RESUME 输入不受影响

- **WHEN** 用户输入类似但不完全匹配的文本（如 "我想继续开发" 无变更名、"resume" 单独出现）
- **THEN** 按 kflow-guide 原有的关键词意图识别流程处理
- **AND** 不强制要求跳过 Plan Mode

### Requirement: kflow-guide 描述中声明 Plan Mode 绕过

kflow-guide SKILL.md 的 description frontmatter SHALL 包含 Plan Mode 绕过提示，确保 Skill 匹配引擎在 Plan Mode 评估前优先匹配该 Skill。

#### Scenario: Skill description 包含绕过提示

- **WHEN** kflow-guide SKILL.md 被加载
- **THEN** description 中包含 RESUME 路由的优先级说明
- **AND** 明确标注 "RESUME 模式优先，禁止 Plan Mode 拦截"

### Requirement: CLAUDE.md 中声明 RESUME 禁止规则

项目根目录 CLAUDE.md SHALL 包含一条强制规则：用户输入匹配「继续/恢复/resume + 变更名」时，禁止进入 Plan Mode，直接执行 Skill 路由。

#### Scenario: CLAUDE.md 规则生效

- **WHEN** Claude Code 加载项目 CLAUDE.md
- **THEN** 识别 RESUME 路由禁令
- **AND** 在处理用户输入时，优先检查是否匹配 RESUME 模式
- **AND** 匹配时跳过 Plan Mode 评估
