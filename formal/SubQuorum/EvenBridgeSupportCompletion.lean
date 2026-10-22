import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.EvenBridgeSupportCompletion

def occupied (label : Fin 3) : Nat := if label = 0 then 0 else 1
def endpoint (label : Fin 3) : Nat := if label = 2 then 1 else 0

def selectedFeasible (corner first second : Fin 3) : Prop :=
  corner = 1 → occupied first + occupied second ≤ 1

def endpointSupported (corner first second : Fin 3) : Prop :=
  corner = 2 → 1 ≤ occupied first + occupied second

def tileValid (northwest northeast southwest southeast : Fin 3) : Prop :=
  selectedFeasible northwest northeast southwest ∧
  selectedFeasible northeast northwest southeast ∧
  selectedFeasible southwest northwest southeast ∧
  selectedFeasible southeast northeast southwest ∧
  endpointSupported northwest northeast southwest ∧
  endpointSupported northeast northwest southeast ∧
  endpointSupported southwest northwest southeast ∧
  endpointSupported southeast northeast southwest

def anchored (corner first second : Fin 3) : Prop :=
  corner = 1 → 1 ≤ endpoint first + endpoint second

def tileAnchored (northwest northeast southwest southeast : Fin 3) : Prop :=
  anchored northwest northeast southwest ∧
  anchored northeast northwest southeast ∧
  anchored southwest northwest southeast ∧
  anchored southeast northeast southwest

def tileConnected (northwest northeast southwest southeast : Fin 3) : Prop :=
  (northwest = 2 ∧ southeast = 2 → northeast = 2 ∨ southwest = 2) ∧
  (northeast = 2 ∧ southwest = 2 → northwest = 2 ∨ southeast = 2)

instance (corner first second : Fin 3) : Decidable (selectedFeasible corner first second) := by
  unfold selectedFeasible
  infer_instance

instance (corner first second : Fin 3) : Decidable (endpointSupported corner first second) := by
  unfold endpointSupported
  infer_instance

instance (corner first second : Fin 3) : Decidable (anchored corner first second) := by
  unfold anchored
  infer_instance

instance (northwest northeast southwest southeast : Fin 3) :
    Decidable (tileValid northwest northeast southwest southeast) := by
  unfold tileValid
  infer_instance

instance (northwest northeast southwest southeast : Fin 3) :
    Decidable (tileAnchored northwest northeast southwest southeast) := by
  unfold tileAnchored
  infer_instance

instance (northwest northeast southwest southeast : Fin 3) :
    Decidable (tileConnected northwest northeast southwest southeast) := by
  unfold tileConnected
  infer_instance

theorem endpoint_internal_neighbor (internal external : Nat)
    (hexternal : external ≤ 2) (hdegree : 3 ≤ internal + external) :
    1 ≤ internal := by omega

theorem selected_tile_anchoring (northwest northeast southwest southeast : Fin 3)
    (hvalid : tileValid northwest northeast southwest southeast)
    (hnonempty : 0 < endpoint northwest + endpoint northeast + endpoint southwest + endpoint southeast) :
    tileAnchored northwest northeast southwest southeast := by
  have checked : ∀ northwest northeast southwest southeast : Fin 3,
      tileValid northwest northeast southwest southeast →
      0 < endpoint northwest + endpoint northeast + endpoint southwest + endpoint southeast →
      tileAnchored northwest northeast southwest southeast := by decide
  exact checked northwest northeast southwest southeast hvalid hnonempty

theorem endpoint_tile_connectivity (northwest northeast southwest southeast : Fin 3)
    (hvalid : tileValid northwest northeast southwest southeast) :
    tileConnected northwest northeast southwest southeast := by
  have checked : ∀ northwest northeast southwest southeast : Fin 3,
      tileValid northwest northeast southwest southeast →
      tileConnected northwest northeast southwest southeast := by decide
  exact checked northwest northeast southwest southeast hvalid

theorem adjacent_occupied_supports_are_endpoints (first second : Fin 3)
    (hfirst : occupied first = 1) (hsecond : occupied second = 1)
    (hfirstFeasible : selectedFeasible first 2 second)
    (hsecondFeasible : selectedFeasible second 2 first) : first = 2 ∧ second = 2 := by
  have checked : ∀ first second : Fin 3,
      occupied first = 1 → occupied second = 1 →
      selectedFeasible first 2 second → selectedFeasible second 2 first →
      first = 2 ∧ second = 2 := by decide
  exact checked first second hfirst hsecond hfirstFeasible hsecondFeasible

theorem even_bridge_unused (half internal crossing : Nat)
    (hcount : 2 * half = 2 * internal + crossing) (hbridge : crossing ≤ 1) :
    crossing = 0 := by omega

theorem odd_bridge_forced (half internal crossing : Nat)
    (hcount : 2 * half + 1 = 2 * internal + crossing) (hbridge : crossing ≤ 1) :
    crossing = 1 := by omega

def charge (matching selected tiles : Int) : Int := matching + selected - 2 * tiles

theorem receiver_additivity
    (matching leftMatching rightMatching selected leftSelected rightSelected
      tiles leftTiles rightTiles shared : Int)
    (hmatching : matching = leftMatching + rightMatching)
    (hselected : leftSelected + rightSelected = selected + 2 * shared)
    (htiles : leftTiles + rightTiles = tiles + shared) :
    charge matching selected tiles =
      charge leftMatching leftSelected leftTiles + charge rightMatching rightSelected rightTiles := by
  unfold charge
  omega

theorem two_endpoint_correction (selected : Int) (hselected : selected = 1) :
    2 - selected = 1 := by omega

theorem three_endpoint_correction (crossBlock : Int) (hcross : 0 ≤ crossBlock ∧ crossBlock ≤ 1) :
    2 * (1 + crossBlock) = crossBlock + (2 + crossBlock) ∧
      2 ≤ 2 + crossBlock ∧ 2 + crossBlock ≤ 3 := by omega

theorem buffer_correction
    (rho leftRho rightRho interface leftInterface rightInterface
      buffer leftBuffer rightBuffer mixed leftMixed rightMixed correction : Int)
    (hglobal : rho = interface - 2 * mixed - buffer)
    (hleft : leftRho = leftInterface - 2 * leftMixed - leftBuffer)
    (hright : rightRho = rightInterface - 2 * rightMixed - rightBuffer)
    (hrho : rho = leftRho + rightRho)
    (hmixed : mixed = leftMixed + rightMixed)
    (hinterface : interface = leftInterface + rightInterface + correction) :
    buffer = leftBuffer + rightBuffer + correction := by omega

theorem net_interface_additivity
    (interface leftInterface rightInterface buffer leftBuffer rightBuffer correction : Int)
    (hinterface : interface = leftInterface + rightInterface + correction)
    (hbuffer : buffer = leftBuffer + rightBuffer + correction) :
    interface - buffer = (leftInterface - leftBuffer) + (rightInterface - rightBuffer) := by omega

def total : List Int → Int
  | [] => 0
  | head :: tail => head + total tail

theorem signed_split_invariance (left right : Int) (others : List Int) :
    total ((left + right) :: others) = total (left :: right :: others) := by
  simp only [total]
  omega

theorem nonpositive_piece_sum (pieces : List Int)
    (hnonpositive : ∀ piece ∈ pieces, piece ≤ 0) : total pieces ≤ 0 := by
  induction pieces with
  | nil => exact Int.le_refl 0
  | cons head tail inductionHypothesis =>
    have hhead : head ≤ 0 := hnonpositive head (List.mem_cons_self ..)
    have htail : total tail ≤ 0 := inductionHypothesis (by
      intro piece hmember
      exact hnonpositive piece (List.mem_cons_of_mem head hmember))
    simp only [total]
    omega

theorem original_deficit_compensation (areaHalf objective originalDeficit receiverSum : Int)
    (hledger : areaHalf - objective = originalDeficit - receiverSum)
    (hpayment : receiverSum ≤ originalDeficit) : objective ≤ areaHalf := by omega

end SubQuorum.EvenBridgeSupportCompletion

#print axioms SubQuorum.EvenBridgeSupportCompletion.endpoint_internal_neighbor
#print axioms SubQuorum.EvenBridgeSupportCompletion.selected_tile_anchoring
#print axioms SubQuorum.EvenBridgeSupportCompletion.endpoint_tile_connectivity
#print axioms SubQuorum.EvenBridgeSupportCompletion.adjacent_occupied_supports_are_endpoints
#print axioms SubQuorum.EvenBridgeSupportCompletion.even_bridge_unused
#print axioms SubQuorum.EvenBridgeSupportCompletion.odd_bridge_forced
#print axioms SubQuorum.EvenBridgeSupportCompletion.receiver_additivity
#print axioms SubQuorum.EvenBridgeSupportCompletion.two_endpoint_correction
#print axioms SubQuorum.EvenBridgeSupportCompletion.three_endpoint_correction
#print axioms SubQuorum.EvenBridgeSupportCompletion.buffer_correction
#print axioms SubQuorum.EvenBridgeSupportCompletion.net_interface_additivity
#print axioms SubQuorum.EvenBridgeSupportCompletion.signed_split_invariance
#print axioms SubQuorum.EvenBridgeSupportCompletion.nonpositive_piece_sum
#print axioms SubQuorum.EvenBridgeSupportCompletion.original_deficit_compensation
