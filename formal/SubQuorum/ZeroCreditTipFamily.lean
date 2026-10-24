import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace SubQuorum.ZeroCreditTipFamily

abbrev Point := Int × Int

structure Module where
  selected : List Point
  matching : List (Point × Point)
  deriving Inhabited

def modules : List Module := [
  { selected := [(0,1),(0,8),(2,1),(2,8),(3,3),(3,6),(4,1),(4,8),(5,3),(5,7),(6,1),(7,3),(8,1),(9,3),(10,1),(11,2)],
    matching := [((0,2),(0,3)),((0,4),(0,5)),((0,6),(0,7)),((1,3),(1,4)),((1,5),(1,6)),((1,2),(2,2)),((3,2),(4,2)),((5,2),(6,2)),((7,2),(8,2)),((9,2),(10,2)),((1,7),(2,7)),((3,7),(4,7))] },
  { selected := [(9,3),(9,5),(9,7),(9,9),(9,11),(9,13),(9,15),(10,2),(11,4),(11,6),(11,8),(11,10),(11,12),(14,12),(15,10),(16,11),(16,13),(16,15)],
    matching := [((10,15),(11,15)),((12,15),(13,15)),((14,15),(15,15)),((11,14),(12,14)),((13,14),(14,14)),((10,14),(10,13)),((10,12),(10,11)),((10,10),(10,9)),((10,8),(10,7)),((10,6),(10,5)),((10,4),(10,3)),((15,14),(15,13)),((15,12),(15,11))] },
  { selected := [(3,11),(3,13),(3,15),(4,10),(5,12),(8,4),(8,6),(8,8),(8,10),(8,12),(9,2),(10,3),(10,5),(10,7),(10,9),(10,11),(10,13),(10,15)],
    matching := [((9,15),(8,15)),((7,15),(6,15)),((5,15),(4,15)),((8,14),(7,14)),((6,14),(5,14)),((9,14),(9,13)),((9,12),(9,11)),((9,10),(9,9)),((9,8),(9,7)),((9,6),(9,5)),((9,4),(9,3)),((4,14),(4,13)),((4,12),(4,11))] }
]

def endpointsOf (module : Module) : List Point :=
  module.matching.flatMap fun edge => [edge.1,edge.2]

def matching := modules.flatMap Module.matching

def endpoints : List Point := matching.flatMap fun edge => [edge.1,edge.2]

def selected : List Point :=
  ((modules.flatMap Module.selected).eraseDups).filter fun point => !endpoints.contains point

def occupied := endpoints ++ selected

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

def newTails (module : Module) : List Point :=
  (endpointsOf module).filter fun point => (neighbors point).any fun other =>
    endpoints.contains other && !(endpointsOf module ++ module.selected).contains other &&
      tile point == tile other

def newFullTiles : List Point :=
  ((endpoints.map tile).eraseDups).filter fun square =>
    (cells square).all endpoints.contains &&
      !modules.any (fun module => (cells square).all (endpointsOf module).contains)

structure Step where
  endpoint : Point
  first : Point
  second : Point

def freezingSteps : List Step := [
  { endpoint := (4,7), first := (4,8), second := (5,7) },
  { endpoint := (4,11), first := (3,11), second := (4,10) },
  { endpoint := (10,2), first := (10,1), second := (11,2) },
  { endpoint := (15,11), first := (15,10), second := (16,11) },
  { endpoint := (2,7), first := (2,8), second := (3,7) },
  { endpoint := (4,13), first := (3,13), second := (4,12) },
  { endpoint := (8,2), first := (8,1), second := (9,2) },
  { endpoint := (15,13), first := (15,12), second := (16,13) },
  { endpoint := (0,7), first := (0,8), second := (1,7) },
  { endpoint := (4,15), first := (3,15), second := (4,14) },
  { endpoint := (6,2), first := (6,1), second := (7,2) },
  { endpoint := (15,15), first := (15,14), second := (16,15) },
  { endpoint := (1,6), first := (0,6), second := (1,7) },
  { endpoint := (4,2), first := (4,1), second := (5,2) },
  { endpoint := (5,14), first := (4,14), second := (5,15) },
  { endpoint := (14,14), first := (14,15), second := (15,14) },
  { endpoint := (0,5), first := (0,6), second := (1,5) },
  { endpoint := (2,2), first := (2,1), second := (3,2) },
  { endpoint := (6,15), first := (5,15), second := (6,14) },
  { endpoint := (13,15), first := (13,14), second := (14,15) },
  { endpoint := (0,2), first := (0,1), second := (1,2) },
  { endpoint := (1,4), first := (0,4), second := (1,5) },
  { endpoint := (7,14), first := (6,14), second := (7,15) },
  { endpoint := (12,14), first := (12,15), second := (13,14) },
  { endpoint := (0,3), first := (0,4), second := (1,3) },
  { endpoint := (1,3), first := (0,3), second := (1,2) },
  { endpoint := (8,15), first := (7,15), second := (8,14) },
  { endpoint := (11,15), first := (11,14), second := (12,15) },
  { endpoint := (0,4), first := (0,3), second := (1,4) },
  { endpoint := (1,2), first := (0,2), second := (1,3) },
  { endpoint := (9,14), first := (8,14), second := (9,15) },
  { endpoint := (10,14), first := (10,15), second := (11,14) },
  { endpoint := (1,5), first := (0,5), second := (1,4) },
  { endpoint := (3,2), first := (2,2), second := (3,3) },
  { endpoint := (9,12), first := (8,12), second := (9,13) },
  { endpoint := (10,12), first := (10,13), second := (11,12) },
  { endpoint := (0,6), first := (0,5), second := (1,6) },
  { endpoint := (5,2), first := (4,2), second := (5,3) },
  { endpoint := (9,10), first := (8,10), second := (9,11) },
  { endpoint := (10,10), first := (10,11), second := (11,10) },
  { endpoint := (1,7), first := (0,7), second := (1,6) },
  { endpoint := (7,2), first := (6,2), second := (7,3) },
  { endpoint := (9,8), first := (8,8), second := (9,9) },
  { endpoint := (10,8), first := (10,9), second := (11,8) },
  { endpoint := (3,7), first := (2,7), second := (3,6) },
  { endpoint := (9,6), first := (8,6), second := (9,7) },
  { endpoint := (10,6), first := (10,7), second := (11,6) },
  { endpoint := (9,4), first := (8,4), second := (9,5) },
  { endpoint := (10,4), first := (10,5), second := (11,4) },
  { endpoint := (9,2), first := (8,2), second := (9,3) },
  { endpoint := (9,3), first := (9,2), second := (10,3) },
  { endpoint := (9,5), first := (9,4), second := (10,5) },
  { endpoint := (10,3), first := (9,3), second := (10,2) },
  { endpoint := (9,7), first := (9,6), second := (10,7) },
  { endpoint := (10,5), first := (9,5), second := (10,4) },
  { endpoint := (9,9), first := (9,8), second := (10,9) },
  { endpoint := (10,7), first := (9,7), second := (10,6) },
  { endpoint := (9,11), first := (9,10), second := (10,11) },
  { endpoint := (10,9), first := (9,9), second := (10,8) },
  { endpoint := (9,13), first := (9,12), second := (10,13) },
  { endpoint := (10,11), first := (9,11), second := (10,10) },
  { endpoint := (9,15), first := (9,14), second := (10,15) },
  { endpoint := (10,13), first := (9,13), second := (10,12) },
  { endpoint := (8,14), first := (8,15), second := (9,14) },
  { endpoint := (10,15), first := (9,15), second := (10,14) },
  { endpoint := (7,15), first := (7,14), second := (8,15) },
  { endpoint := (11,14), first := (10,14), second := (11,15) },
  { endpoint := (6,14), first := (6,15), second := (7,14) },
  { endpoint := (12,15), first := (11,15), second := (12,14) },
  { endpoint := (5,15), first := (5,14), second := (6,15) },
  { endpoint := (13,14), first := (12,14), second := (13,15) },
  { endpoint := (4,14), first := (4,15), second := (5,14) },
  { endpoint := (14,15), first := (13,15), second := (14,14) },
  { endpoint := (4,12), first := (4,13), second := (5,12) },
  { endpoint := (15,14), first := (14,14), second := (15,15) },
  { endpoint := (15,12), first := (14,12), second := (15,13) }
]

def kept (frozen : List Point) (point : Point) : Bool :=
  selected.contains point || matching.any (fun edge =>
    (edge.1 == point && frozen.contains edge.2) ||
      (edge.2 == point && frozen.contains edge.1))

def replay : List Step → List Point → Bool
  | [], frozen => endpoints.all frozen.contains
  | step :: rest, frozen =>
      endpoints.contains step.endpoint && !frozen.contains step.endpoint &&
        step.first != step.second && adjacent step.endpoint step.first &&
        adjacent step.endpoint step.second && kept frozen step.first && kept frozen step.second &&
        replay rest (step.endpoint :: frozen)

theorem original_charges : modules.map charge = [-1,-1,-1] := by decide

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

theorem actual_counts : (endpoints.length,matching.length,selected.length) = (76,38,35) := by decide

theorem inside_rectangle : occupied.all (fun point =>
    0 ≤ point.1 && point.1 < 18 && 0 ≤ point.2 && point.2 < 16) = true := by decide

theorem exactly_one_new_tail : modules.map newTails = [[(10,2)],[],[]] := by decide

theorem event_is_minus_one_irregular_tip :
    let original := modules[0]!
    charge original = -1 ∧ degree (endpointsOf original) (10,2) = 1 ∧
      (cells (5,1)).filter (endpointsOf original).contains = [(10,2)] ∧
      (cells (5,1)).filter original.selected.contains = [(11,2)] := by decide

theorem actual_new_neighbor :
    (endpointsOf modules[1]!).contains (10,3) = true ∧
      !(endpointsOf modules[0]! ++ modules[0]!.selected).contains (10,3) = true ∧
      adjacent (10,2) (10,3) = true ∧ tile (10,2) = tile (10,3) := by decide

theorem tip_tile_not_full :
    (cells (5,1)).filter endpoints.contains = [(10,2),(10,3)] ∧
      (cells (5,1)).filter selected.contains = [(11,2)] := by decide

theorem zero_new_full_tiles : newFullTiles = [] := by decide

theorem nonaligned_contact_square :
    [(9,2),(9,3),(10,2),(10,3)].all endpoints.contains = true ∧
      tile (9,2) ≠ tile (10,2) := by decide

theorem exact_receiver_counts :
    let receiver := (endpoints.map tile).eraseDups
    (receiver.length,(selected.filter fun point => receiver.contains (tile point)).length) =
      (30,20) := by decide

theorem final_receiver_charge :
    let receiver := (endpoints.map tile).eraseDups
    Int.ofNat ((selected.filter fun point => receiver.contains (tile point)).length)+
      Int.ofNat matching.length-2*Int.ofNat receiver.length = -2 := by decide

theorem exact_half_area_slack : (18*16/2-selected.length-matching.length : Nat) = 71 := by decide

theorem full_freezing_certificate : replay freezingSteps [] = true := by decide

theorem freezing_covers_all_endpoints : freezingSteps.length = endpoints.length := by decide

theorem residual_square_credit_rule_refuted :
    ¬ (modules.flatMap newTails).length ≤ 2*newFullTiles.length := by decide

theorem two_kept_neighbors_force_frozen (promoted occupiedSite : Point → Prop)
    (endpoint first second : Point) (hdistinct : first ≠ second)
    (hfirstAdjacent : adjacent endpoint first = true)
    (hsecondAdjacent : adjacent endpoint second = true)
    (hfirst : occupiedSite first) (hsecond : occupiedSite second)
    (hfeasible : promoted endpoint →
      ∀ left right, adjacent endpoint left = true → adjacent endpoint right = true →
        occupiedSite left → occupiedSite right → left = right) :
    ¬ promoted endpoint := by
  intro chosen
  exact hdistinct (hfeasible chosen first second hfirstAdjacent hsecondAdjacent hfirst hsecond)

theorem repeated_budget (slack copies : Int)
    (hledger : 3*copies-copies ≤ slack) : 2*copies ≤ slack := by omega

theorem repeated_credit_rule_fails (copies : Nat) (hpositive : 0 < copies) :
    ¬ copies ≤ 0 := by omega

end SubQuorum.ZeroCreditTipFamily
