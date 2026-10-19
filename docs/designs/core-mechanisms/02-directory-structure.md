# KFlow Skills 核心运行机制

> **版本**: 参见仓库根目录 `VERSION` 文件
> **创建时间**: 2026-04-29
> **更新时间**: 2026-10-19

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
│   │   ├── .status.md                 # 变更总状态文件（**当前有效状态**，≤100 行；含子变更进度矩阵）
│   │   ├── status-log.md              # 变更状态历史日志（各阶段完成时间与耗时、历史轮次、回退与重执行记录）
│   │   │                              #   ↑ 读取场景：**中断恢复与审计**；常规阶段推进与门控判定 SHALL NOT 读取
│   │   ├── revision-history.md        # 变更级产物的修订记录历史（按产物文件分组）
│   │   │                              #   ↑ 读取场景：**版本追溯**（某产物的历史修订内容）；常规读取 SHALL NOT 读取
│   │   ├── tasks.md                   # 变更总任务清单（子变更级checkbox）
│   │   ├── functional-designs/        # 功能设计阶段输出（目录化结构）
│   │   │   ├── index.md               #   功能设计索引入口（全部功能点清单、依赖关系图）
│   │   │   └── part-NN.md             #   功能设计分册文件（每个分册 ≤30 个功能点）
│   │   ├── prototype-changes.md       # 原型改动清单（可选，变更级；含改动前哈希）
│   │   ├── prototype-backup/          # 原型改动前快照（可选，变更级；按产品级相对路径镜像）
│   │   ├── prototype-plan/            # 原型设计过程产物（可选，变更级）
│   │   │   ├── design-prompt.md       #   设计提示词（7 章节，DESIGN 步骤唯一输入）
│   │   │   └── style-decision.md      #   风格决策记录
│   │   ├── element-coverage-tree.md   # 元素覆盖树（可选，变更级；TC-ID 待 design 阶段填充）
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
│   │   │   │   └── report.md           # 单轮验证报告（固定一份）
│   │   │   ├── prototype/              # prototype 阶段自审与验证记录
│   │   │   │   ├── report.md           # SELFREV 单轮验证报告（固定一份）
│   │   │   │   ├── verify-report.md    # VERIFY 单轮合并验证报告（导航/Playwright/UX/对比度四分区）
│   │   │   │   └── cdn-crossref-check/  # CDN 扫描 + 交叉引用检查合并报告
│   │   │   │       └── report.md
│   │   │   ├── design/                 # design 阶段自审记录
│   │   │   │   └── report.md
│   │   │   └── plan/                   # plan 阶段自审记录
│   │   │       └── report.md
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
│           ├── status-log.md
│           ├── revision-history.md
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
│   ├── detailed-designs/             # 产品级详细设计文档（6 文件体系）
│   │   ├── architecture.md            #   全景架构文档（含配置项/错误处理索引）
│   │   ├── data-model.md              #   全景数据模型文档
│   │   ├── api-catalog.md             #   全景 API 目录
│   │   ├── nfr-baseline.md            #   NFR 基线文档
│   │   ├── config-items.md            #   配置项设计文档（新增，对齐 detailed-design.md §五）
│   │   └── error-handling.md          #   错误处理设计文档（新增，对齐 detailed-design.md §六）
│   ├── prototypes/                    # 产品级原型（唯一来源，由原型设计阶段直写）
│   │   ├── index.html                 #   全产品导航入口（卡片网格按功能模块分组）
│   │   ├── manifest.md                #   全产品原型清单（产物/角色/来源变更/修订记录）
│   │   ├── design-tokens.css          #   设计令牌（色板/字号/间距/圆角/阴影 CSS 变量）
│   │   ├── design-system/             #   设计系统
│   │   │   └── MASTER.md              #     设计系统主文档（色彩/字体/间距/组件/交互规则）
│   │   ├── screens/                   #   各屏幕页面 HTML
│   │   ├── components/                #   共享组件
│   │   └── assets/                    #   静态资源
│   ├── changelog.md                   # 变更日志（按年归档）
│   └── ...
│
├── bugs/                              # 项目级缺陷工作区（用户反馈 / 不属于任何活跃变更的缺陷）
│   ├── index.md                       #   问题索引（统计+问题列表+分页表）
│   ├── bug-NNN-NNN.md                 #   分页详情文件（每文件 ≤20 条 BUG）
│   └── fix/{BUG-ID}/                  #   快车道缺陷产物（仅 L4 快车道缺陷存在）
│       ├── bugfix-status.md           #     缺陷级状态文件
│       └── verify-report.md           #     定向验证报告
│
├── CONTEXT.md                         # 项目级领域词汇表（设计探索阶段构建和增补，所有阶段引用）
│
├── adr/                               # 架构决策记录目录
│   ├── index.md                       # ADR 索引（所有 ADR 的列表）
│   └── {序号}-{标题}.md               # 单个 ADR 文件（如 0001-choose-message-queue.md）
│
├── service-guide.md                   # 项目服务指引（init 预生成草稿，code 阶段补充完善，含多环境配置）
│
└── skill-suggestion.md                # Skills 优化建议记录
```

### 2.1.1 缺陷工作区（项目级 / 变更级）

缺陷登记 SHALL 支持两种工作区，由 `kflow-bug-triage` 在登记前判定：

| 工作区 | 触发场景 | 路径根 | 文件清单 | 生命周期 |
|--------|---------|--------|---------|---------|
| 项目级 | 用户反馈的缺陷（A 路径）；不属于任何活跃变更的缺陷；活跃变更存在但缺陷由既有功能或历史代码导致 | `docs/bugs/` | `index.md`、`bug-NNN-NNN.md`、`fix/{BUG-ID}/bugfix-status.md`、`fix/{BUG-ID}/verify-report.md` | 不随任何变更归档移动或删除；收口后保留为历史记录；未关闭的 🔴 阻塞级缺陷阻断任意变更归档 |
| 变更级 | 测试阶段自动发现的缺陷（B 路径）；由活跃变更引入的代码或产物导致的缺陷 | `docs/changes/{change}/bugs/` | 结构同项目级 | 随变更整体归档到 `docs/changes/archive/`；归档前检查该变更未关闭的 🔴 阻塞级缺陷 |

**规则**：

- 两种工作区同构（索引 + 分页详情 + `fix/{BUG-ID}/` 快车道产物），但各自独立维护 BUG-ID 递增序号
- 跨工作区引用缺陷时 SHALL 使用「工作区路径 + BUG-ID」形式，SHALL NOT 仅使用 BUG-ID
- 项目级缺陷 SHALL NOT 创建 `docs/changes/{change}/` 目录，SHALL NOT 进入变更级阶段状态矩阵、审计或归档
- `docs/bugs/index.md` 不存在时，归档门控视为项目级门控满足，SHALL NOT 因缺少该文件而阻塞归档

### 2.2 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 变更目录 | kebab-case | `product-init`, `add-user-auth`, `fix-login-bug` |
| 变更状态日志 | `status-log.md` | `docs/changes/{change}/status-log.md`（读取场景：中断恢复 / 审计） |
| 产物修订历史 | `revision-history.md` | `docs/changes/{change}/revision-history.md`（读取场景：版本追溯） |
| 子变更目录 | kebab-case | `user-auth`, `order-management`, `payment-integration` |
| 功能设计目录 | `functional-designs/` | `docs/changes/{change}/functional-designs/` |
| 功能设计索引 | `index.md` | `docs/changes/{change}/functional-designs/index.md` |
| 功能设计分册 | `part-NN.md` | `docs/changes/{change}/functional-designs/part-01.md` |
| 详细设计文件 | `detailed-design.md` | `docs/changes/{change}/detailed-design.md` |
| 原型改动清单 | `prototype-changes.md` | `docs/changes/{change}/prototype-changes.md` |
| 原型改动前快照 | `prototype-backup/{产品级相对路径}` | `docs/changes/{change}/prototype-backup/screens/login.html` |
| 原型过程产物目录 | `prototype-plan/` | `docs/changes/{change}/prototype-plan/` |
| 元素覆盖树 | `element-coverage-tree.md` | `docs/changes/{change}/element-coverage-tree.md` |
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
| 问题登记目录（变更级） | `bugs/` | `docs/changes/{change}/bugs/` |
| 问题登记目录（项目级） | `bugs/` | `docs/bugs/` |
| 问题索引 | `index.md` | `docs/changes/{change}/bugs/index.md`、`docs/bugs/index.md` |
| 问题详情分页 | `bug-NNN-NNN.md` | `docs/changes/{change}/bugs/bug-001-020.md`、`docs/bugs/bug-001-020.md` |
| 缺陷级状态文件 | `fix/{BUG-ID}/bugfix-status.md` | `docs/changes/{change}/bugs/fix/BUG-001/bugfix-status.md`、`docs/bugs/fix/BUG-001/bugfix-status.md` |
| 定向验证报告 | `fix/{BUG-ID}/verify-report.md` | `docs/changes/{change}/bugs/fix/BUG-001/verify-report.md`、`docs/bugs/fix/BUG-001/verify-report.md` |
| 自审记录目录 | `self-reviews/{phase}/` | `docs/changes/{change}/self-reviews/explore/` |
| 自审记录文件 | `report.md` | `docs/changes/{change}/self-reviews/explore/report.md` |
| 交叉审查目录 | `cross-reviews/{YYYYMMDD}-{HHMMSS}/` | `docs/changes/{change}/cross-reviews/20260514-150000/` |
| 归档目录 | `{YYYY-MM-DD}-{change}` | `docs/changes/archive/2026-05-15-product-init` |
| 测试报告 | `round-{n}.md` | `round-1.md`, `round-2.md` |
| 修复报告 | `fix-{timestamp}.md` | `fix-202604291430.md` |
| 集成测试修复报告 | `fix-{timestamp}.md` | `test-reports/integration/fix-reports/fix-202605041430.md` |
| 迁移脚本 | `{序号}_{子变更}_{描述}.sql` | `001_user-auth_create_users.sql` |
| 回滚脚本 | `{序号}_{子变更}_{描述}_rollback.sql` | `001_user-auth_create_users_rollback.sql` |
| 产品级索引入口 | `index.md` | `docs/designs/index.md` |
| 功能模块目录（前后端） | `{menu}/` | `docs/designs/functional-designs/user-auth/` |
| 功能模块文件（纯后端） | `{domain}.md` | `docs/designs/functional-designs/auth-service.md` |
| 详细设计文档 | `{type}.md` | `docs/designs/detailed-designs/architecture.md` |
| 产品级原型目录 | `prototypes/` | `docs/designs/prototypes/` |
| 产品级原型入口 | `index.html` | `docs/designs/prototypes/index.html` |
| 产品级原型清单 | `manifest.md` | `docs/designs/prototypes/manifest.md` |
| 设计令牌 | `design-tokens.css` | `docs/designs/prototypes/design-tokens.css` |
| 设计系统主文档 | `design-system/MASTER.md` | `docs/designs/prototypes/design-system/MASTER.md` |
| 原型屏幕页面 | `screens/{screen}.html` | `docs/designs/prototypes/screens/login.html` |
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
├── detailed-designs/        # 产品级详细设计文档（6 文件体系）
│   ├── architecture.md       #   全景架构文档（含配置项/错误处理索引）
│   ├── data-model.md         #   全景数据模型文档
│   ├── api-catalog.md        #   全景 API 目录
│   ├── nfr-baseline.md       #   NFR 基线文档
│   ├── config-items.md       #   配置项设计文档（新增）
│   └── error-handling.md     #   错误处理设计文档（新增）
├── prototypes/               # 产品级原型（唯一来源，由原型设计阶段直写）
│   ├── index.html            #   全产品导航入口
│   ├── manifest.md           #   全产品原型清单
│   ├── design-tokens.css     #   设计令牌
│   ├── design-system/        #   设计系统
│   ├── screens/              #   各屏幕页面 HTML
│   ├── components/           #   共享组件
│   └── assets/               #   静态资源
└── changelog.md              # 变更日志（按年归档，文件超过 500 行触发归档）
```

**拆分原则**：
- `index.md` 保持轻量，仅提供全局导航和各模块摘要（每模块 2-3 句）
- 前后端项目：功能设计文档按一级菜单 kebab-case 目录组织，目录内 `index.md` + `part-NN.md` 与变更级 functional-designs 结构一致
- 纯后端项目：功能设计文档按设计域 `{domain}.md` 平铺，使用 backend-domain.md 简化模板
- 详细设计文档 (`detailed-designs/`) 按类型拆分为 6 文件，与变更级 `detailed-design.md` 六大章节对应
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

#### 按需分片读取规则

拆分产生的目录化结构 SHALL 配套按需分片读取，SHALL NOT 被整体读取：

| 规则 | 说明 |
|------|------|
| 经索引定位 | 读取已拆分文档组（functional-designs / api-tests / e2e-tests / integration-tests 的 `part-NN.md`，以及目录化的 detailed-design）前，SHALL 先读取该文档组的 `index.md` 定位目标功能点/接口/场景/设计域所在分册 |
| 只读目标分册 | 定位后 SHALL 仅读取目标分册，或该分册中的目标行区间；SHALL NOT 读取其余分册 |
| 未拆分文档的片段读取 | 未触发拆分但体量较大的文档，SHALL 按章节行区间读取所需片段 |
| 索引文件是唯一可整体读取对象 | 需要了解文档组全貌时，整体读取的对象 SHALL 限于 `index.md`；其体量须保持在可整体读取的范围内 |
| 产品级文档按体积两档处理 | 产品级文档 > 30 KB SHALL 提供章节索引；> 80 KB SHALL 拆分为目录化结构；术语表例外（见 `large-doc-splitting` 能力） |

**片段注入优先于读取指令**：主 Agent 构造子代理 prompt 时，对子代理所需的大文档输入 SHALL 直接选取并注入所需片段，SHALL NOT 仅以「请读取某文件」的形式转嫁读取动作。片段选取范围 SHALL 与该子代理承担的功能点或任务项对应，SHALL NOT 注入与其职责无关的章节；子代理在执行中发现内联片段不足时，SHALL 有权按章节行区间自行读取。

> 权威定义见 `large-doc-splitting` 能力；RELOAD 场景下的具体执行见 `09-phase-hooks.md` §5.5。

#### 修订记录留存边界

承载修订记录的文档，其头部 SHALL 仅保留最近 **3 条**修订记录；超出部分 SHALL 按文档层级移入历史承载位置：

| 文档层级 | 头部保留 | 历史承载位置 | 读取场景 |
|---------|---------|-------------|---------|
| 变更级产物（`functional-designs/part-NN.md`、`detailed-design.md`、`api-tests/part-NN.md`、`e2e-tests/part-NN.md`、`integration-tests/part-NN.md` 等） | 最近 3 条 | `docs/changes/{change}/revision-history.md`（按产物文件分组） | 版本追溯 |
| 产品级文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`） | 最近 3 条 | `docs/designs/changelog.md`（保留原属文档标识） | 版本追溯 |

**规则**：

- 追加第 4 条时，最早的一条 SHALL 移入对应层级的历史承载位置；移出时全部字段（版本、日期、修订类型、修订内容、影响对象、触发阶段）SHALL 原样保留，SHALL NOT 丢失字段或改写表述
- 文档的当前版本号 SHALL 始终反映全部修订的累积结果——移出不改变版本号
- 历史承载位置 SHALL NOT 参与常规读取；各阶段的阶段前置钩子读取修订记录时，只消费文档头部保留的条目
- 留存边界的执行由变更归档的设计合并步骤承担（见 `04-gates-and-transitions.md` 与 `kflow-archive`），新变更产生的文档自动遵守，用户无需额外操作
- 变更级状态文件的阶段记录**不属于**修订记录，按 `status-file-layering` 能力分层，不套用 3 条规则

> 权威定义见 `artifact-revision-record-retention` 能力；模板的修订记录章节见 `templates/`。

#### 产品级文档体积规则

拆分机制的适用范围 SHALL 覆盖产品级文档（`CONTEXT.md`、`docs/designs/**`、`docs/open/**`），按体积触发两档处理：

| 体积 | 处理方式 | 说明 |
|------|---------|------|
| > **30 KB** | 提供章节索引 | 文件头部的章节导航，或同级 `index.md`；索引列出各章节标题与其行号区间或所在文件 |
| > **80 KB** | 拆分为目录化结构 | `<name>/index.md + <name>/<section>.md`；`index.md` 承载章节导航与分册清单；原单文件路径 SHALL NOT 继续存在 |

**规则**：

- 体积为唯一通用且可机器判定的维度（产品级文档多为叙述性内容，无稳定条目计数）
- 拆分 SHALL 在同一步完成引用更新——项目文档、Skill 规则与脚本中的该文档路径 SHALL 被同步更新，SHALL NOT 留待后续
- **术语表例外**：`CONTEXT.md` 的读取模式是「按术语名随机查询」，拆分会破坏随机查询能力，故 MAY 保持单文件，改为提供按模块或按首字母的术语索引，读取侧按索引定位到目标术语所在区间
- 归档的设计合并步骤在改变产品级文档的章节结构或体积时 SHALL 同步维护索引并在跨越阈值时触发拆分

> 权威定义见 `large-doc-splitting` 能力；存量文档的一次性优化入口见 `kflow-doc-optimize`。

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
