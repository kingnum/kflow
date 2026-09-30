# Spec Delta

## MODIFIED Requirements

### Requirement: 子代理异常时主代理禁止接管

系统 SHALL 在各执行类 skill 自身的 `references/repetition.md` §12 中定义全局强制规则：对于所有使用子代理（Agent subagent）开展工作的任务，如果子代理意外停止、报错退出、返回要求重做或继续做，主代理 MUST 重新创建新的子代理继续执行，SHALL NOT 接管子代理的工作直接开始执行。对于执行类阶段，重试粒度为轮次级——新建 Agent 重跑崩溃轮次，最多重试 3 次，全部失败标记阻塞。子代理执行模式 SHALL 推荐前台模式（run_in_background=false），但在权限已预配置时允许后台模式。

#### Scenario: 子代理报错退出

- **WHEN** 子代理在执行过程中报错退出
- **THEN** 主代理 MUST 分析错误原因
- **AND** 调整子代理 prompt（如需要）后重新创建新的子代理
- **AND** SHALL NOT 在主 Agent 上下文中接管子代理未完成的工作
- **AND** 对于执行类阶段，新子代理从崩溃轮次继续执行

#### Scenario: 子代理返回要求重做

- **WHEN** 子代理返回结果要求 "需要重新执行" 或 "请继续完成"
- **THEN** 主代理 MUST 创建新的子代理（新的独立上下文）
- **AND** 新子代理的 prompt 包含上一轮子代理的上下文和未完成的工作说明
- **AND** SHALL NOT 在主 Agent 上下文中直接继续

#### Scenario: 子代理要求继续做

- **WHEN** 子代理因上下文限制返回 "已完成部分工作，需继续"
- **THEN** 主代理 MUST 创建新的子代理继续剩余工作
- **AND** 新子代理应获得之前完成的工作摘要作为起点
- **AND** SHALL NOT 在主 Agent 上下文中从断点继续

#### Scenario: 规则定义位置为 per-skill 文件

- **WHEN** 隔离规则的权威定义位置被解析
- **THEN** 该位置 SHALL 为各执行类 skill 自身的 `references/repetition.md` §12
- **AND** SHALL NOT 为 `.claude/skills/kflow-shared/repetition-model.md` 或任何 `kflow-shared/` 下的路径

### Requirement: 各 SKILL.md 内联子代理强制规则框

所有 7 个执行类阶段的 SKILL.md SHALL 在文档开头（角色声明后、任务声明前）新增独立的「子代理强制规则」引用框，确保规则在执行时直接可见。规则框 SHALL 明确适用于所有入口场景。

#### Scenario: SKILL.md 规则框内容

- **WHEN** 读取执行类阶段的 SKILL.md
- **THEN** SHALL 在角色声明后、任务声明前包含引用框
- **AND** 引用框包含以下五条规则：(1) 本阶段主工作 MUST 通过 Agent 子代理执行，主 Agent 仅负责调度和验收；(2) 主 Agent SHALL NOT 直接执行本阶段主工作，无例外；(3) 子代理 SHOULD 前台运行（推荐 run_in_background=false），后台模式仅在权限已预配置时使用；(4) 适用场景：直接触发 + triage 路由 + 其他 Skill 调用；(5) 后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管
- **AND** 引用框注明"参见 `references/repetition.md` §12"，指向该 skill 自身的相对路径

#### Scenario: 适用阶段清单

- **WHEN** 以下执行类阶段的 SKILL.md 被更新
- **THEN** kflow-plan SHALL 包含规则框
- **AND** kflow-code SHALL 包含规则框
- **AND** kflow-code-review SHALL 包含规则框
- **AND** kflow-api-test SHALL 包含规则框
- **AND** kflow-e2e-test SHALL 包含规则框
- **AND** kflow-integration-test SHALL 包含规则框
- **AND** kflow-bug-fix SHALL 包含规则框

### Requirement: 各 Skill SKILL.md 中标注引用

所有使用子代理的 Skill SHALL 在其 SKILL.md 的相关步骤中标注引用子代理隔离规则。

#### Scenario: 步骤级标注

- **WHEN** Skill 的某步骤使用子代理
- **THEN** 该步骤的描述中 SHALL 包含对该 skill 自身 `references/repetition.md` §12 隔离规则的引用
- **AND** 执行类阶段 SHALL 在文档开头包含「⚠ 子代理强制规则」引用框
- **AND** 标注形式 SHALL 为相对该 skill 的路径引用（如 "参见 `references/repetition.md` §12"）
- **AND** SHALL NOT 使用 `kflow-shared/repetition-model.md` §12 作为标注形式

### Requirement: 权限预配置要求

kflow-init SHALL 在目标项目中自动配置 kflow Skills 执行所需的权限（参见 `skills/kflow-init/references/permission-model.md`），取代之前要求项目手动预配置 `.claude/settings.json` 的方式。后台子代理权限失败时 SHALL 创建新的前台子代理重新执行，主 Agent SHALL NOT 直接接管。

#### Scenario: 权限预配置

- **WHEN** kflow-init 在目标项目中执行 PERM_CONFIG 步骤后
- **THEN** 目标项目的 `.claude/settings.json` permissions.allow 列表 SHALL 包含 `skills/kflow-init/references/permission-model.md` 中定义的全部权限
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
