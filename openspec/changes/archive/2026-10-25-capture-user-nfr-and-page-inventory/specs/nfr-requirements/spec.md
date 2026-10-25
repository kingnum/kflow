# Spec Delta

## MODIFIED Requirements

### Requirement: 详细设计包含 NFR 章节

系统 SHALL 在详细设计文档（design.md）中包含非功能需求（NFR）章节。

#### Scenario: NFR 章节结构
- **WHEN** 详细设计文档生成
- **THEN** design.md 包含 NFR 章节，下设性能需求、安全需求、可用性需求、可维护性需求四个子节
- **AND** 每项 NFR 包含目标值、测量方法、验证阶段

#### Scenario: NFR 章节输入来源
- **WHEN** 详细设计编写 NFR 章节
- **THEN** 系统 SHALL 以 functional-designs/index.md 的「非功能期望」小节为需求输入
- **AND** 将用户视角期望转译为可度量技术目标值（目标值、测量方法、验证阶段）
- **AND** 探索阶段标注「本变更无特殊非功能期望」时，NFR 章节按既有最小要求自行定义

#### Scenario: NFR 最小要求
- **WHEN** 编码阶段门控检查
- **THEN** design.md 的 NFR 章节必须包含至少 1 项性能需求和 1 项安全需求
- **AND** 不满足时 ❌ 阻塞编码阶段

#### Scenario: 功能缺陷级 NFR 简化
- **WHEN** 变更类型为功能缺陷级
- **THEN** NFR 章节可简化（仅包含安全需求，如缺陷涉及安全）
