# Mutation Matrix — catalytic_barrier

| Mutant | Bug put back | Current test | Catches? | Gap |
|---|---|---|---|---|
| M-A1 | τ-homogeneity in Lemma 3.6a | `adversary.v` | No | `[hand-audit-only]` — general statement over all F; k=2, m=2 doesn't falsify |
| M-A2 | Revert target to "extract C_degF" | None | No | `[hand-audit-only]` — target instruction, not identity |
| M-A3 | Use S-projection only | `k2m2.v` (specific) | No | `[hand-audit-only]` — counterexample not mechanized |
| M-A4 | Weaken adversary (drop a_s exponent) | `adversary.v` | **Yes** | Coq-verified |
| M-A5 | Revert theorem target | None | No | `[hand-audit-only]` |

**Honest count:** 1 of 5 mutants caught. A4 is mechanized; A1, A2, A3, A5 are `[hand-audit-only]` with reasons stated.
