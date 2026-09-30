## MODIFIED Requirements

### Requirement: 阶段执行前强制重读基础信息文件

每个阶段 Skill 在 PRE_HOOK 的 RELOAD 步骤中 SHALL 重新读取该阶段钩子配置表中定义的基础信息文件，不得使用对话上下文缓存中的旧版本。RELOAD 清单 SHALL 包含以下新增文件：

- prototype-design 阶段：新增 RELOAD `docs/designs/prototypes/manifest.md`（条件）、RELOAD `prototype-changes.md`（条件）
- design 阶段：新增 RELOAD `docs/designs/prototypes/manifest.md`（如存在）、RELOAD `prototype-changes.md`（如存在）、RELOAD `functional-designs/index.md`
- plan 阶段：新增 RELOAD `functional-designs/index.md`、RELOAD `functional-designs/part-NN.md`、RELOAD `docs/designs/prototypes/manifest.md`（条件，前端SC）、RELOAD `prototype-changes.md`（条件，前端SC）、RELOAD `api-tests/index.md`
- code 阶段：新增 RELOAD `CONTEXT.md`、RELOAD `docs/designs/prototypes/manifest.md`（条件，前端SC）、RELOAD `prototype-changes.md`（条件，前端SC）
- code-review 阶段：新增 RELOAD `docs/designs/prototypes/manifest.md`（条件，前端SC）、RELOAD `prototype-changes.md`（条件，前端SC）
- api-test、e2e-test、integration-test 阶段：新增 RELOAD `functional-designs/index.md`、RELOAD 目标设计目录 index.md 以获取最新修订记录
- e2e-test 阶段：新增 RELOAD `docs/designs/prototypes/manifest.md`（条件，前端SC）、RELOAD `prototype-changes.md`（条件，前端SC）

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

#### Scenario: 重读 functional-designs/index.md

- **WHEN** design、plan、code、code-review、api-test、e2e-test、integration-test 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `docs/changes/{change}/functional-designs/index.md`
- **AND** SHALL 检查修订记录表的最新版本和修订内容

#### Scenario: 重读产品级原型清单与变更级原型改动清单

- **WHEN** 原型设计、详细设计、计划、编码、代码审查、接口测试、E2E 测试阶段执行且产品级 `docs/designs/prototypes/manifest.md` 或变更级 `prototype-changes.md` 存在
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取产品级 `docs/designs/prototypes/manifest.md` 与变更级 `prototype-changes.md`
- **AND** SHALL 检查产品级清单中的文件清单与角色划分、页面清单，以及本变更的原型改动记录

#### Scenario: 重读 detailed-design 修订记录

- **WHEN** plan、code、code-review、api-test、e2e-test、integration-test 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `detailed-design.md` 或 `detailed-design/index.md`
- **AND** SHALL 检查其中的修订记录节以发现设计变更

#### Scenario: Plan 阶段 RELOAD 原型核心产物

- **WHEN** plan 阶段执行且当前子变更为前端子变更
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取产品级 `docs/designs/prototypes/manifest.md` 与变更级 `prototype-changes.md`
- **AND** SHALL NOT 读取 prototype-plan/design-prompt.md 或 design-system/MASTER.md

#### Scenario: Code 阶段 RELOAD CONTEXT.md
- **WHEN** code 阶段执行
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 `CONTEXT.md`
- **AND** SHALL 使用最新领域词汇表进行代码命名对齐

#### Scenario: E2E 测试阶段 RELOAD element-coverage-tree.md
- **WHEN** e2e-test 阶段执行且项目类型为前后端
- **THEN** 变更级 agent SHALL 在 PRE_HOOK 中重新读取 element-coverage-tree.md
- **AND** SHALL 使用树中的 🎯 状态节点和 TC-ID 映射验证 E2E 测试覆盖率
