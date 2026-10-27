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
