import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 500000000

namespace SubQuorum.SingletonNegativeDefects

structure Profile where
  negative : Bool
  endpoints : List Nat
  selected : List Nat
  deriving Inhabited

def corners : List Nat := [0,1,2,3]

def adjacent (first second : Nat) : Bool := first != second && first+second != 3

def catalogue : List Profile := [
  ⟨false,[0],[1,2]⟩,
  ⟨true,[0],[1]⟩,
  ⟨true,[0],[2]⟩,
  ⟨false,[1],[0,3]⟩,
  ⟨true,[1],[0]⟩,
  ⟨true,[1],[3]⟩,
  ⟨false,[2],[0,3]⟩,
  ⟨true,[2],[0]⟩,
  ⟨true,[2],[3]⟩,
  ⟨false,[3],[1,2]⟩,
  ⟨true,[3],[1]⟩,
  ⟨true,[3],[2]⟩,
  ⟨true,[0,1],[]⟩,
  ⟨false,[0,1],[2]⟩,
  ⟨true,[0,1],[2]⟩,
  ⟨false,[0,1],[3]⟩,
  ⟨true,[0,1],[3]⟩,
  ⟨true,[0,2],[]⟩,
  ⟨false,[0,2],[1]⟩,
  ⟨true,[0,2],[1]⟩,
  ⟨false,[0,2],[3]⟩,
  ⟨true,[0,2],[3]⟩,
  ⟨true,[1,3],[]⟩,
  ⟨false,[1,3],[0]⟩,
  ⟨true,[1,3],[0]⟩,
  ⟨false,[1,3],[2]⟩,
  ⟨true,[1,3],[2]⟩,
  ⟨true,[2,3],[]⟩,
  ⟨false,[2,3],[0]⟩,
  ⟨true,[2,3],[0]⟩,
  ⟨false,[2,3],[1]⟩,
  ⟨true,[2,3],[1]⟩,
  ⟨false,[0,1,2],[]⟩,
  ⟨true,[0,1,2],[]⟩,
  ⟨false,[0,1,3],[]⟩,
  ⟨true,[0,1,3],[]⟩,
  ⟨false,[0,2,3],[]⟩,
  ⟨true,[0,2,3],[]⟩,
  ⟨false,[1,2,3],[]⟩,
  ⟨true,[1,2,3],[]⟩,
  ⟨false,[0,1,2,3],[]⟩,
  ⟨true,[0,1,2,3],[]⟩
]

def packings : Nat → List Nat → List (List Profile)
  | 0, _ => [[]]
  | _+1, [] => [[]]
  | fuel+1, first::remaining =>
    packings fuel remaining ++
      ((catalogue.filter fun profile => profile.endpoints.contains first &&
        profile.endpoints.all (first::remaining).contains).flatMap fun profile =>
          (packings fuel ((first::remaining).filter fun corner =>
            !profile.endpoints.contains corner)).map fun tail => profile::tail)

def allPackings : List (List Profile) := packings 4 corners

def endpoints (profiles : List Profile) : List Nat := profiles.flatMap Profile.endpoints

def retained (profiles : List Profile) : List Nat :=
  (profiles.flatMap Profile.selected).eraseDups.filter fun corner =>
    !(endpoints profiles).contains corner

def feasible (profiles : List Profile) : Bool :=
  decide (endpoints profiles).Nodup &&
    (retained profiles).all (fun corner =>
      decide ((corners.filter fun other => adjacent corner other &&
        (endpoints profiles ++ retained profiles).contains other).length ≤ 1))

def irregularProfile (profile : Profile) : Bool :=
  (profile.endpoints.length == 1 && profile.selected.length == 1) ||
    (profile.endpoints.length == 2 && profile.selected.isEmpty)

def singletonProfile (profile : Profile) : Bool :=
  profile.negative && profile.endpoints.length == 1 && profile.selected.length == 1

def barProfile (profile : Profile) : Bool :=
  profile.negative && profile.endpoints.length == 2 && profile.selected.isEmpty

def events (profile : Profile) (profiles : List Profile) : Nat :=
  (profile.endpoints.map fun corner =>
    (corners.filter fun other => adjacent corner other &&
      (endpoints profiles).contains other &&
      !(profile.endpoints ++ profile.selected).contains other).length).sum

structure LocalCharge where
  negativeOwners : Nat
  singletons : Nat
  irregular : Int
  marked : Int
  credit : Int
  bar : Int
  overlap : Int
  quadruple : Int
  zeroCorner : Int
  slots : Int
  exceptionalThree : Int

def charge (profiles : List Profile) : LocalCharge :=
  let negativeOwners := (profiles.filter Profile.negative).length
  let singletons := (profiles.filter singletonProfile).length
  let irregular := (profiles.filter irregularProfile).map fun profile => events profile profiles
  let regular := (profiles.filter fun profile => !irregularProfile profile).map fun profile =>
    events profile profiles
  let newFull := (endpoints profiles).length == 4 && decide (1 < profiles.length)
  let marked := profiles.any fun profile => barProfile profile &&
    profile.endpoints.any fun corner => corners.any fun other =>
      adjacent corner other && !(endpoints profiles).contains other
  let zeroCorner := negativeOwners == 1 && singletons == 1 &&
    profiles.any (fun profile => !profile.negative && profile.endpoints.length == 3)
  {
    negativeOwners := negativeOwners
    singletons := singletons
    irregular := Int.ofNat irregular.sum
    marked := if marked then 1 else 0
    credit := (if newFull then 2 else 0)-Int.ofNat regular.sum
    bar := Int.ofNat (profiles.filter barProfile).length
    overlap := if decide (2 ≤ negativeOwners) && decide (0 < singletons) then 1 else 0
    quadruple := if singletons == 4 then 1 else 0
    zeroCorner := if zeroCorner then 1 else 0
    slots := Int.ofNat ((profiles.filter irregularProfile).map fun profile => profile.endpoints.length).sum
    exceptionalThree := if (endpoints profiles).length == 4 && singletons == 1 &&
      profiles.any (fun profile => profile.endpoints.length == 3) then 1 else 0
  }

def localCheck (profiles : List Profile) : Bool :=
  if feasible profiles then
    let current := charge profiles
    decide (0 ≤ current.credit) &&
      decide (current.irregular+current.marked ≤ current.credit+current.bar+
        current.overlap+current.quadruple+current.zeroCorner)
  else true

def noSingletonCheck (profiles : List Profile) : Bool :=
  let current := charge profiles
  if feasible profiles && current.singletons == 0 then
    decide (current.irregular+current.marked ≤ current.credit+current.bar)
  else true

def halfSlotCheck (profiles : List Profile) : Bool :=
  let current := charge profiles
  if feasible profiles then
    decide (2*(current.irregular-current.credit) ≤ current.slots+current.exceptionalThree)
  else true

theorem catalogue_size : catalogue.length = 42 := by decide

theorem all_packing_count : allPackings.length = 660 := by decide

theorem feasible_packing_count : (allPackings.filter feasible).length = 434 := by decide

theorem all_local_defect_payments : allPackings.all localCheck = true := by decide

theorem no_singleton_packing_count :
    (allPackings.filter fun profiles => feasible profiles && (charge profiles).singletons == 0).length = 114 := by decide

theorem no_singleton_local_payment : allPackings.all noSingletonCheck = true := by decide

theorem actual_half_slot_payment : allPackings.all halfSlotCheck = true := by decide

abbrev Point := Int × Int

def rotorEndpoints : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorSelected : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def tile (point : Point) : Point := (point.1/2,point.2/2)

def rotorProfiles (phase : Point) : List (Nat × Nat) :=
  let sourceP := rotorEndpoints.map fun point => (point.1+phase.1,point.2+phase.2)
  let sourceT := rotorSelected.map fun point => (point.1+phase.1,point.2+phase.2)
  let receiver := (sourceP.map tile).eraseDups
  receiver.map fun square =>
    ((sourceP.filter fun point => tile point == square).length,
     (sourceT.filter fun point => tile point == square).length)

theorem negative_rotor_phase00_catalogue :
    (rotorProfiles (0,0)).length = 5 ∧
      (rotorProfiles (0,0)).count (4,0) = 1 ∧
      (rotorProfiles (0,0)).count (1,1) = 4 := by decide

theorem zero_rotor_phase01_catalogue :
    (rotorProfiles (0,1)).length = 4 ∧
      (rotorProfiles (0,1)).count (1,2) = 2 ∧
      (rotorProfiles (0,1)).count (3,0) = 2 := by decide

theorem zero_rotor_phase10_catalogue :
    (rotorProfiles (1,0)).length = 4 ∧
      (rotorProfiles (1,0)).count (1,2) = 2 ∧
      (rotorProfiles (1,0)).count (3,0) = 2 := by decide

theorem zero_rotor_phase11_catalogue :
    (rotorProfiles (1,1)).length = 4 ∧
      (rotorProfiles (1,1)).count (2,1) = 4 := by decide

theorem refined_global_bound
    (slack positive mass credit irregular corner exceptional bar negativeU negativeRotors overlap quadruple zeroCorner : Int)
    (hledger : positive+mass+credit-irregular-(corner+exceptional) ≤ slack)
    (hlocal : irregular+corner ≤ credit+bar+overlap+quadruple+zeroCorner)
    (hmass : mass = bar+negativeU+2*negativeRotors)
    (hpositive : exceptional ≤ 2*positive) (hnegative : exceptional ≤ 2*negativeU) :
    max (positive-negativeU) (negativeU-positive)+2*negativeRotors-overlap-quadruple-zeroCorner ≤ slack := by
  simp only [Int.max_def]
  split <;> omega

theorem no_singleton_source_bound
    (slack positive mass credit irregular corner exceptional bar negativeU : Int)
    (hledger : positive+mass+credit-irregular-(corner+exceptional) ≤ slack)
    (hlocal : irregular+corner ≤ credit+bar)
    (hmass : mass = bar+negativeU)
    (hpositive : exceptional ≤ 2*positive) (hnegative : exceptional ≤ 2*negativeU) :
    max (positive-negativeU) (negativeU-positive) ≤ slack := by
  simp only [Int.max_def]
  split <;> omega

theorem no_singleton_coefficient_one (halfArea objective positive negativeU : Int)
    (hslack : max (positive-negativeU) (negativeU-positive) ≤ halfArea-objective) :
    objective ≤ halfArea := by
  simp only [Int.max_def] at hslack
  split at hslack <;> omega

theorem half_slot_sum (irregular credit mass diagonal exceptional : Int)
    (hlocal : 2*(irregular-credit) ≤ 2*mass-2*diagonal+exceptional) :
    irregular ≤ mass-diagonal+credit+exceptional/2 := by omega

theorem zero_rotor_exception_budget
    (irregular credit mass diagonal exceptionalU exceptionalR : Int)
    (hlocal : 2*(irregular-credit) ≤ 2*mass-2*diagonal+exceptionalU+exceptionalR)
    (hsource : exceptionalU ≤ 2*diagonal) :
    irregular ≤ mass+credit+exceptionalR/2 := by omega

theorem half_slot_global_slack
    (slack positive mass credit irregular marked exceptionalR : Int)
    (hledger : positive+mass+credit-irregular-marked ≤ slack)
    (hbudget : irregular ≤ mass+credit+exceptionalR/2) :
    positive-marked-exceptionalR/2 ≤ slack := by omega

end SubQuorum.SingletonNegativeDefects
