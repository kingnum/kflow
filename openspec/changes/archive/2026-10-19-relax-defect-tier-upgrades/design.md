# Design

## Context

See `proposal.md` for motivation. The current tier logic has two mechanical upgrade paths:

- `kflow-design` DIVIDE: lightweight + mixed backend/frontend FP types → forced upgrade to `标准`.
- `kflow-design` TIER_RECHECK: `FP × 1 + interfaces × 1.5 + data model changes × 2 > 3` → request upgrade. “Interfaces” is not defined precisely and is commonly read as “affected endpoints”, which makes contract-preserving defect fixes cross the threshold.

The result is that a small defect repeatedly becomes a standard change. The tier should measure how much design surface the change touches, not how much code it affects.

## Goals / Non-Goals

**Goals:**

- Make the tier score measure design surface: new/modified contracts and schema changes.
- Keep the triage impact list as the blast-radius measure for verification, separate from the tier.
- Allow a lightweight change to contain one backend and one frontend subchange.
- Replace mechanical upgrade prompts with hard/soft upgrade categories and a necessity check.
- Remove stale three-tier remnants.

**Non-Goals:**

- Changing the tier thresholds (`<=3` / `>3`).
- Allowing downgrade after an upgrade.
- Changing design-review or code-review modes per tier.
- Changing the fast-lane path selection (covered by `route-simple-defects-to-fast-lane`).

## Decisions

### D1: Two measures, two purposes

**Decision:** Introduce an explicit separation:

| Measure | Purpose | Inputs |
|---------|---------|--------|
| Design-surface score | Tier classification | FP count, new/modified contracts, schema/migration count |
| Blast-radius list | Verification scope and rollback scope | Affected FPs, affected endpoints, affected tests |

The field name “影响范围分数” remains in `.status.md` for compatibility, but its definition becomes the design-surface score. The triage impact assessment remains the blast-radius list and score.

**Rationale:** The tier controls review form and test-stage inclusion. Those are costs driven by how much design/test surface must change. A defect that affects many endpoints but changes no contract still needs targeted verification, not a full re-design. Conversely, a single contract change can affect consumers and warrants standard handling.

**Alternative considered:** Keep the blast-radius formula and raise the threshold for defects (rejected: type-specific exception, and it still conflates the two concepts).

### D2: Define “interface count” as contract changes

**Decision:** `接口契约变更数` counts only APIs whose contract is added or modified in this change. Affected-but-unchanged endpoints are excluded. `数据模型变更数` counts schema/migration changes only; data corrections are excluded.

**Rationale:** This is a definitional clarification, not a defect-specific exception. It applies to all change types and preserves the “no type-specific mapping” principle.

**Risk:** A change might modify implementation behavior in a way that affects consumers without changing the contract (e.g., response semantics). Mitigation: the triage blast-radius list still captures affected endpoints and verification targets; the review still inspects behavior even in lightweight mode.

### D3: Lightweight allows one backend and one frontend subchange

**Decision:** Lightweight subchange count is 1 or 2. Mixed FP types produce exactly two subchanges: backend first, frontend depending on the backend API contract. A minimal division table replaces full DIVIDE dependency analysis. If two subchanges cannot hold the FPs (e.g., a subchange would exceed 10 FPs), upgrade to standard.

**Rationale:** The original single-subchange rule was a simplification to skip DIVIDE, not a safety property. The subchange type dichotomy (backend/frontend) is a real constraint, but it can be satisfied with two subchanges. This removes the forced upgrade for small full-stack work.

**Alternative considered:** Introduce a “full-stack subchange” type (rejected: breaks the test-stage assignment and type validation model).

### D4: Hard vs soft upgrades

**Decision:**

- **Hard upgrade** (no decline): data migration, breaking interface-contract change, cross-change contract impact.
- **Soft upgrade** (default stay lightweight, user may opt in): non-hard cases where the recomputed tier is higher.
- **Necessity check:** only prompt if the upgrade would add at least one downstream test stage that would otherwise be `⏭️ 不适用`, or if it is a hard upgrade. Otherwise stay lightweight and record the reason.

**Rationale:** The current rule asks the user every time the formula crosses the threshold, even when the upgrade only increases review parallelism and adds no tests. That is the “mechanical” behavior the user experiences. The hard/soft split preserves safety where it matters (schema/contract) and returns control where it does not.

### D5: Refuse soft upgrade, record and continue

**Decision:** If the user declines a soft upgrade, the change stays lightweight, the rationale is written to `.status.md`, and downstream stages do not re-prompt. No downgrade is introduced; this is a decision not to upgrade, not a downgrade.

**Rationale:** The current spec does not define what happens when the user declines, which leads to inconsistent behavior. Recording the decision keeps auditability.

### D6: Clean up three-tier remnants

**Decision:** Update `docs/designs/skills/kflow-design.md` and the `change-tier-classification` spec to remove `4~15 / >15 / 完整` language. Keep the historical `完整` read-side merge to `标准`.

**Rationale:** Stale three-tier language causes inconsistent implementation and repeated misreads during changes.

## Risks / Trade-offs

- **[Under-testing]** A contract-preserving fix with wide behavioral impact stays lightweight. → The triage blast-radius list still drives targeted verification; the review checks behavior; hard upgrade triggers on contract/schema changes.
- **[Contract ambiguity]** A change modifies response semantics without changing the declared contract. → The design stage should record semantic changes as contract changes; reviewers should treat them as such. A follow-up change can add a semantic-change signal if needed.
- **[Two-subchange planning overhead]** Lightweight now has a minimal DIVIDE step. → The table is capped at two rows and skips full dependency analysis; the overhead is small compared with a forced standard flow.
- **[User declines a needed upgrade]** → Only soft upgrades are declineable; hard upgrades (schema/contract) remain mandatory. The decision is recorded for audit.
- **[Reference drift]** The tier description appears in many generated references. → Edit `references-src/`, regenerate the slice manifest, run `scripts/sync-references.sh`, and validate.

## Migration Plan

1. Update `skills/kflow-design/SKILL.md` DIVIDE and TIER_RECHECK sections.
2. Update `skills/kflow-explore/SKILL.md` initial-tier wording to reference the design-surface score and the two-subchange allowance.
3. Update `references-src/state-values.md`, `gates.md`, and `phase-transition.md`; regenerate slices.
4. Update design documents and the stale three-tier passages.
5. Run `openspec validate`, front-matter validation, and `scripts/sync-references.sh`.
6. No data migration: historical `完整` values are still read as `标准`; already-upgraded changes are not downgraded.

## Open Questions

None that affect the specs or task breakdown.
