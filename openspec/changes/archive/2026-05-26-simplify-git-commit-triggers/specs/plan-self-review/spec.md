## MODIFIED Requirements

### Requirement: 计划阶段审查维度（定制）

kflow-plan 自审 SHALL 覆盖以下 4 个定制维度，每轮子代理 SHALL 执行全部维度检查。

#### Scenario: 任务覆盖完整性检查

- **WHEN** plan 自审执行任务覆盖完整性维度
- **THEN** 检查是否所有 detailed-design.md 中该子变更的功能点都有对应任务
- **AND** 覆盖率必须 = 100%
- **AND** 检查是否所有 api-tests/ 和 e2e-tests/ 中的测试用例在任务清单中有对应的测试编写步骤
- **AND** 标记缺失任务的功能点

#### Scenario: DoD 验收标准正确性检查

- **WHEN** plan 自审执行 DoD 验收标准正确性维度
- **THEN** 检查每功能点是否包含 Happy Path(≥1) + Error Path(≥2) + Edge Case(≥1) + Quality(≥1)
- **AND** 检查每条验收标准是否使用 WHEN/THEN 格式
- **AND** 检查 Happy Path 是否验证正常业务流程
- **AND** 检查 Error Path 是否覆盖至少 2 种异常场景
- **AND** 检查 Edge Case 是否覆盖边界值
- **AND** 检查 Quality 是否验证性能/安全等质量属性
- **AND** 标记格式错误或数量不足的功能点

#### Scenario: HITL 标注准确性检查

- **WHEN** plan 自审执行 HITL 标注准确性维度
- **THEN** 检查所有 HITL 子变更是否包含决策点列表
- **AND** 检查 `[HITL D{n}]` 标注是否在正确的任务位置（Step 2 或 Step 3 之间）
- **AND** 检查每个决策点是否有明确的决策内容和至少 2 个选项
- **AND** 检查默认建议是否标注
- **AND** 检查 AFK 子变更是否不包含 HITL 标注
- **AND** 标记缺失标注或位置不当的决策点

#### Scenario: 任务粒度合理性检查

- **WHEN** plan 自审执行任务粒度合理性维度
- **THEN** 检查每任务是否符合 2-5 分钟可完成的标准
- **AND** 检查 TDD 循环是否完整（Step 1-7：编写测试→RED→实现→GREEN→质量检查→重构→验证）
- **AND** 标记过粗任务（包含多个独立操作）
- **AND** 标记过细任务（实现细节级别）
