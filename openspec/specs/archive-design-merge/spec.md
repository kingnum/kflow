# archive-design-merge Specification

## Purpose

归档时自动将变更级的功能设计文档与详细设计文档合并到产品级文档，按功能模块组织并去除草稿标记、标注变更溯源，确保产品文档随变更持续累积且可追溯。

## Requirements

### Requirement: 产品级文档按功能模块组织

系统 SHALL 将产品级功能设计文档按功能模块（前后端：一级菜单；纯后端：设计域）拆分为独立目录或文件。

#### Scenario: 创建索引入口
- **WHEN** 首次归档创建产品级文档
- **THEN** 系统创建 docs/designs/index.md 作为索引入口
- **AND** 索引文件列出所有功能模块（目录或文件）的链接和最后更新时间

#### Scenario: 新增功能模块（前后端项目）
- **WHEN** 归档变更涉及新的一级菜单
- **THEN** 系统创建 `docs/designs/functional-designs/{menu}/` 目录
- **AND** 目录包含 index.md + part-NN.md，结构与变更级 functional-designs 一致
- **AND** 文件章节结构与变更级 functional-designs/part-NN.md 一致

#### Scenario: 新增功能模块（纯后端项目）
- **WHEN** 归档变更涉及新的设计域且项目为纯后端
- **THEN** 系统创建 `docs/designs/functional-designs/{domain}.md`
- **AND** 使用 backend-domain-template 简化模板

#### Scenario: 更新已有功能模块
- **WHEN** 归档变更涉及已有功能模块
- **THEN** 系统定位对应目录或文件
- **AND** 按 FP-ID 匹配：已存在则替换更新，不存在则追加

### Requirement: 详细设计全景文档组织

系统 SHALL 将详细设计全景文档放入 docs/designs/detailed-designs/ 目录，包含 6 个文件。

#### Scenario: 技术设计文档创建
- **WHEN** 归档时需要创建详细设计文档
- **THEN** 系统在 docs/designs/detailed-designs/ 下创建
- **AND** 包含 architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md

### Requirement: 草稿标记去除

系统 SHALL 在首次归档合并时自动去除 AI 逆向分析生成的草稿标记。

#### Scenario: 检测草稿标记
- **WHEN** 归档 MERGE 步骤匹配到目标产品文档
- **THEN** 系统检测目标文档是否包含「由 AI 逆向分析生成」草稿标记
- **AND** 若包含，进入首次合并流程

#### Scenario: 首次合并去草稿
- **WHEN** 目标文档包含草稿标记且为首次正式内容合并
- **THEN** 系统将草稿标记替换为正式来源标注（来源变更 + 归档时间）
- **AND** 移除文档顶部的草稿提示语
- **AND** 合并变更级内容到对应章节

#### Scenario: 非首次合并
- **WHEN** 目标文档不含草稿标记
- **THEN** 系统执行标准合并流程
- **AND** 每合并章节标注来源变更和归档时间

### Requirement: 变更溯源标注

系统 SHALL 在每个合并章节标注来源变更和归档时间。

#### Scenario: 标注来源变更
- **WHEN** 内容合并到产品级文档
- **THEN** 每个章节头部包含来源变更链接
- **AND** 包含归档时间和最后更新时间
- **AND** 格式为：来源变更 + 归档时间 + 最后更新

### Requirement: 合并冲突检测

系统 SHALL 在归档合并时检测模块冲突。

#### Scenario: 同模块已有内容
- **WHEN** 新归档变更涉及已有功能模块
- **THEN** 系统检测到冲突并提示用户
- **AND** 提供替换更新、增量追加、人工裁决三种处理选项

#### Scenario: 结构性冲突
- **WHEN** 新旧设计存在结构性冲突（如数据模型不兼容）
- **THEN** 系统标记为需人工裁决
- **AND** 详细展示冲突点

### Requirement: 变更记录维护

系统 SHALL 在归档时更新 changelog.md。

#### Scenario: 追加变更记录
- **WHEN** 归档完成
- **THEN** changelog.md 追加一条记录
- **AND** 记录包含归档日期、变更名称、涉及功能模块、主要变更摘要

#### Scenario: changelog 按年归档
- **WHEN** changelog.md 超过 500 行或年末
- **THEN** 系统将旧记录归档到 changelog-{year}.md
- **AND** changelog.md 仅保留当前年记录

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
