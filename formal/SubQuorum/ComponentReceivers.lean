import SubQuorum.OwnedDonorCompensation

set_option autoImplicit false

namespace SubQuorum.ComponentReceivers

open OwnedDonorCompensation

theorem diagonal_endpoint_bridge (state : Int → Int → Label)
    (hfirst : state 0 0 = .endpoint) (hopposite : state 1 1 = .endpoint)
    (htopFeasible : feasibleAt state 0 1)
    (hleftFeasible : feasibleAt state 1 0)
    (hfirstTerminal : 3 ≤ degree state 0 0) :
    state 0 1 = .endpoint ∨ state 1 0 = .endpoint := by
  cases htop : state 0 1 <;>
    cases hleft : state 1 0 <;>
    cases hnorth : state (-1) 0 <;>
    cases hwest : state 0 (-1) <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem diagonal_endpoint_owner {Owner : Type} (state : Int → Int → Label)
    (owner : Int → Int → Owner)
    (hfirst : state 0 0 = .endpoint) (hopposite : state 1 1 = .endpoint)
    (htopFeasible : feasibleAt state 0 1)
    (hleftFeasible : feasibleAt state 1 0)
    (hfirstTerminal : 3 ≤ degree state 0 0)
    (hhorizontal : ∀ row column, state row column = .endpoint →
      state row (column+1) = .endpoint → owner row column = owner row (column+1))
    (hvertical : ∀ row column, state row column = .endpoint →
      state (row+1) column = .endpoint → owner row column = owner (row+1) column) :
    owner 0 0 = owner 1 1 := by
  rcases diagonal_endpoint_bridge state hfirst hopposite htopFeasible hleftFeasible
    hfirstTerminal with htop | hleft
  · exact (hhorizontal 0 0 hfirst htop).trans (hvertical 0 1 htop hopposite)
  · exact (hvertical 0 0 hfirst hleft).trans (hhorizontal 1 0 hleft hopposite)

theorem aligned_comb_receiver (size : Nat) (selected endpoints tiles : Nat)
    (chargeTwice : Int) (hselected : selected = size)
    (hendpoints : endpoints = 2*size) (htiles : tiles = size)
    (hledger : chargeTwice = 2*(selected : Int)+endpoints-4*tiles) :
    chargeTwice = 0 := by
  omega

theorem misaligned_comb_receiver (size : Nat) (selected endpoints tiles : Nat)
    (chargeTwice : Int) (hselected : selected = size+2)
    (hendpoints : endpoints = 2*size) (htiles : tiles = size+1)
    (hledger : chargeTwice = 2*(selected : Int)+endpoints-4*tiles) :
    chargeTwice = 0 := by
  omega

end SubQuorum.ComponentReceivers
