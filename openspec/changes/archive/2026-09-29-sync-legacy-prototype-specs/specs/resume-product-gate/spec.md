## MODIFIED Requirements

### Requirement: 验证项映射表

系统 SHALL 根据当前阶段映射对应的产物验证项。

#### Scenario: 阶段到产物验证映射

- **WHEN** 系统执行产物验证
- **THEN** 系统 SHALL 使用以下映射：

| 阶段 | 验证项 |
|------|--------|
| 编码 | 执行轮次=10/10 + traceability 编码列=100% + 无占位符 |
| 代码审查 | code-review.md 存在 + 审查通过标记 |
| 接口测试 | api/summary.md 存在 + 健康评分达标 |
| E2E 测试 | e2e/summary.md 存在 |
| 集成测试 | integration/summary.md 存在 |
| 详细设计 | detailed-design.md + self-reviews/design ≥10 文件 + cross-reviews ≥1 批次 + traceability 设计列=100% |
| 原型设计 | `docs/designs/prototypes/manifest.md` 与变更级 `prototype-changes.md` 存在 + BUILD 报告存在（`self-reviews/prototype/cdn-crossref-check/report.md`）+ 用户评审=✅已确认 或 ⏭️跳过 |
