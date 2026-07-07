## ADDED Requirements

### Requirement: L2.5 前端扫描后模块按菜单划分

对前后端项目，L2.5 扫描完成后系统 SHALL 按提取的一级菜单划分功能模块，而非按 L2 代码目录划分。

#### Scenario: 按菜单生成功能模块文档

- **WHEN** L2.5 提取到菜单结构
- **THEN** 系统按一级菜单创建 `docs/designs/functional-designs/{menu}/` 子目录
- **AND** 每个子目录包含 index.md + part-NN.md，与变更级 functional-designs 目录化结构一致

#### Scenario: 按设计域生成功能模块文档（纯后端）

- **WHEN** 项目为纯后端项目
- **THEN** 系统按 L2 扫描提取的设计域创建 `docs/designs/functional-designs/{domain}.md`
- **AND** 使用 `backend-domain-template` 简化模板

### Requirement: 前后端差异化内容填充

LEGACY 逆向分析 SHALL 按项目类型采用差异化内容填充策略。

#### Scenario: 前后端项目内容填充

- **WHEN** 前后端项目生成功能设计文档草稿
- **THEN** 系统从 L2.5 前端扫描结果提取页面与菜单、操作、表单项
- **AND** 从 L3 后端扫描提取业务规则、校验规则
- **AND** 无法推断的内容标注"待人工补充"或"待人工验证"

#### Scenario: 纯后端项目内容填充

- **WHEN** 纯后端项目生成功能设计文档草稿
- **THEN** 系统使用简化模板，从 L2/L3 提取设计域、API 端点、数据实体
- **AND** 从代码注解提取校验规则、调用约束
- **AND** UX 密集型字段不再出现（被替换章节覆盖）

## MODIFIED Requirements

### Requirement: 产品文档草稿生成

系统 SHALL 基于逆向扫描结果生成产品级文档草稿，标注为 AI 生成待审核。

#### Scenario: 生成 CONTEXT.md 草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统从源码语义扫描中提取领域术语
- **AND** 为每个术语生成：定义（从上下文推断）、别名、边界
- **AND** 写入 `docs/CONTEXT.md` 草稿，标注 `> 由 AI 逆向分析生成，待人工审核`

#### Scenario: 生成产品设计入口草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统生成 docs/designs/index.md 草稿
- **AND** 包含：项目概述、功能模块导航表（指向 functional-designs 子目录或文件）、技术设计文档索引、变更日志
- **AND** 标注生成来源

#### Scenario: 生成功能模块文档草稿（前后端项目）

- **WHEN** L2.5 菜单扫描完成
- **THEN** 系统为每个一级菜单创建 `docs/designs/functional-designs/{menu}/` 目录
- **AND** 生成 index.md + part-NN.md，章节结构与变更级 functional-designs/part-NN.md 一致
- **AND** 标注生成来源

#### Scenario: 生成功能模块文档草稿（纯后端项目）

- **WHEN** L2 模块扫描完成且项目为纯后端
- **THEN** 系统为每个设计域生成 `docs/designs/functional-designs/{domain}.md` 草稿
- **AND** 使用 backend-domain-template 简化模板
- **AND** 标注生成来源

#### Scenario: 生成全景文档草稿

- **WHEN** L1+L2+L3 扫描完成
- **THEN** 系统生成 `docs/designs/technical-designs/architecture.md`（从目录结构推断架构模式）
- **AND** 生成 `docs/designs/technical-designs/data-model.md`（从 L3 实体扫描聚合）
- **AND** 生成 `docs/designs/technical-designs/api-catalog.md`（从 L3 路由扫描聚合）
- **AND** 生成 `docs/designs/technical-designs/config-items.md`（从 L1 配置扫描提取，标注骨架）
- **AND** 生成 `docs/designs/technical-designs/error-handling.md`（从 L3 异常处理扫描提取，标注骨架）
- **AND** 每份文档标注生成来源

#### Scenario: 生成 service-guide.md 草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统基于 L1 配置扫描生成 `docs/service-guide.md` 草稿
- **AND** 包含 dev 环境的项目类型、启动命令、端口、数据库信息
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** 标注生成来源

### Requirement: 产品文档缺失检测与询问

kflow-init SHALL 在扫描发现产品级文档缺失时，通过 AskUserQuestion 询问用户是否通过代码逆向分析生成产品级文档草稿。

#### Scenario: 检测到产品文档缺失

- **WHEN** 项目 `docs/CONTEXT.md` 不存在或 `docs/designs/functional-designs/` 目录为空（前后端项目：无子目录；纯后端项目：无 .md 文件）
- **THEN** 系统展示产品文档缺失清单
- **AND** 使用 AskUserQuestion 询问："检测到产品文档缺失，是否通过代码逆向分析生成产品级文档草稿？"
- **AND** 用户可选择「生成草稿」或「跳过」

#### Scenario: 产品文档已存在时跳过询问

- **WHEN** `docs/CONTEXT.md` 和 `docs/designs/functional-designs/` 均已存在且非空
- **THEN** 系统不询问逆向分析
- **AND** 仅在项目画像中标注产品文档状态为 ✅
