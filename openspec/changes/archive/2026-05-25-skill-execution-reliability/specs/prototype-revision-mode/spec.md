## ADDED Requirements

### Requirement: 原型设计修订模式检测

系统 SHALL 在 kflow-prototype-design 的 CHECK 步骤后检测现有原型是否存在，并据此选择新建模式或修订模式。

#### Scenario: 现有原型存在且用户带修订需求

- **WHEN** CHECK 步骤通过且 `prototype/index.html` 文件已存在
- **AND** 用户输入包含修订需求（如"调整原型"、"修改设计"、"改大按钮"等）
- **THEN** 系统 SHALL 进入修订模式分支
- **AND** 加载 `prototype/index.html` 作为现有原型上下文
- **AND** 加载 `prototype/design-prompt.md` 作为已有设计约束
- **AND** 合并用户修订需求到 prompt 中
- **AND** 进入 DESIGN 步骤，委托调用底层原型 skill（如 huashu-design），传入修订指令

#### Scenario: 现有原型存在但用户无明确修订需求

- **WHEN** CHECK 步骤通过且 `prototype/index.html` 文件已存在
- **AND** 用户未表达明确的修订需求
- **THEN** 系统 SHALL 通过 AskUserQuestion 询问：「原型已存在，是否要调整？如需调整请描述修改内容。」
- **AND** 用户选择「要调整」→ 进入修订模式
- **AND** 用户选择「查看现有原型」→ 展示原型摘要，不修改

#### Scenario: 现有原型不存在

- **WHEN** CHECK 步骤通过但 `prototype/index.html` 文件不存在
- **THEN** 系统 SHALL 走新建模式流程
- **AND** 按正常流程执行 INPUT → OPTIMIZE → DESIGN

### Requirement: 修订模式跳过 INPUT 和 OPTIMIZE

修订模式下 SHALL 跳过 INPUT 机械提取和 OPTIMIZE 设计转译步骤，直接使用已有约束并合并修订需求。

#### Scenario: 修订模式流程路径

- **WHEN** 系统进入修订模式
- **THEN** 系统 SHALL 跳过 INPUT 步骤（不重新从 functional-designs/ 提取）
- **AND** 系统 SHALL 跳过 OPTIMIZE 步骤（不重新生成 design-prompt.md）
- **AND** 系统 SHALL 直接读取 `prototype/design-prompt.md` 作为设计约束
- **AND** 系统 SHALL 将用户修订需求附加到 DESIGN 步骤的 prompt 中

### Requirement: 修订模式下底层 skill 可替换

修订模式委托调用的底层原型 skill SHALL 不限于 huashu-design，可通过配置或检测选择可用的原型 skill。

#### Scenario: 底层 skill 检测

- **WHEN** 修订模式进入 DESIGN 步骤
- **THEN** 系统 SHALL 检测可用的原型 skill（扫描 `.claude/skills/` 目录）
- **AND** 优先使用 huashu-design（如存在）
- **AND** 如 huashu-design 不可用但有其他原型 skill，使用该替代 skill
- **AND** 如无任何可用原型 skill，标记阶段为「⚠️ 阻塞」并提示安装命令

### Requirement: 修订模式验证流程

修订模式下完成 DESIGN 后 SHALL 执行完整的 VERIFY 流程（CDN 扫描+交叉引用+导航验证+Playwright 验证）。

#### Scenario: 修订模式后验证

- **WHEN** 修订模式 DESIGN 步骤完成（底层 skill 生成修改后的原型）
- **THEN** 系统 SHALL 执行 VERIFY 步骤的全部检查（6.1 CDN 扫描 → 6.2 交叉引用 → 6.3 导航验证 → 6.4 Playwright 验证）
- **AND** 验证不通过 → 返回 DESIGN 重新修订
- **AND** 验证通过 → 进入 REVIEW 用户评审循环
