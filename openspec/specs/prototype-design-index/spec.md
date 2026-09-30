# prototype-design-index Specification

## Purpose

定义产品级原型清单 `docs/designs/prototypes/manifest.md` 的内容规格，供下游阶段消费。包含产物组织方式、原型文件清单（含角色与来源变更）、页面清单、设计系统引用、共享资源清单和修订记录；变更级 `prototype/index.md` 已废弃。

## Requirements

### Requirement: 产品级原型清单 manifest.md 存在

每个有原型设计的变更 SHALL 使产品级原型清单 `docs/designs/prototypes/manifest.md` 存在并反映本变更的改动，清单 SHALL 供下游阶段消费。

#### Scenario: 原型设计阶段创建 index.md

- **WHEN** kflow-prototype-design 首次生成原型产物
- **THEN** 产品级 `docs/designs/prototypes/manifest.md` SHALL 被创建或更新（该清单即原型产物清单，变更级 `prototype/index.md` 已废弃）
- **AND** 变更级 `prototype-changes.md` SHALL 被创建并记录本次改动
- **AND** 产品级 `manifest.md` SHALL 作为下游阶段（plan、code、code-review、e2e-test）获取全产品原型文件列表的入口
- **AND** 变更级 `prototype-changes.md` SHALL 作为下游阶段获取本变更原型改动的入口

#### Scenario: 无原型设计的变更不创建

- **WHEN** 变更不涉及前端/UI（纯后端项目）
- **THEN** 产品级 `docs/designs/prototypes/manifest.md` SHALL NOT 因该变更被创建或修改
- **AND** 变更级 `prototype-changes.md` SHALL NOT 被创建

### Requirement: 原型文件清单

产品级原型清单 SHALL 包含产品级原型目录下所有文件的清单，每个文件标注角色与来源变更。

#### Scenario: 文件清单结构

- **WHEN** 产品级 `docs/designs/prototypes/manifest.md` 包含文件清单
- **THEN** 清单 SHALL 列出 `docs/designs/prototypes/` 下每个原型文件及其说明、角色、来源变更
- **AND** 角色标注 SHALL 为以下之一：entry（入口页面）/ page（独立页面）/ tokens（设计令牌）/ coverage（元素覆盖树）/ shared（共享资源）/ process（过程产物）
- **AND** 至少包含一个 entry 角色文件
- **AND** 可能包含：`screens/` 下的屏幕 HTML（角色为 page）、`components/` 与 `assets/`（角色为 shared）、`design-tokens.css`（角色为 tokens）
- **AND** 变更级 `element-coverage-tree.md`（角色为 coverage）与 `prototype-plan/`（角色为 process）SHALL NOT 计入产品级文件清单，改由变更级 `prototype-changes.md` 登记

#### Scenario: 文件版本独立标注

- **WHEN** 原型文件清单中标注版本
- **THEN** 每个文件的版本号 SHALL 独立标注
- **AND** 与清单自身版本号不绑定

### Requirement: 页面清单

产品级原型清单 SHALL 包含所有页面的清单，每个页面标注对应的原型 HTML 文件路径。

#### Scenario: 页面清单结构

- **WHEN** 产品级 `docs/designs/prototypes/manifest.md` 包含页面清单
- **THEN** 每个页面 SHALL 标注：页面名称、路由路径、对应原型 HTML 文件路径（相对 `docs/designs/prototypes/` 目录的实际路径）、所含区域列表
- **AND** 对应原型文件路径 SHALL 反映实际文件结构（可能为 `index.html` 内部锚点或 `screens/` 下的独立文件）

### Requirement: 设计系统引用

产品级原型清单 SHALL 包含设计系统引用，链接到 `docs/designs/prototypes/design-system/MASTER.md`。

#### Scenario: 设计系统引用结构

- **WHEN** 产品级 `docs/designs/prototypes/manifest.md` 包含设计系统引用
- **THEN** SHALL 列出以下设计系统属性及其值和来源章节：色彩方案、字体系统、间距系统、组件库引用
- **AND** 每个属性 SHALL 标注在 `docs/designs/prototypes/design-system/MASTER.md` 中的来源章节

#### Scenario: 设计系统尚未生成

- **WHEN** `docs/designs/prototypes/design-system/MASTER.md` 尚不存在
- **THEN** 设计系统引用节 SHALL 标注"⏳ 待生成"
- **AND** 在原型设计阶段后续步骤中检查是否已生成并更新引用

### Requirement: 共享资源清单

产品级原型清单 SHALL 包含共享资源清单（如存在）。

#### Scenario: 共享资源清单结构

- **WHEN** 产品级原型产物包含共享资源子目录（如 `components/`、`assets/`）
- **THEN** SHALL 列出该子目录下所有文件及其用途说明

#### Scenario: 无共享资源时标注

- **WHEN** 产品级原型产物不包含共享资源子目录
- **THEN** 共享资源清单 SHALL 标注"不适用"

### Requirement: 修订记录

产品级原型清单 SHALL 包含与其他设计目录统一格式的"修订记录"表。

#### Scenario: 修订记录格式

- **WHEN** 产品级 `docs/designs/prototypes/manifest.md` 包含修订记录
- **THEN** 表格式 SHALL 与 functional-designs/index.md 和 detailed-design/index.md 中的修订记录一致
- **AND** 包含列：版本、日期、修订类型、修订内容、影响功能点、触发阶段
- **AND** 每次归档登记改动时 SHALL 追加一条修订记录
