# incremental-reload Specification

## Purpose

定义增量 RELOAD 机制：当文件 mtime 未变化且在当前会话中已被读取时，主 Agent 生成「已验证文件标记」与摘要，子代理据此跳过全文读取以减少 token 开销，同时保留按需自主读取的权利。

## Requirements

### Requirement: Incremental RELOAD with verified-file markers
The system SHALL support incremental RELOAD — when files have not changed (mtime unchanged) and were already read in the current session, the main Agent SHALL generate "verified file markers" with summaries. Subagents receiving these markers SHALL skip full file reads for verified files.

#### Scenario: Main Agent generates verified markers
- **WHEN** a subagent is about to be dispatched and RELOAD files have unchanged mtime
- **THEN** the main Agent SHALL inject verified-file markers with 1-3 line summaries into the subagent prompt

#### Scenario: Subagent skips verified files
- **WHEN** a subagent receives verified-file markers
- **THEN** it SHALL NOT re-read those files in full, using the provided summaries instead

### Requirement: Subagent retains self-read right
Subagents SHALL retain the right to self-read a verified file if the summary proves insufficient during execution.

#### Scenario: Subagent self-reads when needed
- **WHEN** a subagent discovers it needs more detail from a verified file than the summary provides
- **THEN** it SHALL read the file directly
