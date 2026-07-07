# 实施任务清单：add-stage-doc-templates

## 1. 模板目录初始化

- [x] 1.1 创建 `docs/designs/templates/` 目录及五子目录（change/、subchange/、integration/、product/、infra/）
- [x] 1.2 创建 `docs/designs/templates/index.md` 模板索引入口（列出全部模板清单及关联 Skill）

## 2. 变更级模板 — 抽取已有模板（10 个）

- [x] 2.1 抽取 `change-status.md`（变更级 .status 文件模板）— 来源 core-mechanisms.md §3.1
- [x] 2.2 抽取 `change-tasks.md`（变更总任务清单模板）— 来源 core-mechanisms.md §4.1
- [x] 2.3 抽取 `detailed-design.md`（统一详细设计模板）— 来源 kflow-design.md
- [x] 2.4 抽取 `review-synthesis.md`（四视角审查综合报告模板）— 来源 kflow-design.md
- [x] 2.5 抽取 `audit-report.md`（审计报告模板）— 来源 kflow-audit.md
- [x] 2.6 抽取 `change-index.md`（变更管理索引模板）— 来源 kflow-archive.md
- [x] 2.7 抽取 `migration-log.md`（数据库迁移记录模板）— 来源 kflow-code.md
- [x] 2.8 抽取 `service-guide.md`（项目服务指引模板）— 来源 kflow-code.md

## 3. 变更级模板 — 创建新模板 + 补全（12 个）

- [x] 3.1 创建 `functional-designs/index.md`（功能设计索引模板）— 含变更概述、功能点逐条清单、依赖关系图
- [x] 3.2 创建 `functional-designs/part-NN.md`（功能设计分册模板）— 含功能行为矩阵、业务规则、交互约束
- [x] 3.3 创建 `api-tests/index.md`（接口测试索引模板）— 含接口逐条清单、用例统计
- [x] 3.4 创建 `api-tests/part-NN.md`（接口测试分册模板）— 含完整响应结构定义、HP/EP/EC 用例
- [x] 3.5 创建 `e2e-tests/index.md`（E2E 测试索引模板）— 含功能点→场景覆盖矩阵、验证类型分布
- [x] 3.6 创建 `e2e-tests/part-NN.md`（E2E 测试分册模板）— 含页面 DOM 验证步骤、修改后回查
- [x] 3.7 创建 `integration-tests/index.md`（集成测试索引模板）— 含跨子变更数据流矩阵、子变更级测试状态
- [x] 3.8 创建 `integration-tests/part-NN.md`（集成测试分册模板）— 含跨模块数据一致性验证
- [x] 3.9 创建 `business-review.md`（业务视角审查报告模板）
- [x] 3.10 创建 `technical-review.md`（技术视角审查报告模板）
- [x] 3.11 创建 `security-review.md`（安全视角审查报告模板）
- [x] 3.12 创建 `quality-review.md`（质量视角审查报告模板）

## 4. 子变更级模板 — 抽取已有模板（5 个）

- [x] 4.1 抽取 `subchange-status.md`（子变更 .status 文件模板）— 来源 core-mechanisms.md §3.2
- [x] 4.2 抽取 `subchange-tasks.md`（子变更任务清单模板）— 来源 kflow-plan.md
- [x] 4.3 抽取 `code-review.md`（代码审查报告模板）— 来源 kflow-code-review.md
- [x] 4.4 抽取 `e2e-round-report.md`（E2E 测试轮次报告模板）— 来源 kflow-e2e-qa.md
- [x] 4.5 抽取 `fix-report.md`（缺陷修复报告模板）— 来源 kflow-bug-fix.md

## 5. 子变更级模板 — 创建新模板（4 个）

- [x] 5.1 创建 `api-round-report.md`（API 测试轮次报告模板）— 与 E2E 同构但使用纯后端健康评分维度
- [x] 5.2 创建 `api-summary.md`（API 测试总结模板）
- [x] 5.3 创建 `e2e-summary.md`（E2E 测试总结模板）
- [x] 5.4 创建 `design-error-report.md`（设计错误报告模板）— 含排除实现/测试错误的理由、联动回退范围

## 6. 集成测试级模板（3 个）

- [x] 6.1 抽取 `integration-round-report.md`（集成测试轮次报告模板）— 来源 kflow-integration-test.md
- [x] 6.2 抽取 `integration-summary.md`（集成测试总结模板）— 来源 kflow-integration-test.md
- [x] 6.3 创建 `contract-error-report.md`（接口契约错误报告模板）— 含冲突三方对照表、修复决策记录

## 7. 产品级模板 — 创建新模板（6 个）

- [x] 7.1 创建 `domain-doc.md`（产品级领域文档模板）— 含来源标注机制
- [x] 7.2 创建 `architecture.md`（全景架构文档模板）
- [x] 7.3 创建 `data-model.md`（全景数据模型文档模板）
- [x] 7.4 创建 `api-catalog.md`（全景 API 目录模板）
- [x] 7.5 创建 `nfr-baseline.md`（NFR 基线文档模板）
- [x] 7.6 创建 `changelog.md`（产品级变更日志模板）— 按年归档

## 8. 基础设施级模板（3 个）

- [x] 8.1 抽取 `toolchain.md`（工具链配置模板）— 来源 kflow-init.md
- [x] 8.2 抽取 `checkpoint.md`（checkpoint 文件模板）— 来源 core-mechanisms.md §8.1
- [x] 8.3 创建 `arch-assessment.md`（架构评估报告模板）— 含多方案对比矩阵

## 9. Skill spec 引用更新（14 个文件）

- [x] 9.1 更新 `kflow-explore.md` — 输出产物表增加模板列，引用 functional-designs/ 模板；移除内联模板
- [x] 9.2 更新 `kflow-design.md` — 输出产物表增加模板列，引用 detailed-design / api-tests / e2e-tests / review 模板
- [x] 9.3 更新 `kflow-plan.md` — 输出产物表增加模板列，引用 subchange-tasks 模板
- [x] 9.4 更新 `kflow-code.md` — 输出产物表增加模板列，引用 service-guide / migration-log 模板
- [x] 9.5 更新 `kflow-code-review.md` — 输出产物表增加模板列，引用 code-review 模板
- [x] 9.6 更新 `kflow-e2e-qa.md` — 输出产物表增加模板列，引用 api-round-report / e2e-round-report / summary 模板
- [x] 9.7 更新 `kflow-bug-fix.md` — 输出产物表增加模板列，引用 fix-report / design-error-report 模板
- [x] 9.8 更新 `kflow-integration-test.md` — 输出产物表增加模板列，引用 integration-tests / contract-error / arch-assessment 模板
- [x] 9.9 更新 `kflow-audit.md` — 输出产物表增加模板列，引用 audit-report 模板
- [x] 9.10 更新 `kflow-archive.md` — 输出产物表增加模板列，引用 change-index / domain-doc 模板
- [x] 9.11 更新 `kflow-init.md` — 输出产物表增加模板列，引用 toolchain 模板
- [x] 9.12 更新 `kflow-resume.md` — 输出产物表增加模板列，引用 checkpoint 模板
- [x] 9.13 更新 `kflow-prototype-design.md` — 输出产物表增加模板列（prototype.pen 标记为 N/A）
- [x] 9.14 更新 `kflow-status.md` — 输出产物表增加模板列（会话输出标记为 N/A）

## 10. 核心机制文档更新

- [x] 10.1 更新 `core-mechanisms.md` §2.1 目录结构 — 反映 functional-designs/、api-tests/、e2e-tests/、integration-tests/ 目录化
- [x] 10.2 更新 `core-mechanisms.md` §2.2 命名规范 — 增加功能设计目录、分册文件、索引文件命名
- [x] 10.3 更新 `core-mechanisms.md` §2.3 文档拆分策略 — 补充按数量拆分（≤30）策略
- [x] 10.4 更新 `core-mechanisms.md` §3.4 门控规则 — 门控检查适配目录化结构（检查 index.md 替代单文件检查）

## 11. 设计文档入口更新

- [x] 11.1 更新 `docs/designs/index.md` — 增加模板目录章节和链接
- [x] 11.2 更新 `docs/designs/examples/index.md` — 补充新模板对应的示例引用（如有）

## 12. 最终验证

- [x] 12.1 验证所有模板文件 frontmatter 格式正确（YAML 可解析）
- [x] 12.2 验证所有 Skill spec 中模板引用路径正确（文件存在）
- [x] 12.3 验证 core-mechanisms.md 中门控规则与目录化结构一致
- [x] 12.4 验证 templates/index.md 列出的模板清单完整（与 specs 定义一致）
