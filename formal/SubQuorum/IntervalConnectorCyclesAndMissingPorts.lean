import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.IntervalConnectorCyclesAndMissingPorts

def localDegree (leftOccupied rightOccupied : Bool) : Nat :=
  2 + (if leftOccupied then 1 else 0) + (if rightOccupied then 1 else 0)

def localPorts (leftOccupied rightOccupied : Bool) : Nat :=
  (if leftOccupied then 0 else 1) + (if rightOccupied then 0 else 1)

theorem terminal_port_degree_inventory (leftOccupied rightOccupied : Bool) :
    localPorts leftOccupied rightOccupied + localDegree leftOccupied rightOccupied = 4 := by
  cases leftOccupied <;> cases rightOccupied <;> decide

theorem terminal_missing_iff_degree_four (leftOccupied rightOccupied : Bool) :
    localPorts leftOccupied rightOccupied = 0 ↔ localDegree leftOccupied rightOccupied = 4 := by
  cases leftOccupied <;> cases rightOccupied <;> decide

theorem missing_paths_and_degree_four_inventory (missing degreeFour bothMissing : Nat)
    (eachMissingHasOneOrTwo : degreeFour = missing + bothMissing)
    (atMostOneExtraPerPath : bothMissing ≤ missing) :
    missing ≤ degreeFour ∧ degreeFour ≤ 2 * missing := by omega

inductive Piece where
  | path (edges : Nat) (marks : Fin 3)
  | cycle (extraEdges : Nat)

def vertices : Piece → Int
  | .path edges _ => edges + 1
  | .cycle extraEdges => extraEdges + 1

def edges : Piece → Int
  | .path count _ => count
  | .cycle extraEdges => extraEdges + 1

def marks : Piece → Int
  | .path _ boundary => boundary.val
  | .cycle _ => 0

def paths : Piece → Int
  | .path _ _ => 1
  | .cycle _ => 0

def cycles : Piece → Int
  | .path _ _ => 0
  | .cycle _ => 1

def pathsWith (count : Nat) : Piece → Int
  | .path _ boundary => if boundary.val = count then 1 else 0
  | .cycle _ => 0

def total (measure : Piece → Int) : List Piece → Int
  | [] => 0
  | piece :: rest => measure piece + total measure rest

theorem finite_multigraph_euler (pieces : List Piece) :
    total vertices pieces - total edges pieces = total paths pieces := by
  induction pieces with
  | nil => rfl
  | cons piece rest inductionHypothesis =>
    cases piece <;> simp_all [total, vertices, edges, paths] <;> omega

theorem path_component_partition (pieces : List Piece) :
    total paths pieces = total (pathsWith 0) pieces +
      total (pathsWith 1) pieces + total (pathsWith 2) pieces := by
  induction pieces with
  | nil => rfl
  | cons piece rest inductionHypothesis =>
    cases piece with
    | cycle extraEdges => simpa [total, paths, pathsWith] using inductionHypothesis
    | path edgeCount boundary =>
      have bound := boundary.isLt
      have alternatives : boundary.val = 0 ∨ boundary.val = 1 ∨ boundary.val = 2 := by omega
      rcases alternatives with zero | one | two <;>
        simp_all [total, paths, pathsWith] <;> omega

theorem boundary_inventory (pieces : List Piece) :
    total marks pieces = total (pathsWith 1) pieces + 2 * total (pathsWith 2) pieces := by
  induction pieces with
  | nil => rfl
  | cons piece rest inductionHypothesis =>
    cases piece with
    | cycle extraEdges => simpa [total, marks, pathsWith] using inductionHypothesis
    | path edgeCount boundary =>
      have bound := boundary.isLt
      have alternatives : boundary.val = 0 ∨ boundary.val = 1 ∨ boundary.val = 2 := by omega
      rcases alternatives with zero | one | two <;>
        simp_all [total, marks, pathsWith] <;> omega

theorem exact_partial_connector_compensation (pieces : List Piece)
    (surplus beta alpha omitted : Int)
    (ppLedger : surplus = total vertices pieces + beta - alpha)
    (pathInventory : alpha = total edges pieces + omitted) :
    surplus - total marks pieces = total (pathsWith 0) pieces + beta -
      total (pathsWith 2) pieces - omitted := by
  have euler := finite_multigraph_euler pieces
  have partition := path_component_partition pieces
  have boundary := boundary_inventory pieces
  omega

theorem packet_bound_iff (pieces : List Piece) (surplus beta alpha omitted : Int)
    (ppLedger : surplus = total vertices pieces + beta - alpha)
    (pathInventory : alpha = total edges pieces + omitted) :
    total marks pieces ≤ surplus ↔
      total (pathsWith 2) pieces + omitted ≤ total (pathsWith 0) pieces + beta := by
  have identity := exact_partial_connector_compensation pieces surplus beta alpha omitted
    ppLedger pathInventory
  omega

theorem all_interior_component_correction (interiorPaths cycleCount allInterior beta
    collisions omitted surplus boundary : Int)
    (allComponents : allInterior = interiorPaths + cycleCount)
    (pathLedger : surplus - boundary = interiorPaths + beta - collisions - omitted) :
    surplus - boundary = allInterior + beta - collisions - omitted - cycleCount := by omega

theorem injection_budget_suffices (surplus boundary interiorPaths beta collisions omitted : Int)
    (ledger : surplus - boundary = interiorPaths + beta - collisions - omitted)
    (distinctResourceBudget : collisions + omitted ≤ interiorPaths + beta) :
    boundary ≤ surplus := by omega

theorem global_with_outside_overlap (margin boundary interiorPaths beta collisions omitted
    deficit positive negative shared : Int)
    (ledger : margin = boundary + interiorPaths + beta - collisions - omitted +
      deficit - positive + negative - 2 * shared)
    (ownedInternal : collisions + omitted ≤ interiorPaths + beta)
    (ownedOutside : positive + 2 * shared ≤ boundary + deficit + negative) :
    0 ≤ margin := by omega

theorem parallel_cycle_has_zero_euler :
    total vertices [.cycle 1] - total edges [.cycle 1] = 0 := by decide

theorem any_cycle_length_has_zero_euler (extraEdges : Nat) :
    total vertices [.cycle extraEdges] - total edges [.cycle extraEdges] = 0 := by
  simp [total, vertices, edges]

theorem cycle_count_not_an_extra_path_debit (pathCount cycleCount surplus : Int)
    (actual : surplus = pathCount) (cyclePresent : 0 < cycleCount) :
    pathCount - cycleCount < surplus := by omega

theorem omitted_paths_are_full_debits (surplus boundary interiorPaths beta collisions omitted : Int)
    (ledger : surplus - boundary = interiorPaths + beta - collisions - omitted) :
    interiorPaths + beta - collisions - (surplus - boundary) = omitted := by omega

theorem mirrored_shared_selection_count (height : Int) :
    2 * (height + 11) - 4 = 2 * height + 18 := by omega

theorem cycle_family_target_margin (surplus area width height : Int)
    (areaNonnegative : 0 ≤ area) (wide : 6 ≤ width) (tall : 4 ≤ height)
    (inventory : surplus = area + 4 * width + 8 * height + 54) :
    0 < surplus - (width + 12) := by omega

theorem missing_port_family_target_margin (surplus area width height : Int)
    (areaNonnegative : 0 ≤ area) (wide : 6 ≤ width) (tall : 4 ≤ height)
    (inventory : surplus = area + 5 * width + 10 * height + 63) :
    0 < surplus - (width + 12) := by omega

theorem connector_choice_invariance (surplus boundary firstInterior firstBeta firstCollision
    firstOmitted secondInterior secondBeta secondCollision secondOmitted : Int)
    (firstLedger : surplus - boundary = firstInterior + firstBeta - firstCollision - firstOmitted)
    (secondLedger : surplus - boundary = secondInterior + secondBeta - secondCollision - secondOmitted) :
    firstInterior + firstBeta - firstCollision - firstOmitted =
      secondInterior + secondBeta - secondCollision - secondOmitted := by omega

end SubQuorum.IntervalConnectorCyclesAndMissingPorts

#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.terminal_port_degree_inventory
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.terminal_missing_iff_degree_four
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.missing_paths_and_degree_four_inventory
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.finite_multigraph_euler
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.path_component_partition
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.boundary_inventory
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.exact_partial_connector_compensation
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.packet_bound_iff
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.all_interior_component_correction
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.injection_budget_suffices
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.global_with_outside_overlap
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.parallel_cycle_has_zero_euler
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.any_cycle_length_has_zero_euler
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.cycle_count_not_an_extra_path_debit
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.omitted_paths_are_full_debits
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.mirrored_shared_selection_count
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.cycle_family_target_margin
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.missing_port_family_target_margin
#print axioms SubQuorum.IntervalConnectorCyclesAndMissingPorts.connector_choice_invariance
