## ADDED Requirements

### Requirement: SKILL.md front matter includes version field
Every KFlow Skill's `SKILL.md` front matter SHALL include a `version` field. The version value SHALL match the repository root `VERSION` file.

#### Scenario: Front matter with version
- **WHEN** `kflow-code/SKILL.md` is read
- **THEN** its front matter SHALL contain `version: <current-version>` (e.g., `version: 0.16.0`)

#### Scenario: All skills share the same version
- **WHEN** any two KFlow Skills are compared
- **THEN** their `version` front matter values SHALL be identical
- **AND** both SHALL match the repository `VERSION` file

### Requirement: sync-version.sh batch version synchronization
A script `scripts/sync-version.sh` SHALL exist that reads the root `VERSION` file and writes the version value into the front matter `version` field of every `skills/kflow-*/SKILL.md` file.

#### Scenario: Manual version sync after VERSION update
- **WHEN** a developer modifies `VERSION` and runs `./scripts/sync-version.sh`
- **THEN** every `skills/kflow-*/SKILL.md` SHALL have its `version:` field updated to the new value

#### Scenario: Existing version field is updated
- **WHEN** `sync-version.sh` runs and a SKILL.md already has a `version:` field
- **THEN** the existing value SHALL be replaced with the current VERSION value

#### Scenario: Missing version field is added
- **WHEN** `sync-version.sh` runs and a SKILL.md does not yet have a `version:` field
- **THEN** a new `version:` line SHALL be inserted into the front matter

### Requirement: package-skills.sh validates version consistency
The packaging script SHALL verify that every SKILL.md's `version` field matches the root `VERSION` file before creating a package. If any mismatch is detected, the packaging SHALL abort with an error message listing the inconsistent files.

#### Scenario: Version mismatch aborts packaging
- **WHEN** `package-skills.sh` runs and a SKILL.md has a different version than `VERSION`
- **THEN** the script SHALL output an error message listing the mismatched file
- **AND** the script SHALL exit with a non-zero status

#### Scenario: Version match allows packaging
- **WHEN** `package-skills.sh` runs and all SKILL.md versions match `VERSION`
- **THEN** the packaging SHALL proceed normally

### Requirement: Consumer version inspection
A consumer SHALL be able to determine the installed KFlow Skills version by reading the `version` field from any skill's SKILL.md front matter.

#### Scenario: Consumer checks installed version
- **WHEN** a consumer runs `grep '^version:' .claude/skills/kflow-guide/SKILL.md`
- **THEN** the installed KFlow Skills version SHALL be output (e.g., `version: 0.16.0`)
