import Std

namespace StarForming.CubicTriplePorts

theorem six_port_deficiency (selected ports isolated complementEdges : Nat)
    (hidentity : 5 * selected + 6 + isolated + 2 * complementEdges = 60 + 2 * ports)
    (hports : ports ≤ 6) :
    selected ≤ 13 ∧ (selected = 13 → ports = 6) := by
  omega

theorem hard_one_pair_case
    (high : Fin 6 → Nat) (leafZero leafOne leafTwo leafFive evenY oddY : Nat)
    (hhigh : ∀ index, high index ≤ 1)
    (hcap : high 0 + high 1 + high 2 + high 3 + high 4 + high 5 ≤ 4)
    (htriple : ∀ index : Fin 6, high index + high (index + 1) + high (index + 2) ≤ 2)
    (hleaf : leafZero ≤ 1 ∧ leafOne ≤ 1 ∧ leafTwo ≤ 1 ∧ leafFive ≤ 1)
    (hy : evenY ≤ 1 ∧ oddY ≤ 1)
    (htwoHigh : leafTwo + high 2 ≤ 1) (hfiveHigh : leafFive + high 5 ≤ 1)
    (htwoY : leafTwo + evenY ≤ 1) (hfiveY : leafFive + oddY ≤ 1)
    (hzeroCenter : leafZero + high 0 + evenY ≤ 2)
    (honeCenter : leafOne + high 1 + oddY ≤ 2)
    (hhighZero : high 0 + high 1 + leafZero ≤ 2) :
    high 0 + high 1 + high 2 + high 3 + high 4 + high 5 +
      leafZero + leafOne + leafTwo + leafFive + evenY + oddY ≤ 7 := by
  have highZero := hhigh 0
  have highOne := hhigh 1
  have highTwo := hhigh 2
  have highThree := hhigh 3
  have highFour := hhigh 4
  have highFive := hhigh 5
  have tripleOne := htriple 1
  have tripleTwo := htriple 2
  have tripleThree := htriple 3
  change high 1 + high 2 + high 3 ≤ 2 at tripleOne
  change high 2 + high 3 + high 4 ≤ 2 at tripleTwo
  change high 3 + high 4 + high 5 ≤ 2 at tripleThree
  have hevenCases : evenY = 0 ∨ evenY = 1 := by omega
  have hoddCases : oddY = 0 ∨ oddY = 1 := by omega
  rcases hevenCases with heven | heven <;>
    rcases hoddCases with hodd | hodd <;> omega

theorem two_omitted_pairs_deficiency (ports isolated complementEdges : Nat)
    (hidentity : 1 + isolated + 2 * complementEdges = 2 * ports)
    (hports : ports ≤ 2) (hcomplement : 1 ≤ complementEdges) :
    ports = 2 ∧ isolated = 1 ∧ complementEdges = 1 := by
  omega

theorem all_pairs_omitted_cap (selected isolated complementEdges : Nat)
    (hidentity : 5 * selected + 6 + isolated + 2 * complementEdges = 60)
    (hcomplement : 3 ≤ complementEdges) :
    selected ≤ 9 := by
  omega

theorem additive_omission_bound (selected omitted : Nat)
    (hcount : omitted ≤ 3) (hzero : selected ≤ 12)
    (hone : 1 ≤ omitted → selected ≤ 11)
    (htwo : 2 ≤ omitted → selected ≤ 10)
    (hthree : omitted = 3 → selected ≤ 9) :
    selected + omitted ≤ 12 := by
  omega

theorem two_obstruction_module_cap (first second core omitted : Nat)
    (hfirst : first ≤ 8) (hsecond : second ≤ 8)
    (homitted : (if first = 8 then 1 else 0) + (if second = 8 then 1 else 0) ≤ omitted)
    (hcore : core + omitted ≤ 12) :
    first + second + core ≤ 26 := by
  by_cases hfirstDense : first = 8 <;> by_cases hsecondDense : second = 8 <;>
    simp_all <;> omega

theorem ring_parameter_accounting (blocks : Nat) :
    28 * blocks = 26 * blocks + 2 * blocks ∧
      24 * (28 * blocks - 26 * blocks) = 48 * blocks ∧
      7 * (28 * blocks) = 3 * (48 * blocks) + 2 * (26 * blocks) := by
  omega

theorem compensation_matches_ring_upper (blocks upper : Nat)
    (hcompensation : 7 * upper ≤ 3 * (48 * blocks) + 2 * (26 * blocks)) :
    upper ≤ 28 * blocks := by
  omega

end StarForming.CubicTriplePorts
