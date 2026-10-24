import SubQuorum.AttachmentCollarCompensation

set_option autoImplicit false
set_option maxHeartbeats 0

namespace SubQuorum.BlankWitnessCompensation

open SubQuorum.CollarCompensation

theorem corner_two_exterior_faces : ∀ corner : Fin 4,
    ([0, 1, 2, 3].filter fun side => (face side).contains corner.val).length = 2 := by
  decide

theorem shared_blank_ledger
    (owners shared privateBlanks unused components cycleRank free surplus marked exports : Nat)
    (chargeTwice : Int)
    (hcomponents : shared+components = owners+cycleRank)
    (hfree : free = shared+privateBlanks+unused)
    (hsurplus : surplus = 2*marked+free)
    (hledger : chargeTwice = (owners : Int)+exports-surplus) :
    chargeTwice+2*marked = (exports : Int)+components-cycleRank-privateBlanks-unused := by
  omega

theorem shared_blank_source_compensation
    (receiver source : Int) (marked exports components cycleRank privateBlanks unused : Nat)
    (hreceiver : receiver+2*marked = (exports : Int)+components-cycleRank-privateBlanks-unused)
    (hsource : source ≤ 2*marked)
    (hbudget : components+exports ≤ cycleRank+privateBlanks+unused) :
    receiver+source ≤ 0 := by
  omega

theorem two_witness_payment
    (owners incidences free surplus marked exports : Nat) (chargeTwice : Int)
    (hleft : 2*owners ≤ incidences) (hright : incidences ≤ 2*free)
    (hsurplus : surplus = 2*marked+free)
    (hledger : chargeTwice = (owners : Int)+exports-surplus) :
    chargeTwice+2*marked ≤ exports := by
  omega

theorem paid_attachment_parity
    (tiles selected blanks internal crossing saturatedEndpoints incoming
      surplus marked owners exports : Nat) (chargeTwice : Int)
    (hvertices : 4*tiles = selected+blanks+2*internal+crossing)
    (hcounts : selected+surplus = blanks+saturatedEndpoints)
    (hendpoints : saturatedEndpoints = owners+incoming)
    (hpaid : 2*marked+owners ≤ surplus)
    (hledger : chargeTwice = (owners : Int)+exports-surplus) :
    chargeTwice+2*marked+(crossing+incoming) % 2 ≤ exports := by
  omega

end SubQuorum.BlankWitnessCompensation
