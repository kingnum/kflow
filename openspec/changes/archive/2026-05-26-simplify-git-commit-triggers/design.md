## Context

当前 Git commit 触发点分散在 4 个 Skill 中（kflow-init、kflow-guide、kflow-plan、kflow-archive），共计 5+ 条强制规则，且上一个变更 `skill-packaging-and-version-unification` 将项目级机制（版本自增+打包）错误注入到 `kflow-archive` Skill 中。本设计将 Git 触发点简化为 2 个询问式节点，并纠正版本+打包的错误归属。

### 当前状态 vs 目标状态

```
当前（5 触发点，全强制）:
  kflow-init  → 「init后必须commit」(规则#10)
  kflow-guide → PRECOMMIT: 新变更前必须检查+提交 (规则#9)
  kflow-plan  → 每功能点 Step 8: git commit
  kflow-plan  → 自审: 检查「提交粒度」
  kflow-archive → VERSION → PACKAGE → COMMIT (强制)

目标（2 触发点，全询问）:
  kflow-init  → 询问是否 git init（创建仓库，不commit）
  kflow-archive → 询问是否 git commit（ANALYZE → ASK → COMMIT）
```

## Goals / Non-Goals

**Goals:**
- Git commit 触发点从 5 个简化为 2 个
- 所有 git 操作从强制改为 AskUserQuestion 询问
- 从 kflow-archive 中移除 VERSION + PACKAGE 步骤（纠正错误注入）
- 从 kflow-guide 中删除 PRECOMMIT 步骤
- 从 kflow-plan 中删除每功能点 commit 步骤及相关自审检查项
- CLAUDE.md 规则从 3 条强制改为 2 条询问

**Non-Goals:**
- 不改变 CLAUDE.md 中的版本自增+打包规则（项目级，位置正确）
- 不改变 scripts/package-skills.sh 和 VERSION 文件
- 不新增任何 git 触发点
- 不自动 push（保持现有行为）

## Decisions

### 1. 所有 git 操作统一使用 AskUserQuestion

选择：所有 git 操作前使用 AskUserQuestion 弹窗询问，三个选项「确认提交」「修改提交信息」「跳过」。

理由：尊重用户控制权。之前"必须 commit"的设计过于刚性，用户在不同场景下有不同的提交节奏偏好。

备选：静默执行+事后提示 → 不采用，git commit 是历史记录锚点，用户应有知情权和否决权。

### 2. kflow-init 从「必须 commit」改为「询问 git init」

当前行为：首次 init 生成产品文档后执行 `git init: 项目初始化...` commit。

改为：检测当前目录是否是 git 仓库。若不是仓库，AskUserQuestion 询问是否执行 `git init`；若已是仓库，跳过。

理由：用户输入的「首次init时询问是否创建git仓库」——语义是 git init（创建仓库），不是 git commit。原规则 #10 将两者混淆了。

### 3. kflow-archive: 移除 VERSION + PACKAGE，COMMIT 改为询问

当前 kflow-archive 的步骤 9-11 为：VERSION → PACKAGE → COMMIT(强制)。

改为：步骤 9 ANALYZE → 步骤 10 COMMIT(AskUserQuestion)。

- 删除步骤 9 (VERSION) 和步骤 10 (PACKAGE)：这些是项目级 CI/CD，非 Skill 功能
- 删除 "# 归档后版本自增、打包与 git commit" 整个 section（约 80 行）
- COMMIT 从 `git add VERSION targets/` + `git add -A` + `git commit` 改为 `git add -A` + AskUserQuestion
- 保留 ANALYZE（分析归档内容生成摘要）和 SUMMARIZE（生成提交信息）逻辑

### 4. kflow-guide: 删除 PRECOMMIT 步骤

从 workflow 图中删除步骤 2 (PRECOMMIT)，workflow 变为：

```
步骤 1: INPUT → 步骤 2: PARSE → 步骤 3: INTENT → ...
```

删除 "# 新变更前 git commit 检查" 整段（约 45 行），包括触发条件说明、检查流程（5 步）、提交信息格式规范表格。

### 5. kflow-plan: 删除 commit 步骤

tasks.md 模板从 8 步改为 7 步，删除 Step 8（提交变更）。TDD 循环变为 Step 1-7：编写测试→RED→实现→GREEN→质量检查→重构→验证。

VERIFY 步骤中删除「提交记录」检查项。

自审维度「任务粒度合理性」中删除「提交粒度」检查项（"每功能点完成后是否包含独立 git commit 步骤"）。

### 6. 提交信息格式规范（仅用于归档后 commit）

归档后询问提交时保留一行中文摘要格式：

| 场景 | 格式 | 示例 |
|------|------|------|
| 归档已完成 | `归档变更 {name}: {一行摘要}` | `归档变更 add-2fa: 新增双因素认证` |
| 归档未完成 | `归档变更 {name}(未完成): {归档原因}` | `归档变更 refactor-user(未完成): 中途归档` |

不再需要的格式（删除）：
- ~~`{动词}: {摘要}`（代码/文档变更类）~~ — 用于 pre-change commit，已删除
- ~~`init: {摘要}`~~ — 用于 init 后 commit，已删除

### 7. 08-governance.md 18.5 强制规则注入

从 3 条改为 2 条：

```
旧（3 条）:
1. 每个变更归档后必须执行 git commit
2. 开始新变更前必须检查 git 状态
3. 首次 init 完成后若生成了产品文档则必须 git commit

新（2 条）:
1. 首次 init 时，若目录非 git 仓库，询问是否执行 git init
2. 归档完成后，询问是否将当前变更及相关文件提交 git
```

## Risks / Trade-offs

- **无 git 版本管理的项目风险**: 删除 PRECOMMIT 后，用户在开始新变更前不会被提醒提交未保存的变更 → 由用户自行负责，Skill 体系不替代 git 最佳实践
- **Plan 阶段缺少提交锚点**: 删除每功能点 commit 后，plan 阶段不再有提交记录 → 如需细粒度历史可由用户在实施阶段自行提交
- **kflow-archive 移除打包步骤确认**: VERSION+PACKAGE 保留在 CLAUDE.md 中，属于本项目开发流程，不影响 skill 在目标项目中的行为
