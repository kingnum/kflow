## MODIFIED Requirements

### Requirement: HTML 原型产物

系统 SHALL 输出 HTML 原型到 `prototype/` 目录，并在原型产物清单（`prototype/index.md`）中声明实际生成的文件结构。

#### Scenario: 原型产物输出

- **WHEN** huashu-design 完成设计
- **THEN** 系统将产物写入 `docs/changes/{change}/prototype/` 目录
- **AND** `prototype/index.md` 中的入口文件 SHALL 指向实际入口（默认为 `index.html`，允许其他入口）
- **AND** 允许多文件架构（多个 HTML 文件 + 共享资源目录），不限制为单文件

#### Scenario: 产物验证

- **WHEN** 原型文件写入完成
- **THEN** 系统验证 `prototype/index.md` 已生成且包含「原型文件清单」
- **AND** 清单中至少包含一个角色为 entry 的文件
- **AND** 验证入口文件中引用的所有内部文件（`<a href>`、`<iframe src>` 等）均存在
- **AND** 文件间引用完整性检查通过后方可进入 VERIFY 步骤

### Requirement: huashu-design 子代理委托调用

系统 SHALL 在用户确认 design-prompt.md 后，通过子代理（Agent）委托调用 huashu-design Skill 执行 HTML 原型设计工作。

#### Scenario: 子代理委托调用
- **WHEN** OPTIMIZE 步骤完成且 `prototype/design-prompt.md` 已用户确认
- **AND** huashu-design Skill 已安装在项目中
- **THEN** 系统 SHALL 启动子代理 `Agent(subagent_type="claude")` 执行 huashu-design
- **AND** 子代理 SHALL 从 `prototype/design-prompt.md` 读取完整提示词
- **AND** 子代理 SHALL 调用 `Skill("huashu-design")` 生成原型
- **AND** SHALL NOT 在主 Agent 上下文中直接调用 `Skill("huashu-design")`

#### Scenario: 子代理完成回主 Agent
- **WHEN** 子代理完成 huashu-design 调用并写入文件
- **THEN** 主 Agent SHALL 验证 `prototype/index.md` 存在且清单中包含角色为 entry 的文件
- **AND** 主 Agent SHALL 验证入口文件中引用的所有内部文件均存在
- **AND** 验证通过后 SHALL 进入 VERIFY 步骤

#### Scenario: huashu-design 不可用
- **WHEN** 进入原型设计阶段 CHECK 步骤
- **AND** huashu-design Skill 未安装
- **THEN** 系统提示用户执行 `npx skills add alchaincyf/huashu-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞
