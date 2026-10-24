import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 500000000

namespace SubQuorum.SeparatedNegativeCompensation

structure Profile where
  endpoints : List Nat
  selected : List Nat
  deriving Inhabited

def corners : List Nat := [0,1,2,3]

def adjacent (first second : Nat) : Bool := first != second && first+second != 3

def good : List Profile := [
  ⟨[],[]⟩,
  ⟨[0],[1,2]⟩, ⟨[1],[0,3]⟩, ⟨[2],[0,3]⟩, ⟨[3],[1,2]⟩,
  ⟨[0,1],[2]⟩, ⟨[0,1],[3]⟩, ⟨[0,2],[1]⟩, ⟨[0,2],[3]⟩,
  ⟨[1,3],[0]⟩, ⟨[1,3],[2]⟩, ⟨[2,3],[0]⟩, ⟨[2,3],[1]⟩
]

def finalEndpoints (profiles : List Profile) : List Nat := profiles.flatMap Profile.endpoints

def retained (profiles : List Profile) : List Nat :=
  ((profiles.flatMap Profile.selected).eraseDups).filter fun corner =>
    !(finalEndpoints profiles).contains corner

def feasible (profiles : List Profile) : Bool :=
  decide (finalEndpoints profiles).Nodup &&
    (retained profiles).all (fun corner =>
      decide (((corners.filter fun other => adjacent corner other &&
        (finalEndpoints profiles ++ retained profiles).contains other).length) ≤ 1))

def events (profile : Profile) (profiles : List Profile) : Nat :=
  (profile.endpoints.map fun corner =>
    (corners.filter fun other => adjacent corner other &&
      (finalEndpoints profiles).contains other &&
      !(profile.endpoints ++ profile.selected).contains other).length).sum

def localCheck (negative : Profile) (reservation : Int) (foreign : List Profile) : Bool :=
  let profiles := negative :: foreign
  if feasible profiles then
    let irregular := events negative profiles
    let regular := (foreign.map fun profile => events profile profiles).sum
    let full := (finalEndpoints profiles).length == 4
    let credit : Int := (if full then 2 else 0)-Int.ofNat regular
    decide (0 ≤ credit) &&
      (irregular == 0 || (full && decide (regular ≤ 1))) &&
      decide (Int.ofNat irregular ≤ credit+reservation)
  else true

theorem singleton_tile_completion_and_payment :
    good.all (fun first => good.all (fun second => good.all (fun third =>
      localCheck ⟨[0],[1]⟩ 0 [first,second,third]))) = true := by decide

theorem double_tile_completion_and_payment :
    good.all (fun first => good.all (fun second => good.all (fun third =>
      localCheck ⟨[0,1],[]⟩ 1 [first,second,third]))) = true := by decide

theorem excluded_three_endpoint_role :
    let profiles : List Profile := [⟨[0],[1]⟩, ⟨[1,2,3],[]⟩]
    feasible profiles = true ∧
      events profiles[0]! profiles = 1 ∧ events profiles[1]! profiles = 2 := by decide

structure TileCharge where
  irregular : Int
  corner : Int
  credit : Int
  reservation : Int

theorem sum_tile_payments (tiles : List TileCharge)
    (hlocal : ∀ tile ∈ tiles, tile.irregular+tile.corner ≤ tile.credit+tile.reservation) :
    (tiles.map TileCharge.irregular).sum+(tiles.map TileCharge.corner).sum ≤
      (tiles.map TileCharge.credit).sum+(tiles.map TileCharge.reservation).sum := by
  induction tiles with
  | nil => simp
  | cons head tail inductionHypothesis =>
    have headPayment := hlocal head (by simp)
    have tailPayment := inductionHypothesis (by
      intro tile membership
      exact hlocal tile (by simp [membership]))
    simp only [List.map_cons, List.sum_cons]
    omega

theorem blank_bar_reservation (irregular corner credit : Int)
    (hirregular : irregular = 0) (hcorner : corner ≤ 1) (hcredit : 0 ≤ credit) :
    irregular+corner ≤ credit+1 := by omega

theorem source_mass_identity (minusOne rowShifted barReservations negativeRotors mass : Int)
    (hsource : mass = minusOne+barReservations+rowShifted+2*negativeRotors) :
    mass = barReservations+(minusOne+rowShifted)+2*negativeRotors := by omega

theorem actual_demand_bound
    (slack positive mass credit irregular corner exceptional barReservations negativeU negativeRotors : Int)
    (hledger : positive+mass+credit-irregular-(corner+exceptional) ≤ slack)
    (hlocal : irregular+corner ≤ credit+barReservations)
    (hmass : mass = barReservations+negativeU+2*negativeRotors) :
    positive+negativeU+2*negativeRotors-exceptional ≤ slack := by omega

theorem imbalance_bound (slack positive negativeU negativeRotors exceptional : Int)
    (hslack : positive+negativeU+2*negativeRotors-exceptional ≤ slack)
    (hpositive : exceptional ≤ 2*positive) (hnegative : exceptional ≤ 2*negativeU) :
    max (positive-negativeU) (negativeU-positive)+2*negativeRotors ≤ slack := by
  simp only [Int.max_def]
  split <;> omega

theorem coefficient_one (halfArea objective positive negativeU negativeRotors : Int)
    (hslack : max (positive-negativeU) (negativeU-positive)+2*negativeRotors ≤ halfArea-objective)
    (hrotors : 0 ≤ negativeRotors) : objective ≤ halfArea := by
  simp only [Int.max_def] at hslack
  split at hslack <;> omega

theorem single_negative_u (halfArea objective positive : Int)
    (hslack : max (positive-1) (1-positive) ≤ halfArea-objective) :
    objective ≤ halfArea := by
  simp only [Int.max_def] at hslack
  split at hslack <;> omega

theorem double_owner_reservation (irregular corner : Int)
    (hcorner : 0 ≤ corner) (honeCorner : corner ≤ 1) (htwo : irregular ≤ 2)
    (hmarked : 0 < corner → irregular ≤ 1) : irregular+corner-1 ≤ 1 := by
  by_cases marked : 0 < corner
  · have := hmarked marked
    omega
  · omega

theorem overlap_excess_bound (owners : Int) (hshared : 2 ≤ owners) :
    owners ≤ 2*(owners-1) := by omega

theorem general_defect_bound
    (slack positive mass credit irregular corner exceptional barReservations negativeU negativeRotors overlap zeroCorner : Int)
    (hledger : positive+mass+credit-irregular-(corner+exceptional) ≤ slack)
    (hlocal : irregular+corner ≤ credit+barReservations+overlap+zeroCorner)
    (hmass : mass = barReservations+negativeU+2*negativeRotors)
    (hpositive : exceptional ≤ 2*positive) (hnegative : exceptional ≤ 2*negativeU) :
    max (positive-negativeU) (negativeU-positive)+2*negativeRotors-overlap-zeroCorner ≤ slack := by
  simp only [Int.max_def]
  split <;> omega

theorem defect_coverage_sufficient
    (halfArea objective positive negativeU negativeRotors overlap zeroCorner : Int)
    (hslack : max (positive-negativeU) (negativeU-positive)+2*negativeRotors-overlap-zeroCorner ≤ halfArea-objective)
    (hcoverage : overlap+zeroCorner ≤ max (positive-negativeU) (negativeU-positive)+2*negativeRotors) :
    objective ≤ halfArea := by omega

end SubQuorum.SeparatedNegativeCompensation
