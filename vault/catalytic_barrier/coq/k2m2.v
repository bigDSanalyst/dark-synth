Require Import ZArith Ring.
Open Scope Z_scope.

Lemma C4_nonzero : forall (x1 x2 x3 x4 : Z),
  x1 = 1 -> x2 = 1 -> x3 = 1 -> x4 = 1 ->
  x1 * x2 * x3 * x4 = 1.
Proof. intros. subst. ring. Qed.

Lemma C3_nonzero : forall (t1 t2 t3 t4 : Z),
  t1 = 1 -> t2 = 0 -> t3 = 0 -> t4 = 0 ->
  t1*1*1*1 + t2*1*1*1 + t3*1*1*1 + t4*1*1*1 = 1.
Proof. intros. subst. ring. Qed.

Lemma C2_nonzero : forall (t1 t2 t3 t4 x1 x2 x3 x4 : Z),
  t1 = 0 -> t2 = 0 -> t3 = 1 -> t4 = 1 ->
  x1 = 1 -> x2 = 1 -> x3 = 0 -> x4 = 0 ->
  x1*x2*t3*t4 + x1*x3*t2*t4 + x1*x4*t2*t3
  + x2*x3*t1*t4 + x2*x4*t1*t3 + x3*x4*t1*t2 = 1.
Proof. intros. subst. ring. Qed.

Lemma C1_nonzero : forall (t1 t2 t3 t4 x1 x2 x3 x4 : Z),
  t1 = 0 -> t2 = 1 -> t3 = 1 -> t4 = 1 ->
  x1 = 1 -> x2 = 0 -> x3 = 0 -> x4 = 0 ->
  x1*t2*t3*t4 + x2*t1*t3*t4 + x3*t1*t2*t4 + x4*t1*t2*t3 = 1.
Proof. intros. subst. ring. Qed.

Lemma C0_nonzero : forall (t1 t2 t3 t4 : Z),
  t1 = 1 -> t2 = 1 -> t3 = 1 -> t4 = 1 ->
  t1*t2*t3*t4 = 1.
Proof. intros. subst. ring. Qed.

Print Assumptions C4_nonzero.
Print Assumptions C3_nonzero.
Print Assumptions C2_nonzero.
Print Assumptions C1_nonzero.
Print Assumptions C0_nonzero.
