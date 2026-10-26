import Lean.Elab.Tactic.Omega

/-! Local geometric exclusions and general guarded-cover arithmetic.
The grid coordinate partition and matching-uniqueness peel remain written.
-/
namespace SubQuorum.GuardedHoleCover

/-- Every selected vertex has at most one occupied neighbour. -/
def Capacity {V : Type} (T P : V → Prop) (adj : V → V → Prop) : Prop :=
  ∀ v, T v → ∀ a b, (T a ∨ P a) → (T b ∨ P b) → adj v a → adj v b → a = b

theorem two_endpoints_exclude_selection {V : Type} (T P : V → Prop)
    (adj : V → V → Prop) (cap : Capacity T P adj)
    {v a b : V} (pa : P a) (pb : P b) (ha : adj v a) (hb : adj v b)
    (distinct : a ≠ b) : ¬ T v := by
  intro tv
  exact distinct (cap v tv a b (Or.inr pa) (Or.inr pb) ha hb)

theorem guarded_pair_exclusion {V : Type} (T P : V → Prop)
    (adj : V → V → Prop) (cap : Capacity T P adj)
    {a b g : V} (pg : P g) (edge : adj a b) (guard : adj a g)
    (distinct : b ≠ g) : ¬ (T a ∧ T b) := by
  intro h
  exact distinct (cap a h.1 b g (Or.inl h.2) (Or.inr pg) edge guard)

theorem partner_injective {V : Type} (partner : V → V)
    (involution : ∀ v, partner (partner v) = v) :
    ∀ a b, partner a = partner b → a = b := by
  intro a b h
  have e := congrArg partner h
  simpa only [involution] using e

theorem selected_partner_is_hole {V : Type} (T P : V → Prop)
    (partner : V → V)
    (exclusive : ∀ v, T v → ¬ T (partner v))
    (outside : ∀ v, T v → ¬ P (partner v)) :
    ∀ v, T v → ¬ T (partner v) ∧ ¬ P (partner v) := by
  intro v tv
  exact ⟨exclusive v tv, outside v tv⟩

def slotSum : List Nat → Nat
  | [] => 0
  | x :: xs => x + slotSum xs

theorem all_length_slot_bound (xs : List Nat)
    (capacity : ∀ x ∈ xs, x ≤ 1) : slotSum xs ≤ xs.length := by
  induction xs with
  | nil => simp [slotSum]
  | cons x xs ih =>
    have hx : x ≤ 1 := capacity x (by simp)
    have rest : ∀ y ∈ xs, y ≤ 1 := by
      intro y hy
      exact capacity y (by simp [hy])
    have bound := ih rest
    simp only [slotSum, List.length_cons]
    omega

theorem exact_hole_margin (t h m area f a : Int)
    (partition : area = t + h + 2*m)
    (holes : h - t = f + 2*a) :
    2*(t+m) = area - f - 2*a := by omega

theorem fixed_footprint_bound (t w : Int) (cover : t ≤ w) :
    t + (w-1) ≤ 2*w-1 := by omega

end SubQuorum.GuardedHoleCover
#print axioms SubQuorum.GuardedHoleCover.two_endpoints_exclude_selection
#print axioms SubQuorum.GuardedHoleCover.guarded_pair_exclusion
#print axioms SubQuorum.GuardedHoleCover.partner_injective
#print axioms SubQuorum.GuardedHoleCover.selected_partner_is_hole
#print axioms SubQuorum.GuardedHoleCover.all_length_slot_bound
#print axioms SubQuorum.GuardedHoleCover.exact_hole_margin
#print axioms SubQuorum.GuardedHoleCover.fixed_footprint_bound
