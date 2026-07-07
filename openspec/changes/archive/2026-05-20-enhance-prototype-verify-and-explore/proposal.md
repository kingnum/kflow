## Why

当前原型设计阶段的验证机制仅依赖"最小点击测试"（走通 1 个业务流程），验证覆盖不足；huashu-design 直接在主 Agent 上下文调用导致上下文膨胀；10 轮自审和验证轮次均采用"分工制"（每轮只审查部分维度），问题发现率不如"重复制"（每轮全维度独立审查）。功能设计阶段的功能点描述在下游阶段缺乏直观的可视化总览。

## What Changes

### 原型设计阶段

- **子代理委托调用 huashu-design**：DESIGN 步骤从直接 `Skill()` 调用改为 `Agent(subagent)` 子代理调用，prompt 读取自 `prototype/design-prompt.md` 文件。子代理独立上下文，避免 HTML 产物污染主 Agent 上下文。
- **新增原型设计提示词文件**：OPTIMIZE 步骤完成后将优化后的 prompt 完整输出到 `prototype/design-prompt.md`（含 7 个章节：项目背景、设计系统、菜单导航、页面规格、业务流程脚本、硬约束、高保真要求），经用户确认后作为 DESIGN 步骤的唯一输入。
- **新增导航合理性验证**：VERIFY 新增 6.3 节，5 轮子代理串行验证（页面可达性、返回/取消按钮语义、表单切换链、弹窗抽屉导航、跨页面流程闭环），每轮子代理执行全部 5 项检查。
- **Playwright 验证升级**：VERIFY 6.4 节从"最小点击测试"升级为 5 轮子代理串行全覆盖验证（页面可达性、按钮/链接全覆盖、表单全覆盖、弹窗抽屉全覆盖、端到端流程），每轮子代理执行全部 5 项检查。
- **10 轮自审模式变更**：prototype SELFREV 从"分工制"（Round 1-3 覆盖性、Round 4-7 可用性、Round 8-10 完整性）改为"重复制"（每轮全维度：覆盖性+一致性+可用性+完整性）。

### 功能设计阶段

- **新增功能结构树**：`functional-designs/index.md` 的"三、页面导航结构图"替换为"三、功能结构树"，以树状图展示模块→功能点层级，每个节点标注 FP-ID、优先级（P0/P1/P2）和简短功能描述，为下游阶段提供直观的功能全景。
- **10 轮自审模式变更**：explore SELFREV 从"分工制"（Round 1-3 结构性、Round 4-7 细节、Round 8-10 边界）改为"重复制"（每轮全维度：完整性+闭环性+必要性+清晰性）。

## Capabilities

### New Capabilities

- `prototype-subagent-delegation`: 子代理委托调用 huashu-design，prompt 来自 design-prompt.md 文件，独立上下文避免主 Agent 上下文膨胀
- `prototype-navigation-verification`: 5 轮子代理串行导航合理性验证（可达性+返回按钮+表单链+弹窗+闭环），每轮完整检查全部 5 项
- `prototype-playwright-5round-verification`: 5 轮子代理串行 Playwright 全覆盖验证（可达性+按钮+表单+弹窗+端到端流程），每轮完整检查全部 5 项
- `prototype-design-prompt-template`: 原型设计提示词文件模板（7 章节），OPTIMIZE 产出经用户确认后作为 DESIGN 输入
- `functional-structure-tree`: 功能设计阶段 index.md 中功能结构树（树状图+FP-ID+优先级+简述）

### Modified Capabilities

- `phase-self-review`: explore 和 prototype 的 10 轮自审从"分工制"改为"重复制"——每轮全维度独立审查，10 轮形成自然收敛
- `html-prototype-workflow`: DESIGN 步骤改为子代理委托调用，VERIFY 步骤新增导航合理性验证和 Playwright 5 轮验证，OPTIMIZE 步骤新增 design-prompt.md 文件输出
- `functional-design-content`: index.md "页面导航结构图"替换为"功能结构树"，新增 FP-ID/优先级/简述标注要求

## Impact

- **设计文档**: `docs/designs/skills/kflow-prototype-design.md`、`docs/designs/skills/kflow-explore.md`
- **技能实现**: `.claude/skills/kflow-prototype-design/SKILL.md`、`.claude/skills/kflow-explore/SKILL.md`
- **核心机制**: `docs/designs/core-mechanisms.md`（自审模式变更影响通用规则）
- **规格文件**: `openspec/specs/html-prototype-workflow/`、`openspec/specs/phase-self-review/`、`openspec/specs/functional-design-content/`
- **新增模板**: `prototype/design-prompt.md` 模板文件
