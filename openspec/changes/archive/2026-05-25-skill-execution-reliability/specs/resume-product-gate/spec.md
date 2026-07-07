## ADDED Requirements

### Requirement: 中断恢复阶段产物完整性验证

系统 SHALL 在 kflow-resume 的 GATE 步骤中，对 .status.md 标记为「✅ 完成」的阶段执行产物完整性验证，验证不通过时拒绝认定该阶段完成。

#### Scenario: 编码阶段产物验证

- **WHEN** kflow-resume 读取 .status.md 发现编码阶段状态为「✅ 完成」
- **THEN** 系统 SHALL 验证以下条件全部满足：
  - `.status.md` 中「执行轮次」字段 = 10/10
  - `traceability.md` 文件中「编码实现」列覆盖率 = 100%
  - 不存在 TODO/TBD/{待填写} 等占位符
- **AND** 任一条件不满足 → 拒绝认定编码阶段完成，标记为「⚠️ 需修订」

#### Scenario: 代码审查阶段产物验证

- **WHEN** kflow-resume 读取 .status.md 发现代码审查阶段状态为「✅ 完成」
- **THEN** 系统 SHALL 验证：`subchanges/{subchange}/test-reports/review/code-review.md` 文件存在且包含审查通过标记
- **AND** 文件不存在或无通过标记 → 拒绝认定代码审查阶段完成

#### Scenario: 接口测试阶段产物验证

- **WHEN** kflow-resume 读取 .status.md 发现接口测试阶段状态为「✅ 完成」
- **THEN** 系统 SHALL 验证：`subchanges/{subchange}/test-reports/api/summary.md` 文件存在且健康评分达到通过阈值
- **AND** 文件不存在或评分不达标 → 拒绝认定接口测试阶段完成

#### Scenario: E2E 测试阶段产物验证

- **WHEN** kflow-resume 读取 .status.md 发现 E2E 测试阶段状态为「✅ 完成」
- **THEN** 系统 SHALL 验证：`subchanges/{subchange}/test-reports/e2e/summary.md` 文件存在
- **AND** 文件不存在 → 拒绝认定 E2E 测试阶段完成

#### Scenario: 详细设计阶段产物验证

- **WHEN** kflow-resume 读取 .status.md 发现详细设计阶段状态为「✅ 完成」
- **THEN** 系统 SHALL 验证：
  - `detailed-design.md` 文件存在
  - `self-reviews/design/` 目录存在且包含至少 10 个自审报告文件
  - `cross-reviews/` 目录存在且至少有一个批次目录
  - `traceability.md` 存在且「详细设计」列覆盖率 = 100%

#### Scenario: 全部验证通过

- **WHEN** 所有标记为「✅ 完成」的阶段产物验证均通过
- **THEN** 门控验证通过，进入 SUMMARIZE 步骤
- **AND** 输出恢复摘要并调度对应阶段 Skill

#### Scenario: 部分验证失败

- **WHEN** 存在阶段标记为「✅ 完成」但产物验证不通过
- **THEN** 系统 SHALL 输出验证失败项清单
- **AND** 将对应阶段状态回退为「⚠️ 需修订」
- **AND** 调度回退到该阶段重新执行
- **AND** 提示用户状态文件与产物不一致

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
| 原型设计 | prototype/index.html 存在 + 用户评审=✅已确认 或 ⏭️跳过 |

### Requirement: 产物验证不影响未验证阶段

产物验证仅针对 .status.md 中标记为「✅ 完成」的阶段，不检查「⏳ 待开始」或「🔄 进行中」的阶段。

#### Scenario: 跳过未验证阶段

- **WHEN** 某阶段状态为「⏳ 待开始」或「🔄 进行中」
- **THEN** 系统 SHALL 不对其执行产物验证
- **AND** 该阶段在恢复后从当前状态继续执行
