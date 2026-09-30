## MODIFIED Requirements

### Requirement: 后端子变更输入源
系统 SHALL 为后端子变更定义以下必选输入源。

#### Scenario: 后端子变更 plan 阶段输入
- **WHEN** kflow-plan 为后端子变更生成 tasks.md
- **THEN** 输入源 SHALL 包含：functional-designs/（业务规则与功能点）、detailed-design.md（数据模型章节 + 接口设计章节 + NFR 章节）、api-tests/（接口测试用例）、CONTEXT.md（命名对齐）、traceability.md（覆盖追踪）
- **AND** SHALL NOT 包含原型产物（`docs/designs/prototypes/`、变更级 `prototype-changes.md`、变更级 `element-coverage-tree.md`）

#### Scenario: 后端子变更 code 阶段输入
- **WHEN** kflow-code 为后端子变更执行编码
- **THEN** 输入源 SHALL 包含：functional-designs/（业务规则验证）、detailed-design.md（实现规格）、api-tests/（TDD 测试来源）、CONTEXT.md（代码命名）、tasks.md（任务清单）、service-guide.md（编译/运行配置）
- **AND** SHALL NOT 包含原型产物（`docs/designs/prototypes/`、变更级 `prototype-changes.md`、变更级 `element-coverage-tree.md`）

### Requirement: 前端子变更输入源
系统 SHALL 为前端子变更定义以下输入源，以产品级原型清单 `docs/designs/prototypes/manifest.md` 与变更级原型改动清单 `prototype-changes.md` 为原型产物消费入口，排除过程产物。

#### Scenario: 前端子变更 plan 阶段输入
- **WHEN** kflow-plan 为前端子变更生成 tasks.md
- **THEN** 输入源 SHALL 包含 `docs/designs/prototypes/manifest.md`（产品级原型产物清单）与变更级 `prototype-changes.md`（本变更原型改动清单）（原型产物清单，前端子变更任务编排的核心输入）、detailed-design.md（仅 API 契约章节）、functional-designs/（业务规则和表单项定义）、traceability.md
- **AND** 系统 SHALL 从 `docs/designs/prototypes/manifest.md` 中获取页面清单（页面-文件映射，角色 page）与设计令牌文件路径（角色 tokens），SHALL 依据变更级 `prototype-changes.md` 界定本变更涉及的原型文件
- **AND** 系统 SHALL 从变更级 `element-coverage-tree.md` 中获取元素覆盖树
- **AND** SHALL NOT 将 docs/designs/prototypes/index.html、docs/designs/prototypes/design-tokens.css 作为输入表的独立条目
- **AND** SHALL NOT 将 prototype-plan/design-prompt.md 作为输入源
- **AND** SHALL NOT 将 design-system/MASTER.md 作为输入源

#### Scenario: 前端子变更 code 阶段输入
- **WHEN** kflow-code 为前端子变更执行编码
- **THEN** 输入源 SHALL 包含 `docs/designs/prototypes/manifest.md`（产品级原型产物清单）与变更级 `prototype-changes.md`（本变更原型改动清单）（原型产物清单，前端子变更编码的核心输入）、detailed-design.md（API 契约与 mock 数据依据）、tasks.md（原型转译模板）、CONTEXT.md（组件命名）
- **AND** 系统 SHALL 从 `docs/designs/prototypes/manifest.md` 中获取入口文件路径（角色 entry）、页面 HTML 文件路径列表（角色 page）与设计令牌文件路径（角色 tokens），SHALL 依据变更级 `prototype-changes.md` 界定本变更改动的原型文件
- **AND** 系统 SHALL 从变更级 `element-coverage-tree.md` 中获取元素覆盖树
- **AND** SHALL NOT 将 docs/designs/prototypes/index.html、docs/designs/prototypes/design-tokens.css 作为输入表的独立条目
- **AND** SHALL NOT 将 prototype-plan/design-prompt.md 或 design-system/MASTER.md 作为执行输入

#### Scenario: 前端子变更过程产物排除
- **WHEN** 前端子变更编码阶段引用原型产物
- **THEN** 系统 SHALL 仅使用 `docs/designs/prototypes/manifest.md` 中角色为 entry/page/tokens/shared 的文件、变更级 `prototype-changes.md` 声明的本变更改动，以及变更级 `element-coverage-tree.md`
- **AND** SHALL NOT 读取角色为 process 的文件（prototype-plan/design-prompt.md、prototype-plan/style-decision.md）
- **AND** SHALL NOT 读取 design-system/ 目录下文件（含 MASTER.md，设计系统说明文档）
- **AND** 设计令牌 SHALL 以 `docs/designs/prototypes/design-tokens.css`（`docs/designs/prototypes/manifest.md` 中角色为 tokens 的文件）为唯一真实来源

### Requirement: 各阶段 Skill 输入表增加适用 SC 类型列
系统 SHALL 在所有阶段 Skill 设计文档的「输入要求」表中增加「适用SC类型」列，并将前端SC 的原型产物入口统一为产品级 `docs/designs/prototypes/manifest.md` 与变更级 `prototype-changes.md`。

#### Scenario: 输入表格式
- **WHEN** 阶段 Skill 设计文档定义输入要求
- **THEN** 输入表 SHALL 包含列：产物、文件、图例、适用SC类型、说明
- **AND** 「适用SC类型」列取值为：全部 / 后端子变更 / 前端子变更
- **AND** 前端子变更的原型产物 SHALL 统一以 `docs/designs/prototypes/manifest.md`（✅ 必须，前端SC）与变更级 `prototype-changes.md`（✅ 必须，前端SC）为入口
- **AND** SHALL NOT 在输入表中单独列出 `docs/designs/prototypes/index.html`、`docs/designs/prototypes/design-tokens.css`、变更级 `element-coverage-tree.md`

#### Scenario: 条件产物标注
- **WHEN** 某产物仅适用于特定子变更类型
- **THEN** 「适用SC类型」列 SHALL 明确标注子变更类型
- **AND** 图例 SHALL 使用 🔶 条件
