# Spec Delta

## MODIFIED Requirements

### Requirement: 优先级覆盖规则

系统 SHALL 支持特定场景下的优先级覆盖。

#### Scenario: 变更名正则优先裁决

- **WHEN** 用户输入匹配「继续/恢复/resume + 变更名称」的变更名正则模式
- **THEN** 系统 SHALL 在关键词优先级裁决之前先执行正则解析
- **AND** 正则命中时 SHALL NOT 进入关键词映射流程
- **AND** 「恢复/resume + 变更名称」SHALL 路由到 `kflow-resume`
- **AND** 「继续 + 变更名称」SHALL 路由到轻量推进路径

#### Scenario: 活跃变更自动路由

- **WHEN** 用户输入为继续类关键词（继续、下一步、接着）且存在活跃变更
- **THEN** 系统忽略其他关键词命中
- **AND** 直接路由到活跃变更的当前阶段
- **AND** 该路由 SHALL NOT 经过 `kflow-resume`

#### Scenario: 明确阶段名称直接匹配

- **WHEN** 用户输入包含明确的 Skill 名称或阶段名称（如"设计探索"、"kflow-design"）
- **THEN** 系统直接路由到对应 Skill
- **AND** 跳过关键词优先级裁决

#### Scenario: 关键词与变更名正则同时命中

- **WHEN** 用户输入同时命中继续类关键词与「继续/恢复/resume + 变更名称」正则
- **THEN** 正则解析结果 SHALL 优先于关键词优先级裁决
- **AND** 系统 SHALL 按变更名对应的路由分支处理，SHALL NOT 按关键词映射再裁决一次
