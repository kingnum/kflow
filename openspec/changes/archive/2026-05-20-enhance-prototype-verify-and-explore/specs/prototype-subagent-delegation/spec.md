# prototype-subagent-delegation Specification

## Purpose

定义原型设计阶段通过子代理（Agent）委托调用 huashu-design 的机制，prompt 来自 prototype/design-prompt.md 文件，子代理独立上下文避免主 Agent 上下文膨胀。

## ADDED Requirements

### Requirement: 子代理委托调用 huashu-design

系统 SHALL 在 DESIGN 步骤中通过子代理（Agent）委托调用 huashu-design Skill，而非直接在主 Agent 上下文中调用 Skill()。

#### Scenario: 子代理启动与传参

- **WHEN** DESIGN 步骤开始且 `prototype/design-prompt.md` 存在且已用户确认
- **THEN** 主 Agent SHALL 启动子代理 `Agent(subagent_type="claude", description="执行原型生成", prompt="读取 prototype/design-prompt.md 中的完整提示词，使用 Skill('huashu-design') 生成 HTML 交互原型到 prototype/ 目录。")`
- **AND** 子代理 prompt SHALL 包含读取 design-prompt.md + 调用 Skill("huashu-design") 的完整指令

#### Scenario: 子代理独立执行

- **WHEN** 子代理启动后
- **THEN** 子代理 SHALL 在其独立上下文中执行 huashu-design 的 placeholder → show → full pass 迭代
- **AND** huashu-design 内部迭代过程不被主 Agent 干预
- **AND** 子代理生成的 HTML 产物不污染主 Agent 上下文

#### Scenario: 子代理完成回主 Agent

- **WHEN** 子代理完成 huashu-design 调用并写入文件
- **THEN** 子代理 SHALL 返回结果摘要（成功/失败、生成页面数）
- **AND** 主 Agent SHALL 验证 `prototype/index.html` 存在且非空
- **AND** 主 Agent SHALL 验证所有内部文件引用目标文件存在

#### Scenario: 子代理执行失败

- **WHEN** 子代理执行失败或返回错误
- **THEN** 主 Agent SHALL 检查 `prototype/index.html` 是否仍可生成
- **AND** 如产物缺失 SHALL 重试一次子代理调用
- **AND** 重试仍失败 SHALL 标记阶段为 ⚠️ 阻塞并提示用户

### Requirement: design-prompt.md 作为唯一真相源

系统 SHALL 以 `prototype/design-prompt.md` 文件作为 DESIGN 步骤的 prompt 唯一来源，子代理从中读取完整提示词。

#### Scenario: 子代理读取 design-prompt.md

- **WHEN** 子代理启动后
- **THEN** 子代理 SHALL 使用 Read 工具读取 `docs/changes/{change}/prototype/design-prompt.md`
- **AND** 提取文件中全部 7 个章节内容作为 huashu-design 的 prompt 输入
- **AND** SHALL NOT 仅使用主 Agent 内存中传递的 prompt 摘要

#### Scenario: design-prompt.md 不存在

- **WHEN** DESIGN 步骤开始但 `prototype/design-prompt.md` 不存在
- **THEN** 系统 SHALL NOT 启动子代理
- **AND** 系统 SHALL 提示用户：需回到 OPTIMIZE 步骤生成 design-prompt.md
