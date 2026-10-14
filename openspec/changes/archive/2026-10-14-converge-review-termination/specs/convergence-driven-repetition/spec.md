# Spec Delta

## Purpose

定义全部多轮审查机制（设计自审 SELFREV、执行类重复制、prototype VERIFY）的统一终止模型：以**见证轮**为唯一成功终止条件，以**审查范围冻结**保证收敛可达，并以不收敛判定与全局安全丝处理不可收敛的情形；取代以轮数上限作为终止依据的档位轮次模型。

## ADDED Requirements

### Requirement: 收敛为唯一成功终止条件

多轮审查循环 SHALL 以**见证轮**为唯一成功终止条件。见证轮定义为同时满足以下四项的一轮审查：(a) 零新发现问题；(b) 零修复、零修改；(c) 审查报告证明全部审查维度与全部审查对象已完成全量遍历；(d) 该轮逐项复核了累积未复核修复清单中的全部条目且全部通过。系统 SHALL NOT 以轮数上限作为终止依据，SHALL NOT 预置审查轮数上限。

#### Scenario: 见证轮达成即终止

- **WHEN** 某轮同时满足零新发现、零修改、报告证明全维全量遍历、且清单内全部条目逐项复核通过
- **THEN** 阶段 SHALL 终止
- **AND** 终止结果 SHALL 记录为 `收敛`

#### Scenario: 任一项不满足则继续

- **WHEN** 本轮存在新发现、或存在修复/修改、或未证明全量遍历、或清单内有条目未通过复核
- **THEN** 系统 SHALL 继续下一轮
- **AND** SHALL NOT 因轮次数量而终止

#### Scenario: 未证明全量遍历的轮次不得判为见证轮

- **WHEN** 某轮报告未证明全部审查维度与全部审查对象已完成全量遍历
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 系统 SHALL 继续下一轮

#### Scenario: 全部档位均不预设轮数上限

- **WHEN** 任一阶段的审查循环启动，无论变更档位为 `轻量`、`标准` 或 `完整`
- **THEN** 系统 SHALL NOT 预置轮数上限
- **AND** 审查轮数 SHALL 由收敛实际发生在第几轮决定

### Requirement: 累积未复核修复清单与复核义务

主 Agent SHALL 维护**累积未复核修复清单**，列出自审查循环开始以来**全部尚未通过独立复核**的修复，并作为轮间摘要的固定字段注入后续轮次。见证轮候选 SHALL 逐项复核该清单内的全部条目，任一项复核不通过（修复失效或引入新问题）时该轮 SHALL NOT 被判定为见证轮。清单为空时 SHALL 记为「（空）」。

#### Scenario: 清单跨轮累加

- **WHEN** 审查循环的第 1 至第 N 轮均产生修复
- **THEN** 累积未复核修复清单 SHALL 包含第 1 至第 N 轮的全部尚未通过独立复核的修复
- **AND** SHALL NOT 仅包含最后一轮的修复

#### Scenario: 复核通过的修复移出清单

- **WHEN** 某轮逐项复核了清单中的若干修复且全部通过
- **THEN** 该批修复 SHALL 从累积未复核修复清单中移除
- **AND** 后续轮次 SHALL NOT 重复复核该批修复

#### Scenario: 清单非空时该轮不构成见证轮

- **WHEN** 本轮零新发现且零修改，但累积未复核修复清单非空且存在未通过复核的条目
- **THEN** 该轮 SHALL NOT 被判定为见证轮
- **AND** 系统 SHALL 继续下一轮

### Requirement: 审查范围冻结

系统 SHALL 在每轮审查开始时由主 Agent 从阶段产物既有内容生成该轮**审查对象集合**并冻结，审查维度 SHALL 限于该阶段既有的固定维度枚举。子代理在轮内 SHALL NOT 扩大审查对象集合、SHALL NOT 新增审查维度、SHALL NOT 借审查之名新增功能点、字段、章节或分支。跨轮审查对象集合 MAY 因阶段输入变化（如回退重执行新增受影响项）而更新，但该更新 SHALL 由主 Agent 执行，SHALL NOT 由子代理自行扩大。

#### Scenario: 审查对象集合冻结

- **WHEN** 主 Agent 构建某轮审查子代理的 prompt
- **THEN** prompt SHALL 包含由阶段产物生成的审查对象清单
- **AND** 子代理 SHALL NOT 审查该清单之外的文件、代码或内容

#### Scenario: 审查维度封闭

- **WHEN** 某轮审查执行
- **THEN** 审查维度 SHALL 限于该阶段固定的维度枚举
- **AND** 子代理 SHALL NOT 新增审查维度

#### Scenario: 轮内不得扩大范围

- **WHEN** 子代理在某轮审查中认为存在值得一并处理的范围外内容
- **THEN** 子代理 SHALL NOT 将其纳入本轮审查对象或修复范围

#### Scenario: 跨轮由主 Agent 更新范围

- **WHEN** 阶段经历回退重执行并产生新的受影响项
- **THEN** 主 Agent SHALL 在后续轮次的审查对象清单中纳入这些受影响项
- **AND** 该更新 SHALL NOT 由子代理自行发起

### Requirement: 范围外发现降级为范围外观察

子代理在冻结范围之外发现的问题 SHALL NOT 在本轮修复、SHALL NOT 计入本轮新发现数、SHALL NOT 阻断收敛；SHALL 记为「**范围外观察**」写入该轮审查报告的「范围外观察」小节。主 Agent SHALL 在阶段终止时汇总范围外观察条目并向用户提示。范围外观察 SHALL NOT 触发对阶段产物的修改。

#### Scenario: 范围外发现不改产物

- **WHEN** 子代理在冻结范围之外发现问题
- **THEN** 系统 SHALL NOT 修改任何阶段产物
- **AND** SHALL NOT 将该问题计为需要修复的项

#### Scenario: 范围外发现不计入发现数

- **WHEN** 某轮仅存在范围外发现而无范围内新发现
- **THEN** 本轮的新发现数 SHALL 记为 0
- **AND** 该轮 MAY 构成见证轮（其余三项条件同时满足时）

#### Scenario: 范围外观察写入报告并由主 Agent 汇总提示

- **WHEN** 某轮产生范围外观察条目
- **THEN** 该轮审查报告 SHALL 在「范围外观察」小节记录这些条目
- **AND** 主 Agent SHALL 在阶段终止时汇总全部范围外观察条目并向用户提示

### Requirement: 引入范围外新内容的轮次不得判为见证轮

某轮引入范围外新内容（审查范围外文件、新增审查维度、新增功能点或章节等）时，该轮 SHALL NOT 被判定为见证轮。主 Agent 在验收时发现越界 SHALL 拒收该轮，并要求子代理在冻结范围内重新审查。

#### Scenario: 越界轮不构成见证轮

- **WHEN** 某轮的新发现或修改落在冻结的审查对象集合之外
- **THEN** 该轮 SHALL NOT 被判定为见证轮

#### Scenario: 主 Agent 拒收越界轮并要求重审

- **WHEN** 主 Agent 验收发现某轮引入范围外新内容
- **THEN** 主 Agent SHALL 拒收该轮
- **AND** SHALL 要求子代理在冻结范围内重新审查该轮
- **AND** SHALL 将越界事实记录到 `docs/skill-suggestion.md`

### Requirement: 不收敛判定与升级

审查循环 SHALL 在出现以下任一情形时判定为不收敛并升级用户，复用非收敛分支（记录 `docs/skill-suggestion.md`、使用 AskUserQuestion 询问用户、MAY 标记 ⚠️ 阻塞）：(a) **无进展**——连续 2 轮「本轮新发现数」不低于其前一轮**且**「累积未复核修复清单长度」不低于其前一轮；(b) **振荡**——同一问题项被「修复 → 重新发现」累计 ≥ 2 次；(c) **安全丝**——该阶段审查轮数达到全局 10 轮。安全丝 SHALL 与变更档位脱钩，SHALL NOT 参与门控或审计判读。

#### Scenario: 无进展触发不收敛升级

- **WHEN** 连续 2 轮的本轮新发现数均不低于其前一轮
- **AND** 同期累积未复核修复清单长度亦均不低于其前一轮
- **THEN** 系统 SHALL 判定为不收敛并升级用户

#### Scenario: 慢收敛不被误伤

- **WHEN** 本轮新发现数与前一轮持平，但累积未复核修复清单长度较前一轮下降
- **THEN** 系统 SHALL NOT 判定为无进展
- **AND** 系统 SHALL 继续下一轮

#### Scenario: 振荡触发不收敛升级

- **WHEN** 同一问题项被「修复 → 重新发现」累计达到 2 次
- **THEN** 系统 SHALL 判定为不收敛并升级用户

#### Scenario: 安全丝触发

- **WHEN** 该阶段审查轮数达到 10 轮且仍未达成见证轮
- **THEN** 系统 SHALL 判定为不收敛并升级用户
- **AND** 该安全丝 SHALL NOT 因变更档位而变化

#### Scenario: 升级复用非收敛分支

- **WHEN** 任一不收敛情形命中
- **THEN** 系统 SHALL 记录到 `docs/skill-suggestion.md`（含阶段、当前轮数、不收敛缘由、覆盖缺口详情、改进建议）
- **AND** SHALL 使用 AskUserQuestion 询问用户是否重新启动审查子代理
- **AND** MAY 将该阶段标记为 ⚠️ 阻塞

### Requirement: 终止结果写入

阶段终止时系统 SHALL 在 `.status.md` 写入**终止结果**字段，取值 `收敛` 或 `未收敛`。`收敛` SHALL 当且仅当该阶段以见证轮终止；`未收敛` SHALL 用于不收敛升级路径。具体缘由（无进展 / 振荡 / 安全丝）SHALL 写入 `docs/skill-suggestion.md`，SHALL NOT 作为终止结果字段的取值。

#### Scenario: 以见证轮终止写入收敛

- **WHEN** 阶段以见证轮终止
- **THEN** 终止结果 SHALL 为 `收敛`

#### Scenario: 不收敛升级写入未收敛

- **WHEN** 阶段因不收敛判定而升级用户
- **THEN** 终止结果 SHALL 为 `未收敛`
- **AND** 具体缘由 SHALL 写入 `docs/skill-suggestion.md`

#### Scenario: 终止结果与实际终止路径一致

- **WHEN** 审计或门控读取终止结果字段
- **THEN** 该取值 SHALL 与该阶段的实际终止路径一致

### Requirement: 档位决定每轮审查强度而非轮数

变更档位 SHALL 决定每轮审查的**审查形态**（`轻量` 单 Agent 串行覆盖全部视角 / `标准` 两视角并行 / `完整` 四视角并行）与产出深度，SHALL NOT 决定审查轮数。全部档位的审查轮数 SHALL 由收敛实际发生在第几轮决定。

#### Scenario: 档位不决定轮数

- **WHEN** 任一阶段的审查循环启动
- **THEN** 系统 SHALL NOT 因变更档位而限制或预置审查轮数

#### Scenario: 档位决定每轮审查强度

- **WHEN** 变更档位为 `轻量`
- **THEN** 每轮审查 SHALL 由单个 Agent 串行覆盖全部视角的检查项
- **AND** 检查项 SHALL NOT 因单 Agent 而缩减

#### Scenario: 档位缺失时的处理

- **WHEN** 变更级 `.status.md` 不含 `变更档位` 字段
- **THEN** 系统 SHALL 按 `完整` 档确定审查形态与产出深度

### Requirement: 全局轮次下限

审查循环 SHALL 执行不少于 1 轮，SHALL NOT 存在 0 轮豁免路径。轻量档 SHALL NOT 豁免审查。kflow-prototype-design 选择「人工审查」审查方式时 SHALL 跳过审查流程，该跳过属流程分支而非 0 轮豁免。

#### Scenario: 下限为 1 轮

- **WHEN** 任一阶段的审查循环启动
- **THEN** 审查轮数 SHALL 不低于 1 轮

#### Scenario: 轻量档无 0 轮豁免

- **WHEN** 变更档位为 `轻量` 且设计类阶段完成产物初稿
- **THEN** 审查 SHALL 执行至少 1 轮
- **AND** SHALL NOT 存在 0 轮豁免路径

#### Scenario: prototype 人工审查跳过审查流程

- **WHEN** kflow-prototype-design 选择「人工审查」审查方式
- **THEN** 系统 SHALL NOT 执行审查流程
- **AND** 该跳过 SHALL NOT 被视为 0 轮豁免

### Requirement: 回退重执行不预置轮数

阶段回退重执行时，系统 SHALL NOT 预置或提高轮数上限，审查轮数 SHALL 同样由收敛决定。验证门控 SHALL 要求受影响项 100% 覆盖：系统 SHALL 从 `.status.md` 「最近修订信息」读取受影响项清单，每个受影响项 SHALL 接受完整的阶段专属验证。

#### Scenario: 回退不预置轮数

- **WHEN** 某执行类阶段因缺陷回退而重执行
- **THEN** 系统 SHALL NOT 因回退而提高或预置轮数上限
- **AND** 审查轮数 SHALL 由收敛决定

#### Scenario: 受影响项 100% 覆盖门控

- **WHEN** 阶段处于回退重执行且 `.status.md` 存在受影响项清单
- **THEN** 每个受影响项 SHALL 接受完整的阶段专属验证
- **AND** 验证结果 SHALL 记录在阶段产物中

### Requirement: 完整档评分并入收敛判据

变更档位为 `完整` 时，每轮审查 SHALL 输出各维度评分（0-10 量纲）。任一维度评分 ≤ 8 时该轮 SHALL 列出对应的具体问题项，使「评分 ≤ 8」等价于「存在新发现」，该轮 SHALL NOT 构成见证轮。系统 SHALL NOT 将评分底线实现为独立于收敛判据的第二套终止条件，SHALL NOT 存在「评分未达标但以轮数上限兜底终止」的路径。

#### Scenario: 评分未达标须列出问题项

- **WHEN** 变更档位为 `完整` 且某轮任一维度评分 ≤ 8
- **THEN** 该轮 SHALL 列出该维度对应的具体问题项
- **AND** 该轮 SHALL NOT 构成见证轮
- **AND** 系统 SHALL 继续下一轮

#### Scenario: 各维度达标且构成见证轮即收敛

- **WHEN** 变更档位为 `完整` 且某轮各维度评分均 > 8 且该轮构成见证轮
- **THEN** 审查 SHALL 以 `收敛` 终止
