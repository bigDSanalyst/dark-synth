# The Six-Phase Scaffold

## Phase 0 — Intake
Restate in one sentence. Identify source and provenance. Tag. Refuse if not
falsifiable.

## Phase 1 — Formalization
State objects, quantifiers, domain. Flag terms and homonym risks. Choose track.

## Phase 2 — Audit
Run each failure mode from FAILURE_MODES.md. FM5 (paste artifact) requires
grep, not eyes.

## Phase 3 — Attempt
Close each flag or state a weaker version. Tag `[t/proved]` / `[t/open]` /
`[t/refuted]`.

## Phase 4 — Verify
Kernel-check every Coq/Lean file. Record sha256. Run the doctor.

## Phase 5 — Merge
Every claim tagged. Every tag matches status. Every claim carries artifact,
track, and scope. tag_lint exits 0. doctor prints ok.

## Phase 6 — Publish or Stop
Identify venue. Identify the referee's most likely objection. Fix it or name
it in Limits. Stop polishing.
