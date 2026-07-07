## MODIFIED Requirements

### Requirement: Phase hooks service management deduplication
`09-phase-hooks.md` SHALL remain the authoritative location for PRE_HOOK/POST_HOOK step sequences. `05-execution-services.md` sections that duplicate service-lifecycle.md content (§7.7 port conflict detection, §7.8 stop timeout chain, §8.2 service refresh detailed steps) SHALL be replaced with references.

#### Scenario: Port conflict detection single source
- **WHEN** port conflict detection rules are needed
- **THEN** they SHALL be read from `09-phase-hooks.md` §八 (or `kflow-shared/service-lifecycle.md` §二), NOT from `05-execution-services.md` §7.7

#### Scenario: Service stop timeout chain single source
- **WHEN** service stop timeout chain is needed
- **THEN** it SHALL be read from `09-phase-hooks.md` §七 (or `kflow-shared/service-lifecycle.md` §三), NOT from `05-execution-services.md` §7.8

#### Scenario: 05-execution-services.md simplified
- **WHEN** `05-execution-services.md` is read after the change
- **THEN** §7.7, §7.8 SHALL be replaced with references to `kflow-shared/service-lifecycle.md`; §8.2 SHALL retain only the synchronization point table and replace detailed steps with a reference
