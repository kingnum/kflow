# 归档规则规范

> **版本**: 1.1.0
> **来源**: core-mechanisms/04-gates-and-transitions.md §6.3, §6.3.1, §6.4, §6.7
> **适用范围**: kflow-archive Skill
> **加载层级**: 归档层
> **适用阶段**: archive
>
> **v1.1.0**: 归档条件接受有声明依据的裁剪阶段（轻量档），无依据的 `⏭️` 阻塞归档并提示缺失裁剪依据。


## 1. 归档条件检查清单

```markdown
归档前检查:
- [ ] 主变更 .status.md 中所有阶段标记完成（✅ 完成 或 ⏭️ 跳过 或 ⏭️ 不适用且有适用性声明依据）
- [ ] 所有子变更各阶段（计划、编码、代码审查、接口单元测试、E2E测试）完成 或 已按轻量档适用性声明裁剪
- [ ] 前后端项目：所有子变更 E2E测试和接口单元测试通过
- [ ] 纯后端项目：所有子变更接口单元测试通过
- [ ] 集成测试通过（test-reports/integration/summary.md 存在且标记"集成测试通过"；集成测试阶段被合法裁剪时视为满足，SHALL NOT 要求该文件存在）
- [ ] 审计门控通过（kflow-audit 七维度评估通过，无阻塞问题）
- [ ] 无遗留的阻碍记录
- [ ] 用户确认归档
- [ ] 裁剪阶段合法：标记 `⏭️ 不适用` 的阶段均在变更级 .status.md 的「阶段适用性声明」区有对应判定依据（有依据的裁剪视为门控满足，无依据的 `⏭️` 阻塞并提示缺失裁剪依据）

归档操作:
- 将变更目录整体移至 docs/changes/archive/{YYYY-MM-DD}-{change}/
- 保留所有子变更结构和文档
- 更新 docs/changes/index.md 归档记录
- 执行设计合并：提取 functional-designs/ + detailed-design.md 关键内容
- 合并功能设计到产品级文档 docs/designs/functional-designs/（前后端：按一级菜单目录 {menu}/index.md + part-NN.md；纯后端：按设计域文件 {domain}.md）
- 合并详细设计到产品级文档 docs/designs/detailed-designs/*.md（6 文件体系：含 config-items.md 和 error-handling.md）
- 登记原型改动到产品级原型清单 docs/designs/prototypes/manifest.md（仅当原型设计阶段非跳过；不做文件级原型合并）
- 标注来源变更和归档时间
- 首次合并时检测草稿标记（「由 AI 逆向分析生成」），执行去草稿替换
- 更新 docs/designs/changelog.md（如有新模块或结构变更）
```

### 1.1 裁剪阶段的归档处理

裁剪 SHALL 仅适用于变更档位为 `轻量` 的变更；`标准` 与 `完整` 档的归档条件维持既有规则，纯后端项目跳过 E2E测试的既有规则不受影响。

| 落点 | 处理 |
|------|------|
| 接受有声明依据的裁剪 | 某阶段标记 `⏭️ 不适用` 且变更级 `.status.md` 的「阶段适用性声明」区存在对应判定依据时，归档门控 SHALL 视为满足，SHALL NOT 因该阶段无产物而阻塞 |
| 无声明依据的 `⏭️` | SHALL 阻塞归档，并提示缺失裁剪依据。本项仅约束声称由变更档位裁剪产生的 `⏭️`；由项目类型产生的 `⏭️`（纯后端项目的 E2E测试阶段与 E2E测试列）依据项目类型判定、与档位无关，不要求声明依据 |
| 集成测试门控 | 集成测试阶段被合法裁剪时视为满足，SHALL NOT 要求 `test-reports/integration/summary.md` 存在 |
| 归档前最终覆盖检查 | `traceability.md` 中具有声明依据的 `⏭️ 不适用` 列视为满足，SHALL NOT 参与覆盖率判定、SHALL NOT 产生缺口记录 |
| 覆盖率分母 | 裁剪列 SHALL 整列填 `⏭️`，覆盖率 = 已填充格数 / (总格数 - 不适用格数) |

> 判定规则见 [core-mechanisms/04-gates-and-transitions.md §5.4](../../../docs/designs/core-mechanisms/04-gates-and-transitions.md)，声明字段定义见 kflow-design 的 `references/state-values.md` §5。

## 2. 设计合并流程

```
归档时设计合并流程:

┌─────────────────────────────────────────────────────────────┐
│                  DESIGN MERGE WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│  1. EXTRACT   → 从变更级文档提取设计内容                      │
│  │   ├── functional-designs/ 的功能设计章节                  │
│  │   └── detailed-design.md 的详细设计章节（含配置项、错误处理） │
│  2. MATCH     → 匹配合并目标产品级文档                        │
│  │   ├── 前后端：已存在 docs/designs/functional-designs/{menu}/ → 按 FP-ID 合并到 part-NN.md │
│  │   ├── 前后端：不存在 → 新建 {menu}/index.md + part-01.md     │
│  │   ├── 纯后端：匹配 docs/designs/functional-designs/{domain}.md │
│  │   ├── 检测草稿标记（「由 AI 逆向分析生成」）→ 首次合并去草稿  │
│  │   └── 模块归属模糊 → AskUserQuestion 确认模块归属           │
│  3. MERGE     → 按功能模块合并内容（更新 index.md 分册总览）   │
│  │   ├── 功能设计 → 合并到功能模块文档对应章节（按 FP-ID 匹配） │
│  │   ├── 详细设计 → 按类型更新 detailed-designs/*.md         │
│  │   ├── 首次合并 → 替换草稿标记为正式来源标注                 │
│  │   ├── NFR 变更 → 更新 docs/designs/detailed-designs/nfr-baseline.md  │
│  │   └── 数据模型变更 → 更新 docs/designs/detailed-designs/data-model.md │
│  4. ANNOTATE  → 标注来源信息                                  │
│  │   └── 每章节标注: > 来源变更: {change-name} | 归档时间: {date} │
│  5. CONFLICT  → 冲突检测与处理                                │
│  │   ├── 默认策略: 替换更新（新设计覆盖旧设计）                │
│  │   ├── 保留旧版本链接                                       │
│  │   ├── 结构性冲突: AskUserQuestion 人工裁决                  │
│  │   │   ├── 同一数据实体字段定义不一致（类型/约束冲突）       │
│  │   │   ├── 同一接口路径方法签名不兼容                       │
│  │   │   ├── 同一功能点被不同变更以互斥方式修改               │
│  │   │   └── 架构层级设计决策发生根本性变更                   │
│  │   └── 内容级冲突（默认策略）: 替换更新，旧版本软链接保留    │
│  6. CHANGELOG → 更新 docs/designs/changelog.md                │
│  7. REGISTER  → 登记原型改动到产品级原型清单                  │
│  │   ├── 原型设计阶段为 ⏭️ 跳过 → 跳过本步                     │
│  │   ├── 读取变更级 prototype-changes.md 的改动清单            │
│  │   ├── 更新 docs/designs/prototypes/manifest.md:            │
│  │   │   ├── 受影响产物的「来源变更」列                        │
│  │   │   ├── 清单版本号与「修订记录」追加一条                  │
│  │   │   └── 最后更新时间                                     │
│  │   └── SHALL NOT 复制或覆盖 docs/designs/prototypes/ 下文件  │
│  8. COMPLETE  → 合并完成，继续目录移动操作                     │
└─────────────────────────────────────────────────────────────┘

注意: 原型产物已在原型设计阶段直写产品级 docs/designs/prototypes/，归档不做文件级原型合并，仅登记改动到 docs/designs/prototypes/manifest.md。变更级 prototype-backup/ 随变更目录进 archive/ 保留。
```

## 3. 归档后禁止操作

已归档的变更禁止任何修改操作：
- 禁止继续已归档的变更
- 禁止修改已归档变更下的任何文件
- 如需继续工作，应创建新变更

## 4. Archive 禁止自动流转

归档阶段 SHALL NOT 被任何前置阶段自动调度进入。审计（kflow-audit）通过后，MUST 通过 AskUserQuestion 获取用户显式确认后方可进入归档阶段。Archive 是 KFlow 体系中唯一禁止自动流转的阶段。

```
归档阶段入口门控:

audit 完成 → 输出审计摘要
    │
    ├── AskUserQuestion: "审计已通过，是否进入归档阶段？"
    │   ├── "确认归档" → 进入 kflow-archive
    │   ├── "暂时不归档" → 变更保持在 audit 完成状态
    │   └── "需要进一步验证" → 用户手动验证后自行调用 kflow-archive
    │
    └── 禁止行为:
        ├── 禁止 audit 阶段自动调度 kflow-archive
        ├── 禁止其他阶段以"流程完成"为由自动进入归档
        └── 违反规则 → 视为 Stage Boundary Enforcement 违规
```
