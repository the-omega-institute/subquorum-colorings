import SubQuorum.CriticalClosedOwnerCounterexample

set_option autoImplicit false
set_option maxRecDepth 1000000
set_option maxHeartbeats 12000000

namespace SubQuorum.DemandHullReserveObstruction

open CriticalClosedOwnerCounterexample

def core : List Specification :=
  [⟨20,24,22,false,false,false,(-22,-1)⟩,
   ⟨6,18,4,true,true,false,(1,19)⟩,
   ⟨28,20,4,true,true,true,(2,21)⟩,
   ⟨18,20,20,false,true,false,(0,0)⟩,
   ⟨6,4,4,true,true,false,(-8,15)⟩,
   ⟨14,4,4,true,false,true,(-1,6)⟩]

def restricted : List Specification := core.drop 3

def familyMatching (family : List Specification) : List (Point × Point) :=
  family.flatMap sourceMatching

def familyEndpoints (family : List Specification) : List Point :=
  family.flatMap sourceEndpoints

def familySelected (family : List Specification) : List Point :=
  ((family.flatMap sourceSupport).filter fun point =>
    !(familyEndpoints family).contains point).eraseDups

def familyOccupied (family : List Specification) : List Point :=
  familyEndpoints family ++ familySelected family

def completeFeasible (family : List Specification) : Prop :=
  (familyEndpoints family).Nodup ∧
  ((familyMatching family).all fun edge => (neighbors edge.1).contains edge.2) = true ∧
  ((familySelected family).all fun point => decide
    (((neighbors point).filter (familyOccupied family).contains).length = 1)) = true ∧
  ((familyEndpoints family).all fun point => decide
    (3 ≤ ((neighbors point).filter (familyOccupied family).contains).length)) = true ∧
  ((family.flatMap sourceSupport).all fun point =>
    (familyEndpoints family).contains point || (familySelected family).contains point) = true

def negativeMass (family : List Specification) : Nat :=
  (family.map fun specification => (-sourceCharge specification).toNat).sum

def mixedFullTiles (family : List Specification) : List Point :=
  (((familyEndpoints family).map tileOrigin).eraseDups).filter fun origin =>
    (tileCells origin).all (familyEndpoints family).contains &&
      !(family.any fun specification =>
        (tileCells origin).all (sourceEndpoints specification).contains)

def directedEvents (family : List Specification) : List (Nat × Point × Point) :=
  family.zipIdx |>.flatMap fun (specification, owner) =>
    (sourceEndpoints specification).flatMap fun point =>
      ((neighbors point).filter fun target =>
        (familyEndpoints family).contains target &&
        !(sourceEndpoints specification ++ sourceSupport specification).contains target &&
        tileOrigin point == tileOrigin target).map fun target => (owner, point, target)

def reserve (family : List Specification) : Int :=
  Int.ofNat (negativeMass family)+2*Int.ofNat (mixedFullTiles family).length-
    Int.ofNat (directedEvents family).length

theorem original_source_dimensions_and_charges :
    (core.all fun specification => decide
      (6 ≤ specification.width ∧ 4 ≤ specification.left ∧ 4 ≤ specification.right ∧
       specification.width%2 = 0 ∧ specification.left%2 = 0 ∧
       specification.right%2 = 0)) = true ∧
    core.map sourceCharge = [-1,-1,-1,-17,1,1] := by decide

theorem full_and_restricted_complete_feasibility :
    completeFeasible core ∧ completeFeasible restricted := by
  unfold completeFeasible
  decide

theorem exact_source_endpoint_matching_and_support_counts :
    (familyEndpoints core).length = 320 ∧ (familyMatching core).length = 160 ∧
    (familySelected core).length = 63 ∧
    (familyEndpoints restricted).length = 126 ∧ (familyMatching restricted).length = 63 ∧
    (familySelected restricted).length = 54 := by decide

theorem adjacent_positive_supports_have_the_same_forced_consumer :
    (sourceSupport core[4]!).contains (-1,11) = true ∧
    (sourceSupport core[5]!).contains (-1,10) = true ∧
    (neighbors (-1,11)).contains (-1,10) = true ∧
    ((neighbors (-1,11)).filter
      (sourceEndpoints core[4]! ++ sourceSupport core[4]!).contains) = [(-2,11)] ∧
    ((neighbors (-1,10)).filter
      (sourceEndpoints core[5]! ++ sourceSupport core[5]!).contains) = [(-2,10)] ∧
    (sourceEndpoints core[3]!).contains (-1,11) = true ∧
    (sourceEndpoints core[3]!).contains (-1,10) = true ∧
    (familySelected (core.drop 4)).contains (-1,11) = true ∧
    (familySelected (core.drop 4)).contains (-1,10) = true := by decide

theorem exact_original_source_event_and_tile_reserve_drop :
    negativeMass core = 20 ∧ (mixedFullTiles core).length = 35 ∧
    (directedEvents core).length = 85 ∧
    negativeMass restricted = 17 ∧ (mixedFullTiles restricted).length = 5 ∧
    (directedEvents restricted).length = 14 ∧
    reserve core = 5 ∧ reserve restricted = 13 ∧ reserve core < reserve restricted := by decide

end SubQuorum.DemandHullReserveObstruction
