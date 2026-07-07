## MODIFIED Requirements

### Requirement: 归档时合并功能设计和详细设计

系统 SHALL 在归档时将变更级的功能设计、详细设计和原型设计合并到产品级文档。

#### Scenario: 合并功能设计

- **WHEN** 归档变更
- **THEN** 系统从 functional-designs/ 提取功能点清单、需求描述、验收标准
- **AND** 按功能点的"所属页面与菜单"信息定位目标产品级目录 `docs/designs/functional-designs/{一级菜单}/`
- **AND** 按 FP-ID 匹配：已存在则替换更新对应 part-NN.md 中的功能点章节，不存在则追加
- **AND** 更新目标目录的 index.md 分册总览

#### Scenario: 合并详细设计

- **WHEN** 归档变更
- **THEN** 系统从 detailed-design.md 提取各章节内容
- **AND** 合并到 docs/designs/technical-designs/ 下对应 6 个文档（architecture.md、data-model.md、api-catalog.md、nfr-baseline.md、config-items.md、error-handling.md）

#### Scenario: 合并原型设计

- **WHEN** 归档变更
- **AND** 变更包含 `prototype/` 目录（原型设计阶段非跳过）
- **THEN** 系统将变更原型合并到 `docs/prototype/`
- **AND** 新屏幕复制到 `screens/`，修改屏幕用户确认后覆盖
- **AND** 新组件复制到 `components/`，新 CSS 变量追加到 `design-tokens.css`
- **AND** 更新 `index.html` 导航

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

### Requirement: 技术设计全景文档组织

系统 SHALL 将技术设计全景文档放入 docs/designs/technical-designs/ 目录，包含 6 个文件。

#### Scenario: 技术设计文档创建

- **WHEN** 归档时需要创建技术设计文档
- **THEN** 系统在 docs/designs/technical-designs/ 下创建
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
