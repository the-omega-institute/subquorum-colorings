import SubQuorum.ThinComponents

set_option autoImplicit false

namespace SubQuorum.BentReceiverCompensation

open OwnedDonorCompensation

theorem canonical_tile_sparse (state : Int → Int → Label)
    (hcoreLeft : state 1 1 = .endpoint) (hcoreRight : state 1 2 = .endpoint)
    (htail : state 2 0 = .endpoint) (haxial : state 3 0 = .selected)
    (hnearNotEndpoint : state 2 1 ≠ .endpoint)
    (hfarNotEndpoint : state 2 2 ≠ .endpoint)
    (hnearFeasible : feasibleAt state 2 1)
    (haxialFeasible : feasibleAt state 3 0)
    (hfarFeasible : feasibleAt state 2 2) :
    occupied (state 2 1)+occupied (state 2 2)+
      occupied (state 3 1)+occupied (state 3 2) ≤ 1 := by
  have hnear : state 2 1 = .blank := by
    cases hlabel : state 2 1 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  have hbelow : state 3 1 = .blank := by
    cases hlabel : state 3 1 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  cases hupper : state 2 2 <;> cases hlower : state 3 2 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem sparse_tile_compensation (selected endpoints saturated : Nat)
    (donorChargeTwice sourceChargeTwice : Int)
    (hoccupancy : selected+endpoints ≤ 1) (hsaturated : saturated ≤ endpoints)
    (hledger : donorChargeTwice = 2*(selected : Int)+endpoints+saturated-4)
    (hsource : sourceChargeTwice = 2) :
    donorChargeTwice ≤ -2 ∧ sourceChargeTwice+donorChargeTwice ≤ 0 := by
  omega

theorem canonical_far_not_endpoint (state : Int → Int → Label)
    (hcore : state 1 2 = .endpoint) (htail : state 2 0 = .endpoint)
    (haxial : state 3 0 = .selected)
    (hupperNotEndpoint : state 2 2 ≠ .endpoint)
    (haxialFeasible : feasibleAt state 3 0)
    (hupperFeasible : feasibleAt state 2 2)
    (hfarTerminal : 3 ≤ degree state 3 2) : state 3 2 ≠ .endpoint := by
  intro hfar
  have hupper : state 2 2 = .blank := by
    cases hlabel : state 2 2 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  have hleft : state 3 1 = .blank := by
    cases hlabel : state 3 1 <;>
      simp_all [feasibleAt, degree, occupied] <;> omega
  cases hbelow : state 4 2 <;> cases hright : state 3 3 <;>
    simp_all [degree, occupied] <;> omega

def footprint : List (Int × Int) :=
  [(-2,-1), (-2,0), (-2,1), (-2,2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-1)]

def orientation (mirror : Bool) (turns : Fin 4) (point : Int × Int) : Int × Int :=
  let reflected := if mirror then (point.1, 1-point.2) else point
  match turns.val with
  | 0 => reflected
  | 1 => (reflected.2, 1-reflected.1)
  | 2 => (1-reflected.1, 1-reflected.2)
  | _ => (1-reflected.2, reflected.1)

theorem shared_donor_orientation (mirror : Bool) (turns : Fin 4) :
    footprint.any (fun point => (footprint.map (orientation mirror turns)).contains point) = true ∨
      turns.val = 2 := by
  rcases turns with ⟨turns, hbound⟩
  have hcases : turns = 0 ∨ turns = 1 ∨ turns = 2 ∨ turns = 3 := by omega
  rcases hcases with hzero | hone | htwo | hthree <;>
    subst turns <;> cases mirror <;> decide +revert

end SubQuorum.BentReceiverCompensation
