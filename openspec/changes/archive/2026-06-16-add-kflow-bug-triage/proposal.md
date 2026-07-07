# Proposal: add-kflow-bug-triage

## Why

当前体系缺少结构化的用户反馈问题处理机制。`kflow-bug-fix` 的三分法根因分类（实现错误/测试错误/设计错误）无法区分需求定义问题、原型设计问题和详细设计问题——所有上游问题都被笼统归为"设计错误"并统一回退到 design 阶段，导致修复方向可能完全错误（例如需求本身有歧义，却在技术方案层面修改）。需要新增一个独立的诊断 Skill，在用户反馈问题时从最上游逐层溯源，精确定位问题源头阶段后再路由修复。

## What Changes

- **新增 `kflow-bug-triage` Skill**：独立诊断 Skill（非流程阶段），接收用户反馈后执行四层溯源漏斗（L1 需求定义 → L2 原型设计 → L3 详细设计 → L4 实现执行），将问题登记到 `bugs/` 目录，并路由到问题源头阶段的 REVISION 模式或调用 `kflow-bug-fix` 执行实现层修复
- **修改 `kflow-bug-fix`**：**BREAKING** 门控入口去掉"用户描述的缺陷信息"（用户反馈统一走 triage）；三分法简化为二分法（去掉"设计错误"出口）；移除设计错误回退路由（上移到 triage）
- **修改 `kflow-guide`**：INTENT 关键词表新增 triage 路由行（用户反馈关键词 → `kflow-bug-triage`）；"修复"关键词增加上下文判断（有活跃 bug-fix 子阶段 → bug-fix，否则 → triage）
- **新增 `bugs/` 目录结构**：在变更目录下新增 `docs/changes/{change}/bugs/`，含 `index.md`（索引）和分页详情文件（每文件最多 20 条 BUG），含明确内容模板
- **新增模板文件**：`bugs-index.md`（索引模板）、`bugs-detail.md`（详情模板）
- **修改 `core-mechanisms/02-directory-structure.md`**：新增 `bugs/` 目录说明

## Capabilities

### New Capabilities

- `bug-triage-skill`: kflow-bug-triage Skill 的完整定义——四层溯源诊断流程、诊断判断标准、路由决策机制、与现有 Skill 的协作关系
- `bug-registration`: 问题登记机制——`bugs/` 目录结构、`index.md` 索引格式、分页详情文件格式（每文件≤20条）、问题严重度分级、状态追踪

### Modified Capabilities

- `defect-root-cause`: 三分法简化为二分法（去掉"设计错误"分类和回退路由），仅保留实现错误/测试错误
- `intent-priority-rules`: 新增 triage 路由关键词（反馈/报告问题/报bug → kflow-bug-triage），"修复"关键词增加上下文判断逻辑
- `change-rollback`: 新增第七种回退触发来源——triage 诊断路由（L1→explore / L2→prototype-design / L3→design）

## Impact

- **Skill 体系**：新增 1 个 Skill（kflow-bug-triage），修改 2 个 Skill（kflow-bug-fix、kflow-guide）
- **目录结构**：变更目录下新增 `bugs/` 子目录
- **模板体系**：新增 2 个模板文件
- **核心机制文档**：`02-directory-structure.md` 需更新
- **已有 Spec**：3 个 spec 需要 delta 修改（defect-root-cause、intent-priority-rules、change-rollback）
- **下游影响**：`kflow-bug-triage` 与 `kflow-verify`（产物诊断）互补不重叠——verify 检查产物质量，triage 诊断问题源头
