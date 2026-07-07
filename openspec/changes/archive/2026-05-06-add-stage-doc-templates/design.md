## Context

当前 14 个 Skill spec 中有 17 个内联模板定义，分散在 `docs/designs/skills/kflow-*.md` 和 `docs/designs/core-mechanisms.md` 中。另有 17 个产物文件完全没有模板定义。模板与 Skill spec 耦合，维护时需要在 Skill 文档中定位和修改。本次变更将模板独立出来，统一管理。

已有产物中，4 组文档（functional-design、api-tests、e2e-tests、integration-tests）可能因功能点/接口/场景数量过大而单文件膨胀，需要引入按量拆分机制。

## Goals / Non-Goals

**Goals:**
- 建立统一的模板目录 `docs/designs/templates/`，按产物层级组织
- 为所有 35 个独立文件产物创建/补全模板（17 个抽取 + 17 个新建 + 1 个补全）
- 4 组大型文档引入 ≤30/分册拆分机制 + 索引文件
- Skill spec 中内联模板替换为模板引用链接
- 索引文件具备可读性，列出关键信息不丢失

**Non-Goals:**
- 不修改 Skill 的执行逻辑或阶段流转规则
- 不修改模板以外的 Skill spec 内容（如执行流程、门控规则）
- prototype.pen / 迁移 SQL 脚本 / 代码文件不创建模板（非结构化内容）
- 不修改已归档的历史变更产物格式

## Decisions

### 决策 1: 五级模板目录结构

**选择**: `templates/` 下按产物层级分为 change / subchange / integration / product / infra 五子目录

**备选**: 按阶段名（explore / design / plan...）分目录

**理由**: 同一产物的产物文件可能跨越阶段边界（如 `.status.md` 在多个阶段使用）。按产物所属的组织层级（变更级/子变更级/集成测试级/产品级/基础设施级）更能反映文件的实际作用域。

### 决策 2: 模板格式 = YAML Frontmatter + Markdown Body

**选择**: 每个模板文件使用 YAML frontmatter 定义元数据（所属阶段、产出 Skill、版本），正文使用 Markdown + `{placeholder}` 占位符

**备选**: 纯 Markdown 无 frontmatter

**理由**: Frontmatter 便于自动化工具解析模板元数据（如检查模板是否被 Skill 引用）。占位符 `{xxx}` 格式在现有规格中已广泛使用，保持一致。

### 决策 3: Skill spec 引用方式 = 产物列表中直接引用模板路径

**选择**: 在 Skill spec 的"输出产物"表格中增加"模板"列，指向 `templates/` 下的文件路径

**示例**:
```markdown
| 产物 | 文件 | 模板 | 图例 |
|------|------|------|------|
| 功能设计 | functional-designs/index.md | [模板](../../templates/change/functional-designs/index.md) | ✅ 必须 |
```

**备选**: 在 Skill spec 末尾集中列出所有模板引用

**理由**: 产物和模板的一一对应关系在"输出产物"表格中最直观。不需要额外的"关联模板"章节。

### 决策 4: 大型文档拆分阈值 = 30

**选择**: 每个分册不超过 30 个条目（功能点/接口/场景）

**备选**: 50 个或 100 个

**理由**: 
- 30 条规则与现有设计约束一致（子变更 ≤10 功能点，变更 ≤20 子变更）
- 一个 Markdown 文件包含 30 个详细条目约 3000-5000 行，是可编辑的上限
- 与 api-tests ≤30 接口/分册保持一致

### 决策 5: 分册命名 = part-NN.md

**选择**: `part-01.md`, `part-02.md` ... 顺序编号，索引文件统一命名为 `index.md`

**备选**: 按内容主题命名（如 `part-user-auth.md`）

**理由**:
- 编号方式简化自动生成逻辑
- 增加/删除条目时不需要重命名文件
- index.md 中已包含各分册的内容主题描述

### 决策 6: 索引文件必须包含逐条概要

**选择**: index.md 不仅列出分册文件范围，还必须列出每个条目的 ID、名称、简述和关键属性

**理由**: 索引文件是变更的"目录"，应当在不打开分册的情况下提供足够信息。对于 e2e-tests/index.md，需要列出每个功能点的覆盖场景和验证类型，以便快速判断覆盖缺口。

### 决策 7: 不创建现有模板的"迁移适配层"

**选择**: 直接修改，不创建过渡期兼容层

**理由**: 当前处于设计阶段，尚无运行态产物依赖旧模板格式。如有少量测试变更使用了旧目录结构，手动调整成本低。

## Risks / Trade-offs

- **[变更范围大]** 35+ 模板文件 + 14 个 Skill spec 更新，工作量大 → 分批实施：先抽取已有模板，再补全新模板，最后更新 Skill spec 引用
- **[模板维护一致性]** 后续 Skill spec 变更可能导致模板与 spec 不同步 → templates/index.md 记录每个模板的关联 Skill，在 kflow-writing-skills 中增加"修改 Skill 时检查关联模板"规则
- **[分册引用复杂度]** 拆分后 Skill 执行时需要知道读取哪个分册 → 门控检查改为检查 index.md 存在即可，index.md 引导定位具体分册
- **[索引文件的维护成本]** 每次增删功能点需要同步更新 index.md → index.md 本身就是门控产物，在对应阶段自然会更新；分册内条目顺序调整不强制同步 index.md 中的序号
