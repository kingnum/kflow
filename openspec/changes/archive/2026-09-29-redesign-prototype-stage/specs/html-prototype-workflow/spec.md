# Spec Delta

## MODIFIED Requirements

### Requirement: 原型子代理委托调用

系统 SHALL 在用户确认变更级 `prototype-plan/design-prompt.md` 后，通过子代理（Agent）按**有效工具链**委托调用设计引擎执行 HTML 原型设计工作；SHALL NOT 硬编码绑定某一具体设计引擎。有效工具链由 `docs/changes/{change}/toolchain.md` 的原型设计章节（存在时）覆盖 `docs/toolchain.md` 的原型设计章节解析得出。

#### Scenario: 子代理委托调用
- **WHEN** OPTIMIZE 步骤完成且 `docs/changes/{change}/prototype-plan/design-prompt.md` 已用户确认
- **AND** 有效工具链已锁定且其 `skills_used` 中列出的 Skill 在环境中均可用
- **THEN** 系统 SHALL 启动子代理 `Agent(subagent_type="claude")` 执行原型生成
- **AND** 子代理 SHALL 从 `docs/changes/{change}/prototype-plan/design-prompt.md` 读取完整提示词
- **AND** 子代理 SHALL 按有效工具链 `execution_order` 指定的 Skill 和顺序逐个调用
- **AND** 子代理 SHALL NOT 调用 `execution_order` 之外的设计 Skill
- **AND** 子代理 SHALL 将原型产物直接写入产品级 `docs/designs/prototypes/` 目录
- **AND** SHALL NOT 在主 Agent 上下文中直接调用设计引擎 Skill

#### Scenario: 子代理完成回主 Agent
- **WHEN** 子代理完成设计引擎调用并写入文件
- **THEN** 主 Agent SHALL 验证产品级 `docs/designs/prototypes/manifest.md` 存在且清单中包含角色为 entry 的文件
- **AND** 主 Agent SHALL 验证入口文件中引用的所有内部文件均存在
- **AND** 验证通过后 SHALL 进入 BUILD 步骤

#### Scenario: 无可用原型生成能力时阻塞
- **WHEN** TOOLCHAIN 步骤的复用判定结论为"需要重新选择"
- **AND** 环境扫描结果中 `prototype-gen` 角色的 Skill 数量为 0
- **THEN** 系统提示用户安装 `huashu-design` 或 `frontend-design`
- **AND** 阶段状态标记为 ⚠️ 阻塞，不跳过原型设计阶段

### Requirement: prompt 上下文组装

系统 SHALL 在委托调用前完成 prompt 上下文机械组装，作为 OPTIMIZE 步骤的输入基础。

#### Scenario: 组装必然存在的前置产物
- **WHEN** 组装 prompt 上下文
- **THEN** 系统从 `functional-designs/` 提取项目背景和 UI 功能点清单
- **AND** 指定产出路径为产品级 `docs/designs/prototypes/` 目录
- **AND** 变更级工作记录 SHALL 写入 `docs/changes/{change}/prototype-plan/` 目录

#### Scenario: 组装条件存在的产品级原型
- **WHEN** `docs/designs/prototypes/design-tokens.css` 存在
- **THEN** 系统将其 CSS 变量内容纳入设计约束
- **AND** 将 `docs/designs/prototypes/screens/` 下已有屏幕清单纳入上下文

#### Scenario: 组装条件存在的品牌资产
- **WHEN** 变更涉及具体品牌且有 brand-spec.md
- **THEN** 系统将品牌资产纳入 prompt

### Requirement: HTML 原型产物

系统 SHALL 将 HTML 原型直接输出到产品级 `docs/designs/prototypes/` 目录，并在产品级原型清单（`docs/designs/prototypes/manifest.md`）中声明实际生成的文件结构；变更级 SHALL NOT 维护原型副本目录，仅通过 `prototype-changes.md` 记录本变更对产品级原型的改动。

#### Scenario: 原型产物输出
- **WHEN** huashu-design 完成设计
- **THEN** 系统将产物直接写入产品级 `docs/designs/prototypes/` 目录
- **AND** `docs/designs/prototypes/manifest.md` 中的入口文件 SHALL 指向实际入口（默认为 `index.html`，允许其他入口）
- **AND** 允许多文件架构（多个 HTML 文件 + 共享资源目录），不限制为单文件
- **AND** SHALL NOT 在 `docs/changes/{change}/` 下维护原型文件副本目录

#### Scenario: 产物验证
- **WHEN** 原型文件写入完成
- **THEN** 系统验证 `docs/designs/prototypes/manifest.md` 已生成且包含「原型文件清单」
- **AND** 清单中至少包含一个角色为 entry 的文件
- **AND** 验证入口文件中引用的所有内部文件（`<a href>`、`<iframe src>` 等）均存在
- **AND** 文件间引用完整性检查通过后方可进入 VERIFY 步骤

### Requirement: 用户评审循环

系统 SHALL 在原型完成后通过 AskUserQuestion 进行用户评审。

#### Scenario: 确认通过
- **WHEN** 用户选择"确认通过"
- **THEN** 系统将原型设计阶段状态更新为 ✅ 完成
- **AND** SHALL 自动生成/更新产品级 `docs/designs/prototypes/manifest.md` 反映最终产物全貌
- **AND** kflow-guide 引导用户进入下一阶段

#### Scenario: 需要修订
- **WHEN** 用户选择"需要修订"
- **THEN** 系统收集用户反馈
- **AND** 将反馈作为修订要求重新调用 huashu-design
- **AND** 修订完成后再次进入评审
- **AND** 修订确认后 SHALL 重新更新产品级 `docs/designs/prototypes/manifest.md`

### Requirement: Playwright 5 轮全覆盖验证

系统 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时，在原型交付前使用 Playwright 执行 5 轮全覆盖验证，每轮启动独立子代理执行全部 5 项检查（页面可达性、按钮/链接全覆盖点击、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）；该变更选择「人工审查」时 SHALL 完全跳过该验证，不保留兜底轮次。

#### Scenario: 5 轮 Playwright 全覆盖验证
- **WHEN** 导航合理性验证（9.1 节）完成
- **AND** 该变更选择「子代理自动审查验证」审查方式
- **AND** Playwright 可用且原型为 flow demo 交互原型
- **THEN** 系统 SHALL 执行 5 轮子代理串行 Playwright 验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查
- **AND** 每轮验证 pageerror 数量 SHALL 为 0
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

#### Scenario: 人工审查路径跳过 Playwright 验证
- **WHEN** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 跳过 Playwright 5 轮全覆盖验证
- **AND** SHALL NOT 启动任何 Playwright 验证子代理
- **AND** 系统 SHALL 直接进入用户评审 REVIEW 步骤

#### Scenario: Playwright 不可用降级
- **WHEN** Playwright 未安装或执行失败
- **THEN** 系统降级为手动文件分析
- **AND** 在验证报告中记录降级原因

### Requirement: 导航合理性验证

系统 SHALL 仅在该变更选择「子代理自动审查验证」审查方式时，在 BUILD 步骤的 CDN 扫描（7.1）和交叉引用检查（7.2）通过后、Playwright 验证之前，执行 5 轮导航合理性验证（9.1 节），每轮启动独立子代理执行全部 5 项检查；该变更选择「人工审查」时 SHALL 完全跳过该验证。

#### Scenario: 5 轮导航合理性验证
- **WHEN** BUILD 步骤的 CDN 扫描（7.1）和交叉引用检查（7.2）通过
- **AND** 该变更选择「子代理自动审查验证」审查方式
- **THEN** 系统 SHALL 执行 5 轮子代理串行导航合理性验证
- **AND** 每轮子代理 SHALL 执行全部 5 项检查（页面可达性、返回/取消按钮合理性、表单切换链、弹窗/抽屉导航、跨页面流程闭环）
- **AND** 每轮子代理完成后主 Agent SHALL 读取报告并修复发现问题
- **AND** SHALL 完成全部 5 轮，不允许提前终止

#### Scenario: 人工审查路径跳过导航合理性验证
- **WHEN** 该变更选择「人工审查」审查方式
- **THEN** 系统 SHALL 跳过 5 轮导航合理性验证
- **AND** SHALL NOT 启动任何导航合理性验证子代理

### Requirement: design-prompt.md 文件输出

系统 SHALL 在 OPTIMIZE 步骤完成后，将优化后的完整提示词写入变更级 `docs/changes/{change}/prototype-plan/design-prompt.md` 文件（含 7 个章节），经用户确认后作为 DESIGN 步骤的唯一输入。

#### Scenario: OPTIMIZE 产出文件化
- **WHEN** OPTIMIZE 步骤完成（菜单树提取 + 页面元素穷举 + 业务流程脚本 + 硬约束注入）
- **THEN** 系统 SHALL 将完整 prompt 写入 `docs/changes/{change}/prototype-plan/design-prompt.md`
- **AND** 文件 SHALL 包含 7 个章节（项目背景、设计系统、菜单导航、页面规格、业务流程脚本、硬约束、高保真要求）
- **AND** 系统 SHALL NOT 在未生成该文件前进入 DESIGN 步骤

#### Scenario: 用户确认 design-prompt.md
- **WHEN** design-prompt.md 写入完成
- **THEN** 系统 SHALL 通过 AskUserQuestion 展示提示词摘要
- **AND** 文件状态初始为"待确认"
- **AND** 用户确认后文件状态更新为"已确认"并进入 DESIGN 步骤
- **AND** DESIGN 步骤完成后文件状态更新为"已执行"
