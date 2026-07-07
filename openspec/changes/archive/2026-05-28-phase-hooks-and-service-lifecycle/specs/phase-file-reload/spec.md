## ADDED Requirements

### Requirement: 阶段执行前强制重读基础信息文件

每个阶段 Skill 在 PRE_HOOK 的 RELOAD 步骤中 SHALL 重新读取该阶段钩子配置表中定义的基础信息文件，不得使用对话上下文缓存中的旧版本。RELOAD 的目标是确保阶段执行基于最新的文件内容。

#### Scenario: 重读 service-guide.md

- **WHEN** 阶段需要服务运行（api-test, e2e-test, integration-test, bug-fix）或需要服务配置信息（code, code-review）
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `docs/service-guide.md` 的完整内容
- **AND** SHALL 使用读取到的端口、启动命令等配置执行后续操作
- **AND** SHALL NOT 使用对话历史中缓存的旧配置值

#### Scenario: 重读 toolchain.md

- **WHEN** prototype-design 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `docs/toolchain.md`
- **AND** SHALL 使用读取到的工具链锁定方案执行 DESIGN 步骤

#### Scenario: 重读 CONTEXT.md

- **WHEN** explore, prototype-design, design, code, code-review 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `CONTEXT.md`
- **AND** SHALL 使用读取到的领域词汇表进行术语对齐

#### Scenario: 重读 detailed-design.md

- **WHEN** plan, code, code-review, api-test, e2e-test, integration-test 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `detailed-design.md`
- **AND** SHALL 仅提取当前阶段相关章节（如当前子变更所属设计域的章节）

#### Scenario: RELOAD 文件未被修改时跳过

- **WHEN** RELOAD 清单中某文件的 mtime 未发生变化且该文件已在当前会话中读取过
- **THEN** 变更级 agent MAY 跳过该文件的重读
- **AND** 以对话上下文中的缓存版本为准

### Requirement: RELOAD 清单由共享钩子文件统一定义

各阶段的 RELOAD 文件清单 SHALL 在 `.claude/skills/kflow-shared/phase-hooks.md` 中统一定义，各阶段 Skill 的 SKILL.md 不得自行增删。

#### Scenario: 集中式 RELOAD 清单

- **WHEN** 阶段的 RELOAD 文件清单需要修改
- **THEN** 修改 SHALL 在 `kflow-shared/phase-hooks.md` 中进行
- **AND** 各阶段 SKILL.md 无需同步修改
