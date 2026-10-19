# Design

## Context

See `proposal.md` for motivation. The current defect lifecycle is change-centric:

- `kflow-bug-triage` requires an active change and registers defects under `docs/changes/{change}/bugs/`.
- `kflow-bug-fix` fast lane reads `bugs/fix/{BUG-ID}/bugfix-status.md` from that change.
- `kflow-guide` treats “no active change” as a reason to create a change through `kflow-explore`.

The change-tier system and the full phase set are designed for feature changes. A defect that only needs an implementation fix is therefore forced through feature-shaped planning, design, review, testing, audit, and archive.

## Goals / Non-Goals

**Goals:**

- Make the L4 defect fast lane reachable without an active change.
- Give user-reported defects a project-level home that is independent of change archives.
- Preserve the existing change-scoped bug path for test-stage failures.
- Make the default route for an eligible simple defect the fast lane, not a new change.
- Ensure project-level blocking defects still gate archive.

**Non-Goals:**

- Changing the change-tier formula or the lightweight subchange rules (covered by `relax-defect-tier-upgrades`).
- Migrating existing change-level `bugs/` data.
- Defining a project release/versioning workflow for standalone defect fixes.
- Adding a new code-review or design-review phase to the fast lane.

## Decisions

### D1: Project-level `docs/bugs/` rather than a pseudo-change directory

**Decision:** User-reported defects are registered under `docs/bugs/`; change-level `docs/changes/{change}/bugs/` remains for test-stage failures.

**Rationale:** A defect is not a change. A pseudo-change directory would appear in `kflow-status`, `kflow-resume`, and `kflow-archive`, and would create ambiguity about whether it must be audited or archived. A separate root keeps the change namespace clean and lets the fast lane close out without touching change state.

**Alternatives considered:** `docs/changes/fix-{id}/` (rejected: pollutes change scanning and archive semantics); a single global `bugs/` at repository root (rejected: `docs/` is the established documentation root).

### D2: Attribute before creating anything

**Decision:** Triage first decides the workspace (project vs change) and then decides the path (fast lane vs change). It asks the user only when attribution is ambiguous.

**Rationale:** The user's second reported scenario is “there is an active change, but a new change is still created”. Attribution prevents that: a defect caused by the active change is linked to it; a defect in existing functionality goes to the project-level workspace. Neither case requires a new change unless the fix needs design work.

**Rule:**

| Condition | Workspace | Path |
|-----------|-----------|------|
| No active change | `docs/bugs/` | L4 eligible → fast lane; otherwise create a change |
| Active change caused the defect | change-level `bugs/` | L4 eligible → change-scoped fast lane; otherwise change REVISION |
| Active change exists but is unrelated | `docs/bugs/` | Same as no-active-change |
| Ambiguous | Ask user | Ask user |

### D3: Fast lane eligibility is “design-correct + bounded”, not “score below a number”

**Decision:** The fast lane gate is:

1. Triage conclusion is L4.
2. The fix does not require modifying L1/L2/L3 artifacts.
3. The fix does not require a data migration or a breaking interface-contract change.
4. The affected items are enumerable as verification targets.
5. The user confirms.

The impact score is shown to the user as a warning signal, not a hard gate. A large but well-bounded L4 fix may still use the fast lane; a small fix that changes a contract must go through a change.

**Rationale:** The fast lane's safety comes from a frozen affected-items list and targeted verification, not from the raw number of affected endpoints. Using the tier score would re-introduce the mechanical upgrade problem in a different place.

**Alternatives considered:** L4 + a hard numeric ceiling (rejected: re-creates the “simple bug suddenly not simple” problem); L4 without user confirmation (rejected: the user should see the affected scope before bypassing design review).

### D4: One fast-lane implementation, two workspace roots

**Decision:** `kflow-bug-fix` fast lane resolves a workspace root from the triage output. The rest of the fast lane (root-cause binary, three-attempt limit, regression test at the correct seam, targeted verification, quick closeout) is shared.

**Rationale:** Duplicating the fast lane for project and change scopes would drift. The only scope-dependent behavior is path resolution and the archive/audit relationship.

### D5: Verification targets, not only test-case IDs

**Decision:** The affected-items list contains verification targets of three kinds: existing automated tests, new regression tests, and manual verification steps. Coverage is measured over this list.

**Rationale:** A project-level defect may have no KFlow `api-tests/` or `e2e-tests/` artifacts. Requiring test-case IDs would make the project-level fast lane unusable in mature projects. The existing “Regression Test at Correct Seam” requirement already provides the fallback.

**Constraint:** The fast lane still SHALL NOT run the full test suite, and the affected-items list is frozen by triage.

### D6: Archive gate reads the project-level blocking-defect index

**Decision:** `kflow-archive` reads `docs/bugs/index.md` and blocks on open 🔴 defects. Missing index means the gate passes.

**Rationale:** The existing triage spec already says blocking defects block archive, but the archive gate does not read `bugs/`. Extending the gate to the project-level registry closes that inconsistency. Missing index is treated as “no project-level defects”, which preserves behavior for projects that never use the workspace.

**Trade-off:** A blocking defect unrelated to the change being archived will still block. This is intentional: a blocking defect is a product-level stop signal. If this proves too strict, a later change can add a user-waiver with a recorded rationale.

## Risks / Trade-offs

- **[Misattribution]** A defect is linked to the wrong change, so the wrong test scope is used. → Ask the user when attribution is ambiguous; record the rationale; the “分诊失效” rule re-opens triage when the actual scope expands.
- **[Fast lane overreach]** A fix that looks implementation-only actually needs a contract change. → The fast lane forbids design-artifact edits; discovering a contract change forces a return to triage and a change path.
- **[Bypassing change audit]** Project-level fixes do not go through change audit. → Quick-closeout checks (100% affected-item coverage, verification report, no placeholders) remain mandatory; archive blocking defects are still gated.
- **[Duplicate registries]** Project-level and change-level `bugs/` could confuse users. → A/B path rule is explicit: user-reported → project-level; test-stage failure → change-level; cross-workspace references use `path + BUG-ID`.
- **[Reference drift]** Many skills carry copies of `references/state-values.md` and `references/gates.md`. → Edit `references-src/` first, regenerate the slice manifest, run `scripts/sync-references.sh`, and validate.
- **[No version bump for standalone fixes]** A project-level fix does not trigger KFlow change archive. → Treated as an open question; the project's own release process can consume `docs/bugs/index.md`.

## Migration Plan

1. Add project-level bug templates and update the templates index.
2. Update `kflow-guide`, `kflow-bug-triage`, `kflow-bug-fix`, and `kflow-archive` SKILL.md and references.
3. Update `references-src/` shared references and regenerate slices.
4. Update design documents (`docs/designs/skills/...`, `core-mechanisms/...`).
5. Run `openspec validate`, front-matter validation, and `scripts/sync-references.sh` checks.
6. No data migration: existing change-level `bugs/` and `bugfix-status.md` remain valid; readers accept both roots.

## Open Questions

- Should a project-level defect fix participate in the project's release/versioning process? This can be answered without changing the specs or the task breakdown; the current design leaves release handling to the project.
