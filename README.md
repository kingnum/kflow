# KFlow DevFlow Skills

一套**文档驱动的阶段门控开发流程体系**，将软件开发从设计到交付的全流程标准化为一系列 Claude Code Skills，确保每个阶段产物可追溯、可验证。

> **版本**: 0.31.0 | **更新时间**: 2026-10-25 | **适用版本**: KFlow Skills 体系 2.0.0+

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
kflow-explore → kflow-prototype-design(可选) → kflow-design
    → kflow-plan → kflow-code → kflow-code-review → kflow-api-test
    → kflow-e2e-test → kflow-bug-fix(按需) → kflow-integration-test
    → kflow-verify(可选诊断) → kflow-audit → kflow-archive
```

### 纯后端项目（9 阶段，含审计门控）

```
kflow-explore → kflow-design
    → kflow-plan → kflow-code → kflow-code-review → kflow-api-test
    → kflow-bug-fix(按需) → kflow-integration-test
    → kflow-verify(可选诊断) → kflow-audit → kflow-archive
```

### 轻量档（阶段集合按适用性声明折叠）

`变更档位 = 轻量` 时，`接口单元测试`、`E2E测试`、`集成测试` 三个阶段为**条件适用**，由 kflow-design 在详细设计阶段产出的「阶段适用性声明」判定是否执行；被裁剪的阶段标注为 `⏭️ 不适用`，不产出对应产物。轻量档允许 1 或 2 个子变更（后端子变更 + 前端子变更），审计由单一子代理执行（全部档位同一形态：四项记账职责）。

```
kflow-explore → kflow-design（含阶段适用性声明）
    → kflow-plan → kflow-code → kflow-code-review
    → kflow-api-test(条件适用) → kflow-e2e-test(条件适用)
    → kflow-integration-test(条件适用) → kflow-audit(记账员审计) → kflow-archive
```

> `标准` 档不受影响，阶段集合维持上方两节所列；纯后端项目跳过 E2E 测试的既有规则亦不变。

### 阶段衔接

阶段之间**自动衔接**：每个阶段 Skill 的 COMPLETE 步骤完成后，按变更级 `.status.md` 的阶段状态直接调度下一阶段 Skill，无需用户输入推进指令。阶段自有的人工评审门控（原型设计决策、原型/详细设计用户评审、审计用户验收）照常执行。**归档是唯一例外**——审计完成后停止自动衔接，须由用户显式发起归档。

需要人工介入时有两种入口：`继续 {change-name}` 为轻量推进（读状态后直接调度目标阶段 Skill）；`恢复 {change-name}` 为中断恢复（定位断点、二次校验产物完整性、输出五问题摘要后调度）。

---

## 变更层级

```
变更 (Change) — 顶层管理单元
    │
    ├── 设计阶段（变更级统一完成）
    │   ├── 设计探索 (kflow-explore)
    │   ├── 原型设计 (kflow-prototype-design, 可选)
    │   └── 详细设计 (kflow-design)
    │         └── 按变更档位分级审查（轻量单 Agent / 标准两视角）+ 子变更划分
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
- 执行类阶段按类型二分：**单轮类**（接口单元测试 / E2E 测试 / 集成测试）单轮全面执行 + 定向重验（仅重跑失败用例，有界重试）；**重复制类**（编码 / 代码审查 / 缺陷修复）每轮遍历全部工作项独立执行完整流程，当前轮无新发现且无可执行工作时终止，连续 3 轮无实质进展则停滞升级；变更档位只决定审查强度与产出深度，不决定轮数，主 Agent 验收闭环

---

## 变更档位

**变更档位**是贯穿全流程的单一分级依据，决定各阶段的**每轮审查强度（审查形态）与产出深度**，SHALL NOT 决定轮数。它作为必填字段记录在变更级 `.status.md` 基本信息中。

| 档位 | 判定（设计面分数 `FP数×1 + 接口契约变更数×1.5 + 数据模型变更数×2`） |
|------|--------------------------------------------------------|
| 轻量 | 分数 ≤ 3 |
| 标准 | 分数 > 3 |

> 接口契约变更数只计**新增/修改**的 API 契约，受影响但契约未修改的接口不计入；数据模型变更数只计新增/修改的 schema/migration。受影响项清单（爆炸半径）由 triage 产出，只用于定向验证与回退判定，不参与档位计算。

**两段式判定**：
- **explore 初判**（SPLIT 之后）：按「变更类型 + 功能点数」映射——功能缺陷 FP≤3→轻量、FP>3→标准；功能需求 FP≤2→轻量、FP>2→标准；**产品需求按功能点数比照功能需求的分档规则判定**，SHALL NOT 无条件判定为 `标准` 之外的档位。用户在确认环节可上调或下调。
- **design 复核**（DIVIDE 之后）：按设计面分数复核。**硬升档**（数据迁移、破坏性契约变更、跨变更契约影响）必须提示且不可拒绝；**软升档**默认保持当前档位，仅在升档会新增下游测试阶段时提示，拒绝后记录理由且后续不再重复提示。仅允许升档，禁止降档，且不回退 explore。

**缺省回退**：历史变更的 `.status.md` 不含该字段，或字段取值不在 `{轻量, 标准}` 枚举内时按 `标准` 档处理（二档合并后 `标准` 等价于合并后的历史行为）；历史遗留的 `完整` 取值在读取侧一律归并为 `标准`，SHALL NOT 要求用户手工修改历史状态文件。

**档位驱动的行为差异**：

| 行为 | 轻量 | 标准 |
|------|------|------|
| 设计审查形态（审查强度） | 单 Agent 综合（覆盖四视角全部检查项） | 两视角并行（业务+技术 / 安全+质量） |
| 代码审查形态（审查强度） | 单 Agent（覆盖两视角全部检查项） | 两视角并行 |
| 子变更划分 | 轻量简化划分，1 或 2 个子变更（最小划分表） | 完整依赖关系划分 |
| 测试阶段适用性（接口单元测试 / E2E测试 / 集成测试） | 条件适用，按阶段适用性声明裁剪 | 必须执行（E2E 仅前后端） |
| 审计形态 | 单一子代理记账员审计（四项职责） | 单一子代理记账员审计（四项职责） |

> 档位决定的是**审查强度（审查形态）与产出深度**，SHALL NOT 决定轮数：设计类与计划阶段的自审为**固定单轮**（签署自证 → 1 轮独立子代理验证 → 统一修复），测试三阶段为**单轮全面执行 + 定向重验**；重复制类阶段（编码 / 代码审查 / 缺陷修复）的轮次由实际执行的循环决定。审查形态随档位变化，但**检查项不得缩减**——两种审查模式 MUST 覆盖业务/技术/安全/质量四视角的全部检查项。轻量档以单 Agent 形态承载审查、不产出多视角并行报告属合法状态，审计与归档不因此判缺项。
>
> **审查范围冻结**：审查对象集合由主 Agent 从阶段产物既有内容生成并冻结，审查维度集合封闭；子代理 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度。冻结范围之外的发现降级为「**范围外观察**」——不改产物、不计入发现数；子代理引入冻结范围外新内容时 SHALL 拒收该轮并要求在冻结范围内重新验证。
>
> **字段与判读**：`.status.md` 的 `执行轮次` 字段格式为 `{N} 轮`（无分母），**终止结果**取 `验证通过` / `验证发现问题({N})`（设计类与计划阶段）、`执行完成` / `定向重验失败` / `停滞`（执行类阶段）；自审报告固定一份 `self-reviews/{phase}/report.md`（原型 VERIFY 合并报告为 `verify-report.md`）。审计与归档据终止结果判读，SHALL NOT 以任何轮次数值为基准。机制权威定义见 `signed-checklist-verification`、`convergence-driven-repetition` 与 `agent-iteration-execution` 能力。

### 轻量档阶段裁剪机制

阶段裁剪**仅适用于轻量档**，用于削减对 1~3 个功能点的变更属空转的验证阶段。

**判定依据**：kflow-design 在 DIVIDE 之后读取客观产物信号，逐阶段判定并写入变更级 `.status.md` 的「阶段适用性声明」区：

| 阶段 | 判为适用的条件 |
|------|--------------|
| 接口单元测试 | `detailed-design.md` 接口设计章节含本变更新增或修改的接口条目 |
| E2E测试 | 项目类型为前后端项目，且本变更含页面、组件或路由的新增或变更 |
| 集成测试 | `detailed-design.md` 接口设计章节含本变更新增或修改的接口条目，或「跨子变更接口契约」章节含本变更条目 |

**保守回退**：判定依据不可读（产物不存在、格式不符、字段缺失）时该阶段判为**适用**——裁剪是优化，不是正确性要求，失败方向偏向执行。

**四态判定**：下游门控按「声明 × 产物」判定——声明不适用且产物不存在为合法跳过（通过）；声明不适用但产物存在为不一致（阻塞）；声明适用且产物存在为通过；声明适用但产物缺失为缺项（阻塞）。**无声明依据的 `⏭️` 一律阻塞**。

**覆盖率口径**：被裁剪阶段在 `traceability.md` 中整列填充 `⏭️`，并从覆盖率分母移除——`覆盖率 = 已填充格数 / (总格数 - 不适用格数)`。

**升档**：轻量档在 FP 类型混合时拆分为后端子变更 + 前端子变更，不升档；仅当超过 2 个子变更或单个子变更 FP > 10 时升档为 `标准`（经用户确认），按标准档重新划分并取消裁剪。复核阶段的硬升档（数据迁移、破坏性契约变更、跨变更契约影响）不可拒绝，软升档默认保持轻量。

> `标准` 档 SHALL NOT 应用裁剪，阶段集合维持既有规则；纯后端项目跳过 E2E 测试的既有规则不受影响。

---

## Skills 清单

### 入口与辅助

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-guide` | 意图识别、项目类型判断、变更检测、中断恢复路由（RESUME）、轻量推进路由（「继续 + 变更名」直接调度阶段 Skill） | 流程指引、帮助、如何开始、继续 {change}、恢复 {change} |
| `kflow-init` | 环境初始化、MCP/Skills 能力扫描、工具链推荐、老项目逆向分析、CLAUDE.md 注入、skill-suggestion 自动捕获规则注入 | 初始化、环境配置、工具推荐 |
| `kflow-status` | 未归档变更汇总 + 子变更进度矩阵 + 加权整体进度 | 状态、进度、任务总结 |
| `kflow-resume` | 中断恢复专用：断点定位（优先级链：checkpoint > .status.md > tasks.md）→ 产物完整性验证 → 五问题摘要 → 按共享阶段衔接决策表调度对应阶段 Skill | 恢复 {change} |
| `kflow-verify` | 独立诊断工具（非流程阶段）——七维度产物完整性诊断（文件存在/内容完整/输入源正确/交叉引用一致/设计决策完整/门控合规/审查闭环）+ 三级严重度分级（阻塞/警告/建议）+ 修复路由 + 诊断报告 | 诊断、验证产物、检查产物、verify |

### 设计阶段（变更级）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-explore` | 创建变更目录、项目类型检测、功能点原子级拆分、构建领域词汇表、需求澄清收敛门（未决问题清单归零后方可 SPLIT）、输出功能结构树、原型设计决策门控 | 开始新需求、设计探索、功能设计 |
| `kflow-prototype-design` | 编排层，默认复用 `docs/toolchain.md` 已锁定工具链 → 委托生成 HTML 原型（**直写产品级 `docs/designs/prototypes/`**）→ BUILD 四项静态门控（CDN 扫描/交叉引用/必检产物/清单一致）→ 审查方式二选一（人工审查 / 子代理自动审查验证）→ 离线自包含 + 生成 element-coverage-tree（Path A 静态解析）（仅前后端，可选） | 原型设计、UI 设计、交互设计 |
| `kflow-design` | 系统架构、数据模型、接口设计、NFR 定义、按变更档位分级设计审查（轻量单 Agent 综合 / 标准两视角并行）、变更档位复核（单向升档）、子变更划分（含 HITL/AFK 分类）、ADR 架构决策记录、element-coverage-tree Path B（playwright-cli 动态探索）+ 100% 覆盖率门控、复杂度评估（高复杂度 FP 逐项用户确认） | 详细设计、技术设计、架构设计 |

### 执行阶段（子变更级，重复制模式）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-plan` | 为子变更创建 TDD 任务清单 + DoD 四维验收标准（功能/质量/测试/文档）+ 单轮验证自审（签署自证 + 1 轮独立子代理验证 + 统一修复） | 任务计划、任务清单、实现计划 |
| `kflow-code` | TDD 编码实现、编译验证（PRE_HOOK）+ 多 Agent 并行编码、跨变更冲突检测、原型到代码一致性约束（从 `docs/designs/prototypes/manifest.md` + 变更级 `prototype-changes.md` 提取 design-tokens/element-coverage-tree 注入）、双层遍历全部子变更 | 编码实现、TDD、功能实现 |
| `kflow-code-review` | 按变更档位分级审查（轻量档单 Agent 覆盖两视角全部检查项 / 标准档两视角并行）+ 修复后验证按档位分支（轻量单轮复检 / 标准档分级重审闭环）+ 原型对账 Grep + 双层遍历全部子变更 | 代码审查、code review |
| `kflow-api-test` | curl/HTTP 方式对 api-tests/ 逐条测试、健康评分五维度（功能完整性/响应时间/HTTP状态码/错误处理/契约一致性）、所有项目类型必须 | 接口测试、API测试、接口单元测试 |
| `kflow-e2e-test` | Playwright snapshot+ref 模式浏览器自动化测试、决策树路由、element-coverage-tree 元素触达率统计、generated-test 可选收集（通过率≥80%）、仅前后端项目 | E2E 测试、QA 测试、浏览器自动化测试 |
| `kflow-bug-fix` | 子变更级二分法根因分类修复（实现错误/测试错误）、多 Agent 并行分析、Post-mortem 复盘。用户反馈统一由 kflow-bug-triage 处理 | 缺陷修复、Bug 修复 |

### 收尾阶段（变更级）

| Skill | 说明 | 触发词 |
|-------|------|--------|
| `kflow-integration-test` | 变更级集成测试 + 内聚四分法修复循环（实现错误/契约错误/测试错误/架构设计错误）、架构评估自动触发（连续 3 轮同用例失败）、服务持久化模式管理 | 集成测试、跨子变更测试 |
| `kflow-audit` | 四项记账职责（门控校验 / 覆盖率与产物校验 / 耗时汇总 / 阻塞兜底）、归档门控集成、审计回退路由、SKILL.md 钩子引用合规检查 | 审计、评估、检查 |
| `kflow-archive` | 门控检查 → 设计合并（功能设计+详细设计）+ 原型改动登记到 `docs/designs/prototypes/manifest.md` → 全景更新 → 移至 docs/changes/archive/ → AskUserQuestion 询问 git commit（含版本自增+打包） | 归档、完成、变更结束 |

---

## 常用工作流

### 新功能开发

```
1. "我想添加用户认证功能"       → 直接进入 kflow-explore（新变更入口）
2. kflow-explore               → 判定变更类型、确定变更名称、变更档位初判、冲突预检、创建变更目录、原子级拆分功能点、构建领域词汇表
3. kflow-prototype-design      → (可选) HTML 交互原型（直写产品级）+ 元素覆盖树 Path A + BUILD 门控 + 可选自动验证
4. kflow-design                → 系统架构 + 分级设计审查 + 划分子变更 + ADR 记录 + 元素覆盖树 Path B + 100% 覆盖率门控
5. kflow-plan                  → 子变更 TDD 任务清单 + DoD 验收标准
6. kflow-code                  → TDD 编码实现 + 编译验证 + 原型到代码一致性约束
7. kflow-code-review           → 按档位分级审查（轻量单 Agent / 标准两视角）+ 修复后验证
8. kflow-api-test              → curl/HTTP 接口逐条测试 + 健康评分
9. kflow-e2e-test              → (仅前后端) Playwright 浏览器自动化测试 + 元素触达率统计
10. kflow-bug-fix               → (按需) 二分法根因分类修复（B路径：测试失败触发）
11. kflow-integration-test      → 变更级跨子变更集成测试
12. kflow-audit → kflow-archive → 记账员审计 + 归档（含版本自增+打包）
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
用户: 恢复 add-user-auth
→ kflow-guide PARSE 正则匹配 → RESUME 路由到 kflow-resume
→ 优先级链读取状态（checkpoint > .status.md > tasks.md）
→ 定位断点 → 产物完整性二次校验 → 五问题快速摘要 → 调度阶段 Skill
```

### 轻量推进

```
用户: 继续 add-user-auth
→ kflow-guide PARSE 正则匹配 → 读取 .status.md
→ 按阶段衔接决策表直接调度目标阶段 Skill（不经过 kflow-resume）
```

---

## 触发词速查

| 你想做的事 | 说这个 |
|-----------|--------|
| 开始新功能 | "开始新需求" / "添加 XX 功能" / "开发 XX" |
| 获取流程指引 | "流程指引" / "帮助" / "如何开始" |
| 继续推进（轻量） | "继续 {change-name}" |
| 中断后恢复（完整） | "恢复 {change-name}" / "resume {change-name}" |
| 查看进度 | "状态" / "进度" / "查看进度" |
| 原型/UI 设计 | "原型设计" / "UI 设计" / "交互设计" |
| 详细设计 | "详细设计" / "技术设计" / "架构设计" |
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

> 以下为**安装 KFlow 后的业务项目**（Skills 的运行目标项目）的目录形态。本仓库是 Skills 的开发仓库，自身结构不同——Skill 实现产物在 `skills/`、体系设计文档在 `docs/designs/`、规格在 `openspec/specs/`，均不出现在业务项目中。

```
.claude/
├── settings.json                      # kflow-init 生成的权限配置（幂等合并，不覆盖既有内容）
├── settings.local.json                # 本地个人配置（可选，Claude Code 标准文件）
└── skills/                            # 安装的 KFlow Skills（每个 Skill 自包含，零外部依赖）
    ├── kflow-guide/SKILL.md
    ├── kflow-explore/SKILL.md
    ├── kflow-code/                    #   单个 Skill 的目录形态（示例）
    │   ├── SKILL.md                   #   阶段主流程定义
    │   ├── references/                #   本阶段专属辅助规则（分层加载的来源，不跨 Skill 共享）
    │   │   ├── state-values.md        #     状态值定义（基础层）
    │   │   ├── gates.md               #     阶段门控规则（基础层）
    │   │   ├── repetition.md          #     重复制执行规范（执行层）
    │   │   ├── hooks.md               #     PRE_HOOK/POST_HOOK 执行规范（服务层）
    │   │   └── service-lifecycle.md   #     服务生命周期管理：daemon 模式、端口冲突检测
    │   └── scripts/                   #   运行该阶段所需的脚本（无则省略）
    │       └── with_server.py         #     服务管理脚本（--daemon/--status/--health/--stop-all）
    └── ...                            # 共 18 个 kflow-* Skills

.kflow-runtime/                        # 运行时隔离区（Playwright 隔离安装等，受 .gitignore 排除）

docs/
├── CONTEXT.md                        # 项目级领域词汇表
├── service-guide.md                  # 项目服务指引（多环境配置）
├── skill-suggestion.md               # Skills 优化建议记录
├── toolchain.md                      # 工具链配置（kflow-init 生成）
│
├── changes/                          # 变更管理目录
│   ├── index.md                      # 变更管理索引（活跃 + 已归档）
│   ├── archive/                      # 归档目录
│   │   └── {YYYY-MM-DD}-{change}/    # 归档的变更（整体归档，保持原结构）
│   └── {change-name}/                # 单个变更
│       ├── .status.md                # 变更总状态文件（含子变更进度矩阵）
│       ├── tasks.md                  # 变更总任务清单（子变更级 checkbox）
│       ├── functional-designs/       # 功能设计文档（目录化，part-NN.md 分册 ≤30 功能点）
│       ├── prototype-changes.md      # 原型改动清单（可选，含改动前哈希）
│       ├── prototype-backup/         # 原型改动前快照（可选，按产品级相对路径镜像）
│       ├── prototype-plan/           # 原型过程产物（design-prompt.md、style-decision.md）
│       ├── detailed-design.md        # 统一详细设计（变更级，含 NFR 章节）
│       ├── element-coverage-tree.md  # 元素覆盖树（四层结构+操作链+TC-ID映射，100% E2E 覆盖）
│       ├── traceability.md           # 覆盖追溯矩阵（FP × 阶段产物）
│       ├── api-tests/                # 接口测试用例（目录化，part-NN.md 分册 ≤30 接口）
│       ├── e2e-tests/                # E2E 测试用例（目录化，仅前后端）
│       ├── integration-tests/        # 集成测试用例（目录化）
│       ├── self-reviews/             # 自循环审查记录（explore/prototype/design）
│       ├── cross-reviews/            # 交叉审查报告（标准两视角/轻量单 synthesis，批次目录，按变更档位）
│       ├── migrations/               # 数据库迁移（变更级）
│       ├── bugs/                     # 问题登记（index.md + bug-NNN-NNN.md 分页详情）
│       └── subchanges/               # 子变更目录
│           └── {subchange-name}/
│               ├── .status.md        # 子变更状态文件
│               ├── tasks.md          # 子变更任务清单（功能点级全展开）
│               └── test-reports/     # 测试报告（api/e2e/review/fix-reports）
│
├── designs/                          # 产品级设计文档
│   ├── index.md                      # 产品级设计索引入口
│   ├── functional-designs/           # 按功能模块拆分的产品级功能设计（{menu}/index.md + part-NN.md 或 {domain}.md）
│   ├── detailed-designs/             # 产品级详细设计（6 文件体系）
│   │   ├── architecture.md           # 全景架构
│   │   ├── data-model.md             # 全景数据模型
│   │   ├── api-catalog.md            # 全景 API 目录
│   │   ├── nfr-baseline.md           # NFR 基线
│   │   ├── config-items.md           # 配置项设计
│   │   └── error-handling.md         # 错误处理设计
│   ├── prototypes/                   # 产品级原型（唯一来源，原型设计阶段直写）
│   │   ├── index.html                # 全产品导航入口
│   │   ├── manifest.md               # 全产品原型清单（产物/角色/来源变更/修订记录）
│   │   ├── design-tokens.css         # 设计令牌
│   │   ├── design-system/MASTER.md   # 设计系统主文档
│   │   ├── screens/                  # 各屏幕页面 HTML
│   │   ├── components/               # 共享组件
│   │   └── assets/                   # 静态资源
│   └── changelog.md                  # 变更日志（按年归档）
│
└── adr/                              # 架构决策记录
```

---

## 最佳实践

**命名规范**：功能新增 `add-{feature}`，Bug 修复 `fix-{issue}`，产品搭建 `{platform}-init`

**功能点拆分**：每个功能点单一明确，原子级拆分，子变更 ≤ 10 个功能点，标注依赖关系

**子变更划分**：按设计域聚合，无依赖可并行，优先基础设施子变更，标注 HITL/AFK 执行类型

**阶段钩子**：所有阶段通过 PRE_HOOK/POST_HOOK 标准化服务生命周期管理——PRE_HOOK 负责状态检查/文件重载/服务启动/健康检查，POST_HOOK 负责服务停止/浏览器清理/状态更新；钩子执行规范统一引用各阶段自身的 `references/hooks.md`，不内联复制

**元素覆盖树**：前后端项目在 prototype-design（Path A 静态 HTML 解析）和 design（Path B playwright-cli 动态探索）阶段双路径生成 `element-coverage-tree.md`，design 阶段 100% 覆盖率门控，e2e-test 阶段统计元素触达率

**原型设计**：前端 UI 变更推荐使用，纯后端自动跳过；TOOLCHAIN 默认复用 `docs/toolchain.md` 已锁定工具链（无锁定/Skill 失效/用户要求更换时才重新扫描选择）；DESIGN 拆分为 STYLE（风格推荐）+ GENERATE（工具链执行），产物**直写产品级 `docs/designs/prototypes/`**，变更级只留 `prototype-changes.md`（含改动前哈希）/`prototype-backup/`/`prototype-plan/`；DESIGN 后 BUILD 四项静态门控必做（CDN 扫描/交叉引用/必检产物/清单一致，零子代理），通过后用户二选一：人工审查（跳过全部自动验证）或子代理自动审查验证（VERIFY 单轮合并验证——导航合理性 / Playwright 全覆盖 / UX 规则审查 / 对比度检测合并为单轮单报告 `self-reviews/prototype/verify-report.md`，另有 SELFREV 单轮验证）；离线自包含（禁 CDN + 系统字体栈）

**代码审查**：独立于编码阶段，按变更档位分级审查——轻量档单 Agent（覆盖两视角全部检查项），标准档两视角并行。修复后验证同样按档位分支：轻量档单轮复检；标准档分级重审闭环（高严重度需全量重审，中严重度原视角重审，低严重度抽查验证）

**接口测试**：所有项目类型必须阶段，curl/HTTP 逐条验证，五维度健康评分

**服务管理**：通过 `with_server.py` 统一管理——`--daemon` 持久化模式保持服务运行、`--status/--health` 状态查询、`--stop-all` 批量停止、端口冲突自动检测

**推进与恢复**：`继续 {change-name}` 为轻量推进——读取状态后直接调度当前/下一阶段 Skill，不执行重恢复流程；`恢复 {change-name}` 为中断恢复——精确定位断点并自动验证产物完整性。日常推进无需输入任何指令：阶段 Skill 的 COMPLETE 步骤完成后会自动衔接下一阶段，仅在归档前停止并提示用户显式发起

---

## 常见问题

**纯后端和前后端项目的流程区别？** 纯后端跳过「原型设计」和「E2E 测试」，共 9 阶段（含审计门控）；前后端 11 阶段。系统自动检测。

**一个变更可以有多少子变更？** 最少 1 个，最多 20 个。超过需拆分多个变更。

**子变更可以并行吗？** 无依赖的可并行，AFK 类型可自动并行。

**执行类阶段的执行模型是什么？** 6 个执行类阶段按类型二分。**单轮类**（api-test/e2e-test/integration-test）采用**单轮全面执行 + 定向重验**——一轮内遍历全部工作项执行完整流程，发现失败项时仅重跑失败用例（有界重试，与已移除的 `recheck-round` 语义不同）；连续 3 次定向重验未通过则终止结果记 `定向重验失败` 并升级用户。**重复制类**（code/code-review/bug-fix）采用**重复制循环**——子代理每轮遍历全部工作项独立执行完整流程，当前轮无新发现且无可执行工作时终止（终止结果 `执行完成`）；连续 3 轮无实质进展则终止结果记 `停滞` 并升级用户（记录 `skill-suggestion.md` + AskUserQuestion，可标记 ⚠️ 阻塞）。审查范围冻结：审查对象集合由主 Agent 从阶段产物既有内容生成并冻结，冻结范围之外的发现降级为「范围外观察」，不改产物、不计入发现数。变更档位只决定审查形态与产出深度，SHALL NOT 决定轮数；`.status.md` 的 `执行轮次` 字段格式为 `{N} 轮`。验证门控要求受影响项 100% 覆盖 + 产物完整性，主 Agent 负责最终验收。kflow-plan 阶段的主工作由子代理执行，其产物自审为单轮验证（签署自证 + 1 轮独立子代理验证 + 统一修复）。

**变更档位怎么判定？** 设计面分数 = `功能点数×1 + 接口契约变更数×1.5 + 数据模型变更数×2`；分数 ≤3 为轻量、>3 为标准（枚举为 `{轻量, 标准}` 二值）。接口契约变更数只计新增/修改的 API 契约，数据模型变更数只计新增/修改的 schema/migration；受影响但未改契约的接口不计入。`产品需求` 无独立映射，按功能点数比照 `功能需求` 的分档规则判定。分两段判定：explore 的 SPLIT 之后按「变更类型 + 功能点数」初判（用户可覆盖），design 的 DIVIDE 之后按设计面分数复核——硬升档（数据迁移、破坏性契约变更、跨变更契约影响）不可拒绝，软升档默认保持轻量、仅在新增下游测试阶段时提示。历史变更缺该字段，或字段取值为历史遗留的 `完整` 时，按 `标准` 档处理。详见上文「变更档位」章节。

**轻量档会不会因为没有多视角报告而被审计判缺项？** 不会。轻量档自审为**单轮验证**、固定产出 `self-reviews/{phase}/report.md`（无 0 轮豁免），但设计审查仅一份 `synthesis.md`（单 Agent 综合四视角）、代码审查为单 Agent——缺少多视角并行报告是**合法状态**，审计与归档 SHALL NOT 因此判缺项或阻塞。

**轻量档可以跳过哪些阶段？** 仅 `接口单元测试`、`E2E测试`、`集成测试` 三个阶段可裁剪，由 kflow-design 在详细设计阶段按客观信号判定并写入变更级 `.status.md` 的「阶段适用性声明」区。判定依据不可读时保守回退为「适用」。**标准档不允许裁剪**。判定依据是唯一的合法性凭证——人工标记的 `⏭️` 若无声明依据，在阶段门控、归档门控与产物诊断中一律阻塞。

**跳过阶段会不会让覆盖率门控报缺口？** 不会。被裁剪阶段在 `traceability.md` 中整列填充 `⏭️`，并从覆盖率分母移除（`覆盖率 = 已填充格数 / (总格数 - 不适用格数)`），该列不参与 100% 判定、不产生缺口记录。无声明依据的 `⏭️` 则相反——阻塞归档并提示缺失裁剪依据。

**设计阶段发现问题？** 触发阶段回退（⚠️ 需修订），三级回退机制——子变更级回退仅影响当前子变更，接口契约变更回退影响相关子变更，架构级回退需重新设计。

**集成测试连续失败？** 连续 3 轮同一用例失败自动触发架构评估，防止设计问题在测试阶段反复消耗资源。

**归档后还能修改吗？** 不能。归档变更移至 `docs/changes/archive/`，禁止修改。需修改应创建新变更。

**阶段钩子（PRE_HOOK/POST_HOOK）是什么？** 每个阶段执行前后的标准化服务生命周期管理步骤。PRE_HOOK 负责状态检查、文件重载、服务启动、健康检查；POST_HOOK 负责服务停止、浏览器清理、状态更新。钩子执行职责归属于变更级 Agent，子变更 Agent 不执行钩子。

**元素覆盖树（element-coverage-tree.md）是什么？** 前后端项目的 E2E 测试覆盖基础文档，提供四层页面→区域→元素→状态结构 + 操作链 + TC-ID 映射。双路径生成——Path A 从 HTML 原型静态解析，Path B 通过 playwright-cli 动态探索实际页面。design 阶段 100% 覆盖率门控通过后方可进入执行阶段。

**各 Skill 如何接入钩子机制？** 每个 Skill 通过自身的 `references/hooks.md`（PRE_HOOK/POST_HOOK 执行规范）与 `references/service-lifecycle.md`（服务生命周期管理指令）接入钩子机制，辅助规则随该 Skill 目录一并打包分发，不在 SKILL.md 中内联复制钩子逻辑，也不依赖任何跨 Skill 共享目录。审计阶段会检查此合规项。

**如何管理长时间运行的服务？** 通过 `with_server.py --daemon` 持久化模式启动，服务在多个阶段间保持运行。使用 `--status` 查询状态，`--health` 检查健康，`--stop-all` 批量停止。端口冲突自动检测并报告。

---

## 相关文档

- [设计文档入口](docs/designs/index.md) — Skills 体系设计文档（版本 2.0.0）
- [核心运行机制](docs/designs/core-mechanisms/index.md) — 目录结构、状态文件、阶段流转、门控规则、重复制模式、回退机制（9 文件拆分）
- [阶段钩子规范](docs/designs/core-mechanisms/09-phase-hooks.md) — PRE_HOOK/POST_HOOK 配置表、RELOAD 清单、服务生命周期
- [运行时钩子规范（示例：kflow-code）](skills/kflow-code/references/hooks.md) — 各阶段自身的 `references/hooks.md` 定义该阶段的 PRE_HOOK/POST_HOOK 步骤序列
- [服务生命周期管理（示例：kflow-code）](skills/kflow-code/references/service-lifecycle.md) — daemon 模式、端口冲突检测、服务停止超时链
- [OpenSpec 规格](openspec/specs/) — 130 个核心机制/阶段规格文件
- [CLAUDE.md](CLAUDE.md) — Claude Code 项目指令（含钩子引用强制规则、版本自增+打包规则）

---

> 本手册随 KFlow Skills 体系持续更新。如有疑问或建议，请通过 `docs/skill-suggestion.md` 记录反馈。

---

## 版本更新说明

### v0.31.0 (2026-10-25)

**探索阶段捕获用户视角非功能期望与页面清单：NFR 需求输入链打通，页面结构获得变更级最低承载**

- **非功能期望小节（§一）**：functional-designs/index.md 变更概述新增「非功能期望」小节（期望维度/期望描述/关联功能点三列，开放枚举），使用用户视角业务语言、SHALL NOT 定义技术目标值；无显式期望时整节标注「本变更无特殊非功能期望」
- **页面清单章节（§四）**：紧随功能结构树新增页面清单（页面名称/菜单路径/类型/区块级结构描述/涉及功能点），作为原型设计输入基线并为跳过原型设计的变更提供页面结构最低承载；原 §四~§八 顺延为 §五~§九；纯后端/无前端 FP 标注「本变更无涉及页面」
- **CLARIFY 遍历域五域扩为六域**：收敛门候选清单新增「非功能期望」域，空清单凭据说明同步扩展，非功能期望歧义进入未决问题清单
- **NFR 消费闭环**：kflow-design 步骤 6（NFR）与 detailed-design.md §三 显式声明以探索侧「非功能期望」小节为需求输入，将用户期望转译为可度量技术目标值；探索侧标注「无」时按既有最小要求自行定义
- **自审与边界**：explore 自审完整性检查新增「页面清单一致性」（无孤页/漏页）；阶段边界约束明确非功能期望为业务语言输入、页面清单为区块级文字描述（视觉稿仍属 prototype 阶段）
- **轻量档配套**：单页压缩形态扩为「功能点清单+影响分析+修复/实现范围+非功能期望（一行，无则标注）+页面清单（简表或『无』标注）」，不新增流程步骤

### v0.30.0 (2026-10-19)

**档位公式回归设计面：缺陷修复不再因影响面被机械升档，轻量档允许前后端各一子变更，升档分型为硬升档/软升档**

- **设计面分数与影响面清单分离**：档位公式改为 `功能点数 x 1 + 接口契约变更数 x 1.5 + 数据模型变更数 x 2`；「接口契约变更数」仅计新增或修改契约的 API，受影响但未改契约的接口不计入；纯数据修正不计入数据模型变更数。受影响项清单（爆炸半径）仍由 triage 产出，仅用于定向验证与回退范围，不参与档位计算。字段名「影响范围分数」在状态文件中保留，语义改为设计面分数
- **轻量档最多两个子变更**：轻量档由「单一子变更」放宽为 1 或 2 个（后端 + 前端各一），使用最小划分表（子变更名称、类型、包含功能点、实现顺序、依赖说明），不执行标准档的完整依赖关系分析；若无法在 2 个子变更内完成划分（例如任一子变更功能点超过 10 个）则升为 `标准`
- **类型混合不再强制升档**：轻量档 FP 类型混合时拆分为后端子变更与前端子变更；标准档同一子变更内混合仍阻塞
- **硬升档与软升档分型**：硬升档（数据迁移、破坏性接口契约变更、跨变更契约影响）不可拒绝；软升档默认保持当前档位、用户可主动选择升档，拒绝后记录理由且后续阶段不再重复提示
- **升档必要性判定**：仅当升档会实际新增至少一个下游测试阶段，或属于硬升档时才提示；否则维持当前档位并记录「未升档理由」
- **三档残留清理**：清理设计文档与规格中的 `4~15 / >15 / 完整` 旧表述；历史 `完整` 取值仍按 `标准` 读取，已升档变更不回退降级
- **兼容性**：状态文件字段名与结构不变，无数据迁移

### v0.29.0 (2026-10-19)

**简单缺陷默认走快车道：修复意图脱离活跃变更门控、新增项目级缺陷工作区、归档门控纳入项目级阻塞缺陷**

- **修复意图脱离活跃变更（BREAKING）**：`kflow-guide` 将修复类意图直接路由到 `kflow-bug-triage`，不再因无活跃变更而引导 `kflow-explore` 创建变更；存在活跃变更时也不直接新建变更。流程概览新增「缺陷修复快车道」作为独立于变更阶段的路径
- **缺陷工作区判定**：`kflow-bug-triage` 解除「必须存在活跃变更」门控。新增项目级 `docs/bugs/` 工作区，承载用户反馈的缺陷（A 路径）与不属于任何活跃变更的缺陷；变更级 `bugs/` 保留给测试阶段自动发现（B 路径）。存在活跃变更时先判归属：由该变更引入则登记到变更级，否则登记到项目级
- **L4 默认进入快车道**：入口条件为 L4 + 不修改 L1/L2/L3 产物 + 无数据迁移/破坏性契约变更 + 受影响项可枚举 + 用户确认；不满足时才创建 `功能缺陷` 变更并路由到对应设计阶段
- **快车道覆盖项目级根**：`bugfix-status.md` 支持 `docs/bugs/fix/{BUG-ID}/` 与变更级 `bugs/fix/{BUG-ID}/` 两种根；验证目标由「测试用例 ID」扩展为已有自动化测试、新增回归测试、手工验证步骤三类；项目级快车道不触发变更审计、归档、版本自增或打包
- **归档门控读取项目级缺陷**：`kflow-archive` 读取 `docs/bugs/index.md`，未关闭的 🔴 阻塞级缺陷阻断归档；`docs/bugs/` 不参与任何变更归档
- **影响范围评估适配两种工作区**：无活跃变更时以产品级设计产物作为证据来源；受影响项清单作为快车道定向验证的唯一范围依据
- **模板与实现层同步**：新增 `docs/designs/templates/bugs/` 模板族；`kflow-guide`、`kflow-bug-triage`、`kflow-bug-fix`、`kflow-archive` 的 SKILL.md 与设计规格同步更新
- **兼容性**：既有变更级 `bugs/` 与 `bugfix-status.md` 保持有效，不回填历史变更

### v0.28.0 (2026-10-17)

**上下文预算优化：references 按阶段切片、读取纪律、状态分层、文档留存边界与主 Agent 门控**

- **references 按阶段切片（BREAKING）**：`gates.md` / `repetition.md` / `state-values.md` / `self-review.md` / `phase-transition.md` / `service-lifecycle.md` / `hooks.md` 由逐字节副本改为按阶段切片。权威源迁至 `references-src/`，各 skill 副本由 `scripts/sync-references.sh`（Python 实现 `scripts/sync_references.py`）按 `references-src/slice-manifest.tsv` 生成并校验；`scripts/gen-slice-manifest.py` 生成切片清单。**`skills/*/references/` 下的共享文件禁止手工编辑**
- **读取纪律**：已拆分文档经 `index.md` 定位后读取目标分册或行区间；主 Agent 构造子代理 prompt 时优先注入片段；同阶段内不重复全文读取、mtime 变化后重读、不依赖上一阶段上下文残留；RELOAD 清单为每个条目标注定位来源
- **状态分层**：`.status.md` 仅承载当前有效状态（≤100 行），历史移入 `status-log.md`（仅中断恢复与审计读取）；阶段完成/回退时双写
- **文档留存边界**：文档头部修订记录保留最近 3 条，超出部分移入 `revision-history.md`（变更级）或 `docs/designs/changelog.md`（产品级）；产品级文档 >30 KB 提供章节索引、>80 KB 拆分为目录化结构，术语表例外；归档设计合并步骤自动执行裁剪、索引维护与拆分触发
- **主 Agent 禁手门控**：新增 `main-agent-execution-gating` 能力——执行类阶段主 Agent 的越界 `Edit`/`Write` 与长输出命令由 `PreToolUse` hook 拒绝，子代理放行。三条实时探针已确认路径 A（stdin 的 `agent_id`/`agent_type`），`Task`/`Agent` 拦截点不可达、会话级 deny 无法被 `permissionMode` 解除
- **子代理粒度上限**：单个子代理不超过 3 个功能点或 10 个 TDD 步骤；工作量上限与轮数上限口径显式区分
- **新 Skill `kflow-doc-optimize`**：独立维护工具（非流程阶段），扫描 → 清单 → 用户确认 → 仅搬移/拆分/建索引 → 引用校验；随包提供 `scan_docs.py`、`check_refs.py`（find/ replace/ verify）与报告模板。Skill 数量 18 → 19
- **`kflow-init` 增强**：写入 `autoCompactWindow: 300000`、安装主 Agent 门控脚本并注册 hook、注入 `kflow-doc-optimize` 适用边界例外声明；新增 `verify_project_config.py` 配置校验。两条幂等规则：已存在且更小的压缩阈值不覆盖、项目自定义 hook 条目保持不变
- **打包修复**：`package-skills.sh` 优先产出真正的 zip（`zip` 命令 / Python `zipfile` / PowerShell `Compress-Archive`），无工具时降级为 `.tar.gz` 并提示
- **兼容性**：历史变更的未分层 `.status.md` 按单文件口径兼容读取，不强制回填；门控在无法判定阶段时放行，异常 fail-open，可设置 `KFLOW_GATING_DISABLE=1` 临时关闭

### v0.27.0 (2026-10-14)

**变更档位由三档收敛为二档：`完整` 档合并入 `标准` 档，四视角并行审查废除**

- **档位枚举二值化（BREAKING）**：`变更档位` 取值由 `{轻量, 标准, 完整}` 三档收敛为 `{轻量, 标准}` 二档——阈值由 `≤3 轻量 / 4~15 标准 / >15 完整` 改为 `≤3 轻量 / >3 标准`；**缺省回退值由 `完整` 改为 `标准`**：字段缺失或取值非法时按 `标准` 档处理；历史变更遗留的 `完整` 取值在**读取侧一律归并为 `标准`**，不要求用户手工修改历史状态文件
- **四视角并行审查废除（BREAKING）**：设计交叉审查形态收敛为两种——`轻量` 单 Agent 串行综合（覆盖四视角全部检查项）/ `标准` 两视角并行（业务+技术 / 安全+质量）；不再存在四份独立视角报告的产出路径，进入计划门控由三分支降为两分支。**检查项覆盖不缩减**——被移除的是并行度，不是审查内容
- **删除 `完整` 档专属的评分报告深度**：自审、代码审查与测试类阶段的执行报告不再要求输出各维度 0–10 评分与不达标项清单（该要求本就不参与终止判定，与审计去除评分的方向一致）
- **同路径既有不一致的清理**：修正 `state-values.md` 档位定义中残留的产品需求硬映射残句（0.24.0 已删除该硬映射）、删除「审计审查维度适配审查模式」要求、删除集成测试阶段将执行轮次挂靠轻量档的残句
- **实现层同步**：10 份 `references/state-values.md`、10 份 `references/gates.md`、8 份 `references/repetition.md`、3 份 `references/self-review.md`、16 份 `SKILL.md`，以及核心机制文档、Skills 设计规格、产物模板、示例与 README 档位章节同步
- **兼容性**：历史变更 `.status.md` 的 `变更档位 = 完整` 由读取侧归并为 `标准`；历史 `cross-reviews/` 下的四份视角报告保留为历史记录，读取侧不再要求其存在、亦不因其存在而阻塞门控

### v0.26.0 (2026-10-14)
**消除流程中途回 guide 的往返：阶段自动衔接、推进与恢复语义分离、guide 职责收敛为新变更外的四项**

> **本次升级需重跑 `/kflow-init`**：消费方 CLAUDE.md 中的「变更流程强制规则」section 不会自动更新，须由 `kflow-init` 依 marker 版本判据替换。未重跑的消费方行为保持原样（旧规则继续生效），升级本身不产生破坏。

- **移除流程中回 guide 的强制（BREAKING）**：删除 CLAUDE.md 注入的「所有用户变更必须首先通过 `kflow-guide` 进行流程指引」与「禁止直接调用阶段 Skill 跳过 guide 指引」两条规则。正常变更执行期间不再被弹回 guide，阶段 Skill 可直接调用
- **新变更入口改由 `kflow-explore` 承接（BREAKING）**：变更类型分类、变更命名、档位初判与冲突预检均在 explore 阶段完成（其 INIT/CLASSIFY/TIER/CONTEXT 步骤已自足），guide 侧的「NEW CHANGE 创建前指引」因完全重复而删除
- **新增阶段自动衔接**：阶段 Skill 的 COMPLETE 步骤完成后 SHALL 直接调度下一阶段 Skill，SHALL NOT 提示用户输入推进指令（如「继续 {change-name}」）。衔接决策表（`✅ 完成` 递归推进 / `🔄`、`⏳` 调度该阶段 / `⚠️ 需修订` 调度回退目标 / `❌` 阻塞不调度 / `⏭️` 视为已通过）从 `kflow-resume` 的私有实现提升为跨 skill 通用规则，落于各阶段 Skill 自带的 `references/phase-transition.md`（含 `kflow-resume` 共 11 份副本，由 `scripts/sync-references.sh` 保障一致）
- **推进与恢复语义分离（BREAKING）**：「继续 {change-name}」为**轻量推进**——读 `.status.md` 后按衔接决策表直接调度目标阶段 Skill，SHALL NOT 经过 `kflow-resume`、SHALL NOT 执行产物完整性二次校验与五问题摘要；「恢复 {change-name}」/`resume {change-name}` 为**中断恢复**，保留完整 7 步重流程。用户日常推进不再需要输入任何指令
- **归档闸口与人工门控边界**：归档阶段 SHALL NOT 纳入自动衔接的推进目标——审计完成后停止自动衔接并提示用户可显式发起归档，SHALL NOT 自动调度 `kflow-archive`；自动衔接免除的**仅为**「提示用户输入推进指令」一步，原型设计决策门控、原型/详细设计用户评审、审计用户验收门控照常执行
- **`kflow-guide` 职责收缩（BREAKING）**：移除 NEW CHANGE 创建前指引、变更类型分类、变更名称建议三项能力，保留状态查看路由、断点恢复路由、轻量推进路由、流程概览、设计修订分流；PARSE 正则由一条合并分支拆为「恢复/resume + 变更名」→ `kflow-resume` 与「继续 + 变更名」→ 轻量推进两条独立分支
- **`kflow-guide` 触发面收敛**：description 移除「做、添加、实现、搭建」等宽泛新工作意图触发词，保留「修复、Bug、缺陷」及其上下文判断（该判断仍是 guide 职责，且 `kflow-bug-triage` 的 description 未覆盖「修复」这一动词）
- **修正既有的 spec 与实现偏差**：`intent-priority-rules` 早已规定「继续类关键词 → 直接路由到活跃变更的当前阶段」，但实现中该词组被优先级 0 的 RESUME 正则先吃掉。本次拆分后该能力的行为首次与实现对齐，无迁移成本
- **`kflow-resume` 定位调整**：DISPATCH 步骤改为引用共享决策表（不再内联私有副本），triggers 与 description 移除 `继续 {change-name}`
- **注入模板同步**：「变更流程强制规则」section 改写为 7 条——新变更由 `kflow-explore` 承接、阶段自动衔接、恢复入口「恢复 {change-name}」、轻量推进入口「继续 {change-name}」、变更名模式禁止 Plan Mode 拦截、流程阶段列表、查看状态关键词
- **能力变更**：新增 `phase-auto-transition`；`init-claude-md-injection`、`devflow-guide`、`intent-priority-rules`、`resume-plan-mode-bypass` 四份既有能力同步 delta
- **实现层同步**：10 个阶段 Skill 的 COMPLETE 步骤与 `kflow-resume` 的 DISPATCH 步骤接入共享衔接决策；新增 11 份 `references/phase-transition.md`；`kflow-init`、`kflow-guide`、`kflow-status`、`kflow-resume` 的 SKILL.md 及其设计文档同步；核心机制 `04-gates-and-transitions.md` §6.1 新增「阶段自动衔接」并与 §6.7 协调

### v0.25.0 (2026-10-14)
**新增缺陷修复快车道：L4 实现层缺陷脱离变更级阶段门控独立闭环，以定向验证替代全量重跑**
- **新增缺陷修复快车道 `bugfix-fast-lane`**：L4 实现层缺陷（设计正确、仅实现有误）不再走「修复 → 返回测试阶段 → 重跑全量测试与全部阶段门控」的路径，改为**用户反馈 → 分诊 → 修复 → 定向验证 → 快速收口**的轻量闭环；快车道 SHALL NOT 生成或重跑 `functional-designs/`、`detailed-design/`、`api-tests/`、`e2e-tests/`，SHALL NOT 进入变更级 11 阶段门控矩阵；**L1/L2/L3 的 REVISION 路径零改动**
- **定向验证机制**：快车道的验证 SHALL 仅执行**受影响项清单**覆盖的测试用例，SHALL NOT 重跑全量测试套件。受影响项清单（受影响功能点 / 接口 / **测试用例**）由 `kflow-bug-triage` 的影响范围评估产出，SHALL NOT 由修复者自行圈定；修复中发现实际影响面超出清单时判定为**分诊失效**并退回分诊重新评估。未通过时复用既有的「三次修复尝试上限」，SHALL NOT 引入新的轮次模型；「定向验证」与已移除的 `recheck-round` 显式区分命名
- **快速收口机制**：定向验证通过后收口缺陷——更新 `bugs/index.md` 状态、写入收口结论、标记「已解决」；收口前同步校验「受影响项清单 100% 覆盖且全部通过 / 定向验证报告存在 / 状态文件全部必填区已填写且无占位符」三项。命名为「快速收口」而非「快速归档」，与变更级归档元工作流（`/opsx:archive` + 版本自增 + 打包）明确区分；快速收口 SHALL NOT 触发阶段回退、SHALL NOT 阻塞变更级阶段流转
- **新增缺陷级状态文件 `bugfix-status.md`**：每个进入快车道的缺陷在 `bugs/fix/{BUG-ID}/bugfix-status.md` 拥有独立状态文件（基本信息 / 分诊结论 / 受影响项清单 / 修复记录 / 定向验证 / 收口结论六区），**独立于**变更级 `.status.md`——快车道 SHALL NOT 读写其阶段状态矩阵字段；同一变更下多个缺陷各自持有独立状态文件，互不干扰；收口后保留为历史记录
- **`kflow-bug-fix` 新增快车道模式**：在无触发测试阶段上下文时以快车道模式执行修复（入口由 `kflow-bug-triage` 的 L4 结论独占，SHALL NOT 提供其他入口）；复用既有的根因二分法、三次修复尝试上限、Regression Test at Correct Seam 与 Post-mortem 复盘，SHALL NOT 定义第二套修复流程；状态写入缺陷级状态文件，**出口由「返回测试阶段」扩展为「进入定向验证 → 快速收口」**。子变更级与变更级两种既有模式的流程、出口与门控保持不变
- **`kflow-bug-triage` L4 路由分流**：L4 诊断结论由「直接调用 `kflow-bug-fix`」改为「进入缺陷修复快车道」——创建缺陷级状态文件、写入受影响项清单、在问题详情中标记快车道入口、路由输出声明快车道入口；L1/L2/L3 路由输出格式与动作不变
- **审计边界**：审计的**门控校验**不覆盖快车道缺陷（不要求其经过阶段门控，不判定为「跳阶段」）；**覆盖率与产物存在性校验**覆盖快车道状态文件的完整性（存在性 + 必填区完整），缺失或不完整判定为阻塞
- **能力变更**：新增 `bugfix-fast-lane` 能力；`bug-triage-skill`、`bug-fix-writeback`、`change-level-bug-fix` 三份既有能力同步 delta
- **实现层同步**：`kflow-bug-fix` 与 `kflow-bug-triage` 的 SKILL.md 及其 `references/`（`repetition.md` §18、`gates.md` §9、`hooks.md` 快车道钩子分支）同步；核心机制 `03-status-and-tasks.md` §3.5、`04-gates-and-transitions.md` §6.9、`overview.md`、`index.md` 同步；新增 `templates/changes/{change}/bugs/fix/{BUG-ID}/bugfix-status.md` 模板与 `examples/bugfix-status.md` 示例
- **依赖**：本变更依赖 `streamline-design-flow`（v0.24.0）确立的「单轮验证 / 有界验证 + 报告完整 + 计数」口径，快车道 SHALL NOT 使用收敛驱动循环

### v0.24.0 (2026-10-14)
**审查模型由无界收敛循环改为固定单轮：自审签署清单化、审计降级为记账员、档位按影响范围分数统一判定，并新增阶段耗时遥测**
- **自审单轮化（BREAKING）**：设计类与计划阶段（explore / prototype-design / design / plan）自审由多轮重复制改为**固定单轮验证**——主 Agent 写作时按 4 维度**签署清单**逐项自证（零子代理，含「维度 / 自证结论 / 证据锚点」三列，锚点为空或指向不存在内容即签署不成立）→ 1 轮独立子代理验证（**先独立遍历产物形成自身结论、此阶段不读签署清单，再逐项打假；只报告不修改产物**）→ 主 Agent 统一修复并生成「本阶段修复清单」随产物交付下游，**不追加确认轮**。轮数恒为 1、无 0 轮豁免路径；自审报告由「每轮一份」改为固定 `self-reviews/{phase}/report.md`
- **终止结果取值更新（BREAKING）**：`收敛` / `未收敛` 二值废弃，改为 `验证通过` / `验证发现问题({N})`（设计类与计划阶段）、`执行完成` / `定向重验失败`（测试三阶段）、`停滞`（编码 / 代码审查 / 缺陷修复）；历史 `收敛` 按读取侧归并规则读作 `验证通过`
- **原型 VERIFY 三环节合并为单轮单报告**：导航合理性（5 项）、Playwright 全覆盖（5 项）、UX 规则审查与对比度检测合并为**单轮单报告** `self-reviews/prototype/verify-report.md`，强制四分区 + 验证结论分区；对比度检测为静态计算，不启动独立子代理；BUILD 四项静态门控保持不变（主 Agent 直接执行、零子代理）；废弃导航 / Playwright / UX / 对比度各自独立的验证子目录与其轮次报告命名（统一为单份 `verify-report.md`）
- **审计降级为记账员（BREAKING）**：删除原评分制审计（四个维度按 45% / 30% / 15% / 10% 合成总分），改为**四项记账职责**——门控校验 / 覆盖率与产物存在性校验 / 阶段耗时汇总 / 阻塞级问题兜底；审计报告由评分表改为**记账记录形态**；保留阻塞级问题拦截权与归档门控地位；删除按档位分化的简化审计路径（全部档位同一形态）
- **变更档位统一按影响范围分数判定（BREAKING）**：删除「产品需求 → `完整` 档」硬映射，产品需求按功能点数**比照功能需求**的分档规则判定（FP ≤ 2 轻量 / 3 ≤ FP ≤ 10 标准 / FP > 10 `完整`）；档位只决定审查形态与产出深度，**不决定轮数**
- **测试三阶段单轮化**：接口单元测试 / E2E 测试 / 集成测试由多轮循环改为**单轮全面执行 + 定向重验**（仅重跑失败用例，有界重试，连续 3 次失败即终止）；「定向重验」与已移除的 `recheck-round` 语义不同，显式区分命名；编码 / 代码审查 / 缺陷修复的重复制循环**保留不变**
- **新增阶段耗时遥测 `phase-time-telemetry`**：变更级 `.status.md` 新增「阶段耗时与轮次统计」区（阶段 / 开始时间 / 结束时间 / 耗时 / 子代理轮次 / 执行方式）与「阶段内事件计时」区（事件级起止与耗时）；阶段耗时占比 > 40% 或子代理轮次超阈值时自动展开最耗时阶段的内部事件；归档时计时摘要回流 `docs/skill-suggestion.md`，回流失败不阻塞归档
- **能力变更**：新增 `signed-checklist-verification`、`phase-time-telemetry`、`prototype-single-round-verify` 三能力；`convergence-driven-repetition`（终止模型改为单轮）、`devflow-audit`、`change-tier-classification`、`agent-iteration-execution`、`subagent-self-review`、`plan-self-review`、`flexible-repetition-mode`、`round-counter`、`inter-round-summary`、`prototype-navigation-verification`、`prototype-playwright-5round-verification`、`prototype-review-artifacts`、`phase-self-review` 共 13 份既有能力同步 delta
- **实现层同步**：`docs/designs/skills/` 下 explore / design / prototype-design / plan / api-test / e2e-test / integration-test / audit 八份设计规格同步；核心机制 `03-status-and-tasks.md` §3.1.1、`07-agent-model.md` §15/§16、`overview.md`、`index.md` 同步；`examples/change-status.md` 与 `examples/audit-report.md` 对齐新模板

### v0.23.0 (2026-10-14)
**终止模型翻转：收敛成为唯一成功终止条件，删除档位轮次上限与复检轮，并以审查范围冻结使收敛可达**
- **删除档位轮次上限（BREAKING）**：执行类 1/3/5、设计自审 1/2/5 全部移除，轮数由收敛实际发生在第几轮决定；档位语义收敛为「每轮审查强度（单 Agent / 两视角 / 四视角）与产出深度」，SHALL NOT 决定轮数
- **删除回退叠加上限（BREAKING）**：`max(档位上限, 影响范围分数映射)`、统一分数→轮次映射表与 `Recommended Rounds` 字段移除；影响范围分数本身保留（供验证门控的受影响项清单与回退判定）
- **收敛成为唯一成功终止条件**：见证轮四项判据——(a) 零新发现、(b) 零修复/零修改、(c) 报告证明全维全量遍历、(d) 累积未复核修复清单内全部条目逐项复核通过
- **复检轮上提为见证轮第 (d) 项（BREAKING）**：`recheck-round` 能力退役，复核义务并入收敛判据，配套的 `份数 = 档位上限 + 1` 判读链与审计例外条款一并删除
- **新增不收敛判定与升级**：无进展（连续 2 轮「新发现数」与「清单长度」双双无改善）/ 振荡（同一问题项「修复→重新发现」≥ 2 次）/ 保险丝（全局 10 轮，与档位脱钩、不参与门控判读），命中即终止并升级用户
- **新增审查范围冻结**：审查对象集合冻结 + 审查维度集合封闭，适用于 SELFREV、执行类重复制与 prototype 三验证；范围外发现降级为「范围外观察」（不改产物、不计入发现数、不阻断收敛），引入范围外新内容的轮次 SHALL NOT 判为见证轮
- **字段与判读简化**：`执行轮次` 由 `{N} / {上限}` 改为 `{N} 轮`；`gates.md` 份数判定四条规则塌为「份数 ≥ 1」；终止结果由三值改二值（`收敛` / `未收敛`，具体缘由写入 `skill-suggestion.md`）
- **能力变更**：新增 `convergence-driven-repetition`（11 条需求，终止模型的唯一权威定义），`tier-driven-repetition` 与 `recheck-round` 两能力退役（变更声明 `retire_capabilities: true`），另有 21 份既有能力同步 delta
- **保留不动**：单用例 3 次修复上限（`defect-strike-limit`）、轮次级子代理重试 3 次上限、全局轮次下限 1 轮
- **实现层同步**：8 份 `references/repetition.md`、10 份 `references/gates.md`、3 份 `references/self-review.md`、`self-review-dimensions.md` 与 14 份 `SKILL.md` 同步；README 档位行为差异表、执行类重复制说明与复检轮 FAQ 同步

### v0.22.0 (2026-10-12)
**新增终止前复检轮，使任何被记入审查报告的修复都经过独立验证；终止原因扩为三值**
- **新增「复检轮」机制**：多轮审查（设计自审 SELFREV、prototype VERIFY、执行类重复制）到达终止点时，主 Agent 先判定**累积未复核修复清单**是否为空——非空即追加 1 轮复检轮，逐项复核自审循环开始以来全部尚未通过独立复核的修复。此前的缺口是：复核义务被绑定在「本轮零新发现且零修改」上，而上限那一轮恰恰因为有修改才成为上限轮，触发条件与待复核修复永远错开
- **复检轮不消耗档位轮次预算**：追加在档位轮次上限之外，单个阶段最多 1 轮；`执行轮次` 字段保持 `{N} / {上限}` 不变。轻量档（上限 1）第 1 轮含修复时实际执行 2 轮，修掉了「轻量档正常发现并修复了 1 个问题却被记为非收敛异常」的语义倒挂
- **通过判据复用见证轮定义**：构成见证轮（零新发现 + 零修改 + 全量遍历证明 + 清单内全部修复逐项复核通过）即为通过，不发明第二套判据；未通过则终止原因 `达上限` 并进入非收敛分支。有界，不会无限续杯
- **终止原因由二值扩为三值（兼容性）**：`收敛` / `收敛（复检轮）` / `达上限`。判读链——`收敛（复检轮）` + 报告份数 = 档位上限 + 1 表示复检轮已执行且通过；`达上限` + 份数 = 档位上限 + 1 表示已执行但未通过。`执行轮次` 字段格式不变，历史 `.status.md` 读取路径不受影响；全部读取点（8 份 `references/repetition.md`、10 份 `references/gates.md`、`kflow-audit`、`kflow-resume`）同步更新
- **前轮修复清单改为累积维护**：轮间摘要新增「累积未复核修复清单」字段（由主 Agent 维护），消费方由「见证轮候选」扩展到「终止判定 + 复检轮」
- **门控与审计同步**：自审报告份数上限允许 `档位上限 + 1` 当且仅当终止原因含复检轮语义（含防滥用条款：多出的 1 份必须能由终止原因解释）；审计 SHALL NOT 因 `收敛（复检轮）` 或份数 = 上限 + 1 判轮次不足、超额或缺项
- **修正三份 `references/self-review.md` 的悬空引用**：`kflow-explore` / `kflow-design` / `kflow-prototype-design` 的 `self-review.md` 引用了其目录下不存在的 `references/repetition.md` §13，现将轮间摘要格式与注入规则内联为各文件 §11，并删除悬空引用
- **新增能力**：`recheck-round`（复检轮的权威定义），10 个既有能力同步 delta（`tier-driven-repetition`、`subagent-self-review`、`agent-iteration-execution`、`plan-self-review`、`inter-round-summary`、`round-counter`、`execution-repetition-mode`、`flexible-repetition-mode`、`prototype-navigation-verification`、`prototype-playwright-5round-verification`）

### v0.21.0 (2026-10-10)
**项目类型确认前移到 init、变更创建链路改为继承项目级记录、新增漂移检测与用户显式覆盖逃生舱**
- **确认动作前移到 init（BREAKING）**：`kflow-init` 在 DETECT 之后新增 CONFIRM 步骤，使用 AskUserQuestion 确认一次项目类型并写入项目级记录；re-init 时记录已存在且重扫结果一致则**静默复用**，仅扫描与记录冲突时才询问。原先「每次创建变更都重扫项目根目录 + 让用户重复回答同一个问题」的行为被消除——项目类型是仓库级不变量，却被当成变更级变量反复重算
- **变更创建链路改为三级回落读取（BREAKING）**：`kflow-explore` 的 TYPEDET/CONFIRM 两步由「重扫 + 询问」改写为读取回落链（CLAUDE.md「项目画像」项目类型行 → `docs/toolchain.md` 头部字段 → 就地检测）＋**静默一致性校验**；一致则静默继承并输出「项目类型: X（继承项目级记录）」，冲突才 AskUserQuestion 复核。`kflow-guide` 的 NEW CHANGE 创建前指引同样由「重新扫描判定」改为「读取项目级记录」，SHALL NOT 在指引阶段重新扫描判定
- **未 init 项目降级自愈**：项目级记录完全缺失时，变更创建链路检测并确认**一次**，补写 `docs/toolchain.md` 头部（不写 CLAUDE.md「项目画像」——该区块为 init 整体扫描产物，残缺写入会与受管 marker 替换逻辑冲突），此后该项目的所有变更均静默继承
- **新增漂移检测**：变更创建时对项目类型执行一次静默一致性校验，扫描前端工程标识并与项目级记录比对；一致时不打扰用户，冲突时用 AskUserQuestion 展示冲突项并请求裁决、可选更新记录；校验因项目根目录不可读等原因无法完成时沿用记录值继续，**不阻塞**变更创建
- **新增用户显式覆盖逃生舱**：用户在需求描述中显式声明项目类型（或指出既有记录有误）时，该声明优先于项目级记录与扫描结果并触发记录更新——为初始误判（扫描信号与错误记录一致，一致性校验无法发现）提供纠正通道，且不要求用户重新执行 init
- **变更级快照保留、来源改为继承**：`.status.md` 与 `functional-designs/index.md` 的项目类型字段继续保留并在变更生命周期内冻结（否则已 `⏭️ 跳过` 的阶段会中途复活），取值来自项目级记录而非重新检测；消费侧（`kflow-design`、`kflow-prototype-design`、`kflow-api-test`、`kflow-e2e-test`、`kflow-verify`、`kflow-audit`、`kflow-archive`）只读快照的判定逻辑与读取路径不变
- **同步范围**：3 个能力（`project-type-detection`、`devflow-guide`、`init-claude-md-injection`）的 delta 已合并到主 specs；实现侧同步 `skills/kflow-init/SKILL.md`、`skills/kflow-explore/SKILL.md`、`skills/kflow-guide/SKILL.md` 与 `docs/designs/core-mechanisms/01-project-types.md` 等设计文档及变更模板

### v0.20.1 (2026-10-10)
**注入模板作用域修正、marker 版本判据内化、注入规则规格去重**
- **注入模板去除开发态内容**：`kflow-init` 注入消费方 CLAUDE.md 的「变更流程强制规则」section 移除归档后 git commit、版本自增、`scripts/` 打包等**技能开发仓库特有**规则（消费方不存在 `VERSION`、`scripts/`、`targets/`，原规则无法执行），section 收敛为 6 条跨 skill 路由约束 / 用户接口约定 / 流程概览。同类项的 skill 内部执行步骤（归档后 git commit 询问、非 git 仓库时的 git init 询问）归还各 SKILL.md 承载，不再在消费方 CLAUDE.md 中双重定义
- **marker 版本判据内化（BREAKING）**：marker 区块的模板版本标识由「参见消费方仓库根 `VERSION` 文件」改为 `kflow-init` 自身 `SKILL.md` front matter 的 `version` 字段——原判据在消费方悬空，导致模板修正后 `re-init` 仍可能判定为无变化。版本判据缺失或无法解析时一律判定为版本不同并全量替换，使存量消费方 CLAUDE.md 中的错误规则能在下次 `kflow-init` 时被清除
- **项目自定义规则区块受保护**：新增不受框架管理的 `## 项目自定义规则` marker 区块；`re-init` 只替换自己管理的 marker 区块，不覆盖项目自行维护的内容，用户在框架管理区块之外新增的内容不被删除
- **注入规则规格去重**：`devflow-init` 与 `init-claude-md-injection` 重复定义的「变更流程强制规则 section 扩展」Requirement 收敛至 `init-claude-md-injection`，后者成为 CLAUDE.md marker 注入规则（内容要求、版本判据、替换策略）的唯一权威定义位置；`devflow-init` 保留工具推荐矩阵与 GAP 检测要求
- **新增注入模板作用域守卫**：新增 `injection-scope-guard` 能力与 `scripts/validate-injection-scope.sh` 校验入口，扫描 kflow-init 的注入模板是否含 `scripts/sync-version.sh`、`scripts/package-skills.sh`、`targets/`、`VERSION` 文件、README 版本条目等开发态词汇，命中时输出词汇与所在行并非零退出，未匹配到校验对象时同样判定失败
- **同步范围**：3 个能力（`devflow-init`、`init-claude-md-injection`、新增 `injection-scope-guard`）的 delta 已合并到主 specs；实现侧同步 `skills/kflow-init/SKILL.md` 与 `docs/designs/skills/kflow-init.md`、`docs/designs/core-mechanisms/08-governance.md` 设计文档

### v0.20.0 (2026-10-09)
**审计执行者统一为单一子代理、维度模型七→四重构、总分门控地位明确**
- **审计执行者统一为单一子代理（BREAKING）**：审计（含轻量档）改由**一个子代理**执行，替换非轻量档的 4 个并行子代理与轻量档的主 Agent 轻量自检——原先轻量档下主 Agent 既执行审计又判定审计、缺少独立视角的问题被消除。新增**证据先于评分**约束：子代理 SHALL 先完成全部维度的事实采集并逐维度呈现判定证据，再统一评分，用以替代原先 4 个子代理互相看不到对方结论的天然隔离，抑制光环效应。子代理异常时禁止主 Agent 接管（最多重试 3 次，与执行类阶段一致）
- **维度模型由七维度合并为四维度（BREAKING）**：合并依据是原切分点落在证据源与判定性质的**内部**而非之间——「流程合规性」与「产物完整性」读同一份 `.status.md` 与同一棵目录树；「审查质量」与「缺陷管理」查同一条「问题 → 修复 → 闭环」链；「效率指标」与「Post-mortem 汇总」从不产出阻塞/严重级问题，而审计判定完全由问题分级决定，故其门控价值为零。新权重直接相加以保留总分历史可比性：流程与产物合规性 **45%**（原 22%+23%）、审查与缺陷闭环 **30%**（原 20%+10%）、测试充分性 **15%**（保留）、效率与改进 **10%**（原 5%+5%）
- **加权总分定位明确**：0-100 总分继续只作变更健康度参考，**不参与门控判定**；判定链路（阻塞 / 严重 / 建议分级 → 阻断或记录）不变
- **轻量档产物形态不变**：仍为 3 项检查项的简化审计记录、不计算评分、不输出评分表；仅执行者由主 Agent 改为子代理。同时消除「非轻量档由子代理执行、轻量档由主 Agent 执行」这一双执行者模型
- **子代理隔离规则适用范围补入审计**：`subagent-isolation-rule` 的适用阶段清单新增 `kflow-audit`（审计评估/轻量自检），并新增「审计阶段的规则适用子集」场景——审计适用隔离规则与 3 次重试上限，但**不适用**轮次级重试粒度（审计为单次执行，无轮次概念）与主 Agent 职责边界硬线（审计非执行类阶段）
- **既存不一致修正**：`devflow-audit` 的 Purpose 写「六维度评估」而需求为七维度、实现为四维度候选，一并改为与新结构一致
- **同步范围**：2 个能力（`devflow-audit`、`subagent-isolation-rule`）的 delta 已合并到主 specs；实现侧同步 `skills/kflow-audit/SKILL.md`、`skills/kflow-archive/SKILL.md`、`skills/kflow-guide/SKILL.md` 与 `docs/designs/` 设计文档及审计报告模板

### v0.19.0 (2026-10-09)
**多轮审查机制由预算制反转为收敛制、explore 澄清收敛门、轮间摘要扩展到设计自审、原型验证轮次去重**
- **轮次模型反转为收敛制（BREAKING）**：档位语义由「必须完成的目标轮次」翻转为**收敛驱动**，全局下限统一为 1 轮（无例外），`完整` 档上限由 10 降至 5（轻量 1 / 标准 2 设计·3 执行 / `完整` 5）。终止判据改为**见证轮**——同时满足「零新发现 + 零修改 + 报告证明全维度全量遍历 + 累积未复核修复清单内全部条目逐项复核通过」的一轮；未收敛则进入**非收敛分支**（记录 `skill-suggestion.md` + AskUserQuestion + 可标记 ⚠️ 阻塞）。`.status.md` 执行轮次字段由 `{N} / 10` 改为 `{N} 轮`，并新增**终止结果**字段（`收敛` / `未收敛`）供审计判读终止路径
- **`完整` 档评分底线由装饰变为有效**：`>8 且收敛` 即止，`≤8` 续审至上限 5——原规则「第 3 轮 >8 仍须做满 10 轮、第 10 轮 ≤8 已无处补审」的两头够不着被消除
- **轮间摘要注入扩展到设计自审**：原仅执行类阶段具备的轮间摘要（`repetition.md` §13）解除被分层加载规则排除在设计类之外的限制，覆盖 explore / design / prototype-design / plan 的 SELFREV。移除「完成全部目标轮次」的冗余复扫后，「零发现」的可信度改由轮间因果保障，而非重复扫描次数——故本轮次模型的移除与摘要扩展在设计上不可分割，同变更落地
- **轻量档不再豁免设计自审（BREAKING）**：设计自审由 0 轮改为 1 轮，补上原本完全缺失的语义审查；产物完整性门控保留为**附加硬门**
- **回退重执行叠加反向**：由 `目标轮次 = max(档位基线, 映射)` 改为 `上限 = max(档位基线, 映射)`，影响范围映射 `>15` 由 10 改为 5，保留「返工验证不因低档而放松」原意
- **原型验证轮次去重**：`html-prototype-workflow` 的「Playwright 5 轮全覆盖验证」与「导航合理性验证」两条与专门能力重复的 requirement 移除，改为一条「原型验证轮次的统一引用」，轮次规则收敛为单一来源；`prototype-navigation-verification` 与 `prototype-playwright-5round-verification` 由「5 轮强制执行」改为 `[1,5]` 收敛驱动
- **既有规格漂移修正**：`round-counter` 的 `{N} / 10` 硬编码与「轮次不足 10/10 视为验收不通过」判据、`agent-iteration-execution` 与 `plan-self-review` 的 Purpose 段「强制 10 轮」、`triage-impact-assessment` 的 `Score > 15: 10 rounds` 与 `max(tier baseline, …)` 一并修正为收敛驱动口径
- **explore 澄清收敛门（BREAKING）**：新增 `requirement-clarification` 能力——进入 SPLIT 前**未决问题清单 SHALL 为 ∅**（每项须被消解，或显式降级为 `待补充` 并记录理由）；消歧路径限定为澄清提问 / `CONTEXT.md` 术语精确化 / 事实查库，**SHALL NOT 以扩增功能设计内容（功能点、字段、章节、分支）的方式消除歧义**；可查证事实项自动解析，仅决策项提交用户且一次只提交一项。SPLIT 门槛由「流程顺序走完」变为「清单为空或已显式降级」
- **CONTEXT.md 格式权威内部化**：`domain-glossary` 的「CONTEXT.md 格式」requirement 由引用外部技能 `grill-with-docs` 的格式文件改为引用 KFlow 自有 `skills/kflow-explore/references/context-template.md`，消除安装布局下不可解析的外部依赖（ADR 一侧另立变更处理）
- **同步范围**：13 个能力（`convergence-driven-repetition`、`agent-iteration-execution`、`round-counter`、`subagent-self-review`、`plan-self-review`、`flexible-repetition-mode`、`execution-repetition-mode`、`inter-round-summary`、`auto-subchange-traversal`、`defect-strike-limit`、`html-prototype-workflow`、`prototype-navigation-verification`、`prototype-playwright-5round-verification`）的 delta 已合并到主 specs；实现侧同步 18 个 `SKILL.md`、8 份 `references/repetition.md`、3 份 `self-review.md`、10 份 `references/gates.md` 及 `docs/designs/` 设计文档。`requirement-clarification` 新增能力与 `domain-glossary` 格式权威变更同步落地于 `kflow-explore` SKILL.md 与新增的 `references/clarify-convergence.md`

### v0.18.0 (2026-09-30)
**变更档位一等机制、轻量档阶段裁剪、原型阶段直写产品级重设计、旧规格原型口径统一、版本管理规则收敛**
- **变更档位（轻量 / 标准 / 完整）**：新增贯穿全流程的单一分级依据，由影响范围分数（`FP数×1 + 接口数×1.5 + 数据模型×2`）派生（≤3 轻量 / 4~15 标准 / >15 完整，变更类型为产品需求时下限抬升为完整），作为必填字段写入变更级 `.status.md`；两段式判定——explore 的 SPLIT 后按「变更类型 + 功能点数」初判（用户可上下调），design 的 DIVIDE 后按完整公式复核（**仅允许单向升档**）；历史变更缺该字段时按最高档回退
- **废除两个「首次一律最大」保守下限（BREAKING）**：执行类阶段目标轮次改由档位决定（轻量 1 / 标准 3 / 完整 10），设计自审改由档位决定（轻量 0 完全跳过 / 标准 2 / 完整 10 并保留各维度评分 > 8 底线）；回退重执行改为在档位基线上取 `max(档位基线, 影响范围分数映射)`，三处轮次映射表统一为一份档位表
- **审查分级改由档位驱动（BREAKING）**：设计审查轻量档单 Agent 综合、标准档降为两视角并行（业务+技术 / 安全+质量）、`完整` 档保留四视角并行；代码审查轻量档单 Agent 单轮且不执行分级重审闭环；检查项不得随档位缩减
- **轻量档阶段裁剪**：kflow-design 在 DIVIDE 后按客观产物信号（接口条目 / UI 变更 / 跨子变更契约）逐阶段判定并写入「阶段适用性声明」；`接口单元测试`、`E2E测试`、`集成测试` 可裁剪为 `⏭️ 不适用`，判定依据不可读时保守回退为适用。下游按「声明 × 产物」四态判定，**无声明依据的 `⏭️` 一律阻塞**；被裁剪列从覆盖率分母移除；轻量档恒为单一子变更（跳过子变更划分），审计由单一子代理执行（轻量档为轻量自检）并保留归档门控地位
- **原型阶段重设计（BREAKING）**：`TOOLCHAIN` 默认复用 `docs/toolchain.md` 已锁定工具链（仅在无锁定 / Skill 已失效 / 用户要求更换时重新选择）；新增 BUILD 四项静态门控（CDN 扫描 / 交叉引用 / 必检产物 / 清单一致，零子代理）；审查方式改为用户二选一——人工审查（跳过全部自动验证）或子代理自动审查验证（5 轮导航 + 5 轮 Playwright + UX 审查 + SELFREV），`VERIFY` 与 `SELFREV` 由无条件强制改为按选择执行
- **原型产物直写产品级（BREAKING）**：废弃变更级原型副本目录，改为直写 `docs/designs/prototypes/`，变更级只保留 `prototype-changes.md`（改动清单 + 改动前哈希）/ `prototype-backup/` / `prototype-plan/` / `element-coverage-tree.md` / `self-reviews/prototype/`；新增并发写入检测（哈希比对不一致时交用户裁决）；归档由「合并原型到产品级」改为「登记改动到 `docs/designs/prototypes/manifest.md`」
- **旧规格原型口径统一**：原型直写产品级的新模型由 `redesign-prototype-stage` 定稿并落地到实现后，主规格侧仍有 20 个 capability 描述旧的「变更级 `prototype/` 副本」模型与已移除的 Pencil 产物（`prototype.pen`、`prototype/index.md`、`prototype/design-tokens.css`、`prototype/design-prompt.md` 等），形成**规格落后于实现**——下游阶段（plan / code / code-review / e2e-test / integration-test / resume / verify / triage）的门控与输入限定会按旧模型判定，属于会实际误报的缺陷。本次统一这 20 个 capability 的口径（37 个 MODIFIED 需求块 + 2 个 RENAMED 需求标题）：原型入口由多处分散引用收敛为「产品级 `docs/designs/prototypes/manifest.md` + 变更级 `prototype-changes.md`」两项；角色集合由 `entry/page/tokens/coverage/shared` 收敛为 `entry/page/tokens/shared`（`coverage` 元素覆盖树归变更级）；`design-change-record` 的记录载体由「三个变更级 `index.md`」改为「两个变更级 + 产品级 `manifest.md`」；并收口内嵌旧路径的 6 处 scenario 标题与 4 处 `## Purpose`。不改变任何运行时行为，已归档变更的变更级 `prototype/` 目录原地保留
- **kflow-shared 规格残留清理**：移除 6 个纯集中式规格（其中 2 个与现行规格直接矛盾），修正 12 个规格中已不存在的 `kflow-shared/` 路径引用与错误前提，并为修正后的需求追加「不依赖集中式目录」回归场景；同步修正 9 个 SKILL.md 与 `07-agent-model.md` 的分层加载措辞、README 目录结构速查与失效链接
- **front matter 合法性缺陷修复**：`kflow-archive`/`kflow-audit`/`kflow-bug-triage` 三个 SKILL.md 的 `description` 是未加引号的 YAML plain scalar，其中 `RELOAD: ` 的 ASCII 冒号使整个 front matter 解析失败；`npx skills add` 对解析失败的 Skill 静默丢弃，导致 18 个 Skill 只识别出 15 个且不报错。改用全角冒号后恢复 18 个，并同步修正 4 个设计规格的 `yaml` 代码块与 SKILL 模板（模板是该写法的传播源头）
- **front matter 校验与打包门控**：新增 `scripts/validate-frontmatter.py`，校验 YAML 可解析、`name`/`description` 必填、`name` 与所在目录名一致、`version` 与 `VERSION` 一致、`description` 含中文触发词，并覆盖 `.claude/skills/*` 与设计规格的 `yaml` 代码块；`package-skills.sh` 接入阻断式门控，校验未通过即在产包前中止，使该缺陷不再漏到发布
- **打包扫描根修正**：`package-skills.sh` 的扫描根由 `.claude/skills` 修正为仓库内实现目录 `skills/`——此前打包循环匹配零个 Skill，静默产出仅含 `VERSION.txt` 的空包，且版本一致性校验因遍历空集合而空转通过（把失败报告为成功）；同时新增空集合断言与版本校验计数守卫，杜绝此类静默通过
- **`kflow-skills-auditor` 残留清理**：该 Skill 已不存在，移除 `skill-packaging` 规格与其变更增量、以及 `package-skills.sh` 中针对它的排除规则（规则指向不存在的对象，且在 `skills/` 扫描根下恒为空操作、无从验证）；已归档变更中的历史记录不改写
- **版本管理规则收敛为单一能力（BREAKING）**：版本管理此前被拆成 `unified-version`、`version-tracking`、`version-field-removal-rule` 三份规格各自演进，对「SKILL.md 是否应含 `version:` 字段」给出**相反**要求（两份要求「有」、两份要求「无」，且 `unified-version` 自身的两条需求亦互相冲突），而 `version-field-removal-rule` 的执法者 `kflow-skills-auditor` 并不在本仓库，该规格既与现行机制相反也无实现可验证。现整体收敛：`version-tracking` 全部需求并入 `unified-version`，`version-field-removal-rule` 整体移除，两个能力退役（变更声明 `retire_capabilities: true`）；`unified-version` 明确三层载体——仓库级 `VERSION` 文件为唯一事实来源、Skill 级 SKILL.md `version` 字段承载同步副本、文档级统一标注「版本: 参见仓库根目录 `VERSION` 文件」，并新增「版本管理规则唯一性」条款：版本字段的存在性、版本值来源与自增级别此后仅由该能力定义
- **归档后版本流程获得规格载体**：此前该顺序无规格可依——CLAUDE.md 声明「由 CLAUDE.md 的归档后规则自动驱动」，但该章节并不存在。现补齐 CLAUDE.md「归档后规则」章节，固定六步顺序（判定自增级别 → 更新 `VERSION` → 运行 `scripts/sync-version.sh` 同步全部 SKILL.md → 更新 README 版本行与条目 → 运行 `scripts/package-skills.sh` 打包 → git commit），并明确 zip 产物受 `.gitignore` 的 `targets/` 规则排除、只提交版本变更文件，任一步骤失败不阻塞归档本身；该章节改为版本无关表述，版本递增不再需要人工编辑它
- 新增 5 个 specs（change-tier-classification、convergence-driven-repetition、lightweight-flow-trimming、prototype-build-gate、prototype-change-tracking）+ 修改 105 个 specs + 移除 8 个 specs（6 个 `shared-*` 集中式规格 + `version-tracking` + `version-field-removal-rule`）
- 同步更新 18 个运行时 SKILL.md、29 个设计文档、21 个模板文件（含产品级原型模板目录、`prototype-plan/` 与 `prototype-changes.md` 新模板）与 README.md

### v0.17.0 (2026-09-28)
**设计自审分级、详细设计术语统一、设计评审分级与归档位置调整**
- **设计自审分级（首次/非首次）**：三设计阶段（explore/prototype/design）SELFREV 从无条件固定 10 轮改为按「首次/非首次创建」分级——首次创建固定 10 轮，非首次创建按影响范围分数弹性决定轮次（下限 1、上限 10）+ 评分底线（各维度评分均 > 8 方通过，未达标补审至 10 轮上限）；判定信号复用 kflow-init 检测（CONTEXT.md 存在 + detailed-designs/ 非空）
- **详细设计术语统一**：产品级目录 `technical-designs/` → `detailed-designs/`（6 文件体系），中文术语「技术设计」归一为「详细设计」；模板目录同步重命名；旧目录兼容读取 + 迁移提示（不自动 git mv）
- **设计评审分级**：kflow-design REVIEW 按变更类型分级——功能缺陷级走简化模式（单 Agent 串行综合审查，单一 synthesis.md，不执行分级重审闭环），功能需求级/产品需求级走四视角并行模式（+ 分级重审闭环）
- **归档位置统一**：归档目录 `docs/archive/` → `docs/changes/archive/`，消除 status/resume 检测路径的文档-实现错位
- 新增 2 个 specs（design-review-tiering、archive-directory-location）+ 修改 7 个 specs（archive-design-merge、doc-naming-convention、init-legacy-reverse-analysis、product-config-items-doc、product-error-handling-doc、stage-doc-templates、subagent-self-review）
- 同步更新 11 个运行时 SKILL.md、设计文档、核心机制文档、模板文件与 README.md

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
- 三阶段 SELFREV 统一改为子代理串行执行（重复制，后续改为首次/非首次分级）
- 五大增强（Plan Mode 绕过、子代理隔离、复杂度评估、kflow-plan SELFREV）
- 7 个执行类阶段统一为重复制模式
- 六项执行规则细化（服务启动绑定、E2E 测试可选收集、原型设计决策门控、原型到代码一致性）
- 五项执行可靠性增强（双层遍历、原型修订模式、skill-suggestion 自动捕获、用户验收门控、中断恢复验证）
- 原型设计工具链灵活性增强（动态扫描环境 Skills、多方案推荐、STYLE+GENERATE 拆分）
- 文档整理与一致性修复（core-mechanisms.md 拆分为 8 文件、锚点引用批量更新）
- 新增项目画像注入、老项目逆向分析、Git 版本管理章节
