## MODIFIED Requirements

### Requirement: 老项目逆向分析

kflow-init SHALL 在检测到产品文档缺失时，询问用户是否通过代码逆向扫描生成产品级文档草稿。详见 `init-legacy-reverse-analysis` spec。

**变更**：产品文档缺失检测条件从 `CONTEXT.md 不存在或 docs/designs/domains/ 为空` 改为 `docs/CONTEXT.md 不存在或 docs/designs/functional-designs/ 为空`。

### Requirement: 项目画像注入

kflow-init SHALL 向 CLAUDE.md 注入「项目画像」section，包含项目类型、技术栈摘要、源码结构、关键入口文件、产品文档状态。使用 marker 机制支持幂等更新。详见 `init-claude-md-injection` spec。

**变更**：产品文档状态检测从 7 项扩展为 8 项，新增 `docs/service-guide.md` 检测项。CONTEXT.md 检测路径从「项目根目录」改为 `docs/CONTEXT.md`。产品级设计文档路径从 `docs/designs/domains/` 改为 `docs/designs/functional-designs/`。

## ADDED Requirements

### Requirement: 产品文档 8 项检测

kflow-init SHALL 在项目画像扫描中检测以下 8 项产品文档的存在性：

| # | 文件 | 路径 |
|---|------|------|
| 1 | CONTEXT.md | docs/CONTEXT.md |
| 2 | 设计索引入口 | docs/designs/index.md |
| 3 | 功能设计文档 | docs/designs/functional-designs/ |
| 4 | 架构全景 | docs/designs/technical-designs/architecture.md |
| 5 | 数据模型 | docs/designs/technical-designs/data-model.md |
| 6 | API 目录 | docs/designs/technical-designs/api-catalog.md |
| 7 | NFR 基线 | docs/designs/technical-designs/nfr-baseline.md |
| 8 | 服务指引 | docs/service-guide.md |

#### Scenario: 产品文档 8 项检测

- **WHEN** kflow-init 执行项目画像扫描
- **THEN** 系统检测上述 8 项文件的存在性
- **AND** 将状态写入 CLAUDE.md 项目画像 section
