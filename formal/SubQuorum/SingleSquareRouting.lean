import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SingleSquareRouting

inductive Corner where
  | nw | ne | se | sw
  deriving DecidableEq

def column : Corner → Bool
  | .nw | .sw => false
  | .ne | .se => true

def ppMate : Corner → Corner
  | .nw => .sw
  | .sw => .nw
  | .ne => .se
  | .se => .ne

theorem pp_mate_preserves_column (p : Corner) : column (ppMate p)=column p := by
  cases p <;> rfl

/-- For an all-P tile with all actual matching edges leaving the tile,
the only internal strand edges are the two original auxiliary PP edges. -/
inductive WireWalk : Corner → Corner → Prop where
  | refl (p : Corner) : WireWalk p p
  | step {start last : Corner} (prior : WireWalk start last) :
      WireWalk start (ppMate last)

theorem arbitrary_wire_walk_preserves_column {p q : Corner} (walk : WireWalk p q) :
    column p=column q := by
  induction walk with
  | refl => rfl
  | step prior ih => exact ih.trans (pp_mate_preserves_column _).symm

theorem fixed_pairing_iff (p q : Corner) :
    (p=q ∨ q=ppMate p) ↔ column p=column q := by
  cases p <;> cases q <;> decide

theorem no_cross_column_switch : ¬ WireWalk .nw .ne := by
  intro walk
  have impossible := arbitrary_wire_walk_preserves_column walk
  contradiction

theorem two_local_wires_have_no_common_corner (p : Corner) :
    ¬ (column p=false ∧ column p=true) := by
  intro both
  have impossible := both.1.symm.trans both.2
  contradiction

/-- Owner routes are generated from alpha sources and actual nonself links.
The physical adapter proves that every link stays in one endpoint component. -/
inductive Reach {O : Type} (alpha : O → Prop) (link : O → O → Prop) : O → Prop where
  | source {a : O} (isAlpha : alpha a) : Reach alpha link a
  | step {a b : O} (prior : Reach alpha link a) (edge : link a b) : Reach alpha link b

theorem reachable_component_has_source {O C : Type}
    (alpha : O → Prop) (link : O → O → Prop) (component : O → C)
    (preserves : ∀ a b, link a b → component a=component b)
    {target : O} (reachable : Reach alpha link target) :
    ∃ source, alpha source ∧ component source=component target := by
  induction reachable with
  | source h => exact ⟨_,h,rfl⟩
  | step prior edge ih =>
    obtain ⟨a,ha,same⟩ := ih
    exact ⟨a,ha,same.trans (preserves _ _ edge)⟩

theorem source_free_component_unreachable {O C : Type}
    (alpha : O → Prop) (link : O → O → Prop) (component : O → C)
    (preserves : ∀ a b, link a b → component a=component b)
    (receiver : C) (noAlpha : ∀ a, component a=receiver → ¬ alpha a)
    {target : O} (inside : component target=receiver) : ¬ Reach alpha link target := by
  intro reachable
  obtain ⟨a,ha,same⟩ := reachable_component_has_source alpha link component preserves reachable
  exact noAlpha a (same.trans inside) ha

/-- A route walk starting at an alpha avoids every gate of a source-free
endpoint component. No claim about resource identity deletion is involved. -/
theorem reachable_gate_outside_removed_component {O C : Type}
    (alpha : O → Prop) (link : O → O → Prop) (component : O → C)
    (preserves : ∀ a b, link a b → component a=component b)
    (receiver : C) (noAlpha : ∀ a, component a=receiver → ¬ alpha a)
    {gate : O} (reachable : Reach alpha link gate) : component gate ≠ receiver := by
  intro inside
  exact source_free_component_unreachable alpha link component preserves receiver noAlpha inside reachable

/-- The geometric seven-pattern proof supplies equal horizontal/vertical
odd-arm counts. This declaration checks the exact open-owner arithmetic. -/
theorem exact_mixed_chain_count (aE aW oddE oddW oddTotal : Nat)
    (parityPattern : oddTotal=2*(oddE+oddW)) :
    (aE+oddE)+(aW+oddW)=aE+aW+oddTotal/2 := by omega

/-- Each primitive keeps its original resource identity and every original
owner incidence. The network adapter supplies reachability of its gates.
Pruning removes no such primitive, including both arms of a beta fork. -/
theorem pruned_primitive_iff_original {O C P : Type}
    (alpha : O → Prop) (link : O → O → Prop) (component : O → C)
    (preserves : ∀ a b, link a b → component a=component b)
    (receiver : C) (noAlpha : ∀ a, component a=receiver → ¬ alpha a)
    (valid : P → Prop) (uses : P → O → Prop)
    (payingGateReachable : ∀ p, valid p → ∀ gate, uses p gate → Reach alpha link gate)
    (p : P) :
    (valid p ∧ ∀ gate, uses p gate → component gate ≠ receiver) ↔ valid p := by
  constructor
  · exact And.left
  · intro hp
    refine ⟨hp,?_⟩
    intro gate used
    exact reachable_gate_outside_removed_component alpha link component preserves receiver noAlpha
      (payingGateReachable p hp gate used)

theorem one_original_owner_is_one_gate (loadLeft loadRight : Nat)
    (ownerCapacity : loadLeft+loadRight ≤ 1) :
    ¬ (loadLeft=1 ∧ loadRight=1) := by omega

theorem arbitrary_shared_gap_capacity (width : Nat) (large : 10 ≤ width) :
    1 ≤ width-6 ∧ (width-5)-1=width-6 := by omega

#print axioms pp_mate_preserves_column
#print axioms arbitrary_wire_walk_preserves_column
#print axioms fixed_pairing_iff
#print axioms no_cross_column_switch
#print axioms two_local_wires_have_no_common_corner
#print axioms reachable_component_has_source
#print axioms source_free_component_unreachable
#print axioms reachable_gate_outside_removed_component
#print axioms exact_mixed_chain_count
#print axioms pruned_primitive_iff_original
#print axioms one_original_owner_is_one_gate
#print axioms arbitrary_shared_gap_capacity

end SubQuorum.SingleSquareRouting
