## MODIFIED Requirements

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
- **AND** 对于 #3（功能设计文档），前后端项目检测子目录数量，纯后端项目检测 .md 文件数量
- **AND** 对于 #4-#7，额外检测新增的 config-items.md 和 error-handling.md 是否存在，作为 completeness 标记（不影响通过/不通过判断）

#### Scenario: 技术设计文档完整性标记

- **WHEN** 检测 #4-#7 号技术设计文档
- **THEN** 系统侧带检测 config-items.md 和 error-handling.md 存在性
- **AND** 如缺失则标注"⚠️ 建议补充"，不阻塞主流程

## ADDED Requirements

### Requirement: 功能设计文档目录化检测

对前后端项目，#3 功能设计文档的检测逻辑 SHALL 从文件计数改为子目录计数。

#### Scenario: 前后端项目检测

- **WHEN** 项目类型为前后端项目
- **AND** 检测 #3 功能设计文档
- **THEN** 系统检测 `docs/designs/functional-designs/` 下是否存在至少一个子目录
- **AND** 各子目录内是否包含 index.md
- **AND** 状态标注为"✅ N个模块" 或 "❌ 不存在"

#### Scenario: 纯后端项目检测

- **WHEN** 项目类型为纯后端项目
- **AND** 检测 #3 功能设计文档
- **THEN** 系统检测 `docs/designs/functional-designs/` 下是否存在 .md 文件
- **AND** 状态标注为"✅ N篇" 或 "❌ 不存在"
