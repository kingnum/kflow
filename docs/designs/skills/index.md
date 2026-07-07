# KFlow Skills 详细规格 - 导航

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-14

---

## Skills 清单

| Skill 名称 | 阶段 | 归属层级 | 必须性 | 核心功能 | 详细文档 |
|-----------|------|---------|--------|---------|---------|
| `kflow-guide` | 流程指引 | — | 按需 | 意图识别、活跃变更检测、跨变更冲突检测 | [kflow-guide.md](kflow-guide.md) |
| `kflow-explore` | 设计探索 | 变更级 | 必须 | 需求澄清、功能点拆分、项目类型检测（不再划分子变更） | [kflow-explore.md](kflow-explore.md) |
| `kflow-prototype-design` | 原型设计 | 变更级 | 可选 | HTML 原型设计（委托 huashu-design）、用户评审确认 | [kflow-prototype-design.md](kflow-prototype-design.md) |
| `kflow-design` | 详细设计 | **变更级** | 必须 | 统一详细设计（含NFR）、四视角审查、子变更划分、测试用例文档、用户评审确认 | [kflow-design.md](kflow-design.md) |
| `kflow-plan` | 计划 | 子变更级 | 必须 | Checkbox 任务清单、DoD验收标准、功能点级全展开 | [kflow-plan.md](kflow-plan.md) |
| `kflow-code` | 编码 | 子变更级 | 必须 | TDD 流程、数据库迁移、跨变更冲突检测、多 Agent 并行编码 | [kflow-code.md](kflow-code.md) |
| `kflow-code-review` | 代码审查 | 子变更级 | 必须 | 两视角并行审查（安全+规范/质量+性能）、闭环验证 | [kflow-code-review.md](kflow-code-review.md) |
| `kflow-api-test` | 接口单元测试 | 子变更级 | 必须 | curl/HTTP 接口测试、健康评分、所有项目类型必须执行 | [kflow-api-test.md](kflow-api-test.md) |
| `kflow-e2e-test` | E2E测试 | 子变更级 | 前后端必须 | 浏览器自动化测试、仅前后端项目 | [kflow-e2e-test.md](kflow-e2e-test.md) |
| `kflow-bug-fix` | 缺陷修复 | 按需 | 按需 | 子变更级二分法根因分类路由、实现/测试错误修复 | [kflow-bug-fix.md](kflow-bug-fix.md) |
| `kflow-bug-triage` | 问题分诊 | — | 按需 | 四层溯源诊断、问题登记（bugs/）、路由决策（REVISION或bug-fix） | [kflow-bug-triage.md](kflow-bug-triage.md) |
| `kflow-integration-test` | 集成测试 | 变更级 | 必须 | 集成测试执行、内聚四分法修复循环、架构评估自动触发 | [kflow-integration-test.md](kflow-integration-test.md) |
| `kflow-status` | 状态总结 | — | 按需 | 未归档变更汇总、子变更进度矩阵 | [kflow-status.md](kflow-status.md) |
| `kflow-archive` | 归档 | 变更级 | 必须 | 变更归档、集成测试门控、索引更新、设计合并 | [kflow-archive.md](kflow-archive.md) |
| `kflow-audit` | 使用评估 | — | 归档门控+按需 | 七维度评估、审计报告、审计回退路由 | [kflow-audit.md](kflow-audit.md) |
| `kflow-init` | 环境初始化 | — | 按需 | 环境能力发现、工具推荐矩阵、toolchain.md 输出 | [kflow-init.md](kflow-init.md) |
| `kflow-resume` | 中断恢复 | — | 按需 | 通过变更名定位断点、按优先级链读取状态、调度阶段 Skill | [kflow-resume.md](kflow-resume.md) |

---

## 触发时机总览

| 触发场景 | 推荐 Skill | 项目类型 |
|---------|-----------|---------|
| 新功能、开始、创建、开发 | `kflow-explore` | 所有项目 |
| 继续、下一步 | 继续活跃变更（单活跃变更自动 resume） | 所有项目 |
| 继续 {change}、恢复 {change}、resume {change} | `kflow-resume` | 所有项目 |
| 接口测试、API测试、接口单元测试 | `kflow-api-test` | 所有项目 |
| 测试、QA、验收、E2E | `kflow-e2e-test` | 仅前后端项目 |
| 修复/Bug/缺陷 | `kflow-bug-fix`（有活跃 bug-fix 时）/ `kflow-bug-triage`（无活跃 bug-fix 时） | 所有项目 |
| 反馈、报告问题、报bug、提bug、问题 | `kflow-bug-triage` | 所有项目 |
| 状态、进度、查看、总结 | `kflow-status` | 所有项目 |
| 归档、完成 | `kflow-archive` | 所有项目 |
| 流程、指引、帮助 | `kflow-guide` | 所有项目 |
| 原型设计、UI 设计、交互设计 | `kflow-prototype-design` | 仅前后端项目 |
| 详细设计、技术设计、架构设计、设计审查 | `kflow-design` | 所有项目 |
| 任务计划、任务清单、实现计划 | `kflow-plan` | 所有项目 |
| 编码实现、TDD、功能实现 | `kflow-code` | 所有项目 |
| 代码审查、审查代码、review | `kflow-code-review` | 所有项目 |
| 集成测试、跨子变更测试 | `kflow-integration-test` | 所有项目 |
| 审计、评估、检查、审核 | `kflow-audit` | 所有项目 |
| 初始化、环境配置、工具推荐、设置 | `kflow-init` | 所有项目 |

---

## 项目类型判断

在进入设计探索阶段时，系统自动检测项目类型：

| 检测标识 | 存在时判断为 |
|---------|------------|
| package.json 前端框架依赖（react, vue, angular 等） | 前后端项目 |
| 前端源文件（.vue, .tsx, .jsx, .svelte） | 前后端项目 |
| 前端构建配置（vite.config, webpack.config） | 前后端项目 |
| 以上均不存在 | 纯后端项目 |

---

## 阶段依赖关系

### 设计层级：设计在变更级，执行在子变更级

```
kflow-explore (变更级) ──────────────────────────────────────────────────
    │
    ├─▶ kflow-prototype-design (变更级，可选)
    │       │
    └───────┴─▶ kflow-design (变更级，统一设计所有功能点)
                    │
                    ├── 输出: detailed-design.md, api-tests/, e2e-tests/, review-reports/*
                    ├── 划分子变更（基于完整设计认知）
                    │
                    ├─▶ kflow-plan (子变更级，输入变更级 detailed-design.md 相关章节)
                    │       │
                    │       └─▶ kflow-code (子变更级)
                    │               │
                    │               └─▶ kflow-code-review (子变更级，代码审查)
                    │                       │
                    │                       ├─▶ kflow-api-test (子变更级，接口单元测试)
                    │                       │       │
                    │                       │       └─▶ kflow-e2e-test (子变更级，仅前后端)
                    │                       │               │
                    │                       │               └─▶ kflow-bug-fix (按需，子变更级)
                    │                       │
                    │                       └─▶ kflow-bug-triage (按需，独立诊断，用户反馈入口)
                    │
                    │                       └─▶ (所有子变更完成)
                    │                               │
                    │                               └─▶ kflow-integration-test (变更级)
                    │                                       │
                    │                                       └─▶ kflow-audit (归档门控)
                    │
                    └─▶ (设计错误回退路由: kflow-bug-fix → kflow-design)
    │
    ├─▶ kflow-bug-triage (独立诊断，用户反馈入口，四层溯源定位问题源头)
    │
    ├─▶ kflow-status (独立，可随时调用)
    │
    ├─▶ kflow-audit (归档门控 + 按需手动调用)
    │
    ├─▶ kflow-init (独立，项目启动时调用)
    │
    ├─▶ kflow-resume (独立，通过 kflow-guide 路由，中断恢复)
    │
    └─▶ kflow-archive (变更级，集成测试通过后，含设计合并)
```

---

## 阶段流转示意

### 前后端项目

```
设计探索 ──▶ 原型设计(可选) ──▶ 详细设计(变更级) ──▶ 划分子变更
    (变更级)      (变更级)          (变更级)              │
                                                         ▼
                                     子变更: 计划 → 编码 → 代码审查 → 接口单元测试(kflow-api-test) → E2E测试(kflow-e2e-test)
                                                                                    │
                                                                                    ▼
                                                                        kflow-integration-test (变更级)
                                                                                    │
                                                                      ┌─────────────┴─────────────┐
                                                                      │                           │
                                                                  kflow-bug-fix (按需)    kflow-audit (门控) → 归档
```

### 纯后端项目

```
设计探索 ──▶ 详细设计(变更级) ──▶ 划分子变更
    (变更级)      (变更级)              │
                                        ▼
                          子变更: 计划 → 编码 → 代码审查 → 接口单元测试(kflow-api-test)
                                                             │
                                                             ▼
                                                  kflow-integration-test (变更级)
                                                             │
                                             ┌───────────────┴───────────────┐
                                             │                               │
                                         kflow-bug-fix (按需)    kflow-audit (门控) → 归档
```

---

## 门控机制说明

每个 Skill 在执行前会进行门控检查，确保前置阶段已完成。详细的门控规则定义在 [core-mechanisms/03-status-and-tasks.md](../core-mechanisms/03-status-and-tasks.md#34-门控规则) 章节，包括：

- **正向门控规则**：7 条阶段进入门控检查
- **审计门控**：归档前七维度审计，新增第 4 种回退触发来源
- **阶段回退门控**：回退条件、联动规则、回退完成条件
- **代码审查门控**：两视角并行审查通过条件
- **审查闭环验证**：分级重审规则
- **functional-designs/ 修订规则**：修订时机/范围/影响
- **设计合并规则**：归档时功能设计+详细设计合并到产品级文档

各 Skill 文件内联具体的门控检查项，便于独立阅读。

---

## 使用建议

1. **新需求启动**：使用 `kflow-guide` 获取流程指引（含跨变更冲突检测），或直接使用 `kflow-explore` 开始设计探索
2. **中断恢复**：使用「继续 {change-name}」通过 `kflow-guide` 路由到 `kflow-resume` 恢复中断的变更
3. **详细设计**：使用 `kflow-design` 在变更级统一设计所有功能点，设计完成后划分子变更
4. **查看进度**：使用 `kflow-status` 查看所有未归档变更状态（含子变更进度矩阵）
5. **执行子变更**：按依赖顺序，依次执行 `kflow-plan` → `kflow-code` → `kflow-code-review` → 接口单元测试 → E2E测试
6. **用户反馈问题**：使用 `kflow-bug-triage` 进行四层溯源诊断和问题登记，triage 会路由到正确的修复流程
7. **测试失败**：使用 `kflow-bug-fix` 进行根因分类和修复（二分法：实现错误/测试错误）
7. **前端变更**：在 `kflow-explore` 完成后，使用 `kflow-prototype-design` 进行原型设计（前后端项目）
8. **所有子变更完成后**：执行变更级集成测试（前后端和纯后端项目均需执行）
9. **归档变更**：集成测试通过后，使用 `kflow-archive` 归档已完成的变更
10. **流程指引错误反馈**：记录到 docs/skill-suggestion.md
