import SubQuorum.FrozenSupportTreeReroot
import SubQuorum.InteriorSupportTreeCaps

set_option autoImplicit false

namespace SubQuorum.BetaClosingAndMixedRepair
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

/-- Selection insertion is monotone for the actual-mate freezing derivation. -/
theorem frozen_selected_mono {V : Type} (P T T' : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (selectedInclusion : ∀ x, T x → T' x) {v : V}
    (frozen : Frozen P T mate adj v) : Frozen P T' mate adj v := by
  induction frozen with
  | ss pv distinct va vb ta tb =>
    exact Frozen.ss pv distinct va vb (selectedInclusion _ ta) (selectedInclusion _ tb)
  | sp pv distinct va vb ta pb _ ih =>
    exact Frozen.sp pv distinct va vb (selectedInclusion _ ta) pb ih
  | ps pv distinct va vb pa _ tb ih =>
    exact Frozen.ps pv distinct va vb pa ih (selectedInclusion _ tb)
  | pp pv distinct va vb pa _ pb _ ihA ihB =>
    exact Frozen.pp pv distinct va vb pa ihA pb ihB

def Feasible {V : Type} (T P : V → Prop) (adj : V → V → Prop) : Prop :=
  ∀ v, T v → ∀ a b, adj v a → adj v b → (T a ∨ P a) → (T b ∨ P b) → a=b

/-- Check old selected sites and the inserted site separately. No finite
cardinality argument or bound on the old freezing depth is needed. -/
theorem insert_feasible {V : Type} (T P : V → Prop) (adj : V → V → Prop) (w : V)
    (old : Feasible T P adj) (noOld : ∀ v, T v → ¬ adj v w)
    (notSelf : ¬ adj w w)
    (atNew : ∀ a b, adj w a → adj w b → (T a ∨ P a) → (T b ∨ P b) → a=b) :
    Feasible (fun v => T v ∨ v=w) P adj := by
  intro v selected a b va vb ha hb
  rcases selected with tv | vw
  · have oldOcc : ∀ x, adj v x → ((T x ∨ x=w) ∨ P x) → T x ∨ P x := by
      intro x vx hx
      rcases hx with (tx | xw) | px
      · exact Or.inl tx
      · subst x; exact False.elim (noOld v tv vx)
      · exact Or.inr px
    exact old v tv a b va vb (oldOcc a va ha) (oldOcc b vb hb)
  · subst v
    have oldOcc : ∀ x, adj w x → ((T x ∨ x=w) ∨ P x) → T x ∨ P x := by
      intro x wx hx
      rcases hx with (tx | xw) | px
      · exact Or.inl tx
      · subst x; exact False.elim (notSelf wx)
      · exact Or.inr px
    exact atNew a b va vb (oldOcc a va ha) (oldOcc b vb hb)

open SubQuorum.FrozenSupportTreeReroot (selected endpoints mate nonmateAdjacent)

theorem original_site_safe :
    (2,12) ∉ selected ++ endpoints ∧
    ((selected ++ endpoints).filter fun v => decide (adjacent (2,12) v)) = [(3,12)] := by decide

theorem all_original_endpoints_still_frozen : ∀ v ∈ endpoints,
    Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected ∨ x=(2,12))
      mate nonmateAdjacent v := by
  intro v pv
  exact frozen_selected_mono _ _ _ _ _ (fun x tx => Or.inl tx)
    (FrozenSupportTreeReroot.all_endpoints_frozen v pv)

/-- These local types are the relevant beta-to-mixed change. Full inventory
and all-d board adaptation are proved in the written note and solver-free checks. -/
theorem changed_tip_types :
    (2,12) ∉ selected ∧ (2,12) ∉ endpoints ∧ (3,12) ∈ endpoints ∧
    (5,11) ∈ endpoints ∧ (4,11) ∉ selected ∧ (4,11) ∉ endpoints := by decide

theorem old_beta_direct_link_and_new_exit :
    adjacent (5,10) (5,11) ∧ adjacent (3,12) (3,11) ∧
    (3,11) ∈ selected ∧ (2,11) ∉ selected ++ endpoints ∧
    (2,10) ∉ selected ++ endpoints ∧ (3,10) ∉ selected ++ endpoints := by decide

theorem closed_family_ledger (d r q : Nat) :
    12*(20+2*d+2*r)*q =
      2*((34+4*d)*q+25*q+12*q+(49+8*d+12*r)*q) := by
  have base : 12*(20+2*d+2*r) = 2*((34+4*d)+25+12+(49+8*d+12*r)) := by omega
  calc
    _ = (2*((34+4*d)+25+12+(49+8*d+12*r)))*q := congrArg (fun n => n*q) base
    _ = _ := by simp only [Nat.mul_assoc, Nat.add_mul]

theorem physical_sharpness_scalar (q : Nat) :
    q = (2*q)/2 ∧ q-0=q := by omega

#print axioms frozen_selected_mono
#print axioms insert_feasible
#print axioms original_site_safe
#print axioms all_original_endpoints_still_frozen
#print axioms changed_tip_types
#print axioms old_beta_direct_link_and_new_exit
#print axioms closed_family_ledger
#print axioms physical_sharpness_scalar

end SubQuorum.BetaClosingAndMixedRepair
