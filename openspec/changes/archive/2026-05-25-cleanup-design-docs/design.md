## Context

设计文档体系经过多轮迭代后积累了以下不一致：

- **CLAUDE.md** 是项目入口文档，但阶段数（7/5）与设计文档（11/9）严重不一致，工作流链缺少 4 个阶段
- **`core-mechanisms.md`** 单文件 2235 行（约 36K tokens），包含大量 ASCII 树形图和模板示例，远超单文档舒适阅读上限
- 3 个 Skill 的设计文档版本号低于运行时 SKILL.md（explore 2.1.0 vs 2.3.0, design/code 2.0.0 vs 2.1.0）

## Goals / Non-Goals

**Goals:**
- CLAUDE.md 阶段数和工作流链与设计文档完全一致
- `core-mechanisms.md` 拆分为 8 个逻辑文件，每个 ≤ 500 行
- 设计文档版本号与运行时 SKILL.md 同步
- 所有对 `core-mechanisms.md` 的锚点引用保持有效

**Non-Goals:**
- 不引入新功能或修改任何机制逻辑
- 不修改运行时 SKILL.md 内容
- 不修改 templates/ 或 examples/ 内容
- 不修改其他 Skill 设计文档（仅 explore/design/code 三处版本号同步）

## Decisions

### D1: `core-mechanisms.md` 拆分方案

拆分为 6 个文件，按逻辑域组织，确保每个文件 ≤ 500 行：

| 文件 | 来源章节 | 行数范围 | 预计行数 |
|------|---------|---------|---------|
| `01-project-types.md` | 一、项目类型区分机制 | L13-46 | ~35 |
| `02-directory-structure.md` | 二、目录结构规范（含 2.3~2.5） | L48-364 | ~320 |
| `03-status-and-tasks.md` | 三、状态文件规范 + 四、任务清单 | L366-860 | ~495 |
| `04-gates-and-transitions.md` | 五、条件产物引用 + 六、阶段流转规则 | L863-1149 | ~290 |
| `05-execution-model.md` | 七~十一、十三~十四（服务/批量/脚本/审查合并/覆盖追溯） | L1151-1700 | ~550 → 需精简模板示例 |
| `06-recovery-and-governance.md` | 十二、十五、十七~十八（中断恢复/子代理模型/阶段边界/Git） | L1371-end | ~870 → 拆为 06a + 06b？不，十五子代理模型 ~385 行，十二 ~170，十七 ~100，十八 ~50，合计 ~705 → 拆为 `06-recovery.md`（十二）+ `07-agent-model.md`（十五）+ `08-governance.md`（十七~十八） |

**修正后的拆分方案（7 文件）**：

| 文件 | 来源章节 | 行数范围 | 预计行数 |
|------|---------|---------|---------|
| `01-project-types.md` | 一 | L13-46 | ~35 |
| `02-directory-structure.md` | 二 | L48-364 | ~320 |
| `03-status-and-tasks.md` | 三 + 四 | L366-860 | ~495 |
| `04-gates-and-transitions.md` | 五 + 六 | L863-1149 | ~290 |
| `05-execution-services.md` | 七~十一、十三~十四 | L1151-1700 | ~550 → 精简模板后 ≤ 500 |
| `06-recovery.md` | 十二 | L1371-1536 | ~165 |
| `07-agent-model.md` | 十五 | L1703-2085 | ~385 |
| `08-governance.md` | 十七~十八 | L2087-2235 | ~150 |

**锚点映射表**（原 `core-mechanisms.md#xxx` → 拆分后路径）：

| 原锚点 | 来源章节 | 目标文件 | 说明 |
|--------|---------|---------|------|
| `#一项目类型区分机制` / `#11-项目类型定义` / `#12-检测规则` / `#13-阶段差异` | 一 | `core-mechanisms/01-project-types.md` | 阶段数定义 |
| `#二目录结构规范` / `#21-变更管理目录` / `#22-设计文档目录` 等 | 二 | `core-mechanisms/02-directory-structure.md` | 目录模板 |
| `#三状态文件规范` / `#31-状态标记` / `#32-格式` 等 | 三 | `core-mechanisms/03-status-and-tasks.md` | 状态门控 |
| `#四任务清单规范` | 四 | `core-mechanisms/03-status-and-tasks.md` | 任务格式 |
| `#五条件产物引用规范` | 五 | `core-mechanisms/04-gates-and-transitions.md` | 产物引用 |
| `#六阶段流转规则` | 六 | `core-mechanisms/04-gates-and-transitions.md` | 流转门控 |
| `#七服务管理职责归属` ~ `#十一文档禁止规则` | 七~十一 | `core-mechanisms/05-execution-services.md` | 执行规则 |
| `#十三多-agent-审查结果合并机制` / `#十四覆盖追溯机制` | 十三~十四 | `core-mechanisms/05-execution-services.md` | 审查合并 |
| `#十二中断恢复机制` | 十二 | `core-mechanisms/06-recovery.md` | 恢复规则 |
| `#十五子代理执行模型` / `#1511-子代理隔离规则` | 十五 | `core-mechanisms/07-agent-model.md` | 子代理规则 |
| `#十七阶段边界强制` / `#十八git-版本管理机制` | 十七~十八 | `core-mechanisms/08-governance.md` | 治理规则 |

**锚点更新策略**：
1. Grep 定位所有 Skill 和模板中 `core-mechanisms.md#xxx` 引用
2. 按上表映射批量替换为 `core-mechanisms/{target-file}#xxx`
3. 拆分后运行 Grep 确认无死链（文件存在 + 锚点存在）

### D2: CLAUDE.md 修改范围

仅修改两处：
1. 行 77-78 的阶段数：`7 阶段` → `11 阶段`，`5 阶段` → `9 阶段`
2. 行 72-73 的工作流链：补全 `kflow-code-review`、`kflow-api-test`、`kflow-integration-test`、`kflow-audit`

不修改 CLAUDE.md 的其他内容（如核心运行机制摘要、已实现 Skills 列表等）。

### D3: 运行时 Skill 内联规则（方案 B）

运行时 Skill（`.claude/skills/`）应自包含，不依赖设计态文档。将 9 处对 `core-mechanisms.md` 的外链替换为内联的 §15.11 子代理隔离规则摘要：

- 规则原文约 10 行（4 条强制规则表格），内联成本低
- 保留"重试上限 3 次"和"主代理编排/子代理执行"核心约束
- 删除设计理由和设计者注释（那是设计文档关心的内容）

涉及 5 个 Skill：

| Skill | 引用次数 | 规则上下文 |
|-------|---------|-----------|
| kflow-prototype-design | 3 处 | DESIGN/VERIFY/SELFREV 步骤 |
| kflow-explore | 1 处 | SELFREV 步骤 |
| kflow-design | 2 处 | SELFREV/REVIEW 步骤 |
| kflow-plan | 2 处 | SELFREV/重复制 步骤 |
| kflow-resume | 1 处 | GATE 门控验证归属说明 |

### D4: 版本号同步

版本号同步不等于内容同步。运行时 SKILL.md 可能有新增机制（如子代理隔离规则），但设计文档不需要逐行追平。本次仅：
1. 更新设计文档的 `> **版本**` 行
2. 检查设计文档是否缺少运行时 SKILL.md 的关键机制段落，如有则补充
3. 不追求完全一致——运行时可以有设计文档没有的细枝末节

## Risks / Trade-offs

| 风险 | 缓解措施 |
|------|---------|
| `core-mechanisms.md` 拆分后锚点断裂 | 批量 Grep 定位 + 逐一验证，拆分后运行 Grep 确认无死链 |
| CLAUDE.md 修改引入新不一致 | 修改后与 `docs/designs/skills/index.md` 的工作流链对照验证 |
| 版本号同步后发现内容差异过大 | 仅同步版本号，内容差异记录为后续变更的输入 |
| 拆分后 `core-mechanisms/index.md` 导航过长 | 保持精简，每文件一行链接 + 一句话描述 |
