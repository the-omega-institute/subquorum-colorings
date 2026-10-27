import Lean.Elab.Tactic.Omega

/-! Contact-word kernels. True labels TT leaves and false labels HH leaves.
The original path-fragment/physical-resource adapter remains a written proof.
-/
set_option autoImplicit false
namespace SubQuorum.SharedTHStar

def tt (previous : Bool) : List Bool → Nat
  | [] => 0
  | b :: bs => (if previous && b then 1 else 0) + tt b bs

def hh (previous : Bool) : List Bool → Nat
  | [] => 0
  | b :: bs => (if !previous && !b then 1 else 0) + hh b bs

def th (previous : Bool) : List Bool → Nat
  | [] => 0
  | b :: bs => (if previous == b then 0 else 1) + th b bs

def Alternating (previous : Bool) : List Bool → Prop
  | [] => True
  | b :: bs => previous ≠ b ∧ Alternating b bs

theorem edge_partition (previous : Bool) (word : List Bool) :
    tt previous word + hh previous word + th previous word = word.length := by
  induction word generalizing previous with
  | nil => simp [tt, hh, th]
  | cons b bs ih =>
      have h := ih b
      cases previous <;> cases b <;> simp [tt, hh, th] at * <;> omega

theorem no_monochrome_iff (previous : Bool) (word : List Bool) :
    (tt previous word = 0 ∧ hh previous word = 0) ↔ Alternating previous word := by
  induction word generalizing previous with
  | nil => simp [tt, hh, Alternating]
  | cons b bs ih =>
      have h := ih b
      cases previous <;> cases b <;> simp_all [tt, hh, Alternating]

def pairedWord : Nat → List Bool
  | 0 => []
  | n+1 => false :: true :: pairedWord n

theorem paired_counts (n : Nat) :
    tt true (pairedWord n ++ [false]) = 0 ∧
    hh true (pairedWord n ++ [false]) = 0 ∧
    th true (pairedWord n ++ [false]) = 2*n+1 := by
  induction n with
  | zero => simp [pairedWord, tt, hh, th]
  | succ n ih => simp [pairedWord, tt, hh, th] at *; omega

theorem true_run (n : Nat) (tail : List Bool) :
    tt true (List.replicate n true ++ tail) = n + tt true tail ∧
    hh true (List.replicate n true ++ tail) = hh true tail ∧
    th true (List.replicate n true ++ tail) = th true tail := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ, tt, hh, th] at *; omega

theorem false_run (n : Nat) (tail : List Bool) :
    tt false (List.replicate n false ++ tail) = tt false tail ∧
    hh false (List.replicate n false ++ tail) = n + hh false tail ∧
    th false (List.replicate n false ++ tail) = th false tail := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ, tt, hh, th] at *; omega

/-- With s=n+1 leaves of each type, the blocked contact order leaves n bad
pairs, although every HH contact precedes every TT contact. -/
theorem blocked_counts (n : Nat) :
    let word := List.replicate (n+1) false ++ List.replicate (n+1) true ++ [false]
    tt true word = n ∧ hh true word = n ∧ th true word = 3 := by
  dsimp only
  have hf := false_run n (List.replicate (n+1) true ++ [false])
  have ht := true_run n [false]
  simp only [List.replicate_succ, List.cons_append, List.append_assoc] at *
  simp [tt, hh, th] at *
  omega

/-- The endpoint-incidence equations are supplied by the written fragment
theorem; this arithmetic kernel identifies the balanced residual defect. -/
theorem balanced_defects (a b c s : Nat)
    (tIncidence : 2*a+c=2*s+1) (hIncidence : 2*b+c=2*s+1) :
    a=b ∧ c=2*s+1-2*a := by omega

end SubQuorum.SharedTHStar
#print axioms SubQuorum.SharedTHStar.edge_partition
#print axioms SubQuorum.SharedTHStar.no_monochrome_iff
#print axioms SubQuorum.SharedTHStar.paired_counts
#print axioms SubQuorum.SharedTHStar.true_run
#print axioms SubQuorum.SharedTHStar.false_run
#print axioms SubQuorum.SharedTHStar.blocked_counts
#print axioms SubQuorum.SharedTHStar.balanced_defects
