# Spec Delta

## MODIFIED Requirements

### Requirement: 审查目录结构分离

系统 SHALL 将自循环审查与交叉审查的记录存储在不同根目录。

#### Scenario: self-reviews 目录
- **WHEN** explore/prototype/design 阶段执行自审
- **THEN** 自审记录保存到 `self-reviews/{phase}/` 目录
- **AND** 文件以时间戳命名 `{YYYYMMDD}-{HHMMSS}.md`

#### Scenario: 轻量档自审记录
- **WHEN** 变更档位为 `轻量`
- **THEN** 自审 SHALL 执行不少于 1 轮（全局下限）并产出 `self-reviews/{phase}/` 记录
- **AND** 审查轮数 SHALL 由收敛实际发生在第几轮决定，SHALL NOT 由变更档位预置轮数上限

#### Scenario: cross-reviews 目录
- **WHEN** kflow-design 执行交叉审查
- **THEN** 审查报告保存到 `cross-reviews/{YYYYMMDD}-{HHMMSS}/` 目录
- **AND** 目录内包含该档位要求的视角审查报告和 synthesis.md

#### Scenario: 两个审查目录不交叉
- **WHEN** 读取审查记录
- **THEN** self-reviews/ 仅含自审记录
- **AND** cross-reviews/ 仅含交叉审查报告
