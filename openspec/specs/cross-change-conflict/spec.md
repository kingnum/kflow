## Requirements

### Requirement: 跨变更冲突检测

系统 SHALL 在开始新变更和编码阶段启动前检测与其他活跃变更的文件冲突。

#### Scenario: 新变更启动时冲突检测
- **WHEN** kflow-guide 或 kflow-explore 启动新变更
- **THEN** 系统扫描 docs/changes/index.md 获取所有活跃变更
- **AND** 检查新变更可能影响的文件是否与其他活跃变更重叠

#### Scenario: 冲突风险评估
- **WHEN** 检测到文件修改重叠
- **THEN** 系统评估冲突风险等级
- **AND** 无共享文件 → 无冲突风险
- **AND** 共享文件但不同区域 → 低风险，提示关注
- **AND** 相同区域修改 → 高风险，建议等待或协调
- **AND** 相同方法/类修改 → 严重冲突，强烈建议等待

#### Scenario: 编码阶段跨变更检查
- **WHEN** kflow-code 启动多 Agent 并行编码前
- **THEN** 检查当前变更修改的文件是否在其他活跃变更中也修改
- **AND** 冲突文件 > 2 个 → 建议先完成/归档冲突变更

### Requirement: 变更索引包含影响文件追踪

系统 SHALL 在 docs/changes/index.md 中增加影响文件字段。

#### Scenario: 索引记录影响文件
- **WHEN** 变更进入编码阶段
- **THEN** index.md 中该变更的记录增加"影响文件(关键)"列
- **AND** 列出被修改的关键文件（非全部，仅核心共享文件）
