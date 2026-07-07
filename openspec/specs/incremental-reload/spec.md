# incremental-reload Specification

## ADDED by token-opt-incremental-reload

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
