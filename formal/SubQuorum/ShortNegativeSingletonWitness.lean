import Lean

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 0

namespace SubQuorum.ShortNegativeSingletonWitness

abbrev Point := Int × Int
abbrev Edge := Point × Point

structure Source where
  width : Nat
  near : Nat
  far : Nat
  transpose : Bool
  flipRow : Bool
  flipColumn : Bool
  rowOffset : Int
  columnOffset : Int

def move (source : Source) (point : Point) : Point :=
  let row := if source.flipRow then -point.1 else point.1
  let column := if source.flipColumn then -point.2 else point.2
  if source.transpose then
    (column+source.rowOffset,row+source.columnOffset)
  else (row+source.rowOffset,column+source.columnOffset)

def originalMatching (source : Source) : List Edge :=
  let top := (List.range (source.width/2)).map fun (index : Nat) =>
    (((0,2*(index : Int)+1),(0,2*(index : Int)+2)) : Edge)
  let lower := (List.range ((source.width-2)/2)).map fun (index : Nat) =>
    (((1,2*(index : Int)+2),(1,2*(index : Int)+3)) : Edge)
  let near := (List.range (source.near/2)).map fun (index : Nat) =>
    (((2*(index : Int)+1,1),(2*(index : Int)+2,1)) : Edge)
  let far := (List.range (source.far/2)).map fun (index : Nat) =>
    (((2*(index : Int)+1,source.width),(2*(index : Int)+2,source.width)) : Edge)
  (top++lower++near++far).map fun edge => (move source edge.1,move source edge.2)

def endpoints (source : Source) : List Point :=
  (originalMatching source).flatMap fun edge => [edge.1,edge.2]

def supports (source : Source) : List Point :=
  let caps : List Point := [(0,0),(0,source.width+1),
    (source.near+1,1),(source.far+1,source.width)]
  let near := (List.range (source.near-1)).map fun index =>
    (((index+2 : Nat) : Int),if (index+2)%2 == 0 then 0 else 2)
  let far := (List.range (source.far-1)).map fun index =>
    (((index+2 : Nat) : Int),if (index+2)%2 == 0 then
      (source.width : Int)+1 else (source.width : Int)-1)
  (caps++near++far).map (move source)

def witness : List Source := [
  ⟨12,4,4,false,false,false,0,0⟩,
  ⟨6,6,4,false,true,false,9,1⟩,
  ⟨14,8,4,true,true,false,1,10⟩,
  ⟨6,4,4,false,false,false,3,2⟩,
  ⟨6,4,4,false,false,false,5,-5⟩,
  ⟨6,4,8,false,false,false,-4,-6⟩,
  ⟨6,6,6,true,false,false,15,6⟩,
  ⟨8,4,8,true,true,true,5,17⟩,
  ⟨10,4,4,false,true,false,6,10⟩,
  ⟨10,4,6,false,true,false,14,-2⟩,
  ⟨10,6,6,false,true,false,21,-5⟩]

def allEndpoints : List Point := witness.flatMap endpoints
def allMatching : List Edge := witness.flatMap originalMatching
def allSupports : List Point := (witness.flatMap supports).eraseDups
def selected : List Point := allSupports.filter fun point => !allEndpoints.contains point
def occupied : List Point := (allEndpoints++allSupports).eraseDups

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),
   (point.1,point.2-1),(point.1,point.2+1)]

def occupiedDegree (points : List Point) (point : Point) : Nat :=
  ((neighbors point).filter points.contains).length

def originalFeasible (source : Source) : Bool :=
  let sourceOccupied := (endpoints source++supports source).eraseDups
  (supports source).all (fun point => occupiedDegree sourceOccupied point == 1) &&
  (endpoints source).all (fun point => decide (3 ≤ occupiedDegree sourceOccupied point))

theorem every_original_source_is_feasible : witness.all originalFeasible = true := by
  decide

theorem endpoint_ownership_is_disjoint :
    allEndpoints.length = 278 ∧ allEndpoints.eraseDups.length = 278 := by
  decide

theorem unchanged_matching_is_a_lattice_matching :
    allMatching.length = 139 ∧
    allMatching.all (fun edge => (neighbors edge.1).contains edge.2) = true := by
  decide

theorem every_retained_support_has_one_occupied_neighbor :
    selected.length = 62 ∧
    selected.all (fun point => occupiedDegree occupied point == 1) = true := by
  decide

theorem every_endpoint_has_at_least_three_occupied_neighbors :
    allEndpoints.all (fun point => decide (3 ≤ occupiedDegree occupied point)) = true := by
  decide

theorem the_marked_gate_has_a_negative_singleton_consumer :
    (supports ⟨12,4,4,false,false,false,0,0⟩).contains (3,2) = true ∧
    [(2,2),(2,3),(3,2),(3,3)].map
      (endpoints ⟨6,6,4,false,true,false,9,1⟩).contains = [false,false,true,false] ∧
    (supports ⟨6,6,4,false,true,false,9,1⟩).contains (2,2) = true := by
  decide

theorem the_actual_transverse_and_upper_corner_chain_is_present :
    [(2,2),(2,3)].all (endpoints ⟨14,8,4,true,true,false,1,10⟩).contains = true ∧
    (supports ⟨14,8,4,true,true,false,1,10⟩).contains (3,3) = true ∧
    (endpoints ⟨6,4,4,false,false,false,3,2⟩).contains (3,3) = true := by
  decide

theorem the_first_lower_pair_is_original_irregular_and_finally_nonfull :
    [(4,4),(4,5),(5,4),(5,5)].map allEndpoints.contains = [true,true,false,false] ∧
    [(4,4),(4,5),(5,4),(5,5)].map selected.contains = [false,false,false,false] ∧
    [(4,4),(4,5),(5,4),(5,5)].map
      (endpoints ⟨6,4,4,false,false,false,3,2⟩).contains = [true,true,false,false] ∧
    [(4,4),(4,5),(5,4),(5,5)].map
      (supports ⟨6,4,4,false,false,false,3,2⟩).contains = [false,false,false,false] := by
  decide

end SubQuorum.ShortNegativeSingletonWitness
