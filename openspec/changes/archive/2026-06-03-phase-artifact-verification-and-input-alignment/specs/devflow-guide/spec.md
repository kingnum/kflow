# devflow-guide Delta Spec

## ADDED Requirements

### Requirement: kflow-verify 路由入口

kflow-guide SHALL 支持 kflow-verify Skill 的路由识别和调用。

#### Scenario: 诊断触发词识别
- **WHEN** 用户输入包含「诊断/验证产物/检查产物/产物完整性/输入源检查/verify」等关键词
- **THEN** kflow-guide SHALL 识别为 kflow-verify 调用意图
- **AND** 路由到 kflow-verify Skill

#### Scenario: 带变更名的诊断
- **WHEN** 用户输入「诊断 {change-name}」或「验证 {change-name} 产物」
- **THEN** kflow-guide SHALL 提取变更名称
- **AND** 调用 kflow-verify 对指定变更执行诊断

#### Scenario: 无变更名诊断
- **WHEN** 用户输入「诊断产物」且存在单个活跃变更
- **THEN** kflow-guide SHALL 自动选择该变更
- **AND** 调用 kflow-verify 执行诊断
- **AND** 多个活跃变更时列出供用户选择

### Requirement: kflow-verify 纳入流程概览

kflow-guide 的流程概览 SHALL 包含 kflow-verify 作为独立诊断工具的说明。

#### Scenario: 流程概览显示 verify
- **WHEN** 用户请求查看流程概览
- **THEN** 系统 SHALL 在流程末尾（audit 之前）显示 kflow-verify 作为独立诊断工具
- **AND** 标注为「独立诊断（非流程阶段），可随时调用诊断产物完整性」
