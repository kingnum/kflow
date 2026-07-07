## Why

执行到编码、测试等下游阶段时，经常发现功能设计、原型设计或详细设计需要调整。当前缺少一个统一的设计变更记录与同步追踪机制——设计文档被修订后，缺乏显式记录来追踪哪些下游产物（plan、code、tests）已经同步更新、哪些尚未更新，导致用户无法判断当前各阶段产物的时效性和一致性。

## What Changes

- **三个设计目录各自建立 index.md**：`functional-designs/`（增强现有）、`prototype/`（新建）、`detailed-design/`（增强），均包含统一格式的"修订记录"表（版本、日期、修订类型、修订内容、影响功能点、触发阶段）
- **prototype/index.md 新建**：包含原型文件清单、页面清单、设计系统引用、修订记录
- **功能设计 index.md 合并表结构**：将现有的"需求变更记录"与"修订记录"合并为统一的"修订记录"表
- **详细设计增加修订记录**：在 `detailed-design.md`（单文件或目录化）中新增修订记录
- **`.status.md` 新增"设计修订同步追踪"区**：每阶段独立确认列（plan/code/review/api-test/e2e-test/integ-test），各阶段完成后独立标记本阶段同步状态，消除频繁变更时的状态跟踪丢失
- **kflow-guide 集中检测设计修订意图**：新增 DESIGN_REVISION 模式，统一解析用户输入（"功能设计需调整"/"原型需调整"/"详细设计需调整"等）并分流到对应设计 Skill 的 REVISION 模式
- **各阶段 Skill 的 description 不添加无关触发词**：防止 Skill 匹配歧义

## Capabilities

### New Capabilities

- `design-change-record`: 设计变更记录核心机制——三个设计目录 index.md 中的统一修订记录表格式，以及 .status.md 中的设计修订同步追踪表（每阶段独立确认列），kflow-guide 的 DESIGN_REVISION 集中检测与分流路由
- `prototype-design-index`: prototype/index.md 规格——原型文件清单、页面清单、设计系统引用、修订记录

### Modified Capabilities

- `change-rollback`: .status.md 新增"设计修订同步追踪"区，回退流程中追加同步追踪行
- `functional-design-content`: functional-designs/index.md 中"需求变更记录"与"修订记录"合并为统一的"修订记录"表，增加"修订类型"列
- `devflow-guide`: kflow-guide SKILL.md 新增 DESIGN_REVISION 模式的触发词检测和分流路由
- `phase-file-reload`: 各阶段 RELOAD 列表增加 prototype/index.md 和 detailed-design/index.md

## Impact

- 设计文档模板: `docs/designs/templates/changes/{change}/functional-designs/index.md`
- 新增模板: `docs/designs/templates/changes/{change}/prototype/index.md`
- 详细设计模板: `docs/designs/templates/changes/{change}/detailed-design.md`
- 状态文件模板: `docs/designs/templates/changes/{change}/change-status.md`
- 运行时 Skill: `.claude/skills/kflow-guide/SKILL.md`
- 设计文档: `docs/designs/core-mechanisms/09-phase-hooks.md`
- 设计文档: `docs/designs/skills/kflow-explore.md`、`kflow-prototype-design.md`、`kflow-design.md`
- OpenSpec spec: `openspec/specs/change-rollback/spec.md`
