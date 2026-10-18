import Std

namespace StarForming.CubicPaddingRings

def highWeight (index : Fin 6) : Int :=
  match index.val with
  | 0 => 1
  | 3 => -1
  | 4 => 2
  | 5 => -2
  | _ => 0

def leafWeight (index : Fin 6) : Int :=
  match index.val with
  | 1 | 4 => -1
  | 2 | 5 => 1
  | _ => 0

def outsideWeight (index : Fin 6) : Int :=
  match index.val with
  | 0 => -1
  | 1 => 2
  | 2 => -2
  | 3 => 1
  | _ => 0

def cutFlux (index : Fin 6) (flux : Int) : Int :=
  match index.val with
  | 0 | 1 => -flux
  | 2 | 3 => flux
  | _ => 0

theorem periodic_weight_rows :
    (∀ index : Fin 6,
      highWeight (index + 5) + highWeight (index + 1) + leafWeight index +
        2 * highWeight index = 0 ∧
      outsideWeight (index + 5) + outsideWeight (index + 1) + leafWeight index +
        2 * outsideWeight index = 0 ∧
      highWeight index + outsideWeight index + 2 * leafWeight index = 0) ∧
    leafWeight 0 + leafWeight 2 + leafWeight 4 = 0 ∧
    leafWeight 1 + leafWeight 3 + leafWeight 5 = 0 := by
  decide

theorem cut_pair_weights :
    outsideWeight 0 + outsideWeight 1 = 1 ∧
      outsideWeight 2 + outsideWeight 3 = -1 := by
  decide

theorem periodic_balance_forces_zero_flux
    (high leaf outside : Nat → Int) (evenY oddY copies flux : Int)
    (hhigh : ∀ index : Fin 6,
      high ((index.val + 5) % 6) + high ((index.val + 1) % 6) + leaf index.val +
        2 * high index.val = 3 * copies)
    (hleaf : ∀ index : Fin 6,
      high index.val + outside index.val +
        (if index.val % 2 = 0 then evenY else oddY) + 2 * leaf index.val = 3 * copies)
    (houtside : ∀ index : Fin 6,
      outside ((index.val + 5) % 6) + outside ((index.val + 1) % 6) + leaf index.val +
        2 * outside index.val = 3 * copies + cutFlux index flux)
    (heven : leaf 0 + leaf 2 + leaf 4 + 2 * evenY = 3 * copies)
    (hodd : leaf 1 + leaf 3 + leaf 5 + 2 * oddY = 3 * copies) :
    flux = 0 := by
  have highZero := hhigh 0
  have highOne := hhigh 1
  have highTwo := hhigh 2
  have highThree := hhigh 3
  have highFour := hhigh 4
  have highFive := hhigh 5
  have leafZero := hleaf 0
  have leafOne := hleaf 1
  have leafTwo := hleaf 2
  have leafThree := hleaf 3
  have leafFour := hleaf 4
  have leafFive := hleaf 5
  have outsideZero := houtside 0
  have outsideOne := houtside 1
  have outsideTwo := houtside 2
  have outsideThree := houtside 3
  have outsideFour := houtside 4
  have outsideFive := houtside 5
  change high 5 + high 1 + leaf 0 + 2 * high 0 = 3 * copies at highZero
  change high 0 + high 2 + leaf 1 + 2 * high 1 = 3 * copies at highOne
  change high 1 + high 3 + leaf 2 + 2 * high 2 = 3 * copies at highTwo
  change high 2 + high 4 + leaf 3 + 2 * high 3 = 3 * copies at highThree
  change high 3 + high 5 + leaf 4 + 2 * high 4 = 3 * copies at highFour
  change high 4 + high 0 + leaf 5 + 2 * high 5 = 3 * copies at highFive
  change high 0 + outside 0 + evenY + 2 * leaf 0 = 3 * copies at leafZero
  change high 1 + outside 1 + oddY + 2 * leaf 1 = 3 * copies at leafOne
  change high 2 + outside 2 + evenY + 2 * leaf 2 = 3 * copies at leafTwo
  change high 3 + outside 3 + oddY + 2 * leaf 3 = 3 * copies at leafThree
  change high 4 + outside 4 + evenY + 2 * leaf 4 = 3 * copies at leafFour
  change high 5 + outside 5 + oddY + 2 * leaf 5 = 3 * copies at leafFive
  change outside 5 + outside 1 + leaf 0 + 2 * outside 0 = 3 * copies + -flux at outsideZero
  change outside 0 + outside 2 + leaf 1 + 2 * outside 1 = 3 * copies + -flux at outsideOne
  change outside 1 + outside 3 + leaf 2 + 2 * outside 2 = 3 * copies + flux at outsideTwo
  change outside 2 + outside 4 + leaf 3 + 2 * outside 3 = 3 * copies + flux at outsideThree
  change outside 3 + outside 5 + leaf 4 + 2 * outside 4 = 3 * copies + 0 at outsideFour
  change outside 4 + outside 0 + leaf 5 + 2 * outside 5 = 3 * copies + 0 at outsideFive
  omega

theorem four_port_deficiency
    (copies selected ports isolated complementEdges : Nat)
    (hidentity : 5 * selected + 4 + isolated + 2 * complementEdges = 60 * copies + 2 * ports)
    (hports : ports ≤ 4) :
    selected ≤ 12 * copies ∧
      (selected = 12 * copies → ports ≤ 2 →
        ports = 2 ∧ isolated = 0 ∧ complementEdges = 0) := by
  omega

theorem ring_parameter_accounting (blocks totalCore : Nat) :
    8 * blocks + 12 * totalCore = (7 * blocks + 12 * totalCore) + blocks ∧
      7 * (8 * blocks + 12 * totalCore) =
        3 * (14 * blocks + 20 * totalCore) + 2 * (7 * blocks + 12 * totalCore) := by
  omega

theorem compensation_matches_ring_upper (blocks totalCore upper : Nat)
    (hcompensation : 7 * upper ≤
      3 * (14 * blocks + 20 * totalCore) + 2 * (7 * blocks + 12 * totalCore)) :
    upper ≤ 8 * blocks + 12 * totalCore := by
  omega

theorem endpoint_padding_order (order size highCount : Nat)
    (heven : order % 2 = 0) (hendpoint : 5 * size = 3 * order)
    (hcycle : 4 ≤ highCount) (hleaves : 2 * highCount ≤ size) :
    20 ≤ order := by
  omega

end StarForming.CubicPaddingRings
