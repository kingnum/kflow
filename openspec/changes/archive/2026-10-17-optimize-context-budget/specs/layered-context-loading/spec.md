# Spec Delta

## MODIFIED Requirements

### Requirement: Layered context loading strategy

The system SHALL define a layered context loading strategy for subagent invocations. The sources for each loading tier SHALL reside in the skill's own `references/` subdirectory. Subagent prompts SHALL load only the tiers relevant to the current phase. The loading granularity SHALL descend to the section level — a subagent SHALL load only the sections its own phase and responsibility require, SHALL NOT load an entire references file when only part of it applies.

#### Scenario: Loading tier annotation

- **WHEN** any references file is loaded for a subagent
- **THEN** the file SHALL be loaded from `.claude/skills/<skill-name>/references/` (consumer) or `skills/<skill-name>/references/` (dev)
- **AND** the loading instruction in SKILL.md SHALL list the specific references files and their tiers

#### Scenario: Execution phase subagent loads only relevant tiers

- **WHEN** a code phase subagent is constructed
- **THEN** its prompt SHALL instruct loading of 基础层 + 执行层 from the skill's own `references/` directory
- **AND** SHALL NOT load files from any external shared directory

#### Scenario: No reference to kflow-shared in loading instructions

- **WHEN** any KFlow Skill constructs a subagent prompt
- **THEN** the loading instructions SHALL NOT reference `kflow-shared/`
- **AND** all file paths SHALL point to the skill's own `references/` directory

#### Scenario: 加载粒度下沉到阶段

- **WHEN** 一个执行类阶段的子代理被构造
- **THEN** 其引用的 references 文件 SHALL 已按该阶段切片，仅含本阶段章节
- **AND** 子代理 SHALL NOT 加载按阶段类型分层但包含其他阶段章节的完整文件

#### Scenario: 移除跨阶段无关章节的加载

- **WHEN** 一个子代理加载某 references 文件
- **THEN** 该文件中属于其他阶段的章节 SHALL 已在切片阶段被移除
- **AND** 子代理的加载内容中 SHALL NOT 出现其他阶段的门控矩阵、钩子步骤或状态取值

#### Scenario: 切片后原分层定义继续适用

- **WHEN** 判定一个子代理应加载哪些层级的文件
- **THEN** 基础层 / 执行层 / 服务层 / 创意层 / 恢复层 / 归档层的层级划分 SHALL 保持不变
- **AND** 各层级的文件清单 SHALL 按切片后的实际文件列出

#### Scenario: 设计类子代理的加载范围

- **WHEN** 一个设计类阶段（explore / prototype-design / design）的子代理被构造
- **THEN** 其 SHALL 加载基础层 + 创意层
- **AND** SHALL NOT 加载执行层与服务层文件
