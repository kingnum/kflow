## MODIFIED Requirements

### Requirement: 产品级原型目录

系统 SHALL 维护 `docs/designs/prototypes/` 作为产品级原型的唯一来源。

#### Scenario: 目录结构初始化
- **WHEN** 首次创建产品级原型
- **THEN** 系统创建 `docs/designs/prototypes/` 及 `index.html`、`manifest.md`、`design-tokens.css`、`design-system/MASTER.md`、`screens/`、`components/`、`assets/`
- **AND** `index.html` 为全产品导航，以卡片网格按功能模块分组

#### Scenario: design-tokens.css 定义
- **WHEN** 产品级原型首次创建
- **THEN** `docs/designs/prototypes/design-tokens.css` 包含色板、字号、间距、圆角、阴影的 CSS 变量
- **AND** 所有原型屏幕通过 `<link rel="stylesheet">` 引用此文件

### Requirement: 新变更原型引导

系统 SHALL 在新变更进入原型设计时加载产品级原型上下文，并 SHALL 以产品级原型目录作为本次变更的直接写入目标。

#### Scenario: 加载已有原型
- **WHEN** 新变更进入原型设计
- **AND** `docs/designs/prototypes/` 存在
- **THEN** 系统读取 `manifest.md`、`design-tokens.css`、`design-system/MASTER.md`、`screens/` 清单、`components/` 清单
- **AND** 将已有信息纳入委托 prompt 的设计约束
- **AND** 以 `docs/designs/prototypes/` 为写入目标，SHALL NOT 在变更级创建原型副本目录

#### Scenario: 首次原型设计
- **WHEN** 新变更进入原型设计
- **AND** `docs/designs/prototypes/` 不存在
- **THEN** 系统在 prompt 中标注"无已有设计令牌，请建立"
- **AND** 按首次设计执行

## ADDED Requirements

### Requirement: 产品级原型清单 manifest.md

系统 SHALL 维护 `docs/designs/prototypes/manifest.md` 作为全产品原型清单，登记产品级原型目录下的全部产物及其来源变更。

#### Scenario: 清单内容与结构
- **WHEN** `docs/designs/prototypes/manifest.md` 生成或更新
- **THEN** 清单 SHALL 列出产品级原型目录下的全部产物（导航入口 `index.html`、`screens/` 屏幕、`components/` 组件、`design-tokens.css`、`design-system/MASTER.md`、`assets/` 资源）
- **AND** 每个产物 SHALL 标注角色与来源变更
- **AND** 清单 SHALL 记录最后更新时间

#### Scenario: 清单与目录一致
- **WHEN** 产品级原型目录新增、修改或删除文件
- **THEN** `manifest.md` SHALL 在同一阶段内同步更新
- **AND** 清单声明的文件 SHALL 与磁盘实际文件一致

### Requirement: 变更直写产品级原型

系统 SHALL 采用变更直写模型维护产品级原型：变更 SHALL NOT 维护原型副本目录，SHALL 直接写入 `docs/designs/prototypes/`。

#### Scenario: 变更级仅保留工作记录
- **WHEN** 变更进入原型设计阶段
- **THEN** 变更级 SHALL 仅保留工作记录：`prototype-changes.md`、`prototype-backup/`、`prototype-plan/design-prompt.md`、`prototype-plan/style-decision.md`、`element-coverage-tree.md`、`self-reviews/prototype/`
- **AND** 变更级 SHALL NOT 创建 `index.html`、`screens/`、`components/`、`design-tokens.css` 等原型产物

#### Scenario: 改动前备份与记录
- **WHEN** 变更新增、修改或删除 `docs/designs/prototypes/` 中的文件
- **THEN** 修改或删除前 SHALL 将原文件备份到变更级 `prototype-backup/`
- **AND** SHALL 在变更级 `prototype-changes.md` 中按「文件路径 | 类型（新增/修改/删除）| 改动前哈希 | 说明」记录该改动

#### Scenario: 并发写入检测
- **WHEN** 写入 `docs/designs/prototypes/` 前比对 `prototype-changes.md` 中记录的改动前哈希
- **AND** 该文件当前哈希与记录的改动前哈希不一致
- **THEN** 系统 SHALL 提示"该文件已被其他变更修改"
- **AND** SHALL 交由用户裁决：基于新版本继续修改 / 覆盖 / 人工合并

## REMOVED Requirements

### Requirement: 原型合并

**Reason**: 变更直写模型下，变更在原型设计阶段已直接写入产品级目录 `docs/designs/prototypes/`，归档时不再执行"将变更级原型合并到产品级"的合并流程。
**Migration**: 删除归档原型合并流程；归档改为将本变更的原型改动登记到 `docs/designs/prototypes/manifest.md`。已归档变更的 `prototype/` 目录原地保留，不再回填产品级。
