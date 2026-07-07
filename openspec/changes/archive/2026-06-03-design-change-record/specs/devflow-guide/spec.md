## ADDED Requirements

### Requirement: 设计修订意图集中检测与分流

kflow-guide SHALL 在 PARSE 阶段检测用户的设计修订意图并分流到对应设计 Skill。

#### Scenario: 检测设计修订触发词

- **WHEN** 用户输入包含"功能设计需调整/原型需调整/详细设计需调整/接口设计要改/修改设计/调整设计/设计要改"等关键词
- **THEN** kflow-guide SHALL 进入 DESIGN_REVISION 模式
- **AND** 解析关键词确定目标设计目录：含"功能"/"需求" → functional-designs，含"原型"/"UI"/"交互" → prototype，含"详细"/"接口"/"架构" → detailed-design

#### Scenario: 分流到目标设计 Skill

- **WHEN** 设计修订目标确定
- **THEN** kflow-guide SHALL 唤醒对应设计 Skill：functional-designs → kflow-explore（REVISION）、prototype → kflow-prototype-design（REVISION）、detailed-design → kflow-design（REVISION）

#### Scenario: 设计修订完成后返回

- **WHEN** 目标设计 Skill 完成修订
- **THEN** kflow-guide SHALL 更新目标目录 index.md 的修订记录（版本号递增 + 追加行）
- **AND** SHALL 更新 .status.md 的设计修订同步追踪表（追加行）
- **AND** SHALL 通过 AskUserQuestion 询问用户：「设计修订完成。是否立即回退并重新执行受影响阶段？」选项：确认回退 / 暂缓继续

### Requirement: DESIGN_REVISION 触发词维护在 kflow-guide

设计修订触发词 SHALL 仅维护在 kflow-guide 的 description 和 SKILL.md 中，不分散到各阶段 Skill。

#### Scenario: 阶段 Skill 不含设计修订触发词

- **WHEN** 任意阶段 Skill 的 SKILL.md description 被编写或更新
- **THEN** description SHALL 仅包含该阶段自身的触发词
- **AND** SHALL NOT 包含指向其他阶段的触发词或设计修订触发词
