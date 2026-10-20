import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 100000000

namespace SubQuorum.RotorOnlyReserve

abbrev Point := Int × Int
abbrev Owner := Bool × Int × Int

def endpoints : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def selected : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),
   (point.1,point.2-1),(point.1,point.2+1)]

def move (owner : Owner) (point : Point) : Point :=
  (point.1+owner.2.1,(if owner.1 then -point.2 else point.2)+owner.2.2)

def sourceP (owner : Owner) : List Point := endpoints.map (move owner)

def sourceT (owner : Owner) : List Point := selected.map (move owner)

def allP (sources : List Owner) : List Point := sources.flatMap sourceP

def allT (sources : List Owner) : List Point := sources.flatMap sourceT

def samePoints (first second : List Point) : Bool :=
  first.length == second.length && first.all second.contains && second.all first.contains

def possibleOwners (target : Point) (existing : List Owner) : List Owner :=
  (([false,true].flatMap fun mirror => endpoints.map fun endpoint =>
    (mirror,target.1-endpoint.1,target.2-(if mirror then -endpoint.2 else endpoint.2))).filter
      fun owner => (sourceP owner).all fun point => !(allP existing).contains point)

def sameOwners (first second : List Owner) : Bool :=
  first.length == second.length && first.all second.contains && second.all first.contains

def forcedSupport (target : Point) (existing : List Owner) : Bool :=
  (allT existing).contains target && !(allP existing).contains target &&
    decide (2 ≤ ((neighbors target).filter (allP existing).contains).length)

theorem quarter_invariance :
    samePoints (endpoints.map fun point => (point.2,5-point.1)) endpoints = true ∧
    samePoints (selected.map fun point => (point.2,5-point.1)) selected = true := by decide

theorem original_occupied_degrees :
    endpoints.all (fun point =>
      ((neighbors point).filter (endpoints ++ selected).contains).length == 3) = true ∧
    selected.all (fun point =>
      ((neighbors point).filter (endpoints ++ selected).contains).length == 1 &&
      ((neighbors point).filter endpoints.contains).length == 1) = true := by decide

theorem initial_blank_owners :
    sameOwners (possibleOwners (1,3) [(false,0,0)])
      [(false,-2,2),(false,-3,0),(true,-3,6)] = true := by decide

theorem type_a_first_owners :
    forcedSupport (1,1) [(false,0,0),(false,-3,0)] = true ∧
    sameOwners (possibleOwners (1,1) [(false,0,0),(false,-3,0)])
      [(false,-1,-3),(true,-2,2)] = true := by decide

theorem type_a_reflected_dead_end :
    forcedSupport (2,1) [(false,0,0),(false,-3,0),(true,-2,2)] = true ∧
    possibleOwners (2,1) [(false,0,0),(false,-3,0),(true,-2,2)] = [] := by decide

theorem type_a_second_owner :
    forcedSupport (0,0) [(false,0,0),(false,-3,0),(false,-1,-3)] = true ∧
    sameOwners (possibleOwners (0,0) [(false,0,0),(false,-3,0),(false,-1,-3)])
      [(false,-4,-3)] = true := by decide

theorem type_b_first_owner :
    forcedSupport (1,4) [(false,0,0),(true,-3,6)] = true ∧
    sameOwners (possibleOwners (1,4) [(false,0,0),(true,-3,6)])
      [(true,-1,8)] = true := by decide

theorem type_b_second_owner :
    forcedSupport (3,4) [(false,0,0),(true,-3,6),(true,-1,8)] = true ∧
    sameOwners (possibleOwners (3,4) [(false,0,0),(true,-3,6),(true,-1,8)])
      [(false,2,2)] = true := by decide

def negativeOwner (mirror : Bool) (row column : Int) : Owner :=
  (mirror,2*row,if mirror then 5+2*column else 2*column)

def cardinal : List Point := [(-1,0),(0,1),(1,0),(0,-1)]

def diagonal : List Point := [(-1,-1),(-1,1),(1,-1),(1,1)]

def overlap (first second : Owner) : Bool :=
  (sourceP first).any (sourceP second).contains

theorem cardinal_centers_overlap :
    [false,true].all (fun firstMirror => [false,true].all fun secondMirror =>
      cardinal.all fun offset =>
        overlap (negativeOwner firstMirror 0 0)
          (negativeOwner secondMirror offset.1 offset.2)) = true := by decide

theorem opposite_diagonal_chiralities_overlap :
    [false,true].all (fun mirror => diagonal.all fun offset =>
      overlap (negativeOwner mirror 0 0)
        (negativeOwner (!mirror) offset.1 offset.2)) = true := by decide

def tile (point : Point) : Point := (point.1/2,point.2/2)

def eventCount (first second : Owner) : Nat :=
  ((sourceP first).map fun point => ((neighbors point).filter fun other =>
    (sourceP second).contains other &&
    !(sourceP first ++ sourceT first).contains other &&
    tile point == tile other).length).sum

theorem diagonal_pair_has_two_events :
    [false,true].all (fun mirror => diagonal.all fun offset =>
      let first := negativeOwner mirror 0 0
      let second := negativeOwner mirror offset.1 offset.2
      eventCount first second+eventCount second first == 2) = true := by decide

def portTile : List Point := [(2,2),(2,3),(3,2),(3,3)]

def portCheck (mirror : Bool) (entry : Point × Point × Point) : Bool :=
  let offset := entry.1
  let expectedP := entry.2.1
  let expectedT := entry.2.2
  let owner := negativeOwner mirror offset.1 offset.2
  samePoints ((sourceP owner).filter portTile.contains) [expectedP] &&
  samePoints ((sourceT owner).filter portTile.contains) [expectedT]

theorem complete_port_table :
    [((-1,0),(2,3),(3,3)),((0,1),(3,3),(3,2)),
     ((1,0),(3,2),(2,2)),((0,-1),(2,2),(2,3))].all (portCheck false) = true ∧
    [((-1,0),(2,2),(3,2)),((0,1),(2,3),(2,2)),
     ((1,0),(3,3),(2,3)),((0,-1),(3,2),(3,3))].all (portCheck true) = true := by decide

def inverseIndex (point : Point) : Option Point :=
  if (point.1+point.2)%4 == 0 && (point.1-point.2)%4 == 0 then
    some ((point.1+point.2)/4,(point.1-point.2)/4)
  else none

def roleDisplacements (first second : List Point) : List Point :=
  ((first.flatMap fun left => second.filterMap fun right =>
    inverseIndex (left.1-right.1,left.2-right.2))).eraseDups

theorem family_endpoint_and_support_disjointness :
    roleDisplacements endpoints endpoints = [(0,0)] ∧
    roleDisplacements selected selected = [(0,0)] := by decide

def familySupportCheck (entry : Point × Point) : Bool :=
  samePoints (roleDisplacements [entry.1] endpoints) [entry.2] &&
  (roleDisplacements ((neighbors entry.1).filter fun point => !endpoints.contains point)
    (endpoints ++ selected)).all (fun offset =>
      if entry.2.1 != 0 then offset.1 == entry.2.1 else offset.2 == entry.2.2)

theorem complete_family_support_roles :
    [((0,2),(-1,0)),((1,1),(-1,0)),((1,4),(0,-1)),((2,5),(0,-1)),
     ((4,4),(1,0)),((5,3),(1,0)),((3,0),(0,1)),((4,1),(0,1))].all
      familySupportCheck = true := by decide

theorem rectangle_euler_identity (firstSize secondSize : Int) :
    firstSize*secondSize-((firstSize-1)*secondSize+firstSize*(secondSize-1))+
      (firstSize-1)*(secondSize-1) = 1 := by
  simp [Int.sub_mul, Int.mul_sub]
  omega

theorem component_reserve (mass credit irregular vertices edges faces components : Int)
    (hmass : mass = 2*vertices)
    (hevents : irregular = 2*edges)
    (hcredit : 2*faces ≤ credit)
    (heuler : vertices-edges+faces = components) :
    2*components ≤ mass+credit-irregular := by omega

theorem all_negative_exact_reserve (mass credit irregular vertices edges faces components : Int)
    (hmass : mass = 2*vertices)
    (hevents : irregular = 2*edges)
    (hcredit : credit = 2*faces)
    (heuler : vertices-edges+faces = components) :
    mass+credit-irregular = 2*components := by omega

theorem exact_other_credit (mass credit irregular vertices edges faces components otherCredit : Int)
    (hmass : mass = 2*vertices)
    (hevents : irregular = 2*edges)
    (hcredit : credit = 2*faces+otherCredit)
    (heuler : vertices-edges+faces = components) :
    mass+credit-irregular = 2*components+otherCredit := by omega

theorem ambient_slack (slack mass credit irregular components : Int)
    (hledger : mass+credit-irregular ≤ slack)
    (hreserve : 2*components ≤ mass+credit-irregular) :
    2*components ≤ slack := by omega

end SubQuorum.RotorOnlyReserve
