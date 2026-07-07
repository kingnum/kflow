## MODIFIED Requirements

### Requirement: Checkpoint 恢复优先级

系统 SHALL 在恢复时优先读取子变更级 checkpoint，无则回退到变更级，并在恢复输出中展示五问题快速摘要。

#### Scenario: 从子变更级恢复
- **WHEN** 系统从中断恢复且存在子变更级 checkpoint
- **THEN** 系统读取最近子变更级 checkpoint
- **AND** 解析 frontmatter 获取子变更名、状态、修改文件列表
- **AND** 恢复该子变更的阶段状态和任务进度

#### Scenario: 从变更级恢复
- **WHEN** 系统从中断恢复且无子变更级 checkpoint
- **THEN** 系统读取最近变更级 checkpoint
- **AND** 解析 frontmatter 获取变更级状态
- **AND** 恢复变更级阶段状态和进度

#### Scenario: 两级 checkpoint 均不存在
- **WHEN** 系统从中断恢复且两级均无 checkpoint
- **THEN** 系统读取 `.status.md` 和 `tasks.md` 推断当前阶段
- **AND** 显示推断结果供用户确认

#### Scenario: 恢复摘要输出
- **WHEN** kflow-resume 完成状态恢复
- **THEN** 系统 SHALL 在详细恢复信息前输出五问题快速摘要
- **AND** 摘要包含：当前位置、剩余路径、变更目标、设计依据、已完成
- **AND** 摘要 SHALL 控制在 15 行以内
