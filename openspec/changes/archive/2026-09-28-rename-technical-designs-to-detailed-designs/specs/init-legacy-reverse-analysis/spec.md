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
- **AND** 包含：项目概述、功能模块导航表（指向 functional-designs 子目录或文件）、详细设计文档索引、变更日志
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
- **THEN** 系统生成 `docs/designs/detailed-designs/architecture.md`（从目录结构推断架构模式）
- **AND** 生成 `docs/designs/detailed-designs/data-model.md`（从 L3 实体扫描聚合）
- **AND** 生成 `docs/designs/detailed-designs/api-catalog.md`（从 L3 路由扫描聚合）
- **AND** 生成 `docs/designs/detailed-designs/config-items.md`（从 L1 配置扫描提取，标注骨架）
- **AND** 生成 `docs/designs/detailed-designs/error-handling.md`（从 L3 异常处理扫描提取，标注骨架）
- **AND** 每份文档标注生成来源

#### Scenario: 生成 service-guide.md 草稿

- **WHEN** 逆向扫描完成
- **THEN** 系统基于 L1 配置扫描生成 `docs/service-guide.md` 草稿
- **AND** 包含 dev 环境的项目类型、启动命令、端口、数据库信息
- **AND** test/staging/prod 环境标注「待后续补充」
- **AND** 标注生成来源
