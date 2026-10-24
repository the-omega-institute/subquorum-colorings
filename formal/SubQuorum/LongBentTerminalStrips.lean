import SubQuorum.BentReceiverCompensation

set_option autoImplicit false

namespace SubQuorum.LongBentTerminalStrips

open OwnedDonorCompensation

def selectedCount : Label → Nat
  | .selected => 1
  | _ => 0

theorem selected_square_capacity (state : Int → Int → Label)
    (hupperLeft : feasibleAt state 0 0) (hupperRight : feasibleAt state 0 1)
    (hlowerLeft : feasibleAt state 1 0) (hlowerRight : feasibleAt state 1 1) :
    selectedCount (state 0 0)+selectedCount (state 0 1)+
      selectedCount (state 1 0)+selectedCount (state 1 1) ≤ 2 := by
  cases hfirst : state 0 0 <;> cases hsecond : state 0 1 <;>
    cases hthird : state 1 0 <;> cases hfourth : state 1 1 <;>
    simp_all [selectedCount, feasibleAt, degree, occupied] <;> omega

theorem terminal_supports_force_boundary (state : Int → Int → Label)
    (hprevious : state (-1) 0 = .endpoint)
    (hinside : state (-1) 1 = .selected)
    (htip : state 0 0 = .endpoint) (haxial : state 1 0 = .selected)
    (hinsideFeasible : feasibleAt state (-1) 1)
    (haxialFeasible : feasibleAt state 1 0) :
    state 0 1 = .blank ∧ state 1 1 = .blank := by
  constructor
  · cases hlabel : state 0 1 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  · cases hlabel : state 1 1 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega

theorem shifted_strip_budget (squares : List Nat) (selected : Nat) (charge : Int)
    (hlocal : ∀ count ∈ squares, count ≤ 2)
    (hselected : selected = squares.sum)
    (hledger : charge = (selected : Int)-2*(squares.length+1)) :
    charge ≤ -2 := by
  have hsum : ∀ counts : List Nat, (∀ count ∈ counts, count ≤ 2) →
      counts.sum ≤ 2*counts.length := by
    intro counts hbounded
    induction counts with
    | nil => simp
    | cons count rest inductionHypothesis =>
        have hcount := hbounded count (by simp)
        have hrest := inductionHypothesis (by
          intro following hfollowing
          exact hbounded following (by simp [hfollowing]))
        simp only [List.sum_cons, List.length_cons]
        omega
  have hbound := hsum squares hlocal
  omega

theorem parallel_interval_overlap (firstLeft firstRight secondLeft secondRight : Int)
    (_hfirst : firstLeft ≤ firstRight) (hsecond : secondLeft ≤ secondRight)
    (hoverlap : firstLeft ≤ secondRight ∧ secondLeft ≤ firstRight) :
    (firstLeft = secondLeft ∧ firstRight = secondRight) ∨
    (firstLeft ≤ secondLeft-1 ∧ secondLeft-1 ≤ firstRight) ∨
    (firstLeft ≤ secondRight+1 ∧ secondRight+1 ≤ firstRight) ∨
    (secondLeft ≤ firstLeft-1 ∧ firstLeft-1 ≤ secondRight) ∨
    (secondLeft ≤ firstRight+1 ∧ firstRight+1 ≤ secondRight) := by
  omega

theorem paid_strip_sum (charges : List Int)
    (hlocal : ∀ charge ∈ charges, charge ≤ -2) :
    charges.sum+(charges.length : Int) ≤ -(charges.length : Int) := by
  induction charges with
  | nil => simp
  | cons charge rest inductionHypothesis =>
      have hcharge := hlocal charge (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hlocal following (by simp [hfollowing]))
      simp only [List.sum_cons, List.length_cons]
      omega

end SubQuorum.LongBentTerminalStrips
