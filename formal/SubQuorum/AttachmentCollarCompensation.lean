import SubQuorum.CollarCompensation

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SubQuorum.AttachmentCollarCompensation

open SubQuorum.CollarCompensation

theorem unpressured_deficient_tile : ∀ tile : Fin 81,
    valid tile 0 = true → count tile 1 ≤ 1 → count tile 1 ≤ count tile 0 := by
  decide

theorem saturated_endpoints : ∀ tile : Fin 81,
    valid tile 0 = true → count tile 1 = 2 →
      count tile 2 ≤ 1 ∧ count tile 0 + count tile 2 = 2 := by
  decide

theorem attachment_corrected_charge
    (tiles selected blanks internal crossing saturatedEndpoints surplus
      leaves internalAttachments exports : Nat) (chargeTwice : Int)
    (hvertices : 4*tiles = selected+blanks+2*internal+crossing)
    (hsurplus_count : selected+surplus = blanks+saturatedEndpoints)
    (hsurplus : 2*leaves ≤ surplus)
    (hledger : chargeTwice = (internalAttachments : Int)+exports-surplus) :
    chargeTwice + 2*leaves + (crossing+saturatedEndpoints) % 2 ≤
      internalAttachments+exports := by
  omega

theorem pressure_free_source_compensation
    (receiver source : Int) (leaves crossing saturatedEndpoints internalAttachments exports : Nat)
    (hreceiver : receiver + 2*leaves + (crossing+saturatedEndpoints) % 2 ≤
      internalAttachments+exports)
    (hsource : source ≤ 2*leaves)
    (hbudget : internalAttachments+exports ≤ (crossing+saturatedEndpoints) % 2) :
    receiver+source ≤ 0 := by
  omega

end SubQuorum.AttachmentCollarCompensation
