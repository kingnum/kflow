# Proposal: phase-review-mechanism-upgrade

## Why

当前 KFlow Skills 体系存在阶段边界模糊、设计阶段缺乏系统化自审机制、功能设计文档内容不足以支撑后续阶段等问题。同一设计层级的 explore/prototype/design 三个 Skill 均缺少量化的自我完善流程，导致设计质量依赖单次产出。此外，各阶段允许创建的文档边界不明确，存在越界创建文档的风险。

## What Changes

### 核心机制变更

- **新增 10 轮自循环审查机制**：kflow-explore、kflow-prototype-design、kflow-design 均强制执行 10 轮自审，每轮独立保存时间戳命名的审查记录，不允许提前终止
- **新增阶段边界强制规则**：每个阶段采用文档白名单模式，只允许创建输出产物表中列出的文件。信息不足时记录到 `skill-suggestion.md`，禁止自创新文档填补信息空缺
- **新增标准产物强制生成规则**：无论用户输入来源是什么（口述/文件/URL），各阶段必须生成完整的标准输出产物

### 功能设计文档升维

- **functional-designs/ 内容扩展**：新增页面结构/菜单层级、可执行操作清单、详细表单项定义（字段名/类型/校验规则/默认值）、业务规则（前置条件/校验规则/触发条件/后置结果）、业务流程闭环图
- 聚焦"用户能做什么、页面什么样、业务规则是什么"，为原型设计提供精确输入

### 目录结构调整

- **新增 `self-reviews/` 目录**：存放各设计阶段 10 轮自审记录，按阶段分子目录（explore/prototype/design）
- **重命名审查目录**：现有 `review-reports/` 改为 `cross-reviews/`，语义明确区分自审与交叉审查
- **时间戳命名**：审查记录统一以开始时间的 `{YYYYMMDD}-{HHMMSS}` 命名，文件为 `.md`，目录为目录
- **四视角审查存储调整**：每次四视角审查以时间戳命名的独立子目录保存，支持多次审查结果的完整保留

### 阶段边界明确化

- 明确 explore/prototype/design 三个设计阶段的 IN/OUT 边界
- explore 聚焦用户视角（页面/操作/表单/规则），design 聚焦技术视角（架构/数据模型/接口/NFR），prototype 聚焦视觉+交互
- 各阶段禁止越界输出内容

## Capabilities

### New Capabilities

- `phase-self-review`: 10 轮自循环审查机制，覆盖 explore/prototype/design 三个设计阶段，每轮独立记录，强制完成 10 轮，支持提前收敛但不提前终止
- `phase-boundary-enforcement`: 阶段边界强制规则，包括文档白名单模式、标准产物强制生成、越界禁止、信息不足时的 skill-suggestion.md 溢出路径
- `functional-design-content`: 功能设计文档内容升维，新增页面菜单、可执行操作、表单项定义、业务规则、业务流程闭环

### Modified Capabilities

- `review-closed-loop`: 审查目录结构从 `review-reports/` 调整为 `cross-reviews/`，新增 `self-reviews/` 目录，四视角审查结果以时间戳子目录存储
- `stage-doc-templates`: functional-designs/ 模板变更，新增页面结构、操作、表单、业务规则章节
- `doc-naming-convention`: 新增 self-reviews/ 和 cross-reviews/ 目录命名规范，审查记录采用 `{YYYYMMDD}-{HHMMSS}` 时间戳命名
- `design-level-restructure`: 阶段边界重新明确，explore/prototype/design 各自 IN/OUT 边界调整

## Impact

- **影响的 Skill 设计文档**: `kflow-explore.md`, `kflow-prototype-design.md`, `kflow-design.md` — 新增 10 轮自审流程、边界约束、内容要求
- **影响的机制文档**: `core-mechanisms.md` — 新增 10 轮自审机制章节、文档白名单约束、目录结构调整
- **影响的设计入口**: `index.md` — 版本号更新，目录结构调整
- **影响的模板**: functional-designs/ 模板需扩展，新增 self-review 轮次报告模板
- **影响的 specs**: 4 个新 spec + 4 个修改 spec
