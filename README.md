# KFlow DevFlow Skills

一套**文档驱动的阶段门控开发流程体系**，将软件开发从设计到交付的全流程标准化为一系列 Claude Code Skills，确保每个阶段产物可追溯、可验证。

> **版本**: 0.16.0 | **更新时间**: 2026-06-18 | **适用版本**: KFlow Skills 体系 2.0.0+

---

## 快速开始

```
# 1. 环境初始化（推荐首次使用）
kflow-init

# 2. 开启新需求（自然语言即可）
我想添加用户认证功能
```

`kflow-init` 扫描项目环境，检测 MCP 服务和 Skills，生成工具链推荐，注入项目画像。之后直接用自然语言描述需求即可，系统自动识别意图并路由到正确阶段。

---

## 核心理念

- **文档驱动**：每个阶段产出标准化文档，文档是阶段流转的门控条件
- **阶段门控**：下一阶段启动前必须验证上一阶段产物完整且状态为完成
- **变更层级**：Change（变更）是顶层管理单元，Subchange（子变更）是执行单元
- **设计先行**：设计在变更级统一完成，执行在子变更级按依赖顺序依次推进
- **阶段钩子**：每个阶段执行前后通过 PRE_HOOK/POST_HOOK 自动化服务生命周期管理（启动/健康检查/停止/端口冲突检测）
- **元素覆盖树**：四层页面→区域→元素→状态结构 + 操作链 + TC-ID 映射，确保 100% E2E 测试覆盖率

## 适用场景

| 场景 | 说明 |
|------|------|
| 新功能开发 | 从需求到交付的完整流程 |
| Bug 修复 | 简化流程，快速定位和修复 |
| 产品搭建 | 完整流程，可能跨多个变更 |
| 老项目接手 | 环境初始化 + 逆向分析 |

## 流程概览

### 前后端项目（11 阶段，含审计门控）

```
kflow-guide → kflow-explore → kflow-prototype-design(可选) → kflow-design
    → kflow-plan → kflow-code → kflow-code-review → kflow-api-test
    → kflow-e2e-test → kflow-bug-fix(按需) → kflow-integration-test
    → kflow-verify(可选诊断) → kflow-audit → kflow-archive
```

### 纯后端项目（9 阶段，含审计门控）

```
kflow-guide → kflow-explore → kflow-design
    → kflow-plan → kflow-code → kflow-code-review → kflow-api-test
    → kflow-bug-fix(按需) → kflow-integration-test
    → kflow-verify(可选诊断) → kflow-audit → kflow-archive
```

---

## 变更层级

```
变更 (Change) — 顶层管理单元
    │
    ├── 设计阶段（变更级统一完成）
    │   ├── 设计探索 (kflow-explore)
    │   ├── 原型设计 (kflow-prototype-design, 可选)
    │   └── 详细设计 (kflow-design)
    │         └── 四视角审查 + 子变更划分
    │
    └── 执行阶段（子变更级，重复制模式）
        ├── 子变更 1: 计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试
        ├── 子变更 2: 计划 → 编码 → 代码审查 → 接口单元测试 → E2E测试
        └── 子变更 N: ...
              │
              ▼
        集成测试 (变更级) → 审计 → 归档
```

**关键规则**：
- 设计在变更级统一完成，子变更划分在详细设计之后
- 每个子变更功能点 ≤ 10 个
- 每个变更最多 20 个子变更
- 子变更按依赖关系依次完成
- 执行类阶段采用**弹性重复制模式**：子代理每轮遍历全部工作项独立执行完整流程，首次执行标准 10 轮，回退重执行按影响范围分数动态决定轮次（1-5分→3-5轮，6-15分→5-8轮，>15分→10轮），主 Agent 验收闭环

---

## Skills 清单

### 入口与辅助

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-guide` | 意图识别、项目类型判断、变更检测、RESUME 路由 | 流程指引、帮助、如何开始、继续、恢复 |
| `kflow-init` | 环境初始化、MCP/Skills 能力扫描、工具链推荐、老项目逆向分析、CLAUDE.md 注入、skill-suggestion 自动捕获规则注入 | 初始化、环境配置、工具推荐 |
| `kflow-status` | 未归档变更汇总 + 子变更进度矩阵 + 加权整体进度 | 状态、进度、任务总结 |
| `kflow-resume` | 断点定位（优先级链：checkpoint > .status.md > tasks.md）→ 产物完整性验证 → 五问题摘要 → 调度对应阶段 Skill | 继续 {change}、恢复 {change} |
| `kflow-verify` | 独立诊断工具（非流程阶段）——七维度产物完整性诊断（文件存在/内容完整/输入源正确/交叉引用一致/设计决策完整/门控合规/审查闭环）+ 三级严重度分级（阻塞/警告/建议）+ 修复路由 + 诊断报告 | 诊断、验证产物、检查产物、verify |

### 设计阶段（变更级）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-explore` | 创建变更目录、项目类型检测、功能点原子级拆分、构建领域词汇表、输出功能结构树、原型设计决策门控 | 开始新需求、设计探索、功能设计 |
| `kflow-prototype-design` | 编排层，动态扫描环境设计 Skills → 多方案推荐 → 用户锁定工具链 → 委托生成 HTML 原型 + 5 轮导航验证 + 5 轮 Playwright 验证 + UX 规则审查 + 对比度检测 + 离线自包含 + 生成 element-coverage-tree（Path A 静态解析）（仅前后端，可选） | 原型设计、UI 设计、交互设计 |
| `kflow-design` | 系统架构、数据模型、接口设计、NFR 定义、四视角并行审查（业务/技术/安全/质量）、子变更划分（含 HITL/AFK 分类）、ADR 架构决策记录、element-coverage-tree Path B（playwright-cli 动态探索）+ 100% 覆盖率门控、复杂度评估（高复杂度 FP 逐项用户确认） | 详细设计、技术设计、架构设计 |

### 执行阶段（子变更级，重复制模式）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-plan` | 为子变更创建 TDD 任务清单 + DoD 四维验收标准（功能/质量/测试/文档）+ 10 轮子代理自审查 | 任务计划、任务清单、实现计划 |
| `kflow-code` | TDD 编码实现、编译验证（PRE_HOOK）+ 多 Agent 并行编码、跨变更冲突检测、原型到代码一致性约束（从 prototype 提取 design-tokens/element-coverage-tree 注入）、双层遍历全部子变更 | 编码实现、TDD、功能实现 |
| `kflow-code-review` | 两视角并行审查（安全+规范 / 质量+性能）+ 分级重审闭环验证 + 原型对账 Grep + 双层遍历全部子变更 | 代码审查、code review |
| `kflow-api-test` | curl/HTTP 方式对 api-tests/ 逐条测试、健康评分五维度（功能完整性/响应时间/HTTP状态码/错误处理/契约一致性）、所有项目类型必须 | 接口测试、API测试、接口单元测试 |
| `kflow-e2e-test` | Playwright snapshot+ref 模式浏览器自动化测试、决策树路由、element-coverage-tree 元素触达率统计、generated-test 可选收集（通过率≥80%）、仅前后端项目 | E2E 测试、QA 测试、浏览器自动化测试 |
| `kflow-bug-fix` | 子变更级二分法根因分类修复（实现错误/测试错误）、多 Agent 并行分析、Post-mortem 复盘。用户反馈统一由 kflow-bug-triage 处理 | 缺陷修复、Bug 修复 |

### 收尾阶段（变更级）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-integration-test` | 变更级集成测试 + 内聚四分法修复循环（实现错误/契约错误/测试错误/架构设计错误）、架构评估自动触发（连续 3 轮同用例失败）、服务持久化模式管理 | 集成测试、跨子变更测试 |
| `kflow-audit` | 七维度加权评估（流程 22%/产物 23%/审查 20%/测试 15%/缺陷 10%/效率 5%/Post-mortem 5%）、归档门控集成、审计回退路由、SKILL.md 钩子引用合规检查 | 审计、评估、检查 |
| `kflow-archive` | 门控检查 → 设计合并（功能设计+技术设计）→ 全景更新 → 移至 archive/ → AskUserQuestion 询问 git commit（含版本自增+打包） | 归档、完成、变更结束 |

---

## 常用工作流

### 新功能开发

```
1. "我想添加用户认证功能"       → kflow-guide 识别意图
2. kflow-explore               → 创建变更目录，原子级拆分功能点，构建领域词汇表
3. kflow-prototype-design      → (可选) HTML 交互原型 + 元素覆盖树 Path A + 导航/Playwright 验证
4. kflow-design                → 系统架构 + 四视角并行审查 + 划分子变更 + ADR 记录 + 元素覆盖树 Path B + 100% 覆盖率门控
5. kflow-plan                  → 子变更 TDD 任务清单 + DoD 验收标准
6. kflow-code                  → TDD 编码实现 + 编译验证 + 原型到代码一致性约束
7. kflow-code-review           → 两视角并行审查 + 分级重审闭环
8. kflow-api-test              → curl/HTTP 接口逐条测试 + 健康评分
9. kflow-e2e-test              → (仅前后端) Playwright 浏览器自动化测试 + 元素触达率统计
10. kflow-bug-fix               → (按需) 二分法根因分类修复（B路径：测试失败触发）
11. kflow-integration-test      → 变更级跨子变更集成测试
12. kflow-audit → kflow-archive → 七维度审计 + 归档（含版本自增+打包）
```

### Bug 修复（简化流程）

```
1. "修复登录页面报错"           → 识别为功能缺陷
2. kflow-explore（简化）       → 缺陷描述、影响分析
3. kflow-design（简化）        → 修复方案
4. plan → code → code-review → api-test → e2e-test  → 执行修复
5. kflow-archive               → 归档
```

### 中断恢复

```
用户: 继续 add-user-auth
→ kflow-guide PARSE 正则匹配 → RESUME 路由到 kflow-resume
→ 优先级链读取状态（checkpoint > .status.md > tasks.md）
→ 定位断点 → 五问题快速摘要 → 调度阶段 Skill
```

---

## 触发词速查

| 你想做的事 | 说这个 |
|-----------|--------|
| 开始新功能 | "开始新需求" / "添加 XX 功能" / "开发 XX" |
| 获取流程指引 | "流程指引" / "帮助" / "如何开始" |
| 继续中断的工作 | "继续 {change-name}" / "恢复 {change-name}" |
| 查看进度 | "状态" / "进度" / "查看进度" |
| 原型/UI 设计 | "原型设计" / "UI 设计" / "交互设计" |
| 详细/技术设计 | "详细设计" / "技术设计" / "架构设计" |
| 制定任务计划 | "任务计划" / "任务清单" / "实现计划" |
| 编码实现 | "编码实现" / "TDD" / "功能实现" |
| 代码审查 | "代码审查" / "review" / "审查代码" |
| 接口/API 测试 | "接口测试" / "API测试" / "接口单元测试" |
| E2E/浏览器测试 | "E2E 测试" / "QA 测试" / "浏览器自动化测试" |
| 修复 Bug | "修复 XX" / "Bug 修复" / "测试失败" |
| 集成测试 | "集成测试" / "跨子变更测试" |
| 审计评估 | "审计" / "评估" / "检查" / "审核" |
| 归档完成 | "归档" / "完成" / "变更结束" |
| 环境初始化 | "初始化" / "环境配置" / "工具推荐" |
| 诊断产物 | "诊断" / "验证产物" / "检查产物" |

---

## 阶段门控状态

每个阶段的完成状态记录在 `.status.md` 文件中：

| 状态值 | 含义 |
|--------|------|
| ✅ 完成 | 阶段已完成，产物已生成 |
| 🔄 进行中 | 阶段正在执行 |
| ⏳ 待开始 | 阶段未开始 |
| ⏭️ 跳过 | 阶段被跳过（可选或不适用） |
| ❌ 阻塞 | 阶段被阻塞 |
| ⚠️ 需修订 | 阶段产物需回退修订 |
| ⏸️ 等待同步 | 等待外部依赖或并行子变更同步 |

---

## 目录结构速查

```
VERSION                                # 统一版本号（Skill 体系版本标识）
.claude/
├── settings.local.json                # 项目级 Claude Code 配置
└── skills/                            # 运行时 Skills
    ├── kflow-shared/                 # 运行时共享 Skill（非用户直接调用）
    │   ├── phase-hooks.md             #   PRE_HOOK/POST_HOOK 执行规范（各阶段引用）
    │   ├── service-lifecycle.md       #   服务生命周期管理（daemon 模式、端口冲突检测）
    │   └── scripts/                   #   运行时脚本（随 Skills 打包分发）
    │       └── with_server.py         #   服务管理脚本（--daemon/--status/--health/--stop-all）
    ├── kflow-guide/SKILL.md
    ├── kflow-explore/SKILL.md
    ├── ...                            # 16 个 kflow-* Skills + openspec-* + 设计 Skills
    └── skill-creator/SKILL.md

docs/
├── CONTEXT.md                        # 项目级领域词汇表
├── service-guide.md                  # 项目服务指引（多环境配置）
├── skill-suggestion.md               # Skills 优化建议记录
├── toolchain.md                      # 工具链配置（kflow-init 生成）
│
├── changes/                          # 变更管理目录
│   ├── index.md                      # 变更管理索引（活跃 + 已归档）
│   └── {change-name}/                # 单个变更
│       ├── .status.md                # 变更总状态文件（含子变更进度矩阵）
│       ├── tasks.md                  # 变更总任务清单（子变更级 checkbox）
│       ├── functional-designs/       # 功能设计文档（目录化，part-NN.md 分册 ≤30 功能点）
│       ├── prototype/                # HTML 原型（可选）
│       ├── detailed-design.md        # 统一详细设计（变更级，含 NFR 章节）
│       ├── element-coverage-tree.md  # 元素覆盖树（四层结构+操作链+TC-ID映射，100% E2E 覆盖）
│       ├── traceability.md           # 覆盖追溯矩阵（FP × 阶段产物）
│       ├── api-tests/                # 接口测试用例（目录化，part-NN.md 分册 ≤30 接口）
│       ├── e2e-tests/                # E2E 测试用例（目录化，仅前后端）
│       ├── integration-tests/        # 集成测试用例（目录化）
│       ├── self-reviews/             # 自循环审查记录（explore/prototype/design）
│       ├── cross-reviews/            # 四视角交叉审查报告（批次目录）
│       ├── migrations/               # 数据库迁移（变更级）
│       └── subchanges/               # 子变更目录
│           └── {subchange-name}/
│               ├── .status.md        # 子变更状态文件
│               ├── tasks.md          # 子变更任务清单（功能点级全展开）
│               └── test-reports/     # 测试报告（api/e2e/review/fix-reports）
│
├── designs/                          # 产品级设计文档
│   ├── architecture.md               # 全景架构
│   ├── data-model.md                 # 全景数据模型
│   ├── api-catalog.md                # 全景 API 目录
│   └── nfr-baseline.md               # NFR 基线
│
├── adr/                              # 架构决策记录
└── archive/                          # 归档目录

openspec/
└── specs/                            # OpenSpec 规格文件（87 个核心机制/阶段规格）
```

---

## 最佳实践

**命名规范**：功能新增 `add-{feature}`，Bug 修复 `fix-{issue}`，产品搭建 `{platform}-init`

**功能点拆分**：每个功能点单一明确，原子级拆分，子变更 ≤ 10 个功能点，标注依赖关系

**子变更划分**：按设计域聚合，无依赖可并行，优先基础设施子变更，标注 HITL/AFK 执行类型

**阶段钩子**：所有阶段通过 PRE_HOOK/POST_HOOK 标准化服务生命周期管理——PRE_HOOK 负责状态检查/文件重载/服务启动/健康检查，POST_HOOK 负责服务停止/浏览器清理/状态更新；钩子执行规范统一引用 `kflow-shared/phase-hooks.md`，不内联复制

**元素覆盖树**：前后端项目在 prototype-design（Path A 静态 HTML 解析）和 design（Path B playwright-cli 动态探索）阶段双路径生成 `element-coverage-tree.md`，design 阶段 100% 覆盖率门控，e2e-test 阶段统计元素触达率

**原型设计**：前端 UI 变更推荐使用，纯后端自动跳过；编排层动态扫描环境设计 Skills，多方案推荐后用户锁定工具链执行；DESIGN 拆分为 STYLE（风格推荐）+ GENERATE（工具链执行）；离线自包含（禁 CDN + 系统字体栈）

**代码审查**：独立于编码阶段，两视角并行审查，分级重审闭环——高严重度需全量重审，中严重度抽查验证，低严重度记录即可

**接口测试**：所有项目类型必须阶段，curl/HTTP 逐条验证，五维度健康评分

**服务管理**：通过 `with_server.py` 统一管理——`--daemon` 持久化模式保持服务运行、`--status/--health` 状态查询、`--stop-all` 批量停止、端口冲突自动检测

**中断恢复**：使用 `继续 {change-name}` 即可精确定位断点，无需记忆当前阶段；恢复时自动验证产物完整性

---

## 常见问题

**纯后端和前后端项目的流程区别？** 纯后端跳过「原型设计」和「E2E 测试」，共 9 阶段（含审计门控）；前后端 11 阶段。系统自动检测。

**一个变更可以有多少子变更？** 最少 1 个，最多 20 个。超过需拆分多个变更。

**子变更可以并行吗？** 无依赖的可并行，AFK 类型可自动并行。

**执行类阶段的重复制模式是什么？** 7 个执行类阶段（plan/code/code-review/api-test/e2e-test/integration-test/bug-fix）统一采用弹性重复制——子代理每轮遍历全部工作项独立执行完整流程，首次执行标准 10 轮，回退重执行按影响范围分数动态决定轮次（公式：FP数×1 + 接口数×1.5 + 数据模型×2；分数-轮次映射：1-5分→max(3,ceil(分数))轮，6-15分→max(5,ceil(分数/2))轮，>15分→10轮），验证门控要求受影响项 100% 覆盖 + 全量至少 1 轮兜底 + 产物完整性，主 Agent 负责最终验收。

**设计阶段发现问题？** 触发阶段回退（⚠️ 需修订），三级回退机制——子变更级回退仅影响当前子变更，接口契约变更回退影响相关子变更，架构级回退需重新设计。

**集成测试连续失败？** 连续 3 轮同一用例失败自动触发架构评估，防止设计问题在测试阶段反复消耗资源。

**归档后还能修改吗？** 不能。归档变更移至 `docs/archive/`，禁止修改。需修改应创建新变更。

**阶段钩子（PRE_HOOK/POST_HOOK）是什么？** 每个阶段执行前后的标准化服务生命周期管理步骤。PRE_HOOK 负责状态检查、文件重载、服务启动、健康检查；POST_HOOK 负责服务停止、浏览器清理、状态更新。钩子执行职责归属于变更级 Agent，子变更 Agent 不执行钩子。

**元素覆盖树（element-coverage-tree.md）是什么？** 前后端项目的 E2E 测试覆盖基础文档，提供四层页面→区域→元素→状态结构 + 操作链 + TC-ID 映射。双路径生成——Path A 从 HTML 原型静态解析，Path B 通过 playwright-cli 动态探索实际页面。design 阶段 100% 覆盖率门控通过后方可进入执行阶段。

**kflow-shared 是什么？** 运行时共享 Skill，包含 `phase-hooks.md`（阶段钩子执行规范）和 `service-lifecycle.md`（服务生命周期管理指令）。各阶段 SKILL.md 通过引用这些共享文件接入钩子机制，不在自身 SKILL.md 中内联复制钩子逻辑。审计阶段会检查此合规项。

**如何管理长时间运行的服务？** 通过 `with_server.py --daemon` 持久化模式启动，服务在多个阶段间保持运行。使用 `--status` 查询状态，`--health` 检查健康，`--stop-all` 批量停止。端口冲突自动检测并报告。

---

## 相关文档

- [设计文档入口](docs/designs/index.md) — Skills 体系设计文档（版本 2.0.0）
- [核心运行机制](docs/designs/core-mechanisms/index.md) — 目录结构、状态文件、阶段流转、门控规则、重复制模式、回退机制（9 文件拆分）
- [阶段钩子规范](docs/designs/core-mechanisms/09-phase-hooks.md) — PRE_HOOK/POST_HOOK 配置表、RELOAD 清单、服务生命周期
- [运行时钩子规范](.claude/skills/kflow-shared/phase-hooks.md) — 各阶段引用的运行时钩子执行规范
- [服务生命周期管理](.claude/skills/kflow-shared/service-lifecycle.md) — daemon 模式、端口冲突检测、服务停止超时链
- [OpenSpec 规格](openspec/specs/) — 87 个核心机制/阶段规格文件
- [CLAUDE.md](CLAUDE.md) — Claude Code 项目指令（含钩子引用强制规则、版本自增+打包规则）

---

> 本手册随 KFlow Skills 体系持续更新。如有疑问或建议，请通过 `docs/skill-suggestion.md` 记录反馈。

---

## 版本更新说明

### v0.16.0 (2026-06-18)
**权限声明可移植化与后台权限失败回退机制**
- **权限声明集中定义**：新增 `kflow-shared/permission-model.md`（§1 全局必需权限清单、§2 权限聚合规则、§3 环境适配指引、§4 权限配置幂等规则），作为权限配置的 source of truth，跟随 Skills 打包分发
- **kflow-init 权限自动配置**：新增 PERM_CONFIG 步骤（SCAN 后、MATCH 前），读取 permission-model.md 自动配置目标项目 `.claude/settings.json`，幂等合并不覆盖，用户确认机制，配置状态输出到 toolchain.md
- **后台权限失败回退前台子代理**：`repetition-model.md` 新增 §12.7 后台权限失败回退前台子代理机制（权限错误模式检测、创建新前台子代理重新执行、主 Agent 禁止接管硬线、不计入轮次级重试 3 次上限、前台也失败标记阻塞）
- **§12.5 权限预配置重构**：移除硬编码权限列表，改为引用 `kflow-shared/permission-model.md`；新增 kflow-init 自动配置说明
- **子代理强制规则框扩展**：7 个执行类阶段 SKILL.md 规则框从 4 条扩展为 5 条，新增第 5 条后台权限失败回退规则
- **本项目配置清理**：删除 `.claude/settings.json`（硬编码），改为 kflow-init 自动生成
- 新增 2 个 specs（kflow-permission-model/background-permission-fallback）+ 修改 3 个 specs（shared-repetition-model/subagent-enforcement-notice/subagent-isolation-rule）
- 同步更新 8 个运行时 SKILL.md + 3 个设计文档 + 1 个模板文件 + 1 个核心机制文档

### v0.15.0 (2026-06-18)
**弹性重复制与子代理强制规则双写强化**
- **弹性重复制机制**：移除固定 10 轮下限，改为首次执行标准 10 轮 + 回退重执行按影响范围分数动态决定轮次（影响范围分数公式：FP数×1 + 接口数×1.5 + 数据模型×2；分数-轮次映射：1-5分→max(3,ceil(分数))轮，6-15分→max(5,ceil(分数/2))轮，>15分→10轮）
- **验证门控（弹性模式）**：受影响项 100% 覆盖验证 + 全量至少 1 轮兜底遍历 + 产物完整性检查
- **子代理强制规则框升级**：7 个执行类阶段 SKILL.md 规则框从 3 条扩展为 4 条，新增前台/后台执行模式推荐（推荐前台模式，权限已预配置时允许后台模式）
- **kflow-bug-triage 增强**：新增影响范围评估步骤（DIAGNOSE 后、REPORT 前），输出新增 EXECUTION_MODE = SUBAGENT_REQUIRED 声明；bug 模板新增影响范围评估节（受影响功能点/接口/数据模型/分数）和执行模式字段
- **阶段执行历史追踪**：.status.md 模板新增「阶段执行历史」表（Phase/Execution Count/Last Type/Rounds/Score/Notes）和「最近修订信息」节（Trigger/Source/Timestamp/Summary/Affected Items/Score/Rounds），供执行阶段读取历史轮次信息
- **权限预配置**：新增 `.claude/settings.json` 预配置 kflow 所需权限（Bash 命令模式、Read/Write/Edit、Glob/Grep、Agent、WebFetch），子代理继承权限无中断
- **kflow-shared/repetition-model.md 升级**：新增 §14 弹性轮次决策、§15 验证门控、§16 阶段执行历史追踪、§17 影响范围分数读取；§12 新增 §12.4 执行模式推荐、§12.5 权限预配置；§4 流程图新增 CHECK_HISTORY 步骤；§7/§8/§10 从"10轮"改为"N轮（弹性决策）"
- **全局 10 轮硬编码消除**：7 个执行类阶段 SKILL.md + kflow-shared/gate-rules.md + kflow-resume SKILL.md 中"1/10"/"10/10"计数改为"1/N"/"N/N"（自审类阶段保留 10/10）
- 新增 3 个 specs（triage-impact-assessment/flexible-repetition-mode/subagent-enforcement-notice）+ 合并 4 个 specs（shared-repetition-model/subagent-isolation-rule/bug-triage-skill/execution-repetition-mode）
- 同步更新 9 个运行时 SKILL.md + 8 个设计文档 + 2 个模板文件

### v0.14.1 (2026-06-17)
**bugs/ 目录产出规范化——分页追加优先、BUG-ID 去前缀、修复记录归属重构**
- BUG-ID 改为纯序号 `BUG-{NNN}`，消除 `B-`/`W-`/`S-` 严重度前缀混用问题，严重度作为独立字段（`🔴 阻塞`/`🟡 警告`/`🔵 建议`）
- 分页规则强化「追加优先、满额新建」：登记新 BUG SHALL 追加到当前分页文件末尾，SHALL NOT 每次创建新文件；文件名统一为 `bug-{start}-{end}.md`
- 修复记录归属重构（A/B 双路径）：A 路径（用户反馈 → triage → L4 → bug-fix）修复记录回写到 `bugs/bug-NNN-NNN.md` 修复记录节，bugs/ 不再产出独立 fix-report；B 路径（测试发现 → bug-fix）fix-report 保留在子变更目录，若 bug 已在 bugs/ 登记则同步追加摘要
- 问题详情模板精简：去掉无意义 frontmatter（stage/skill/template_for），新增「修复记录」节（修复日期/根因分类/修复文件/验证结果/修复内容/Post-mortem），SKILL.md REGISTER 步骤增加 7 个必填节硬约束清单
- 新增 `bug-fix-writeback` capability spec，定义 bug-fix 对 bugs/ 目录的回写职责
- 同步更新 2 个运行时 SKILL.md（kflow-bug-triage、kflow-bug-fix）+ 2 个设计文档 + 2 个模板文件 + 3 个 specs（1 新建 + 2 修改）

### v0.14.0 (2026-06-16)
**子代理强制执行规则双写强化（集中+分散）**
- `repetition-model.md` §12 强化：新增 §12.1 主 Agent 职责边界硬线声明（调度+验收，SHALL NOT 执行阶段主工作，无例外）；细化 §12.2 重试粒度为轮次级（某轮子代理崩溃 → 新建 Agent 重跑该轮，≤3 次重试）；§12.3 适用阶段清单新增「子代理强制规则」列，覆盖全部 7 个执行类阶段
- 7 个执行类阶段 SKILL.md 新增「⚠ 子代理强制规则」引用框（3 条规则 + 参见 repetition-model.md §12），确保规则在执行时直接可见
- 7 个对应设计文档（docs/designs/skills/）同步新增子代理强制规则引用
- `07-agent-model.md` 新增 §15.3 子代理隔离规则强化子章节
- `subagent-isolation-rule` spec 新增 3 个 requirement（主 Agent 硬线、轮次级重试、SKILL.md 规则框），扩展适用范围至全部 7 个执行类阶段
- `shared-repetition-model` spec 新增 §12 强化场景
- 修复 kflow-plan.md 中指向不存在的 §15.11 断链引用

### v0.13.0 (2026-06-16)
**新增 kflow-bug-triage 问题分诊 Skill——四层溯源诊断+用户反馈统一入口**
- 新增 `kflow-bug-triage` 独立诊断 Skill：四层溯源漏斗（L1需求→L2原型→L3设计→L4实现），精确定位问题源头阶段后路由到对应 REVISION 模式或调用 kflow-bug-fix
- 新增 `bugs/` 问题登记目录：index.md 索引 + bug-NNN-NNN.md 分页详情（每文件≤20条），含完整生命周期状态追踪（待处理→处理中→已解决→已关闭）
- `kflow-bug-fix` **BREAKING**：三分法简化为二分法（去掉"设计错误"分类和回退路由），门控入口去掉"用户描述的缺陷信息"（用户反馈统一走 triage A路径），入口仅限测试阶段自动发现（B路径）
- `kflow-guide` 路由表更新：新增 triage 路由关键词（反馈/报告问题/报bug/提bug/问题 → kflow-bug-triage，优先级 1），"修复/Bug/缺陷"增加上下文判断逻辑（有活跃 bug-fix → bug-fix，否则 → triage）
- change-rollback spec 新增第七种回退触发来源（triage 诊断路由），支持回退到 explore/prototype-design/design
- 新增 2 个模板文件（bugs-index.md + bugs-detail.md）、2 个新 specs（bug-triage-skill + bug-registration）、修改 5 个 specs
- 同步更新 3 个运行时 SKILL.md + 9 个设计文档 + 5 个核心机制文档 + README.md

### v0.12.0 (2026-06-16)
**原型产物清单统一（Prototype Manifest Unification）**
- `prototype/index.md` 升级为 Prototype Manifest——新增「产物组织方式」段落（文件结构类型、入口文件路径）和「共享资源清单」段落
- 「原型文件清单」新增「角色」列（entry/page/tokens/coverage/shared/process），下游阶段按角色动态获取文件路径
- 下游阶段输入表统一入口：kflow-plan/kflow-code/kflow-code-review/kflow-e2e-test 的输入表中三个硬编码原型产物引用合并为 `prototype/index.md`（✅ 必须，前端SC）
- 门控检查从"三文件检查"改为"清单完整性检查"——检查 prototype/index.md 存在且含 entry 角色文件
- phase-hooks.md PRE_HOOK 和 RELOAD 表统一为 `prototype/index.md(条件,前端SC)`
- 编码阶段原型转译四阶段流程改为从清单获取文件路径，降级逻辑改为基于清单角色
- prototype/ 目录写权限仅归属原型设计阶段，其他阶段只读
- 同步更新 9 个运行时 SKILL.md + 3 个核心机制文档 + 7 个设计文档 + 5 个模板文件 + 6 个 specs（1 新建 + 5 修改）

### v0.11.0 (2026-06-16)
**RELOAD 增量模式——子代理 Token 优化**
- 新增 RELOAD 增量模式（phase-hooks.md §4.3）：主 Agent 调度子代理前为已读取且 mtime 未变的文件生成"已验证标记"（含 1-3 行摘要）
- 子代理收到已验证标记后可跳过完整文件读取，使用摘要信息；保留自行读取权（摘要不足时自行重读）
- 安全保障：标记仅在当前子代理调用内有效，下一个调用须重新检测 mtime；mtime 变化时不生成标记
- 设计规范文档同步更新（09-phase-hooks.md §5.4）
- 所有阶段 SKILL.md 通过引用 phase-hooks.md 自然兼容增量模式，无需修改引用格式
- 预估收益：子代理 RELOAD 步骤 Token 减少 40-60%
- 新增 1 个 spec（incremental-reload）+ 修改 2 个 specs（phase-file-reload / phase-hooks）

### v0.10.0 (2026-06-03)
**子变更类型严格二分执行机制**
- 新增 FP 类型标记体系（explore 阶段后端/前端二分 + 无法归类强制拆分），functional-designs/index.md 功能点清单增加「类型」列
- 子变更类型一致性自动校验（design 阶段 DIVIDE 步骤读取 FP 类型 → 全部一致通过/不一致阻塞流程），子变更类型由系统自动推断
- plan/code 阶段 FP 类型前置校验与跳过（类型不匹配 → 警告 + 跳过该 FP），向后兼容旧版文档
- 共享关切归属规则：错误码→后端子变更 / 配置项→后端子变更 / 共享 DTO→变更级 shared-types/ 目录 / Schema 变更→后端子变更 + UI 影响链追踪
- verify D3 维度拆分为 D3.1 输入源检查 + D3.2 输出越界检测（grep 模式 + 误报排除），严重度不阻塞
- code-review 新增跨层越界检测（在原型对账前执行），审查报告增加「跨层一致性」章节
- 新增 shared-types/ 条件产物目录模板，新增 4 个 specs（fp-type-classification / shared-concern-ownership / subchange-type-validation / cross-tier-violation-detection）+ 修改 5 个 specs

### v0.9.0 (2026-06-03)
**阶段产物验证与输入源对齐**
- 新增 kflow-verify 独立诊断 Skill（七维度诊断体系 + 三级严重度分级 + 修复路由）
- HITL 语义重定义（执行类型→设计不完整标记），子变更类型严格二分
- 前端编码输入限定为核心原型产物白名单，排除 design-prompt.md + design-system/MASTER.md
- plan/code/e2e-test/integration-test 阶段门控增强，RELOAD 清单扩展
- 新增 3 个 specs + 修改 5 个 specs

### v0.8.0 (2026-06-03)
**阶段产物验证与输入源对齐**
- 新增 kflow-verify 独立诊断 Skill（七维度诊断体系 + 三级严重度分级 + 修复路由），可随时调用诊断产物完整性
- HITL 语义重定义：从「执行类型」改为「设计不完整标记」，HITL 子变更 MUST 在设计阶段解决所有未决决策后方可进入 plan 阶段
- 子变更类型严格二分（后端子变更/前端子变更），禁止创建前后端混合子变更
- 各阶段输入源按 SC 类型区分：后端 SC 使用 functional-designs/ + detailed-design.md，前端 SC 使用 prototype/ 核心产物
- 前端编码输入限定为核心原型产物白名单（index.html/design-tokens.css/element-coverage-tree.md），排除 design-prompt.md 和 design-system/MASTER.md
- plan/code/e2e-test/integration-test 阶段门控增强（CONTEXT.md/functional-designs/api-tests/element-coverage-tree 条件检查）
- RELOAD 清单扩展（plan 增加 functional-designs/part-NN + prototype 核心产物 + api-tests；code 增加 CONTEXT.md + 前端条件）
- 新增前端子变更 API 契约依赖声明格式（METHOD /path → detailed-design.md §章节），在 plan 阶段传递到 tasks.md
- 门控规则显式标注 SC 类型适用性（[全部]/[后端子变更]/[前端子变更]/[前端项目]/[纯后端项目]）
- 新增 3 个 specs + 修改 5 个 specs

### v0.7.0 (2026-06-03)
**设计变更记录与同步追踪机制**
- 三个设计目录（functional-designs/prototype/detailed-design）统一修订记录表格式（合并原需求变更记录与修订记录），新增"修订类型"枚举列
- 新增 prototype/index.md 模板（原型文件清单、页面清单、设计系统引用、修订记录）
- .status.md 新增"设计修订同步追踪"节（每阶段独立确认列 plan/code/review/api-test/e2e-test/integ-test），频繁修订时各行独立追踪
- kflow-guide 新增 DESIGN_REVISION 模式（关键词→目标设计目录映射 + 分流到对应设计 Skill REVISION 模式 + 修订后回退/暂缓询问）
- 12 阶段 RELOAD 清单新增 functional-designs/index.md、prototype/index.md（条件）等文件，确保下游阶段感知设计修订
- 各阶段 Skill SKILL.md 同步更新产物输出规范

### v0.6.0 (2026-06-02)
**运行时环境隔离与首次就绪检测**
- 新增 `.kflow-runtime/` 运行时隔离目录，playwright 运行时环境从 `prototype/` 污染迁移到隔离区
- PRE_HOOK `READ_SERVICE_GUIDE` 扩展为四阶段就绪检测（DETECT→VALIDATE→COLLECT→PERSIST），含外部服务依赖自动识别与连接信息收集
- POST_HOOK `BROWSER_CLEANUP` 增加项目根目录执行约束
- kflow-code service-guide.md 生成增加外部服务依赖识别与配置状态标记（✅已就绪/⏳待配置）

### v0.5.0 (2026-06-02)
**前端实现子流程与阶段边界守卫**
- 前端实现集中为独立子变更（依赖 API 契约、原型转译任务模板、工程骨架→逐页转译→状态覆盖）
- Archive 阶段设为唯一禁止自动流转的阶段（必须用户显式确认）
- 阶段回退触发源从 4 个扩展到 6 个，新增编码发现原型问题/功能设计问题回退路径
- 原型产物从提示性约束升级为执行输入（含 design-system/MASTER.md 引用）
- 代码审查新增原型对账机制（硬编码检测/元素覆盖对账/路由覆盖对账）

### v0.4.0 (2026-05-29)
**元素覆盖树统一产物**
- 新增 `element-coverage-tree.md` 替代分散的 `element-spec.md` 和 `nav-tree.md`
- 四层页面→区域→元素→状态结构 + 操作链 + TC-ID 映射，强制 100% E2E 测试覆盖率
- 双路径生成：Path A 静态 HTML 解析 / Path B playwright-cli 动态探索
- design 阶段 100% 覆盖率门控，e2e-test 阶段元素触达率统计

### v0.3.1 (2026-05-28)
**运行时打包完整性**
- `with_server.py` 移入 `kflow-shared/scripts/`，实现运行时脚本随 Skills 打包分发
- 更新 service-lifecycle.md 和 phase-hooks.md 引用路径
- 合并 delta spec 到主 skill-packaging spec

### v0.3.0 (2026-05-28)
**阶段钩子与服务生命周期管理**
- 新增核心机制 09-phase-hooks.md（12 阶段钩子配置表、RELOAD 清单、服务停止超时链）
- 新增运行时共享 Skill（kflow-shared/phase-hooks.md + service-lifecycle.md）
- 新增 SKILL-template.md 通用模板（含钩子引用占位）
- 增强 with_server.py（--daemon 持久化模式、--status/--health/--stop-all、端口冲突检测）
- 12 个阶段 Skill 同步 PRE_HOOK/POST_HOOK 引用
- 5 个模板文件新增配置项追踪体系

### v0.2.0 (2026-05-26)
**简化 Git Commit 触发点**
- Git commit 触发点从 5 个强制简化为 2 个询问式
- 删除 kflow-guide PRECOMMIT 步骤、kflow-plan 每功能点 commit 步骤
- kflow-archive COMMIT 改为 AskUserQuestion 询问
- CLAUDE.md 强制规则改为询问式（保留版本自增+打包）

### v0.1.0 (2026-05-26)
**统一版本号管理与打包机制**
- 统一版本号管理（VERSION 文件替代 16 个 Skills 独立版本号）
- 新增打包机制（scripts/package-skills.sh → targets/kflow-devflow-skills-0.1.0.zip）
- CLAUDE.md 归档后打包规则注入
- 设计文档与运行时 Skill 同步

### v0.0.1 (2026-05-14 至 2026-05-25)
**初始版本与基础体系构建**
- KFlow Skills 体系项目初始化
- 实现 15 个 KFlow Skills（基于 docs/designs/ 设计文档）
- 原型设计阶段 v2.0.0 → v2.1.0 四大增强（OPTIMIZE 步骤、多文件输出、业务流程驱动、离线自包含）
- 原型验证与探索阶段增强（子代理委托调用、导航合理性验证、Playwright 全覆盖）
- 拆分 kflow-e2e-test 为 kflow-api-test + kflow-e2e-test
- 三阶段 SELFREV 统一改为子代理串行执行（10 轮重复制）
- 五大增强（Plan Mode 绕过、子代理隔离、复杂度评估、kflow-plan SELFREV）
- 7 个执行类阶段统一为重复制模式
- 六项执行规则细化（服务启动绑定、E2E 测试可选收集、原型设计决策门控、原型到代码一致性）
- 五项执行可靠性增强（双层遍历、原型修订模式、skill-suggestion 自动捕获、用户验收门控、中断恢复验证）
- 原型设计工具链灵活性增强（动态扫描环境 Skills、多方案推荐、STYLE+GENERATE 拆分）
- 文档整理与一致性修复（core-mechanisms.md 拆分为 8 文件、锚点引用批量更新）
- 新增项目画像注入、老项目逆向分析、Git 版本管理章节
