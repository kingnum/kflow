## RENAMED Requirements

- FROM: `### Requirement: 三个设计目录均含 index.md`
- TO: `### Requirement: 设计产物记录载体均含修订记录表`

## MODIFIED Requirements

### Requirement: 设计产物记录载体均含修订记录表

系统 SHALL 确保每个变更的设计产物载体均包含统一格式的修订记录表：变更级 `functional-designs/index.md`（已有，增强）、变更级 `detailed-design/index.md` 或 `detailed-design.md`（增强，含修订记录节）、产品级 `docs/designs/prototypes/manifest.md`（新增，含同格式修订记录表）。

#### Scenario: functional-designs/index.md 存在且含修订记录

- **WHEN** kflow-explore 生成功能设计产物
- **THEN** functional-designs/index.md SHALL 包含统一格式的"修订记录"表
- **AND** 修订记录表包含列：版本、日期、修订类型、修订内容、影响功能点、触发阶段

#### Scenario: 产品级原型清单由原型设计阶段创建

- **WHEN** kflow-prototype-design 生成原型产物
- **THEN** 产品级 `docs/designs/prototypes/manifest.md` SHALL 被创建或更新
- **AND** 包含原型文件清单、页面清单、设计系统引用、修订记录

#### Scenario: detailed-design 含修订记录

- **WHEN** kflow-design 生成详细设计产物
- **THEN** detailed-design.md（单文件）SHALL 包含"修订记录"节
- **AND** 或 detailed-design/index.md（目录化）SHALL 包含"修订记录"节
- **AND** 修订记录表格式与其他两个载体一致

### Requirement: 统一修订记录表格式

变更级 `functional-designs/index.md`、变更级 `detailed-design/index.md`（或 `detailed-design.md`）、产品级 `docs/designs/prototypes/manifest.md` 中的修订记录表 SHALL 使用同一格式。

#### Scenario: 修订记录表结构

- **WHEN** 上述任一载体包含修订记录表
- **THEN** 表 SHALL 包含以下列：版本（语义版本号）、日期（YYYY-MM-DD 或 YYYY-MM-DD HH:MM）、修订类型（枚举：初始版本/需求变更/业务规则/接口签名/数据模型/UI布局/交互行为/架构设计/配置项/其他）、修订内容（一句话描述）、影响功能点（FP-ID 列表，多个以逗号分隔）、触发阶段（触发此次修订的阶段 Skill 名称）

#### Scenario: 版本号递增规则

- **WHEN** 设计文档被修订
- **THEN** 版本号 SHALL 按语义化版本递增：结构性变更（大范围重写/架构变化）递增 Major、功能性变更（新增/修改功能点定义）递增 Minor、修正性变更（描述修正/格式调整）递增 Patch

#### Scenario: 同一变更中存在多种修订类型

- **WHEN** 修订类型枚举不足以描述变更性质
- **THEN** 选择"其他"作为修订类型
- **AND** 在修订内容中补充说明

### Requirement: .status.md 设计修订同步追踪

变更级 .status.md SHALL 包含"设计修订同步追踪"节，以表格形式追踪每次设计修订在各受影响阶段的同步状态。

#### Scenario: 同步追踪表结构

- **WHEN** .status.md 包含设计修订同步追踪节
- **THEN** 表 SHALL 包含以下列：序号、修订时间、修订目标（functional-designs / 产品级 `docs/designs/prototypes/` / detailed-design）、变更简述、影响范围、以及每受影响阶段的独立确认列（plan/code/review/api-test/e2e-test/integ-test）
- **AND** 每个阶段列的值 SHALL 为 ⏳（待同步）/✅（已同步）/—（不适用）
- **AND** 修订目标为产品级 `docs/designs/prototypes/` 时，修订 SHALL 经 `kflow-prototype-design` 的 REVISION 模式执行

#### Scenario: 设计修订后追加追踪行

- **WHEN** 设计修订完成且用户确认
- **THEN** 同步追踪表 SHALL 追加一行
- **AND** 所有阶段列初始值 SHALL 为 ⏳
- **AND** 不受影响的阶段列 SHALL 标记为 —

#### Scenario: 各阶段独立确认同步

- **WHEN** 受影响阶段完成执行
- **THEN** 该阶段 SHALL 在 POST_HOOK 中检查同步追踪表
- **AND** 确认本阶段产物已反映该修订后 SHALL 将本阶段列标记为 ✅
- **AND** 其他阶段列不受影响

#### Scenario: 频繁修订时不丢失追踪状态

- **WHEN** 存在多条未完成同步的追踪行
- **THEN** 每行独立追踪各自的状态
- **AND** 新修订追加新行而不修改已有行
- **AND** 各阶段按行确认各自的同步状态

#### Scenario: 所有适用阶段均已同步

- **WHEN** 某追踪行中所有适用列均为 ✅
- **THEN** 该修订视为已完全同步
- **AND** 不阻塞后续流程

### Requirement: kflow-guide 集中检测设计修订意图

kflow-guide SHALL 在其 description 中包含设计修订意图的触发词，并在 PARSE 阶段统一解析目标设计产物载体并分流到对应设计 Skill。

#### Scenario: 解析设计修订目标

- **WHEN** 用户输入匹配设计修订触发词（如"功能设计需调整"、"原型需调整"、"详细设计需调整"、"接口设计要改"、"修改设计文档"）
- **THEN** kflow-guide SHALL 解析为 DESIGN_REVISION 模式
- **AND** SHALL 根据关键词定位目标设计产物载体：含"功能"/"需求" → 变更级 functional-designs，含"原型"/"UI"/"交互" → 产品级 `docs/designs/prototypes/`，含"详细"/"接口"/"架构" → 变更级 detailed-design

#### Scenario: 分流到设计 Skill

- **WHEN** 目标设计产物载体确定为 functional-designs
- **THEN** kflow-guide SHALL 唤醒 kflow-explore（REVISION 模式）
- **AND** 当目标为产品级 `docs/designs/prototypes/` 时 SHALL 唤醒 kflow-prototype-design（REVISION 模式）
- **AND** 当目标为 detailed-design 时 SHALL 唤醒 kflow-design（REVISION 模式）

#### Scenario: 设计修订完成后返回

- **WHEN** 目标设计 Skill 的 REVISION 模式完成
- **THEN** kflow-guide SHALL 更新 .status.md 的"设计修订同步追踪"节
- **AND** SHALL 更新目标设计产物载体的修订记录：变更级 `functional-designs/index.md`、变更级 `detailed-design.md` 或 `detailed-design/index.md`、产品级 `docs/designs/prototypes/manifest.md`
- **AND** SHALL 询问用户是否立即回退并重执行受影响阶段
