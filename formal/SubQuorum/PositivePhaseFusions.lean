import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 16000000

namespace SubQuorum.PositivePhaseFusions

def present (mask : Fin 16) (corner : Fin 4) : Bool := mask.val.testBit corner.val

def adjacent (first second : Fin 4) : Bool :=
  (first.val+1)%4 == second.val || (second.val+1)%4 == first.val

def profiles : List (Fin 16 × Fin 16) :=
  [(1,10),(2,5),(4,10),(8,5),(3,4),(3,8),(6,1),(6,8),
   (12,1),(12,2),(9,2),(9,4),(15,0)]

def profile (index : Fin 13) : Fin 16 × Fin 16 := profiles[index.val]

def corners (mask : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present mask corner).length

def validFinal (index : Fin 13) (finalEndpoints finalSelected : Fin 16) : Prop :=
  (∀ corner : Fin 4, present (profile index).1 corner = true →
    present finalEndpoints corner = true) ∧
  (∀ corner : Fin 4, present (profile index).2 corner = true →
    present finalEndpoints corner = true ∨ present finalSelected corner = true) ∧
  (∀ corner : Fin 4, present finalSelected corner = true →
    present finalEndpoints corner = false ∧
      ((List.finRange 4).filter fun other => adjacent corner other &&
        (present finalEndpoints other || present finalSelected other)).length ≤ 1)

instance (index : Fin 13) (finalEndpoints finalSelected : Fin 16) :
    Decidable (validFinal index finalEndpoints finalSelected) := by
  unfold validFinal
  infer_instance

def internalTails (index : Fin 13) (finalEndpoints : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present (profile index).1 corner &&
    (List.finRange 4).any (fun other => adjacent corner other &&
      !(present (profile index).1 other || present (profile index).2 other) &&
      present finalEndpoints other)).length

theorem internal_event_forces_full : ∀ index : Fin 13,
    ∀ finalEndpoints finalSelected : Fin 16,
    validFinal index finalEndpoints finalSelected →
    0 < internalTails index finalEndpoints → finalEndpoints = 15 := by decide

theorem each_profile_at_most_one_tail : ∀ index : Fin 13,
    ∀ finalEndpoints : Fin 16, internalTails index finalEndpoints ≤ 1 := by decide

theorem event_uses_two_original_endpoints : ∀ index : Fin 13,
    ∀ finalEndpoints : Fin 16, 0 < internalTails index finalEndpoints →
    corners (profile index).1 = 2 := by decide

theorem profile_receiver_charge : ∀ index : Fin 13,
    2*(corners (profile index).2 : Int)+(corners (profile index).1 : Int)-4 =
      if corners (profile index).1 = 1 then 1 else 0 := by decide

theorem exterior_gate_excludes {Owner Point : Type}
    (endpoint : Owner → Point → Prop) (reference foreign : Owner)
    (gate first second : Point)
    (hdisjoint : ∀ point, endpoint reference point → ¬endpoint foreign point)
    (hfirst : endpoint reference first) (hsecond : endpoint reference second)
    (hexterior : endpoint foreign gate → endpoint foreign first ∨ endpoint foreign second) :
    ¬endpoint foreign gate := by
  intro hgate
  rcases hexterior hgate with hneighbor | hneighbor
  · exact hdisjoint first hfirst hneighbor
  · exact hdisjoint second hsecond hneighbor

theorem continuation_excludes {Owner Point : Type}
    (endpoint : Owner → Point → Prop) (reference foreign : Owner)
    (candidate continuation : Point)
    (hdisjoint : ∀ point, endpoint reference point → ¬endpoint foreign point)
    (hold : endpoint reference continuation)
    (hcontinuation : endpoint foreign candidate → endpoint foreign continuation) :
    ¬endpoint foreign candidate := by
  intro hcandidate
  exact hdisjoint continuation hold (hcontinuation hcandidate)

theorem retained_support {Endpoint Selected : Prop}
    (hretained : Endpoint ∨ Selected) (hnot : ¬Endpoint) : Selected := by
  exact hretained.resolve_left hnot

theorem full_tile_defect_le_two (events : Nat) (hdisjointPairs : 2*events ≤ 4) :
    events ≤ 2 := by omega

theorem summed_tile_cancellation (events squares : Int)
    (hcapacity : events ≤ 2*squares) : -2*squares+events ≤ 0 := by omega

theorem automatic_positive_compensation
    (halfArea selected matching deficit charge modules squares events : Int)
    (hledger : halfArea-selected-matching = deficit-charge)
    (hcharge : charge = modules-2*squares+events)
    (hdonors : 2*modules ≤ deficit) (hcapacity : events ≤ 2*squares) :
    modules ≤ halfArea-selected-matching := by omega

theorem automatic_finer_criterion (events squares : Int)
    (hcapacity : events ≤ 2*squares) : events+0 ≤ 0+2*squares := by omega

theorem unspent_square_credit (positiveEvents squares credit : Int)
    (hcapacity : positiveEvents ≤ 2*squares)
    (hcredit : credit = 2*squares-positiveEvents) : 0 ≤ credit := by omega

theorem mixed_positive_tail_budget
    (halfArea selected matching modules negativeMass squares positiveEvents
      otherEvents marked credit : Int)
    (hbudget : modules+negativeMass+2*squares-(positiveEvents+otherEvents)-marked ≤
      halfArea-selected-matching)
    (hcredit : credit = 2*squares-positiveEvents) :
    modules+negativeMass+credit-otherEvents-marked ≤ halfArea-selected-matching := by omega

theorem mixed_positive_tail_compensation
    (halfArea selected matching modules negativeMass credit otherEvents marked : Int)
    (hbudget : modules+negativeMass+credit-otherEvents-marked ≤
      halfArea-selected-matching)
    (hcredit : 0 ≤ credit) (hpayment : otherEvents+marked ≤ modules+negativeMass) :
    selected+matching ≤ halfArea := by omega

end SubQuorum.PositivePhaseFusions
