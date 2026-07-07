## Purpose

定义老项目产品文档缺失检测与逆向分析生成机制——kflow-init 在检测到产品级文档缺失时，通过 L1/L2/L3 三层逆向扫描生成产品文档草稿，经用户审核确认后写入。

## Requirements

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

### Requirement: 三层逆向扫描

系统 SHALL 按三层深度对项目代码进行逆向扫描，逐层提取信息用于生成产品级文档。

#### Scenario: L1 配置文件扫描

- **WHEN** 用户确认执行逆向分析
- **THEN** 系统扫描项目根目录的配置文件（package.json、pom.xml、build.gradle、requirements.txt、Cargo.toml 等）
- **AND** 提取：项目名称、语言、框架依赖、构建工具、数据库驱动/依赖
- **AND** 输出技术栈摘要

#### Scenario: L2 目录结构扫描

- **WHEN** L1 扫描完成
- **THEN** 系统扫描 src/ 子目录结构
- **AND** 识别模块划分（如 controllers/、models/、services/、routes/）
- **AND** 将模块映射为候选设计域

#### Scenario: L3 源码语义扫描

- **WHEN** L2 扫描完成
- **THEN** 系统读取路由定义文件，提取 API 端点（方法、路径）
- **AND** 读取数据模型/实体定义文件，提取实体名和关键字段
- **AND** 从关键注释和 README 提取领域术语
- **AND** 输出 API 目录、数据模型、领域术语表

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
