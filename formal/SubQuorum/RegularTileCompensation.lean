import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 20000000

namespace SubQuorum.RegularTileCompensation

abbrev Point := Int × Int

def rotorEndpoints : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorSelected : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def core : List Point :=
  [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
   (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,1),(3,1),(4,1)]

def quarter (point : Point) : Point := (point.2, 5-point.1)

def orient (mirror : Bool) (point : Point) : Point :=
  if mirror then (point.1,-point.2) else point

def anchored (mirror : Bool) (role : Fin 8) (target point : Point) : Point :=
  let source := orient mirror rotorEndpoints[role.val]
  let moved := orient mirror point
  (moved.1+target.1-source.1, moved.2+target.2-source.2)

def endpointAt (mirror : Bool) (role : Fin 8) (target point : Point) : Bool :=
  rotorEndpoints.any fun source => anchored mirror role target source == point

def occupiedAt (mirror : Bool) (role : Fin 8) (target point : Point) : Bool :=
  (rotorEndpoints++rotorSelected).any fun source => anchored mirror role target source == point

def blocked (mirror : Bool) (role : Fin 8) (target : Point) : Bool :=
  core.any fun point => endpointAt mirror role target point

theorem quarter_endpoints :
    rotorEndpoints.all (fun point => rotorEndpoints.contains (quarter point)) = true := by decide

theorem quarter_selections :
    rotorSelected.all (fun point => rotorSelected.contains (quarter point)) = true := by decide

theorem translation_determined (source point target : Point) (rowShift columnShift : Int)
    (hrow : source.1+rowShift = target.1) (hcolumn : source.2+columnShift = target.2) :
    (point.1+rowShift, point.2+columnShift) =
      (point.1+target.1-source.1, point.2+target.2-source.2) := by
  apply Prod.ext
  · change point.1+rowShift = point.1+target.1-source.1
    omega
  · change point.2+columnShift = point.2+target.2-source.2
    omega

theorem rotor_gate_blocked : ∀ mirror : Bool, ∀ role : Fin 8,
    blocked mirror role (2,2) = true := by decide

theorem rotor_selection_blocked_or_gate_occupied : ∀ mirror : Bool, ∀ role : Fin 8,
    (blocked mirror role (3,2) || occupiedAt mirror role (3,2) (2,2)) = true := by decide

theorem rotor_opposite_blocked_or_gate_occupied : ∀ mirror : Bool, ∀ role : Fin 8,
    (blocked mirror role (2,3) || occupiedAt mirror role (2,3) (2,2)) = true := by decide

def present (mask : Fin 16) (corner : Fin 4) : Bool := mask.val.testBit corner.val

def adjacent (first second : Fin 4) : Bool :=
  (first.val+1)%4 == second.val || (second.val+1)%4 == first.val

def profiles : List (Fin 16 × Fin 16) :=
  [(1,10),(2,5),(4,10),(8,5),(3,4),(3,8),(6,1),(6,8),
   (12,1),(12,2),(9,2),(9,4),(15,0),(7,0),(11,0),(13,0),(14,0)]

def profile (index : Fin 17) : Fin 16 × Fin 16 := profiles[index.val]

def corners (mask : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present mask corner).length

def validFinal (index : Fin 17) (finalEndpoints finalSelected : Fin 16) : Prop :=
  (∀ corner : Fin 4, present (profile index).1 corner = true →
    present finalEndpoints corner = true) ∧
  (∀ corner : Fin 4, present (profile index).2 corner = true →
    present finalEndpoints corner = true ∨ present finalSelected corner = true) ∧
  (∀ corner : Fin 4, present finalSelected corner = true →
    present finalEndpoints corner = false ∧
      ((List.finRange 4).filter fun other => adjacent corner other &&
        (present finalEndpoints other || present finalSelected other)).length ≤ 1)

instance (index : Fin 17) (finalEndpoints finalSelected : Fin 16) :
    Decidable (validFinal index finalEndpoints finalSelected) := by
  unfold validFinal
  infer_instance

def internalTails (index : Fin 17) (finalEndpoints : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present (profile index).1 corner &&
    (List.finRange 4).any (fun other => adjacent corner other &&
      !(present (profile index).1 other || present (profile index).2 other) &&
      present finalEndpoints other)).length

def capacity (count : Nat) : Nat := if count = 2 then 1 else if count = 3 then 2 else 0

theorem regular_event_forces_full : ∀ index : Fin 17,
    ∀ finalEndpoints finalSelected : Fin 16, validFinal index finalEndpoints finalSelected →
    0 < internalTails index finalEndpoints → finalEndpoints = 15 := by decide

theorem regular_profile_capacity : ∀ index : Fin 17, ∀ finalEndpoints : Fin 16,
    internalTails index finalEndpoints ≤ capacity (corners (profile index).1) := by decide

def label (pattern : Fin 625) (corner : Fin 4) : Nat := pattern.val / 5^corner.val % 5

def labelCount (pattern : Fin 625) (owner : Nat) : Nat :=
  ((List.finRange 4).filter fun corner => label pattern corner == owner).length

def partitionCapacity (pattern : Fin 625) : Nat :=
  ((List.range 4).map fun owner => capacity (labelCount pattern (owner+1))).sum

theorem full_tile_partition_capacity : ∀ pattern : Fin 625,
    (∀ corner : Fin 4, 0 < label pattern corner) → partitionCapacity pattern ≤ 2 := by decide

def irregularProfiles : List (Fin 16 × Fin 16) :=
  [(1,2),(1,8),(2,1),(2,4),(4,2),(4,8),(8,1),(8,4),(3,0),(6,0),(12,0),(9,0)]

def irregularProfile (index : Fin 12) : Fin 16 × Fin 16 := irregularProfiles[index.val]

def irregularTails (index : Fin 12) (finalEndpoints : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present (irregularProfile index).1 corner &&
    (List.finRange 4).any (fun other => adjacent corner other &&
      !(present (irregularProfile index).1 other || present (irregularProfile index).2 other) &&
      present finalEndpoints other)).length

theorem irregular_profile_capacity : ∀ index : Fin 12, ∀ finalEndpoints : Fin 16,
    irregularTails index finalEndpoints ≤ corners (irregularProfile index).1 := by decide

theorem irregular_full_tail_count : ∀ index : Fin 12,
    irregularTails index 15 = corners (irregularProfile index).1 := by decide

theorem column_phase_potential : (2 : Int) = 2*1 := by decide

theorem row_phase_potential (width : Int) : 2*(width-2)+2 = 2*(width-1) := by omega

theorem diagonal_phase_potential (width : Int) : 2*(width-2) = 2*(width-1)-2 := by omega

theorem rotor_negative_potential : (4 : Int) = 2*2 := by decide

theorem mixed_irregular_budget
    (slack positive negativeMass squares regular irregular marked credit : Int)
    (hbudget : positive+negativeMass+2*squares-(regular+irregular)-marked ≤ slack)
    (hcredit : credit = 2*squares-regular) :
    positive+negativeMass+credit-irregular-marked ≤ slack := by omega

theorem height_independent_budget
    (slack positive negativeMass diagonal credit irregular marked : Int)
    (hbudget : positive+negativeMass+credit-irregular-marked ≤ slack)
    (hpotential : irregular ≤ 2*negativeMass-2*diagonal) :
    positive-negativeMass+2*diagonal+credit-marked ≤ slack := by omega

theorem zero_rotor_automatic_budget
    (halfArea selected matching deficit charge positive squares events : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge = positive-2*squares+events)
    (hdonors : 2*positive ≤ deficit) (hcapacity : events ≤ 2*squares) :
    positive ≤ halfArea-selected-matching := by omega

theorem arbitrary_rotor_coarse_budget
    (slack positive negativeRotors credit irregular : Int)
    (hbudget : positive+2*negativeRotors+credit-irregular ≤ slack)
    (hpotential : irregular ≤ 4*negativeRotors) :
    positive-2*negativeRotors+credit ≤ slack := by omega

theorem arbitrary_rotor_sufficient
    (slack positive negativeRotors credit : Int)
    (hbudget : positive-2*negativeRotors+credit ≤ slack)
    (hcredit : 0 ≤ credit) (hpositive : 2*negativeRotors ≤ positive) :
    0 ≤ slack := by omega

theorem zero_rotor_chain_cancellation (amount : Int) :
    4*(amount-1) = 2*(2*(amount-1)) := by omega

theorem zero_rotor_chain_charge (amount : Int) :
    (4 : Int)+4*amount-2*(2*amount+2) = 0 := by omega

end SubQuorum.RegularTileCompensation
