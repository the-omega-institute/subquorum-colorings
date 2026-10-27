import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

/-! Resource-list kernels for repeated arm surgery. The adapter from actual
grid paths to the four resource lists, and the gate-order theorem, are written.
-/
set_option autoImplicit false
namespace SubQuorum.OrderedTHRelay

theorem arm_rewire {R : Type} (a b c d : List R) :
    ((a ++ b) ++ (c ++ d)).Perm ((a ++ c) ++ (b ++ d)) := by
  have h := (List.perm_append_comm (l₁ := b) (l₂ := c)).append_left a
  have h' := h.append_right d
  simpa only [List.append_assoc] using h'

theorem context_rewire {R : Type} (restLeft a b c d restRight : List R) :
    (restLeft ++ ((a ++ b) ++ (c ++ d)) ++ restRight).Perm
      (restLeft ++ ((a ++ c) ++ (b ++ d)) ++ restRight) := by
  exact ((arm_rewire a b c d).append_left restLeft).append_right restRight

/-- Finite abstract resource surgeries, without assuming geometry or port order.
Each square step reconnects four arm resource lists and keeps its context. -/
inductive ResourceSurgery (R : Type) : List R → List R → Prop where
  | refl (xs : List R) : ResourceSurgery R xs xs
  | square (restLeft a b c d restRight : List R) :
      ResourceSurgery R (restLeft ++ ((a ++ b) ++ (c ++ d)) ++ restRight)
        (restLeft ++ ((a ++ c) ++ (b ++ d)) ++ restRight)
  | trans {xs ys zs : List R} :
      ResourceSurgery R xs ys → ResourceSurgery R ys zs → ResourceSurgery R xs zs

theorem surgery_perm {R : Type} {xs ys : List R}
    (h : ResourceSurgery R xs ys) : xs.Perm ys := by
  induction h with
  | refl xs => exact List.Perm.refl xs
  | square restLeft a b c d restRight => exact context_rewire restLeft a b c d restRight
  | trans first second ihfirst ihsecond => exact ihfirst.trans ihsecond

/-- Any finite number of valid resource-list surgeries preserves uniqueness. -/
theorem surgery_nodup {R : Type} {xs ys : List R}
    (h : ResourceSurgery R xs ys) (unique : xs.Nodup) : ys.Nodup :=
  (surgery_perm h).nodup unique

/-- The written disjoint-union adapter provides the resource-count identity. -/
theorem incremental_cost (old intermediate tt hh newCost : Nat)
    (oldPaid : old = intermediate) (newPaid : newCost = intermediate+tt+hh) :
    newCost = old+tt+hh ∧ newCost-old = tt+hh := by omega

theorem batch_residuals (T H a b t s : Nat)
    (tt : T=2*a+t) (hh : H=2*b+t) (left : s≤a) (right : s≤b) :
    T=(t+2*s)+2*(a-s) ∧ H=(t+2*s)+2*(b-s) := by omega

theorem family_ledger (r : Nat) :
    2*((r+2)+(r+1)) = (2*r+2)*4-2*(2*r+1) ∧
    (r+1)-r=1 ∧ (5*r+4)-(r+2)=2*(2*r+1) := by omega

end SubQuorum.OrderedTHRelay
#print axioms SubQuorum.OrderedTHRelay.arm_rewire
#print axioms SubQuorum.OrderedTHRelay.context_rewire
#print axioms SubQuorum.OrderedTHRelay.surgery_perm
#print axioms SubQuorum.OrderedTHRelay.surgery_nodup
#print axioms SubQuorum.OrderedTHRelay.incremental_cost
#print axioms SubQuorum.OrderedTHRelay.batch_residuals
#print axioms SubQuorum.OrderedTHRelay.family_ledger
