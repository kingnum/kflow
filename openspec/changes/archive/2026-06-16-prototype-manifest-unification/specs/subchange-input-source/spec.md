## MODIFIED Requirements

### Requirement: 前端子变更输入源
系统 SHALL 为前端子变更定义以下输入源，以 `prototype/index.md` 为原型产物消费入口，排除过程产物。

#### Scenario: 前端子变更 plan 阶段输入
- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 输入源 SHALL 包含 `prototype/index.md`（原型产物清单，前端子变更任务编排的核心输入）、detailed-design.md（仅 API 契约章节）、functional-designs/（业务规则和表单项定义）、traceability.md
- **AND** 系统 SHALL 从 `prototype/index.md` 中获取页面清单（页面-文件映射）、设计令牌文件路径、元素覆盖树文件路径
- **AND** SHALL NOT 将 prototype/index.html、prototype/design-tokens.css、prototype/element-coverage-tree.md 作为输入表的独立条目
- **AND** SHALL NOT 将 prototype/design-prompt.md 作为输入源
- **AND** SHALL NOT 将 design-system/MASTER.md 作为输入源

#### Scenario: 前端子变更 code 阶段输入
- **WHEN** kflow-code 为前端子变更执行编码
- **THEN** 输入源 SHALL 包含 `prototype/index.md`（原型产物清单，前端子变更编码的核心输入）、detailed-design.md（API 契约与 mock 数据依据）、tasks.md（原型转译模板）、CONTEXT.md（组件命名）
- **AND** 系统 SHALL 从 `prototype/index.md` 中获取入口文件路径、页面 HTML 文件路径列表、设计令牌文件路径、元素覆盖树文件路径
- **AND** SHALL NOT 将 prototype/index.html、prototype/design-tokens.css、prototype/element-coverage-tree.md 作为输入表的独立条目
- **AND** SHALL NOT 将 prototype/design-prompt.md 或 design-system/MASTER.md 作为执行输入

#### Scenario: 前端子变更过程产物排除
- **WHEN** 前端子变更编码阶段引用原型产物
- **THEN** 系统 SHALL 仅使用 `prototype/index.md` 中角色为 entry/page/tokens/coverage/shared 的文件
- **AND** SHALL NOT 读取角色为 process 的文件（design-prompt.md、style-decision.md）
- **AND** SHALL NOT 读取 design-system/ 目录下文件（含 MASTER.md，设计系统说明文档）
- **AND** 设计令牌 SHALL 以 `prototype/index.md` 中角色为 tokens 的文件为唯一真实来源

### Requirement: 各阶段 Skill 输入表增加适用 SC 类型列
系统 SHALL 在所有阶段 Skill 设计文档的「输入要求」表中增加「适用SC类型」列，并将前端SC 的原型产物入口统一为 `prototype/index.md`。

#### Scenario: 输入表格式
- **WHEN** 阶段 Skill 设计文档定义输入要求
- **THEN** 输入表 SHALL 包含列：产物、文件、图例、适用SC类型、说明
- **AND** 「适用SC类型」列取值为：全部 / 后端子变更 / 前端子变更
- **AND** 前端子变更的原型产物 SHALL 统一以 `prototype/index.md`（✅ 必须，前端SC）为入口
- **AND** SHALL NOT 在输入表中单独列出 `prototype/index.html`、`prototype/design-tokens.css`、`prototype/element-coverage-tree.md`

#### Scenario: 条件产物标注
- **WHEN** 某产物仅适用于特定子变更类型
- **THEN** 「适用SC类型」列 SHALL 明确标注子变更类型
- **AND** 图例 SHALL 使用 🔶 条件
