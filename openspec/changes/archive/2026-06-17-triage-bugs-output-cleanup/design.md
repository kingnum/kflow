# Design: triage-bugs-output-cleanup

## Context

`bugs/` 目录是变更级问题追踪的唯一载体，设计由 `kflow-bug-triage` 维护。实际运行中，目录产出严重偏离设计规范：

**现状**：
1. **分页文件命名**：规范要求 `bug-001-020.md`（每文件 ≤20 条），实际产出如 `bug-001-005.md`、`bug-005-008.md`（命名语义不明，每次登记都新建文件）
2. **BUG-ID 前缀**：规范定义 `BUG-{NNN}` 为序号，但实际使用中混入严重度前缀（`B-001`、`W-001`、`S-001`），导致 index.md 与详情文件的 ID 不一致
3. **fix-report 位置**：`kflow-bug-fix` 的修复报告按设计应在子变更目录 `subchanges/{sc}/test-reports/fix-reports/`，但 A 路径（用户反馈 → triage → L4 → bug-fix）没有子变更上下文，实际被放到了 `bugs/` 下，与 triage 产出混在一起
4. **模板不遵循**：实际详情文件缺少 frontmatter、基本信息表格、处理状态 checkbox、关联节等必填内容

**约束**：
- bugs/ 目录归 `kflow-bug-triage` 维护
- fix-report 归 `kflow-bug-fix` 产出
- 两个 Skill 的产出需要在同一处（bug 详情）汇合，但不能互相覆盖对方的内容

## Goals / Non-Goals

**Goals:**
- 明确 fix-report 在不同路径（A/B）的存放规则，消除 bugs/ 目录归属混乱
- 强化分页规则：追加优先、满额新建，文件名统一为 `bug-{start}-{end}.md`
- 统一 BUG-ID 为纯序号 `BUG-{NNN}`，严重度独立字段
- 精简问题详情模板，SKILL.md 增加硬约束确保遵循

**Non-Goals:**
- 不重构 `kflow-bug-fix` 的核心修复流程（二分法、10轮迭代、3次上限）
- 不修改 `kflow-bug-triage` 的四层诊断逻辑
- 不强制迁移已存在的 bugs/ 目录（测试项目的历史文件），仅在下次 triage 时自然对齐新规范

## Decisions

### D1: fix-report 双路径存放策略

**决定**：A 路径（用户反馈 → bug-fix）的修复记录回写到 `bugs/bug-NNN-NNN.md`；B 路径（测试发现 → bug-fix）的 fix-report 保持在 `subchanges/{sc}/test-reports/fix-reports/`。

**理由**：
- A 路径的入口来自 triage，没有子变更上下文，fix-report 在子变更目录无处安放；将修复记录合并到 bug 详情中，一个问题一个文件即可见完整生命周期
- B 路径的入口来自测试阶段，有明确的子变更上下文，fix-report 与测试轮次报告同目录便于追溯；且 B 路径可能同时修复多个 bug，fix-report 按批次产出更合理
- 若 B 路径修复的 bug 同时已在 bugs/ 登记，则同步在 bugs/ 详情中追加修复记录做关联

**替代方案**：
- 所有 fix-report 放在 bugs/ 下：违反设计文档定义的职责边界（bugs/ 归 triage）
- 所有 fix-report 放在子变更目录：A 路径没有子变更上下文，路径不存在

### D2: bug 详情中新增「修复记录」节

**决定**：在问题详情模板的「处理状态」和「关联」节之间，新增「修复记录」节（占位，由 bug-fix 回写）。

**修复记录节内容**：
```markdown
### 修复记录

| 字段 | 值 |
|------|---|
| 修复日期 | {YYYY-MM-DD} |
| 根因分类 | {实现错误 / 测试错误} |
| 修复文件 | {逗号分隔的文件路径} |
| 验证结果 | {✅ 通过 / ❌ 失败} |

**修复内容**:
{修复的具体变更}

**Post-mortem**:
{什么可以防止此类缺陷}
```

**理由**：
- 节结构按问题生命周期排列：基本信息 → 问题描述 → 诊断结果 → 解决方案 → 处理状态 → 修复记录 → 关联
- 修复记录节在 triage 登记时留空（占位），bug-fix 完成后填写，职责清晰
- Post-mortem 从 fix-report 的独立节变成 bug 详情内的子内容，与具体 bug 绑定

**替代方案**：
- 保持 Post-mortem 在分页文件末尾汇总：跨 bug 的 Post-mortem 与单个 bug 的修复记录割裂，难以追溯

### D3: BUG-ID 去前缀

**决定**：BUG-ID 改为纯序号 `BUG-{NNN}`，严重度用独立字段 `🔴/🟡/🔵` 表示。

**理由**：
- 严重度会随处理过程变化（如降级/升级），编码到 ID 中会产生不一致
- 前缀与序号混用是当前 ID 混乱的直接原因（index.md 用 `B-001`，详情文件写 `BUG-ID: W-001`）
- 纯序号稳定，不受严重度变化影响，也便于排序和引用

**变更点**：
- `kflow-bug-triage.md` 严重度分级表去掉「编号前缀」列
- `bug-registration` spec 中 BUG-ID 相关描述更新
- `bugs-index.md` 和 `bugs-detail.md` 模板更新
- `kflow-bug-triage/SKILL.md` 严重度表更新

### D4: 分页规则强化方式

**决定**：在 SKILL.md 的 REGISTER 步骤增加明确约束（不是建议），并在 spec 中强化场景。

**约束措辞**：
- SKILL.md REGISTER 步骤：`SHALL 追加到当前分页文件，SHALL NOT 每次登记创建新文件`
- spec：`系统 SHALL 在登记新问题时追加到当前分页文件末尾；仅当当前分页文件已满 20 条时，SHALL 创建新分页文件`

**理由**：当前 spec 虽然有「单个文件上限」场景，但没有明确「追加优先」；SKILL.md 的执行流程只是提到「创建/更新」，没有强调 SHALL NOT 新建文件

### D5: 模板精简范围

**决定**：去掉 frontmatter 中的 `stage`、`skill`、`template_for`（仅保留版本和创建时间），去掉无实际业务意义的字段；保留并强化有业务价值的节（基本信息、问题描述、诊断结果、解决方案、处理状态、修复记录、关联）。

**SKILL.md 硬约束**：在 REGISTER 步骤列出必填节清单，使用 `SHALL 按以下节的顺序输出，SHALL NOT 省略任何节` 格式，而非"参考模板"。

## Risks / Trade-offs

**[风险] A 路径 bug-fix 写 bugs/ 目录违反职责边界**
→ 通过 spec 明确约束：bug-fix 仅允许写入「修复记录」节（追加），不允许修改 triage 登记的其他节（诊断结果、解决方案等）。两个 Skill 写入同一文件的不同节，职责通过「节级锁定」而非「文件级锁定」实现。

**[风险] 去前缀后严重度不可见**
→ 在 index.md 和详情文件的基本信息表格中，严重度作为独立列/字段使用 emoji + 文字（`🔴 阻塞`、`🟡 警告`、`🔵 建议`），视觉上同样清晰，但不编码到 ID。

**[风险] 已有测试项目的历史 bugs/ 文件与新规范不一致**
→ 不在本次变更中强制迁移。规范生效时机：下次 triage 登记新 bug 时，按新规范操作；历史 fix-report 文件保留不动，不影响功能。

**[Trade-off] Post-mortem 从跨 bug 汇总改为单 bug 绑定**
→ 失去了跨 bug 的 Post-mortem 视角，但获得了每个 bug 完整生命周期的可追溯性。跨 bug 的改进建议汇总职责转移到 `kflow-audit`（读取所有 bug 详情中的 Post-mortem 节）。

## Migration Plan

不涉及代码迁移。变更范围是设计文档、模板、运行时 Skill、specs。

**生效时机**：
- 归档完成后立即生效
- 下一次 kflow-bug-triage 执行时按新规范产出
- 已有的历史 bugs/ 目录文件不强制迁移

## Open Questions

无。方案已在 explore 阶段与用户确认完毕。
