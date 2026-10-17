# Spec Delta

## MODIFIED Requirements

### Requirement: Incremental RELOAD with verified-file markers

The system SHALL support incremental RELOAD — when files have not changed (mtime unchanged) and were already read in the current session, the main Agent SHALL generate "verified file markers" with summaries. Subagents receiving these markers SHALL skip full file reads for verified files. The scope of this mechanism SHALL cover all phase artifacts read during a change, not only the files on a phase's RELOAD list.

#### Scenario: Main Agent generates verified markers

- **WHEN** a subagent is about to be dispatched and RELOAD files have unchanged mtime
- **THEN** the main Agent SHALL inject verified-file markers with 1-3 line summaries into the subagent prompt

#### Scenario: Subagent skips verified files

- **WHEN** a subagent receives verified-file markers
- **THEN** it SHALL NOT re-read those files in full, using the provided summaries instead

#### Scenario: 验证标记覆盖阶段产物

- **WHEN** 一个子代理被构造且其输入包含已在本阶段读取过的阶段产物（如详细设计、功能设计、接口测试用例）
- **THEN** 主 Agent SHALL 为这些产物生成验证标记与摘要
- **AND** 子代理 SHALL 以摘要为起点，SHALL NOT 重新全文读取

#### Scenario: 大产物的验证标记

- **WHEN** 带验证标记的产物超过单次读取的合理体量
- **THEN** 摘要在标明该产物未变化的同时 SHALL 给出与本次任务相关的章节定位
- **AND** 子代理 SHALL 按章节定位读取所需片段而非全文

## ADDED Requirements

### Requirement: 会话内产物读取去重

在同一阶段内，主 Agent 与子代理 SHALL NOT 对同一文件重复全文读取；已读取过的文件 SHALL 通过行区间读取或摘要引用获取后续所需内容。

#### Scenario: 同阶段内第二次读取

- **WHEN** 某文件已在当前阶段被读取过，且 mtime 未变化
- **THEN** 后续读取 SHALL 使用行区间读取（仅读取所需片段）
- **AND** SHALL NOT 重复全文读取

#### Scenario: 读取同一文件的不同章节

- **WHEN** 需要在同一文件中获取多个不连续章节
- **THEN** 读取 SHALL 按章节行区间分别进行
- **AND** SHALL NOT 以「整文件读取一次更省事」为由读取全文

#### Scenario: 文件发生变更后的重新读取

- **WHEN** 某文件的 mtime 相比上次读取发生变化
- **THEN** 该文件 SHALL 被视为新文件并重新读取
- **AND** 此前的读取记录 SHALL 不再用于跳过

#### Scenario: 读取去重不适用于首次跨阶段读取

- **WHEN** 某产物在上一阶段被读取过，本阶段为首次读取
- **THEN** 该产物 SHALL 按当前阶段的需要重新读取或按章节定位读取
- **AND** SHALL NOT 依赖上一阶段上下文的残留记忆
