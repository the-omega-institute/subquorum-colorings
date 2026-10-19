import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 20000000

namespace SubQuorum.MinusOneGateWitness

abbrev Point := Int × Int

structure Module where
  selected : List Point
  matching : List (Point × Point)

def modules : List Module := [
  { selected := [(0,6),(0,21),(2,6),(2,21),(3,8),(3,19),(4,6),(4,21),(5,7),(5,20)],
    matching := [((0,7),(0,8)),((0,9),(0,10)),((0,11),(0,12)),((0,13),(0,14)),((0,15),(0,16)),((0,17),(0,18)),((0,19),(0,20)),((1,8),(1,9)),((1,10),(1,11)),((1,12),(1,13)),((1,14),(1,15)),((1,16),(1,17)),((1,18),(1,19)),((1,7),(2,7)),((3,7),(4,7)),((1,20),(2,20)),((3,20),(4,20))] },
  { selected := [(2,7),(2,14),(4,7),(4,14),(5,9),(5,12),(6,7),(6,14),(7,8),(7,13)],
    matching := [((2,8),(2,9)),((2,10),(2,11)),((2,12),(2,13)),((3,9),(3,10)),((3,11),(3,12)),((3,8),(4,8)),((5,8),(6,8)),((3,13),(4,13)),((5,13),(6,13))] },
  { selected := [(2,13),(2,20),(4,13),(4,20),(5,15),(5,18),(6,13),(6,20),(7,14),(7,19)],
    matching := [((2,14),(2,15)),((2,16),(2,17)),((2,18),(2,19)),((3,15),(3,16)),((3,17),(3,18)),((3,14),(4,14)),((5,14),(6,14)),((3,19),(4,19)),((5,19),(6,19))] },
  { selected := [(4,2),(4,7),(5,1),(5,8),(6,3),(6,6),(7,1),(7,8),(9,1),(9,8)],
    matching := [((9,2),(9,3)),((9,4),(9,5)),((9,6),(9,7)),((8,3),(8,4)),((8,5),(8,6)),((8,2),(7,2)),((6,2),(5,2)),((8,7),(7,7)),((6,7),(5,7))] },
  { selected := [(4,20),(4,25),(5,19),(5,26),(6,21),(6,24),(7,19),(7,26),(9,19),(9,26)],
    matching := [((9,20),(9,21)),((9,22),(9,23)),((9,24),(9,25)),((8,21),(8,22)),((8,23),(8,24)),((8,20),(7,20)),((6,20),(5,20)),((8,25),(7,25)),((6,25),(5,25))] },
  { selected := [(6,8),(6,13),(7,7),(7,14),(8,9),(8,12),(9,7),(9,14),(11,7),(11,14)],
    matching := [((11,8),(11,9)),((11,10),(11,11)),((11,12),(11,13)),((10,9),(10,10)),((10,11),(10,12)),((10,8),(9,8)),((8,8),(7,8)),((10,13),(9,13)),((8,13),(7,13))] },
  { selected := [(6,14),(6,19),(7,13),(7,20),(8,15),(8,18),(9,13),(9,20),(11,13),(11,20)],
    matching := [((11,14),(11,15)),((11,16),(11,17)),((11,18),(11,19)),((10,15),(10,16)),((10,17),(10,18)),((10,14),(9,14)),((8,14),(7,14)),((10,19),(9,19)),((8,19),(7,19))] }
]

def endpointsOf (module : Module) : List Point :=
  module.matching.flatMap fun edge => [edge.1,edge.2]

def matching := modules.flatMap Module.matching

def endpoints : List Point := matching.flatMap fun edge => [edge.1,edge.2]

def selected : List Point :=
  ((modules.flatMap Module.selected).eraseDups).filter fun point => !endpoints.contains point

def occupied := endpoints++selected

def adjacent (first second : Point) : Bool :=
  (first.1-second.1).natAbs+(first.2-second.2).natAbs == 1

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),(point.1,point.2-1),(point.1,point.2+1)]

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

def donorTiles : List Point := [(1,4),(1,9)]

instance : Inhabited Module := ⟨{selected := [], matching := []}⟩

def oldPositive : Module := modules[0]!

theorem original_charges : modules.map charge = [1,-1,-1,-1,-1,-1,-1] := by decide

theorem matching_endpoints_distinct : endpoints.Nodup := by decide

theorem actual_matching_edges : matching.all (fun edge => adjacent edge.1 edge.2) = true := by decide

theorem original_feasibility : modules.all (fun module =>
    let sites := endpointsOf module ++ module.selected
    module.selected.all (fun point => degree sites point == 1) &&
      (endpointsOf module).all (fun point => degree sites point == 3)) = true := by decide

theorem final_selected_feasibility :
    selected.all (fun point => degree occupied point == 1) = true := by decide

theorem final_endpoint_min_degree :
    endpoints.all (fun point => 3 ≤ degree occupied point) = true := by decide

theorem actual_counts :
    (endpoints.length, matching.length, selected.length) = (142,71,28) := by decide

theorem inside_rectangle : occupied.all (fun point =>
    0 ≤ point.1 && point.1 < 12 && 0 ≤ point.2 && point.2 < 28) = true := by decide

theorem no_intratile_new_neighbors : modules.all (fun module =>
    (endpointsOf module).all (fun point =>
      (neighbors point).all (fun other =>
        !endpoints.contains other || (endpointsOf module ++ module.selected).contains other ||
          tile point != tile other))) = true := by decide

theorem no_new_full_tiles : ((endpoints.map tile).eraseDups).all (fun square =>
    !((cells square).all endpoints.contains) ||
      modules.any (fun module => (cells square).all (endpointsOf module).contains)) = true := by decide

theorem old_donor_profiles : donorTiles.all (fun square =>
    !((cells square).any (endpointsOf oldPositive).contains) &&
      ((cells square).filter oldPositive.selected.contains).length == 1) = true := by decide

theorem both_old_donors_fully_consumed :
    donorTiles.all (fun square => (cells square).all endpoints.contains) = true := by decide

theorem final_receiver_charge :
    let receiver := (endpoints.map tile).eraseDups
    Int.ofNat ((selected.filter fun point => receiver.contains (tile point)).length)+
      Int.ofNat matching.length-2*Int.ofNat receiver.length = -5 := by decide

theorem exact_half_area_slack : (12*28/2-selected.length-matching.length : Nat) = 69 := by decide

end SubQuorum.MinusOneGateWitness
