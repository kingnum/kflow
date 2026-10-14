# Spec Delta

## REMOVED Requirements

### Requirement: 轮次上限模型与全局下限

**Reason**: 「全局下限 + 档位上限」的轮次模型被收敛驱动模型取代——审查轮数不再由档位决定，上限不再是终止依据（上限只在循环不收敛时生效，且现行参数使「预算内收敛」成为少数派）。

**Migration**: 全局轮次下限（≥1 轮，无 0 轮豁免）保留并迁移至 `convergence-driven-repetition` 能力的「全局轮次下限」Requirement；档位上限全部删除，轮数由收敛实际发生在第几轮决定。

### Requirement: 收敛终止条件

**Reason**: 原收敛终止条件为「见证轮 或 执行轮次 = 轮次上限」的二元结构，并配套复检轮与三值终止原因。上限废除后，二元结构塌为单一条件，复检轮的复核义务（原第 4 项判据）并入见证轮定义本身。

**Migration**: 迁移至 `convergence-driven-repetition` 能力的「收敛为唯一成功终止条件」Requirement——见证轮扩为 4 项（三个原条件 + 清单逐项复核通过）；终止结果由三值改二值（`收敛` / `未收敛`）；不收敛的兜底改由该能力的「不收敛判定与升级」Requirement 承载。

### Requirement: 执行类阶段轮次上限按档位决定

**Reason**: 执行类阶段（编码/代码审查/接口单元测试/E2E测试/集成测试/缺陷修复）的轮次上限按档位取 1/3/5 的规定废除——档位不再决定轮数。

**Migration**: 执行类阶段改用 `convergence-driven-repetition` 的收敛终止模型；档位仅决定每轮审查强度。kflow-plan 阶段取设计自审口径的例外条款一并失效（该阶段同口径）。

### Requirement: 设计自审轮次上限按档位决定

**Reason**: 设计类阶段（kflow-explore / kflow-prototype-design / kflow-design）SELFREV 轮次上限按档位取 1/2/5 的规定废除。

**Migration**: 设计自审改用 `convergence-driven-repetition` 的收敛终止模型。原 Requirement 中「prototype 选择人工审查时跳过自审」的规定保留，迁移至该能力的「全局轮次下限」Requirement（作为流程分支而非 0 轮豁免）；档位与审查形态的对应关系由 `design-review-tiering` 继续承载。

### Requirement: 废除首次一律最大的轮次下限

**Reason**: 该 Requirement 的立法目的是禁止以「首次执行/首次创建」作为轮次依据。收敛驱动模型下轮数由收敛决定，不存在任何轮次依据，该禁令的前提已消失。

**Migration**: 无需迁移——收敛模型中不存在「轮次下限随首次执行而抬高」的可能，任何以项目历史或执行次数决定轮次的规则一并失效。

### Requirement: 回退重执行的轮次上限叠加规则

**Reason**: `max(档位上限, 影响范围分数映射)` 的叠加规则以上限存在为前提；上限废除后该规则无对象。

**Migration**: 回退重执行不再预置或提高轮数，迁移至 `convergence-driven-repetition` 的「回退重执行不预置轮数」Requirement；影响范围分数本身保留，用于验证门控的「受影响项 100% 覆盖」。

### Requirement: 统一轮次映射口径

**Reason**: 影响范围分数到轮次的映射表（≤3→1 / 4~15→3 / >15→5）仅用于抬高上限，随上限一并废除。

**Migration**: 删除映射表；`triage-impact-assessment` 的「影响评分 → 重复制轮次」映射要求同步移除，影响评分本身保留。

### Requirement: 完整档自审评分底线

**Reason**: 原规则「各维度评分 > 8 **且**达成收敛，或达上限 5」在无上限模型下会让评分卡在 ≤8 的循环永不终止；且「零发现但评分 ≤8」在语义上自洽，构成独立的死循环源。

**Migration**: 迁移为 `convergence-driven-repetition` 的「完整档评分并入收敛判据」Requirement——评分 ≤8 时须列出具体问题项，使「评分 ≤8」等价于「存在新发现」，从而内化为收敛判据的一部分；不再存在独立于收敛的第二套终止条件与上限兜底。

### Requirement: 轻量档一轮自审与产物门控

**Reason**: 「轻量档执行 1 轮」的轮次规定随档位上限废除；产物门控部分并非轮次规则，只是借该 Requirement 承载。

**Migration**: 一轮下限由 `convergence-driven-repetition` 的「全局轮次下限」承载（轻量档不豁免、无 0 轮豁免路径）；产物存在性与占位符门控保留为各阶段的既有硬门（`phase-artifact-verification` 与各阶段 `references/gates.md`），不受本变更影响。

### Requirement: 目标轮次写入状态文件

**Reason**: `.status.md` 执行轮次字段的分母来自档位轮次上限，随上限废除而失去含义。

**Migration**: 迁移为 `round-counter` 能力的 `{N} 轮` 格式（仅分子，下限 1 轮）；读取侧对历史 `{N} / {上限}` 形式忽略分母处理。
