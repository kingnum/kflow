# Tasks

## 1. 项目级缺陷工作区与模板

- [x] 1.1 新增项目级缺陷模板 `docs/designs/templates/bugs/bugs-index.md`、`bugs-detail.md`、`fix/{BUG-ID}/bugfix-status.md`、`fix/{BUG-ID}/verify-report.md`，并在 `docs/designs/templates/index.md` 登记；验证：四个模板文件存在且索引表包含对应行
- [x] 1.2 更新 `docs/designs/core-mechanisms/02-directory-structure.md`，登记 `docs/bugs/` 的目录结构、文件清单与生命周期；验证：文档同时描述项目级与变更级两种工作区
- [x] 1.3 更新 `docs/designs/core-mechanisms/03-status-and-tasks.md` §3.5，定义 `bugfix-status.md` 的工作区字段与两种路径；验证：路径表同时列出 `docs/bugs/fix/{BUG-ID}/` 与 `docs/changes/{change}/bugs/fix/{BUG-ID}/`

## 2. kflow-guide 路由调整

- [x] 2.1 修改 `skills/kflow-guide/SKILL.md` 的 INTENT 与 CHANGES 步骤：修复类关键词不再以活跃变更数量作为前置条件，无活跃变更时直接路由到 `kflow-bug-triage`，禁止引导到 `kflow-explore` 创建变更；验证：SKILL.md 中不再存在“无活跃变更 → 引导创建变更”的修复意图分支
- [x] 2.2 修改 `skills/kflow-guide/SKILL.md` 的流程概览，增加“缺陷修复快车道”独立路径与“简单缺陷无需创建变更”说明；验证：流程概览输出包含该路径且与阶段集合分开
- [x] 2.3 更新 `skills/kflow-guide/SKILL.md` 的 description 与核心提醒，确保触发词覆盖“修复/Bug/缺陷”且不要求变更名；验证：description 与核心提醒一致

## 3. kflow-bug-triage 工作区与路径判定

- [x] 3.1 修改 `skills/kflow-bug-triage/SKILL.md` 门控检查：移除“必须存在活跃变更”，新增缺陷工作区判定（项目级 / 变更级）与归属判定；验证：门控表不再要求 `.status.md` 必须存在，且包含归属判定分支
- [x] 3.2 修改 `skills/kflow-bug-triage/SKILL.md` 输入要求与输出产物：项目级使用 `docs/bugs/`，变更级使用 `docs/changes/{change}/bugs/`；验证：输入/输出表的路径按工作区分支
- [x] 3.3 修改 `skills/kflow-bug-triage/SKILL.md` 四层溯源证据来源：无活跃变更时使用 `docs/designs/functional-designs/`、`docs/designs/prototypes/`、`docs/designs/detailed-designs/`；验证：证据来源表包含两种工作区
- [x] 3.4 修改 `skills/kflow-bug-triage/SKILL.md` 路由决策：L4 满足快车道条件时进入快车道；L1/L2/L3 或 L4 不满足条件时创建 `功能缺陷` 变更；验证：路由表包含“创建变更”分支与“不新建变更”分支
- [x] 3.5 更新 `skills/kflow-bug-triage/references/hooks.md`、`gates.md`、`repetition.md` 中的路径与 RELOAD 集合，使其支持两种工作区；验证：references 中不存在只指向变更级 `bugs/` 的硬编码路径
- [x] 3.6 在 SKILL.md 增加工作区判定与归属判定的可执行流程（含 AskUserQuestion 兜底）；验证：流程图中存在归属无法判断的分支

## 4. kflow-bug-fix 快车道双工作区

- [x] 4.1 修改 `skills/kflow-bug-fix/SKILL.md` 模式判定：快车道入口不再要求活跃变更，工作区由 `kflow-bug-triage` 声明；验证：门控表包含项目级与变更级两种入口
- [x] 4.2 修改 `skills/kflow-bug-fix/SKILL.md` 输入/输出产物：`bugfix-status.md` 与 `verify-report.md` 路径按工作区解析；验证：输入/输出表不再只写变更级路径
- [x] 4.3 修改 `skills/kflow-bug-fix/SKILL.md` 定向验证：验证目标扩展为已有测试、新增回归测试、手工验证步骤；验证：定向验证节不再只写“测试用例”
- [x] 4.4 修改 `skills/kflow-bug-fix/SKILL.md` 快速收口与回写：项目级更新 `docs/bugs/index.md`，变更级更新 `docs/changes/{change}/bugs/index.md`；验证：收口动作表包含两种索引路径
- [x] 4.5 更新 `skills/kflow-bug-fix/references/gates.md`、`hooks.md`、`repetition.md`、`state-values.md` 中的路径与状态载体描述；验证：references 中不存在只指向变更级的硬编码路径
- [x] 4.6 在 SKILL.md 增加“项目级快车道不与变更级状态/审计耦合”的约束；验证：核心提醒包含该约束

## 5. kflow-archive 阻塞缺陷门控

- [x] 5.1 修改 `skills/kflow-archive/SKILL.md` 与 `references/archive-rules.md`，读取 `docs/bugs/index.md` 并阻断未关闭的 🔴 阻塞级缺陷；验证：归档条件表包含项目级阻塞缺陷项
- [x] 5.2 增加“`docs/bugs/index.md` 不存在时视为门控满足”的兼容规则；验证：归档规则包含该分支
- [x] 5.3 更新 `skills/kflow-archive` 的输入要求与门控输出，列出阻塞缺陷清单；验证：输出模板包含 BUG-ID、标题、状态、详情文件列

## 6. 共享 references、设计文档与运行时同步

- [x] 6.1 修改 `references-src/` 中受影响的共享 references（`gates.md`、`hooks.md`、`repetition.md`、`state-values.md`、`phase-transition.md`），加入项目级缺陷工作区与双路径规则；验证：权威源包含两种工作区
- [x] 6.2 运行 `python scripts/gen-slice-manifest.py` 刷新切片清单，再运行 `bash scripts/sync-references.sh` 生成并校验各 skill 副本；验证：脚本退出码为 0 且无漂移告警
- [x] 6.3 更新 `docs/designs/skills/kflow-guide.md`、`kflow-bug-triage.md`、`kflow-bug-fix.md`、`kflow-archive.md` 的设计规格，使其与 SKILL.md 行为一致；验证：设计文档包含项目级工作区、归属判定、快车道路径与归档门控
- [x] 6.4 更新 `docs/designs/index.md` 与 `docs/designs/overview.md` 的目录结构与机制表，登记项目级缺陷工作区；验证：索引包含 `docs/bugs/` 且不把其计入变更阶段
- [x] 6.5 执行“设计文档 → SKILL.md 同步”：将 6.3 的设计规格同步到 `.claude/skills/` 中对应的 SKILL.md；验证：差异比对无遗漏章节
- [x] 6.6 运行 `python scripts/validate-frontmatter.py` 与 `openspec validate route-simple-defects-to-fast-lane --strict`；验证：两者均通过

## 7. 集成场景验证

- [x] 7.1 模拟“无活跃变更 + 简单 L4 缺陷”：执行 triage 与快车道流程，验证不创建 `docs/changes/` 目录、`docs/bugs/fix/{BUG-ID}/` 产物齐全、收口后索引状态为“已解决”
- [x] 7.2 模拟“有活跃变更 + 与该变更无关的缺陷”：验证缺陷登记到 `docs/bugs/`、不创建新变更、不修改活跃变更 `.status.md`
- [x] 7.3 模拟“有活跃变更 + 由该变更引入的缺陷”：验证缺陷登记到变更级 `bugs/`、进入变更级快车道或 REVISION、不创建新变更
- [x] 7.4 模拟“L1/L2/L3 缺陷”与“L4 但不满足快车道条件”：验证均创建 `功能缺陷` 变更并正确路由
- [x] 7.5 模拟“项目级 🔴 阻塞缺陷未关闭”：验证 `kflow-archive` 阻塞并输出缺陷清单；关闭后再次验证归档门控通过
