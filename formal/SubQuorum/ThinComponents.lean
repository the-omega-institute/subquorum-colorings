import SubQuorum.ComponentReceivers

set_option autoImplicit false

namespace SubQuorum.ThinComponents

open OwnedDonorCompensation

theorem occupied_le_one (label : Label) : occupied label ≤ 1 := by
  cases label <;> simp [occupied]

theorem attached_column_extends (state : Int → Int → Label)
    (hleft : state 0 (-1) = .endpoint)
    (htop : state 0 0 = .endpoint) (hbottom : state 1 0 = .endpoint)
    (hgapNotEndpoint : state 1 (-1) ≠ .endpoint)
    (houtsideNotEndpoint : state (-1) (-1) ≠ .endpoint)
    (hgapFeasible : feasibleAt state 1 (-1))
    (houtsideFeasible : feasibleAt state (-1) (-1))
    (hrightTopFeasible : feasibleAt state 0 1)
    (hrightBottomFeasible : feasibleAt state 1 1)
    (hleftTerminal : 3 ≤ degree state 0 (-1))
    (htopTerminal : 3 ≤ degree state 0 0)
    (hbottomTerminal : 3 ≤ degree state 1 0) :
    state 0 1 = .endpoint ∧ state 1 1 = .endpoint := by
  have hgap : state 1 (-1) = .blank := by
    cases hlabel : state 1 (-1) <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  have houtside : state (-1) (-1) = .selected := by
    have hbound := occupied_le_one (state 0 (-2))
    cases hlabel : state (-1) (-1) <;>
      simp_all [degree, occupied] <;> omega
  have hnorth : state (-1) 0 = .blank := by
    cases hlabel : state (-1) 0 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  have hrightTop : 1 ≤ occupied (state 0 1) := by
    cases hlabel : state 0 1 <;>
      simp_all [degree, occupied] <;> omega
  have hrightBottom : 1 ≤ occupied (state 1 1) := by
    cases hsouth : state 2 0 <;> cases hlabel : state 1 1 <;>
      simp_all [degree, occupied] <;> omega
  cases hfirst : state 0 1 <;> cases hsecond : state 1 1 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem single_chamber_exit_count (chambers bridgeExits tailExits : Nat)
    (hpositive : 1 ≤ chambers) (hbridges : bridgeExits+1 = chambers)
    (htails : tailExits ≤ 2)
    (hexits : 2*chambers = bridgeExits+tailExits) :
    chambers = 1 ∧ bridgeExits = 0 ∧ tailExits = 2 := by
  omega

theorem receiver_budget (width optional : Nat) (charge : Int)
    (hoptional : optional+3 ≤ width)
    (hcases : charge = -1 ∨ charge = 2-(width : Int)+optional ∨
      charge = 3-(width : Int)+optional ∨ charge = 1-(width : Int)+optional) :
    charge ≤ 0 ∧ (charge = 0 → charge = 3-(width : Int)+optional ∧ optional+3 = width) := by
  omega

theorem two_step_receiver_invariant (selected endpoints tiles : Nat)
    (chargeBefore chargeAfter : Int)
    (hbefore : chargeBefore = 2*(selected : Int)+endpoints-4*tiles)
    (hafter : chargeAfter = 2*((selected : Int)+1)+(endpoints+2)-4*(tiles+1)) :
    chargeAfter = chargeBefore := by
  omega

end SubQuorum.ThinComponents
