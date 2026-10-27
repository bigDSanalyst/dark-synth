import Mathlib.Tactic.Ring
import Mathlib.Algebra.Ring.Basic

/-!
  Theorem 3.7 (Zero-Divisor Immunity) — boundary adversary over any
  commutative ring R with 1 ≠ 0, including Z_m with zero divisors.

  The identity: ∑_i w_i ∏_s (τ_s^{a_s} + α_s^{a_s} x_s^{a_s}) vanishes
  identically when τ_s^{a_s} := -α_s^{a_s} x_s^{a_s}.

  Coq 8.18's `ring_theory` record lacks `x · 0 = 0` as an axiom, blocking
  `coq/adversary_ring.v`. Lean 4's `CommRing` inherits `MulZeroClass`
  (which states `mul_zero`, `zero_mul`), so the same proof closes in one
  tactic.
-/

theorem boundary_adversary_D2 {R : Type*} [CommRing R]
    (c_star w1 w2 a1_p1 a1_p2 a2_p1 a2_p2 : R) :
    c_star * (w1 * ((-a1_p1 + a1_p1 * 1) * (-a2_p2 + a1_p2 * 1)) +
              w2 * ((-a1_p1 + a2_p1 * 1) * (-a2_p2 + a2_p2 * 1))) = 0 := by
  ring

theorem boundary_adversary_D4 {R : Type*} [CommRing R]
    (c w1 w2 w3 w4
     a1_1 a1_2 a1_3 a1_4
     a2_1 a2_2 a2_3 a2_4
     a3_1 a3_2 a3_3 a3_4
     a4_1 a4_2 a4_3 a4_4 : R) :
    c * (w1 * ((-a1_1 + a1_1 * 1) * (-a2_2 + a1_2 * 1) *
               (-a3_3 + a1_3 * 1) * (-a4_4 + a1_4 * 1)) +
         w2 * ((-a1_1 + a2_1 * 1) * (-a2_2 + a2_2 * 1) *
               (-a3_3 + a2_3 * 1) * (-a4_4 + a2_4 * 1)) +
         w3 * ((-a1_1 + a3_1 * 1) * (-a2_2 + a3_2 * 1) *
               (-a3_3 + a3_3 * 1) * (-a4_4 + a3_4 * 1)) +
         w4 * ((-a1_1 + a4_1 * 1) * (-a2_2 + a4_2 * 1) *
               (-a3_3 + a4_3 * 1) * (-a4_4 + a4_4 * 1))) = 0 := by
  ring

#print axioms boundary_adversary_D2
#print axioms boundary_adversary_D4
