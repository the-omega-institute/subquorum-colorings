import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.EndpointComponentResourceGluing

def Incident (vertex edge : Nat) : Prop := vertex=edge ∨ vertex=edge+1

def Lost (n : Nat) (deleted : Nat → Prop) (vertex : Nat) : Prop :=
  ∀ edge, edge+1<n → Incident vertex edge → deleted edge

def parentEdge (retained vertex : Nat) : Nat :=
  if vertex ≤ retained then vertex else vertex-1

theorem lost_avoids_retained_endpoints (n r v : Nat) (deleted : Nat → Prop)
    (hr : r+1<n) (kept : ¬ deleted r) (lost : Lost n deleted v) :
    v ≠ r ∧ v ≠ r+1 := by
  constructor
  · intro same
    exact kept (lost r hr (Or.inl same))
  · intro same
    exact kept (lost r hr (Or.inr same))

theorem parent_edge_in_range (n r v : Nat)
    (hr : r+1<n) (hv : v<n) :
    parentEdge r v+1<n := by
  unfold parentEdge
  split <;> omega

theorem parent_edge_incident (r v : Nat) : Incident v (parentEdge r v) := by
  unfold parentEdge Incident
  split
  · exact Or.inl rfl
  · right; omega

/-- The two branches lie strictly on opposite sides of the retained edge.
Excluding BOTH of its endpoints is necessary for injectivity. -/
theorem parent_edge_injective (r x y : Nat)
    (yl : y ≠ r) (yr : y ≠ r+1)
    (same : parentEdge r x=parentEdge r y) : x=y := by
  unfold parentEdge at same
  split at same <;> split at same <;> omega

theorem lost_parent_deleted (n r v : Nat) (deleted : Nat → Prop)
    (hr : r+1<n) (hv : v<n) (lost : Lost n deleted v) :
    deleted (parentEdge r v) := by
  exact lost _ (parent_edge_in_range n r v hr hv) (parent_edge_incident r v)

/-- Pointwise finite-injection certificate. The written proof applies
finite cardinality monotonicity; this file does not import finite-set APIs. -/
theorem lost_vertices_inject_into_deleted_edges (n r : Nat) (deleted : Nat → Prop)
    (hr : r+1<n) (kept : ¬ deleted r) :
    (∀ v, v<n → Lost n deleted v →
      parentEdge r v+1<n ∧ deleted (parentEdge r v)) ∧
    (∀ x y, Lost n deleted y →
      parentEdge r x=parentEdge r y → x=y) := by
  constructor
  · intro v hv lost
    exact ⟨parent_edge_in_range n r v hr hv,
      lost_parent_deleted n r v deleted hr hv lost⟩
  · intro x y hy same
    obtain ⟨yl,yr⟩ := lost_avoids_retained_endpoints n r y deleted hr kept hy
    exact parent_edge_injective r x y yl yr same

def outputCharge (available inside : Bool) : Nat :=
  if available && inside then 1 else 0

/-- Assign UNION availability to INTERSECTION source side, and vice versa.
This is the nontrivial orientation in the availability-rank cut proof. -/
theorem output_cut_uncrossing (r s u w : Bool) :
    outputCharge r u+outputCharge s w ≥
      outputCharge (r || s) (u && w)+outputCharge (r && s) (u || w) := by
  cases r <;> cases s <;> cases u <;> cases w <;> decide

theorem aggregate_uncrossing (a b c d x y z t : Nat)
    (fixed : a+b ≥ c+d) (switchable : x+y ≥ z+t) :
    (a+x)+(b+y) ≥ (c+z)+(d+t) := by omega

theorem optimal_witness_uncrossing (minimum a b meet join : Nat)
    (ha : a=minimum) (hb : b=minimum)
    (hm : minimum ≤ meet) (hj : minimum ≤ join)
    (uncross : a+b ≥ meet+join) : meet=minimum ∧ join=minimum := by omega

theorem private_unit_addition_never_increases (outside afterOutside before after : Nat)
    (oneUnit : afterOutside+1=outside) (localIncrement : after ≤ before+1) :
    afterOutside+after ≤ outside+before := by omega

theorem full_withdrawal_path_excess (n : Nat) (large : 2 ≤ n) :
    n-(n-1)=1 ∧ n-1<n := by omega

#print axioms lost_avoids_retained_endpoints
#print axioms parent_edge_in_range
#print axioms parent_edge_incident
#print axioms parent_edge_injective
#print axioms lost_parent_deleted
#print axioms lost_vertices_inject_into_deleted_edges
#print axioms output_cut_uncrossing
#print axioms aggregate_uncrossing
#print axioms optimal_witness_uncrossing
#print axioms private_unit_addition_never_increases
#print axioms full_withdrawal_path_excess

end SubQuorum.EndpointComponentResourceGluing
