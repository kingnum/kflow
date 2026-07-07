## MODIFIED Requirements

### Requirement: 产品文档缺失检测与询问

kflow-init SHALL 在扫描发现产品级文档缺失时，通过 AskUserQuestion 询问用户是否通过代码逆向分析生成产品级文档草稿。

#### Scenario: 检测到产品文档缺失

- **WHEN** 项目 `docs/CONTEXT.md` 不存在或 `docs/designs/functional-designs/` 目录为空
- **THEN** 系统展示产品文档缺失清单
- **AND** 使用 AskUserQuestion 询问："检测到产品文档缺失，是否通过代码逆向分析生成产品级文档草稿？"
- **AND** 用户可选择「生成草稿」或「跳过」

#### Scenario: 产品文档已存在时跳过询问

- **WHEN** `docs/CONTEXT.md` 和 `docs/designs/functional-designs/` 均已存在
- **THEN** 系统不询问逆向分析
- **AND** 仅在项目画像中标注产品文档状态为 ✅

### Requirement: 产品文档草稿生成

系统 SHALL 基于逆向扫描结果生成产品级文档草稿，标注为 AI 生成待审核。

#### Scenario: 生成 CONTEXT.md 草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统从源码语义扫描中提取领域术语
- **AND** 为每个术语生成：定义（从上下文推断）、别名、边界
- **AND** 写入 `docs/CONTEXT.md` 草稿，标注 `> 由 AI 逆向分析生成，待人工审核`

#### Scenario: 生成产品设计入口草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统生成 `docs/designs/index.md` 草稿
- **AND** 包含：项目概述、功能模块导航表、技术设计文档索引、变更日志
- **AND** 标注生成来源

#### Scenario: 生成功能模块文档草稿

- **WHEN** L2 模块扫描完成
- **THEN** 系统为每个识别的模块生成 `docs/designs/functional-designs/{module}.md` 草稿
- **AND** 按功能模块以 kebab-case 命名（与产品菜单/功能分组对齐）
- **AND** 章节结构与变更级 functional-designs/part-NN.md 一致
- **AND** 标注生成来源

#### Scenario: 生成全景文档草稿

- **WHEN** L1+L2+L3 扫描完成
- **THEN** 系统生成 `docs/designs/technical-designs/architecture.md`（从目录结构推断架构模式）
- **AND** 生成 `docs/designs/technical-designs/data-model.md`（从 L3 实体扫描聚合）
- **AND** 生成 `docs/designs/technical-designs/api-catalog.md`（从 L3 路由扫描聚合）
- **AND** 每份文档标注生成来源

#### Scenario: 生成 service-guide.md 草稿（新增）

- **WHEN** 逆向扫描完成
- **THEN** 系统基于 L1 配置扫描生成 `docs/service-guide.md` 草稿
- **AND** 包含 dev 环境的项目类型、启动命令、端口、数据库信息
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** 标注生成来源

### Requirement: 用户审核确认

系统 SHALL 在所有草稿生成后，提交用户审核确认，未经确认不写入正式文档。

#### Scenario: 展示草稿供用户审核

- **WHEN** 所有草稿生成完成（含 service-guide.md 草稿）
- **THEN** 系统展示 7 类文档清单和每份文档的关键内容摘要
- **AND** 使用 AskUserQuestion 询问用户确认（可逐文档确认或一次性确认全部）
- **AND** 用户可选择「确认写入」「修改后写入」或「放弃」

#### Scenario: 用户确认后写入

- **WHEN** 用户确认文档草稿
- **THEN** 系统将确认的文档写入对应路径
- **AND** 更新项目画像 section 中的产品文档状态

#### Scenario: 用户放弃或跳过

- **WHEN** 用户选择跳过或放弃逆向分析
- **THEN** 系统不写入任何产品级文档
- **AND** 在项目画像中标注产品文档为 ❌ 不存在
- **AND** 提示用户后续可手动补充或重新执行 init
