import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.CapRelayDistance

inductive Walk : Int → Int → Nat → Prop where
  | stay (start : Int) : Walk start start 0
  | left {start finish : Int} {count : Nat} (prior : Walk start finish count) :
      Walk start (finish - 1) (count + 1)
  | right {start finish : Int} {count : Nat} (prior : Walk start finish count) :
      Walk start (finish + 1) (count + 1)

theorem displacement_bound {start finish : Int} {count : Nat}
    (walk : Walk start finish count) :
    finish - start ≤ (count : Int) ∧ start - finish ≤ (count : Int) := by
  induction walk with
  | stay => omega
  | left prior hypothesis => omega
  | right prior hypothesis => omega

theorem left_route (start : Int) (count : Nat) :
    Walk start (start - (count : Int)) count := by
  induction count with
  | zero => simpa using Walk.stay start
  | succ count hypothesis =>
    have equality : start - ((count + 1 : Nat) : Int) = (start - (count : Int)) - 1 := by omega
    rw [equality]
    exact Walk.left hypothesis

theorem right_route (start : Int) (count : Nat) :
    Walk start (start + (count : Int)) count := by
  induction count with
  | zero => simpa using Walk.stay start
  | succ count hypothesis =>
    have equality : start + ((count + 1 : Nat) : Int) = (start + (count : Int)) + 1 := by omega
    rw [equality]
    exact Walk.right hypothesis

theorem exit_lower_bound {leftDepth rightDepth count : Nat} {finish : Int}
    (walk : Walk 0 finish count)
    (exit : finish = -(leftDepth : Int) ∨ finish = (rightDepth : Int)) :
    min leftDepth rightDepth ≤ count := by
  have bound := displacement_bound walk
  omega

theorem nearest_exit_attained (leftDepth rightDepth : Nat) :
    ∃ finish : Int, Walk 0 finish (min leftDepth rightDepth) ∧
      (finish = -(leftDepth : Int) ∨ finish = (rightDepth : Int)) := by
  by_cases comparison : leftDepth ≤ rightDepth
  · have route := left_route 0 leftDepth
    refine ⟨-(leftDepth : Int), ?_, Or.inl rfl⟩
    simpa [Nat.min_eq_left comparison] using route
  · have comparison' : rightDepth ≤ leftDepth := by omega
    have route := right_route 0 rightDepth
    refine ⟨(rightDepth : Int), ?_, Or.inr rfl⟩
    simpa [Nat.min_eq_right comparison'] using route

theorem two_corridor_lower_bound {upper lower rightDepth upperCount lowerCount : Nat}
    {upperFinish lowerFinish : Int}
    (upperWalk : Walk 0 upperFinish upperCount)
    (lowerWalk : Walk 0 lowerFinish lowerCount)
    (upperExit : upperFinish = -(upper : Int) ∨ upperFinish = 2)
    (lowerExit : lowerFinish = -(lower : Int) ∨ lowerFinish = (rightDepth : Int)) :
    min upper 2 + min lower rightDepth ≤ upperCount + lowerCount := by
  have upperBound := exit_lower_bound (rightDepth := 2) upperWalk upperExit
  have lowerBound := exit_lower_bound lowerWalk lowerExit
  omega

theorem fixed_height_unbounded_access {length upperCount lowerCount : Nat}
    {upperFinish lowerFinish : Int} (lengthBound : 3 ≤ length)
    (upperWalk : Walk 0 upperFinish upperCount)
    (lowerWalk : Walk 0 lowerFinish lowerCount)
    (upperExit : upperFinish = -(length : Int) ∨ upperFinish = 2)
    (lowerExit : lowerFinish = -(length : Int) ∨ lowerFinish = (length : Int)) :
    length + 2 ≤ upperCount + lowerCount := by
  have bound := two_corridor_lower_bound upperWalk lowerWalk upperExit lowerExit
  omega

end SubQuorum.CapRelayDistance

#print axioms SubQuorum.CapRelayDistance.displacement_bound
#print axioms SubQuorum.CapRelayDistance.left_route
#print axioms SubQuorum.CapRelayDistance.right_route
#print axioms SubQuorum.CapRelayDistance.exit_lower_bound
#print axioms SubQuorum.CapRelayDistance.nearest_exit_attained
#print axioms SubQuorum.CapRelayDistance.two_corridor_lower_bound
#print axioms SubQuorum.CapRelayDistance.fixed_height_unbounded_access
