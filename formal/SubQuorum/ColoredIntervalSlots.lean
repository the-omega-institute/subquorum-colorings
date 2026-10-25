import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false

namespace SubQuorum.ColoredIntervalSlots

/-- An alpha has only one end of the chosen color. Its assigned interval
is therefore a function, rather than two independently spendable incidences. -/
theorem chosen_owner_injection {A R : Type} (assigned : A → R) (pick : R → A)
    (resources : List R)
    (witness : ∀ r ∈ resources, assigned (pick r)=r)
    (r s : R) (hr : r ∈ resources) (hs : s ∈ resources)
    (same : pick r=pick s) : r=s := by
  calc
    r = assigned (pick r) := (witness r hr).symm
    _ = assigned (pick s) := congrArg assigned same
    _ = s := witness s hs

/-- The actual resource->owner choices are distinct. This is the constructive
one-color allocation step, with original resource identities retained. -/
theorem chosen_owners_nodup {A R : Type} (assigned : A → R) (pick : R → A)
    (resources : List R) (distinct : resources.Nodup)
    (witness : ∀ r ∈ resources, assigned (pick r)=r) :
    (resources.map pick).Nodup := by
  induction resources with
  | nil => simp
  | cons r rest ih =>
    have hd := List.nodup_cons.mp distinct
    have tailWitness : ∀ s ∈ rest, assigned (pick s)=s := by
      intro s hs
      exact witness s (by simp [hs])
    apply List.nodup_cons.mpr
    constructor
    · intro member
      obtain ⟨s, hs, same⟩ := List.mem_map.mp member
      have equal : r=s := chosen_owner_injection assigned pick (r::rest)
        witness r s (by simp) (by simp [hs]) same.symm
      exact hd.1 (equal ▸ hs)
    · exact ih hd.2 tailWitness

theorem actual_one_color_allocation {A R : Type} (assigned : A → R) (pick : R → A)
    (resources : List R) (alphas : List A)
    (distinct : resources.Nodup)
    (witness : ∀ r ∈ resources, assigned (pick r)=r)
    (eligible : ∀ r ∈ resources, pick r ∈ alphas) :
    (resources.map pick).Nodup ∧ resources.length≤alphas.length := by
  have nd := chosen_owners_nodup assigned pick resources distinct witness
  refine ⟨nd, ?_⟩
  have included : ∀ a ∈ resources.map pick, a ∈ alphas := by
    intro a ha
    obtain ⟨r,hr,ha⟩ := List.mem_map.mp ha
    exact ha ▸ eligible r hr
  have h := nd.length_le_of_subset included
  simpa only [List.length_map] using h

/-- The actual list/count adapter supplies one assigned color-end per alpha
except holes and one redundant incidence per same-color collision. -/
theorem one_color_deficit_bound (alphas holes collisions chosen paid : Nat)
    (count : chosen+holes+collisions=alphas) (allocation : chosen≤paid) :
    alphas-paid≤holes+collisions := by omega

theorem signed_color_identity (alphas h0 h1 e0 e1 s0 s1 mixed : Nat)
    (zero : h0+2*e0+s0+mixed=alphas)
    (one : h1+2*e1+s1+mixed=alphas) :
    h0+2*e0+s0=h1+2*e1+s1 := by omega

theorem two_zero_holes_force_one_collision (e0 e1 : Nat)
    (balance : 2+2*e0=2*e1) : e1=e0+1 := by omega

theorem two_one_holes_force_zero_collision (e0 e1 : Nat)
    (balance : 2*e0=2+2*e1) : e0=e1+1 := by omega

theorem monochromatic_holes_no_opposite_collision (loss h0 h1 e0 e1 : Nat)
    (zeroBound : loss≤h0+e0) (oneBound : loss≤h1+e1)
    (condition : (h0=0 ∧ e0=0) ∨ (h1=0 ∧ e1=0)) : loss=0 := by
  rcases condition with h | h <;> omega

theorem colored_slots_loss_bound (loss h0 h1 : Nat)
    (zeroBound : loss≤h0) (oneBound : loss≤h1) : loss≤min h0 h1 := by omega

theorem signed_payment_ledger (a b afterA afterB paid loss : Nat)
    (conservation : a+afterB=b+afterA) (betaMonotone : afterB≤b)
    (allocation : paid+loss=afterA) : b-afterB+paid+loss=a := by omega

/-- In the actual paired family, the signed identity is sharp: each two-hole
chain has one opposite-color collision, and different chains use different j. -/
theorem sharp_stack_counts (q : Nat) :
    (2*q+0)/2=q ∧ min (2*q+0) (0+q)=q ∧ 2*q-q=q := by omega

theorem actual_hole_colors (i w : Nat) (width : 30≤w) (even : w%2=0) :
    ((10+14*i)+6)%2=0 ∧ ((3+14*i)+(w-7))%2=0 := by omega

theorem actual_assigned_tip_colors (i w : Nat) (width : 30≤w) (even : w%2=0) :
    ((7+14*i)+8)%2=1 ∧ ((6+14*i)+(w-9))%2=1 := by omega

theorem actual_copy_separation (i w : Nat) (width : 30≤w) :
    13+3≤w-14 ∧ (12+14*i)+3=1+14*(i+1) := by omega

theorem half_turn_preserves_color (r c w : Nat) (row : r≤9)
    (col : c<w) (even : w%2=0) :
    ((9-r)+(w-1-c))%2=(r+c)%2 := by omega

#print axioms chosen_owner_injection
#print axioms chosen_owners_nodup
#print axioms actual_one_color_allocation
#print axioms one_color_deficit_bound
#print axioms signed_color_identity
#print axioms two_zero_holes_force_one_collision
#print axioms two_one_holes_force_zero_collision
#print axioms monochromatic_holes_no_opposite_collision
#print axioms colored_slots_loss_bound
#print axioms signed_payment_ledger
#print axioms sharp_stack_counts
#print axioms actual_hole_colors
#print axioms actual_assigned_tip_colors
#print axioms actual_copy_separation
#print axioms half_turn_preserves_color

end SubQuorum.ColoredIntervalSlots
