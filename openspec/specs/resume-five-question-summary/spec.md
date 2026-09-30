# resume-five-question-summary Specification

## Purpose

定义 kflow-resume 设计文档的引用去重规范：恢复工作流与恢复优先级链、调度映射表 SHALL 引用 `skills/kflow-resume/references/recovery-protocol.md`，而非在 `kflow-resume.md` 中内联展开。

## Requirements

### Requirement: Resume workflow references shared recovery protocol

`kflow-resume.md` design doc SHALL reference `skills/kflow-resume/references/recovery-protocol.md` for the recovery priority chain and dispatch mapping table instead of inlining them.

#### Scenario: Resume design doc deduplicated

- **WHEN** `docs/designs/skills/kflow-resume.md` is read after the change
- **THEN** the RESUME WORKFLOW section SHALL reference `skills/kflow-resume/references/recovery-protocol.md` instead of containing the full workflow diagram and priority chain inline

#### Scenario: No reference to the removed centralized directory

- **WHEN** `docs/designs/skills/kflow-resume.md` is read
- **THEN** it SHALL NOT reference `.claude/skills/kflow-shared/recovery-protocol.md` or any other path under a `kflow-shared/` directory
