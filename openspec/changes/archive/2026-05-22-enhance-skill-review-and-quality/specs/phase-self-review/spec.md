## MODIFIED Requirements

### Requirement: 三阶段 10 轮自审强制执行

系统 SHALL 在 kflow-explore、kflow-prototype-design、kflow-design、kflow-plan 四个阶段各强制执行 10 轮自循环审查，不允许提前终止。四阶段统一采用"重复制"（每轮全维度独立审查，不允许按维度分工）。

#### Scenario: explore 阶段自审（重复制）
- **WHEN** kflow-explore 完成 functional-designs/ 初稿
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按完整性、闭环性、必要性、清晰性**全部四个维度**独立检查
- **AND** SHALL NOT 按维度分组分配轮次（如 Round 1-3 仅结构性检查）
- **AND** 子代理发现问题直接修复产物文件
- **AND** 必须串行完成全部 10 轮后方可标记阶段完成

#### Scenario: prototype 阶段自审（重复制）
- **WHEN** kflow-prototype-design 完成 VERIFY 步骤后
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按覆盖性、一致性、可用性、完整性**全部四个维度**独立检查
- **AND** 覆盖性为第一优先级：确保所有 FP 有对应原型页面
- **AND** 子代理发现问题直接修复原型文件
- **AND** SHALL NOT 按维度分组分配轮次
- **AND** 必须串行完成全部 10 轮后方可进入用户评审

#### Scenario: design 阶段自审（重复制）
- **WHEN** kflow-design 完成 detailed-design.md 初稿
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按一致性、完备性、可行性、可测性**全部四个维度**独立检查
- **AND** SHALL NOT 按维度分组分配轮次（如 Round 1-3 结构性、Round 4-7 细节、Round 8-10 边界）
- **AND** 子代理发现问题直接修复设计文档
- **AND** 必须串行完成全部 10 轮后方可进入四视角交叉审查

#### Scenario: plan 阶段自审（重复制，新增）
- **WHEN** kflow-plan 完成所有子变更 tasks.md 初稿
- **THEN** 主 Agent 启动第一轮子代理执行自审
- **AND** 每轮子代理 SHALL 按任务覆盖完整性、DoD 验收标准正确性、HITL 标注准确性、任务粒度合理性**全部四个维度**独立检查
- **AND** 子代理发现问题直接修复 tasks.md 文件
- **AND** 必须串行完成全部 10 轮后方可标记阶段完成
- **AND** 报告保存到 `self-reviews/plan/{YYYYMMDD}-{HHMMSS}.md`

### Requirement: 自审后进入交叉审查或用户评审

系统 SHALL 在自审完成后按阶段类型进入下一步：explore 进入完成态，prototype 进入用户评审，design 进入四视角交叉审查，plan 进入完成态。

#### Scenario: explore 自审完成后
- **WHEN** explore 完成 10 轮自审
- **THEN** 标记阶段完成
- **AND** 释放 prototype 或 design 阶段门控

#### Scenario: prototype 自审完成后进入用户评审
- **WHEN** prototype 完成 10 轮自审
- **THEN** 自审记录全部保存完毕
- **AND** 进入用户评审流程（AskUserQuestion）
- **AND** 用户确认后标记阶段完成

#### Scenario: design 自审完成后进入四视角审查
- **WHEN** design 完成 10 轮自审
- **THEN** 自审记录全部保存完毕
- **AND** 进入四视角交叉审查流程

#### Scenario: plan 自审完成后标记完成（新增）
- **WHEN** plan 完成 10 轮自审
- **THEN** 自审记录全部保存完毕
- **AND** 标记阶段完成
- **AND** 释放 code 阶段门控
