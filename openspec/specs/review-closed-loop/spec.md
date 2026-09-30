## Purpose

定义四视角交叉审查的闭环机制，包括审查问题分级验证、问题追踪矩阵、审查关闭条件，以及 self-reviews/ 和 cross-reviews/ 目录分离和批次独立存储规则。
## Requirements
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

### Requirement: 审查问题追踪矩阵

系统 SHALL 在审查综合报告 (synthesis.md) 中维护问题追踪矩阵，并增加审查批次索引。

#### Scenario: 追踪矩阵内容
- **WHEN** synthesis.md 生成或更新
- **THEN** 问题追踪矩阵包含每个问题的 ID、fingerprint、严重度、类别、描述、发现者、修复状态、验证结果、最终状态

#### Scenario: 修复验证轮次记录
- **WHEN** 问题修复后验证
- **THEN** 记录验证批次（对应 cross-reviews/{timestamp}/ 目录）、验证方式、验证结果
- **AND** 修复引入新问题时进入下一批次验证

#### Scenario: 审查批次索引
- **WHEN** synthesis.md 首次生成
- **THEN** 包含审查批次表格（批次序号、目录路径、审查原因、审查时间、涉及视角）
- **AND** 每次分级重审时追加批次记录

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

