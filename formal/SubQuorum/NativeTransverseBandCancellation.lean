import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NativeTransverseBandCancellation

def bit (mask : Fin 64) (position : Nat) : Bool :=
  decide (mask.val / 2 ^ position % 2 = 1)

def upperNative (mask : Fin 64) : Nat :=
  (bit mask 0).toNat + (bit mask 1).toNat + (bit mask 2).toNat

def lowerNative (mask : Fin 64) : Nat :=
  (bit mask 3).toNat + (bit mask 4).toNat + (bit mask 5).toNat

theorem native_cross_edge_is_pinwheel (mask : Fin 64)
    (upper : 2 ≤ upperNative mask) (lower : 2 ≤ lowerNative mask)
    (leftConflict : bit mask 1 && bit mask 3 = false)
    (rightConflict : bit mask 2 && bit mask 4 = false) : mask = 45 ∨ mask = 51 := by
  have checked : ∀ mask : Fin 64,
      2 ≤ upperNative mask → 2 ≤ lowerNative mask →
      (bit mask 1 && bit mask 3 = false) →
      (bit mask 2 && bit mask 4 = false) → mask = 45 ∨ mask = 51 := by decide
  exact checked mask upper lower leftConflict rightConflict

theorem pinwheel_has_both_outer_supports (mask : Fin 64)
    (shape : mask = 45 ∨ mask = 51) : bit mask 0 = true ∧ bit mask 5 = true := by
  rcases shape with shape | shape <;> subst mask <;> decide

theorem supported_selection_forces_blank (label : Fin 3)
    (feasible : 1 + (if label.val = 0 then 0 else 1) ≤ 1) : label.val = 0 := by
  split at feasible <;> omega

theorem alternating_interval_odd (doubleColumns : Nat) :
    (2 * doubleColumns + 1) % 2 = 1 := by omega

inductive PathSpan : Nat → Prop where
  | one (doubleColumns : Nat) : PathSpan (2 * doubleColumns + 1)
  | extend {span : Nat} (prior : PathSpan span) (doubleColumns : Nat) :
      PathSpan (span + 1 + (2 * doubleColumns + 1))

theorem arbitrary_path_span_odd {span : Nat} (path : PathSpan span) : span % 2 = 1 := by
  induction path with
  | one doubleColumns => omega
  | extend prior doubleColumns inductionHypothesis => omega

theorem even_packet_excludes_boundary_path (columns : Nat)
    (evenColumns : columns % 2 = 0) (path : PathSpan columns) : False := by
  have oddSpan := arbitrary_path_span_odd path
  omega

theorem indegree_source_identity (incoming : List Bool) :
    incoming.length = incoming.countP id + incoming.countP (fun flag => !flag) := by
  induction incoming with
  | nil => simp
  | cons flag rest inductionHypothesis => cases flag <;> simp_all <;> omega

theorem interval_minus_edges_counts_sources (incoming : List Bool)
    (vertices edges sources : Nat)
    (vertexCount : vertices = incoming.length)
    (edgeCount : edges = incoming.countP id)
    (sourceCount : sources = incoming.countP (fun flag => !flag)) :
    vertices = edges + sources := by
  have identity := indegree_source_identity incoming
  omega

theorem source_and_sealed_budget (vertices edges sources bands sealed : Nat)
    (forest : vertices = edges + sources)
    (distinctBoundarySources : bands + sealed ≤ sources) :
    edges + bands + sealed ≤ vertices := by omega

theorem exact_joint_flux (surplusTwice exports vertices edges unused paths : Int)
    (localFlux : surplusTwice + exports = 2 * vertices + unused)
    (twoIncidences : exports = 2 * edges)
    (pathForest : vertices - edges = paths) :
    surplusTwice = 2 * paths + unused := by omega

theorem packet_compensation (surplusTwice paths unused bands sealed : Int)
    (jointFlux : surplusTwice = 2 * paths + unused)
    (matchingInjection : 0 ≤ unused)
    (boundaryPaths : bands + sealed ≤ paths) :
    2 * (bands + sealed) ≤ surplusTwice := by omega

theorem internal_objective_with_all_cuts (halfArea selected internal cuts
    surplusTwice bands sealed : Int)
    (endpointAccounting : surplusTwice = 2 * halfArea - 2 * selected - 2 * internal - cuts)
    (packetBound : 2 * (bands + sealed) ≤ surplusTwice) :
    2 * selected + 2 * internal + cuts ≤ 2 * (halfArea - bands - sealed) := by omega

theorem union_receiver_ledger_bound (marginTwice packetSurplusTwice outsideDeficit
    outsidePositive outsideNegative boundaryBudget : Int)
    (originalLedger : marginTwice = packetSurplusTwice + 2 * outsideDeficit -
      2 * outsidePositive + 2 * outsideNegative)
    (packetBound : 2 * boundaryBudget ≤ packetSurplusTwice) :
    2 * (boundaryBudget + outsideDeficit - outsidePositive + outsideNegative) ≤ marginTwice := by omega

theorem union_receiver_coefficient_one (marginTwice packetSurplusTwice outsideDeficit
    outsidePositive outsideNegative boundaryBudget : Int)
    (originalLedger : marginTwice = packetSurplusTwice + 2 * outsideDeficit -
      2 * outsidePositive + 2 * outsideNegative)
    (packetBound : 2 * boundaryBudget ≤ packetSurplusTwice)
    (covered : outsidePositive ≤ boundaryBudget)
    (deficitNonnegative : 0 ≤ outsideDeficit) (negativeNonnegative : 0 ≤ outsideNegative) :
    0 ≤ marginTwice := by omega

theorem sharp_all_parameter_counts (pairs sealed : Nat)
    (positivePairs : 1 ≤ pairs) (atMostTwoSealed : sealed ≤ 2) :
    2 * (4 * pairs + 2) = (7 * pairs + 2 - sealed) + pairs + 2 + sealed := by omega

theorem arbitrarily_many_debits_do_not_require_extra_budget (pairs : Nat)
    (positivePairs : 1 ≤ pairs) :
    (2 : Int) - pairs < 2 ∧ (pairs : Int) + 2 - pairs = 2 := by omega

end SubQuorum.NativeTransverseBandCancellation

#print axioms SubQuorum.NativeTransverseBandCancellation.native_cross_edge_is_pinwheel
#print axioms SubQuorum.NativeTransverseBandCancellation.pinwheel_has_both_outer_supports
#print axioms SubQuorum.NativeTransverseBandCancellation.supported_selection_forces_blank
#print axioms SubQuorum.NativeTransverseBandCancellation.alternating_interval_odd
#print axioms SubQuorum.NativeTransverseBandCancellation.arbitrary_path_span_odd
#print axioms SubQuorum.NativeTransverseBandCancellation.even_packet_excludes_boundary_path
#print axioms SubQuorum.NativeTransverseBandCancellation.indegree_source_identity
#print axioms SubQuorum.NativeTransverseBandCancellation.interval_minus_edges_counts_sources
#print axioms SubQuorum.NativeTransverseBandCancellation.source_and_sealed_budget
#print axioms SubQuorum.NativeTransverseBandCancellation.exact_joint_flux
#print axioms SubQuorum.NativeTransverseBandCancellation.packet_compensation
#print axioms SubQuorum.NativeTransverseBandCancellation.internal_objective_with_all_cuts
#print axioms SubQuorum.NativeTransverseBandCancellation.union_receiver_ledger_bound
#print axioms SubQuorum.NativeTransverseBandCancellation.union_receiver_coefficient_one
#print axioms SubQuorum.NativeTransverseBandCancellation.sharp_all_parameter_counts
#print axioms SubQuorum.NativeTransverseBandCancellation.arbitrarily_many_debits_do_not_require_extra_budget
