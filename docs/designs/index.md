# KFlow Skills 体系设计文档

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-06-03

---

## 设计目标

设计一套适用于公司内部开发流程的 Skills 体系，采用文档驱动的阶段门控机制，确保需求从设计到交付的全流程可追溯、可验证。

---

## 核心概念

**设计层级重新划分（v1.4.0 重大变更）**：

```
变更—— 顶层管理单元（设计在变更级，执行在子变更级）
    │
    ├─▶ 设计探索 (变更级) → 原型设计 (变更级，可选) → 详细设计 (变更级)
    │       │
    │       └─▶ 输出 detailed-design.md（统一详细设计，含 NFR 章节）
    │
    ├─▶ 子变更划分（设计完成后，基于完整设计认知）
    │
    └─▶ 子变更—— 执行单元（计划 → 编码 → 接口单元测试 → E2E测试）
            │                                      功能点 ≤ 10
            │
            └─▶ 按依赖顺序依次完成
                   │
                   ▼
              集成测试 (变更级) → 归档
```

**关键规则**：
- 设计在变更级统一完成，子变更划分后置到详细设计之后
- 子变更职责简化为执行单元：仅负责计划、编码、测试
- 子变更目录包含 .status.md、tasks.md、test-reports/、checkpoints/ 等文件
- 当变更的功能点超过 10 个时，必须拆分为多个子变更
- 每个变更最多 20 个子变更，超过时需拆分为多个变更
- 子变更按依赖关系确定实现顺序，依次完成
- 所有子变更完成后，执行集成测试，然后变更整体归档

**项目类型区分**：
- 前后端项目（11 阶段）：设计探索 → 原型设计(可选) → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试 → 集成测试 → 审计(门控) → 归档
- 纯后端项目（9 阶段）：设计探索 → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → 集成测试 → 审计(门控) → 归档

**v1.4.0 核心机制**：
- **阶段回退**：`⚠️ 需修订` 状态 + 三级联动回退（当前子变更 / 接口契约变更 / 架构级变更）
- **代码审查**：编码阶段新增两视角并行代码审查（安全+规范、质量+性能）
- **集成测试**：变更级集成测试，验证跨子变更接口契约
- **审查闭环**：分级重审 + 问题追踪矩阵
- **根因分类路由**：`kflow-bug-triage` 四层溯源诊断 + `kflow-bug-fix` 二分法（实现错误 / 测试错误）
- **条件产物引用**：标准化图例（✅ 必须 / 🔶 条件 / ⏭️ 不适用）

---

## Skills 清单

| Skill 名称 | 阶段 | 归属层级 | 必须性 | 核心功能 |
|-----------|------|---------|--------|---------|
| `kflow-guide` | 流程指引 | — | 按需 | 意图识别、活跃变更检测、跨变更冲突检测 |
| `kflow-explore` | 设计探索 | 变更级 | 必须 | 需求澄清、功能点拆分+类型标记（后端/前端）、项目类型检测（不再划分子变更） |
| `kflow-prototype-design` | 原型设计 | 变更级 | 可选 | HTML 原型设计（动态工具链选择+STYLE/GENERATE 拆分+增强验证）、用户评审确认 |
| `kflow-design` | 详细设计 | **变更级** | 必须 | 统一详细设计（含NFR）、四视角审查、子变更划分、测试用例文档、用户评审确认 |
| `kflow-plan` | 计划 | 子变更级 | 必须 | Checkbox 任务清单、DoD验收标准、功能点级全展开 |
| `kflow-code` | 编码 | 子变更级 | 必须 | TDD 流程、数据库迁移、跨变更冲突检测、多 Agent 并行编码 |
| `kflow-code-review` | 代码审查 | 子变更级 | 必须 | 两视角并行审查（安全+规范/质量+性能）、闭环验证 |
| `kflow-api-test` | 接口单元测试 | 子变更级 | 必须 | curl/HTTP 接口测试、健康评分、所有项目类型必须执行 |
| `kflow-e2e-test` | E2E测试 | 子变更级 | 前后端必须 | 浏览器自动化测试、仅前后端项目、依赖前置 kflow-api-test |
| `kflow-bug-fix` | 缺陷修复 | 按需 | 按需 | 子变更级二分法根因分类路由、实现/测试错误修复 |
| `kflow-bug-triage` | 问题分诊 | — | 按需 | 四层溯源诊断、问题登记（bugs/）、路由决策（REVISION或bug-fix） |
| `kflow-integration-test` | 集成测试 | 变更级 | 必须 | 集成测试执行、内聚四分法修复循环、架构评估自动触发 |
| `kflow-status` | 状态总结 | — | 按需 | 未归档变更汇总、子变更进度矩阵 |
| `kflow-archive` | 归档 | 变更级 | 必须 | 变更归档、集成测试门控、索引更新、设计合并 |
| `kflow-audit` | 使用评估 | — | 归档门控+按需 | 七维度评估、审计报告、审计回退路由 |
| `kflow-init` | 环境初始化 | — | 按需 | 环境能力发现、工具推荐矩阵、toolchain.md 输出 |
| `kflow-resume` | 中断恢复 | — | 按需 | 变更名定位断点、优先级链读取状态、调度阶段 Skill |

---

## 文档结构索引

### 设计背景与路线图
- [overview.md](overview.md) - 设计概述、参考资源、实施计划

### 核心运行机制
- [core-mechanisms/index.md](core-mechanisms/index.md) - 目录结构、状态文件、任务清单、阶段流转、回退机制、条件产物引用（8 文件拆分）

### Skills 详细规格
- [skills/index.md](skills/index.md) - Skills 导航与触发时机
- [skills/kflow-guide.md](skills/kflow-guide.md) - 流程指引阶段
- [skills/kflow-explore.md](skills/kflow-explore.md) - 设计探索阶段（变更级，不再划分子变更）
- [skills/kflow-prototype-design.md](skills/kflow-prototype-design.md) - 原型设计阶段（HTML 原型，动态工具链选择+STYLE/GENERATE 拆分）
- [skills/kflow-design.md](skills/kflow-design.md) - 详细设计阶段（**变更级**，含 NFR、子变更划分）
- [skills/kflow-plan.md](skills/kflow-plan.md) - 计划阶段（子变更级，含 DoD 验收标准）
- [skills/kflow-code.md](skills/kflow-code.md) - 编码阶段（子变更级，TDD 流程、数据库迁移、跨变更冲突检测、多 Agent 并行）
- [skills/kflow-code-review.md](skills/kflow-code-review.md) - 代码审查阶段（子变更级，两视角并行审查 + 闭环验证）
- [skills/kflow-api-test.md](skills/kflow-api-test.md) - 接口单元测试阶段（子变更级，curl/HTTP 测试，所有项目类型）
- [skills/kflow-e2e-test.md](skills/kflow-e2e-test.md) - E2E测试阶段（子变更级，仅前后端项目）
- [skills/kflow-bug-fix.md](skills/kflow-bug-fix.md) - 缺陷修复阶段（子变更级，二分法根因分类路由）
- [skills/kflow-bug-triage.md](skills/kflow-bug-triage.md) - 问题分诊（独立诊断 Skill，四层溯源+问题登记+路由决策）
- [skills/kflow-integration-test.md](skills/kflow-integration-test.md) - 集成测试阶段（变更级，内聚四分法修复循环 + 架构评估自动触发）
- [skills/kflow-status.md](skills/kflow-status.md) - 状态总结（含子变更进度矩阵）
- [skills/kflow-archive.md](skills/kflow-archive.md) - 归档阶段（含集成测试门控、设计合并）
- [skills/kflow-audit.md](skills/kflow-audit.md) - 使用评估（含七维度审计、归档门控集成）
- [skills/kflow-init.md](skills/kflow-init.md) - 环境初始化（含工具推荐矩阵、toolchain.md 输出）
- [skills/kflow-resume.md](skills/kflow-resume.md) - 中断恢复（变更名定位断点、优先级链读取、直接调度阶段 Skill）

### 产物模板
- [templates/index.md](templates/index.md) - 模板目录索引（48 个模板，含 1 个已废弃，五层级分类）

### 附录示例
- [examples/index.md](examples/index.md) - 示例导航
- [examples/change-status.md](examples/change-status.md) - 变更级状态文件示例（子变更进度矩阵）
- [examples/subchange-status.md](examples/subchange-status.md) - 子变更状态文件示例（5 阶段表格）
- [examples/rollback-status.md](examples/rollback-status.md) - 回退前状态文件示例（⚠️ 需修订）
- [examples/subchange-tasks.md](examples/subchange-tasks.md) - 子变更任务清单示例（含 DoD 验收标准）
- [examples/design-level-restructure.md](examples/design-level-restructure.md) - 变更级统一详细设计示例（含 NFR 章节）
- [examples/code-review-report.md](examples/code-review-report.md) - 代码审查报告示例
- [examples/integration-tests.md](examples/integration-tests.md) - 集成测试用例示例
- [examples/migration-log.md](examples/migration-log.md) - 数据库迁移记录示例
- [examples/service-guide.md](examples/service-guide.md) - 项目服务指引示例（多环境配置）
- [examples/change-index.md](examples/change-index.md) - 变更管理索引示例（含影响文件字段）
- [examples/skill-suggestion.md](examples/skill-suggestion.md) - Skills 优化建议记录示例
- [examples/audit-report.md](examples/audit-report.md) - 审计报告示例
- [examples/toolchain.md](examples/toolchain.md) - toolchain 配置示例
- [examples/integration-fix-report.md](examples/integration-fix-report.md) - 集成测试修复报告示例
- [examples/arch-assessment.md](examples/arch-assessment.md) - 架构评估报告示例（连续3轮同用例失败自动触发）
- [examples/product-domain-doc.md](examples/product-domain-doc.md) - 产品级领域文档示例
- [examples/product-design-index.md](examples/product-design-index.md) - 产品级索引入口示例

---

## 核心设计决策

| 决策项 | 选择 | 说明 |
|-------|------|------|
| 粒度区分 | 渐进式流程 | 一个 Skill 内部根据输入自动判断产品级/功能级/缺陷级 |
| 设计层级 | 设计在变更级，执行在子变更级 | 详细设计提升到变更级，消除"先划分后设计"的矛盾 |
| 项目类型区分 | 自动检测 | 设计探索阶段检测项目类型，区分前后端项目和纯后端项目 |
| 前后端项目流程 | 11 阶段 | 设计探索 → 原型设计(可选) → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试 → 集成测试 → 审计(门控) → 归档 |
| 纯后端项目流程 | 9 阶段 | 设计探索 → 详细设计 → 计划 → 编码 → 代码审查 → 接口单元测试 → 集成测试 → 审计(门控) → 归档 |
| 原型设计 | 可选推荐 | 前端变更推荐 HTML 原型设计，委托 huashu-design，但不强制 |
| 多视角审查 | Agent 并行审查（变更级） | 四视角在变更级一次审查，非每子变更 |
| 代码审查 | 独立 Skill，两视角并行审查 | `kflow-code-review`：安全+规范、质量+性能，含闭环验证 |
| 变更级服务刷新 | 编码→测试门控同步点 | 所有子变更编码+审查完成后统一编译-迁移-重启-健康检查 |
| checkpoint 两级化 | 变更级 + 子变更级分开存储 | 恢复时优先读子变更级，含过期清理规则 |
| 架构评估自动触发 | 连续3轮同用例失败自动触发 | 自动收集证据 + 多方案分析 + 用户决策，在 `kflow-integration-test` 中实现 |
| 阶段回退 | ⚠️ 需修订 状态 + 分级联动 | 分三级：当前子变更 / 接口契约变更 / 架构级变更 |
| 目录位置 | docs/changes/ | 遵循项目文档结构规范 |
| 阶段门控 | 状态文件门控 | 每个阶段完成后更新状态文件，含正向和回退门控 |
| 任务清单 | Markdown checkbox | 功能点级全展开形式，每功能点含 DoD 验收标准 |
| 子变更划分 | 设计完成后基于完整认知划分 | 按业务功能划分，每子变更不超过10个功能点 |
| 测试时机 | 设计文档先行 | 设计阶段编写测试用例文档，编码阶段编写测试代码 |
| 审查闭环 | 分级重审 + 追踪矩阵 | 高严重度双视角重审，中严重度原视角重审，低严重度抽查 |
| 状态格式 | Markdown 表格 | 便于人类阅读 |
| 缺陷修复 | 根因分类路由 | 实现错误修复代码 / 测试错误修正测试 / 设计错误触发回退 |
| 归档方式 | 整体归档 | 所有子变更完成 + 集成测试通过后，变更整体归档 |
| 归档条件 | 集成测试 + 全阶段完成 | 集成测试通过 + 所有子变更各阶段完成 |
| NFR 要求 | 设计阶段定义 | detailed-design.md 含性能/安全/可用性/可维护性章节 |
| DoD 验收标准 | 计划阶段定义 | 每功能点 4 维验收（Happy Path + Error Path + Edge Case + Quality） |
| 条件产物引用 | 标准化图例 | ✅ 必须 / 🔶 条件 / ⏭️ 不适用 |
| 数据库迁移 | 变更级管理 | migrations/ 目录，含迁移脚本和回滚脚本 |
| 多环境配置 | 四环境 | service-guide.md 区分 dev/test/staging/prod |
| 跨变更冲突检测 | 编码前检查 | 检查活跃变更影响文件重叠 |
| 使用评估 | 归档前自动审计 + 手动调用 | 七维度评估（流程合规性、产物完整性、审查质量、测试充分性、缺陷管理、效率指标、Post-mortem汇总） |
| 环境初始化 | 能力发现 + 工具推荐 | 检测 MCP servers 和 Skills，评估组合可行性，输出 toolchain.md |
| 缺陷修复等级 | 三级分离 | `kflow-bug-triage` 负责用户反馈四层溯源诊断；`kflow-bug-fix` 负责子变更级二分法；`kflow-integration-test` 内聚变更级四分法 |
| 设计合并 | 归档时合并到产品级 | 功能设计合并到 docs/designs/functional-designs/（前后端：{menu}/index.md + part-NN.md；纯后端：{domain}.md）+ 技术设计分散更新到 technical-designs/ 6 文件（含 config-items.md、error-handling.md），标注来源变更 |
| 文件命名 | 双层目录体系 | functional-designs/（功能设计目录）+ detailed-design.md（详细设计） |
| 文档拆分 | 产品级多文件 + 变更级目录化拆分 | 产品级从一开始多文件拆分，变更级功能点>30拆分为多文件（index.md + part-NN.md），4 组文档目录化 |
| 10 轮自审机制 | explore/prototype/design 三阶段强制执行 | 每阶段 10 轮自循环审查，每轮独立记录时间戳文件，覆盖阶段专属维度，不允许提前终止 |
| 执行类阶段重复制 | plan/code/code-review/api-test/e2e-test/integration-test/bug-fix 七阶段统一 | 子代理每轮遍历全部工作项独立执行完整流程，禁止按轮次分段分配工作重点，复杂度评估仅信息展示 |
| 阶段边界强制 | 文档白名单 + 标准产物强制 + 越界禁止 | 每阶段仅允许创建输出产物表列出的文件，信息不足记录到 skill-suggestion.md，禁止越界输出 |
| 功能设计升维 | functional-designs/ 扩展为用户体验规格说明书 | 新增页面菜单、可执行操作、表单项定义、业务规则、业务流程闭环，为 prototype 提供精确输入 |
| 审查目录分离 | self-reviews/ + cross-reviews/ | 自审与交叉审查分目录存储，语义明确，时间戳命名自然排序 |
| FP 类型标记 | 后端/前端 严格二分，explore 阶段标记 | 每个功能点在拆分时标记为后端或前端，无法归类则强制拆分，类型作为后续子变更划分校验依据 |
| 子变更类型自动校验 | design 阶段自动推断 | 基于 FP 类型一致性自动推断子变更类型（后端子变更/前端子变更），混合 FP 拒绝划分，禁止人工手动填写 |
| 共享关切归属 | 按归属规则分配 | 错误码→后端SC / 错误码提示→前端SC / 配置项→后端SC / 共享DTO→变更级 shared-types/ / Schema变更→后端SC+关联标注 |
| 跨层越界检测 | verify D3.2 + code-review 步骤 3.3 | Grep 模式检测后端SC中的前端文件/样式，前端SC中的后端代码/数据库操作，严重度🟡警告不阻塞 |
