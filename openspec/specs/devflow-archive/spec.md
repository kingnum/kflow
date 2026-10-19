# devflow-archive Specification

## Purpose

本能力定义 KFlow 归档阶段的条件判定与设计合并流程，规定归档条件与设计合并的单一权威定义位置，并要求归档时生成模块摘要产物，供后续变更按需加载。

## Requirements

### Requirement: Archive conditions and design merge single source with summary generation
The core definition of archive conditions and design merge workflow SHALL reside in `skills/kflow-archive/references/archive-rules.md`. `04-gates-and-transitions.md` §6.3-6.3.1 SHALL be replaced with references. Archive phase SHALL include a summary generation step (step 5.6 SUMMARY) after design merge, outputting `module-summary.md`.

#### Scenario: Core mechanism doc archive sections simplified

- **WHEN** `04-gates-and-transitions.md` §6.3 is read after the change
- **THEN** it SHALL reference the per-skill archive rules file (`kflow-archive` 的 `references/archive-rules.md`) as the location of the full specification
- **THEN** the full archive checklist and design merge workflow SHALL NOT appear in `04-gates-and-transitions.md`
- **THEN** it SHALL NOT reference any path under a `kflow-shared/` directory
- **AND** the referenced path SHALL resolve to an existing file in the repository

#### Scenario: Archive includes summary generation step

- **WHEN** `kflow-archive` SKILL.md execution flow is read
- **THEN** it SHALL contain a step 5.6 SUMMARY for generating/updating `module-summary.md` after design merge

#### Scenario: Output artifacts table updated

- **WHEN** archive output artifacts table is read
- **THEN** it SHALL include `module-summary.md` as an output artifact entry

#### Scenario: Archive conditions source is the per-skill reference file

- **WHEN** the archive condition checklist is needed
- **THEN** it SHALL be read from `skills/kflow-archive/references/archive-rules.md` (dev) or `.claude/skills/kflow-archive/references/archive-rules.md` (consumer)
- **AND** the read SHALL NOT depend on a `kflow-shared/` directory existing at any project root

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
