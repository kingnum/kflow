## Context

当前产品级文档体系存在三处结构性缺陷：

1. **路径不一致**：`core-mechanisms.md` 定义 CONTEXT.md 在 `docs/` 下，但 `kflow-init` 设计和 SKILL 中错误引用为「项目根目录」
2. **文档命名与结构脱节**：产品级 `domains/{domain}.md` 按「设计域」拆分，但变更级按功能点拆分；产品级为单文件合并，变更级为 functional-designs/ + detailed-design.md 分离。归档合并时需做结构转换，容易遗漏
3. **模板组织抽象**：`templates/change/`、`templates/product/` 等抽象分层，无法从产物路径直观找到对应模板

另有两处功能缺口：
- init 老项目逆向分析不生成 `service-guide.md`
- 草稿标记「由 AI 逆向分析生成」的去除时机未定义

## Goals / Non-Goals

**Goals:**
- 统一 CONTEXT.md 路径为 `docs/CONTEXT.md`
- 产品级文档结构镜像变更级：`functional-designs/{module}.md` + `technical-designs/`
- 功能设计按功能模块拆分，模块名对应产品菜单/业务模块
- 产品级 `{module}.md` 章节与变更级 `part-NN.md` 完全一致，归档时直接追加无需转换
- init LEGACY 新增第 7 类输出 `docs/service-guide.md`（初步版本，标注草稿）
- 定义去草稿规则：首次归档合并时替换标记
- 模板目录重组为镜像实际 `docs/` 输出结构

**Non-Goals:**
- 不改变变更级文档结构和命名
- 不改变 Skill 的阶段门控逻辑
- 不新增 Skill（本变更纯修正，不引入新 Skill）
- 不改变已有的 `kflow-explore` 输出格式

## Decisions

### Decision 1: 产品级文档目录结构

```
docs/designs/
├── index.md                          # 产品级设计索引入口（不变）
├── functional-designs/               # 产品级功能设计（原 domains/）
│   ├── index.md                      # 功能模块导航索引
│   └── {module}.md                   # 按功能模块命名，kebab-case
│                                     # 例: user-registration-login.md
│                                     #     order-management.md
│                                     #     payment-integration.md
├── technical-designs/                # 产品级技术设计（新增目录）
│   ├── architecture.md               # 全景架构文档
│   ├── data-model.md                 # 全景数据模型文档
│   ├── api-catalog.md                # 全景 API 目录
│   └── nfr-baseline.md               # NFR 基线文档
└── changelog.md                      # 变更日志
```

**理由**：变更级分离 functional + technical，产品级同样分离，归档合并时路径对应清晰：
- `functional-designs/part-NN.md` → `functional-designs/{module}.md`（追加同一模块的功能点）
- `detailed-design.md` → `technical-designs/*.md`（按类型分散更新）

### Decision 2: 功能模块 vs 设计域

从「设计域（domain）」改为「功能模块（module）」：

| 维度 | Domain | Module |
|------|--------|--------|
| 边界 | 抽象领域边界，常争议 | 产品菜单/功能分组，直观 |
| 拆分粒度 | 粗（一个域可能涵盖巨大范围） | 细（一个业务模块） |
| 归档匹配 | 需关键词推断 domain 归属 | 变更名/功能点名直接对应模块 |
| 查找 | 需理解领域分类体系 | 按产品功能菜单定位 |

模块命名规则：kebab-case，与产品菜单项/功能分组对齐，如 `user-registration-login`、`order-management`。

### Decision 3: 产品级 {module}.md 与变更级 part-NN.md 章节一致

产品级 `{module}.md` 结构完全镜像变更级 `part-NN.md`，仅增加来源标注：

```
变更级 part-NN.md                产品级 {module}.md
───────────────────              ─────────────────
## 本册功能点列表                  ## 本模块功能点列表
## 功能点详细定义                  ## 功能点详细定义
  ### FP-xxx: 名称                 ### FP-xxx: 名称
  #### 优先级                       #### 优先级
  #### 用户故事                     #### 用户故事
  #### 所属页面与菜单               #### 所属页面与菜单
  #### 可执行操作                   #### 可执行操作
  #### 表单项定义                   #### 表单项定义
  #### 业务规则                     #### 业务规则
  #### 业务流程上下文               #### 业务流程上下文
  #### 功能行为矩阵                 #### 功能行为矩阵
  #### 交互约束                     #### 交互约束
## 修订记录                        > 来源变更: xxx | 归档时间: yyyy
                                  ## 修订记录
```

归档时操作：对每个 FP，在目标 `{module}.md` 中按 FP-ID 查找 → 已存在则替换更新 → 不存在则追加。

### Decision 4: 模板目录镜像 docs/ 结构

```
当前                                →  目标
──────────────────────────             ──────────────────────────
templates/                             templates/
├── change/                            ├── changes/{change}/
│   ├── functional-designs/            │   ├── functional-designs/
│   ├── api-tests/                     │   ├── api-tests/
│   ├── e2e-tests/                     │   ├── e2e-tests/
│   ├── ...                            │   ├── detailed-design.md
│   └── service-guide.md               │   └── ...
├── subchange/                         ├── design-templates/
├── product/                           │   ├── functional-designs/
│   ├── domain-doc.md  →               │   │   └── {module}.md
│   ├── architecture.md                │   └── technical-designs/
│   └── ...                            │       ├── architecture.md
├── integration/                       │       └── ...
└── infra/                             ├── service-guide.md
                                        ├── toolchain.md
                                        └── ...
```

**理由**：模板路径镜像产物路径，查找时无需查索引表。`templates/` 下的子目录名直接对应实际的 `docs/` 路径。

### Decision 5: init LEGACY 新增 service-guide.md

L1 扫描已具备配置信息（package.json scripts、端口、数据库依赖），可直接生成 dev 环境初步配置：

```markdown
# 项目服务指引

> 由 AI 逆向分析生成，待人工审核

## 项目类型
- **类型**: {从 L1 扫描推断}
- **框架**: {从 L1 扫描推断}

## 多环境配置

### dev 环境
| 配置项 | 值 | 说明 |
|--------|---|------|
| 启动命令 | {从 package.json scripts 推断} | |
| 端口 | {从配置文件扫描} | |
| 数据库 | {从依赖/配置推断} | |

### test / staging / prod 环境
> 待后续补充
```

kflow-code 阶段检测到草稿标记时，进入正常生成/补充流程，替换草稿内容。

### Decision 6: 去草稿规则

archive MERGE 步骤检测目标文档：

```
MATCH 时判断目标文档状态:
  ├── 目标文档包含 "由 AI 逆向分析生成" 草稿标记
  │   → 首次正式内容合并
  │   → 替换草稿标记为: > 来源变更: {change-name} | 归档时间: {YYYY-MM-DD}
  │   → 移除文档顶部草稿提示语
  └── 目标文档不含草稿标记
      → 标准合并流程（追加/替换更新 + 来源标注）
```

## Risks / Trade-offs

- **BREAKING 路径变更**：已有项目的 `CONTEXT.md`（项目根目录）和 `docs/designs/domains/` 需迁移。旧体系项目不受影响（仅新体系 skill 引用受影响）。
  → Mitigation: 在 `kflow-init` re-init 时自动检测旧路径并提示迁移
- **模板重组影响 skill-creator**：`skill-creator` 执行模板初始化时引用旧模板路径
  → Mitigation: 同步更新 `skill-creator` 中的模板路径引用
- **模块边界仍需人工判断**：虽然功能模块比设计域更直观，但模块归属仍可能模糊
  → Mitigation: 归档时 MATCH 步骤使用 AskUserQuestion 确认模块归属

## Migration Plan

1. 更新所有设计文档和 specs 中的路径引用
2. 更新模板文件结构和内容
3. 更新 SKILL.md 实现
4. 已有的产品文档（`docs/designs/domains/`）需手动或通过 re-init 迁移到新结构
5. `git mv` 方式移动 CONTEXT.md（从根目录到 docs/）和 domains/ → functional-designs/
