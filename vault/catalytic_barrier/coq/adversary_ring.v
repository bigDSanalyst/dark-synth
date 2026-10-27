Require Import Coq.setoid_ring.Ring_theory.
Require Import Coq.setoid_ring.Ring.
Require Import Coq.Classes.RelationClasses.
Require Import Coq.Classes.Morphisms.

Section CommutativeRingAdversary.
  Variable R : Type.
  Variable rO rI : R.
  Variable radd rmul : R -> R -> R.
  Variable rsub : R -> R -> R.
  Variable ropp : R -> R.
  Variable req : R -> R -> Prop.
  Hypothesis R_ring : ring_theory rO rI radd rmul rsub ropp req.

  (* Register Equivalence and Proper as instances so Add Ring can find them *)
  Hypothesis R_setoid : Equivalence req.
  Hypothesis R_add_proper : Proper (req ==> req ==> req) radd.
  Hypothesis R_mul_proper : Proper (req ==> req ==> req) rmul.
  Hypothesis R_sub_proper : Proper (req ==> req ==> req) rsub.
  Hypothesis R_opp_proper : Proper (req ==> req) ropp.

  Instance R_eq_inst : Equivalence req := R_setoid.
  Instance R_add_inst : Proper (req ==> req ==> req) radd := R_add_proper.
  Instance R_mul_inst : Proper (req ==> req ==> req) rmul := R_mul_proper.
  Instance R_sub_inst : Proper (req ==> req ==> req) rsub := R_sub_proper.
  Instance R_opp_inst : Proper (req ==> req) ropp := R_opp_proper.

  Infix "+" := radd.
  Infix "*" := rmul.
  Infix "-" := rsub.
  Notation "- x" := (ropp x).
  Infix "==" := req (at level 70, no associativity).

  Add Ring R_ring_inst : R_ring.

  Definition factor (tau_s alpha_i_pow x_s : R) : R :=
    tau_s + alpha_i_pow * x_s.

  Theorem boundary_adversary_D2_ring :
    forall (c_star w1 w2 a1_p1 a1_p2 a2_p1 a2_p2 : R),
      let tau1 := - a1_p1 in
      let tau2 := - a2_p2 in
      c_star * (w1 * (factor tau1 a1_p1 rI * factor tau2 a1_p2 rI) +
                w2 * (factor tau1 a2_p1 rI * factor tau2 a2_p2 rI)) == rO.
  Proof.
    intros. unfold factor. cbv zeta. ring.
  Qed.

  Theorem boundary_adversary_D4_ring :
    forall (c_star w1 w2 w3 w4
            a1_1 a1_2 a1_3 a1_4
            a2_1 a2_2 a2_3 a2_4
            a3_1 a3_2 a3_3 a3_4
            a4_1 a4_2 a4_3 a4_4 : R),
      let t1 := - a1_1 in
      let t2 := - a2_2 in
      let t3 := - a3_3 in
      let t4 := - a4_4 in
      c_star * (
        w1 * (factor t1 a1_1 rI * factor t2 a1_2 rI * factor t3 a1_3 rI * factor t4 a1_4 rI) +
        w2 * (factor t1 a2_1 rI * factor t2 a2_2 rI * factor t3 a2_3 rI * factor t4 a2_4 rI) +
        w3 * (factor t1 a3_1 rI * factor t2 a3_2 rI * factor t3 a3_3 rI * factor t4 a3_4 rI) +
        w4 * (factor t1 a4_1 rI * factor t2 a4_2 rI * factor t3 a4_3 rI * factor t4 a4_4 rI)
      ) == rO.
  Proof.
    intros. unfold factor. cbv zeta. ring.
  Qed.

  Print Assumptions boundary_adversary_D2_ring.
  Print Assumptions boundary_adversary_D4_ring.

End CommutativeRingAdversary.
