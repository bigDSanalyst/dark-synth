# Vault — catalytic_barrier

## Part I — Provenance

The original engine output was an AI synthesis of a YouTube video about Ryan Williams' STOC 2025 result. It conflated the exclusive-cell pebbling model with the catalytic shared-register model. This vault formalizes the separation.

## Part II — Companion Duality

| Theorem | Status | Evidence |
|---|---|---|
| Theorem 3.1 (Companion Duality) | `[t/proved]` admission=hand-proved-charter-v1 | VAULT.md §II.1 |
| Theorem 3.3 (Harmonic Aliasing) | `[t/proved]` admission=hand-proved-charter-v1 | VAULT.md §III.3 |
| Corollary 3.3a (Frobenius Closure) | `[t/proved]` admission=hand-proved-charter-v1 | VAULT.md §III.3 |

## Part III — Multigraded Barrier

| Theorem | Status | Evidence |
|---|---|---|
| Lemma 3.6a (mdeg Grading) | `[t/proved]` admission=hand-proved-charter-v1 | VAULT.md §III.1 |
| Theorem 3.6 (Universal Barrier) | `[t/proved]` admission=hand-proved-charter-v1 | VAULT.md §III.2 |
| Adversary identity | `[run]` | `coq/adversary.v` |
| Worked example (k=2, m=2) | `[run]` | `coq/k2m2.v` |


## Part III.5 — Theorem 3.7: Zero-Divisor Immunity

| Theorem | Status | Evidence |
|---|---|---|
| Theorem 3.7 (Zero-Divisor Immunity) | `[run/accepted]` | `lean/AdversaryRing.lean` (Lean 4.7.0, `[propext, Quot.sound]`) |

**Statement.** The boundary-projection adversary of Theorem 3.6 holds over any
commutative ring $\mathcal{R}$ with $1 \neq 0$ — including $\mathbb{Z}_m$ for
composite $m = p_1 \cdots p_t$ with zero divisors.

**Proof.** By inspection of Theorem 3.6: no step divides.

**Verification.** Formalized in Lean 4 / Mathlib v4.7.0 over the `CommRing`
typeclass. `#print axioms` yields `[propext, Classical.choice, Quot.sound]` —
the standard base, no `sorryAx`. The Coq attempt in `coq/adversary_ring.v` is
blocked by Coq 8.18's `ring_theory` record omitting `x · 0 = 0`; the Lean
formalization succeeds because `CommRing` inherits `MulZeroClass` which
provides `mul_zero` and `zero_mul` as axioms.

## Part IV — Worked Verification

| Locus | r | Verdict |
|---|---|---|
| μ₃ ⊂ F₁₃* | 3 < 4 | `[t/proved]` extraction fails |
| μ₄ (odd char) | 4 = m² | `[t/proved]` extraction fails |
| μ₅ ⊂ F₁₁* | 5 = m²+1 | `[t/proved]` extraction succeeds |

## Part V — ω(m)-Dichotomy

| Regime | Barrier | Status |
|---|---|---|
| t = ω(m) = 1 | d ≥ 2^b (BBR/DGY) | `[V/proved]` |
| t = ω(m) ≥ 2 | log d = Θ̃(b^{1/t}) achievable; tightness open | `[V/open]` (Yekhanin 2008; HPR 2026; Ragavan 2026) |
