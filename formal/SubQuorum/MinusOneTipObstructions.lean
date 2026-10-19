import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 30000000

namespace SubQuorum.MinusOneTipObstructions

abbrev Point := Int × Int

structure Module where
  selected : List Point
  matching : List (Point × Point)
  deriving Inhabited

structure Example where
  rows : Nat
  columns : Nat
  modules : List Module
  deriving Inhabited

def twoTipModules : List Module := [
  { selected := [(0,5),(0,20),(2,5),(2,20),(3,7),(3,18),(4,5),(4,20),(5,7),(5,19),(6,5),(7,7),(8,5),(9,6)],
    matching := [((0,6),(0,7)),((0,8),(0,9)),((0,10),(0,11)),((0,12),(0,13)),((0,14),(0,15)),((0,16),(0,17)),((0,18),(0,19)),((1,7),(1,8)),((1,9),(1,10)),((1,11),(1,12)),((1,13),(1,14)),((1,15),(1,16)),((1,17),(1,18)),((1,6),(2,6)),((3,6),(4,6)),((5,6),(6,6)),((7,6),(8,6)),((1,19),(2,19)),((3,19),(4,19))] },
  { selected := [(2,6),(2,13),(4,6),(4,13),(5,8),(5,11),(6,6),(6,13),(7,7),(7,12)],
    matching := [((2,12),(2,11)),((2,10),(2,9)),((2,8),(2,7)),((3,11),(3,10)),((3,9),(3,8)),((3,12),(4,12)),((5,12),(6,12)),((3,7),(4,7)),((5,7),(6,7))] },
  { selected := [(2,12),(2,19),(4,12),(4,19),(5,14),(5,17),(6,12),(6,19),(7,13),(7,18)],
    matching := [((2,18),(2,17)),((2,16),(2,15)),((2,14),(2,13)),((3,17),(3,16)),((3,15),(3,14)),((3,18),(4,18)),((5,18),(6,18)),((3,13),(4,13)),((5,13),(6,13))] },
  { selected := [(6,7),(6,12),(7,6),(7,13),(8,8),(8,11),(9,6),(9,13),(11,6),(11,13)],
    matching := [((11,7),(11,8)),((11,9),(11,10)),((11,11),(11,12)),((10,8),(10,9)),((10,10),(10,11)),((10,7),(9,7)),((8,7),(7,7)),((10,12),(9,12)),((8,12),(7,12))] },
  { selected := [(4,19),(5,18),(5,21),(6,22),(7,17),(8,18),(8,21),(9,20)],
    matching := [((6,19),(5,19)),((6,20),(6,21)),((7,20),(8,20)),((7,19),(7,18))] },
  { selected := [(6,13),(7,12),(8,14),(9,12),(10,14),(10,18),(11,12),(11,19),(12,14),(12,17),(13,12),(13,19),(15,12),(15,19)],
    matching := [((15,13),(15,14)),((15,15),(15,16)),((15,17),(15,18)),((14,14),(14,15)),((14,16),(14,17)),((14,13),(13,13)),((12,13),(11,13)),((10,13),(9,13)),((8,13),(7,13)),((14,18),(13,18)),((12,18),(11,18))] },
  { selected := [(8,6),(9,7),(10,5),(11,7),(12,1),(12,5),(13,0),(13,7),(14,2),(14,5),(15,0),(15,7),(17,0),(17,7)],
    matching := [((17,6),(17,5)),((17,4),(17,3)),((17,2),(17,1)),((16,5),(16,4)),((16,3),(16,2)),((16,6),(15,6)),((14,6),(13,6)),((12,6),(11,6)),((10,6),(9,6)),((16,1),(15,1)),((14,1),(13,1))] }
]

def overloadedModules : List Module := [
  { selected := [(4,7),(4,22),(6,7),(6,22),(7,9),(7,20),(8,7),(8,22),(9,9),(9,21),(10,7),(11,9),(12,7),(13,8)],
    matching := [((4,8),(4,9)),((4,10),(4,11)),((4,12),(4,13)),((4,14),(4,15)),((4,16),(4,17)),((4,18),(4,19)),((4,20),(4,21)),((5,9),(5,10)),((5,11),(5,12)),((5,13),(5,14)),((5,15),(5,16)),((5,17),(5,18)),((5,19),(5,20)),((5,8),(6,8)),((7,8),(8,8)),((9,8),(10,8)),((11,8),(12,8)),((5,21),(6,21)),((7,21),(8,21))] },
  { selected := [(6,14),(6,21),(8,14),(8,21),(9,16),(9,19),(10,14),(10,21),(11,15),(11,20)],
    matching := [((6,20),(6,19)),((6,18),(6,17)),((6,16),(6,15)),((7,19),(7,18)),((7,17),(7,16)),((7,20),(8,20)),((9,20),(10,20)),((7,15),(8,15)),((9,15),(10,15))] },
  { selected := [(8,2),(8,7),(9,1),(9,8),(10,3),(10,6),(11,1),(11,8),(13,1),(13,8)],
    matching := [((13,2),(13,3)),((13,4),(13,5)),((13,6),(13,7)),((12,3),(12,4)),((12,5),(12,6)),((12,2),(11,2)),((10,2),(9,2)),((12,7),(11,7)),((10,7),(9,7))] },
  { selected := [(10,15),(10,20),(11,14),(11,21),(12,16),(12,19),(13,14),(13,21),(15,14),(15,21)],
    matching := [((15,15),(15,16)),((15,17),(15,18)),((15,19),(15,20)),((14,16),(14,17)),((14,18),(14,19)),((14,15),(13,15)),((12,15),(11,15)),((14,20),(13,20)),((12,20),(11,20))] },
  { selected := [(8,21),(8,26),(9,20),(9,27),(10,22),(10,25),(11,20),(11,27),(13,20),(13,27)],
    matching := [((13,26),(13,25)),((13,24),(13,23)),((13,22),(13,21)),((12,25),(12,24)),((12,23),(12,22)),((12,26),(11,26)),((10,26),(9,26)),((12,21),(11,21)),((10,21),(9,21))] },
  { selected := [(10,9),(11,8),(11,11),(12,12),(13,7),(14,8),(14,11),(15,10)],
    matching := [((12,9),(11,9)),((12,10),(12,11)),((13,10),(14,10)),((13,9),(13,8))] },
  { selected := [(0,1),(0,8),(2,1),(2,8),(3,3),(3,6),(4,1),(4,8),(5,2),(5,6),(6,8),(7,6),(8,8),(9,7)],
    matching := [((0,7),(0,6)),((0,5),(0,4)),((0,3),(0,2)),((1,6),(1,5)),((1,4),(1,3)),((1,7),(2,7)),((3,7),(4,7)),((5,7),(6,7)),((7,7),(8,7)),((1,2),(2,2)),((3,2),(4,2))] },
  { selected := [(6,8),(6,15),(8,8),(8,15),(9,10),(9,13),(10,8),(10,15),(11,9),(11,13),(12,15),(13,13),(14,15),(15,14)],
    matching := [((6,14),(6,13)),((6,12),(6,11)),((6,10),(6,9)),((7,13),(7,12)),((7,11),(7,10)),((7,14),(8,14)),((9,14),(10,14)),((11,14),(12,14)),((13,14),(14,14)),((7,9),(8,9)),((9,9),(10,9))] },
  { selected := [(14,14),(15,15),(16,13),(17,15),(18,9),(18,13),(19,8),(19,15),(20,10),(20,13),(21,8),(21,15),(23,8),(23,15)],
    matching := [((23,14),(23,13)),((23,12),(23,11)),((23,10),(23,9)),((22,13),(22,12)),((22,11),(22,10)),((22,14),(21,14)),((20,14),(19,14)),((18,14),(17,14)),((16,14),(15,14)),((22,9),(21,9)),((20,9),(19,9))] }
]

def examples : List Example :=
  [{ rows := 18, columns := 24, modules := twoTipModules },
   { rows := 24, columns := 28, modules := overloadedModules }]

def endpointsOf (module : Module) : List Point :=
  module.matching.flatMap fun edge => [edge.1,edge.2]

def matching (witness : Example) := witness.modules.flatMap Module.matching

def endpoints (witness : Example) : List Point :=
  (matching witness).flatMap fun edge => [edge.1,edge.2]

def selected (witness : Example) : List Point :=
  ((witness.modules.flatMap Module.selected).eraseDups).filter fun point =>
    !(endpoints witness).contains point

def occupied (witness : Example) := endpoints witness ++ selected witness

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),(point.1,point.2-1),(point.1,point.2+1)]

def adjacent (first second : Point) : Bool :=
  (first.1-second.1).natAbs+(first.2-second.2).natAbs == 1

def degree (sites : List Point) (point : Point) : Nat :=
  ((neighbors point).filter sites.contains).length

def tile (point : Point) : Point := (point.1/2,point.2/2)

def cells (square : Point) : List Point :=
  [(2*square.1,2*square.2),(2*square.1+1,2*square.2),
   (2*square.1,2*square.2+1),(2*square.1+1,2*square.2+1)]

def charge (module : Module) : Int :=
  let receiver := ((endpointsOf module).map tile).eraseDups
  Int.ofNat ((module.selected.filter fun point => receiver.contains (tile point)).length)+
    Int.ofNat module.matching.length-2*Int.ofNat receiver.length

def irregular (module : Module) (point : Point) : Bool :=
  let square := cells (tile point)
  let endpointCount := (square.filter (endpointsOf module).contains).length
  let selectionCount := (square.filter module.selected.contains).length
  (endpointCount == 1 && selectionCount == 1) ||
    (endpointCount == 2 && selectionCount == 0)

def newTails (witness : Example) (module : Module) : List Point :=
  (endpointsOf module).filter fun point =>
    (neighbors point).any fun other =>
      (endpoints witness).contains other &&
      !(endpointsOf module ++ module.selected).contains other && tile point == tile other

def regularTails (witness : Example) : List Point :=
  witness.modules.flatMap fun module => (newTails witness module).filter fun point =>
    !irregular module point

def irregularTails (witness : Example) : List Point :=
  witness.modules.flatMap fun module => (newTails witness module).filter (irregular module)

def newFullTiles (witness : Example) : List Point :=
  (((endpoints witness).map tile).eraseDups).filter fun square =>
    (cells square).all (endpoints witness).contains &&
      !witness.modules.any (fun module => (cells square).all (endpointsOf module).contains)

def eventsAt (tails : List Point) (square : Point) : Nat :=
  (tails.filter fun point => tile point == square).length

theorem original_charges : examples.map (fun witness => witness.modules.map charge) =
    [[-1,1,1,1,0,1,1],[-1,1,-1,1,1,0,-1,1,1]] := by decide

theorem matching_endpoints_distinct :
    examples.all (fun witness => (endpoints witness).eraseDups.length ==
      (endpoints witness).length) = true := by decide

theorem actual_matching_edges : examples.all (fun witness =>
    (matching witness).all (fun edge => adjacent edge.1 edge.2)) = true := by decide

theorem original_feasibility : examples.all (fun witness =>
    witness.modules.all (fun module =>
      let sites := endpointsOf module ++ module.selected
      module.selected.all (fun point => degree sites point == 1) &&
        (endpointsOf module).all (fun point => degree sites point == 3))) = true := by decide

theorem final_selected_feasibility : examples.all (fun witness =>
    (selected witness).all (fun point => degree (occupied witness) point == 1)) = true := by decide

theorem final_endpoint_min_degree : examples.all (fun witness =>
    (endpoints witness).all (fun point => 3 ≤ degree (occupied witness) point)) = true := by decide

theorem actual_counts : examples.map (fun witness =>
    ((endpoints witness).length,(matching witness).length,(selected witness).length)) =
    [(144,72,41),(184,92,51)] := by decide

theorem inside_rectangles : examples.all (fun witness =>
    (occupied witness).all (fun point =>
      0 ≤ point.1 && point.1 < Int.ofNat witness.rows &&
        0 ≤ point.2 && point.2 < Int.ofNat witness.columns)) = true := by decide

theorem both_minus_one_tips_gain : examples.all (fun witness =>
    let original := witness.modules[0]!
    charge original == -1 &&
      ((endpointsOf original).filter (fun point => degree (endpointsOf original) point == 1)).length == 2 &&
      (endpointsOf original).all (fun point =>
        degree (endpointsOf original) point != 1 ||
          (newTails witness original).contains point)) = true := by decide

theorem irregular_events_are_original_tips : examples.all (fun witness =>
    (irregularTails witness).length == 2 &&
      (irregularTails witness).all (fun point =>
        (endpointsOf witness.modules[0]!).contains point &&
          degree (endpointsOf witness.modules[0]!) point == 1)) = true := by decide

theorem exact_event_and_square_counts : examples.all (fun witness =>
    (regularTails witness).length == 21 && (irregularTails witness).length == 2 &&
      (newFullTiles witness).length == 13) = true := by decide

theorem exact_unused_regular_credit : examples.all (fun witness =>
    2*(newFullTiles witness).length-(regularTails witness).length == 5) = true := by decide

theorem overloaded_tile_partition :
    let witness := examples[1]!
    let square := (6,4)
    (newFullTiles witness).contains square = true ∧
      (cells square).filter (endpointsOf witness.modules[0]!).contains = [(12,8)] ∧
      (cells square).filter (endpointsOf witness.modules[5]!).contains = [(13,8),(12,9),(13,9)] := by decide

theorem overloaded_tile_events :
    let witness := examples[1]!
    eventsAt (regularTails witness) (6,4) = 2 ∧
      eventsAt (irregularTails witness) (6,4) = 1 ∧
      eventsAt (regularTails witness ++ irregularTails witness) (6,4) = 3 := by decide

theorem final_receiver_charges : examples.map (fun witness =>
    let receiver := ((endpoints witness).map tile).eraseDups
    Int.ofNat (((selected witness).filter fun point => receiver.contains (tile point)).length)+
      Int.ofNat (matching witness).length-2*Int.ofNat receiver.length) = [1,-1] := by decide

theorem exact_half_area_slacks : examples.map (fun witness =>
    witness.rows*witness.columns/2-(selected witness).length-(matching witness).length) =
    [103,193] := by decide

theorem per_tile_capacity_two_refuted :
    let witness := examples[1]!
    ¬ eventsAt (regularTails witness ++ irregularTails witness) (6,4) ≤ 2 := by decide

end SubQuorum.MinusOneTipObstructions
