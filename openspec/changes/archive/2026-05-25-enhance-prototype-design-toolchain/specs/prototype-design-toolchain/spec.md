## ADDED Requirements

### Requirement: 原型设计工具链灵活性

系统 SHALL 在 `kflow-prototype-design` 阶段支持动态识别环境中可用的设计相关 Skills，组合为可行的工具链方案供用户选择，选定后锁定执行。

#### Scenario: 环境扫描设计 Skills

- **WHEN** `kflow-prototype-design` 进入原型设计阶段
- **THEN** 系统 SHALL 扫描 `.claude/skills/` 目录下所有设计相关 Skills
- **AND** 读取每个 Skill 的 SKILL.md 的 name + description 字段
- **AND** 按能力角色分类:
  - `prototype-gen`: 能生成 HTML 交互原型（如 huashu-design、frontend-design）
  - `design-system`: 能输出色板/字体/风格决策（如 ui-ux-pro-max）
  - `ux-review`: 能做 UX 规则审查（如 ui-ux-pro-max、huashu-design）
  - `code-gen`: 能生成生产级前端代码（如 frontend-design）
- **AND** 输出扫描结果到 `available-skills.json`（内部使用）

#### Scenario: 零 prototype-gen 能力阻塞

- **WHEN** 环境扫描结果中 `prototype-gen` 角色的 Skill 数量为 0
- **THEN** 系统 SHALL 标记阶段为 ⚠️ 阻塞
- **AND** 输出提示信息："未检测到能编写 HTML 原型的 Skill。请安装 huashu-design 或 frontend-design"
- **AND** 系统 SHALL NOT 跳过原型设计阶段

#### Scenario: 单一 prototype-gen 自动选择

- **WHEN** 环境扫描结果中 `prototype-gen` 角色的 Skill 数量为 1
- **THEN** 系统 SHALL 自动生成单一工具链方案
- **AND** 直接使用该方案进入 DESIGN 步骤，不询问用户

#### Scenario: 多个 prototype-gen 推荐方案

- **WHEN** 环境扫描结果中 `prototype-gen` 角色的 Skill 数量 ≥ 2
- **THEN** 系统 SHALL 根据扫描到的 Skill 及其角色组合生成 2-3 条工具链方案
- **AND** 每条方案标注：包含的 Skills、流程描述、优点、缺点、适用场景
- **AND** 通过 AskUserQuestion 展示方案供用户选择
- **AND** 方案数量 SHALL NOT 超过 3 个

#### Scenario: 用户选定工具链后锁定

- **WHEN** 用户在 AskUserQuestion 中选择一种工具链方案
- **THEN** 系统 SHALL 将选定方案写入 `docs/toolchain.md` 的原型设计章节
- **AND** 记录字段包含：change_name、selected_toolchain、skills_used、execution_order、decision_time、status
- **AND** DESIGN 步骤 SHALL 严格按 toolchain.md 中指定的 Skill 和顺序执行
- **AND** 系统 SHALL NOT 在执行过程中自行切换工具链

### Requirement: toolchain.md 为唯一执行依据

系统 SHALL 严格以 `docs/toolchain.md` 作为原型设计阶段调用 Skills 的唯一依据，禁止任何偏离。

#### Scenario: toolchain.md 缺失时阻塞

- **WHEN** DESIGN 步骤启动
- **THEN** 系统 SHALL 检查 `docs/toolchain.md` 是否存在
- **AND** 如不存在 SHALL 标记阶段为 ⚠️ 阻塞
- **AND** 提示："docs/toolchain.md 未定义。请先在 kflow-init 阶段生成或手动创建"

#### Scenario: 严格按 execution_order 逐个调用

- **WHEN** 系统读取 toolchain.md 中的 execution_order 字段
- **THEN** 系统 SHALL 按数组顺序逐个调用 skills_used 中列出的 Skill
- **AND** SHALL NOT 跳过 execution_order 中定义的任一 Skill
- **AND** SHALL NOT 在 execution_order 之外调用任何其他设计 Skill
- **AND** SHALL NOT 自行调整调用顺序

#### Scenario: 禁止运行时切换工具链

- **WHEN** DESIGN 步骤执行过程中某个 Skill 调用失败
- **THEN** 系统 SHALL 重试该 Skill 一次
- **AND** 重试仍失败 SHALL 标记阶段为 ⚠️ 阻塞并提示用户
- **AND** SHALL NOT 自行切换到 toolchain.md 中未列出的其他 Skill
- **AND** SHALL NOT 自行切换到 toolchain.md 中列出的其他备选 Skill（除非用户显式修改 toolchain.md）

### Requirement: 风格/布局推荐（STYLE 子阶段）

系统 SHALL 在正式生成原型之前，先推荐差异化风格/布局方向供用户选择，选定后锁定执行。

#### Scenario: 风格推荐子代理启动

- **WHEN** `prototype/design-prompt.md` 存在且状态为"已确认"
- **AND** 用户未在之前轮次中已选择风格（`prototype/style-decision.md` 不存在）
- **THEN** 系统 SHALL 启动一个子代理执行风格/布局推荐
- **AND** 子代理 SHALL 读取 design-prompt.md 中的项目背景、产品类型、目标用户
- **AND** 子代理 SHALL 推荐 3 个差异化风格方向

#### Scenario: 每个风格方向的内容

- **WHEN** 子代理生成风格推荐
- **THEN** 每个方向 SHALL 包含:
  - 风格名称 + 设计哲学描述（一句话）
  - 色彩方案（主色/背景色/文字色/强调色，含色值）
  - 字体系统（标题字体 + 正文字体）
  - 布局模式（如"顶部导航 + 卡片网格" / "侧边栏 + 列表详情"）
  - ASCII 线框图（页面结构示意，10 行以内）
  - 适用场景 + 不适用场景

#### Scenario: 用户选择风格

- **WHEN** 子代理完成风格推荐
- **THEN** 系统 SHALL 通过 AskUserQuestion 展示风格选项
- **AND** 每个选项的 preview 字段 SHALL 包含 ASCII 线框图 + 色彩方案
- **AND** 选项 SHALL 包含"需要更多方向"（回到推荐步骤重新生成）
- **AND** 选项 SHALL 包含"自行指定"（用户自由描述期望风格）

#### Scenario: 风格选择决策记录

- **WHEN** 用户选定一种风格
- **THEN** 系统 SHALL 写入 `prototype/style-decision.md`
- **AND** 文件 SHALL 包含：selected_style、style_description（设计哲学 + 色彩 + 字体 + 布局）、ascii_wireframe、decision_time
- **AND** GENERATE 子阶段 SHALL 将 style-decision.md 的内容注入到设计引擎的 prompt 中
