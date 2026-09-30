## ADDED Requirements

### Requirement: 归档时合并功能设计和详细设计文档

系统 SHALL 在归档时将变更级的功能设计文档和详细设计文档合并到产品级文档。

#### Scenario: 合并功能设计
- **WHEN** 归档变更
- **THEN** 系统从 functional-designs/ 提取功能点清单、需求描述、验收标准
- **AND** 按功能点的"所属页面与菜单"信息定位目标产品级目录 `docs/designs/functional-designs/{一级菜单}/`
- **AND** 按 FP-ID 匹配：已存在则替换更新对应 part-NN.md 中的功能点章节，不存在则追加
- **AND** 更新目标目录的 index.md 分册总览

#### Scenario: 合并详细设计
- **WHEN** 归档变更
- **THEN** 系统从 detailed-design.md 提取各章节内容
- **AND** 合并到 docs/designs/detailed-designs/ 下对应 6 个文档（architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md）

### Requirement: 归档时登记原型改动

系统 SHALL 在归档时将本变更对产品级原型的改动登记到产品级原型清单，SHALL NOT 执行文件级原型合并。

#### Scenario: 登记原型改动
- **WHEN** 归档变更
- **AND** 该变更原型设计阶段非跳过
- **THEN** 系统 SHALL 将变更级 `prototype-changes.md` 中记录的改动登记到 `docs/designs/prototypes/manifest.md`
- **AND** SHALL NOT 复制或覆盖 `docs/designs/prototypes/` 下的原型文件（原型已在原型设计阶段直写）
- **AND** SHALL 在 `manifest.md` 中更新受影响产物的来源变更与最后更新时间

#### Scenario: 原型设计跳过的变更
- **WHEN** 归档变更
- **AND** 该变更原型设计阶段为 ⏭️ 跳过
- **THEN** 系统 SHALL NOT 修改 `docs/designs/prototypes/manifest.md`
- **AND** SHALL NOT 读取该变更的 `prototype-changes.md`

## REMOVED Requirements

### Requirement: 归档时合并功能设计和详细设计

**Reason**: 该需求同时覆盖功能设计、详细设计与原型合并三类产物；变更直写模型下原型合并已取消，需求按产物边界拆分为「归档时合并功能设计和详细设计文档」与「归档时登记原型改动」。
**Migration**: 功能设计与详细设计的合并行为不变，由「归档时合并功能设计和详细设计文档」承接（两个场景逐字保留）；原型相关行为由「归档时登记原型改动」承接——归档只把改动登记到 `docs/designs/prototypes/manifest.md`，不再合并或复制原型文件。
