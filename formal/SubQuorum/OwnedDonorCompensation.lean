import SubQuorum.FrozenPromotion

set_option autoImplicit false

namespace SubQuorum.OwnedDonorCompensation

inductive Label where
  | blank | selected | endpoint
  deriving DecidableEq

def occupied : Label → Nat
  | .blank => 0
  | _ => 1

def degree (state : Int → Int → Label) (row column : Int) : Nat :=
  occupied (state (row-1) column) + occupied (state (row+1) column) +
  occupied (state row (column-1)) + occupied (state row (column+1))

def feasibleAt (state : Int → Int → Label) (row column : Int) : Prop :=
  state row column = .selected → degree state row column ≤ 1

theorem face_pair_exclusion (first second : Label)
    (hfirst : first = .selected → 1+occupied second ≤ 1)
    (hsecond : second = .selected → 1+occupied first ≤ 1)
    (hsquare : ¬(first = .endpoint ∧ second = .endpoint)) :
    occupied first+occupied second ≤ 1 := by
  cases first <;> cases second <;> simp_all [occupied]

theorem pinwheel_incidence (northLeft northRight eastTop eastBottom
    southLeft southRight westTop westBottom : Nat)
    (hnorth : northLeft+northRight ≤ 1)
    (heast : eastTop+eastBottom ≤ 1)
    (hsouth : southLeft+southRight ≤ 1)
    (hwest : westTop+westBottom ≤ 1)
    (htopLeft : 1 ≤ northLeft+westTop)
    (htopRight : 1 ≤ northRight+eastTop)
    (hbottomRight : 1 ≤ eastBottom+southRight)
    (hbottomLeft : 1 ≤ southLeft+westBottom) :
    (northLeft = 1 ∧ northRight = 0 ∧ eastTop = 1 ∧ eastBottom = 0 ∧
     southLeft = 0 ∧ southRight = 1 ∧ westTop = 0 ∧ westBottom = 1) ∨
    (northLeft = 0 ∧ northRight = 1 ∧ eastTop = 0 ∧ eastBottom = 1 ∧
     southLeft = 1 ∧ southRight = 0 ∧ westTop = 1 ∧ westBottom = 0) := by
  omega

theorem central_matching_patterns (top right bottom left : Nat)
    (htopLeft : top+left ≤ 1) (htopRight : top+right ≤ 1)
    (hbottomRight : bottom+right ≤ 1) (hbottomLeft : bottom+left ≤ 1) :
    (top = 0 ∧ right = 0 ∧ bottom = 0 ∧ left = 0) ∨
    (top = 1 ∧ right = 0 ∧ bottom = 0 ∧ left = 0) ∨
    (top = 0 ∧ right = 1 ∧ bottom = 0 ∧ left = 0) ∨
    (top = 0 ∧ right = 0 ∧ bottom = 1 ∧ left = 0) ∨
    (top = 0 ∧ right = 0 ∧ bottom = 0 ∧ left = 1) ∨
    (top = 1 ∧ right = 0 ∧ bottom = 1 ∧ left = 0) ∨
    (top = 0 ∧ right = 1 ∧ bottom = 0 ∧ left = 1) := by
  omega

theorem central_parity_ledger (outward internal capacity degree : Nat)
    (hmatching : outward+2*internal = 4)
    (hcapacity : capacity+internal = 2) (hdegree : degree = outward) :
    (outward = 0 ∨ outward = 2 ∨ outward = 4) ∧
    (degree : Int)-2*capacity = 0 := by
  omega

theorem turn_forces_square (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint) (hwest : state 0 (-1) = .endpoint)
    (hsouth : state 1 0 = .endpoint) (hnorth : state (-1) 0 = .selected)
    (hnorthFeasible : feasibleAt state (-1) 0)
    (hsouthwestFeasible : feasibleAt state 1 (-1))
    (hwestTerminal : 3 ≤ degree state 0 (-1)) :
    state 1 (-1) = .endpoint := by
  cases hnorthwest : state (-1) (-1) <;>
    cases hsouthwest : state 1 (-1) <;>
    cases houter : state 0 (-2) <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem branch_forces_square (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint) (hwest : state 0 (-1) = .endpoint)
    (hsouth : state 1 0 = .endpoint) (heast : state 0 1 = .endpoint)
    (hsouthwestFeasible : feasibleAt state 1 (-1))
    (hsoutheastFeasible : feasibleAt state 1 1)
    (hsouthTerminal : 3 ≤ degree state 1 0) :
    state 1 (-1) = .endpoint ∨ state 1 1 = .endpoint := by
  cases hsouthwest : state 1 (-1) <;>
    cases hsoutheast : state 1 1 <;>
    cases houter : state 2 0 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem two_side_supports_impossible (state : Int → Int → Label)
    (hcenter : state 0 0 = .endpoint)
    (hnorth : state (-1) 0 = .selected) (hsouth : state 1 0 = .selected)
    (hnorthFeasible : feasibleAt state (-1) 0)
    (hsouthFeasible : feasibleAt state 1 0)
    (heastTerminal : 3 ≤ degree state 0 1) : False := by
  cases hnortheast : state (-1) 1 <;>
    cases hsoutheast : state 1 1 <;>
    cases houter : state 0 2 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem frozen_chain {Vertex : Type} (adjacent : Vertex → Vertex → Prop)
    (selected : Vertex → Prop) (mate : Vertex → Vertex)
    (path support : Nat → Vertex) (length : Nat)
    (hbase : FrozenPromotion.Frozen adjacent selected mate (path 0))
    (hsupport : ∀ index, index < length → selected (support index))
    (hselectedAdjacent : ∀ index, index < length →
      adjacent (path (2*(index+1))) (support index))
    (hpreviousAdjacent : ∀ index, index < length →
      adjacent (path (2*(index+1))) (path (2*index+1)))
    (hdistinct : ∀ index, index < length → support index ≠ path (2*index+1))
    (hmate : ∀ index, index < length → mate (path (2*index+1)) = path (2*index)) :
    ∀ index, index ≤ length → FrozenPromotion.Frozen adjacent selected mate (path (2*index)) := by
  intro index
  induction index with
  | zero =>
      intro hbound
      simpa using hbase
  | succ index inductionHypothesis =>
      intro hbound
      have hstep : index < length := by omega
      apply FrozenPromotion.Frozen.selected_frozen _ (support index) (path (2*index+1))
        (hselectedAdjacent index hstep) (hpreviousAdjacent index hstep)
        (hdistinct index hstep) (hsupport index hstep)
      rw [hmate index hstep]
      exact inductionHypothesis (by omega)

theorem single_endpoint_donor_unique {Vertex Owner : Type}
    (endpoint : Vertex → Prop) (inDonor : Vertex → Prop)
    (belongs : Owner → Vertex → Prop) (mate : Vertex → Vertex)
    (hunique : ∀ first second, inDonor first → endpoint first →
      inDonor second → endpoint second → first = second)
    (hdisjoint : ∀ first second vertex, belongs first vertex → belongs second vertex →
      first = second)
    (firstOwner secondOwner : Owner) (firstEndpoint secondEndpoint : Vertex)
    (hfirstDonor : inDonor firstEndpoint) (hfirstEndpoint : endpoint firstEndpoint)
    (hsecondDonor : inDonor secondEndpoint) (hsecondEndpoint : endpoint secondEndpoint)
    (hfirstClaim : belongs firstOwner (mate firstEndpoint))
    (hsecondClaim : belongs secondOwner (mate secondEndpoint)) : firstOwner = secondOwner := by
  have hsame := hunique firstEndpoint secondEndpoint hfirstDonor hfirstEndpoint
    hsecondDonor hsecondEndpoint
  rw [← hsame] at hsecondClaim
  exact hdisjoint firstOwner secondOwner (mate firstEndpoint) hfirstClaim hsecondClaim

theorem owned_donor_budget (selected endpoints saturated claims : Nat) (chargeTwice : Int)
    (hoccupancy : selected+endpoints ≤ 2)
    (hclaims : saturated+claims ≤ endpoints)
    (hledger : chargeTwice = 2*(selected : Int)+endpoints+saturated-4) :
    chargeTwice+claims = -2*(2-(selected : Int)-endpoints)-
      ((endpoints : Int)-saturated-claims) ∧ chargeTwice+claims ≤ 0 := by
  omega

theorem owned_aggregate (source donor : Int) (claims : Nat)
    (hsource : source ≤ claims) (hdonor : donor+claims ≤ 0) : source+donor ≤ 0 := by
  omega

end SubQuorum.OwnedDonorCompensation
