import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SupportClassSaturation

def Injective {A B : Type} (f : A → B) : Prop := ∀ a b, f a=f b → a=b

/-- Disjoint cancellation components supply an original-owner witness whose
component is the paid virtual alpha itself. -/
theorem component_witness_injective {D O : Type} (owner : D → O) (component : O → D)
    (belongs : ∀ d, component (owner d)=d) : Injective owner := by
  intro a b same
  exact (belongs a).symm.trans ((congrArg component same).trans (belongs b))

def reassigned {D O R K : Type} (old : D → R) (owner : D → O) (cls : R → K)
    (saturated : K → Prop) [DecidablePred saturated] (select : K → O → R) (d : D) : R :=
  if saturated (cls (old d)) then select (cls (old d)) (owner d) else old d

theorem reassigned_same_class {D O R K : Type} (old : D → R) (owner : D → O)
    (cls : R → K) (saturated : K → Prop) [DecidablePred saturated]
    (select : K → O → R) (eligible : O → K → Prop)
    (witness : ∀ d, eligible (owner d) (cls (old d)))
    (selectedClass : ∀ k o, eligible o k → cls (select k o)=k) (d : D) :
    cls (reassigned old owner cls saturated select d)=cls (old d) := by
  unfold reassigned
  split
  · exact selectedClass _ _ (witness d)
  · rfl

/-- Arbitrary finite size is not needed for the injection exchange itself.
Finite cardinality supplies selectors in the written saturation proof. -/
theorem reassigned_injective {D O R K : Type} (old : D → R) (owner : D → O)
    (cls : R → K) (saturated : K → Prop) [DecidablePred saturated]
    (select : K → O → R) (eligible : O → K → Prop)
    (oldDistinct : Injective old) (ownerDistinct : Injective owner)
    (witness : ∀ d, eligible (owner d) (cls (old d)))
    (selectedClass : ∀ k o, eligible o k → cls (select k o)=k)
    (selectedDistinct : ∀ k o p, eligible o k → eligible p k →
      select k o=select k p → o=p) :
    Injective (reassigned old owner cls saturated select) := by
  intro a b same
  have ca := reassigned_same_class old owner cls saturated select eligible witness selectedClass a
  have cb := reassigned_same_class old owner cls saturated select eligible witness selectedClass b
  have classes : cls (old a)=cls (old b) :=
    ca.symm.trans ((congrArg cls same).trans cb)
  by_cases ha : saturated (cls (old a))
  · have hb : saturated (cls (old b)) := classes ▸ ha
    apply ownerDistinct a b
    apply selectedDistinct (cls (old b)) (owner a) (owner b)
    · simpa only [classes] using witness a
    · exact witness b
    · simpa only [reassigned, if_pos ha, if_pos hb, classes] using same
  · have hb : ¬ saturated (cls (old b)) := by
      intro yes
      exact ha (classes.symm ▸ yes)
    apply oldDistinct a b
    simpa only [reassigned, if_neg ha, if_neg hb] using same

theorem reassigned_supported {D O R K : Type} (old : D → R) (owner : D → O)
    (cls : R → K) (saturated : K → Prop) [DecidablePred saturated]
    (select : K → O → R) (eligible : O → K → Prop) (support : O → R → Prop)
    (witness : ∀ d, eligible (owner d) (cls (old d)))
    (oldSupport : ∀ d, support (owner d) (old d))
    (selectedSupport : ∀ k o, eligible o k → support o (select k o)) (d : D) :
    support (owner d) (reassigned old owner cls saturated select d) := by
  unfold reassigned
  split
  · exact selectedSupport _ _ (witness d)
  · exact oldSupport d

def pairSelect {O R : Type} [DecidableEq O] (left : O) (x y : R) (o : O) : R :=
  if o=left then x else y

theorem two_owner_selector_injective {O R : Type} [DecidableEq O]
    (left right : O) (x y : R) (resourcesDistinct : x ≠ y)
    (a b : O) (ha : a=left ∨ a=right) (hb : b=left ∨ b=right)
    (same : pairSelect left x y a=pairSelect left x y b) : a=b := by
  by_cases al : a=left
  · by_cases bl : b=left
    · exact al.trans bl.symm
    · have impossible : x=y := by simpa [pairSelect, al, bl] using same
      exact False.elim (resourcesDistinct impossible)
  · by_cases bl : b=left
    · have impossible : y=x := by simpa [pairSelect, al, bl] using same
      exact False.elim (resourcesDistinct impossible.symm)
    · exact (ha.resolve_left al).trans (hb.resolve_left bl).symm

theorem two_owner_selector_values {O R : Type} [DecidableEq O]
    (left right : O) (ownersDistinct : left ≠ right) (x y : R) :
    pairSelect left x y left=x ∧ pairSelect left x y right=y := by
  simp [pairSelect, Ne.symm ownersDistinct]

theorem positive_pair_class_unsaturated_iff_singleton (q : Nat) (positive : 0<q) :
    (¬ 2≤q) ↔ q=1 := by omega

/-- The packet adapter supplies the exact ledger. Raw intervals and boundary
marks are retained; the number of compressed support arcs is not substituted. -/
theorem full_compensation_packet_margin (halfArea selected matching raw boundary beta alpha : Nat)
    (boundary_le : boundary ≤ raw)
    (ledger : halfArea+alpha=selected+matching+raw+beta)
    (full : alpha ≤ raw-boundary+beta) :
    selected+matching+boundary ≤ halfArea := by omega

#print axioms component_witness_injective
#print axioms reassigned_same_class
#print axioms reassigned_injective
#print axioms reassigned_supported
#print axioms two_owner_selector_injective
#print axioms two_owner_selector_values
#print axioms positive_pair_class_unsaturated_iff_singleton
#print axioms full_compensation_packet_margin

end SubQuorum.SupportClassSaturation
