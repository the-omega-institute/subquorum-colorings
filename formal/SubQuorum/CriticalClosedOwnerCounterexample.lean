import Std

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 4000000

namespace SubQuorum.CriticalClosedOwnerCounterexample

abbrev Point := Int × Int

structure Specification where
  width : Nat
  left : Nat
  right : Nat
  transpose : Bool
  flipRow : Bool
  flipColumn : Bool
  offset : Point
  deriving Inhabited

def specifications : List Specification :=
  [⟨26,12,4,false,false,false,(0,1)⟩,
   ⟨10,4,4,true,false,false,(1,3)⟩,
   ⟨6,4,4,true,true,false,(11,7)⟩,
   ⟨6,4,4,false,true,false,(8,8)⟩,
   ⟨8,6,6,false,false,false,(2,7)⟩,
   ⟨10,4,4,true,true,false,(1,20)⟩]

def move (specification : Specification) (point : Point) : Point :=
  let row := if specification.flipRow then -point.1 else point.1
  let column := if specification.flipColumn then -point.2 else point.2
  if specification.transpose then
    (column+specification.offset.1,row+specification.offset.2)
  else (row+specification.offset.1,column+specification.offset.2)

def canonicalMatching (specification : Specification) : List (Point × Point) :=
  ((List.range (specification.width/2)).map fun index =>
    ((0,Int.ofNat (1+2*index)),(0,Int.ofNat (2+2*index)))) ++
  ((List.range (specification.width/2-1)).map fun index =>
    ((1,Int.ofNat (2+2*index)),(1,Int.ofNat (3+2*index)))) ++
  ((List.range (specification.left/2)).map fun index =>
    ((Int.ofNat (1+2*index),1),(Int.ofNat (2+2*index),1))) ++
  ((List.range (specification.right/2)).map fun index =>
    ((Int.ofNat (1+2*index),Int.ofNat specification.width),
     (Int.ofNat (2+2*index),Int.ofNat specification.width)))

def canonicalSupport (specification : Specification) : List Point :=
  [(0,0),(0,Int.ofNat (specification.width+1)),
   (Int.ofNat (specification.left+1),1),
   (Int.ofNat (specification.right+1),Int.ofNat specification.width)] ++
  ((List.range (specification.left-1)).map fun index =>
    (Int.ofNat (index+2),if (index+2)%2 = 0 then 0 else 2)) ++
  ((List.range (specification.right-1)).map fun index =>
    (Int.ofNat (index+2),if (index+2)%2 = 0 then
      Int.ofNat (specification.width+1) else Int.ofNat (specification.width-1)))

def sourceMatching (specification : Specification) : List (Point × Point) :=
  (canonicalMatching specification).map fun edge =>
    (move specification edge.1,move specification edge.2)

def sourceEndpoints (specification : Specification) : List Point :=
  (sourceMatching specification).flatMap fun edge => [edge.1,edge.2]

def sourceSupport (specification : Specification) : List Point :=
  (canonicalSupport specification).map (move specification)

def matching : List (Point × Point) := specifications.flatMap sourceMatching

def endpoints : List Point := matching.flatMap fun edge => [edge.1,edge.2]

def selected : List Point :=
  ((specifications.flatMap sourceSupport).filter fun point =>
    !endpoints.contains point).eraseDups

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),
   (point.1,point.2-1),(point.1,point.2+1)]

def tileCells (origin : Point) : List Point :=
  [origin,(origin.1+1,origin.2),(origin.1,origin.2+1),
   (origin.1+1,origin.2+1)]

def tileOrigin (point : Point) : Point := (2*(point.1/2),2*(point.2/2))

def profile (origin : Point) : Nat × Nat :=
  ((tileCells origin).filter endpoints.contains |>.length,
   (tileCells origin).filter selected.contains |>.length)

def sourceProfile (specification : Specification) (origin : Point) : Nat × Nat :=
  ((tileCells origin).filter (sourceEndpoints specification).contains |>.length,
   (tileCells origin).filter (sourceSupport specification).contains |>.length)

def sourceCharge (specification : Specification) : Int :=
  let receivers := ((sourceEndpoints specification).map tileOrigin).eraseDups
  let retained := (sourceSupport specification).filter fun point =>
    receivers.contains (tileOrigin point)
  Int.ofNat retained.length+Int.ofNat (sourceMatching specification).length-
    2*Int.ofNat receivers.length

def inside (point : Point) : Bool :=
  decide (0 ≤ point.1 ∧ point.1 < 20 ∧ 0 ≤ point.2 ∧ point.2 < 30)

theorem source_dimensions_and_charges :
    (specifications.all fun specification => decide
      (6 ≤ specification.width ∧ 4 ≤ specification.left ∧ 4 ≤ specification.right ∧
       specification.width%2 = 0 ∧ specification.left%2 = 0 ∧
       specification.right%2 = 0)) = true ∧
    specifications.map sourceCharge = [-1,-9,-1,-5,-1,-9] := by decide

theorem complete_matching_and_retained_support_feasibility :
    endpoints.Nodup ∧ selected.Nodup ∧
    endpoints.all inside = true ∧ selected.all inside = true ∧
    (selected.all fun point => !endpoints.contains point) = true ∧
    (matching.all fun edge => (neighbors edge.1).contains edge.2) = true ∧
    (selected.all fun point => decide
      (((neighbors point).filter (endpoints ++ selected).contains).length ≤ 1)) = true ∧
    ((specifications.flatMap sourceSupport).all fun point =>
      endpoints.contains point || selected.contains point) = true := by decide

theorem exact_cardinalities :
    matching.length = 90 ∧ endpoints.length = 180 ∧ selected.length = 38 := by decide

theorem first_neutral_contact_and_phase_eleven_owner :
    move specifications[0]! (12,1) = (12,2) ∧
    move specifications[2]! (4,1) = (12,3) ∧
    profile (12,2) = (2,1) ∧
    (sourceSupport specifications[0]!).contains (11,3) = true ∧
    (sourceSupport specifications[2]!).contains (11,3) = true ∧
    move specifications[1]! (0,10) = (11,3) ∧
    sourceProfile specifications[1]! (10,4) = (3,0) ∧
    profile (10,2) = (4,0) := by decide

theorem critical_point_is_an_original_closed_owner_bar_corner :
    specifications[0]!.left = specifications[1]!.width+2 ∧
    move specifications[1]! (5,1) = (2,8) ∧
    (sourceSupport specifications[1]!).contains (2,8) = true ∧
    move specifications[4]! (0,1) = (2,8) ∧
    ((tileCells (2,8)).all (sourceEndpoints specifications[4]!).contains) = true ∧
    profile (2,8) = (4,0) ∧
    move specifications[4]! (6,1) ≠ (2,8) ∧
    move specifications[4]! (6,8) ≠ (2,8) := by decide

theorem both_phase_zero_one_terminals_have_neutral_contacts :
    move specifications[4]! (6,1) = (8,8) ∧
    move specifications[4]! (6,8) = (8,15) ∧
    move specifications[3]! (0,1) = (8,9) ∧
    move specifications[3]! (0,6) = (8,14) ∧
    profile (8,8) = (2,1) ∧ profile (8,14) = (2,1) ∧
    sourceProfile specifications[4]! (8,8) = (1,1) ∧
    sourceProfile specifications[4]! (8,14) = (1,1) ∧
    sourceProfile specifications[3]! (8,8) = (1,1) ∧
    sourceProfile specifications[3]! (8,14) = (1,1) ∧
    ((tileCells (8,8)).filter endpoints.contains) = [(8,8),(8,9)] ∧
    ((tileCells (8,14)).filter endpoints.contains) = [(8,14),(8,15)] := by decide

end SubQuorum.CriticalClosedOwnerCounterexample
