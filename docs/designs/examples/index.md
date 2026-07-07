# KFlow Skills 附录示例 - 导航

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-14

---

## 示例清单

### 状态文件示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| 变更级状态文件示例 | [change-status.md](change-status.md) | 完整的变更级 `.status.md` 文件示例（含子变更进度矩阵） |
| 子变更状态文件示例 | [subchange-status.md](subchange-status.md) | 完整的子变更级 `.status.md` 文件示例（5 阶段表格） |
| 回退前状态文件示例 | [rollback-status.md](rollback-status.md) | 变更级 `.status.md` 展示 ⚠️ 需修订 状态 |

### 设计文档示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| 变更级统一详细设计示例 | [design-level-restructure.md](design-level-restructure.md) | 完整的变更级 detailed-design.md（含 NFR 章节、多子变更设计） |
| 子变更任务清单示例 | [subchange-tasks.md](subchange-tasks.md) | 完整的子变更 tasks.md（含 DoD 验收标准） |

### 测试与审查示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| 代码审查报告示例 | [code-review-report.md](code-review-report.md) | 代码审查报告（两视角并行审查，含闭环验证） |
| 架构评估报告示例 | [arch-assessment.md](arch-assessment.md) | 架构评估报告（连续3轮同用例失败自动触发，含多方案输出） |
| 集成测试用例示例 | [integration-tests.md](integration-tests.md) | 变更级集成测试用例文档 |

### 运维配置示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| 项目服务指引示例 | [service-guide.md](service-guide.md) | 项目服务指引（含多环境配置 dev/test/staging/prod） |
| 数据库迁移记录示例 | [migration-log.md](migration-log.md) | 数据库迁移记录文档 |
| 变更管理索引示例 | [change-index.md](change-index.md) | docs/changes/index.md 索引文件（含影响文件字段） |

### 其他示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| Skills 优化建议记录示例 | [skill-suggestion.md](skill-suggestion.md) | Skills 优化建议记录示例 |

### v1.5.0 新增示例

| 示例 | 文件 | 内容说明 |
|------|------|---------|
| 审计报告示例 | [audit-report.md](audit-report.md) | 七维度审计报告（含评分、问题分级、效率统计） |
| 工具链配置示例 | [toolchain.md](toolchain.md) | toolchain.md 配置（含 MCP/Skills 扫描、方案对比） |
| 集成测试修复报告示例 | [integration-fix-report.md](integration-fix-report.md) | 变更级缺陷修复报告（含四分法根因分类） |
| 产品级领域文档示例 | [product-domain-doc.md](product-domain-doc.md) | docs/designs/functional-designs/{module}.md（含功能+技术设计、来源标注） |
| 产品级索引入口示例 | [product-design-index.md](product-design-index.md) | docs/designs/index.md（含领域导航、全景文档、changelog） |

### v1.5.0 更新示例

| 更新示例 | 变更内容 |
|---------|---------|
| [change-status.md](change-status.md) | 使用新文件命名（functional-design.md / detailed-design.md） |
| [change-index.md](change-index.md) | 归档表新增"设计合并域"字段 |

### v1.6.0 更新示例

| 更新示例 | 变更内容 |
|---------|---------|
| [change-status.md](change-status.md) | 新增代码审查阶段行、服务刷新状态行；子变更进度矩阵增加代码审查列 |
| [rollback-status.md](rollback-status.md) | 新增代码审查阶段行、服务刷新状态行；子变更进度矩阵增加代码审查列 |
| [code-review-report.md](code-review-report.md) | 全面更新至 v1.6.0 格式：独立的 `kflow-code-review` Skill 输出 + 闭环验证记录 |

---

## 示例背景

以下示例基于一个电商平台初始化变更 `ecommerce-platform-init`，包含 3 个子变更：

- `user-auth`：用户认证模块（10 个功能点）
- `order-management`：订单管理模块（8 个功能点）
- `payment-integration`：支付集成模块（6 个功能点）

项目类型：前后端项目（包含 Vue 前端工程）

---

## v1.4.0 新增示例

| 新增示例 | 说明 |
|---------|------|
| [design-level-restructure.md](design-level-restructure.md) | 展示变更级统一详细设计格式，含 NFR 章节、按设计域组织 |
| [rollback-status.md](rollback-status.md) | 展示 ⚠️ 需修订 状态和阶段回退流程 |
| [code-review-report.md](code-review-report.md) | 展示代码审查子阶段的两视角报告格式 |
| [integration-tests.md](integration-tests.md) | 展示变更级集成测试用例和跨子变更接口契约验证 |
| [migration-log.md](migration-log.md) | 展示数据库迁移脚本和迁移执行记录 |

## v1.4.0 重大更新示例

| 更新示例 | 变更内容 |
|---------|---------|
| [change-status.md](change-status.md) | 子变更进度从"当前阶段"改为阶段完成矩阵 |
| [subchange-status.md](subchange-status.md) | 阶段表从 4 列调整为 5 列（接口单元测试 + E2E测试） |
| [subchange-tasks.md](subchange-tasks.md) | 每功能点增加 DoD 验收标准区块（4 维验收） |
| [service-guide.md](service-guide.md) | 扩展为多环境配置（dev/test/staging/prod） |
| [change-index.md](change-index.md) | 增加影响文件字段，支持跨变更冲突检测 |

### v1.7.0 更新示例

| 更新示例 | 变更内容 |
|---------|---------|
| [change-status.md](change-status.md) | 设计探索产物从 functional-design.md 改为 functional-designs/（目录化），api-tests/e2e-tests/integration-tests 改为目录化 |
| [subchange-status.md](subchange-status.md) | 门控检查点适配目录化结构（检查 index.md 替代单文件检查） |

---

## 状态文件格式参考

状态文件的格式模板定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md) 的「三、状态文件规范」章节。

以下示例展示了填充具体数据后的完整状态文件。

---

## 任务清单格式参考

任务清单的格式模板定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md) 的「四、任务清单规范」章节。

以下示例展示了填充具体数据后的完整任务清单文件。
