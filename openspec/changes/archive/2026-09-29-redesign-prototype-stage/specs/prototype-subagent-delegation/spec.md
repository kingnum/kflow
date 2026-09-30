## MODIFIED Requirements

### Requirement: 子代理按 toolchain 锁定执行

系统 SHALL 在 DESIGN 步骤的 6.2 GENERATE 子阶段中按有效工具链执行原型生成，而非硬编码调用 huashu-design。子代理 SHALL 直接将原型写入产品级原型目录 `docs/designs/prototypes/`，变更级 SHALL NOT 维护原型副本目录。

#### Scenario: 子代理启动与传参

- **WHEN** DESIGN 步骤的 6.2 GENERATE 子阶段开始且 `docs/changes/{change}/prototype-plan/design-prompt.md` 存在且已用户确认
- **AND** `docs/changes/{change}/prototype-plan/style-decision.md` 存在
- **AND** toolchain 配置存在（`docs/toolchain.md` 或变更级覆盖 `docs/changes/{change}/toolchain.md`）
- **THEN** 主 Agent SHALL 启动子代理 `Agent(subagent_type="claude", description="执行原型生成", prompt="读取 docs/changes/{change}/prototype-plan/design-prompt.md + docs/changes/{change}/prototype-plan/style-decision.md 中的完整提示词，按 docs/toolchain.md 中 execution_order 指定的设计引擎和顺序生成 HTML 交互原型，并输出 docs/designs/prototypes/design-system/MASTER.md。")`
- **AND** 子代理 prompt SHALL 包含读取 prototype-plan/design-prompt.md + prototype-plan/style-decision.md + toolchain 配置的完整指令
- **AND** 子代理 SHALL 严格按有效工具链中 execution_order 指定的 Skill 顺序逐个调用
- **AND** 子代理 SHALL NOT 调用有效工具链中未列出的任何设计 Skill

#### Scenario: 子代理写入产品级原型目录

- **WHEN** 子代理执行 GENERATE 子阶段
- **THEN** 子代理 SHALL 将原型文件写入产品级目录 `docs/designs/prototypes/`
- **AND** 页面文件 SHALL 写入 `docs/designs/prototypes/screens/`，共享组件 SHALL 写入 `docs/designs/prototypes/components/`，静态资源 SHALL 写入 `docs/designs/prototypes/assets/`
- **AND** 子代理 SHALL 更新 `docs/designs/prototypes/index.html` 全产品导航与 `docs/designs/prototypes/design-tokens.css`
- **AND** 子代理 SHALL NOT 在 `docs/changes/{change}/prototype/` 下创建原型副本目录
- **AND** 子代理 SHALL 在写入产品级原型前，将受影响文件的改动前副本备份到 `docs/changes/{change}/prototype-backup/`
- **AND** 子代理 SHALL 将本次改动登记到变更级 `docs/changes/{change}/prototype-changes.md`

#### Scenario: 子代理独立执行

- **WHEN** 子代理启动后
- **THEN** 子代理 SHALL 在其独立上下文中执行设计引擎的迭代流程
- **AND** 设计引擎内部迭代过程不被主 Agent 干预
- **AND** 子代理生成的 HTML 产物不污染主 Agent 上下文

#### Scenario: 子代理完成回主 Agent

- **WHEN** 子代理完成设计引擎调用并写入文件
- **THEN** 子代理 SHALL 返回结果摘要（成功/失败、生成页面数、改动文件数）
- **AND** 主 Agent SHALL 验证 `docs/designs/prototypes/index.html` 存在且非空
- **AND** 主 Agent SHALL 验证 `docs/designs/prototypes/design-system/MASTER.md` 存在
- **AND** 主 Agent SHALL 验证变更级 `docs/changes/{change}/prototype-changes.md` 已生成，且登记的改动条目覆盖本次产品级原型目录实际变更
- **AND** 主 Agent SHALL 验证所有内部文件引用目标文件存在

#### Scenario: 子代理执行失败

- **WHEN** 子代理执行失败或返回错误
- **THEN** 主 Agent SHALL 检查 `docs/designs/prototypes/index.html` 是否仍可生成
- **AND** 如产物缺失 SHALL 重试一次子代理调用
- **AND** 重试仍失败 SHALL 标记阶段为 ⚠️ 阻塞并提示用户
- **AND** SHALL NOT 自行切换到有效工具链中未列出的其他 Skill

### Requirement: design-prompt.md 作为唯一真相源

系统 SHALL 以 `docs/changes/{change}/prototype-plan/design-prompt.md` 文件作为 DESIGN 步骤的 prompt 唯一来源，子代理从中读取完整提示词。

#### Scenario: 子代理读取 design-prompt.md

- **WHEN** 子代理启动后
- **THEN** 子代理 SHALL 使用 Read 工具读取 `docs/changes/{change}/prototype-plan/design-prompt.md`
- **AND** 提取文件中全部 7 个章节内容作为设计引擎的 prompt 输入
- **AND** SHALL NOT 仅使用主 Agent 内存中传递的 prompt 摘要

#### Scenario: design-prompt.md 不存在

- **WHEN** DESIGN 步骤开始但 `docs/changes/{change}/prototype-plan/design-prompt.md` 不存在
- **THEN** 系统 SHALL NOT 启动子代理
- **AND** 系统 SHALL 提示用户：需回到 OPTIMIZE 步骤生成 prototype-plan/design-prompt.md
