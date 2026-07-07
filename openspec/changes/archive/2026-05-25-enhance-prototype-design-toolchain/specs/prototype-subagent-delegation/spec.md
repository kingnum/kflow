## MODIFIED Requirements

### Requirement: 子代理委托调用 huashu-design

系统 SHALL 在 DESIGN 步骤的 5.2 GENERATE 子阶段中按 toolchain.md 锁定的工具链执行原型生成，而非硬编码调用 huashu-design。

#### Scenario: 子代理启动与传参

- **WHEN** DESIGN 步骤的 5.2 GENERATE 子阶段开始且 `prototype/design-prompt.md` 存在且已用户确认
- **AND** `prototype/style-decision.md` 存在
- **AND** toolchain 配置存在（`docs/toolchain.md`）
- **THEN** 主 Agent SHALL 启动子代理 `Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype/design-prompt.md + prototype/style-decision.md 中的完整提示词，按 toolchain.md 中指定的设计引擎和顺序生成 HTML 交互原型到 prototype/ 目录，并输出 design-system/MASTER.md。")`
- **AND** 子代理 prompt SHALL 包含读取 design-prompt.md + style-decision.md + toolchain.md 的完整指令
- **AND** 子代理 SHALL 严格按 toolchain.md 中 execution_order 指定的 Skill 顺序逐个调用
- **AND** 子代理 SHALL NOT 调用 toolchain.md 中未列出的任何设计 Skill

#### Scenario: 子代理独立执行

- **WHEN** 子代理启动后
- **THEN** 子代理 SHALL 在其独立上下文中执行设计引擎的迭代流程
- **AND** 设计引擎内部迭代过程不被主 Agent 干预
- **AND** 子代理生成的 HTML 产物不污染主 Agent 上下文

#### Scenario: 子代理完成回主 Agent

- **WHEN** 子代理完成设计引擎调用并写入文件
- **THEN** 子代理 SHALL 返回结果摘要（成功/失败、生成页面数）
- **AND** 主 Agent SHALL 验证 `prototype/index.html` 存在且非空
- **AND** 主 Agent SHALL 验证 `design-system/MASTER.md` 存在
- **AND** 主 Agent SHALL 验证所有内部文件引用目标文件存在
