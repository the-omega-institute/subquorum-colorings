import Lean.Elab.Tactic.Omega

/-! Abstract kernels for the isolated-hole and detour cover note.
The periodic partition, fractional weights and path-resource adapter are written.
-/
namespace SubQuorum.IsolatedHoleDetours

def Adjacent (u v : Nat × Nat) : Prop :=
  (u.1 = v.1 ∧ (u.2 + 1 = v.2 ∨ v.2 + 1 = u.2)) ∨
  (u.2 = v.2 ∧ (u.1 + 1 = v.1 ∨ v.1 + 1 = u.1))

def CoreP (u : Nat × Nat) : Prop :=
  (u.1 = 0 ∧ u.2 = 2) ∨ (u.1 = 1 ∧ u.2 = 2) ∨
  (u.1 = 2 ∧ u.2 = 0) ∨ (u.1 = 2 ∧ u.2 = 1) ∨
  (u.1 = 2 ∧ u.2 = 3) ∨ (u.1 = 2 ∧ u.2 = 4) ∨
  (u.1 = 3 ∧ u.2 = 2) ∨ (u.1 = 4 ∧ u.2 = 2)

theorem centre_neighbour_in_P (u : Nat × Nat)
    (h : Adjacent u (2, 2)) : CoreP u := by
  simp only [Adjacent] at h
  simp only [CoreP]
  omega

/-- Every three-corner selection is excluded by the local degree rule. -/
theorem square_capacity (a b c d : Nat)
    (abc : a+b+c ≤ 2) (bcd : b+c+d ≤ 2)
    (cda : c+d+a ≤ 2) (dab : d+a+b ≤ 2) : a+b+c+d ≤ 2 := by
  omega

def chosen : List (Nat × Nat) → Nat
  | [] => 0
  | x :: xs => x.1 + chosen xs

def capacity : List (Nat × Nat) → Nat
  | [] => 0
  | x :: xs => x.2 + capacity xs

theorem unrestricted_disjoint_capacity (xs : List (Nat × Nat))
    (localBounds : ∀ x ∈ xs, x.1 ≤ x.2) : chosen xs ≤ capacity xs := by
  induction xs with
  | nil => simp [chosen, capacity]
  | cons x xs ih =>
    have hx : x.1 ≤ x.2 := localBounds x (by simp)
    have hr : ∀ y ∈ xs, y.1 ≤ y.2 := by
      intro y hy
      exact localBounds y (by simp [hy])
    have h := ih hr
    simp only [chosen, capacity]
    omega

/-- The geometric colour ledger and mandatory singleton count are hypotheses.
This integer consequence does not formalize the fractional cover argument. -/
theorem singleton_colour_obstruction (singletons isolated : Nat)
    (positive : 0 < isolated) (forced : isolated ≤ singletons)
    (balance : singletons = 0) : False := by omega

theorem exact_mixed_margin (t m area f g b s deficit : Int)
    (partition : area = 2*m+f+2*g+2*b+4*s)
    (capacityBound : t ≤ g+b+2*s)
    (definition : deficit = g+b+2*s-t) :
    0 ≤ deficit ∧ 2*(t+m) = area-f-2*deficit := by omega

theorem padded_footprint_bound (t q extra : Int)
    (cover : t ≤ 20*q+extra) : t+4*q ≤ 24*q+extra := by omega

/-- Both sides of the matching equality come from the written geometric proof. -/
theorem exact_adjacent_defect (t matched isolated : Nat)
    (upper : matched+isolated ≤ t) (lower : t ≤ matched+isolated) :
    t-matched = isolated := by omega

/-- A point on the outer L is at least 2k+1 away from the removed centre. -/
theorem outer_L_distance (k r c : Nat)
    (boundary : r = 4*k+1 ∨ c = 4*k+1) :
    2*k+1 ≤ (r-2*k)+(2*k-r)+(c-2*k)+(2*k-c) := by omega

/-- An alternating payment path of length 2a+1 needs at least k actual edges. -/
theorem unbounded_relay_cost (k actualEdges length : Nat)
    (alternating : length = 2*actualEdges+1)
    (distance : 2*k+1 ≤ length) : k ≤ actualEdges := by omega

end SubQuorum.IsolatedHoleDetours
#print axioms SubQuorum.IsolatedHoleDetours.centre_neighbour_in_P
#print axioms SubQuorum.IsolatedHoleDetours.square_capacity
#print axioms SubQuorum.IsolatedHoleDetours.unrestricted_disjoint_capacity
#print axioms SubQuorum.IsolatedHoleDetours.singleton_colour_obstruction
#print axioms SubQuorum.IsolatedHoleDetours.exact_mixed_margin
#print axioms SubQuorum.IsolatedHoleDetours.padded_footprint_bound
#print axioms SubQuorum.IsolatedHoleDetours.exact_adjacent_defect
#print axioms SubQuorum.IsolatedHoleDetours.outer_L_distance
#print axioms SubQuorum.IsolatedHoleDetours.unbounded_relay_cost
