import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false

namespace SubQuorum.FrozenGapRetraction

def uniqueOccupied {V : Type} (T O : V → Prop) (adj : V → V → Prop) : Prop :=
  ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y

/-- Actual isolated added selections preserve the full selection feasibility
condition. The geometry must establish isolation, not assume a new budget. -/
theorem isolated_selection_extension {V : Type} (T O X : V → Prop)
    (adj : V → V → Prop) (symmetric : ∀ a b, adj a b → adj b a)
    (selectedOccupied : ∀ t, T t → O t)
    (oldFeasible : uniqueOccupied T O adj)
    (isolate : ∀ x, X x → ∀ y, O y ∨ X y → ¬ adj x y) :
    uniqueOccupied (fun v => T v ∨ X v) (fun v => O v ∨ X v) adj := by
  intro t ht a ha hta b hb htb
  rcases ht with ht | ht
  · have oldA : O a := by
      rcases ha with h | h
      · exact h
      · exact False.elim (isolate a h t (Or.inl (selectedOccupied t ht))
          (symmetric t a hta))
    have oldB : O b := by
      rcases hb with h | h
      · exact h
      · exact False.elim (isolate b h t (Or.inl (selectedOccupied t ht))
          (symmetric t b htb))
    exact oldFeasible t ht a oldA hta b oldB htb
  · exact False.elim (isolate t ht a ha hta)

theorem old_occupied_neighbors_unchanged {V : Type} (O X : V → Prop)
    (adj : V → V → Prop) (symmetric : ∀ a b, adj a b → adj b a)
    (isolate : ∀ x, X x → ∀ y, O y → ¬ adj x y)
    (v : V) (old : O v) (w : V) :
    ((O w ∨ X w) ∧ adj v w) ↔ (O w ∧ adj v w) := by
  constructor
  · intro h
    rcases h.1 with ho | hx
    · exact ⟨ho,h.2⟩
    · exact False.elim (isolate w hx v old (symmetric v w h.2))
  · intro h
    exact ⟨Or.inl h.1,h.2⟩

theorem surviving_link_value (k c : Nat) (kept : k≤2) :
    2-k+min k c=2-(k-c) := by omega

theorem per_copy_retraction_identity (k c : Nat) (kept : k≤2) :
    k-c=(2-c)-(2-k) := by omega

theorem per_copy_retraction_lower_bound (k c : Nat) (kept : k≤2) :
    2-c≤(k-c)+(2-k) := by omega

def initialDeficit (profile : List (Nat × Nat)) : Nat :=
  (profile.map fun p => 2-p.2).sum
def remainingDeficit (profile : List (Nat × Nat)) : Nat :=
  (profile.map fun p => p.1-p.2).sum
def releasedCount (profile : List (Nat × Nat)) : Nat :=
  (profile.map fun p => 2-p.1).sum

/-- Different profile entries represent disjoint copies in the application.
Their physical identities and support separation are checked separately. -/
theorem global_retraction_lower_bound (profile : List (Nat × Nat))
    (kept : ∀ p ∈ profile, p.1≤2) :
    initialDeficit profile≤remainingDeficit profile+releasedCount profile := by
  induction profile with
  | nil => simp [initialDeficit,remainingDeficit,releasedCount]
  | cons p rest ih =>
    have hp := per_copy_retraction_lower_bound p.1 p.2 (kept p (by simp))
    have hr := ih (by intro x hx; exact kept x (by simp [hx]))
    simp only [initialDeficit,remainingDeficit,releasedCount,List.map_cons,List.sum_cons] at *
    omega

theorem budget_remaining_lower_bound (D remaining released budget : Nat)
    (localToGlobal : D≤remaining+released) (allowed : released≤budget) :
    D-budget≤remaining := by omega

/-- Repair tokens are actual original links; a prefix cannot select a link
twice. This is not a creation of interval resources. -/
theorem labelled_repair_prefix {L : Type} (tokens : List L) (distinct : tokens.Nodup)
    (budget : Nat) :
    (tokens.take budget).Nodup ∧ (tokens.take budget).length=min budget tokens.length := by
  exact ⟨distinct.take (i:=budget),List.length_take⟩

theorem exact_budget_arithmetic (q D budget : Nat) (capacity : D≤2*q) :
    (2*q-D)+min budget D=2*q-(D-budget) := by omega

theorem full_payment_needs_all_deficit_releases (D budget : Nat)
    (full : D-budget=0) : D≤budget := by omega

theorem one_unit_per_copy_frontier (q budget : Nat) :
    2*q-(q-budget)=q+min budget q := by omega

theorem one_copy_selection_count (w c : Nat) (width : 30≤w) (cap : c≤w-20) :
    42+(w-20-c)=w+22-c := by omega

theorem one_copy_half_area_margin (w c : Nat) (width : 30≤w) (cap : c≤w-20) :
    7*w-((w+22-c)+20)=6*w-42+c ∧ 0<6*w-42+c := by omega

abbrev Point := Nat × Nat
def adjacent (v w : Point) : Prop :=
  (v.1=w.1 ∧ (v.2+1=w.2 ∨ w.2+1=v.2)) ∨
  (v.2=w.2 ∧ (v.1+1=w.1 ∨ w.1+1=v.1))

theorem alternating_new_selections_nonadjacent (c d : Nat) :
    ¬ adjacent (6+c%2,c) (6+d%2,d) := by
  simp only [adjacent]
  omega

theorem last_filled_selection_row (w : Nat) (width : 30≤w) (even : w%2=0) :
    6+(w-11)%2=7 := by omega

#print axioms isolated_selection_extension
#print axioms old_occupied_neighbors_unchanged
#print axioms surviving_link_value
#print axioms per_copy_retraction_identity
#print axioms per_copy_retraction_lower_bound
#print axioms global_retraction_lower_bound
#print axioms budget_remaining_lower_bound
#print axioms labelled_repair_prefix
#print axioms exact_budget_arithmetic
#print axioms full_payment_needs_all_deficit_releases
#print axioms one_unit_per_copy_frontier
#print axioms one_copy_selection_count
#print axioms one_copy_half_area_margin
#print axioms alternating_new_selections_nonadjacent
#print axioms last_filled_selection_row

end SubQuorum.FrozenGapRetraction
