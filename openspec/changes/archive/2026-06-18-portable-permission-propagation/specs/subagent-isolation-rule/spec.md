## MODIFIED Requirements

### Requirement: 权限预配置要求

kflow-init SHALL 在目标项目中自动配置 kflow Skills 执行所需的权限（参见 `kflow-shared/permission-model.md`），取代之前要求项目手动预配置 `.claude/settings.json` 的方式。重试机制新增权限回退场景——后台子代理权限失败时创建新前台子代理，不计入 3 次上限。

#### Scenario: 权限预配置

- **WHEN** kflow-init 在目标项目中执行 PERM_CONFIG 步骤后
- **THEN** 目标项目的 `.claude/settings.json` permissions.allow 列表 SHALL 包含 `kflow-shared/permission-model.md` 中定义的全部权限
- **AND** 权限配置 SHALL 由 kflow-init 自动完成，而非要求项目手动预配置

#### Scenario: 子代理权限继承

- **WHEN** 执行阶段启动子代理
- **THEN** 子代理 SHALL 继承 settings.json 中的预配置权限
- **AND** SHALL NOT 在执行过程中因权限问题请求用户批准

#### Scenario: 后台子代理权限失败回退

- **WHEN** 后台子代理因权限问题执行失败
- **THEN** 主 Agent SHALL 创建新的前台子代理（run_in_background=false）重新执行同一任务
- **AND** 主 Agent SHALL NOT 在主 Agent 上下文中直接接管执行
- **AND** 该回退 SHALL NOT 计入轮次级重试的 3 次上限
- **AND** 前台子代理也失败时，主 Agent SHALL 标记该阶段为 ⚠️ 阻塞

### Requirement: 各 SKILL.md 内联子代理强制规则框

所有 7 个执行类阶段的 SKILL.md SHALL 在文档开头（角色声明后、任务声明前）新增独立的「子代理强制规则」引用框，确保规则在执行时直接可见。规则框 SHALL 明确适用于所有入口场景，并包含后台权限失败回退规则。

#### Scenario: SKILL.md 规则框内容

- **WHEN** 读取执行类阶段的 SKILL.md
- **THEN** SHALL 在角色声明后、任务声明前包含引用框
- **AND** 引用框包含以下五条规则：(1) 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收；(2) 主 Agent SHALL NOT 直接执行本阶段主工作，无例外；(3) 子代理 SHOULD 前台运行（推荐 run_in_background=false），后台模式仅在权限已预配置时使用；(4) 适用场景：直接触发 + triage 路由 + 其他 Skill 调用；(5) 后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管
- **AND** 引用框注明"参见 kflow-shared/repetition-model.md §12"
