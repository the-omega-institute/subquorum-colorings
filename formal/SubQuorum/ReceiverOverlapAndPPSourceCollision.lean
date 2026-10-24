import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ReceiverOverlapAndPPSourceCollision

def label (profile : Fin 81) (position : Nat) : Nat :=
  profile.val / 3 ^ position % 3

def occupied (profile : Fin 81) (position : Nat) : Nat :=
  if label profile position = 0 then 0 else 1

def horizontal (position : Fin 4) : Nat :=
  if position.val % 2 = 0 then position.val + 1 else position.val - 1

def vertical (position : Fin 4) : Nat :=
  if position.val < 2 then position.val + 2 else position.val - 2

def feasible (profile : Fin 81) : Prop :=
  ∀ position : Fin 4, label profile position.val = 1 →
    occupied profile (horizontal position) + occupied profile (vertical position) ≤ 1

instance (profile : Fin 81) : Decidable (feasible profile) :=
  inferInstanceAs (Decidable (∀ position : Fin 4, label profile position.val = 1 →
    occupied profile (horizontal position) + occupied profile (vertical position) ≤ 1))

def disconnectedProfile (profile : Fin 81) : Prop :=
  (label profile 0 = 2 ∧ label profile 3 = 2 ∧ label profile 1 ≠ 2 ∧ label profile 2 ≠ 2) ∨
  (label profile 1 = 2 ∧ label profile 2 = 2 ∧ label profile 0 ≠ 2 ∧ label profile 3 ≠ 2)

instance (profile : Fin 81) : Decidable (disconnectedProfile profile) :=
  inferInstanceAs (Decidable ((label profile 0 = 2 ∧ label profile 3 = 2 ∧
    label profile 1 ≠ 2 ∧ label profile 2 ≠ 2) ∨ (label profile 1 = 2 ∧
    label profile 2 = 2 ∧ label profile 0 ≠ 2 ∧ label profile 3 ≠ 2)))

def sharedShape (profile : Fin 81) : Prop :=
  (label profile 0 = 2 ∧ label profile 3 = 2 ∧ label profile 1 = 0 ∧ label profile 2 = 0) ∨
  (label profile 1 = 2 ∧ label profile 2 = 2 ∧ label profile 0 = 0 ∧ label profile 3 = 0)

instance (profile : Fin 81) : Decidable (sharedShape profile) :=
  inferInstanceAs (Decidable ((label profile 0 = 2 ∧ label profile 3 = 2 ∧
    label profile 1 = 0 ∧ label profile 2 = 0) ∨ (label profile 1 = 2 ∧
    label profile 2 = 2 ∧ label profile 0 = 0 ∧ label profile 3 = 0)))

theorem disconnected_tile_has_two_blanks (profile : Fin 81)
    (legal : feasible profile) (disconnected : disconnectedProfile profile) : sharedShape profile := by
  have checked : ∀ profile : Fin 81, feasible profile → disconnectedProfile profile →
      sharedShape profile := by decide
  exact checked profile legal disconnected

def selectedCorners (profile : Fin 81) : Nat :=
  (if label profile 0 = 1 then 1 else 0) + (if label profile 1 = 1 then 1 else 0) +
  (if label profile 2 = 1 then 1 else 0) + (if label profile 3 = 1 then 1 else 0)

theorem feasible_tile_has_at_most_two_selections (profile : Fin 81)
    (legal : feasible profile) : selectedCorners profile ≤ 2 := by
  have checked : ∀ profile : Fin 81, feasible profile → selectedCorners profile ≤ 2 := by decide
  exact checked profile legal

theorem shared_tile_excluded_by_native_degree (degree : Nat)
    (twoBlankNeighbors : degree ≤ 2) (singleTerminal : 3 ≤ degree) : False := by omega

inductive ReceiverTile where
  | exclusive (selections : Fin 3)
  | shared

def componentPenalty : ReceiverTile → Int
  | .exclusive selections => 2 - selections.val
  | .shared => 4

def unionPenalty : ReceiverTile → Int
  | .exclusive selections => 2 - selections.val
  | .shared => 2

def sharedCount : ReceiverTile → Int
  | .exclusive _ => 0
  | .shared => 1

def tileSum (measure : ReceiverTile → Int) : List ReceiverTile → Int
  | [] => 0
  | tile :: rest => measure tile + tileSum measure rest

theorem exact_arbitrary_receiver_overlap (tiles : List ReceiverTile) :
    tileSum componentPenalty tiles - tileSum unionPenalty tiles =
      2 * tileSum sharedCount tiles := by
  induction tiles with
  | nil => rfl
  | cons tile rest inductionHypothesis =>
    cases tile <;> simp_all [tileSum, componentPenalty, unionPenalty, sharedCount] <;> omega

theorem exact_global_packet_ledger (margin packetSurplus deficit unionCharge
    componentCharge positive negative shared : Int)
    (physicalPartition : margin = packetSurplus + deficit - unionCharge)
    (overlap : unionCharge = componentCharge + 2 * shared)
    (signedComponents : componentCharge = positive - negative) :
    margin = packetSurplus + deficit - positive + negative - 2 * shared := by omega

theorem coefficient_one_with_overlap (margin packetSurplus deficit positive negative
    shared boundaryBudget : Int)
    (ledger : margin = packetSurplus + deficit - positive + negative - 2 * shared)
    (packetBounds : boundaryBudget ≤ packetSurplus) (deficitNonnegative : 0 ≤ deficit)
    (negativeNonnegative : 0 ≤ negative) (ownedBudget : positive + 2 * shared ≤ boundaryBudget) :
    0 ≤ margin := by omega

theorem uncorrected_ledger_excess (margin uncorrected shared : Int)
    (ledger : margin = uncorrected - 2 * shared) : uncorrected - margin = 2 * shared := by omega

inductive BoundaryBlock where
  | isolated
  | mergedPair

def sourceCount : BoundaryBlock → Nat
  | .isolated => 1
  | .mergedPair => 2

def collisionCount : BoundaryBlock → Nat
  | .isolated => 0
  | .mergedPair => 1

def boundarySum (measure : BoundaryBlock → Nat) : List BoundaryBlock → Nat
  | [] => 0
  | block :: rest => measure block + boundarySum measure rest

theorem arbitrary_boundary_source_inventory (blocks : List BoundaryBlock) :
    boundarySum sourceCount blocks = blocks.length + boundarySum collisionCount blocks := by
  induction blocks with
  | nil => rfl
  | cons block rest inductionHypothesis =>
    cases block <;> simp_all [boundarySum, sourceCount, collisionCount] <;> omega

theorem exact_source_component_loss (blocks : List BoundaryBlock) (sources collisions : Nat)
    (sourceInventory : sources = boundarySum sourceCount blocks)
    (collisionInventory : collisions = boundarySum collisionCount blocks) :
    blocks.length + collisions = sources := by
  have identity := arbitrary_boundary_source_inventory blocks
  omega

theorem source_injection_fails_with_a_collision (components sources collisions : Nat)
    (inventory : components + collisions = sources) (collision : 1 ≤ collisions) :
    components < sources := by omega

theorem both_boundary_component_inventory (first last total bands collisions : Int)
    (firstCount : first = bands - collisions) (lastCount : last = bands)
    (disjointBoundaryComponents : total = first + last) : total = 2 * bands - collisions := by omega

theorem all_matching_edges_accounted (halfWidth halfHeight : Nat) (wide : 3 ≤ halfWidth) :
    halfWidth + (halfWidth - 1) + (2 * halfHeight + 1) =
      2 * halfWidth + 2 * halfHeight := by omega

theorem unused_interior_reserve (surplus boundaryComponents bands collisions interior : Int)
    (boundaryInventory : boundaryComponents = 2 * bands - collisions)
    (componentPartition : surplus = boundaryComponents + interior) :
    surplus - 2 * bands = interior - collisions := by omega

theorem collision_family_unit_target_holds (surplus areaTerm width height : Int)
    (areaNonnegative : 0 ≤ areaTerm) (wide : 6 ≤ width) (tall : 4 ≤ height)
    (surplusCount : surplus = areaTerm + 2 * width + 4 * height + 25) :
    0 < surplus - (width + 12) := by omega

end SubQuorum.ReceiverOverlapAndPPSourceCollision

#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.disconnected_tile_has_two_blanks
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.feasible_tile_has_at_most_two_selections
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.shared_tile_excluded_by_native_degree
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.exact_arbitrary_receiver_overlap
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.exact_global_packet_ledger
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.coefficient_one_with_overlap
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.uncorrected_ledger_excess
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.arbitrary_boundary_source_inventory
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.exact_source_component_loss
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.source_injection_fails_with_a_collision
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.both_boundary_component_inventory
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.all_matching_edges_accounted
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.unused_interior_reserve
#print axioms SubQuorum.ReceiverOverlapAndPPSourceCollision.collision_family_unit_target_holds
