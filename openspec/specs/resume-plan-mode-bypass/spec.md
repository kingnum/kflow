# resume-plan-mode-bypass Specification

## Purpose
定义变更名模式的 Skill 路由优先级规则：用户输入匹配「恢复/resume + 变更名」时进入 kflow-guide → kflow-resume → 目标阶段 Skill 的恢复链，匹配「继续 + 变更名」时进入 kflow-guide → 目标阶段 Skill 的轻量推进链；两条链路均禁止被 Claude Code Plan Mode 拦截，并要求 CLAUDE.md 与 kflow-guide SKILL.md 同步声明该规则。
## Requirements
### Requirement: RESUME 输入禁止进入 Plan Mode

系统 SHALL 在 CLAUDE.md 和 kflow-guide SKILL.md 中强制要求：当用户输入匹配变更名模式（「恢复/resume + 变更名」或「继续 + 变更名」）时，直接进入 Skill 路由链，SHALL NOT 先进入 Claude Code Plan Mode 等待用户审批计划。两条路径的路由链分别为：`kflow-guide → kflow-resume → 目标阶段 Skill`（恢复）与 `kflow-guide → 目标阶段 Skill`（轻量推进）。

#### Scenario: RESUME 路由不被 Plan Mode 拦截

- **WHEN** 用户输入 "恢复 add-user-auth" 或 "resume add-user-auth"
- **THEN** Claude Code MUST 直接触发 kflow-guide Skill
- **AND** kflow-guide 正则解析命中恢复模式后路由到 kflow-resume
- **AND** 全程不进入 Plan Mode，不展示计划审批界面
- **AND** kflow-resume 定位断点后直接调度对应阶段 Skill

#### Scenario: 轻量推进路由不被 Plan Mode 拦截

- **WHEN** 用户输入 "继续 add-user-auth"
- **THEN** Claude Code MUST 直接触发 kflow-guide Skill
- **AND** kflow-guide 正则解析命中轻量推进模式后读取 `.status.md` 并直接调度目标阶段 Skill
- **AND** 全程不进入 Plan Mode，不展示计划审批界面
- **AND** SHALL NOT 调用 kflow-resume

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

### Requirement: CLAUDE.md 中声明变更名模式禁止 Plan Mode 规则

项目根目录 CLAUDE.md SHALL 包含一条强制规则：用户输入匹配变更名模式（「恢复/resume + 变更名」或「继续 + 变更名」）时，禁止进入 Plan Mode，直接执行 Skill 路由。

#### Scenario: CLAUDE.md 规则生效

- **WHEN** Claude Code 加载项目 CLAUDE.md
- **THEN** 识别变更名模式路由禁令
- **AND** 在处理用户输入时，优先检查是否匹配变更名模式
- **AND** 匹配时跳过 Plan Mode 评估
- **AND** 该强制规则 SHALL 由 kflow-init 注入到「变更流程强制规则」section

