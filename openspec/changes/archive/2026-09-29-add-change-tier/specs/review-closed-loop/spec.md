# Spec Delta

## ADDED Requirements

### Requirement: 交叉审查结果按批次独立存储

系统 SHALL 将每次交叉审查（包括初次审查和分级重审）的结果保存到独立的时间戳目录，目录内视角报告数量按变更档位确定。

#### Scenario: 初次交叉审查

- **WHEN** design 自审完成后首次执行交叉审查
- **THEN** 创建 `cross-reviews/{timestamp}/` 目录
- **AND** 目录包含该档位要求的视角报告与 synthesis.md（完整档四份视角报告、标准档两份视角报告、轻量档仅 synthesis.md）

#### Scenario: 分级重审

- **WHEN** 变更档位为 `标准` 或 `完整` 且高严重度问题修复后需要重新审查
- **THEN** 创建新的 `cross-reviews/{timestamp}/` 目录
- **AND** 仅包含需要重审的视角报告（如原视角+安全视角）和 synthesis.md

#### Scenario: 审查批次索引

- **WHEN** synthesis.md 生成或更新
- **THEN** 包含"审查批次"章节

## MODIFIED Requirements

### Requirement: 审查问题分级验证

系统 SHALL 按问题严重度分级执行修复后的验证。变更档位为 `轻量` 时，系统 SHALL 改为执行单轮复检。

#### Scenario: 轻量档单轮复检

- **WHEN** 变更档位为 `轻量` 且存在问题标记为"已修复"
- **THEN** 系统 SHALL 执行单轮复检，复核全部已修复问题
- **AND** SHALL NOT 执行按高/中/低严重度分级的差异化重审

#### Scenario: 高严重度问题验证

- **WHEN** 变更档位为 `标准` 或 `完整` 且存在高严重度问题
- **THEN** 执行重新审查，原审查视角 + 安全视角交叉检查
- **AND** 验证修复方案正确且未引入新的高/中严重度问题

#### Scenario: 中严重度问题验证

- **WHEN** 变更档位为 `标准` 或 `完整` 且存在中严重度问题
- **THEN** 执行重新审查，原审查视角
- **AND** 验证修复方案正确且未引入新的高严重度问题

#### Scenario: 低严重度问题验证

- **WHEN** 变更档位为 `标准` 或 `完整` 且存在低严重度问题
- **THEN** 随机抽取 30% 问题执行重新审查
- **AND** 可人工确认替代自动抽查

### Requirement: 审查关闭条件

系统 SHALL 定义审查综合报告的关闭条件，关闭条件按变更档位分支。

#### Scenario: 轻量档审查可关闭

- **WHEN** 变更档位为 `轻量`
- **AND** 所有高严重度问题已修复并通过单轮复检
- **AND** 所有中严重度问题已修复并通过单轮复检
- **THEN** 综合报告最终状态标记为 ✅ 关闭
- **AND** 详细设计阶段可以标记完成

#### Scenario: 审查可关闭

- **WHEN** 变更档位为 `标准` 或 `完整`
- **AND** 所有高/中严重度问题：修复 + 重审通过
- **AND** 所有低严重度问题：至少 30% 抽查通过
- **THEN** 综合报告最终状态标记为 ✅ 关闭
- **AND** 详细设计阶段可以标记完成

#### Scenario: 审查不可关闭

- **WHEN** 仍有高/中严重度问题未通过重新审查或单轮复检
- **THEN** 综合报告状态保持为 🔄 进行中
- **AND** 详细设计阶段保持 ❌ 阻塞

### Requirement: 审查目录结构分离

系统 SHALL 将自循环审查与交叉审查的记录存储在不同根目录。

#### Scenario: self-reviews 目录

- **WHEN** explore/prototype/design 阶段执行自审 且 目标轮次大于 0
- **THEN** 自审记录保存到 `self-reviews/{phase}/` 目录
- **AND** 文件以时间戳命名 `{YYYYMMDD}-{HHMMSS}.md`

#### Scenario: 轻量档不产生自审记录

- **WHEN** 变更档位为 `轻量`（自审目标轮次为 0）
- **THEN** `self-reviews/{phase}/` 目录 SHALL NOT 创建
- **AND** 审计 SHALL NOT 因缺少自审记录判定为缺项

#### Scenario: cross-reviews 目录

- **WHEN** kflow-design 执行交叉审查
- **THEN** 审查报告保存到 `cross-reviews/{YYYYMMDD}-{HHMMSS}/` 目录
- **AND** 目录内包含该档位要求的视角审查报告和 synthesis.md

#### Scenario: 两个审查目录不交叉

- **WHEN** 读取审查记录
- **THEN** self-reviews/ 仅含自审记录
- **AND** cross-reviews/ 仅含交叉审查报告

## REMOVED Requirements

### Requirement: 四视角审查结果按批次独立存储

**Reason**: 交叉审查的视角报告数量改由变更档位决定（完整档四份、标准档两份、轻量档一份综合报告），原需求硬编码四份视角报告，与轻量档和标准档的审查形态冲突。

**Migration**: 改由本能力新增的「交叉审查结果按批次独立存储」承担，按批次独立存储与审查批次索引机制保持不变，仅视角报告数量改为按档位确定。
