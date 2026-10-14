# Spec Delta

## REMOVED Requirements

### Requirement: Playwright 全覆盖验证轮次（纯收敛驱动）

**Reason**: Playwright 全覆盖验证的收敛驱动循环被原型 VERIFY 的单轮合并验证取代——导航、Playwright 与 UX 三项验证合并为一轮子代理、一份报告，各自独立的轮次循环不再存在。

**Migration**: Playwright 的 5 项检查项迁移至 `prototype-single-round-verify` 能力的「Playwright 全覆盖检查项（合并报告环节二）」Requirement；不可用降级规则迁移至同能力的「Playwright 不可用降级」Requirement；运行时隔离规则由本能力保留的「playwright 运行时隔离」Requirement 继续承载。

### Requirement: 每轮 Playwright 验证检查项

**Reason**: 该 Requirement 以「每轮」为组织单位。单轮合并验证下不存在轮次概念。

**Migration**: 5 项检查项（页面可达性扫描、按钮/链接全覆盖点击、表单全覆盖、弹窗/抽屉全覆盖、端到端业务流程）内容逐条迁移至 `prototype-single-round-verify` 能力的「Playwright 全覆盖检查项（合并报告环节二）」Requirement，检查内容不变。

### Requirement: Playwright 验证报告内容与存放

**Reason**: 报告路径 `self-reviews/prototype/playwright-check/round-{N}.md` 以轮次编号命名并以独立目录存放。单轮合并验证下由单一合并报告取代。

**Migration**: Playwright 检查结果改为合并报告的「Playwright 全覆盖」分区，报告路径 `self-reviews/prototype/verify-report.md`。见 `prototype-single-round-verify` 能力的「合并报告按环节强制分区」与「合并验证报告存放与读取」Requirement。

### Requirement: Playwright 验证适用审查范围冻结与范围外观察

**Reason**: 该 Requirement 以「每轮审查对象集合」与「SHALL NOT 阻断收敛」为组织口径，属多轮循环语义。单轮合并验证下审查范围一次冻结、适用于四类检查。

**Migration**: 审查范围冻结与范围外观察规则上收至 `prototype-single-round-verify` 能力的「合并验证的审查范围冻结与范围外观察」Requirement。

### Requirement: Playwright 不可用降级

**Reason**: 该 Requirement 的降级判定与安装引导逻辑有效，但其载体（独立的 Playwright 验证环节与独立报告文件）被单轮合并验证取代，报告落点由独立目录改为合并报告的 Playwright 分区。

**Migration**: 安装引导命令、降级为手动文件分析的规则与报告标注要求迁移至 `prototype-single-round-verify` 能力的「Playwright 不可用降级」Requirement；降级记录落点改为合并报告的「Playwright 全覆盖」分区。
