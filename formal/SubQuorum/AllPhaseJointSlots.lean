import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SubQuorum.AllPhaseJointSlots

abbrev Point := Int × Int

structure Module where
  selected : List Point
  matching : List (Point × Point)
  deriving Inhabited

def modules : List Module := [
  { selected := [(0,0),(0,7),(2,0),(2,7),(3,2),(3,5),(4,0),(4,7),(5,2),(5,6),(6,0),(7,2),(8,0),(9,1)],
    matching := [((0,1),(0,2)),((0,3),(0,4)),((0,5),(0,6)),((1,2),(1,3)),((1,4),(1,5)),((1,1),(2,1)),((3,1),(4,1)),((5,1),(6,1)),((7,1),(8,1)),((1,6),(2,6)),((3,6),(4,6))] },
  { selected := [(0,1),(0,8),(2,1),(2,8),(3,3),(3,6),(4,1),(4,8),(5,3),(5,7),(6,1),(7,3),(8,1),(9,2)],
    matching := [((0,2),(0,3)),((0,4),(0,5)),((0,6),(0,7)),((1,3),(1,4)),((1,5),(1,6)),((1,2),(2,2)),((3,2),(4,2)),((5,2),(6,2)),((7,2),(8,2)),((1,7),(2,7)),((3,7),(4,7))] },
  { selected := [(1,0),(1,7),(3,0),(3,7),(4,2),(4,5),(5,0),(5,7),(6,2),(6,6),(7,0),(8,2),(9,0),(10,1)],
    matching := [((1,1),(1,2)),((1,3),(1,4)),((1,5),(1,6)),((2,2),(2,3)),((2,4),(2,5)),((2,1),(3,1)),((4,1),(5,1)),((6,1),(7,1)),((8,1),(9,1)),((2,6),(3,6)),((4,6),(5,6))] },
  { selected := [(1,1),(1,8),(3,1),(3,8),(4,3),(4,6),(5,1),(5,8),(6,3),(6,7),(7,1),(8,3),(9,1),(10,2)],
    matching := [((1,2),(1,3)),((1,4),(1,5)),((1,6),(1,7)),((2,3),(2,4)),((2,5),(2,6)),((2,2),(3,2)),((4,2),(5,2)),((6,2),(7,2)),((8,2),(9,2)),((2,7),(3,7)),((4,7),(5,7))] }
]

def endpoints (module : Module) : List Point :=
  module.matching.flatMap fun edge => [edge.1,edge.2]

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),(point.1,point.2-1),(point.1,point.2+1)]

def tile (point : Point) : Point := (point.1/2,point.2/2)

def cells (square : Point) : List Point :=
  [(2*square.1,2*square.2),(2*square.1+1,2*square.2),
   (2*square.1,2*square.2+1),(2*square.1+1,2*square.2+1)]

def degree (sites : List Point) (point : Point) : Nat :=
  ((neighbors point).filter sites.contains).length

def blankNeighbors (module : Module) (point : Point) : List Point :=
  (neighbors point).filter fun other =>
    tile point == tile other && !(endpoints module ++ module.selected).contains other

def noExterior (module : Module) : List Point :=
  (endpoints module).filter fun point =>
    !(neighbors point).any (fun other =>
      tile point != tile other && (endpoints module).contains other)

def failures (module : Module) : List Point :=
  (endpoints module).filter fun point => (blankNeighbors module point).any fun blank =>
    (neighbors point).any fun other =>
      tile point == tile other && other != blank &&
        !(endpoints module).contains (2*point.1-other.1,2*point.2-other.2)

def irregular (module : Module) : List Point :=
  (endpoints module).filter fun point =>
    let square := cells (tile point)
    let profile := ((square.filter (endpoints module).contains).length,
                    (square.filter module.selected.contains).length)
    (profile == (1,1) || profile == (2,0)) && !(blankNeighbors module point).isEmpty

def pool (module : Module) : List Point :=
  (irregular module ++ noExterior module ++ failures module).eraseDups

def charge (module : Module) : Int :=
  let receiver := ((endpoints module).map tile).eraseDups
  Int.ofNat ((module.selected.filter fun point => receiver.contains (tile point)).length)+
    Int.ofNat module.matching.length-2*Int.ofNat receiver.length

def sameSites (first second : List Point) : Bool :=
  first.all second.contains && second.all first.contains

theorem source_charges : modules.map charge = [1,-1,-5,-5] := by decide

theorem source_matching_distinct : modules.all
    (fun module => decide (endpoints module).Nodup) = true := by decide

theorem source_feasibility : modules.all (fun module =>
    let occupied := endpoints module ++ module.selected
    module.selected.all (fun point => degree occupied point == 1) &&
      (endpoints module).all (fun point => degree occupied point == 3)) = true := by decide

theorem exterior_exception_counts : modules.map (fun module => (noExterior module).length) =
    [0,2,2,2] := by decide

theorem exterior_exceptions_positive : noExterior modules[0]! = [] := by decide

theorem exterior_exceptions_minus_one :
    sameSites (noExterior modules[1]!) [(0,2),(0,7)] = true := by decide

theorem exterior_exceptions_phase10 :
    sameSites (noExterior modules[2]!) [(9,1),(5,6)] = true := by decide

theorem exterior_exceptions_phase11 :
    sameSites (noExterior modules[3]!) [(9,2),(5,7)] = true := by decide

theorem continuation_exception_counts : modules.map (fun module => (failures module).length) =
    [0,0,0,4] := by decide

theorem continuation_exceptions_phase11 :
    sameSites (failures modules[3]!) [(1,2),(1,7),(9,2),(5,7)] = true := by decide

theorem irregular_counts : modules.map (fun module => (irregular module).length) =
    [0,2,10,8] := by decide

theorem joint_pool_counts : modules.map (fun module => (pool module).length) =
    [0,4,12,10] := by decide

theorem minus_one_pools_disjoint : (noExterior modules[1]!).all
    (fun point => !(irregular modules[1]!).contains point) = true := by decide

theorem phase10_tips_not_irregular : (noExterior modules[2]!).all
    (fun point => !(irregular modules[2]!).contains point) = true := by decide

theorem phase11_tips_not_irregular : (noExterior modules[3]!).all
    (fun point => !(irregular modules[3]!).contains point) = true := by decide

theorem phase11_overlap_exact :
    sameSites ((failures modules[3]!).filter (irregular modules[3]!).contains)
      [(1,2),(1,7)] = true := by decide

def sharedCorner (index : Fin 2) : Point := if index.val == 0 then (1,2) else (1,7)

def sharedGate (index : Fin 2) : Point := if index.val == 0 then (0,2) else (0,7)

theorem shared_slot_unique_blank : ∀ index : Fin 2,
    blankNeighbors modules[3]! (sharedCorner index) = [sharedGate index] := by decide

theorem blank_gate_excludes_irregular (index : Fin 2) (finalEndpoint : Point → Bool)
    (hblank : finalEndpoint (sharedGate index) = false) :
    (blankNeighbors modules[3]! (sharedCorner index)).any finalEndpoint = false := by
  rw [shared_slot_unique_blank index]
  simpa using hblank

theorem all_boundary_candidates_in_pool : modules.all (fun module =>
    (noExterior module ++ failures module).all (pool module).contains) = true := by decide

theorem joint_capacity (mass minusOne phase10 irregularCost sideCost poolSize : Int)
    (hinjection : irregularCost+sideCost ≤ poolSize)
    (hpool : poolSize = 2*mass+2*minusOne+2*phase10) :
    irregularCost+sideCost ≤ 2*mass+2*minusOne+2*phase10 := by omega

theorem all_phase_slack (slack positive mass credit irregularCost sideCost minusOne phase10 : Int)
    (hledger : positive+mass+credit-irregularCost-sideCost ≤ slack)
    (hjoint : irregularCost+sideCost ≤ 2*mass+2*minusOne+2*phase10) :
    positive-mass-2*minusOne-2*phase10+credit ≤ slack := by omega

theorem residual_sufficient (slack positive mass credit minusOne phase10 : Int)
    (hslack : positive-mass-2*minusOne-2*phase10+credit ≤ slack)
    (hcoverage : mass+2*minusOne+2*phase10 ≤ positive+credit) : 0 ≤ slack := by omega

theorem density_sufficient (slack positive mass credit minusOne phase10 : Int)
    (hslack : positive-mass-2*minusOne-2*phase10+credit ≤ slack)
    (hcredit : 0 ≤ credit)
    (hdensity : mass+2*minusOne+2*phase10 ≤ positive) : 0 ≤ slack := by omega

theorem coefficient_one (halfArea objective positive mass credit minusOne phase10 : Int)
    (hslack : positive-mass-2*minusOne-2*phase10+credit ≤ halfArea-objective) :
    objective ≤ halfArea-positive+mass+2*minusOne+2*phase10-credit := by omega

theorem old_phase_restriction (slack positive minusOne negativeRotors credit : Int)
    (hslack : positive-(minusOne+2*negativeRotors)-2*minusOne-2*0+credit ≤ slack) :
    positive-3*minusOne-2*negativeRotors+credit ≤ slack := by omega

end SubQuorum.AllPhaseJointSlots
