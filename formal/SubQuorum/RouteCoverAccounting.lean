import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.RouteCoverAccounting

theorem twofold_load_sum (loads : List Nat) :
    loads.sum ≤ 2 * loads.length + (loads.map (fun load => load - 2)).sum := by
  induction loads with
  | nil => simp
  | cons load rest inductionHypothesis =>
      simp only [List.sum_cons, List.length_cons, List.map_cons]
      have localBound : load ≤ 2 + (load - 2) := by omega
      omega

theorem separator_excess_bound (blocked units totalLoad excess deficit : Nat)
    (incidenceBound : 2 * blocked ≤ totalLoad)
    (loadBound : totalLoad ≤ 2 * units + excess)
    (attainingSeparator : blocked = units + deficit) :
    2 * deficit ≤ excess := by
  omega

theorem subcritical_excess_full_payment (deficit excess : Nat)
    (deficitBound : 2 * deficit ≤ excess) (subcritical : excess ≤ 1) :
    deficit = 0 := by
  omega

theorem integral_layer_remainder (aggregate multiplicity layer : Nat)
    (positive : 0 < multiplicity) (bounded : aggregate ≤ multiplicity)
    (unitCapacity : layer ≤ 1) (supported : layer ≤ aggregate)
    (lowerBound : aggregate - (multiplicity - 1) ≤ layer) :
    aggregate - layer ≤ multiplicity - 1 := by
  omega

theorem saturated_boundary_in_every_layer (multiplicity layer remainder : Nat)
    (positive : 0 < multiplicity) (unitCapacity : layer ≤ 1)
    (remainderBound : remainder ≤ multiplicity - 1)
    (decomposition : layer + remainder = multiplicity) :
    layer = 1 := by
  omega

theorem cheaper_twofold_layer (firstCost secondCost certificateCost : Nat)
    (costBound : firstCost + secondCost ≤ certificateCost) :
    2 * firstCost ≤ certificateCost ∨ 2 * secondCost ≤ certificateCost := by
  omega

#print axioms twofold_load_sum
#print axioms separator_excess_bound
#print axioms subcritical_excess_full_payment
#print axioms integral_layer_remainder
#print axioms saturated_boundary_in_every_layer
#print axioms cheaper_twofold_layer

end SubQuorum.RouteCoverAccounting
