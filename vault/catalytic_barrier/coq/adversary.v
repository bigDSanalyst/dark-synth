Require Import ZArith Lia Ring.
Open Scope Z_scope.

(* Local power function. Independent of the stdlib's Z.pow signature,
   which differs between Coq builds labeled the same version. *)
Fixpoint zpow_nat (x : Z) (n : nat) : Z :=
  match n with
  | O => 1
  | S k => x * zpow_nat x k
  end.

Fixpoint prod_range (f : nat -> Z) (n : nat) : Z :=
  match n with
  | O => 1
  | S k => f k * prod_range f k
  end.

Fixpoint sum_range (f : nat -> Z) (n : nat) : Z :=
  match n with
  | O => 0
  | S k => f k + sum_range f k
  end.

Lemma prod_range_zero_of_factor_zero :
  forall (D s0 : nat) (f : nat -> Z),
    Nat.lt s0 D -> f s0 = 0 -> prod_range f D = 0.
Proof.
  intros D. induction D as [| D' IH].
  - intros s0 f Hlt Hf. lia.
  - intros s0 f Hlt Hf. simpl.
    destruct (Nat.eq_dec s0 D') as [Heq | Hne].
    + subst. rewrite Hf. ring.
    + assert (Hlt' : Nat.lt s0 D') by lia.
      rewrite (IH s0 f Hlt' Hf). ring.
Qed.

Lemma adversary_sum_zero :
  forall (r D : nat) (alpha : nat -> Z) (a : nat -> nat) (w : nat -> Z),
    Nat.le r D ->
    sum_range (fun i =>
      w i * prod_range (fun s =>
        zpow_nat (alpha i) (a s) - zpow_nat (alpha s) (a s)) D) r = 0.
Proof.
  intros r. induction r as [| r' IH]; intros D alpha a w HrD.
  - reflexivity.
  - simpl. rewrite (IH D alpha a w) by lia.
    assert (Hr' : Nat.lt r' D) by lia.
    assert (Hprod :
      prod_range (fun s =>
        zpow_nat (alpha r') (a s) - zpow_nat (alpha s) (a s)) D = 0).
    { apply prod_range_zero_of_factor_zero with (s0 := r').
      - exact Hr'.
      - ring. }
    rewrite Hprod. ring.
Qed.

Corollary adversary_contradiction :
  forall (r D : nat) (alpha : nat -> Z) (a : nat -> nat) (w : nat -> Z)
         (c_gamma : Z),
    Nat.le r D -> c_gamma <> 0 ->
    sum_range (fun i =>
      w i * prod_range (fun s =>
        zpow_nat (alpha i) (a s) - zpow_nat (alpha s) (a s)) D) r = c_gamma ->
    False.
Proof.
  intros r D alpha a w c_gamma HrD Hc Hsum.
  rewrite (adversary_sum_zero r D alpha a w HrD) in Hsum.
  apply Hc. symmetry. exact Hsum.
Qed.

Print Assumptions adversary_sum_zero.
Print Assumptions adversary_contradiction.
