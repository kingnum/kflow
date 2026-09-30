# Spec Delta

## MODIFIED Requirements

### Requirement: 原型设计修订模式检测

系统 SHALL 在 kflow-prototype-design 的 CHECK 步骤后检测本变更是否已做过原型工作（变更级 `prototype-changes.md` 是否存在），并据此选择新建模式或修订模式。

#### Scenario: 现有原型存在且用户带修订需求
- **WHEN** CHECK 步骤通过且变更级 `prototype-changes.md` 文件已存在
- **AND** 用户输入包含修订需求（如"调整原型"、"修改设计"、"改大按钮"等）
- **THEN** 系统 SHALL 进入修订模式分支
- **AND** 加载 `prototype-changes.md` 所记录的产品级 `docs/designs/prototypes/` 原型文件作为现有原型上下文
- **AND** 加载变更级 `prototype-plan/design-prompt.md` 作为已有设计约束
- **AND** 加载变更级 `prototype-changes.md` 作为已有改动记录
- **AND** 合并用户修订需求到 prompt 中
- **AND** 进入 DESIGN 步骤，委托调用底层原型 skill（如 huashu-design），传入修订指令

#### Scenario: 现有原型存在但用户无明确修订需求
- **WHEN** CHECK 步骤通过且变更级 `prototype-changes.md` 文件已存在
- **AND** 用户未表达明确的修订需求
- **THEN** 系统 SHALL 通过 AskUserQuestion 询问：「原型已存在，是否要调整？如需调整请描述修改内容。」
- **AND** 用户选择「要调整」→ 进入修订模式
- **AND** 用户选择「查看现有原型」→ 展示原型摘要，不修改

#### Scenario: 现有原型不存在
- **WHEN** CHECK 步骤通过但变更级 `prototype-changes.md` 文件不存在
- **THEN** 系统 SHALL 判定本变更未做过原型工作，走新建模式流程
- **AND** 按正常流程执行 INPUT → OPTIMIZE → DESIGN

### Requirement: 修订模式跳过 INPUT 和 OPTIMIZE

修订模式下 SHALL 跳过 INPUT 机械提取和 OPTIMIZE 设计转译步骤，直接使用已有约束并合并修订需求。

#### Scenario: 修订模式流程路径
- **WHEN** 系统进入修订模式
- **THEN** 系统 SHALL 跳过 INPUT 步骤（不重新从 functional-designs/ 提取）
- **AND** 系统 SHALL 跳过 OPTIMIZE 步骤（不重新生成 design-prompt.md）
- **AND** 系统 SHALL 直接读取变更级 `prototype-plan/design-prompt.md` 作为设计约束
- **AND** 系统 SHALL 读取变更级 `prototype-changes.md` 获取已有改动清单与改动前哈希
- **AND** 系统 SHALL 将用户修订需求附加到 DESIGN 步骤的 prompt 中

### Requirement: 修订模式复用有效工具链

修订模式委托调用的底层设计引擎 SHALL 由**有效工具链**决定，SHALL NOT 硬编码绑定某一具体设计引擎，也 SHALL NOT 在修订模式下重新执行工具链选择（除非有效工具链未锁定）。

#### Scenario: 修订模式复用已锁定工具链

- **WHEN** 修订模式进入 DESIGN 步骤
- **AND** 有效工具链已锁定（`docs/changes/{change}/toolchain.md` 或 `docs/toolchain.md` 的原型设计章节存在且 `status` 已锁定）
- **THEN** 系统 SHALL 直接复用该有效工具链执行修订，SHALL NOT 扫描 `.claude/skills/` 目录
- **AND** SHALL NOT 在该次修订中调用 AskUserQuestion 询问工具链

#### Scenario: 修订模式无已锁定工具链

- **WHEN** 修订模式进入 DESIGN 步骤
- **AND** 变更级与项目级均无已锁定的原型设计工具链章节
- **THEN** 系统 SHALL 执行一次最小化 TOOLCHAIN 选择（环境扫描 → 方案推荐 → 锁定）
- **AND** 如扫描结果中 `prototype-gen` 角色的 Skill 数量为 0，SHALL 标记阶段为「⚠️ 阻塞」并提示安装命令

### Requirement: 修订模式验证流程

修订模式下完成 DESIGN 后 SHALL 执行 BUILD 步骤的静态门控检查；导航合理性验证与 Playwright 全覆盖验证 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时执行。

#### Scenario: 修订模式后验证
- **WHEN** 修订模式 DESIGN 步骤完成（底层 skill 生成修改后的原型）
- **THEN** 系统 SHALL 执行 BUILD 步骤的静态门控检查（CDN 外部依赖扫描、交叉引用完整性、必检产物存在、清单与磁盘一致）
- **AND** 该变更选择「子代理自动审查验证」审查方式时，系统 SHALL 继续执行导航合理性验证（9.1）与 Playwright 验证（9.2）
- **AND** 该变更选择「人工审查」审查方式时，系统 SHALL 跳过导航合理性验证（9.1）与 Playwright 验证（9.2），直接进入 REVIEW 用户评审循环
- **AND** BUILD 门控不通过或验证不通过 → 返回 DESIGN 重新修订
- **AND** 全部检查通过 → 进入 REVIEW 用户评审循环
