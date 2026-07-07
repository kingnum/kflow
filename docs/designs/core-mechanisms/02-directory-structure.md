# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-05-17

> **加载层级**: 基础层
> **适用阶段**: 全部

本文档定义 KFlow Skills 体系的核心运行机制，包括目录结构、状态文件、任务清单、阶段流转规则、回退机制和条件产物引用规范。

---


## 二、目录结构规范

### 2.1 变更管理目录

```
docs/
├── changes/                           # 变更管理目录
│   ├── index.md                       # 变更管理索引（活跃变更列表 + 已归档变更列表）
│   ├── {change-name}/                 # 单个变更目录（kebab-case命名）
│   │   ├── .status.md                 # 变更总状态文件（含子变更进度矩阵）
│   │   ├── tasks.md                   # 变更总任务清单（子变更级checkbox）
│   │   ├── functional-designs/        # 功能设计阶段输出（目录化结构）
│   │   │   ├── index.md               #   功能设计索引入口（全部功能点清单、依赖关系图）
│   │   │   └── part-NN.md             #   功能设计分册文件（每个分册 ≤30 个功能点）
│   │   ├── prototype/                 # 原型设计阶段输出（可选，变更级，HTML 格式）
│   │   │   └── index.html              #   HTML 交互原型入口文件
│   │   ├── detailed-design.md         # 统一详细设计（变更级，合并原 architecture.md + 所有子变更设计）
│   │   ├── api-tests/                 # 统一接口测试用例（目录化结构）
│   │   │   ├── index.md               #   接口测试索引入口
│   │   │   └── part-NN.md             #   接口测试分册文件（每个分册 ≤30 个接口）
│   │   ├── e2e-tests/                 # 统一E2E测试用例（目录化结构，仅前后端项目）
│   │   │   ├── index.md               #   E2E测试索引入口
│   │   │   └── part-NN.md             #   E2E测试分册文件（每个分册 ≤30 个场景）
│   │   ├── integration-tests/         # 统一集成测试用例（目录化结构）
│   │   │   ├── index.md               #   集成测试索引入口
│   │   │   └── part-NN.md             #   集成测试分册文件（每个分册 ≤30 个场景）
│   │   ├── traceability.md            # 覆盖追溯矩阵（独立文件，记录FP×阶段产物覆盖映射）
│   │   │
│   │   ├── bugs/                      # 问题登记目录（kflow-bug-triage 首次登记时创建）
│   │   │   ├── index.md               #   问题索引（统计+问题列表+分页表）
│   │   │   └── bug-NNN-NNN.md         #   分页详情文件（每文件 ≤20 条 BUG）
│   │   │
│   │   ├── subchanges/                # 子变更目录
│   │   │   ├── {subchange-1}/         # 子变更1（如：user-auth，功能点≤10）
│   │   │   │   ├── .status.md         # 子变更状态文件
│   │   │   │   ├── tasks.md           # 子变更任务清单（功能点级全展开，含DoD验收标准）
│   │   │   │   └── test-reports/      # 子变更测试报告目录
│   │   │   │       ├── api/           # 接口单元测试报告
│   │   │   │       │   ├── round-1.md
│   │   │   │       │   └── summary.md
│   │   │   │       ├── e2e/           # E2E测试报告（仅前后端项目）
│   │   │   │       │   ├── round-1.md
│   │   │   │       │   └── summary.md
│   │   │   │       ├── review/        # 代码审查报告
│   │   │   │       │   └── code-review.md
│   │   │   │       └── fix-reports/   # 缺陷修复报告目录
│   │   │   │           └── fix-{timestamp}.md
│   │   │   │
│   │   │   ├── {subchange-2}/         # 子变更2（如：order-management）
│   │   │   │   └── ...                # 结构同子变更1
│   │   │   │
│   │   │   └── {subchange-3}/         # 子变更3（如：payment-integration）
│   │   │       └── ...
│   │   │
│   │   ├── self-reviews/               # 自循环审查记录目录
│   │   │   ├── explore/                # explore 阶段自审记录
│   │   │   │   └── {YYYYMMDD}-{HHMMSS}.md  # 自审轮次报告（时间戳命名）
│   │   │   ├── prototype/              # prototype 阶段自审与验证记录
│   │   │   │   ├── {YYYYMMDD}-{HHMMSS}.md  # 自审轮次报告（时间戳命名）
│   │   │   │   ├── nav-check/           # 导航合理性验证报告（5 轮）
│   │   │   │   │   └── round-{1..5}.md
│   │   │   │   ├── playwright-check/    # Playwright 全覆盖验证报告（5 轮）
│   │   │   │   │   └── round-{1..5}.md
│   │   │   │   └── cdn-crossref-check/  # CDN 扫描 + 交叉引用检查合并报告
│   │   │   │       └── report.md
│   │   │   └── design/                 # design 阶段自审记录
│   │   │       └── {YYYYMMDD}-{HHMMSS}.md
│   │   │
│   │   ├── cross-reviews/              # 四视角交叉审查报告目录
│   │   │   └── {YYYYMMDD}-{HHMMSS}/    # 审查批次目录（时间戳命名）
│   │   │       ├── business-review.md  # 业务视角审查报告
│   │   │       ├── technical-review.md # 技术视角审查报告
│   │   │       ├── security-review.md  # 安全视角审查报告
│   │   │       ├── quality-review.md   # 质量视角审查报告
│   │   │       └── synthesis.md        # 审查综合报告（含问题追踪矩阵）
│   │   │
│   │   ├── migrations/                # 数据库迁移（变更级）
│   │   │   ├── 001_{subchange}_{描述}.sql  # 迁移脚本
│   │   │   ├── 001_{subchange}_{描述}_rollback.sql  # 回滚脚本
│   │   │   └── migration-log.md       # 迁移执行记录
│   │   │
│   │   ├── test-reports/              # 变更级测试报告
│   │   │   └── integration/           # 集成测试报告
│   │   │       ├── round-1.md
│   │   │       ├── summary.md
│   │   │       └── fix-reports/       # 集成测试缺陷修复报告
│   │   │           └── fix-{timestamp}.md
│   │   │
│   │   ├── checkpoints/               # 变更级 checkpoint
│   │   │   ├── {YYYYMMDD-HHMMSS}-checkpoint.md
│   │   │   └── {YYYYMMDD-HHMMSS}-checkpoint-auto.md
│   │   │
│   │   └── subchanges/
│   │       └── {subchange}/checkpoints/  # 子变更级 checkpoint
│   │           ├── {YYYYMMDD-HHMMSS}-checkpoint.md
│   │           └── {YYYYMMDD-HHMMSS}-checkpoint-auto.md
│   │
│   └── archive/                       # 归档目录
│       └── {YYYY-MM-DD}-{change}/     # 归档的变更（整体归档，保持原结构）
│           ├── .status.md
│           ├── tasks.md
│           ├── subchanges/
│           └── ...
│
├── designs/                           # 产品级设计文档
│   ├── index.md                       # 产品级设计索引入口
│   ├── functional-designs/            # 按功能模块拆分的产品级功能设计文档
│   │   ├── index.md                   #   功能模块导航索引
│   │   ├── {一级菜单}/                 #   前后端项目：按菜单目录化（章节与变更级一致）
│   │   │   ├── index.md               #     菜单级索引（功能点清单、分册总览、修订记录）
│   │   │   └── part-NN.md             #     功能设计分册（与变更级 part-NN.md 同结构，额外增加来源标注）
│   │   ├── {domain}.md                #   纯后端项目：按设计域平铺（backend-domain.md 简化模板）
│   │   └── ...
│   ├── technical-designs/             # 产品级技术设计文档（6 文件体系）
│   │   ├── architecture.md            #   全景架构文档（含配置项/错误处理索引）
│   │   ├── data-model.md              #   全景数据模型文档
│   │   ├── api-catalog.md             #   全景 API 目录
│   │   ├── nfr-baseline.md            #   NFR 基线文档
│   │   ├── config-items.md            #   配置项设计文档（新增，对齐 detailed-design.md §五）
│   │   └── error-handling.md          #   错误处理设计文档（新增，对齐 detailed-design.md §六）
│   ├── changelog.md                   # 变更日志（按年归档）
│   ├── prototypes/
│   │   └── index.html
│   └── ...
│
├── CONTEXT.md                         # 项目级领域词汇表（设计探索阶段构建和增补，所有阶段引用）
│
├── adr/                               # 架构决策记录目录
│   ├── index.md                       # ADR 索引（所有 ADR 的列表）
│   └── {序号}-{标题}.md               # 单个 ADR 文件（如 0001-choose-message-queue.md）
│
├── service-guide.md                   # 项目服务指引（init 预生成草稿，code 阶段补充完善，含多环境配置）
│
├── skill-suggestion.md                # Skills 优化建议记录
│
└── archive/                           # 归档的设计文档
    └── {YYYY-MM-DD}-{design}/
```

### 2.2 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 变更目录 | kebab-case | `product-init`, `add-user-auth`, `fix-login-bug` |
| 子变更目录 | kebab-case | `user-auth`, `order-management`, `payment-integration` |
| 功能设计目录 | `functional-designs/` | `docs/changes/{change}/functional-designs/` |
| 功能设计索引 | `index.md` | `docs/changes/{change}/functional-designs/index.md` |
| 功能设计分册 | `part-NN.md` | `docs/changes/{change}/functional-designs/part-01.md` |
| 详细设计文件 | `detailed-design.md` | `docs/changes/{change}/detailed-design.md` |
| API测试目录 | `api-tests/` | `docs/changes/{change}/api-tests/` |
| API测试索引 | `index.md` | `docs/changes/{change}/api-tests/index.md` |
| API测试分册 | `part-NN.md` | `docs/changes/{change}/api-tests/part-01.md` |
| E2E测试目录 | `e2e-tests/` | `docs/changes/{change}/e2e-tests/` |
| E2E测试索引 | `index.md` | `docs/changes/{change}/e2e-tests/index.md` |
| E2E测试分册 | `part-NN.md` | `docs/changes/{change}/e2e-tests/part-01.md` |
| 集成测试目录 | `integration-tests/` | `docs/changes/{change}/integration-tests/` |
| 集成测试索引 | `index.md` | `docs/changes/{change}/integration-tests/index.md` |
| 集成测试分册 | `part-NN.md` | `docs/changes/{change}/integration-tests/part-01.md` |
| 覆盖追溯矩阵 | `traceability.md` | `docs/changes/{change}/traceability.md` |
| 问题登记目录 | `bugs/` | `docs/changes/{change}/bugs/` |
| 问题索引 | `index.md` | `docs/changes/{change}/bugs/index.md` |
| 问题详情分页 | `bug-NNN-NNN.md` | `docs/changes/{change}/bugs/bug-001-020.md` |
| 自审记录目录 | `self-reviews/{phase}/` | `docs/changes/{change}/self-reviews/explore/` |
| 自审记录文件 | `{YYYYMMDD}-{HHMMSS}.md` | `docs/changes/{change}/self-reviews/explore/20260514-093000.md` |
| 交叉审查目录 | `cross-reviews/{YYYYMMDD}-{HHMMSS}/` | `docs/changes/{change}/cross-reviews/20260514-150000/` |
| 归档目录 | `{YYYY-MM-DD}-{change}` | `2026-05-15-product-init` |
| 测试报告 | `round-{n}.md` | `round-1.md`, `round-2.md` |
| 修复报告 | `fix-{timestamp}.md` | `fix-202604291430.md` |
| 集成测试修复报告 | `fix-{timestamp}.md` | `test-reports/integration/fix-reports/fix-202605041430.md` |
| 迁移脚本 | `{序号}_{子变更}_{描述}.sql` | `001_user-auth_create_users.sql` |
| 回滚脚本 | `{序号}_{子变更}_{描述}_rollback.sql` | `001_user-auth_create_users_rollback.sql` |
| 产品级索引入口 | `index.md` | `docs/designs/index.md` |
| 功能模块目录（前后端） | `{menu}/` | `docs/designs/functional-designs/user-auth/` |
| 功能模块文件（纯后端） | `{domain}.md` | `docs/designs/functional-designs/auth-service.md` |
| 技术设计文档 | `{type}.md` | `docs/designs/technical-designs/architecture.md` |
| ADR 文件 | `{序号}-{kebab-case标题}.md` | `docs/adr/0001-choose-redis-cluster.md` |
| ADR 索引 | `index.md` | `docs/adr/index.md` |
| checkpoint | `{YYYYMMDD-HHMMSS}-checkpoint[-auto].md` | `20260430-143000-checkpoint.md` |

### 2.3 功能点与子变更数量限制

| 场景 | 规则 |
|------|------|
| 功能点 ≤ 10 | 不需要拆分子变更，子变更目录为空或只有一个子变更 |
| 功能点 > 10 且 ≤ 20 | 必须拆分为多个子变更，每个子变更功能点 ≤ 10 |
| 子变更数量 | 每个变更最多 20 个子变更，超过时需拆分为多个变更 |
| 子变更依赖 | 明确子变更之间的依赖关系和实现顺序 |
| 子变更划分时机 | 详细设计完成后，基于完整设计认知划分 |

### 2.4 文档拆分策略

#### 产品级文档拆分（从一开始即多文件）

产品级文档 (`docs/designs/`) 从一开始即采用多文件拆分策略，避免单文件随归档合并持续膨胀：

```
docs/designs/
├── index.md                  # 索引入口（轻量，全局导航）
├── functional-designs/       # 按功能模块拆分的功能设计文档
│   ├── index.md              #   功能模块导航索引
│   ├── user-auth/            #   用户认证模块（前后端项目：按一级菜单目录化）
│   │   ├── index.md          #     菜单级索引（功能点清单、分册总览、修订记录）
│   │   └── part-01.md        #     功能设计分册
│   ├── order-management/     #   订单管理模块
│   │   ├── index.md
│   │   └── part-01.md
│   └── ...                   #   纯后端项目则使用 {domain}.md 平铺文件
├── technical-designs/        # 产品级技术设计文档（6 文件体系）
│   ├── architecture.md       #   全景架构文档（含配置项/错误处理索引）
│   ├── data-model.md         #   全景数据模型文档
│   ├── api-catalog.md        #   全景 API 目录
│   ├── nfr-baseline.md       #   NFR 基线文档
│   ├── config-items.md       #   配置项设计文档（新增）
│   └── error-handling.md     #   错误处理设计文档（新增）
└── changelog.md              # 变更日志（按年归档，文件超过 500 行触发归档）
```

**拆分原则**：
- `index.md` 保持轻量，仅提供全局导航和各模块摘要（每模块 2-3 句）
- 前后端项目：功能设计文档按一级菜单 kebab-case 目录组织，目录内 `index.md` + `part-NN.md` 与变更级 functional-designs 结构一致
- 纯后端项目：功能设计文档按设计域 `{domain}.md` 平铺，使用 backend-domain.md 简化模板
- 技术设计文档 (`technical-designs/`) 按类型拆分为 6 文件，与变更级 `detailed-design.md` 六大章节对应
- 全景文档仅在涉及跨模块变更时更新（如新增数据实体追加到 data-model.md）
- `changelog.md` 按年归档：文件超过 500 行时触发归档，同时保留年末强制归档

#### 变更级文档拆分（条件触发）

| 条件 | 处理方式 |
|------|---------|
| 功能点 ≤ 20 | 单文件 `detailed-design.md`，内部分章节按设计域组织 |
| 功能点 > 20 | 拆分为多文件 `detailed-design/{domain}.md` + 索引入口 `detailed-design/index.md` |
| 子变更 ≤ 20 | 按子变更目录组织（现有机制） |
| 子变更 > 20 | 拆分为多个变更 |

#### 按条目数量拆分（≤30 规则，4 组文档）

以下 4 组文档统一采用 index.md + part-NN.md 目录化结构，每个分册 ≤ 30 个条目：

| 文档组 | 目录 | 拆分依据 | 分册条目上限 | 索引文件要点 |
|--------|------|---------|------------|------------|
| 功能设计 | `functional-designs/` | 功能点数 | ≤ 30 | 逐条列出功能点ID、名称、简述、优先级、依赖、所在分册 |
| API测试 | `api-tests/` | 接口数 | ≤ 30 | 逐条列出接口ID、方法、路径、简述、用例数、所在分册 |
| E2E测试 | `e2e-tests/` | 场景数 | ≤ 30 | 逐条列出功能点ID、覆盖场景列表、验证类型、所在分册 |
| 集成测试 | `integration-tests/` | 场景数 | ≤ 30 | 逐条列出功能点ID、所属子变更、集成场景、验证要点、所在分册 |

**拆分规则**：
- 条目数 ≤ 30：仅包含 `index.md` + 一个 `part-01.md`
- 条目数 > 30：拆分为 `index.md` + N 个 `part-NN.md`（每个 ≤ 30 条目）
- 最后一个分册条目数可能少于 30
- 分册文件统一使用 `part-01.md`, `part-02.md` ... 两位数字编号
- `index.md` 包含逐条概要（不丢失关键信息），具备独立可读性

**索引入口格式** (`functional-designs/index.md` 示例)：

```markdown
# 功能设计索引：{change-name}

> **版本**: 1.0.0
> **总功能点数**: {n}

## 分册总览

| 分册 | 文件 | 功能点范围 | 功能点数 | 内容简述 |
|------|------|-----------|---------|---------|
| Part 01 | [part-01.md](part-01.md) | FP-001 ~ FP-030 | 30 | 核心业务功能 |
| Part 02 | [part-02.md](part-02.md) | FP-031 ~ FP-045 | 15 | 辅助功能 |

## 功能点逐条清单

| 功能点ID | 名称 | 简述 | 优先级 | 依赖功能点 | 所在分册 |
|----------|------|------|--------|-----------|---------|
| FP-001 | 用户注册 | 新用户通过邮箱注册账号 | P0 | 无 | part-01 |
| FP-002 | 用户登录 | 已注册用户通过邮箱密码登录 | P0 | #001 | part-01 |
```

### 2.5 项目级 CONTEXT.md 领域词汇表

`CONTEXT.md` 是项目级领域词汇表，作为所有阶段术语引用的唯一真实来源。

**生命周期**：

```
CONTEXT.md 生命周期:

  检测 ──▶ 构建 ──▶ 增补 ──▶ 消费
   │         │        │        │
   │         │        │        └── 所有后续阶段引用（design/plan/code/review）
   │         │        │
   │         │        └── kflow-explore 后续变更中增补新术语
   │         │
   │         └── kflow-explore 首次构建
   │
   └── kflow-init 检测存在性
```

**格式规范**：

```markdown
# CONTEXT — {项目名} 领域词汇表

> **版本**: 1.0.0
> **创建时间**: {YYYY-MM-DD}
> **修订记录**:
> | 版本 | 日期 | 修订内容 | 触发阶段 |
> |------|------|---------|---------|
> | 1.0.0 | {YYYY-MM-DD} | 初始构建 | 设计探索 |

## {领域术语}

- **定义**: 该概念在项目中的精确定义
- **别名**: （可选，代码中出现的变体名称）
- **边界**: 明确什么不是这个概念（显式排除）
```

**规则**：

| 规则 | 说明 |
|------|------|
| 禁止实现耦合 | 术语不包含类名、表名等实现细节 |
| 修订记录强制 | 每次增补必须更新版本号和修订记录 |
| 单一真实来源 | 所有阶段涉及领域概念时必须引用 CONTEXT.md，不自定义 |
| 消费链 | explore 构建 → design 引用审查 → plan 用于任务描述 → code 用于命名 → review 用于审查 |

---
