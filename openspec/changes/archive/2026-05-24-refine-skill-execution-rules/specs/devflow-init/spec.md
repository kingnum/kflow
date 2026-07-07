## ADDED Requirements

### Requirement: re-init 变更对齐检查

kflow-init 在执行 Re-init 幂等更新时，SHALL 扫描所有未归档变更的阶段列表，与当前 skill 体系的阶段定义做对齐检查，输出报告但不自动修改。

#### Scenario: 扫描未归档变更

- **WHEN** kflow-init 执行 Re-init 流程
- **THEN** 系统扫描 docs/changes/ 目录下所有未归档变更
- **AND** 排除 docs/archive/ 目录下的已归档变更
- **AND** 读取每个变更的 .status.md 获取当前阶段列表

#### Scenario: 对比当前 skill 体系阶段定义

- **WHEN** 系统获取到所有未归档变更的阶段列表
- **THEN** 系统读取 core-mechanisms.md §1.3 中的当前阶段定义
- **AND** 对每个变更 .status.md 中的阶段列表与当前阶段定义逐一对比
- **AND** 项目类型匹配：前后端项目使用 11 阶段列表，纯后端项目使用 9 阶段列表

#### Scenario: 缺失阶段检测

- **WHEN** 变更 .status.md 中的阶段列表缺少当前 skill 体系定义的某个阶段
- **THEN** 系统在输出报告中标记: "⚠️ 变更 {change-name} 缺少阶段: {阶段名}"
- **AND** 标注该阶段在当前体系中的位置和职责

#### Scenario: 多余阶段检测

- **WHEN** 变更 .status.md 中包含当前 skill 体系已废弃的阶段
- **THEN** 系统在输出报告中标记: "ℹ️ 变更 {change-name} 包含已废弃阶段: {阶段名}"
- **AND** 标注该阶段为何被废弃或已合并到其他阶段

#### Scenario: 阶段顺序变更检测

- **WHEN** 变更 .status.md 中的阶段顺序与当前 skill 体系定义不一致
- **THEN** 系统在输出报告中标记: "ℹ️ 变更 {change-name} 阶段顺序不同: {具体差异}"
- **AND** 仅标记差异，不自动调整

#### Scenario: 输出对齐报告

- **WHEN** 所有变更的对齐检查完成
- **THEN** 系统在对话中输出对齐报告摘要
- **AND** 报告包含：检测到的变更总数、对齐的变更数、存在差异的变更数及清单
- **AND** 系统 SHALL NOT 自动修改任何 .status.md 文件
- **AND** 如存在差异，提示用户"是否需要协助修复不一致的变更"

#### Scenario: 无未归档变更时跳过

- **WHEN** docs/changes/ 下无未归档变更
- **THEN** 系统跳过对齐检查
- **AND** 不输出任何对齐报告
