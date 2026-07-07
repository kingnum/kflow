## Purpose

定义探索阶段的两动作规则，防止信息收集操作（WebFetch/WebSearch/Read外部资源/图片/PDF）的结果在上下文轮转后不可恢复。
## Requirements
### Requirement: 两动作规则

系统 SHALL 在探索阶段遵循两动作规则：每执行 2 次信息收集操作后，将关键发现写入当前阶段的产出文件。

#### Scenario: 信息收集操作触发保存
- **WHEN** 系统在探索阶段执行了 2 次信息收集操作（WebFetch / WebSearch / Read 外部资源 / 图片查看 / PDF 阅读）
- **THEN** 系统 SHALL 将收集到的关键发现写入 `functional-designs/` 或当前阶段的产出文件
- **AND** 保存内容包含信息来源、关键要点、对功能设计的影响

#### Scenario: 代码阅读不触发
- **WHEN** 系统 Read 操作用于阅读项目内源代码（非外部资源）
- **THEN** 此操作不计入两动作计数
- **AND** 因为代码内容可通过文件系统随时重新获取

#### Scenario: 阶段结束时强制保存
- **WHEN** 探索阶段即将结束（门控检查触发）
- **THEN** 系统 SHALL 确保所有中间发现已合入 functional-designs/index.md
- **AND** 检查是否有未保存的发现并提示保存

#### Scenario: 连续信息收集无需严格计数
- **WHEN** 系统在探索阶段需要连续执行 3 次以上信息收集才能形成完整认知
- **THEN** 系统 SHALL 在每批相关信息收集完成后立即保存
- **AND** "2 次"为启发式指导值，核心原则是"频繁保存中间发现"
