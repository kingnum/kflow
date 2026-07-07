# 模板目录索引

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-05-05
> **更新时间**: 2026-05-28
> **总模板数**: 49（含 1 个已废弃）

本文档是 KFlow Skills 体系中所有阶段产物模板的索引入口。模板目录按镜像实际 `docs/` 输出结构组织，模板路径与产物路径形成直接映射。

---

## 一、目录组织

```
templates/
├── index.md                                   # 本文件：模板目录索引
├── changes/{change}/                           # 变更级模板（镜像 docs/changes/{change}/）
│   ├── functional-designs/                     #   功能设计文档
│   │   ├── index.md                            #     功能设计索引模板
│   │   └── part-NN.md                          #     功能设计分册模板
│   ├── api-tests/                              #   接口测试用例
│   │   ├── index.md                            #     接口测试索引模板
│   │   └── part-NN.md                          #     接口测试分册模板
│   ├── e2e-tests/                              #   E2E 测试用例
│   │   ├── index.md                            #     E2E 测试索引模板
│   │   └── part-NN.md                          #     E2E 测试分册模板
│   ├── integration-tests/                      #   集成测试用例
│   │   ├── index.md                            #     集成测试索引模板
│   │   └── part-NN.md                          #     集成测试分册模板
│   ├── integration/                            #   集成测试报告（镜像 test-reports/integration/）
│   │   ├── integration-round-report.md         #     集成测试轮次报告模板
│   │   ├── integration-summary.md              #     集成测试总结模板
│   │   ├── contract-error-report.md            #     接口契约错误报告模板
│   │   └── arch-assessment.md                  #     架构评估报告模板
│   ├── review-reports/                         #   交叉审查报告
│   │   ├── business-review.md                  #     业务视角审查报告模板
│   │   ├── technical-review.md                 #     技术视角审查报告模板
│   │   ├── security-review.md                  #     安全视角审查报告模板
│   │   ├── quality-review.md                   #     质量视角审查报告模板
│   │   └── review-synthesis.md                 #     审查综合报告模板
│   ├── self-reviews/                           #   自循环审查报告
│   │   └── review-round.md                     #     自审轮次报告模板
│   ├── change-status.md                        #   变更级状态文件模板
│   ├── change-tasks.md                         #   变更总任务清单模板
│   ├── detailed-design.md                      #   统一详细设计模板
│   ├── audit-report.md                         #   审计报告模板
│   ├── change-index.md                         #   变更管理索引模板
│   ├── migration-log.md                        #   数据库迁移记录模板
│   ├── traceability.md                         #   覆盖追溯矩阵模板
│   └── checkpoint.md                           #   checkpoint 文件模板
├── subchanges/{subchange}/                     # 子变更级模板（镜像 subchanges/{subchange}/）
│   ├── subchange-status.md                     #   子变更状态文件模板
│   ├── subchange-tasks.md                      #   子变更任务清单模板
│   ├── code-review.md                          #   代码审查报告模板
│   ├── api-round-report.md                     #   API 测试轮次报告模板
│   ├── api-summary.md                          #   API 测试总结模板
│   ├── e2e-round-report.md                     #   E2E 测试轮次报告模板
│   ├── e2e-summary.md                          #   E2E 测试总结模板
│   ├── fix-report.md                           #   缺陷修复报告模板
│   └── design-error-report.md                  #   设计错误报告模板
├── design-templates/                           # 产品级设计模板
│   ├── functional-designs/                     #   功能设计模板（镜像 docs/designs/functional-designs/）
│   │   ├── index.md                            #     菜单级索引模板（新）
│   │   ├── part-NN.md                          #     产品级分册模板（新）
│   │   ├── backend-domain.md                   #     纯后端简化模板（新）
│   │   └── module.md                           #     功能模块文档模板（⚠️ 已废弃，使用 index.md + part-NN.md 替代）
│   ├── technical-designs/                      #   技术设计模板（镜像 docs/designs/technical-designs/）
│   │   ├── architecture.md                     #     全景架构文档模板（已修订：增加配置项/错误处理索引）
│   │   ├── data-model.md                       #     全景数据模型文档模板（已修订：兼容性说明）
│   │   ├── api-catalog.md                      #     全景 API 目录模板（已修订：兼容性说明）
│   │   ├── nfr-baseline.md                     #     NFR 基线文档模板（已修订：兼容性说明）
│   │   ├── config-items.md                     #     配置项设计模板（新）
│   │   └── error-handling.md                   #     错误处理设计模板（新）
│   └── changelog.md                            #   产品级变更日志模板
├── docs/                                       # 项目级文档模板（镜像 docs/）
│   ├── service-guide.md                        #   项目服务指引模板
│   └── toolchain.md                            #   工具链配置模板
├── skills/                                     #   Skill 通用模板
│   └── SKILL-template.md                       #     阶段 Skill SKILL.md 通用模板
└── index.md                                   # 本文件
```

---

## 二、完整模板清单

### 变更级模板 (changes/{change}/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 1 | changes/{change}/change-status.md | .status.md（变更级） | kflow-explore / 多个阶段更新 | 抽取 |
| 2 | changes/{change}/change-tasks.md | tasks.md（变更级） | kflow-explore | 抽取 |
| 3 | changes/{change}/functional-designs/index.md | functional-designs/index.md | kflow-explore | 新建 |
| 4 | changes/{change}/functional-designs/part-NN.md | functional-designs/part-NN.md | kflow-explore | 新建 |
| 5 | changes/{change}/detailed-design.md | detailed-design.md | kflow-design | 抽取 |
| 6 | changes/{change}/review-reports/review-synthesis.md | cross-reviews/{timestamp}/synthesis.md | kflow-design | 抽取 |
| 7 | changes/{change}/self-reviews/review-round.md | self-reviews/{phase}/{YYYYMMDD}-{HHMMSS}.md | kflow-explore / kflow-prototype-design / kflow-design | 新建 |
| 8 | changes/{change}/review-reports/business-review.md | cross-reviews/{timestamp}/business-review.md | kflow-design | 新建 |
| 9 | changes/{change}/review-reports/technical-review.md | cross-reviews/{timestamp}/technical-review.md | kflow-design | 新建 |
| 10 | changes/{change}/review-reports/security-review.md | cross-reviews/{timestamp}/security-review.md | kflow-design | 新建 |
| 11 | changes/{change}/review-reports/quality-review.md | cross-reviews/{timestamp}/quality-review.md | kflow-design | 新建 |
| 12 | changes/{change}/api-tests/index.md | api-tests/index.md | kflow-design | 新建 |
| 13 | changes/{change}/api-tests/part-NN.md | api-tests/part-NN.md | kflow-design | 新建 |
| 14 | changes/{change}/e2e-tests/index.md | e2e-tests/index.md | kflow-design | 新建 |
| 15 | changes/{change}/e2e-tests/part-NN.md | e2e-tests/part-NN.md | kflow-design | 新建 |
| 16 | changes/{change}/integration-tests/index.md | integration-tests/index.md | kflow-design | 新建 |
| 17 | changes/{change}/integration-tests/part-NN.md | integration-tests/part-NN.md | kflow-design | 新建 |
| 18 | changes/{change}/audit-report.md | audit-report.md | kflow-audit | 抽取 |
| 19 | changes/{change}/change-index.md | docs/changes/index.md | kflow-archive | 抽取 |
| 20 | changes/{change}/migration-log.md | migrations/migration-log.md | kflow-code | 抽取 |
| 21 | changes/{change}/traceability.md | docs/changes/{change}/traceability.md | kflow-design | 新建 |
| 22 | changes/{change}/checkpoint.md | checkpoints/{timestamp}-checkpoint.md | kflow-resume | 抽取 |

### 集成测试模板 (changes/{change}/integration/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 23 | changes/{change}/integration/integration-round-report.md | test-reports/integration/round-{n}.md | kflow-integration-test | 抽取 |
| 24 | changes/{change}/integration/integration-summary.md | test-reports/integration/summary.md | kflow-integration-test | 抽取 |
| 25 | changes/{change}/integration/contract-error-report.md | test-reports/integration/fix-reports/contract-error-{timestamp}.md | kflow-integration-test | 新建 |
| 26 | changes/{change}/integration/arch-assessment.md | test-reports/integration/fix-reports/arch-assessment-{timestamp}.md | kflow-integration-test | 新建 |

### 子变更级模板 (subchanges/{subchange}/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 27 | subchanges/{subchange}/subchange-status.md | subchanges/{subchange}/.status.md | kflow-plan / 多个阶段更新 | 抽取 |
| 28 | subchanges/{subchange}/subchange-tasks.md | subchanges/{subchange}/tasks.md | kflow-plan | 抽取 |
| 29 | subchanges/{subchange}/code-review.md | subchanges/{subchange}/test-reports/review/code-review.md | kflow-code-review | 抽取 |
| 30 | subchanges/{subchange}/e2e-round-report.md | subchanges/{subchange}/test-reports/e2e/round-{n}.md | kflow-e2e-test | 抽取 |
| 31 | subchanges/{subchange}/fix-report.md | subchanges/{subchange}/test-reports/fix-reports/fix-{timestamp}.md | kflow-bug-fix | 抽取 |
| 32 | subchanges/{subchange}/api-round-report.md | subchanges/{subchange}/test-reports/api/round-{n}.md | kflow-api-test | 新建 |
| 33 | subchanges/{subchange}/api-summary.md | subchanges/{subchange}/test-reports/api/summary.md | kflow-api-test | 新建 |
| 34 | subchanges/{subchange}/e2e-summary.md | subchanges/{subchange}/test-reports/e2e/summary.md | kflow-e2e-test | 新建 |
| 35 | subchanges/{subchange}/design-error-report.md | subchanges/{subchange}/test-reports/fix-reports/design-error-{timestamp}.md | kflow-bug-fix | 新建 |

### 产品级设计模板 (design-templates/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 36 | design-templates/functional-designs/index.md | docs/designs/functional-designs/{menu}/index.md | kflow-archive | 新建 |
| 37 | design-templates/functional-designs/part-NN.md | docs/designs/functional-designs/{menu}/part-NN.md | kflow-archive | 新建 |
| 38 | design-templates/functional-designs/backend-domain.md | docs/designs/functional-designs/{domain}.md | kflow-archive | 新建 |
| 39 | design-templates/functional-designs/module.md | docs/designs/functional-designs/{module}.md | kflow-archive | ⚠️ 废弃 |
| 40 | design-templates/technical-designs/architecture.md | docs/designs/technical-designs/architecture.md | kflow-archive | 修订 |
| 41 | design-templates/technical-designs/data-model.md | docs/designs/technical-designs/data-model.md | kflow-archive | 修订 |
| 42 | design-templates/technical-designs/api-catalog.md | docs/designs/technical-designs/api-catalog.md | kflow-archive | 修订 |
| 43 | design-templates/technical-designs/nfr-baseline.md | docs/designs/technical-designs/nfr-baseline.md | kflow-archive | 修订 |
| 44 | design-templates/technical-designs/config-items.md | docs/designs/technical-designs/config-items.md | kflow-archive | 新建 |
| 45 | design-templates/technical-designs/error-handling.md | docs/designs/technical-designs/error-handling.md | kflow-archive | 新建 |
| 46 | design-templates/changelog.md | docs/designs/changelog.md | kflow-archive | 新建 |

### 项目级文档模板 (docs/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 47 | docs/service-guide.md | docs/service-guide.md | kflow-init（预生成）+ kflow-code（补充完善） | 抽取 |
| 48 | docs/toolchain.md | docs/toolchain.md | kflow-init | 抽取 |

### Skill 模板 (skills/)

| 序号 | 模板文件 | 对应产物 | 产出 Skill | 类型 |
|------|---------|---------|-----------|------|
| 49 | skills/SKILL-template.md | .claude/skills/{skill-name}/SKILL.md | skill-creator | 新建 |

---

## 三、模板类型说明

| 类型 | 说明 |
|------|------|
| 抽取 | 从现有 Skill spec 或 core-mechanisms/ 中提取内联模板，独立为模板文件 |
| 新建 | 原本缺少模板定义，全新创建的模板文件 |
| 补全 | 原有模板不完整，补充缺失章节 |
| 修订 | 已有模板内容调整（增加章节、兼容性说明等） |
| ⚠️ 废弃 | 已标记 `deprecated: true`，不再使用，保留作为历史参考 |

---

## 四、模板维护规则

1. 修改 Skill spec 的产物输出格式时，必须同步更新对应模板文件
2. 模板文件的版本号在 frontmatter 中维护
3. 模板文件的修订记录区记录每次变更的内容
4. 新增阶段产物时，本索引文件同步更新
5. 模板文件路径与 Skill spec 中的模板引用路径必须一致
6. 模板目录结构镜像实际 `docs/` 输出结构，查找时无需查索引表

---

## 五、使用说明

- Skill 执行时，读取对应模板文件作为产物输出格式指引
- 模板中的 `{placeholder}` 格式占位符由 Skill 在运行时填充
- 索引类模板（index.md）按照 `large-doc-splitting` spec 的 ≤30 规则组织
- 分册类模板（part-NN.md）包含本册覆盖范围摘要和详细条目定义
- 模板路径与产物路径直接映射：产物 `docs/service-guide.md` → 模板 `templates/docs/service-guide.md`
