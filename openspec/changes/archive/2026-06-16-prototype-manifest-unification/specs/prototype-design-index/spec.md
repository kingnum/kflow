## MODIFIED Requirements

### Requirement: prototype/index.md 存在

每个有原型设计的变更 SHALL 在 `prototype/` 目录下包含 `index.md` 文件，作为原型产物清单（Prototype Manifest），供下游阶段消费。

#### Scenario: 原型设计阶段创建 index.md

- **WHEN** kflow-prototype-design 首次生成原型产物
- **THEN** prototype/index.md SHALL 被创建
- **AND** 版本号 SHALL 设为 1.0.0
- **AND** index.md SHALL 作为下游阶段（plan、code、code-review、e2e-test）获取原型文件列表的唯一入口

#### Scenario: 无原型设计的变更不创建

- **WHEN** 变更不涉及前端/UI（纯后端项目）
- **THEN** prototype/index.md SHALL NOT 被创建

### Requirement: 原型文件清单

prototype/index.md SHALL 包含原型目录下所有文件的清单，每个文件标注角色。

#### Scenario: 文件清单结构

- **WHEN** prototype/index.md 包含文件清单
- **THEN** 清单 SHALL 列出每个原型文件及其说明、角色、版本
- **AND** 角色标注 SHALL 为以下之一：entry（入口页面）/ page（独立页面）/ tokens（设计令牌）/ coverage（元素覆盖树）/ shared（共享资源）/ process（过程产物）
- **AND** 至少包含一个 entry 角色文件
- **AND** 可能包含：page-*.html（多页面场景，角色为 page）、shared/（共享资源，角色为 shared）、nav-check-round-*.md、playwright-check-round-*.md、ux-check-round-*.md、contrast-check.md（角色为 process）

#### Scenario: 文件版本独立标注

- **WHEN** 原型文件清单中标注版本
- **THEN** 每个文件的版本号 SHALL 独立标注
- **AND** 与 index.md 自身版本号不绑定

### Requirement: 页面清单

prototype/index.md SHALL 包含所有页面的清单，每个页面标注对应的原型 HTML 文件路径。

#### Scenario: 页面清单结构

- **WHEN** prototype/index.md 包含页面清单
- **THEN** 每个页面 SHALL 标注：页面名称、路由路径、对应原型 HTML 文件路径（相对 prototype/ 目录的实际路径）、所含区域列表
- **AND** 对应原型文件路径 SHALL 反映实际文件结构（可能为 `index.html` 内部锚点或 `page-xxx.html` 等独立文件）

### Requirement: 设计系统引用

prototype/index.md SHALL 包含设计系统引用，链接到 design-system/MASTER.md。

#### Scenario: 设计系统引用结构

- **WHEN** prototype/index.md 包含设计系统引用
- **THEN** SHALL 列出以下设计系统属性及其值和来源章节：色彩方案、字体系统、间距系统、组件库引用
- **AND** 每个属性 SHALL 标注在 design-system/MASTER.md 中的来源章节

#### Scenario: 设计系统尚未生成

- **WHEN** design-system/MASTER.md 尚不存在
- **THEN** 设计系统引用节 SHALL 标注"⏳ 待生成"
- **AND** 在 VERIFY 步骤中检查是否已生成并更新引用

### Requirement: 修订记录

prototype/index.md SHALL 包含与其他设计目录统一格式的"修订记录"表。

#### Scenario: 修订记录格式

- **WHEN** prototype/index.md 包含修订记录
- **THEN** 表格式 SHALL 与 functional-designs/index.md 和 detailed-design/index.md 中的修订记录一致
- **AND** 包含列：版本、日期、修订类型、修订内容、影响功能点、触发阶段
