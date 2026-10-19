import Std

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 5000000

namespace SubQuorum.MinusOneJointCompensation

abbrev Point := Int × Int

def ring : List Point :=
  [(-1,-1),(-1,0),(-1,1),(-1,2),(0,-1),(0,2),
   (1,-1),(1,2),(2,-1),(2,0),(2,1),(2,2)]

def sevenCore : List Point :=
  [(-1,-1),(-1,0),(-1,1),(-1,2),(0,-1),(1,-1),(2,-1)]

def orient (symmetry : Fin 8) (point : Point) : Point :=
  let row := if symmetry.val.testBit 1 then 1-point.1 else point.1
  let column := if symmetry.val.testBit 0 then 1-point.2 else point.2
  if symmetry.val.testBit 2 then (column,row) else (row,column)

def coreImage (symmetry : Fin 8) : List Point := sevenCore.map (orient symmetry)

theorem ring_size : ring.length = 12 := by decide

theorem core_size : ∀ symmetry : Fin 8, (coreImage symmetry).length = 7 := by decide

theorem core_inside_ring : ∀ symmetry : Fin 8,
    (coreImage symmetry).all ring.contains = true := by decide

theorem core_images_overlap : ∀ first second : Fin 8,
    (coreImage first).any (coreImage second).contains = true := by decide

theorem core_images_overlap_twice : ∀ first second : Fin 8,
    ((coreImage first).filter (coreImage second).contains).length ≥ 2 := by decide

theorem tip_predecessor_continuation : ∀ symmetry : Fin 8,
    let endpoint := orient symmetry (0,0)
    let selected := orient symmetry (1,0)
    (2*endpoint.1-selected.1, 2*endpoint.2-selected.2) =
      orient symmetry (-1,0) := by decide

def present (mask : Fin 16) (corner : Fin 4) : Bool := mask.val.testBit corner.val

def adjacent (first second : Fin 4) : Bool :=
  first.val ^^^ second.val == 1 || first.val ^^^ second.val == 2

def tip (axis : Bool) : Fin 4 := if axis then 1 else 2

def oldTipBlank (axis : Bool) (corner : Fin 4) : Bool :=
  adjacent (tip axis) corner && corner.val != 3

theorem tip_only_adjacent_blank : ∀ axis : Bool, ∀ corner : Fin 4,
    oldTipBlank axis corner = true → corner.val = 0 := by decide

def tipEvent (axis : Bool) (finalEndpoints : Fin 16) : Bool :=
  (List.finRange 4).any fun corner => oldTipBlank axis corner && present finalEndpoints corner

theorem blank_gate_excludes_tip_event : ∀ axis : Bool, ∀ finalEndpoints : Fin 16,
    present finalEndpoints 0 = false → tipEvent axis finalEndpoints = false := by decide

def countMask (mask : Fin 16) : Nat :=
  ((List.finRange 4).filter fun corner => present mask corner).length

theorem four_disjoint_slots : ∀ sideMask eventMask : Fin 16,
    (∀ corner : Fin 4, present sideMask corner && present eventMask corner = false) →
    countMask sideMask + countMask eventMask ≤ 4 := by decide

theorem joint_tax_bound (irregular tipEvents rotorEvents marked minusOne negativeRotors : Int)
    (hpartition : irregular = tipEvents+rotorEvents)
    (htips : tipEvents+marked ≤ 4*minusOne)
    (hrotors : rotorEvents ≤ 4*negativeRotors) :
    irregular+marked ≤ 4*minusOne+4*negativeRotors := by omega

theorem joint_slack_bound
    (slack positive negativeMass credit irregular marked minusOne negativeRotors : Int)
    (hbudget : positive+negativeMass+credit-irregular-marked ≤ slack)
    (hmass : negativeMass = minusOne+2*negativeRotors)
    (hjoint : irregular+marked ≤ 4*minusOne+4*negativeRotors) :
    positive-3*minusOne-2*negativeRotors+credit ≤ slack := by omega

theorem residual_sufficient (slack positive credit minusOne negativeRotors : Int)
    (hslack : positive-3*minusOne-2*negativeRotors+credit ≤ slack)
    (hcoverage : 3*minusOne+2*negativeRotors ≤ positive+credit) : 0 ≤ slack := by omega

theorem density_sufficient (slack positive credit minusOne negativeRotors : Int)
    (hslack : positive-3*minusOne-2*negativeRotors+credit ≤ slack)
    (hcredit : 0 ≤ credit)
    (hcoverage : 3*minusOne+2*negativeRotors ≤ positive) : 0 ≤ slack := by omega

theorem objective_bound (halfArea objective positive minusOne negativeRotors credit : Int)
    (hslack : positive-3*minusOne-2*negativeRotors+credit ≤ halfArea-objective) :
    objective ≤ halfArea-positive+3*minusOne+2*negativeRotors-credit := by omega

end SubQuorum.MinusOneJointCompensation
