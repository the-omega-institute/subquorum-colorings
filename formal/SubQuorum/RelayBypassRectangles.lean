import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.RelayBypassRectangles

def Injective {A B : Type} (f : A → B) : Prop :=
  ∀ x y, f x = f y → x = y

def NoHole {A R : Type} (cover : A → R → Prop) (c : Nat) : Prop :=
  ∀ (sources : Fin (c+1) → A) (units : Fin (c+1) → R),
    Injective sources → Injective units →
    ∃ i j, cover (sources i) (units j)

def initialSegment {c n : Nat} (overload : c < n) (i : Fin (c+1)) : Fin n :=
  ⟨i.val, by have h := i.isLt; omega⟩

theorem initialSegment_injective {c n : Nat} (overload : c < n) :
    Injective (initialSegment overload) := by
  intro x y same
  apply Fin.ext
  exact congrArg (fun z : Fin n => z.val) same

/-- The square criterion supplies a cheap pair at EVERY finite overload,
not just at c+1 total original entrants. Source and unit identities are
separately injective, as required by a projected matching. -/
theorem arbitrary_overload_has_bypass {A R : Type} (cover : A → R → Prop)
    (c n : Nat) (safe : NoHole cover c) (overload : c < n)
    (sources : Fin n → A) (units : Fin n → R)
    (sourceDistinct : Injective sources) (unitDistinct : Injective units) :
    ∃ i j, cover (sources i) (units j) := by
  have hs : Injective (fun i : Fin (c+1) => sources (initialSegment overload i)) := by
    intro i j same
    exact initialSegment_injective overload i j (sourceDistinct _ _ same)
  have hj : Injective (fun i : Fin (c+1) => units (initialSegment overload i)) := by
    intro i j same
    exact initialSegment_injective overload i j (unitDistinct _ _ same)
  obtain ⟨i,j,h⟩ := safe _ _ hs hj
  exact ⟨initialSegment overload i,initialSegment overload j,h⟩

/-- Conversely, the arbitrary-load pair-existence property includes a square
of side c+1. This is the combinatorial iff, before the route/cost adapter. -/
theorem square_criterion_iff {A R : Type} (cover : A → R → Prop) (c : Nat) :
    NoHole cover c ↔
      ∀ (n : Nat), c < n → ∀ (sources : Fin n → A) (units : Fin n → R),
        Injective sources → Injective units → ∃ i j, cover (sources i) (units j) := by
  constructor
  · intro safe n large sources units hs hj
    exact arbitrary_overload_has_bypass cover c n safe large sources units hs hj
  · intro every sources units hs hj
    exact every (c+1) (by omega) sources units hs hj

theorem empty_square_refutes_uniform_criterion {A R : Type}
    (cover : A → R → Prop) (c : Nat)
    (sources : Fin (c+1) → A) (units : Fin (c+1) → R)
    (hs : Injective sources) (hj : Injective units)
    (empty : ∀ i j, ¬ cover (sources i) (units j)) : ¬ NoHole cover c := by
  intro safe
  obtain ⟨i,j,pair⟩ := safe sources units hs hj
  exact empty i j pair

/-- Hereditary criterion on subsets: maps into a safe interface preserve
the criterion if both original identity maps are injective. -/
theorem restrict_safe_interface {A R A' R' : Type}
    (cover : A → R → Prop) (c : Nat) (safe : NoHole cover c)
    (sourceMap : A' → A) (unitMap : R' → R)
    (sourceDistinct : Injective sourceMap) (unitDistinct : Injective unitMap) :
    NoHole (fun a j => cover (sourceMap a) (unitMap j)) c := by
  intro sources units hs hj
  apply safe (fun i => sourceMap (sources i)) (fun i => unitMap (units i))
  · intro i j same
    exact hs i j (sourceDistinct _ _ same)
  · intro i j same
    exact hj i j (unitDistinct _ _ same)

/-- Explicit transposition cost, valid for arbitrary entrant/output terms.
The physical module must supply separability and a genuinely private bypass. -/
theorem cheap_transposition (direct entryA entryB outputJ outputK : Nat)
    (cheap : direct ≤ entryA+outputJ) :
    direct+entryB+outputK ≤ entryA+outputK+entryB+outputJ := by omega

theorem absent_cheap_pair_means_expensive (direct entry output : Nat)
    (notCheap : ¬ direct ≤ entry+output) : entry+output < direct := by omega

/-- Any maximum private matching is in particular unaugmentable by one edge.
The matching adapter must establish the premise from its maximality proof. -/
theorem unmatched_rectangle_empty {A R : Type}
    (cover : A → R → Prop) (unmatchedSource : A → Prop) (unmatchedUnit : R → Prop)
    (noExtension : ¬ ∃ a j, unmatchedSource a ∧ unmatchedUnit j ∧ cover a j) :
    ∀ a j, unmatchedSource a → unmatchedUnit j → ¬ cover a j := by
  intro a j ha hj pair
  exact noExtension ⟨a,j,ha,hj,pair⟩

/-- Exact cardinality and deficiency of the cheap-route subsystem once mu
is the maximum cheap-matching size. Finite matching construction is written. -/
theorem local_payment_and_loss (t c mu : Nat) (mu_le : mu ≤ t) :
    mu+min c (t-mu) = min t (c+mu) ∧
    t-(mu+min c (t-mu)) = t-c-mu := by omega

theorem quota_iff_full_payment (t c mu : Nat) (mu_le : mu ≤ t) :
    mu+min c (t-mu) = t ↔ t-c ≤ mu := by omega

theorem unmatched_defect_is_rectangle_weight (t c mu q : Nat)
    (mu_le : mu ≤ t) (unmatched : q=t-mu) : t-c-mu=q-c := by omega

theorem old_entrant_bound_recovers_one_loss (t c mu : Nat)
    (oldBound : t ≤ c+1) (covered : 1 ≤ mu) : t-c-mu=0 := by omega

/-- A hypothetical costly private route can preserve cardinality without
preserving the projection's cost; this is a cost obstruction only. -/
theorem cost_only_control : min 2 (1+2)=2 ∧ 2+1>2 := by decide

theorem coupled_deficiency_bound (sources projection paid rectangleRank : Nat)
    (projection_le : projection ≤ sources)
    (certificate : projection ≤ paid+rectangleRank) :
    sources-paid ≤ (sources-projection)+rectangleRank := by omega

theorem sharp_family_arithmetic (n c k : Nat) (large : c+k < n) :
    n-(c+k)=n-k-c ∧ c+k+(n-k-c)=n := by omega

#print axioms initialSegment_injective
#print axioms arbitrary_overload_has_bypass
#print axioms square_criterion_iff
#print axioms empty_square_refutes_uniform_criterion
#print axioms restrict_safe_interface
#print axioms cheap_transposition
#print axioms absent_cheap_pair_means_expensive
#print axioms unmatched_rectangle_empty
#print axioms local_payment_and_loss
#print axioms quota_iff_full_payment
#print axioms unmatched_defect_is_rectangle_weight
#print axioms old_entrant_bound_recovers_one_loss
#print axioms cost_only_control
#print axioms coupled_deficiency_bound
#print axioms sharp_family_arithmetic

end SubQuorum.RelayBypassRectangles
