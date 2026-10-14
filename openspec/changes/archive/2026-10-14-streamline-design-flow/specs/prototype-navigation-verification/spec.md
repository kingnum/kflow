# Spec Delta

## REMOVED Requirements

### Requirement: 导航合理性验证轮次（纯收敛驱动）

**Reason**: 导航合理性验证的收敛驱动循环被原型 VERIFY 的单轮合并验证取代——导航、Playwright 与 UX 三项验证合并为一轮子代理、一份报告，各自独立的轮次循环不再存在，见证轮四项判据在该环节失去载体。

**Migration**: 导航合理性的 5 项检查项迁移至 `prototype-single-round-verify` 能力的「导航合理性检查项（合并报告环节一）」Requirement，在合并验证的单轮内执行。审查方式为「人工审查」时跳过该验证的规则迁移至同能力的「原型 VERIFY 单轮合并验证」Requirement。

### Requirement: 每轮导航验证检查项

**Reason**: 该 Requirement 以「每轮」为组织单位。单轮合并验证下不存在轮次概念。

**Migration**: 5 项检查项（页面可达性、返回/取消按钮合理性、表单切换链、弹窗/抽屉导航、跨页面流程闭环）内容逐条迁移至 `prototype-single-round-verify` 能力的「导航合理性检查项（合并报告环节一）」Requirement，检查内容不变。

### Requirement: 导航验证报告内容与存放

**Reason**: 报告路径 `self-reviews/prototype/nav-check/round-{N}.md` 以轮次编号命名并以独立目录存放。单轮合并验证下由单一合并报告取代。

**Migration**: 导航检查结果改为合并报告的「导航合理性」分区，报告路径 `self-reviews/prototype/verify-report.md`。见 `prototype-single-round-verify` 能力的「合并报告按环节强制分区」与「合并验证报告存放与读取」Requirement。

### Requirement: 导航验证适用审查范围冻结与范围外观察

**Reason**: 该 Requirement 以「每轮审查对象集合」与「SHALL NOT 阻断收敛」为组织口径，属多轮循环语义。单轮合并验证下审查范围一次冻结、适用于四类检查。

**Migration**: 审查范围冻结与范围外观察规则上收至 `prototype-single-round-verify` 能力的「合并验证的审查范围冻结与范围外观察」Requirement。
