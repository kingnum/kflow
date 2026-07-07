## MODIFIED Requirements

### Requirement: 阶段执行前强制重读基础信息文件

每个阶段 Skill 在 PRE_HOOK 的 RELOAD 步骤中 SHALL 重新读取该阶段钩子配置表中定义的基础信息文件，不得使用对话上下文缓存中的旧版本。RELOAD 清单 SHALL 包含以下新增文件：

- prototype-design 阶段：新增 RELOAD `prototype/index.md`
- design 阶段：新增 RELOAD `prototype/index.md`（如存在）、RELOAD `functional-designs/index.md`
- plan、code、code-review、api-test、e2e-test、integration-test 阶段：新增 RELOAD `prototype/index.md`（如存在，前后端项目）、RELOAD `functional-designs/index.md`、RELOAD 目标设计目录 index.md 以获取最新修订记录

#### Scenario: 重读 functional-designs/index.md

- **WHEN** design、plan、code、code-review、api-test、e2e-test、integration-test 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `docs/changes/{change}/functional-designs/index.md`
- **AND** SHALL 检查修订记录表的最新版本和修订内容

#### Scenario: 重读 prototype/index.md

- **WHEN** 原型设计、详细设计、计划、编码、代码审查、接口测试、E2E 测试阶段执行且 prototype/index.md 存在
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `docs/changes/{change}/prototype/index.md`
- **AND** SHALL 检查修订记录和设计系统引用

#### Scenario: 重读 detailed-design 修订记录

- **WHEN** plan、code、code-review、api-test、e2e-test、integration-test 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `detailed-design.md` 或 `detailed-design/index.md`
- **AND** SHALL 检查其中的修订记录节以发现设计变更
