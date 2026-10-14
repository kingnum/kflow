# Spec Delta

## Purpose

定义以「签署清单自证 + 单轮独立验证」取代多轮收敛循环的审查机制：主 Agent 在写作阶段按阶段专属维度逐项签署并留下产物内的证据锚点，独立子代理经单轮验证打假签署并独立发现遗漏，使审查成本固定可预算、质量控制在写作阶段完成。

## ADDED Requirements

### Requirement: 签署清单结构与证据锚点

签署清单 SHALL 按阶段专属的 4 个审查维度组织，每个维度 SHALL 包含「维度」「自证结论」「证据锚点」三列。证据锚点 SHALL 指向产物内的具体位置——章节号、功能点 ID、接口 ID、用例 ID 或表名之一。证据锚点为空、或指向产物中不存在的内容时，该维度的签署 SHALL 判定为不成立。

#### Scenario: 签署清单包含维度、自证结论与证据锚点三列

- **WHEN** 主 Agent 在阶段产物中填写签署清单
- **THEN** 每个维度行 SHALL 包含维度名、自证结论（通过 / 不通过）与证据锚点
- **AND** 证据锚点 SHALL 指向产物内的具体位置

#### Scenario: 锚点为空时签署不成立

- **WHEN** 某维度行的证据锚点为空
- **THEN** 该维度的签署 SHALL 判定为不成立
- **AND** 该阶段 SHALL NOT 判定为签署通过

#### Scenario: 锚点指向不存在内容时签署不成立

- **WHEN** 验证子代理按某维度行的证据锚点定位产物内容
- **AND** 该锚点指向的位置在产物中不存在或内容不匹配
- **THEN** 该维度的签署 SHALL 判定为不成立

#### Scenario: 签署清单落于阶段产物模板

- **WHEN** 某阶段的产物模板定义签署区
- **THEN** 签署清单 SHALL 作为该产物模板的组成部分存在
- **AND** SHALL NOT 以独立文件形式产出

### Requirement: 主 Agent 写作时自证签署

产物初稿完成后，主 Agent SHALL 逐个 4 维度完成签署自证，填写自证结论与证据锚点。签署自证 SHALL 由主 Agent 执行，SHALL NOT 启动子代理。

#### Scenario: 主 Agent 逐维度自证

- **WHEN** 阶段产物初稿完成
- **THEN** 主 Agent SHALL 按本阶段 4 个维度逐项填写自证结论与证据锚点
- **AND** SHALL NOT 启动子代理执行签署自证

#### Scenario: 自证发现维度不通过时先行修复

- **WHEN** 主 Agent 在某维度的自证过程中发现产物不满足该维度要求
- **THEN** 主 Agent SHALL 在完成签署前修复该产物
- **AND** 修复后 SHALL 重新完成该维度的自证

#### Scenario: 签署完成后进入单轮验证

- **WHEN** 4 个维度的签署自证全部完成
- **THEN** 系统 SHALL 进入单轮验证环节

### Requirement: 验证子代理的打假契约与执行顺序

验证子代理 SHALL 先独立遍历产物并形成自身的 4 维度结论，此阶段 SHALL NOT 读取签署清单。独立遍历完成后，验证子代理 SHALL 逐项对照签署清单执行打假。执行顺序反转（先读签署清单再遍历产物）时该轮验证结果 SHALL NOT 被接受。

#### Scenario: 先独立遍历后读取签署清单

- **WHEN** 验证子代理启动
- **THEN** 验证子代理 SHALL 先独立遍历产物并形成自身的 4 维度结论
- **AND** 在此阶段 SHALL NOT 读取签署清单

#### Scenario: 独立遍历完成后执行打假

- **WHEN** 验证子代理完成独立遍历
- **THEN** 验证子代理 SHALL 逐项对照签署清单执行打假
- **AND** SHALL 判定每项签署是否属实

#### Scenario: 执行顺序反转时结果不被接受

- **WHEN** 验证子代理先读取签署清单再遍历产物
- **THEN** 该轮验证结果 SHALL NOT 被接受
- **AND** 主 Agent SHALL 重新启动验证子代理

#### Scenario: 验证子代理只报告不修改产物

- **WHEN** 验证子代理发现产物的任何问题
- **THEN** 验证子代理 SHALL NOT 修改任何阶段产物
- **AND** SHALL 将问题记入验证报告

### Requirement: 验证发现的分级与终止结果

验证子代理 SHALL 将发现分为「渐进式审查发现」与「阻塞级发现」两类。存在阻塞级发现时终止结果 SHALL 为 `验证发现问题({N})`，其中 N 为发现总数；不存在任何发现且无签署不成立项时终止结果 SHALL 为 `验证通过`。终止结果 SHALL 写入变更级 `.status.md`。

#### Scenario: 零发现且无签署不成立时验证通过

- **WHEN** 验证子代理独立遍历未发现问题
- **AND** 全部 4 个维度的签署经打假属实
- **THEN** 终止结果 SHALL 为 `验证通过`

#### Scenario: 存在发现时记录发现数

- **WHEN** 验证子代理在独立遍历或打假中发现问题
- **THEN** 终止结果 SHALL 为 `验证发现问题({N})`
- **AND** N SHALL 为该阶段发现总数

#### Scenario: 终止结果写入状态文件

- **WHEN** 单轮验证终止
- **THEN** 终止结果 SHALL 写入变更级 `.status.md`
- **AND** 主 Agent SHALL 据此决定后续流转

### Requirement: 修复责任在验证后统一执行

验证完成后，主 Agent SHALL 统一修复全部渐进式审查发现与阻塞级发现，并生成「本阶段修复清单」。主 Agent SHALL NOT 在验证子代理报告问题后追加确认轮次。修复后的产物 SHALL 连同修复清单交付下游。

#### Scenario: 主 Agent 统一修复

- **WHEN** 验证子代理报告发现项
- **THEN** 主 Agent SHALL 统一修复全部发现项
- **AND** SHALL 生成「本阶段修复清单」记录修复内容

#### Scenario: 不追加确认轮

- **WHEN** 主 Agent 完成修复
- **THEN** 系统 SHALL NOT 追加确认轮次验证修复结果
- **AND** 修复后的产物 SHALL 直接交付下游

#### Scenario: 修复清单随产物交付

- **WHEN** 阶段产物交付下游
- **THEN** 「本阶段修复清单」SHALL 一并交付
- **AND** 下游审查环节 SHALL 可读取该清单以验证修复结果

### Requirement: 签署清单的维度定义

各阶段的签署清单 SHALL 采用该阶段既有的 4 个审查维度，SHALL NOT 因单轮化而减少维度或检查项。

#### Scenario: 设计类阶段维度

- **WHEN** kflow-explore 完成产物初稿
- **THEN** 签署清单 SHALL 采用完整性、闭环性、必要性、清晰性四个维度

#### Scenario: 详细设计阶段维度

- **WHEN** kflow-design 完成产物初稿
- **THEN** 签署清单 SHALL 采用一致性、完备性、可行性、可测性四个维度

#### Scenario: 原型设计阶段维度

- **WHEN** kflow-prototype-design 完成产物初稿
- **THEN** 签署清单 SHALL 采用覆盖性、一致性、可用性、完整性四个维度
- **AND** 覆盖性 SHALL 保持第一优先级

#### Scenario: 计划阶段维度

- **WHEN** kflow-plan 完成产物初稿
- **THEN** 签署清单 SHALL 采用任务覆盖完整性、DoD 验收标准正确性、子变更类型标注准确性、任务粒度合理性四个维度
