import SubQuorum.CollarCompensation

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SubQuorum.MixedPChainCompensation

open SubQuorum.CollarCompensation

def internalOccupied (tile : Fin 81) (corner : Nat) : Nat :=
  ((neighbors corner).filter fun adjacent => label tile adjacent != 0).length

def normalizedGap (tile : Fin 81) : Bool :=
  [1, 2].all fun corner => label tile corner != 2 || 2 ≤ internalOccupied tile corner

theorem blank_exterior_gap : ∀ tile : Fin 81,
    count tile 1 ≤ 1 → label tile 3 = 0 → valid tile 0 = true →
    normalizedGap tile = true → count tile 1 + 1 ≤ count tile 0 := by
  decide

theorem occupied_exterior_gap : ∀ tile : Fin 81,
    count tile 1 ≤ 1 → label tile 0 = 0 → valid tile 9 = true →
    count tile 1 + 1 ≤ count tile 0 := by
  decide

theorem transition_charge (owners changes surplus internal exports incoming : Nat)
    (chargeTwice : Int)
    (hlinks : changes + 1 ≤ owners)
    (hsurplus : 2 * (owners - 1 - changes) ≤ surplus)
    (hendpoints : internal + incoming = owners)
    (hledger : chargeTwice = -(surplus : Int) + internal + exports) :
    chargeTwice ≤ 2 - (owners : Int) + 2 * changes + exports - incoming := by
  omega

end SubQuorum.MixedPChainCompensation
