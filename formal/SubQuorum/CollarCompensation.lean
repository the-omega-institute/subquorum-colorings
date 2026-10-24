import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SubQuorum.CollarCompensation

def label (tile : Fin 81) (corner : Nat) : Nat := tile.val / 3^corner % 3

def face (side : Nat) : List Nat :=
  match side with
  | 0 => [0, 1]
  | 1 => [1, 3]
  | 2 => [2, 3]
  | _ => [0, 2]

def neighbors (corner : Nat) : List Nat :=
  match corner with
  | 0 => [1, 2]
  | 1 => [0, 3]
  | 2 => [0, 3]
  | _ => [1, 2]

def count (tile : Fin 81) (kind : Nat) : Nat :=
  ([0, 1, 2, 3].filter fun corner => label tile corner == kind).length

def pressure (mask : Fin 16) (corner : Nat) : Nat :=
  ([0, 1, 2, 3].filter fun side =>
    mask.val / 2^side % 2 == 1 && (face side).contains corner).length

def valid (tile : Fin 81) (mask : Fin 16) : Bool :=
  [0, 1, 2, 3].all fun corner =>
    label tile corner != 1 || pressure mask corner +
      ((neighbors corner).filter fun adjacent => label tile adjacent != 0).length <= 1

def terminal (tile : Fin 81) (side : Fin 4) : Bool :=
  (face side.val).all fun corner => label tile corner == 0

def railMask (side : Fin 4) : Fin 16 :=
  if side.val % 2 = 0 then 10 else 5

theorem pressured_tile : ∀ (tile : Fin 81) (mask : Fin 16),
    mask.val > 0 → valid tile mask = true →
      count tile 1 ≤ count tile 0 ∧ (count tile 1 = 2 → count tile 2 = 0) := by
  decide

theorem terminal_tile : ∀ (tile : Fin 81) (side : Fin 4),
    terminal tile side = true → valid tile (railMask side) = true →
      count tile 1 + 2 ≤ count tile 0 := by
  decide

def surplusSum : List (Int × Bool) → Int
  | [] => 0
  | tile :: rest => tile.1 + surplusSum rest

def terminalCount : List (Int × Bool) → Int
  | [] => 0
  | tile :: rest => (if tile.2 then 1 else 0) + terminalCount rest

theorem disjoint_tile_surplus (tiles : List (Int × Bool))
    (hlocal : ∀ tile ∈ tiles, 0 ≤ tile.1 ∧ (tile.2 = true → 2 ≤ tile.1)) :
    2 * terminalCount tiles ≤ surplusSum tiles := by
  induction tiles with
  | nil => simp [surplusSum, terminalCount]
  | cons tile rest inductionHypothesis =>
      have htile := hlocal tile (by simp)
      have hrest := inductionHypothesis (by
        intro following hfollowing
        exact hlocal following (by simp [hfollowing]))
      cases hmarked : tile.2 <;> simp [surplusSum, terminalCount, hmarked] at * <;> omega

theorem collar_parity_charge (tiles selected blanks internal crossing leaves exports : Nat)
    (chargeTwice : Int)
    (hvertices : 4*tiles = selected+blanks+2*internal+crossing)
    (hsurplus : 2*leaves+selected ≤ blanks)
    (hledger : chargeTwice = (selected : Int)-blanks+exports) :
    chargeTwice + 2*leaves + crossing % 2 ≤ exports := by
  omega

theorem aggregate_source_compensation (receiver source : Int)
    (leaves crossing exports : Nat)
    (hreceiver : receiver + 2*leaves + crossing % 2 ≤ exports)
    (hsource : source ≤ 2*leaves) :
    receiver + source ≤ (exports : Int) - crossing % 2 := by
  omega

theorem compensated_core_nonpositive (receiver source : Int)
    (leaves crossing exports : Nat)
    (hreceiver : receiver + 2*leaves + crossing % 2 ≤ exports)
    (hsource : source ≤ 2*leaves) (hbudget : exports ≤ crossing % 2) :
    receiver + source ≤ 0 := by
  have hcompensation := aggregate_source_compensation receiver source
    leaves crossing exports hreceiver hsource
  omega

end SubQuorum.CollarCompensation
