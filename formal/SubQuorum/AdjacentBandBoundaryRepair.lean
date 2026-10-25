import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.AdjacentBandBoundaryRepair

theorem two_adjacent_TT_pairs_impossible (a b c d : Bool)
    (feasible : b = true → (if a then 1 else 0) + (if c then 1 else 0) ≤ (1 : Nat)) :
    ¬ ((a = true ∧ b = true) ∧ (c = true ∧ d = true)) := by
  cases a <;> cases b <;> cases c <;> cases d <;> simp_all

theorem adjacent_pair_has_positive_unit (above below : Nat)
    (balancedAbove balancedBelow : Prop)
    (zeroAbove : above = 0 → balancedAbove)
    (zeroBelow : below = 0 → balancedBelow)
    (incompatible : ¬ (balancedAbove ∧ balancedBelow)) : 1 ≤ above + below := by
  by_cases a : above = 0
  · by_cases b : below = 0
    · exact False.elim (incompatible ⟨zeroAbove a, zeroBelow b⟩)
    · omega
  · omega

def chosenBand (pair : Nat) (second : Bool) : Nat :=
  2 * pair + if second then 1 else 0

theorem chosen_band_in_pair (pair : Nat) (second : Bool) :
    2 * pair ≤ chosenBand pair second ∧ chosenBand pair second < 2 * pair + 2 := by
  cases second <;> simp [chosenBand] <;> omega

theorem disjoint_pairs_choose_distinct_bands (u v : Nat) (a b : Bool)
    (same : chosenBand u a = chosenBand v b) : u = v := by
  cases a <;> cases b <;> simp [chosenBand] at same <;> omega

theorem run_pair_count (bands pairs : Nat) (pairing : 2 * pairs ≤ bands)
    (leftover : bands < 2 * pairs + 2) : pairs = bands / 2 := by omega

theorem global_exposed_band_budget (units guards beta alpha margin : Int)
    (incidenceBound : guards ≤ 2 * units)
    (ledger : margin = units + beta - alpha) :
    2 * beta + guards - 2 * alpha ≤ 2 * margin := by omega

theorem global_coefficient_one_criterion (units guards beta alpha margin : Int)
    (incidenceBound : guards ≤ 2 * units)
    (ledger : margin = units + beta - alpha)
    (criterion : 2 * alpha - 1 ≤ guards + 2 * beta) : 0 ≤ margin := by omega

-- These are the cut ledger and restored-owner identities, not extra credits.
theorem restored_interface_coefficient_one
    (units guards localBeta localAlpha boundaryB boundaryCC crossing
      interfaceBeta interfaceAlpha margin : Int)
    (cutLedger : margin = units + localBeta - localAlpha + boundaryB + boundaryCC - crossing)
    (restore : boundaryB + boundaryCC - crossing = interfaceBeta - interfaceAlpha)
    (incidenceBound : guards ≤ 2 * units)
    (criterion : 2 * (localAlpha + interfaceAlpha) - 1 ≤
      guards + 2 * (localBeta + interfaceBeta)) : 0 ≤ margin := by omega

theorem uniform_four_guard_slack (units guards beta alpha margin : Int)
    (fourPerAlpha : 4 * alpha ≤ guards)
    (incidenceBound : guards ≤ 2 * units)
    (ledger : margin = units + beta - alpha) : beta + alpha ≤ margin := by omega

theorem private_four_guard_slack (units guards beta alpha margin : Int)
    (fourPerAlpha : 4 * alpha ≤ guards)
    (privateIncidenceBound : guards ≤ units)
    (ledger : margin = units + beta - alpha) : beta + 3 * alpha ≤ margin := by omega

theorem alternating_reachable_withdrawal_bound (g sources deficit withdrawn : Nat)
    (atLeastTwo : 2 ≤ g) (unmatchedSubset : deficit ≤ sources)
    (incidences : g * sources ≤ 2 * (sources - deficit + withdrawn)) :
    g * deficit ≤ 2 * withdrawn := by
  have splitSources : sources = deficit + (sources - deficit) := by omega
  have extra : 2 * (sources - deficit) ≤ g * (sources - deficit) :=
    Nat.mul_le_mul_right (sources - deficit) atLeastTwo
  rw [splitSources, Nat.mul_add] at incidences
  omega

theorem small_withdrawal_keeps_two_neighbours (g withdrawn remaining : Nat)
    (fewRemoved : withdrawn + 2 ≤ g) (oldNeighbours : g ≤ remaining + withdrawn) :
    2 ≤ remaining := by omega

theorem private_disjoint_reserve_bound (g unpaid lost withdrawn : Nat)
    (onlyLostCanBeUnpaid : unpaid ≤ lost)
    (differentLostPrivateUnits : g * lost ≤ withdrawn) : g * unpaid ≤ withdrawn := by
  exact Nat.le_trans (Nat.mul_le_mul_left g onlyLostCanBeUnpaid) differentLostPrivateUnits

theorem four_private_reserves (unpaid withdrawn : Nat)
    (differentPrivateUnits : 4 * unpaid ≤ withdrawn) : unpaid ≤ withdrawn / 4 := by omega

theorem arbitrary_copy_slack (q : Int) :
    (32 * q - 2) * 15 - 72 * q - 72 * q = 336 * q - 30 := by omega

theorem arbitrary_copy_port_defects (q : Nat) : 2 * (2 * q) = 4 * q := by omega

theorem arbitrary_copy_positive_margin (q : Int) (nonempty : 1 ≤ q) :
    0 < 336 * q - 30 := by omega

end SubQuorum.AdjacentBandBoundaryRepair

#print axioms SubQuorum.AdjacentBandBoundaryRepair.two_adjacent_TT_pairs_impossible
#print axioms SubQuorum.AdjacentBandBoundaryRepair.adjacent_pair_has_positive_unit
#print axioms SubQuorum.AdjacentBandBoundaryRepair.chosen_band_in_pair
#print axioms SubQuorum.AdjacentBandBoundaryRepair.disjoint_pairs_choose_distinct_bands
#print axioms SubQuorum.AdjacentBandBoundaryRepair.run_pair_count
#print axioms SubQuorum.AdjacentBandBoundaryRepair.global_exposed_band_budget
#print axioms SubQuorum.AdjacentBandBoundaryRepair.global_coefficient_one_criterion
#print axioms SubQuorum.AdjacentBandBoundaryRepair.restored_interface_coefficient_one
#print axioms SubQuorum.AdjacentBandBoundaryRepair.uniform_four_guard_slack
#print axioms SubQuorum.AdjacentBandBoundaryRepair.private_four_guard_slack
#print axioms SubQuorum.AdjacentBandBoundaryRepair.alternating_reachable_withdrawal_bound
#print axioms SubQuorum.AdjacentBandBoundaryRepair.small_withdrawal_keeps_two_neighbours
#print axioms SubQuorum.AdjacentBandBoundaryRepair.private_disjoint_reserve_bound
#print axioms SubQuorum.AdjacentBandBoundaryRepair.four_private_reserves
#print axioms SubQuorum.AdjacentBandBoundaryRepair.arbitrary_copy_slack
#print axioms SubQuorum.AdjacentBandBoundaryRepair.arbitrary_copy_port_defects
#print axioms SubQuorum.AdjacentBandBoundaryRepair.arbitrary_copy_positive_margin
