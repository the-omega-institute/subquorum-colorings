import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.JointSelectionBlockBalance

def endpoints {Vertex : Type} (edges : List (Vertex × Vertex)) : List Vertex :=
  edges.flatMap fun edge => [edge.1, edge.2]

theorem endpoint_count {Vertex : Type} (edges : List (Vertex × Vertex)) :
    (endpoints edges).length = 2 * edges.length := by
  induction edges with
  | nil => simp [endpoints]
  | cons edge remaining inductionHypothesis =>
    simp [endpoints] at inductionHypothesis ⊢
    omega

theorem covered_domain_parity {Vertex : Type}
    (oldEdges newEdges : List (Vertex × Vertex))
    (sources resources mixedPorts : List Vertex) (activeMixed : Nat)
    (mixedCount : mixedPorts.length = 2 * activeMixed)
    (domain : (endpoints newEdges).Perm
      (endpoints oldEdges ++ sources ++ resources ++ mixedPorts)) :
    (sources.length + resources.length) % 2 = 0 := by
  have cardinality := domain.length_eq
  simp only [List.length_append, endpoint_count] at cardinality
  omega

theorem source_only_domain_parity {Vertex : Type}
    (oldEdges newEdges : List (Vertex × Vertex))
    (sources mixedPorts : List Vertex) (activeMixed : Nat)
    (mixedCount : mixedPorts.length = 2 * activeMixed)
    (domain : (endpoints newEdges).Perm
      (endpoints oldEdges ++ sources ++ mixedPorts)) :
    sources.length % 2 = 0 := by
  have cardinality := domain.length_eq
  simp only [List.length_append, endpoint_count] at cardinality
  omega

structure BlockCharge where
  sources : Nat
  resources : Nat
  negative : Nat
  positive : Nat
  incidence : (sources : Int) - resources = 2 * ((negative : Int) - positive)

theorem block_coherent_balance (block : BlockCharge)
    (noNegative : block.negative = 0) (noPositive : block.positive = 0) :
    block.sources = block.resources := by
  have balance := block.incidence
  omega

theorem block_excess_error (block : BlockCharge) :
    block.sources - block.resources ≤ 2 * block.negative := by
  have balance := block.incidence
  omega

theorem disjoint_block_error_sum (blocks : List BlockCharge) :
    (blocks.map fun block => block.sources - block.resources).sum ≤
      2 * (blocks.map fun block => block.negative).sum := by
  induction blocks with
  | nil => simp
  | cons block remaining inductionHypothesis =>
    have bound := block_excess_error block
    simp only [List.map_cons, List.sum_cons]
    omega

theorem cut_flux_capacity (sources resources negative positive
    crossingNegative crossingPositive cutCapacity : Nat)
    (incidence : (sources : Int) - resources =
      2 * ((negative : Int) - positive) + crossingNegative - crossingPositive)
    (coherentNegative : negative = 0) (coherentPositive : positive = 0)
    (capacity : crossingNegative + crossingPositive ≤ cutCapacity) :
    (sources : Int) - resources ≤ cutCapacity ∧
      (resources : Int) - sources ≤ cutCapacity := by
  omega

theorem source_blocks_half_progress
    (copies alphas betas mixed originalMixed selected activeMixed : Nat)
    (tpInventory : 2 * alphas + mixed + selected + activeMixed = 4 * copies + originalMixed)
    (bpInventory : 2 * betas + mixed + activeMixed = originalMixed) :
    4 * copies ≤ 2 * alphas + selected := by
  omega

theorem half_progress_error (copies alphas selected errors : Nat)
    (inventoryBound : 4 * copies ≤ 2 * alphas + selected)
    (transferBound : alphas + selected ≤ 2 * copies + errors) :
    selected ≤ 2 * errors := by
  omega

theorem positive_selection_not_coherent (copies alphas selected : Nat)
    (positiveSelection : 0 < selected)
    (inventoryBound : 4 * copies ≤ 2 * alphas + selected)
    (coherentTransfer : alphas + selected ≤ 2 * copies) : False := by
  omega

theorem odd_slot_obstruction (matchingEdges localPairs slots : Nat)
    (coverage : 2 * matchingEdges = 2 * localPairs + slots)
    (oddSlots : slots % 2 = 1) : False := by
  omega

#print axioms endpoint_count
#print axioms covered_domain_parity
#print axioms source_only_domain_parity
#print axioms block_coherent_balance
#print axioms block_excess_error
#print axioms disjoint_block_error_sum
#print axioms cut_flux_capacity
#print axioms source_blocks_half_progress
#print axioms half_progress_error
#print axioms positive_selection_not_coherent
#print axioms odd_slot_obstruction

end SubQuorum.JointSelectionBlockBalance
