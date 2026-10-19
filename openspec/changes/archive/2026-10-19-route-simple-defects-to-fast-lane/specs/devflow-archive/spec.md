# Spec Delta

## ADDED Requirements

### Requirement: 项目级阻塞缺陷归档门控

归档门控 SHALL 读取项目级缺陷工作区 `docs/bugs/index.md`，并将未关闭的 🔴 阻塞级缺陷纳入归档条件。

#### Scenario: 存在未关闭的项目级阻塞缺陷

- **WHEN** 尝试进入归档阶段
- **AND** `docs/bugs/index.md` 存在未关闭的 🔴 阻塞级缺陷
- **THEN** 归档门控 SHALL 阻塞归档
- **AND** SHALL 输出阻塞缺陷清单（BUG-ID、标题、状态、详情文件）

#### Scenario: 项目级缺陷工作区不存在

- **WHEN** 尝试进入归档阶段
- **AND** `docs/bugs/index.md` 不存在
- **THEN** 归档门控 SHALL 视为该项目级门控满足
- **AND** SHALL NOT 因缺少该文件而阻塞归档

#### Scenario: 项目级无阻塞缺陷

- **WHEN** 尝试进入归档阶段
- **AND** `docs/bugs/index.md` 中不存在未关闭的 🔴 阻塞级缺陷
- **THEN** 归档门控 SHALL 视为该项目级门控满足
- **AND** 🟡 警告与 🔵 建议级缺陷 SHALL NOT 阻塞归档
