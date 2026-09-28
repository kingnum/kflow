## Purpose

钉死归档目录位置为 `docs/changes/archive/`，统一归档移动、归档检测与活跃变更扫描排除规则，消除归档路径在 status/resume 检测逻辑与文档表述之间的错位。

## Requirements

### Requirement: 归档目录位置

系统 SHALL 将归档目录定义为 `docs/changes/archive/{YYYY-MM-DD}-{change}/`。

#### Scenario: 归档目录路径
- **WHEN** 归档一个变更
- **THEN** 变更目录 SHALL 移动至 `docs/changes/archive/{YYYY-MM-DD}-{change}/`

### Requirement: 归档移动与索引更新

kflow-archive 归档时 SHALL 将变更目录整体移动至归档目录，并在 `docs/changes/index.md` 的归档列表中记录归档路径。

#### Scenario: 归档移动
- **WHEN** kflow-archive 执行归档 MOVE 步骤
- **THEN** 变更目录 SHALL 整体移动至 `docs/changes/archive/{YYYY-MM-DD}-{change}/`

#### Scenario: 归档索引记录
- **WHEN** 归档完成
- **THEN** `docs/changes/index.md` 的归档列表 SHALL 记录指向 `docs/changes/archive/{YYYY-MM-DD}-{change}/` 的路径

### Requirement: 活跃变更扫描排除归档目录

kflow-status/kflow-guide/kflow-init SHALL 在扫描活跃变更时排除 `docs/changes/archive/` 子目录。

#### Scenario: status 扫描排除
- **WHEN** kflow-status 扫描 `docs/changes/` 下的变更
- **THEN** SHALL 排除 `docs/changes/archive/` 子目录
- **AND** 已归档变更 SHALL NOT 出现在活跃变更列表

#### Scenario: guide 与 init 扫描排除
- **WHEN** kflow-guide 或 kflow-init 扫描活跃变更
- **THEN** SHALL 排除 `docs/changes/archive/` 下的变更

### Requirement: 归档检测路径

kflow-resume SHALL 通过 `docs/changes/archive/` 路径检测变更是否已归档。

#### Scenario: 已归档变更检测
- **WHEN** kflow-resume 恢复一个变更
- **THEN** SHALL 通过 `docs/changes/archive/*/{change}/` 或 `docs/changes/archive/*-{change}/` 路径检测是否已归档
- **AND** 已归档变更 SHALL 报错「变更已归档，无法恢复」
