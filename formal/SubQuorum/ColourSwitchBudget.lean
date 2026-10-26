import Lean.Elab.Tactic.Omega
set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0
namespace SubQuorum.ColourSwitchBudget

/-- Nonnegative local slacks. Geometry and actual-mate injection supply
    these premises in the written coordinate adapter. -/
structure BlackSlacks (t h : Nat → Nat → Int) : Prop where
  s0 : 0 ≤ (1 - (h 2 3))
  s1 : 0 ≤ (1 - (h 3 2))
  s2 : 0 ≤ (1 - (h 3 4))
  s3 : 0 ≤ (1 - (t 0 0))
  s4 : 0 ≤ (1 - (t 0 2))
  s5 : 0 ≤ (1 - (t 1 3))
  s6 : 0 ≤ (1 - (t 4 2))
  s7 : 0 ≤ (4 + (h 0 1) - (t 0 0) - (t 0 2) - (t 2 0) - (t 2 2) - (t 3 1))
  s8 : 0 ≤ (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))
  s9 : 0 ≤ (1 + (h 5 0) - (t 4 0) - (t 5 1))
  s10 : 0 ≤ (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 3 3) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))
  s11 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0))
  s12 : 0 ≤ ((h 0 1) + (h 0 3) - (t 0 2))
  s13 : 0 ≤ ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2))
  s14 : 0 ≤ ((h 0 1) + (h 1 2) - (t 0 2))
  s15 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2))
  s16 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4))
  s17 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))
  s18 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4))
  s19 : 0 ≤ ((h 0 5) + (h 0 7) - 2 * (t 0 6))
  s20 : 0 ≤ ((h 0 7) - (t 0 6))
  s21 : 0 ≤ ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))
  s22 : 0 ≤ ((h 0 3) + (h 1 4) - (t 1 3))
  s23 : 0 ≤ ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))
  s24 : 0 ≤ ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3))
  s25 : 0 ≤ ((h 1 0) - (t 2 0))
  s26 : 0 ≤ ((h 1 0) + (h 3 0) - 2 * (t 2 0))
  s27 : 0 ≤ ((h 3 0) - (t 2 0))
  s28 : 0 ≤ ((h 1 2) - (t 2 2))
  s29 : 0 ≤ ((h 1 2) + (h 2 3) - 2 * (t 2 2))
  s30 : 0 ≤ ((h 2 3) - (t 2 2))
  s31 : 0 ≤ ((h 2 3) + (h 3 2) - 2 * (t 2 2))
  s32 : 0 ≤ ((h 1 4) - (t 2 4))
  s33 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4))
  s34 : 0 ≤ ((h 1 4) + (h 2 3) + (h 3 4) - 3 * (t 2 4))
  s35 : 0 ≤ ((h 3 4) - (t 2 4))
  s36 : 0 ≤ ((h 3 0) - (t 3 1))
  s37 : 0 ≤ ((h 3 0) + (h 3 2) - 2 * (t 3 1))
  s38 : 0 ≤ ((h 3 0) + (h 4 1) - 2 * (t 3 1))
  s39 : 0 ≤ ((h 4 1) - (t 3 1))
  s40 : 0 ≤ ((h 2 3) + (h 3 2) - (t 3 3))
  s41 : 0 ≤ ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3))
  s42 : 0 ≤ ((h 3 0) + (h 4 1) - (t 4 0))
  s43 : 0 ≤ ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0))
  s44 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0))
  s45 : 0 ≤ ((h 3 2) + (h 4 1) + (h 4 3) - 2 * (t 4 2))
  s46 : 0 ≤ ((h 3 2) + (h 4 3) + (h 5 2) - 2 * (t 4 2))
  s47 : 0 ≤ ((h 4 1) + (h 4 3) - (t 4 2))
  s48 : 0 ≤ ((h 4 3) + (h 5 2) - (t 4 2))
  s49 : 0 ≤ ((h 3 4) + (h 4 3) + (h 5 4) - 3 * (t 4 4))
  s50 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1))
  s51 : 0 ≤ ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1))
  s52 : 0 ≤ ((h 4 1) + (h 5 2) - (t 5 1))
  s53 : 0 ≤ ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))
  s54 : 0 ≤ ((h 4 3) + (h 5 4) - (t 5 3))
  s55 : 0 ≤ ((h 5 2) + (h 5 4) - (t 5 3))
  s56 : 0 ≤ ((h 0 7))
  s57 : 0 ≤ ((h 5 4))

theorem black_case_1 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 1)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s11
    omega
  have hn0 : 0 ≤ 2 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2)) := by
    have := p.s15
    omega
  have hn1 : 0 ≤ 2 * ((h 0 3) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s16
    omega
  have hn2 : 0 ≤ 3 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := by
    have := p.s17
    omega
  have hn3 : 0 ≤ 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s20
    omega
  have hn4 : 0 ≤ 3 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := by
    have := p.s19
    omega
  have hn5 : 0 ≤ 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := by
    have := p.s23
    omega
  have hn6 : 0 ≤ 1 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s27
    omega
  have hn7 : 0 ≤ 2 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 2 3) - (t 2 2)) := by
    have := p.s30
    omega
  have hn8 : 0 ≤ 2 * ((h 2 3) - (t 2 2)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 1 4) - (t 2 4)) := by
    have := p.s32
    omega
  have hn9 : 0 ≤ 1 * ((h 1 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := by
    have := p.s33
    omega
  have hn10 : 0 ≤ 4 * ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 4 1) - (t 3 1)) := by
    have := p.s39
    omega
  have hn11 : 0 ≤ 2 * ((h 4 1) - (t 3 1)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 2 3) + (h 3 2) - (t 3 3)) := by
    have := p.s40
    omega
  have hn12 : 0 ≤ 2 * ((h 2 3) + (h 3 2) - (t 3 3)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ (- 3 + (h 3 4) + (h 4 3) + (h 5 4)) := by
    have := p.s49
    omega
  have hn13 : 0 ≤ 9 * (- 3 + (h 3 4) + (h 4 3) + (h 5 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s8
    omega
  have hn14 : 0 ≤ 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 3 3) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s10
    omega
  have hn15 : 0 ≤ 7 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 3 3) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 0 7)) := by
    have := p.s56
    omega
  have hn16 : 0 ≤ 3 * ((h 0 7)) := Int.mul_nonneg (by decide) hs16
  have htotal : 0 ≤ ((((((((((((((((2 * ((h 0 1) + (h 1 0) - (t 0 0)) + 2 * ((h 0 3) + (h 1 2) - (t 0 2))) + 3 * ((h 0 3) + (h 0 5) - (t 0 4))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 2 3) - (t 2 2))) + 1 * ((h 1 4) - (t 2 4))) + 4 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 2 * ((h 4 1) - (t 3 1))) + 2 * ((h 2 3) + (h 3 2) - (t 3 3))) + 9 * (- 3 + (h 3 4) + (h 4 3) + (h 5 4))) + 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 7 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 3 3) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 3 * ((h 0 7))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16)
  have identity : ((((((((((((((((2 * ((h 0 1) + (h 1 0) - (t 0 0)) + 2 * ((h 0 3) + (h 1 2) - (t 0 2))) + 3 * ((h 0 3) + (h 0 5) - (t 0 4))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 2 3) - (t 2 2))) + 1 * ((h 1 4) - (t 2 4))) + 4 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 2 * ((h 4 1) - (t 3 1))) + 2 * ((h 2 3) + (h 3 2) - (t 3 3))) + 9 * (- 3 + (h 3 4) + (h 4 3) + (h 5 4))) + 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 7 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 3 3) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 3 * ((h 0 7))) = 7 - 9 * (1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_case_2 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 0)
    (fix_t33 : t 3 3 = 0)
    (fix_h41 : h 4 1 = 0)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (t 0 0)) := by
    have := p.s3
    omega
  have hn0 : 0 ≤ 1 * (1 - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s11
    omega
  have hn1 : 0 ≤ 1 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2)) := by
    have := p.s13
    omega
  have hn2 : 0 ≤ 1 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := by
    have := p.s17
    omega
  have hn3 : 0 ≤ 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := by
    have := p.s19
    omega
  have hn4 : 0 ≤ 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := by
    have := p.s24
    omega
  have hn5 : 0 ≤ 1 * ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 1 0) - (t 2 0)) := by
    have := p.s25
    omega
  have hn6 : 0 ≤ 1 * ((h 1 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s27
    omega
  have hn7 : 0 ≤ 1 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 2 3) + (h 3 2) - 2 * (t 2 2)) := by
    have := p.s31
    omega
  have hn8 : 0 ≤ 1 * ((h 2 3) + (h 3 2) - 2 * (t 2 2)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 3 4) - (t 2 4)) := by
    have := p.s35
    omega
  have hn9 : 0 ≤ 2 * ((h 3 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ (- (t 3 1)) := by
    have := p.s39
    omega
  have hn10 : 0 ≤ 2 * (- (t 3 1)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 3 0) + (h 5 0) - 2 * (t 4 0)) := by
    have := p.s43
    omega
  have hn11 : 0 ≤ 1 * ((h 3 0) + (h 5 0) - 2 * (t 4 0)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 3 2) + (h 4 3) - 2 * (t 4 2)) := by
    have := p.s45
    omega
  have hn12 : 0 ≤ 1 * ((h 3 2) + (h 4 3) - 2 * (t 4 2)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 5 0) + (h 5 2) - 2 * (t 5 1)) := by
    have := p.s51
    omega
  have hn13 : 0 ≤ 1 * ((h 5 0) + (h 5 2) - 2 * (t 5 1)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := by
    have := p.s53
    omega
  have hn14 : 0 ≤ 1 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 0 7)) := by
    have := p.s56
    omega
  have hn15 : 0 ≤ 1 * ((h 0 7)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 5 4)) := by
    have := p.s57
    omega
  have hn16 : 0 ≤ 1 * ((h 5 4)) := Int.mul_nonneg (by decide) hs16
  have htotal : 0 ≤ ((((((((((((((((1 * (1 - (t 0 0)) + 1 * ((h 0 1) + (h 1 0) - (t 0 0))) + 1 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2))) + 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 1 * ((h 1 0) - (t 2 0))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 2 3) + (h 3 2) - 2 * (t 2 2))) + 2 * ((h 3 4) - (t 2 4))) + 2 * (- (t 3 1))) + 1 * ((h 3 0) + (h 5 0) - 2 * (t 4 0))) + 1 * ((h 3 2) + (h 4 3) - 2 * (t 4 2))) + 1 * ((h 5 0) + (h 5 2) - 2 * (t 5 1))) + 1 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 1 * ((h 0 7))) + 1 * ((h 5 4))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16)
  have identity : ((((((((((((((((1 * (1 - (t 0 0)) + 1 * ((h 0 1) + (h 1 0) - (t 0 0))) + 1 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2))) + 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 1 * ((h 1 0) - (t 2 0))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 2 3) + (h 3 2) - 2 * (t 2 2))) + 2 * ((h 3 4) - (t 2 4))) + 2 * (- (t 3 1))) + 1 * ((h 3 0) + (h 5 0) - 2 * (t 4 0))) + 1 * ((h 3 2) + (h 4 3) - 2 * (t 4 2))) + 1 * ((h 5 0) + (h 5 2) - 2 * (t 5 1))) + 1 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 1 * ((h 0 7))) + 1 * ((h 5 4))) = 1 - 2 * (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_case_3 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 0)
    (fix_t33 : t 3 3 = 0)
    (fix_h41 : h 4 1 = 1)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (t 0 0)) := by
    have := p.s3
    omega
  have hn0 : 0 ≤ 2 * (1 - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s11
    omega
  have hn1 : 0 ≤ 2 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2)) := by
    have := p.s13
    omega
  have hn2 : 0 ≤ 2 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4)) := by
    have := p.s18
    omega
  have hn3 : 0 ≤ 2 * ((h 0 5) + (h 1 4) - (t 0 4)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := by
    have := p.s17
    omega
  have hn4 : 0 ≤ 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s20
    omega
  have hn5 : 0 ≤ 2 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := by
    have := p.s19
    omega
  have hn6 : 0 ≤ 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ (1 - (t 1 3)) := by
    have := p.s5
    omega
  have hn7 : 0 ≤ 1 * (1 - (t 1 3)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3)) := by
    have := p.s21
    omega
  have hn8 : 0 ≤ 1 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 1 0) - (t 2 0)) := by
    have := p.s25
    omega
  have hn9 : 0 ≤ 2 * ((h 1 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s27
    omega
  have hn10 : 0 ≤ 2 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 2 3) - (t 2 2)) := by
    have := p.s30
    omega
  have hn11 : 0 ≤ 2 * ((h 2 3) - (t 2 2)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 1 2) + (h 2 3) - 2 * (t 2 2)) := by
    have := p.s29
    omega
  have hn12 : 0 ≤ 1 * ((h 1 2) + (h 2 3) - 2 * (t 2 2)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 3 4) - (t 2 4)) := by
    have := p.s35
    omega
  have hn13 : 0 ≤ 4 * ((h 3 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 3 0) + (h 3 2) - 2 * (t 3 1)) := by
    have := p.s37
    omega
  have hn14 : 0 ≤ 2 * ((h 3 0) + (h 3 2) - 2 * (t 3 1)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 3 2) + (h 4 3) + (h 5 2) - 2 * (t 4 2)) := by
    have := p.s46
    omega
  have hn15 : 0 ≤ 2 * ((h 3 2) + (h 4 3) + (h 5 2) - 2 * (t 4 2)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := by
    have := p.s53
    omega
  have hn16 : 0 ≤ 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ (1 + (h 5 0) - (t 4 0) - (t 5 1)) := by
    have := p.s9
    omega
  have hn17 : 0 ≤ 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ ((h 0 7)) := by
    have := p.s56
    omega
  have hn18 : 0 ≤ 1 * ((h 0 7)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 5 4)) := by
    have := p.s57
    omega
  have hn19 : 0 ≤ 2 * ((h 5 4)) := Int.mul_nonneg (by decide) hs19
  have htotal : 0 ≤ (((((((((((((((((((2 * (1 - (t 0 0)) + 2 * ((h 0 1) + (h 1 0) - (t 0 0))) + 2 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2))) + 2 * ((h 0 5) + (h 1 4) - (t 0 4))) + 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * (1 - (t 1 3))) + 1 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))) + 2 * ((h 1 0) - (t 2 0))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 2 3) - (t 2 2))) + 1 * ((h 1 2) + (h 2 3) - 2 * (t 2 2))) + 4 * ((h 3 4) - (t 2 4))) + 2 * ((h 3 0) + (h 3 2) - 2 * (t 3 1))) + 2 * ((h 3 2) + (h 4 3) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1))) + 1 * ((h 0 7))) + 2 * ((h 5 4))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19)
  have identity : (((((((((((((((((((2 * (1 - (t 0 0)) + 2 * ((h 0 1) + (h 1 0) - (t 0 0))) + 2 * ((h 0 1) + (h 0 3) + (h 1 2) - 2 * (t 0 2))) + 2 * ((h 0 5) + (h 1 4) - (t 0 4))) + 1 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 1 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 1 * (1 - (t 1 3))) + 1 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))) + 2 * ((h 1 0) - (t 2 0))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 2 3) - (t 2 2))) + 1 * ((h 1 2) + (h 2 3) - 2 * (t 2 2))) + 4 * ((h 3 4) - (t 2 4))) + 2 * ((h 3 0) + (h 3 2) - 2 * (t 3 1))) + 2 * ((h 3 2) + (h 4 3) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1))) + 1 * ((h 0 7))) + 2 * ((h 5 4))) = 3 - 4 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_case_4 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 0)
    (fix_t33 : t 3 3 = 1)
    (fix_t24 : t 2 4 = 0)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (t 0 0)) := by
    have := p.s3
    omega
  have hn0 : 0 ≤ 3 * (1 - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 0 3) - (t 0 2)) := by
    have := p.s12
    omega
  have hn1 : 0 ≤ 3 * ((h 0 1) + (h 0 3) - (t 0 2)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4)) := by
    have := p.s18
    omega
  have hn2 : 0 ≤ 3 * ((h 0 5) + (h 1 4) - (t 0 4)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := by
    have := p.s17
    omega
  have hn3 : 0 ≤ 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s20
    omega
  have hn4 : 0 ≤ 3 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := by
    have := p.s19
    omega
  have hn5 : 0 ≤ 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 3) + (h 1 4) - (t 1 3)) := by
    have := p.s22
    omega
  have hn6 : 0 ≤ 3 * ((h 0 3) + (h 1 4) - (t 1 3)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 1 0) - (t 2 0)) := by
    have := p.s25
    omega
  have hn7 : 0 ≤ 3 * ((h 1 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 1 2) - (t 2 2)) := by
    have := p.s28
    omega
  have hn8 : 0 ≤ 3 * ((h 1 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 3 0) - (t 3 1)) := by
    have := p.s36
    omega
  have hn9 : 0 ≤ 1 * ((h 3 0) - (t 3 1)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 3 0) + (h 4 1) - 2 * (t 3 1)) := by
    have := p.s38
    omega
  have hn10 : 0 ≤ 1 * ((h 3 0) + (h 4 1) - 2 * (t 3 1)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := by
    have := p.s41
    omega
  have hn11 : 0 ≤ 9 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 3 0) + (h 4 1) - (t 4 0)) := by
    have := p.s42
    omega
  have hn12 : 0 ≤ 1 * ((h 3 0) + (h 4 1) - (t 4 0)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ (1 - (t 4 2)) := by
    have := p.s6
    omega
  have hn13 : 0 ≤ 1 * (1 - (t 4 2)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s50
    omega
  have hn14 : 0 ≤ 1 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 5 2) + (h 5 4) - (t 5 3)) := by
    have := p.s55
    omega
  have hn15 : 0 ≤ 1 * ((h 5 2) + (h 5 4) - (t 5 3)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s8
    omega
  have hn16 : 0 ≤ 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s10
    omega
  have hn17 : 0 ≤ 6 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ (1 - (h 3 2)) := by
    have := p.s1
    omega
  have hn18 : 0 ≤ 6 * (1 - (h 3 2)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 0 7)) := by
    have := p.s56
    omega
  have hn19 : 0 ≤ 3 * ((h 0 7)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 5 4)) := by
    have := p.s57
    omega
  have hn20 : 0 ≤ 8 * ((h 5 4)) := Int.mul_nonneg (by decide) hs20
  have htotal : 0 ≤ ((((((((((((((((((((3 * (1 - (t 0 0)) + 3 * ((h 0 1) + (h 0 3) - (t 0 2))) + 3 * ((h 0 5) + (h 1 4) - (t 0 4))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 3 * ((h 0 3) + (h 1 4) - (t 1 3))) + 3 * ((h 1 0) - (t 2 0))) + 3 * ((h 1 2) - (t 2 2))) + 1 * ((h 3 0) - (t 3 1))) + 1 * ((h 3 0) + (h 4 1) - 2 * (t 3 1))) + 9 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 1 * ((h 3 0) + (h 4 1) - (t 4 0))) + 1 * (1 - (t 4 2))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 1 * ((h 5 2) + (h 5 4) - (t 5 3))) + 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 6 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 6 * (1 - (h 3 2))) + 3 * ((h 0 7))) + 8 * ((h 5 4))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20)
  have identity : ((((((((((((((((((((3 * (1 - (t 0 0)) + 3 * ((h 0 1) + (h 0 3) - (t 0 2))) + 3 * ((h 0 5) + (h 1 4) - (t 0 4))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 5) + (h 0 7) - 2 * (t 0 6))) + 3 * ((h 0 3) + (h 1 4) - (t 1 3))) + 3 * ((h 1 0) - (t 2 0))) + 3 * ((h 1 2) - (t 2 2))) + 1 * ((h 3 0) - (t 3 1))) + 1 * ((h 3 0) + (h 4 1) - 2 * (t 3 1))) + 9 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 1 * ((h 3 0) + (h 4 1) - (t 4 0))) + 1 * (1 - (t 4 2))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 1 * ((h 5 2) + (h 5 4) - (t 5 3))) + 2 * (2 + (h 5 0) + (h 5 2) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 6 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 4 1) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 6 * (1 - (h 3 2))) + 3 * ((h 0 7))) + 8 * ((h 5 4))) = 8 - 9 * (1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 3 1) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_case_5 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 0)
    (fix_t33 : t 3 3 = 1)
    (fix_t24 : t 2 4 = 1)
    (fix_h41 : h 4 1 = 0)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s11
    omega
  have hn0 : 0 ≤ 1 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ (1 - (t 0 2)) := by
    have := p.s4
    omega
  have hn1 : 0 ≤ 1 * (1 - (t 0 2)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s16
    omega
  have hn2 : 0 ≤ 3 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s20
    omega
  have hn3 : 0 ≤ 3 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ (1 - (t 1 3)) := by
    have := p.s5
    omega
  have hn4 : 0 ≤ 1 * (1 - (t 1 3)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s27
    omega
  have hn5 : 0 ≤ 1 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 1 2) - (t 2 2)) := by
    have := p.s28
    omega
  have hn6 : 0 ≤ 1 * ((h 1 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ (- 3 + (h 1 4) + (h 2 3) + (h 3 4)) := by
    have := p.s34
    omega
  have hn7 : 0 ≤ 3 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ (- (t 3 1)) := by
    have := p.s39
    omega
  have hn8 : 0 ≤ 1 * (- (t 3 1)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := by
    have := p.s41
    omega
  have hn9 : 0 ≤ 1 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 5 0) - (t 4 0)) := by
    have := p.s44
    omega
  have hn10 : 0 ≤ 1 * ((h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 4 3) - (t 4 2)) := by
    have := p.s47
    omega
  have hn11 : 0 ≤ 1 * ((h 4 3) - (t 4 2)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 5 2) - (t 5 1)) := by
    have := p.s52
    omega
  have hn12 : 0 ≤ 1 * ((h 5 2) - (t 5 1)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 4 3) + (h 5 4) - (t 5 3)) := by
    have := p.s54
    omega
  have hn13 : 0 ≤ 1 * ((h 4 3) + (h 5 4) - (t 5 3)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s10
    omega
  have hn14 : 0 ≤ 2 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ (1 - (h 2 3)) := by
    have := p.s0
    omega
  have hn15 : 0 ≤ 1 * (1 - (h 2 3)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (1 - (h 3 4)) := by
    have := p.s2
    omega
  have hn16 : 0 ≤ 1 * (1 - (h 3 4)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 5 4)) := by
    have := p.s57
    omega
  have hn17 : 0 ≤ 2 * ((h 5 4)) := Int.mul_nonneg (by decide) hs17
  have htotal : 0 ≤ (((((((((((((((((1 * ((h 0 1) + (h 1 0) - (t 0 0)) + 1 * (1 - (t 0 2))) + 3 * ((h 0 3) + (h 0 5) - (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 1 * (1 - (t 1 3))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 1 2) - (t 2 2))) + 3 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4))) + 1 * (- (t 3 1))) + 1 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 1 * ((h 5 0) - (t 4 0))) + 1 * ((h 4 3) - (t 4 2))) + 1 * ((h 5 2) - (t 5 1))) + 1 * ((h 4 3) + (h 5 4) - (t 5 3))) + 2 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 1 * (1 - (h 2 3))) + 1 * (1 - (h 3 4))) + 2 * ((h 5 4))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17)
  have identity : (((((((((((((((((1 * ((h 0 1) + (h 1 0) - (t 0 0)) + 1 * (1 - (t 0 2))) + 3 * ((h 0 3) + (h 0 5) - (t 0 4))) + 3 * ((h 0 7) - (t 0 6))) + 1 * (1 - (t 1 3))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 1 2) - (t 2 2))) + 3 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4))) + 1 * (- (t 3 1))) + 1 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 1 * ((h 5 0) - (t 4 0))) + 1 * ((h 4 3) - (t 4 2))) + 1 * ((h 5 2) - (t 5 1))) + 1 * ((h 4 3) + (h 5 4) - (t 5 3))) + 2 * (2 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 1 * (1 - (h 2 3))) + 1 * (1 - (h 3 4))) + 2 * ((h 5 4))) = 2 - 3 * (2 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 3 1) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_case_6 (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (fix_t44 : t 4 4 = 0)
    (fix_t33 : t 3 3 = 1)
    (fix_t24 : t 2 4 = 1)
    (fix_h41 : h 4 1 = 1)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (t 0 0)) := by
    have := p.s3
    omega
  have hn0 : 0 ≤ 1 * (1 - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s11
    omega
  have hn1 : 0 ≤ 2 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ (1 - (t 0 2)) := by
    have := p.s4
    omega
  have hn2 : 0 ≤ 2 * (1 - (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 1) + (h 1 2) - (t 0 2)) := by
    have := p.s14
    omega
  have hn3 : 0 ≤ 1 * ((h 0 1) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s16
    omega
  have hn4 : 0 ≤ 12 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s20
    omega
  have hn5 : 0 ≤ 12 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ (1 - (t 1 3)) := by
    have := p.s5
    omega
  have hn6 : 0 ≤ 4 * (1 - (t 1 3)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 1 0) - (t 2 0)) := by
    have := p.s25
    omega
  have hn7 : 0 ≤ 1 * ((h 1 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := by
    have := p.s26
    omega
  have hn8 : 0 ≤ 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 1 2) - (t 2 2)) := by
    have := p.s28
    omega
  have hn9 : 0 ≤ 3 * ((h 1 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ (- 3 + (h 1 4) + (h 2 3) + (h 3 4)) := by
    have := p.s34
    omega
  have hn10 : 0 ≤ 12 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 3 0) - (t 3 1)) := by
    have := p.s36
    omega
  have hn11 : 0 ≤ 3 * ((h 3 0) - (t 3 1)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := by
    have := p.s41
    omega
  have hn12 : 0 ≤ 4 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 4 3) + (h 5 2) - (t 4 2)) := by
    have := p.s48
    omega
  have hn13 : 0 ≤ 4 * ((h 4 3) + (h 5 2) - (t 4 2)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 4 3) + (h 5 4) - (t 5 3)) := by
    have := p.s54
    omega
  have hn14 : 0 ≤ 4 * ((h 4 3) + (h 5 4) - (t 5 3)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ (4 + (h 0 1) - (t 0 0) - (t 0 2) - (t 2 0) - (t 2 2) - (t 3 1)) := by
    have := p.s7
    omega
  have hn15 : 0 ≤ 1 * (4 + (h 0 1) - (t 0 0) - (t 0 2) - (t 2 0) - (t 2 2) - (t 3 1)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (1 + (h 5 0) - (t 4 0) - (t 5 1)) := by
    have := p.s9
    omega
  have hn16 : 0 ≤ 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := by
    have := p.s10
    omega
  have hn17 : 0 ≤ 8 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ (1 - (h 2 3)) := by
    have := p.s0
    omega
  have hn18 : 0 ≤ 4 * (1 - (h 2 3)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ (1 - (h 3 4)) := by
    have := p.s2
    omega
  have hn19 : 0 ≤ 4 * (1 - (h 3 4)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 5 4)) := by
    have := p.s57
    omega
  have hn20 : 0 ≤ 8 * ((h 5 4)) := Int.mul_nonneg (by decide) hs20
  have htotal : 0 ≤ ((((((((((((((((((((1 * (1 - (t 0 0)) + 2 * ((h 0 1) + (h 1 0) - (t 0 0))) + 2 * (1 - (t 0 2))) + 1 * ((h 0 1) + (h 1 2) - (t 0 2))) + 12 * ((h 0 3) + (h 0 5) - (t 0 4))) + 12 * ((h 0 7) - (t 0 6))) + 4 * (1 - (t 1 3))) + 1 * ((h 1 0) - (t 2 0))) + 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 3 * ((h 1 2) - (t 2 2))) + 12 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4))) + 3 * ((h 3 0) - (t 3 1))) + 4 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 4 * ((h 4 3) + (h 5 2) - (t 4 2))) + 4 * ((h 4 3) + (h 5 4) - (t 5 3))) + 1 * (4 + (h 0 1) - (t 0 0) - (t 0 2) - (t 2 0) - (t 2 2) - (t 3 1))) + 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1))) + 8 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 4 * (1 - (h 2 3))) + 4 * (1 - (h 3 4))) + 8 * ((h 5 4))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20)
  have identity : ((((((((((((((((((((1 * (1 - (t 0 0)) + 2 * ((h 0 1) + (h 1 0) - (t 0 0))) + 2 * (1 - (t 0 2))) + 1 * ((h 0 1) + (h 1 2) - (t 0 2))) + 12 * ((h 0 3) + (h 0 5) - (t 0 4))) + 12 * ((h 0 7) - (t 0 6))) + 4 * (1 - (t 1 3))) + 1 * ((h 1 0) - (t 2 0))) + 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 3 * ((h 1 2) - (t 2 2))) + 12 * (- 3 + (h 1 4) + (h 2 3) + (h 3 4))) + 3 * ((h 3 0) - (t 3 1))) + 4 * (- 3 + (h 2 3) + (h 3 2) + (h 3 4) + (h 4 3))) + 4 * ((h 4 3) + (h 5 2) - (t 4 2))) + 4 * ((h 4 3) + (h 5 4) - (t 5 3))) + 1 * (4 + (h 0 1) - (t 0 0) - (t 0 2) - (t 2 0) - (t 2 2) - (t 3 1))) + 4 * (1 + (h 5 0) - (t 4 0) - (t 5 1))) + 8 * (3 + (h 0 1) + (h 1 0) + (h 1 2) + (h 3 0) + (h 3 2) + (h 5 0) + (h 5 2) - (t 0 0) - (t 0 2) - (t 1 3) - (t 2 0) - (t 2 2) - (t 3 1) - (t 4 0) - (t 4 2) - (t 5 1) - (t 5 3))) + 4 * (1 - (h 2 3))) + 4 * (1 - (h 3 4))) + 8 * ((h 5 4))) = 11 - 12 * (1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 3 1) + (t 4 0) + (t 4 2) + (t 5 1) + (t 5 3)) := by omega
  rw [identity] at htotal
  omega

theorem black_local_budget (t h : Nat → Nat → Int) (p : BlackSlacks t h)
    (bit_h41 : 0 ≤ h 4 1 ∧ h 4 1 ≤ 1)
    (bit_t24 : 0 ≤ t 2 4 ∧ t 2 4 ≤ 1)
    (bit_t33 : 0 ≤ t 3 3 ∧ t 3 3 ≤ 1)
    (bit_t44 : 0 ≤ t 4 4 ∧ t 4 4 ≤ 1)
    : (- (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) - (h 5 4) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) ≤ 0 := by
  have split_t44 : t 4 4 = 0 ∨ t 4 4 = 1 := by omega
  rcases split_t44 with fix_t44 | fix_t44
  ·
    have split_t33 : t 3 3 = 0 ∨ t 3 3 = 1 := by omega
    rcases split_t33 with fix_t33 | fix_t33
    ·
      have split_h41 : h 4 1 = 0 ∨ h 4 1 = 1 := by omega
      rcases split_h41 with fix_h41 | fix_h41
      ·
        exact black_case_2 t h p fix_t44 fix_t33 fix_h41
      ·
        exact black_case_3 t h p fix_t44 fix_t33 fix_h41
    ·
      have split_t24 : t 2 4 = 0 ∨ t 2 4 = 1 := by omega
      rcases split_t24 with fix_t24 | fix_t24
      ·
        exact black_case_4 t h p fix_t44 fix_t33 fix_t24
      ·
        have split_h41 : h 4 1 = 0 ∨ h 4 1 = 1 := by omega
        rcases split_h41 with fix_h41 | fix_h41
        ·
          exact black_case_5 t h p fix_t44 fix_t33 fix_t24 fix_h41
        ·
          exact black_case_6 t h p fix_t44 fix_t33 fix_t24 fix_h41
  ·
    exact black_case_1 t h p fix_t44

/-- Nonnegative local slacks. Geometry and actual-mate injection supply
    these premises in the written coordinate adapter. -/
structure SwitchSlacks (t h : Nat → Nat → Int) : Prop where
  s0 : 0 ≤ (1 - (t 0 2))
  s1 : 0 ≤ (1 - (t 0 3))
  s2 : 0 ≤ (1 - (t 3 0))
  s3 : 0 ≤ (1 - (t 4 1))
  s4 : 0 ≤ (1 - (t 5 0))
  s5 : 0 ≤ (1 - (t 5 3))
  s6 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0))
  s7 : 0 ≤ ((h 0 1) + (h 0 3) - (t 0 2))
  s8 : 0 ≤ ((h 0 1) + (h 1 2) - (t 0 2))
  s9 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2))
  s10 : 0 ≤ ((h 0 2) + (h 0 4) + (h 1 3) - 2 * (t 0 3))
  s11 : 0 ≤ ((h 0 2) + (h 1 3) - (t 0 3))
  s12 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4))
  s13 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))
  s14 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4))
  s15 : 0 ≤ ((h 0 5) + (h 0 7) - (t 0 6))
  s16 : 0 ≤ ((h 0 0) + (h 2 0) - 2 * (t 1 0))
  s17 : 0 ≤ ((h 1 3) + (h 2 2) - 2 * (t 1 2))
  s18 : 0 ≤ ((h 0 3) + (h 1 2) - (t 1 3))
  s19 : 0 ≤ ((h 0 3) + (h 1 2) + (h 1 4) - 2 * (t 1 3))
  s20 : 0 ≤ ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))
  s21 : 0 ≤ ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))
  s22 : 0 ≤ ((h 1 2) + (h 1 4) + (h 2 3) - 2 * (t 1 3))
  s23 : 0 ≤ ((h 1 2) + (h 2 3) - (t 1 3))
  s24 : 0 ≤ ((h 1 3) + (h 2 4) - 2 * (t 1 4))
  s25 : 0 ≤ ((h 1 0) + (h 3 0) - 2 * (t 2 0))
  s26 : 0 ≤ ((h 1 2) + (h 3 2) - 2 * (t 2 2))
  s27 : 0 ≤ ((h 1 3) + (h 2 2) + (h 2 4) + (h 3 3) - 3 * (t 2 3))
  s28 : 0 ≤ ((h 1 3) + (h 2 4) - (t 2 3))
  s29 : 0 ≤ ((h 2 2) + (h 2 4) + (h 3 3) - 2 * (t 2 3))
  s30 : 0 ≤ ((h 2 2) + (h 3 3) - (t 2 3))
  s31 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4))
  s32 : 0 ≤ ((h 2 0) + (h 3 1) - (t 3 0))
  s33 : 0 ≤ ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0))
  s34 : 0 ≤ ((h 2 0) + (h 4 0) - (t 3 0))
  s35 : 0 ≤ ((h 3 1) + (h 4 0) - (t 3 0))
  s36 : 0 ≤ ((h 2 2) + (h 3 1) + (h 3 3) + (h 4 2) - 3 * (t 3 2))
  s37 : 0 ≤ ((h 2 3) + (h 3 2) - (t 3 3))
  s38 : 0 ≤ ((h 2 3) + (h 3 2) + (h 3 4) - 2 * (t 3 3))
  s39 : 0 ≤ ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3))
  s40 : 0 ≤ ((h 2 3) + (h 3 4) + (h 4 3) - 2 * (t 3 3))
  s41 : 0 ≤ ((h 2 4) + (h 3 3) - (t 3 4))
  s42 : 0 ≤ ((h 3 3) + (h 4 4) - 2 * (t 3 4))
  s43 : 0 ≤ ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0))
  s44 : 0 ≤ ((h 3 0) + (h 5 0) - (t 4 0))
  s45 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0))
  s46 : 0 ≤ ((h 3 1) + (h 4 0) + (h 4 2) + (h 5 1) - 3 * (t 4 1))
  s47 : 0 ≤ ((h 4 0) + (h 4 2) + (h 5 1) - 2 * (t 4 1))
  s48 : 0 ≤ ((h 3 2) + (h 4 1) - (t 4 2))
  s49 : 0 ≤ ((h 3 2) + (h 4 1) + (h 4 3) + (h 5 2) - 3 * (t 4 2))
  s50 : 0 ≤ ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2))
  s51 : 0 ≤ ((h 3 2) + (h 4 3) - (t 4 2))
  s52 : 0 ≤ ((h 4 1) + (h 4 3) + (h 5 2) - 2 * (t 4 2))
  s53 : 0 ≤ ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3))
  s54 : 0 ≤ ((h 3 3) + (h 4 4) - (t 4 3))
  s55 : 0 ≤ ((h 3 3) + (h 4 4) + (h 5 3) - 2 * (t 4 3))
  s56 : 0 ≤ ((h 3 4) + (h 4 3) - 2 * (t 4 4))
  s57 : 0 ≤ ((h 4 0) + (h 5 1) - (t 5 0))
  s58 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1))
  s59 : 0 ≤ ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1))
  s60 : 0 ≤ ((h 5 0) + (h 5 2) - (t 5 1))
  s61 : 0 ≤ ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))
  s62 : 0 ≤ ((h 4 2) + (h 5 3) - (t 5 2))
  s63 : 0 ≤ ((h 5 1) + (h 5 3) - (t 5 2))
  s64 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3))
  s65 : 0 ≤ ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))
  s66 : 0 ≤ ((h 0 0) - (t 0 1))
  s67 : 0 ≤ ((h 0 2) - (t 0 1))
  s68 : 0 ≤ ((h 0 7) - (t 0 6))
  s69 : 0 ≤ ((h 0 0) - (t 1 0))
  s70 : 0 ≤ ((h 2 0) - (t 1 0))
  s71 : 0 ≤ ((h 0 2) - (t 1 2))
  s72 : 0 ≤ ((h 1 3) - (t 1 2))
  s73 : 0 ≤ ((h 2 2) - (t 1 2))
  s74 : 0 ≤ ((h 1 3) - (t 1 4))
  s75 : 0 ≤ ((h 2 4) - (t 1 4))
  s76 : 0 ≤ ((h 1 0) - (t 2 0))
  s77 : 0 ≤ ((h 3 0) - (t 2 0))
  s78 : 0 ≤ ((h 2 0))
  s79 : 0 ≤ ((h 1 2) - (t 2 2))
  s80 : 0 ≤ ((h 2 3) - (t 2 2))
  s81 : 0 ≤ ((h 3 2) - (t 2 2))
  s82 : 0 ≤ ((h 1 4) - (t 2 4))
  s83 : 0 ≤ ((h 2 3) - (t 2 4))
  s84 : 0 ≤ ((h 3 4) - (t 2 4))
  s85 : 0 ≤ ((h 3 0) - (t 3 1))
  s86 : 0 ≤ ((h 3 2) - (t 3 1))
  s87 : 0 ≤ ((h 4 1) - (t 3 1))
  s88 : 0 ≤ ((h 4 4) - (t 3 4))
  s89 : 0 ≤ ((h 3 4) - (t 4 4))
  s90 : 0 ≤ ((h 4 3) - (t 4 4))
  s91 : 0 ≤ ((h 3 1))
  s92 : 0 ≤ ((h 5 3))
  s93 : 0 ≤ ((t 5 4))
  s94 : 0 ≤ (1 - (h 0 0) - (t 0 0))
  s95 : 0 ≤ (1 - (h 0 2) - (t 0 2))
  s96 : 0 ≤ (1 - (h 0 3) - (t 0 3))
  s97 : 0 ≤ (1 - (h 0 4) - (t 0 4))
  s98 : 0 ≤ (1 - (h 1 3) - (t 1 3))
  s99 : 0 ≤ (1 - (h 2 3) - (t 2 3))
  s100 : 0 ≤ (1 - (h 3 0) - (t 3 0))
  s101 : 0 ≤ (1 - (h 3 2) - (t 3 2))
  s102 : 0 ≤ (1 - (h 3 3) - (t 3 3))
  s103 : 0 ≤ (1 - (h 4 0) - (t 4 0))
  s104 : 0 ≤ (1 - (h 4 1) - (t 4 1))
  s105 : 0 ≤ (1 - (h 4 2) - (t 4 2))
  s106 : 0 ≤ (1 - (h 4 3) - (t 4 3))
  s107 : 0 ≤ (1 - (h 5 0) - (t 5 0))
  s108 : 0 ≤ (1 - (h 5 4) - (t 5 4))
  s109 : 0 ≤ (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))
  s110 : 0 ≤ (2 - (t 0 2) - (t 0 3) - (t 1 2) - (t 1 3))
  s111 : 0 ≤ (2 - (t 2 2) - (t 2 3) - (t 3 2) - (t 3 3))
  s112 : 0 ≤ (2 - (t 3 0) - (t 3 1) - (t 4 0) - (t 4 1))
  s113 : 0 ≤ (2 - (t 3 2) - (t 3 3) - (t 4 2) - (t 4 3))
  s114 : 0 ≤ (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))
  s115 : 0 ≤ (2 - (t 4 1) - (t 4 2) - (t 5 1) - (t 5 2))
  s116 : 0 ≤ (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))

theorem switch_case_1 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 0)
    (fix_t41 : t 4 1 = 0)
    (fix_h00 : h 0 0 = 0)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn0 : 0 ≤ 12 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ (- (t 0 1)) := by
    have := p.s66
    omega
  have hn1 : 0 ≤ 84 * (- (t 0 1)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2)) := by
    have := p.s9
    omega
  have hn2 : 0 ≤ 10 * ((h 0 3) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ (1 - (h 0 3) - (t 0 3)) := by
    have := p.s96
    omega
  have hn3 : 0 ≤ 15 * (1 - (h 0 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ (1 - (t 0 3)) := by
    have := p.s1
    omega
  have hn4 : 0 ≤ 17 * (1 - (t 0 3)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 2) + (h 1 3) - (t 0 3)) := by
    have := p.s11
    omega
  have hn5 : 0 ≤ 50 * ((h 0 2) + (h 1 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s12
    omega
  have hn6 : 0 ≤ 12 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn7 : 0 ≤ 12 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ (- (t 1 0)) := by
    have := p.s69
    omega
  have hn8 : 0 ≤ 84 * (- (t 1 0)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 0 2) - (t 1 2)) := by
    have := p.s71
    omega
  have hn9 : 0 ≤ 34 * ((h 0 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 2 2) - (t 1 2)) := by
    have := p.s73
    omega
  have hn10 : 0 ≤ 48 * ((h 2 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := by
    have := p.s21
    omega
  have hn11 : 0 ≤ 5 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := by
    have := p.s24
    omega
  have hn12 : 0 ≤ 34 * ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 2 4) - (t 1 4)) := by
    have := p.s75
    omega
  have hn13 : 0 ≤ 16 * ((h 2 4) - (t 1 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s77
    omega
  have hn14 : 0 ≤ 12 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 2 0)) := by
    have := p.s78
    omega
  have hn15 : 0 ≤ 12 * ((h 2 0)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 1 2) - (t 2 2)) := by
    have := p.s79
    omega
  have hn16 : 0 ≤ 2 * ((h 1 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 2 3) - (t 2 2)) := by
    have := p.s80
    omega
  have hn17 : 0 ≤ 10 * ((h 2 3) - (t 2 2)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ (1 - (h 2 3) - (t 2 3)) := by
    have := p.s99
    omega
  have hn18 : 0 ≤ 14 * (1 - (h 2 3) - (t 2 3)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 2 2) + (h 3 3) - (t 2 3)) := by
    have := p.s30
    omega
  have hn19 : 0 ≤ 2 * ((h 2 2) + (h 3 3) - (t 2 3)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 2 2) + (h 2 4) + (h 3 3) - 2 * (t 2 3)) := by
    have := p.s29
    omega
  have hn20 : 0 ≤ 34 * ((h 2 2) + (h 2 4) + (h 3 3) - 2 * (t 2 3)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := by
    have := p.s31
    omega
  have hn21 : 0 ≤ 5 * ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ ((h 1 4) - (t 2 4)) := by
    have := p.s82
    omega
  have hn22 : 0 ≤ 2 * ((h 1 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ ((h 2 0) + (h 3 1) - (t 3 0)) := by
    have := p.s32
    omega
  have hn23 : 0 ≤ 60 * ((h 2 0) + (h 3 1) - (t 3 0)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0)) := by
    have := p.s33
    omega
  have hn24 : 0 ≤ 12 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 3 1)) := by
    have := p.s91
    omega
  have hn25 : 0 ≤ 12 * ((h 3 1)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 3 2) - (t 3 1)) := by
    have := p.s86
    omega
  have hn26 : 0 ≤ 12 * ((h 3 2) - (t 3 1)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 2 3) + (h 3 4) + (h 4 3) - 2 * (t 3 3)) := by
    have := p.s40
    omega
  have hn27 : 0 ≤ 6 * ((h 2 3) + (h 3 4) + (h 4 3) - 2 * (t 3 3)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := by
    have := p.s42
    omega
  have hn28 : 0 ≤ 24 * ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn29 : 0 ≤ 36 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0)) := by
    have := p.s45
    omega
  have hn30 : 0 ≤ 12 * ((h 4 1) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3)) := by
    have := p.s53
    omega
  have hn31 : 0 ≤ 24 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3)) := Int.mul_nonneg (by decide) hs31
  have hs32 : 0 ≤ ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := by
    have := p.s56
    omega
  have hn32 : 0 ≤ 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := Int.mul_nonneg (by decide) hs32
  have hs33 : 0 ≤ (1 - (h 5 0) - (t 5 0)) := by
    have := p.s107
    omega
  have hn33 : 0 ≤ 12 * (1 - (h 5 0) - (t 5 0)) := Int.mul_nonneg (by decide) hs33
  have hs34 : 0 ≤ ((h 4 0) + (h 5 1) - (t 5 0)) := by
    have := p.s57
    omega
  have hn34 : 0 ≤ 72 * ((h 4 0) + (h 5 1) - (t 5 0)) := Int.mul_nonneg (by decide) hs34
  have hs35 : 0 ≤ ((h 5 0) + (h 5 2) - (t 5 1)) := by
    have := p.s60
    omega
  have hn35 : 0 ≤ 12 * ((h 5 0) + (h 5 2) - (t 5 1)) := Int.mul_nonneg (by decide) hs35
  have hs36 : 0 ≤ ((h 4 2) + (h 5 3) - (t 5 2)) := by
    have := p.s62
    omega
  have hn36 : 0 ≤ 48 * ((h 4 2) + (h 5 3) - (t 5 2)) := Int.mul_nonneg (by decide) hs36
  have hs37 : 0 ≤ ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := by
    have := p.s61
    omega
  have hn37 : 0 ≤ 12 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := Int.mul_nonneg (by decide) hs37
  have hs38 : 0 ≤ (2 - (t 0 2) - (t 0 3) - (t 1 2) - (t 1 3)) := by
    have := p.s110
    omega
  have hn38 : 0 ≤ 2 * (2 - (t 0 2) - (t 0 3) - (t 1 2) - (t 1 3)) := Int.mul_nonneg (by decide) hs38
  have hs39 : 0 ≤ (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := by
    have := p.s116
    omega
  have hn39 : 0 ≤ 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs39
  have hs40 : 0 ≤ (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn40 : 0 ≤ 12 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs40
  have htotal : 0 ≤ ((((((((((((((((((((((((((((((((((((((((12 * ((h 0 1) + (h 1 0) - (t 0 0)) + 84 * (- (t 0 1))) + 10 * ((h 0 3) + (h 1 2) - (t 0 2))) + 15 * (1 - (h 0 3) - (t 0 3))) + 17 * (1 - (t 0 3))) + 50 * ((h 0 2) + (h 1 3) - (t 0 3))) + 12 * ((h 0 3) + (h 0 5) - (t 0 4))) + 12 * ((h 0 7) - (t 0 6))) + 84 * (- (t 1 0))) + 34 * ((h 0 2) - (t 1 2))) + 48 * ((h 2 2) - (t 1 2))) + 5 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 34 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 16 * ((h 2 4) - (t 1 4))) + 12 * ((h 3 0) - (t 2 0))) + 12 * ((h 2 0))) + 2 * ((h 1 2) - (t 2 2))) + 10 * ((h 2 3) - (t 2 2))) + 14 * (1 - (h 2 3) - (t 2 3))) + 2 * ((h 2 2) + (h 3 3) - (t 2 3))) + 34 * ((h 2 2) + (h 2 4) + (h 3 3) - 2 * (t 2 3))) + 5 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 2 * ((h 1 4) - (t 2 4))) + 60 * ((h 2 0) + (h 3 1) - (t 3 0))) + 12 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0))) + 12 * ((h 3 1))) + 12 * ((h 3 2) - (t 3 1))) + 6 * ((h 2 3) + (h 3 4) + (h 4 3) - 2 * (t 3 3))) + 24 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 36 * ((h 4 4) - (t 3 4))) + 12 * ((h 4 1) + (h 5 0) - (t 4 0))) + 24 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3))) + 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 12 * (1 - (h 5 0) - (t 5 0))) + 72 * ((h 4 0) + (h 5 1) - (t 5 0))) + 12 * ((h 5 0) + (h 5 2) - (t 5 1))) + 48 * ((h 4 2) + (h 5 3) - (t 5 2))) + 12 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 2 * (2 - (t 0 2) - (t 0 3) - (t 1 2) - (t 1 3))) + 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 12 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31) hn32) hn33) hn34) hn35) hn36) hn37) hn38) hn39) hn40)
  have identity : ((((((((((((((((((((((((((((((((((((((((12 * ((h 0 1) + (h 1 0) - (t 0 0)) + 84 * (- (t 0 1))) + 10 * ((h 0 3) + (h 1 2) - (t 0 2))) + 15 * (1 - (h 0 3) - (t 0 3))) + 17 * (1 - (t 0 3))) + 50 * ((h 0 2) + (h 1 3) - (t 0 3))) + 12 * ((h 0 3) + (h 0 5) - (t 0 4))) + 12 * ((h 0 7) - (t 0 6))) + 84 * (- (t 1 0))) + 34 * ((h 0 2) - (t 1 2))) + 48 * ((h 2 2) - (t 1 2))) + 5 * ((h 0 3) + (h 1 4) + (h 2 3) - 2 * (t 1 3))) + 34 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 16 * ((h 2 4) - (t 1 4))) + 12 * ((h 3 0) - (t 2 0))) + 12 * ((h 2 0))) + 2 * ((h 1 2) - (t 2 2))) + 10 * ((h 2 3) - (t 2 2))) + 14 * (1 - (h 2 3) - (t 2 3))) + 2 * ((h 2 2) + (h 3 3) - (t 2 3))) + 34 * ((h 2 2) + (h 2 4) + (h 3 3) - 2 * (t 2 3))) + 5 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 2 * ((h 1 4) - (t 2 4))) + 60 * ((h 2 0) + (h 3 1) - (t 3 0))) + 12 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0))) + 12 * ((h 3 1))) + 12 * ((h 3 2) - (t 3 1))) + 6 * ((h 2 3) + (h 3 4) + (h 4 3) - 2 * (t 3 3))) + 24 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 36 * ((h 4 4) - (t 3 4))) + 12 * ((h 4 1) + (h 5 0) - (t 4 0))) + 24 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3))) + 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 12 * (1 - (h 5 0) - (t 5 0))) + 72 * ((h 4 0) + (h 5 1) - (t 5 0))) + 12 * ((h 5 0) + (h 5 2) - (t 5 1))) + 48 * ((h 4 2) + (h 5 3) - (t 5 2))) + 12 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 2 * (2 - (t 0 2) - (t 0 3) - (t 1 2) - (t 1 3))) + 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 12 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 74 - 84 * (- (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_2 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 0)
    (fix_t41 : t 4 1 = 0)
    (fix_h00 : h 0 0 = 1)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ (- (t 0 0)) := by
    have := p.s94
    omega
  have hn0 : 0 ≤ 18 * (- (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 2) - (t 0 1)) := by
    have := p.s67
    omega
  have hn1 : 0 ≤ 27 * ((h 0 2) - (t 0 1)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 1) + (h 0 3) - (t 0 2)) := by
    have := p.s7
    omega
  have hn2 : 0 ≤ 18 * ((h 0 1) + (h 0 3) - (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ (1 - (h 0 3) - (t 0 3)) := by
    have := p.s96
    omega
  have hn3 : 0 ≤ 24 * (1 - (h 0 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ (1 - (t 0 3)) := by
    have := p.s1
    omega
  have hn4 : 0 ≤ 3 * (1 - (t 0 3)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s12
    omega
  have hn5 : 0 ≤ 18 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn6 : 0 ≤ 18 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 2 0) - (t 1 0)) := by
    have := p.s70
    omega
  have hn7 : 0 ≤ 27 * ((h 2 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 1 3) + (h 2 2) - 2 * (t 1 2)) := by
    have := p.s17
    omega
  have hn8 : 0 ≤ 9 * ((h 1 3) + (h 2 2) - 2 * (t 1 2)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 2 2) - (t 1 2)) := by
    have := p.s73
    omega
  have hn9 : 0 ≤ 9 * ((h 2 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3)) := by
    have := p.s20
    omega
  have hn10 : 0 ≤ 6 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := by
    have := p.s24
    omega
  have hn11 : 0 ≤ 9 * ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 2 4) - (t 1 4)) := by
    have := p.s75
    omega
  have hn12 : 0 ≤ 9 * ((h 2 4) - (t 1 4)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 1 0) - (t 2 0)) := by
    have := p.s76
    omega
  have hn13 : 0 ≤ 18 * ((h 1 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 1 2) + (h 3 2) - 2 * (t 2 2)) := by
    have := p.s26
    omega
  have hn14 : 0 ≤ 6 * ((h 1 2) + (h 3 2) - 2 * (t 2 2)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 1 2) - (t 2 2)) := by
    have := p.s79
    omega
  have hn15 : 0 ≤ 6 * ((h 1 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 1 3) + (h 2 2) + (h 2 4) + (h 3 3) - 3 * (t 2 3)) := by
    have := p.s27
    omega
  have hn16 : 0 ≤ 9 * ((h 1 3) + (h 2 2) + (h 2 4) + (h 3 3) - 3 * (t 2 3)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := by
    have := p.s31
    omega
  have hn17 : 0 ≤ 6 * ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ ((h 1 4) - (t 2 4)) := by
    have := p.s82
    omega
  have hn18 : 0 ≤ 6 * ((h 1 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 3 1) + (h 4 0) - (t 3 0)) := by
    have := p.s35
    omega
  have hn19 : 0 ≤ 27 * ((h 3 1) + (h 4 0) - (t 3 0)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 3 0) - (t 3 1)) := by
    have := p.s85
    omega
  have hn20 : 0 ≤ 18 * ((h 3 0) - (t 3 1)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3)) := by
    have := p.s39
    omega
  have hn21 : 0 ≤ 6 * ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := by
    have := p.s42
    omega
  have hn22 : 0 ≤ 9 * ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn23 : 0 ≤ 9 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ (1 - (h 4 0) - (t 4 0)) := by
    have := p.s103
    omega
  have hn24 : 0 ≤ 18 * (1 - (h 4 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2)) := by
    have := p.s50
    omega
  have hn25 : 0 ≤ 4 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 4 1) + (h 4 3) + (h 5 2) - 2 * (t 4 2)) := by
    have := p.s52
    omega
  have hn26 : 0 ≤ 2 * ((h 4 1) + (h 4 3) + (h 5 2) - 2 * (t 4 2)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 3 2) + (h 4 1) + (h 4 3) + (h 5 2) - 3 * (t 4 2)) := by
    have := p.s49
    omega
  have hn27 : 0 ≤ 2 * ((h 3 2) + (h 4 1) + (h 4 3) + (h 5 2) - 3 * (t 4 2)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3)) := by
    have := p.s53
    omega
  have hn28 : 0 ≤ 9 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := by
    have := p.s56
    omega
  have hn29 : 0 ≤ 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ ((h 3 4) - (t 4 4)) := by
    have := p.s89
    omega
  have hn30 : 0 ≤ 6 * ((h 3 4) - (t 4 4)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ (1 - (t 5 0)) := by
    have := p.s4
    omega
  have hn31 : 0 ≤ 9 * (1 - (t 5 0)) := Int.mul_nonneg (by decide) hs31
  have hs32 : 0 ≤ ((h 4 0) + (h 5 1) - (t 5 0)) := by
    have := p.s57
    omega
  have hn32 : 0 ≤ 18 * ((h 4 0) + (h 5 1) - (t 5 0)) := Int.mul_nonneg (by decide) hs32
  have hs33 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s58
    omega
  have hn33 : 0 ≤ 10 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs33
  have hs34 : 0 ≤ ((h 5 0) + (h 5 2) - (t 5 1)) := by
    have := p.s60
    omega
  have hn34 : 0 ≤ 8 * ((h 5 0) + (h 5 2) - (t 5 1)) := Int.mul_nonneg (by decide) hs34
  have hs35 : 0 ≤ ((h 4 2) + (h 5 3) - (t 5 2)) := by
    have := p.s62
    omega
  have hn35 : 0 ≤ 9 * ((h 4 2) + (h 5 3) - (t 5 2)) := Int.mul_nonneg (by decide) hs35
  have hs36 : 0 ≤ ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := by
    have := p.s61
    omega
  have hn36 : 0 ≤ 9 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := Int.mul_nonneg (by decide) hs36
  have hs37 : 0 ≤ (1 - (t 5 3)) := by
    have := p.s5
    omega
  have hn37 : 0 ≤ 14 * (1 - (t 5 3)) := Int.mul_nonneg (by decide) hs37
  have hs38 : 0 ≤ ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := by
    have := p.s65
    omega
  have hn38 : 0 ≤ 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3)) := Int.mul_nonneg (by decide) hs38
  have hs39 : 0 ≤ (1 - (h 5 4) - (t 5 4)) := by
    have := p.s108
    omega
  have hn39 : 0 ≤ 2 * (1 - (h 5 4) - (t 5 4)) := Int.mul_nonneg (by decide) hs39
  have hs40 : 0 ≤ ((t 5 4)) := by
    have := p.s93
    omega
  have hn40 : 0 ≤ 2 * ((t 5 4)) := Int.mul_nonneg (by decide) hs40
  have hs41 : 0 ≤ (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn41 : 0 ≤ 18 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs41
  have htotal : 0 ≤ (((((((((((((((((((((((((((((((((((((((((18 * (- (t 0 0)) + 27 * ((h 0 2) - (t 0 1))) + 18 * ((h 0 1) + (h 0 3) - (t 0 2))) + 24 * (1 - (h 0 3) - (t 0 3))) + 3 * (1 - (t 0 3))) + 18 * ((h 0 3) + (h 0 5) - (t 0 4))) + 18 * ((h 0 7) - (t 0 6))) + 27 * ((h 2 0) - (t 1 0))) + 9 * ((h 1 3) + (h 2 2) - 2 * (t 1 2))) + 9 * ((h 2 2) - (t 1 2))) + 6 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))) + 9 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 9 * ((h 2 4) - (t 1 4))) + 18 * ((h 1 0) - (t 2 0))) + 6 * ((h 1 2) + (h 3 2) - 2 * (t 2 2))) + 6 * ((h 1 2) - (t 2 2))) + 9 * ((h 1 3) + (h 2 2) + (h 2 4) + (h 3 3) - 3 * (t 2 3))) + 6 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 6 * ((h 1 4) - (t 2 4))) + 27 * ((h 3 1) + (h 4 0) - (t 3 0))) + 18 * ((h 3 0) - (t 3 1))) + 6 * ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3))) + 9 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 9 * ((h 4 4) - (t 3 4))) + 18 * (1 - (h 4 0) - (t 4 0))) + 4 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 4 1) + (h 4 3) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 3 2) + (h 4 1) + (h 4 3) + (h 5 2) - 3 * (t 4 2))) + 9 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3))) + 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 6 * ((h 3 4) - (t 4 4))) + 9 * (1 - (t 5 0))) + 18 * ((h 4 0) + (h 5 1) - (t 5 0))) + 10 * ((h 4 1) + (h 5 0) - (t 5 1))) + 8 * ((h 5 0) + (h 5 2) - (t 5 1))) + 9 * ((h 4 2) + (h 5 3) - (t 5 2))) + 9 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 14 * (1 - (t 5 3))) + 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 2 * (1 - (h 5 4) - (t 5 4))) + 2 * ((t 5 4))) + 18 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31) hn32) hn33) hn34) hn35) hn36) hn37) hn38) hn39) hn40) hn41)
  have identity : (((((((((((((((((((((((((((((((((((((((((18 * (- (t 0 0)) + 27 * ((h 0 2) - (t 0 1))) + 18 * ((h 0 1) + (h 0 3) - (t 0 2))) + 24 * (1 - (h 0 3) - (t 0 3))) + 3 * (1 - (t 0 3))) + 18 * ((h 0 3) + (h 0 5) - (t 0 4))) + 18 * ((h 0 7) - (t 0 6))) + 27 * ((h 2 0) - (t 1 0))) + 9 * ((h 1 3) + (h 2 2) - 2 * (t 1 2))) + 9 * ((h 2 2) - (t 1 2))) + 6 * ((h 0 3) + (h 1 2) + (h 1 4) + (h 2 3) - 3 * (t 1 3))) + 9 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 9 * ((h 2 4) - (t 1 4))) + 18 * ((h 1 0) - (t 2 0))) + 6 * ((h 1 2) + (h 3 2) - 2 * (t 2 2))) + 6 * ((h 1 2) - (t 2 2))) + 9 * ((h 1 3) + (h 2 2) + (h 2 4) + (h 3 3) - 3 * (t 2 3))) + 6 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 6 * ((h 1 4) - (t 2 4))) + 27 * ((h 3 1) + (h 4 0) - (t 3 0))) + 18 * ((h 3 0) - (t 3 1))) + 6 * ((h 2 3) + (h 3 2) + (h 3 4) + (h 4 3) - 3 * (t 3 3))) + 9 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 9 * ((h 4 4) - (t 3 4))) + 18 * (1 - (h 4 0) - (t 4 0))) + 4 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 4 1) + (h 4 3) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 3 2) + (h 4 1) + (h 4 3) + (h 5 2) - 3 * (t 4 2))) + 9 * ((h 3 3) + (h 4 2) + (h 4 4) + (h 5 3) - 3 * (t 4 3))) + 6 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 6 * ((h 3 4) - (t 4 4))) + 9 * (1 - (t 5 0))) + 18 * ((h 4 0) + (h 5 1) - (t 5 0))) + 10 * ((h 4 1) + (h 5 0) - (t 5 1))) + 8 * ((h 5 0) + (h 5 2) - (t 5 1))) + 9 * ((h 4 2) + (h 5 3) - (t 5 2))) + 9 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 14 * (1 - (t 5 3))) + 2 * ((h 4 3) + (h 5 2) + (h 5 4) - 2 * (t 5 3))) + 2 * (1 - (h 5 4) - (t 5 4))) + 2 * ((t 5 4))) + 18 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 25 - 27 * (- 1 - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_3 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 0)
    (fix_t41 : t 4 1 = 1)
    (fix_h23 : h 2 3 = 0)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn0 : 0 ≤ 6 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 0) - (t 0 1)) := by
    have := p.s66
    omega
  have hn1 : 0 ≤ 2 * ((h 0 0) - (t 0 1)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ (1 - (h 0 2) - (t 0 2)) := by
    have := p.s95
    omega
  have hn2 : 0 ≤ 2 * (1 - (h 0 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ (1 - (t 0 2)) := by
    have := p.s0
    omega
  have hn3 : 0 ≤ 1 * (1 - (t 0 2)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2)) := by
    have := p.s9
    omega
  have hn4 : 0 ≤ 3 * ((h 0 3) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 2) + (h 1 3) - (t 0 3)) := by
    have := p.s11
    omega
  have hn5 : 0 ≤ 2 * ((h 0 2) + (h 1 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := by
    have := p.s13
    omega
  have hn6 : 0 ≤ 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 0 5) + (h 0 7) - (t 0 6)) := by
    have := p.s15
    omega
  have hn7 : 0 ≤ 3 * ((h 0 5) + (h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn8 : 0 ≤ 3 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 2 0) - (t 1 0)) := by
    have := p.s70
    omega
  have hn9 : 0 ≤ 2 * ((h 2 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 0 2) - (t 1 2)) := by
    have := p.s71
    omega
  have hn10 : 0 ≤ 2 * ((h 0 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 1 2) + (h 1 4) - 2 * (t 1 3)) := by
    have := p.s22
    omega
  have hn11 : 0 ≤ 3 * ((h 1 2) + (h 1 4) - 2 * (t 1 3)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 2 4) - (t 1 4)) := by
    have := p.s75
    omega
  have hn12 : 0 ≤ 2 * ((h 2 4) - (t 1 4)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s77
    omega
  have hn13 : 0 ≤ 6 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ (- (t 2 2)) := by
    have := p.s80
    omega
  have hn14 : 0 ≤ 6 * (- (t 2 2)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 2 2) + (h 3 3) - (t 2 3)) := by
    have := p.s30
    omega
  have hn15 : 0 ≤ 2 * ((h 2 2) + (h 3 3) - (t 2 3)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (- (t 2 4)) := by
    have := p.s83
    omega
  have hn16 : 0 ≤ 6 * (- (t 2 4)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 4 1) - (t 3 1)) := by
    have := p.s87
    omega
  have hn17 : 0 ≤ 4 * ((h 4 1) - (t 3 1)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ ((h 3 2) - (t 3 3)) := by
    have := p.s37
    omega
  have hn18 : 0 ≤ 2 * ((h 3 2) - (t 3 3)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 3 2) + (h 3 4) - 2 * (t 3 3)) := by
    have := p.s38
    omega
  have hn19 : 0 ≤ 2 * ((h 3 2) + (h 3 4) - 2 * (t 3 3)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn20 : 0 ≤ 2 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0)) := by
    have := p.s45
    omega
  have hn21 : 0 ≤ 2 * ((h 4 1) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ (- (h 4 1)) := by
    have := p.s104
    omega
  have hn22 : 0 ≤ 6 * (- (h 4 1)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1)) := by
    have := p.s46
    omega
  have hn23 : 0 ≤ 2 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2)) := by
    have := p.s50
    omega
  have hn24 : 0 ≤ 2 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := by
    have := p.s56
    omega
  have hn25 : 0 ≤ 2 * ((h 3 4) + (h 4 3) - 2 * (t 4 4)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 3 4) - (t 4 4)) := by
    have := p.s89
    omega
  have hn26 : 0 ≤ 2 * ((h 3 4) - (t 4 4)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s58
    omega
  have hn27 : 0 ≤ 4 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 5 3)) := by
    have := p.s92
    omega
  have hn28 : 0 ≤ 2 * ((h 5 3)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3)) := by
    have := p.s64
    omega
  have hn29 : 0 ≤ 4 * ((h 4 3) + (h 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ (1 - (t 3 0) - (t 3 1) - (t 4 0)) := by
    have := p.s112
    omega
  have hn30 : 0 ≤ 2 * (1 - (t 3 0) - (t 3 1) - (t 4 0)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ (1 - (t 4 0) - (t 5 0) - (t 5 1)) := by
    have := p.s114
    omega
  have hn31 : 0 ≤ 2 * (1 - (t 4 0) - (t 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs31
  have hs32 : 0 ≤ (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := by
    have := p.s116
    omega
  have hn32 : 0 ≤ 2 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs32
  have hs33 : 0 ≤ (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn33 : 0 ≤ 6 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs33
  have htotal : 0 ≤ (((((((((((((((((((((((((((((((((6 * ((h 0 1) + (h 1 0) - (t 0 0)) + 2 * ((h 0 0) - (t 0 1))) + 2 * (1 - (h 0 2) - (t 0 2))) + 1 * (1 - (t 0 2))) + 3 * ((h 0 3) + (h 1 2) - (t 0 2))) + 2 * ((h 0 2) + (h 1 3) - (t 0 3))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 5) + (h 0 7) - (t 0 6))) + 3 * ((h 0 7) - (t 0 6))) + 2 * ((h 2 0) - (t 1 0))) + 2 * ((h 0 2) - (t 1 2))) + 3 * ((h 1 2) + (h 1 4) - 2 * (t 1 3))) + 2 * ((h 2 4) - (t 1 4))) + 6 * ((h 3 0) - (t 2 0))) + 6 * (- (t 2 2))) + 2 * ((h 2 2) + (h 3 3) - (t 2 3))) + 6 * (- (t 2 4))) + 4 * ((h 4 1) - (t 3 1))) + 2 * ((h 3 2) - (t 3 3))) + 2 * ((h 3 2) + (h 3 4) - 2 * (t 3 3))) + 2 * ((h 4 4) - (t 3 4))) + 2 * ((h 4 1) + (h 5 0) - (t 4 0))) + 6 * (- (h 4 1))) + 2 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1))) + 2 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 2 * ((h 3 4) - (t 4 4))) + 4 * ((h 4 1) + (h 5 0) - (t 5 1))) + 2 * ((h 5 3))) + 4 * ((h 4 3) + (h 5 2) - (t 5 3))) + 2 * (1 - (t 3 0) - (t 3 1) - (t 4 0))) + 2 * (1 - (t 4 0) - (t 5 0) - (t 5 1))) + 2 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 6 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31) hn32) hn33)
  have identity : (((((((((((((((((((((((((((((((((6 * ((h 0 1) + (h 1 0) - (t 0 0)) + 2 * ((h 0 0) - (t 0 1))) + 2 * (1 - (h 0 2) - (t 0 2))) + 1 * (1 - (t 0 2))) + 3 * ((h 0 3) + (h 1 2) - (t 0 2))) + 2 * ((h 0 2) + (h 1 3) - (t 0 3))) + 3 * ((h 0 3) + (h 0 5) + (h 1 4) - 2 * (t 0 4))) + 3 * ((h 0 5) + (h 0 7) - (t 0 6))) + 3 * ((h 0 7) - (t 0 6))) + 2 * ((h 2 0) - (t 1 0))) + 2 * ((h 0 2) - (t 1 2))) + 3 * ((h 1 2) + (h 1 4) - 2 * (t 1 3))) + 2 * ((h 2 4) - (t 1 4))) + 6 * ((h 3 0) - (t 2 0))) + 6 * (- (t 2 2))) + 2 * ((h 2 2) + (h 3 3) - (t 2 3))) + 6 * (- (t 2 4))) + 4 * ((h 4 1) - (t 3 1))) + 2 * ((h 3 2) - (t 3 3))) + 2 * ((h 3 2) + (h 3 4) - 2 * (t 3 3))) + 2 * ((h 4 4) - (t 3 4))) + 2 * ((h 4 1) + (h 5 0) - (t 4 0))) + 6 * (- (h 4 1))) + 2 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1))) + 2 * ((h 3 2) + (h 4 1) + (h 5 2) - 2 * (t 4 2))) + 2 * ((h 3 4) + (h 4 3) - 2 * (t 4 4))) + 2 * ((h 3 4) - (t 4 4))) + 4 * ((h 4 1) + (h 5 0) - (t 5 1))) + 2 * ((h 5 3))) + 4 * ((h 4 3) + (h 5 2) - (t 5 3))) + 2 * (1 - (t 3 0) - (t 3 1) - (t 4 0))) + 2 * (1 - (t 4 0) - (t 5 0) - (t 5 1))) + 2 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 6 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 1 - 2 * (1 - (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_4 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 0)
    (fix_t41 : t 4 1 = 1)
    (fix_h23 : h 2 3 = 1)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn0 : 0 ≤ 1 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 0) - (t 0 1)) := by
    have := p.s66
    omega
  have hn1 : 0 ≤ 3 * ((h 0 0) - (t 0 1)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 2) - (t 0 1)) := by
    have := p.s67
    omega
  have hn2 : 0 ≤ 2 * ((h 0 2) - (t 0 1)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ (1 - (h 0 2) - (t 0 2)) := by
    have := p.s95
    omega
  have hn3 : 0 ≤ 1 * (1 - (h 0 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 2) + (h 1 3) - (t 0 3)) := by
    have := p.s11
    omega
  have hn4 : 0 ≤ 3 * ((h 0 2) + (h 1 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 2) + (h 0 4) + (h 1 3) - 2 * (t 0 3)) := by
    have := p.s10
    omega
  have hn5 : 0 ≤ 1 * ((h 0 2) + (h 0 4) + (h 1 3) - 2 * (t 0 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ (1 - (h 0 4) - (t 0 4)) := by
    have := p.s97
    omega
  have hn6 : 0 ≤ 1 * (1 - (h 0 4) - (t 0 4)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 0 5) + (h 0 7) - (t 0 6)) := by
    have := p.s15
    omega
  have hn7 : 0 ≤ 1 * ((h 0 5) + (h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 0 0) + (h 2 0) - 2 * (t 1 0)) := by
    have := p.s16
    omega
  have hn8 : 0 ≤ 2 * ((h 0 0) + (h 2 0) - 2 * (t 1 0)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 2 0) - (t 1 0)) := by
    have := p.s70
    omega
  have hn9 : 0 ≤ 1 * ((h 2 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 2 2) - (t 1 2)) := by
    have := p.s73
    omega
  have hn10 : 0 ≤ 5 * ((h 2 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 0 3) + (h 1 2) - (t 1 3)) := by
    have := p.s18
    omega
  have hn11 : 0 ≤ 1 * ((h 0 3) + (h 1 2) - (t 1 3)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := by
    have := p.s24
    omega
  have hn12 : 0 ≤ 1 * ((h 1 3) + (h 2 4) - 2 * (t 1 4)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 2 4) - (t 1 4)) := by
    have := p.s75
    omega
  have hn13 : 0 ≤ 3 * ((h 2 4) - (t 1 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s77
    omega
  have hn14 : 0 ≤ 1 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 3 2) - (t 2 2)) := by
    have := p.s81
    omega
  have hn15 : 0 ≤ 1 * ((h 3 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (- (t 2 3)) := by
    have := p.s99
    omega
  have hn16 : 0 ≤ 5 * (- (t 2 3)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 1 4) - (t 2 4)) := by
    have := p.s82
    omega
  have hn17 : 0 ≤ 1 * ((h 1 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ (1 - (t 3 0)) := by
    have := p.s2
    omega
  have hn18 : 0 ≤ 1 * (1 - (t 3 0)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0)) := by
    have := p.s33
    omega
  have hn19 : 0 ≤ 2 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 4 1) - (t 3 1)) := by
    have := p.s87
    omega
  have hn20 : 0 ≤ 1 * ((h 4 1) - (t 3 1)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ (1 - (h 3 3) - (t 3 3)) := by
    have := p.s102
    omega
  have hn21 : 0 ≤ 1 * (1 - (h 3 3) - (t 3 3)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ ((h 2 4) + (h 3 3) - (t 3 4)) := by
    have := p.s41
    omega
  have hn22 : 0 ≤ 1 * ((h 2 4) + (h 3 3) - (t 3 4)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := by
    have := p.s42
    omega
  have hn23 : 0 ≤ 2 * ((h 3 3) + (h 4 4) - 2 * (t 3 4)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0)) := by
    have := p.s45
    omega
  have hn24 : 0 ≤ 1 * ((h 4 1) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ (- (h 4 1)) := by
    have := p.s104
    omega
  have hn25 : 0 ≤ 1 * (- (h 4 1)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1)) := by
    have := p.s46
    omega
  have hn26 : 0 ≤ 3 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 3 3) + (h 4 4) - (t 4 3)) := by
    have := p.s54
    omega
  have hn27 : 0 ≤ 1 * ((h 3 3) + (h 4 4) - (t 4 3)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 3 3) + (h 4 4) + (h 5 3) - 2 * (t 4 3)) := by
    have := p.s55
    omega
  have hn28 : 0 ≤ 2 * ((h 3 3) + (h 4 4) + (h 5 3) - 2 * (t 4 3)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ ((h 3 4) - (t 4 4)) := by
    have := p.s89
    omega
  have hn29 : 0 ≤ 1 * ((h 3 4) - (t 4 4)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ (1 - (t 5 0)) := by
    have := p.s4
    omega
  have hn30 : 0 ≤ 5 * (1 - (t 5 0)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := by
    have := p.s61
    omega
  have hn31 : 0 ≤ 2 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2)) := Int.mul_nonneg (by decide) hs31
  have hs32 : 0 ≤ ((h 5 3)) := by
    have := p.s92
    omega
  have hn32 : 0 ≤ 1 * ((h 5 3)) := Int.mul_nonneg (by decide) hs32
  have hs33 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3)) := by
    have := p.s64
    omega
  have hn33 : 0 ≤ 1 * ((h 4 3) + (h 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs33
  have hs34 : 0 ≤ (1 - (t 4 2) - (t 5 1) - (t 5 2)) := by
    have := p.s115
    omega
  have hn34 : 0 ≤ 1 * (1 - (t 4 2) - (t 5 1) - (t 5 2)) := Int.mul_nonneg (by decide) hs34
  have hs35 : 0 ≤ (- 2 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn35 : 0 ≤ 1 * (- 2 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs35
  have htotal : 0 ≤ (((((((((((((((((((((((((((((((((((1 * ((h 0 1) + (h 1 0) - (t 0 0)) + 3 * ((h 0 0) - (t 0 1))) + 2 * ((h 0 2) - (t 0 1))) + 1 * (1 - (h 0 2) - (t 0 2))) + 3 * ((h 0 2) + (h 1 3) - (t 0 3))) + 1 * ((h 0 2) + (h 0 4) + (h 1 3) - 2 * (t 0 3))) + 1 * (1 - (h 0 4) - (t 0 4))) + 1 * ((h 0 5) + (h 0 7) - (t 0 6))) + 2 * ((h 0 0) + (h 2 0) - 2 * (t 1 0))) + 1 * ((h 2 0) - (t 1 0))) + 5 * ((h 2 2) - (t 1 2))) + 1 * ((h 0 3) + (h 1 2) - (t 1 3))) + 1 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 3 * ((h 2 4) - (t 1 4))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 3 2) - (t 2 2))) + 5 * (- (t 2 3))) + 1 * ((h 1 4) - (t 2 4))) + 1 * (1 - (t 3 0))) + 2 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0))) + 1 * ((h 4 1) - (t 3 1))) + 1 * (1 - (h 3 3) - (t 3 3))) + 1 * ((h 2 4) + (h 3 3) - (t 3 4))) + 2 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 1 * ((h 4 1) + (h 5 0) - (t 4 0))) + 1 * (- (h 4 1))) + 3 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1))) + 1 * ((h 3 3) + (h 4 4) - (t 4 3))) + 2 * ((h 3 3) + (h 4 4) + (h 5 3) - 2 * (t 4 3))) + 1 * ((h 3 4) - (t 4 4))) + 5 * (1 - (t 5 0))) + 2 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 1 * ((h 5 3))) + 1 * ((h 4 3) + (h 5 2) - (t 5 3))) + 1 * (1 - (t 4 2) - (t 5 1) - (t 5 2))) + 1 * (- 2 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31) hn32) hn33) hn34) hn35)
  have identity : (((((((((((((((((((((((((((((((((((1 * ((h 0 1) + (h 1 0) - (t 0 0)) + 3 * ((h 0 0) - (t 0 1))) + 2 * ((h 0 2) - (t 0 1))) + 1 * (1 - (h 0 2) - (t 0 2))) + 3 * ((h 0 2) + (h 1 3) - (t 0 3))) + 1 * ((h 0 2) + (h 0 4) + (h 1 3) - 2 * (t 0 3))) + 1 * (1 - (h 0 4) - (t 0 4))) + 1 * ((h 0 5) + (h 0 7) - (t 0 6))) + 2 * ((h 0 0) + (h 2 0) - 2 * (t 1 0))) + 1 * ((h 2 0) - (t 1 0))) + 5 * ((h 2 2) - (t 1 2))) + 1 * ((h 0 3) + (h 1 2) - (t 1 3))) + 1 * ((h 1 3) + (h 2 4) - 2 * (t 1 4))) + 3 * ((h 2 4) - (t 1 4))) + 1 * ((h 3 0) - (t 2 0))) + 1 * ((h 3 2) - (t 2 2))) + 5 * (- (t 2 3))) + 1 * ((h 1 4) - (t 2 4))) + 1 * (1 - (t 3 0))) + 2 * ((h 2 0) + (h 3 1) + (h 4 0) - 2 * (t 3 0))) + 1 * ((h 4 1) - (t 3 1))) + 1 * (1 - (h 3 3) - (t 3 3))) + 1 * ((h 2 4) + (h 3 3) - (t 3 4))) + 2 * ((h 3 3) + (h 4 4) - 2 * (t 3 4))) + 1 * ((h 4 1) + (h 5 0) - (t 4 0))) + 1 * (- (h 4 1))) + 3 * (- 3 + (h 3 1) + (h 4 0) + (h 4 2) + (h 5 1))) + 1 * ((h 3 3) + (h 4 4) - (t 4 3))) + 2 * ((h 3 3) + (h 4 4) + (h 5 3) - 2 * (t 4 3))) + 1 * ((h 3 4) - (t 4 4))) + 5 * (1 - (t 5 0))) + 2 * ((h 4 2) + (h 5 1) + (h 5 3) - 2 * (t 5 2))) + 1 * ((h 5 3))) + 1 * ((h 4 3) + (h 5 2) - (t 5 3))) + 1 * (1 - (t 4 2) - (t 5 1) - (t 5 2))) + 1 * (- 2 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 4 - 5 * (1 - (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_5 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 1)
    (fix_h13 : h 1 3 = 0)
    (fix_h03 : h 0 3 = 0)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (h 0 0) - (t 0 0)) := by
    have := p.s94
    omega
  have hn0 : 0 ≤ 1 * (1 - (h 0 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn1 : 0 ≤ 1 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 0) - (t 0 1)) := by
    have := p.s66
    omega
  have hn2 : 0 ≤ 1 * ((h 0 0) - (t 0 1)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 1) - (t 0 2)) := by
    have := p.s7
    omega
  have hn3 : 0 ≤ 1 * ((h 0 1) - (t 0 2)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 1 2) - (t 0 2)) := by
    have := p.s9
    omega
  have hn4 : 0 ≤ 1 * ((h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 2) - (t 0 3)) := by
    have := p.s11
    omega
  have hn5 : 0 ≤ 1 * ((h 0 2) - (t 0 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 5) - (t 0 4)) := by
    have := p.s12
    omega
  have hn6 : 0 ≤ 2 * ((h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn7 : 0 ≤ 2 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 0 0) - (t 1 0)) := by
    have := p.s69
    omega
  have hn8 : 0 ≤ 1 * ((h 0 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ (- (t 1 2)) := by
    have := p.s72
    omega
  have hn9 : 0 ≤ 1 * (- (t 1 2)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 1 2) + (h 1 4) - 2 * (t 1 3)) := by
    have := p.s19
    omega
  have hn10 : 0 ≤ 1 * ((h 1 2) + (h 1 4) - 2 * (t 1 3)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ (- (t 1 4)) := by
    have := p.s74
    omega
  have hn11 : 0 ≤ 1 * (- (t 1 4)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := by
    have := p.s25
    omega
  have hn12 : 0 ≤ 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 3 2) - (t 2 2)) := by
    have := p.s81
    omega
  have hn13 : 0 ≤ 2 * ((h 3 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 2 4) - (t 2 3)) := by
    have := p.s28
    omega
  have hn14 : 0 ≤ 1 * ((h 2 4) - (t 2 3)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 1 4) - (t 2 4)) := by
    have := p.s82
    omega
  have hn15 : 0 ≤ 1 * ((h 1 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 2 3) - (t 2 4)) := by
    have := p.s83
    omega
  have hn16 : 0 ≤ 1 * ((h 2 3) - (t 2 4)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 2 0) + (h 4 0) - (t 3 0)) := by
    have := p.s34
    omega
  have hn17 : 0 ≤ 1 * ((h 2 0) + (h 4 0) - (t 3 0)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ ((h 3 2) - (t 3 1)) := by
    have := p.s86
    omega
  have hn18 : 0 ≤ 2 * ((h 3 2) - (t 3 1)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ (- (h 3 2)) := by
    have := p.s101
    omega
  have hn19 : 0 ≤ 4 * (- (h 3 2)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := by
    have := p.s36
    omega
  have hn20 : 0 ≤ 1 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ ((h 2 3) + (h 3 2) - (t 3 3)) := by
    have := p.s37
    omega
  have hn21 : 0 ≤ 1 * ((h 2 3) + (h 3 2) - (t 3 3)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn22 : 0 ≤ 1 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ ((h 3 0) + (h 5 0) - (t 4 0)) := by
    have := p.s44
    omega
  have hn23 : 0 ≤ 1 * ((h 3 0) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 3 2) + (h 4 1) - (t 4 2)) := by
    have := p.s48
    omega
  have hn24 : 0 ≤ 1 * ((h 3 2) + (h 4 1) - (t 4 2)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 3 4) - (t 4 4)) := by
    have := p.s89
    omega
  have hn25 : 0 ≤ 2 * ((h 3 4) - (t 4 4)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s58
    omega
  have hn26 : 0 ≤ 1 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 5 1) + (h 5 3) - (t 5 2)) := by
    have := p.s63
    omega
  have hn27 : 0 ≤ 1 * ((h 5 1) + (h 5 3) - (t 5 2)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3)) := by
    have := p.s64
    omega
  have hn28 : 0 ≤ 2 * ((h 4 3) + (h 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ (1 - (t 3 3) - (t 4 2) - (t 4 3)) := by
    have := p.s113
    omega
  have hn29 : 0 ≤ 1 * (1 - (t 3 3) - (t 4 2) - (t 4 3)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := by
    have := p.s114
    omega
  have hn30 : 0 ≤ 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ (- 1 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn31 : 0 ≤ 2 * (- 1 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs31
  have htotal : 0 ≤ (((((((((((((((((((((((((((((((1 * (1 - (h 0 0) - (t 0 0)) + 1 * ((h 0 1) + (h 1 0) - (t 0 0))) + 1 * ((h 0 0) - (t 0 1))) + 1 * ((h 0 1) - (t 0 2))) + 1 * ((h 1 2) - (t 0 2))) + 1 * ((h 0 2) - (t 0 3))) + 2 * ((h 0 5) - (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 1 * ((h 0 0) - (t 1 0))) + 1 * (- (t 1 2))) + 1 * ((h 1 2) + (h 1 4) - 2 * (t 1 3))) + 1 * (- (t 1 4))) + 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 2 * ((h 3 2) - (t 2 2))) + 1 * ((h 2 4) - (t 2 3))) + 1 * ((h 1 4) - (t 2 4))) + 1 * ((h 2 3) - (t 2 4))) + 1 * ((h 2 0) + (h 4 0) - (t 3 0))) + 2 * ((h 3 2) - (t 3 1))) + 4 * (- (h 3 2))) + 1 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 1 * ((h 2 3) + (h 3 2) - (t 3 3))) + 1 * ((h 4 4) - (t 3 4))) + 1 * ((h 3 0) + (h 5 0) - (t 4 0))) + 1 * ((h 3 2) + (h 4 1) - (t 4 2))) + 2 * ((h 3 4) - (t 4 4))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 1 * ((h 5 1) + (h 5 3) - (t 5 2))) + 2 * ((h 4 3) + (h 5 2) - (t 5 3))) + 1 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 2 * (- 1 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31)
  have identity : (((((((((((((((((((((((((((((((1 * (1 - (h 0 0) - (t 0 0)) + 1 * ((h 0 1) + (h 1 0) - (t 0 0))) + 1 * ((h 0 0) - (t 0 1))) + 1 * ((h 0 1) - (t 0 2))) + 1 * ((h 1 2) - (t 0 2))) + 1 * ((h 0 2) - (t 0 3))) + 2 * ((h 0 5) - (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 1 * ((h 0 0) - (t 1 0))) + 1 * (- (t 1 2))) + 1 * ((h 1 2) + (h 1 4) - 2 * (t 1 3))) + 1 * (- (t 1 4))) + 1 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 2 * ((h 3 2) - (t 2 2))) + 1 * ((h 2 4) - (t 2 3))) + 1 * ((h 1 4) - (t 2 4))) + 1 * ((h 2 3) - (t 2 4))) + 1 * ((h 2 0) + (h 4 0) - (t 3 0))) + 2 * ((h 3 2) - (t 3 1))) + 4 * (- (h 3 2))) + 1 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 1 * ((h 2 3) + (h 3 2) - (t 3 3))) + 1 * ((h 4 4) - (t 3 4))) + 1 * ((h 3 0) + (h 5 0) - (t 4 0))) + 1 * ((h 3 2) + (h 4 1) - (t 4 2))) + 2 * ((h 3 4) - (t 4 4))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 1 * ((h 5 1) + (h 5 3) - (t 5 2))) + 2 * ((h 4 3) + (h 5 2) - (t 5 3))) + 1 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 2 * (- 1 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 0 - 1 * (1 - (h 0 0) - (h 0 2) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_6 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 1)
    (fix_h13 : h 1 3 = 0)
    (fix_h03 : h 0 3 = 1)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn0 : 0 ≤ 2 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 2) - (t 0 1)) := by
    have := p.s67
    omega
  have hn1 : 0 ≤ 4 * ((h 0 2) - (t 0 1)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ (1 - (t 0 2)) := by
    have := p.s0
    omega
  have hn2 : 0 ≤ 2 * (1 - (t 0 2)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ (- (t 0 3)) := by
    have := p.s96
    omega
  have hn3 : 0 ≤ 4 * (- (t 0 3)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4)) := by
    have := p.s14
    omega
  have hn4 : 0 ≤ 2 * ((h 0 5) + (h 1 4) - (t 0 4)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn5 : 0 ≤ 2 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 0) - (t 1 0)) := by
    have := p.s69
    omega
  have hn6 : 0 ≤ 4 * ((h 0 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ (- (t 1 2)) := by
    have := p.s72
    omega
  have hn7 : 0 ≤ 4 * (- (t 1 2)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 1 2) + (h 2 3) - (t 1 3)) := by
    have := p.s23
    omega
  have hn8 : 0 ≤ 2 * ((h 1 2) + (h 2 3) - (t 1 3)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ (- (t 1 4)) := by
    have := p.s74
    omega
  have hn9 : 0 ≤ 4 * (- (t 1 4)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s77
    omega
  have hn10 : 0 ≤ 2 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 3 2) - (t 2 2)) := by
    have := p.s81
    omega
  have hn11 : 0 ≤ 2 * ((h 3 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ ((h 2 4) - (t 2 3)) := by
    have := p.s28
    omega
  have hn12 : 0 ≤ 4 * ((h 2 4) - (t 2 3)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 3 4) - (t 2 4)) := by
    have := p.s84
    omega
  have hn13 : 0 ≤ 2 * ((h 3 4) - (t 2 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 2 0) + (h 4 0) - (t 3 0)) := by
    have := p.s34
    omega
  have hn14 : 0 ≤ 4 * ((h 2 0) + (h 4 0) - (t 3 0)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 3 2) - (t 3 1)) := by
    have := p.s86
    omega
  have hn15 : 0 ≤ 2 * ((h 3 2) - (t 3 1)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ (- (h 3 2)) := by
    have := p.s101
    omega
  have hn16 : 0 ≤ 2 * (- (h 3 2)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := by
    have := p.s36
    omega
  have hn17 : 0 ≤ 4 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn18 : 0 ≤ 4 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0)) := by
    have := p.s45
    omega
  have hn19 : 0 ≤ 1 * ((h 4 1) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ (1 - (t 4 1)) := by
    have := p.s3
    omega
  have hn20 : 0 ≤ 3 * (1 - (t 4 1)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ (1 - (h 4 3) - (t 4 3)) := by
    have := p.s106
    omega
  have hn21 : 0 ≤ 2 * (1 - (h 4 3) - (t 4 3)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ ((h 4 3) - (t 4 4)) := by
    have := p.s90
    omega
  have hn22 : 0 ≤ 2 * ((h 4 3) - (t 4 4)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ (1 - (t 5 0)) := by
    have := p.s4
    omega
  have hn23 : 0 ≤ 3 * (1 - (t 5 0)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s58
    omega
  have hn24 : 0 ≤ 1 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 5 1) + (h 5 3) - (t 5 2)) := by
    have := p.s63
    omega
  have hn25 : 0 ≤ 4 * ((h 5 1) + (h 5 3) - (t 5 2)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3)) := by
    have := p.s64
    omega
  have hn26 : 0 ≤ 2 * ((h 4 3) + (h 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ (1 - (t 3 3) - (t 4 2) - (t 4 3)) := by
    have := p.s113
    omega
  have hn27 : 0 ≤ 2 * (1 - (t 3 3) - (t 4 2) - (t 4 3)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := by
    have := p.s114
    omega
  have hn28 : 0 ≤ 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ (- 2 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn29 : 0 ≤ 2 * (- 2 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs29
  have htotal : 0 ≤ (((((((((((((((((((((((((((((2 * ((h 0 1) + (h 1 0) - (t 0 0)) + 4 * ((h 0 2) - (t 0 1))) + 2 * (1 - (t 0 2))) + 4 * (- (t 0 3))) + 2 * ((h 0 5) + (h 1 4) - (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 4 * ((h 0 0) - (t 1 0))) + 4 * (- (t 1 2))) + 2 * ((h 1 2) + (h 2 3) - (t 1 3))) + 4 * (- (t 1 4))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 3 2) - (t 2 2))) + 4 * ((h 2 4) - (t 2 3))) + 2 * ((h 3 4) - (t 2 4))) + 4 * ((h 2 0) + (h 4 0) - (t 3 0))) + 2 * ((h 3 2) - (t 3 1))) + 2 * (- (h 3 2))) + 4 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 4 * ((h 4 4) - (t 3 4))) + 1 * ((h 4 1) + (h 5 0) - (t 4 0))) + 3 * (1 - (t 4 1))) + 2 * (1 - (h 4 3) - (t 4 3))) + 2 * ((h 4 3) - (t 4 4))) + 3 * (1 - (t 5 0))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 4 * ((h 5 1) + (h 5 3) - (t 5 2))) + 2 * ((h 4 3) + (h 5 2) - (t 5 3))) + 2 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 2 * (- 2 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29)
  have identity : (((((((((((((((((((((((((((((2 * ((h 0 1) + (h 1 0) - (t 0 0)) + 4 * ((h 0 2) - (t 0 1))) + 2 * (1 - (t 0 2))) + 4 * (- (t 0 3))) + 2 * ((h 0 5) + (h 1 4) - (t 0 4))) + 2 * ((h 0 7) - (t 0 6))) + 4 * ((h 0 0) - (t 1 0))) + 4 * (- (t 1 2))) + 2 * ((h 1 2) + (h 2 3) - (t 1 3))) + 4 * (- (t 1 4))) + 2 * ((h 3 0) - (t 2 0))) + 2 * ((h 3 2) - (t 2 2))) + 4 * ((h 2 4) - (t 2 3))) + 2 * ((h 3 4) - (t 2 4))) + 4 * ((h 2 0) + (h 4 0) - (t 3 0))) + 2 * ((h 3 2) - (t 3 1))) + 2 * (- (h 3 2))) + 4 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 4 * ((h 4 4) - (t 3 4))) + 1 * ((h 4 1) + (h 5 0) - (t 4 0))) + 3 * (1 - (t 4 1))) + 2 * (1 - (h 4 3) - (t 4 3))) + 2 * ((h 4 3) - (t 4 4))) + 3 * (1 - (t 5 0))) + 1 * ((h 4 1) + (h 5 0) - (t 5 1))) + 4 * ((h 5 1) + (h 5 3) - (t 5 2))) + 2 * ((h 4 3) + (h 5 2) - (t 5 3))) + 2 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 1 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 2 * (- 2 - (h 0 1) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 2 - 4 * (1 - (h 0 0) - (h 0 2) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_case_7 (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (fix_t32 : t 3 2 = 1)
    (fix_h13 : h 1 3 = 1)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have hs0 : 0 ≤ (1 - (h 0 0) - (t 0 0)) := by
    have := p.s94
    omega
  have hn0 : 0 ≤ 3 * (1 - (h 0 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs0
  have hs1 : 0 ≤ ((h 0 1) + (h 1 0) - (t 0 0)) := by
    have := p.s6
    omega
  have hn1 : 0 ≤ 33 * ((h 0 1) + (h 1 0) - (t 0 0)) := Int.mul_nonneg (by decide) hs1
  have hs2 : 0 ≤ ((h 0 0) - (t 0 1)) := by
    have := p.s66
    omega
  have hn2 : 0 ≤ 15 * ((h 0 0) - (t 0 1)) := Int.mul_nonneg (by decide) hs2
  have hs3 : 0 ≤ ((h 0 1) + (h 1 2) - (t 0 2)) := by
    have := p.s8
    omega
  have hn3 : 0 ≤ 3 * ((h 0 1) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs3
  have hs4 : 0 ≤ ((h 0 3) + (h 1 2) - (t 0 2)) := by
    have := p.s9
    omega
  have hn4 : 0 ≤ 33 * ((h 0 3) + (h 1 2) - (t 0 2)) := Int.mul_nonneg (by decide) hs4
  have hs5 : 0 ≤ (1 - (h 0 3) - (t 0 3)) := by
    have := p.s96
    omega
  have hn5 : 0 ≤ 15 * (1 - (h 0 3) - (t 0 3)) := Int.mul_nonneg (by decide) hs5
  have hs6 : 0 ≤ ((h 0 3) + (h 0 5) - (t 0 4)) := by
    have := p.s12
    omega
  have hn6 : 0 ≤ 18 * ((h 0 3) + (h 0 5) - (t 0 4)) := Int.mul_nonneg (by decide) hs6
  have hs7 : 0 ≤ ((h 0 5) + (h 1 4) - (t 0 4)) := by
    have := p.s14
    omega
  have hn7 : 0 ≤ 18 * ((h 0 5) + (h 1 4) - (t 0 4)) := Int.mul_nonneg (by decide) hs7
  have hs8 : 0 ≤ ((h 0 7) - (t 0 6)) := by
    have := p.s68
    omega
  have hn8 : 0 ≤ 36 * ((h 0 7) - (t 0 6)) := Int.mul_nonneg (by decide) hs8
  have hs9 : 0 ≤ ((h 0 0) + (h 2 0) - 2 * (t 1 0)) := by
    have := p.s16
    omega
  have hn9 : 0 ≤ 3 * ((h 0 0) + (h 2 0) - 2 * (t 1 0)) := Int.mul_nonneg (by decide) hs9
  have hs10 : 0 ≤ ((h 2 0) - (t 1 0)) := by
    have := p.s70
    omega
  have hn10 : 0 ≤ 9 * ((h 2 0) - (t 1 0)) := Int.mul_nonneg (by decide) hs10
  have hs11 : 0 ≤ ((h 0 2) - (t 1 2)) := by
    have := p.s71
    omega
  have hn11 : 0 ≤ 15 * ((h 0 2) - (t 1 2)) := Int.mul_nonneg (by decide) hs11
  have hs12 : 0 ≤ (- (t 1 3)) := by
    have := p.s98
    omega
  have hn12 : 0 ≤ 36 * (- (t 1 3)) := Int.mul_nonneg (by decide) hs12
  have hs13 : 0 ≤ ((h 2 4) - (t 1 4)) := by
    have := p.s75
    omega
  have hn13 : 0 ≤ 15 * ((h 2 4) - (t 1 4)) := Int.mul_nonneg (by decide) hs13
  have hs14 : 0 ≤ ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := by
    have := p.s25
    omega
  have hn14 : 0 ≤ 3 * ((h 1 0) + (h 3 0) - 2 * (t 2 0)) := Int.mul_nonneg (by decide) hs14
  have hs15 : 0 ≤ ((h 3 0) - (t 2 0)) := by
    have := p.s77
    omega
  have hn15 : 0 ≤ 30 * ((h 3 0) - (t 2 0)) := Int.mul_nonneg (by decide) hs15
  have hs16 : 0 ≤ ((h 3 2) - (t 2 2)) := by
    have := p.s81
    omega
  have hn16 : 0 ≤ 21 * ((h 3 2) - (t 2 2)) := Int.mul_nonneg (by decide) hs16
  have hs17 : 0 ≤ ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := by
    have := p.s31
    omega
  have hn17 : 0 ≤ 18 * ((h 1 4) + (h 2 3) - 2 * (t 2 4)) := Int.mul_nonneg (by decide) hs17
  have hs18 : 0 ≤ (1 - (h 3 0) - (t 3 0)) := by
    have := p.s100
    omega
  have hn18 : 0 ≤ 12 * (1 - (h 3 0) - (t 3 0)) := Int.mul_nonneg (by decide) hs18
  have hs19 : 0 ≤ ((h 2 0) + (h 4 0) - (t 3 0)) := by
    have := p.s34
    omega
  have hn19 : 0 ≤ 3 * ((h 2 0) + (h 4 0) - (t 3 0)) := Int.mul_nonneg (by decide) hs19
  have hs20 : 0 ≤ ((h 3 2) - (t 3 1)) := by
    have := p.s86
    omega
  have hn20 : 0 ≤ 36 * ((h 3 2) - (t 3 1)) := Int.mul_nonneg (by decide) hs20
  have hs21 : 0 ≤ (- (h 3 2)) := by
    have := p.s101
    omega
  have hn21 : 0 ≤ 56 * (- (h 3 2)) := Int.mul_nonneg (by decide) hs21
  have hs22 : 0 ≤ (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := by
    have := p.s36
    omega
  have hn22 : 0 ≤ 15 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2)) := Int.mul_nonneg (by decide) hs22
  have hs23 : 0 ≤ ((h 2 3) + (h 3 2) - (t 3 3)) := by
    have := p.s37
    omega
  have hn23 : 0 ≤ 18 * ((h 2 3) + (h 3 2) - (t 3 3)) := Int.mul_nonneg (by decide) hs23
  have hs24 : 0 ≤ ((h 4 4) - (t 3 4)) := by
    have := p.s88
    omega
  have hn24 : 0 ≤ 15 * ((h 4 4) - (t 3 4)) := Int.mul_nonneg (by decide) hs24
  have hs25 : 0 ≤ ((h 3 0) + (h 5 0) - (t 4 0)) := by
    have := p.s44
    omega
  have hn25 : 0 ≤ 5 * ((h 3 0) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs25
  have hs26 : 0 ≤ ((h 4 1) + (h 5 0) - (t 4 0)) := by
    have := p.s45
    omega
  have hn26 : 0 ≤ 4 * ((h 4 1) + (h 5 0) - (t 4 0)) := Int.mul_nonneg (by decide) hs26
  have hs27 : 0 ≤ ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0)) := by
    have := p.s43
    omega
  have hn27 : 0 ≤ 10 * ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0)) := Int.mul_nonneg (by decide) hs27
  have hs28 : 0 ≤ ((h 4 0) + (h 4 2) + (h 5 1) - 2 * (t 4 1)) := by
    have := p.s47
    omega
  have hn28 : 0 ≤ 4 * ((h 4 0) + (h 4 2) + (h 5 1) - 2 * (t 4 1)) := Int.mul_nonneg (by decide) hs28
  have hs29 : 0 ≤ (1 - (h 4 2) - (t 4 2)) := by
    have := p.s105
    omega
  have hn29 : 0 ≤ 4 * (1 - (h 4 2) - (t 4 2)) := Int.mul_nonneg (by decide) hs29
  have hs30 : 0 ≤ ((h 3 2) + (h 4 1) - (t 4 2)) := by
    have := p.s48
    omega
  have hn30 : 0 ≤ 5 * ((h 3 2) + (h 4 1) - (t 4 2)) := Int.mul_nonneg (by decide) hs30
  have hs31 : 0 ≤ ((h 3 2) + (h 4 3) - (t 4 2)) := by
    have := p.s51
    omega
  have hn31 : 0 ≤ 12 * ((h 3 2) + (h 4 3) - (t 4 2)) := Int.mul_nonneg (by decide) hs31
  have hs32 : 0 ≤ ((h 3 4) - (t 4 4)) := by
    have := p.s89
    omega
  have hn32 : 0 ≤ 36 * ((h 3 4) - (t 4 4)) := Int.mul_nonneg (by decide) hs32
  have hs33 : 0 ≤ ((h 4 0) + (h 5 1) - (t 5 0)) := by
    have := p.s57
    omega
  have hn33 : 0 ≤ 8 * ((h 4 0) + (h 5 1) - (t 5 0)) := Int.mul_nonneg (by decide) hs33
  have hs34 : 0 ≤ ((h 4 1) + (h 5 0) - (t 5 1)) := by
    have := p.s58
    omega
  have hn34 : 0 ≤ 5 * ((h 4 1) + (h 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs34
  have hs35 : 0 ≤ ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1)) := by
    have := p.s59
    omega
  have hn35 : 0 ≤ 12 * ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1)) := Int.mul_nonneg (by decide) hs35
  have hs36 : 0 ≤ ((h 5 1) + (h 5 3) - (t 5 2)) := by
    have := p.s63
    omega
  have hn36 : 0 ≤ 3 * ((h 5 1) + (h 5 3) - (t 5 2)) := Int.mul_nonneg (by decide) hs36
  have hs37 : 0 ≤ ((h 5 3)) := by
    have := p.s92
    omega
  have hn37 : 0 ≤ 12 * ((h 5 3)) := Int.mul_nonneg (by decide) hs37
  have hs38 : 0 ≤ ((h 4 3) + (h 5 2) - (t 5 3)) := by
    have := p.s64
    omega
  have hn38 : 0 ≤ 24 * ((h 4 3) + (h 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs38
  have hs39 : 0 ≤ (1 - (t 2 2) - (t 2 3) - (t 3 3)) := by
    have := p.s111
    omega
  have hn39 : 0 ≤ 15 * (1 - (t 2 2) - (t 2 3) - (t 3 3)) := Int.mul_nonneg (by decide) hs39
  have hs40 : 0 ≤ (1 - (t 3 3) - (t 4 2) - (t 4 3)) := by
    have := p.s113
    omega
  have hn40 : 0 ≤ 3 * (1 - (t 3 3) - (t 4 2) - (t 4 3)) := Int.mul_nonneg (by decide) hs40
  have hs41 : 0 ≤ (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := by
    have := p.s114
    omega
  have hn41 : 0 ≤ 7 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1)) := Int.mul_nonneg (by decide) hs41
  have hs42 : 0 ≤ (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := by
    have := p.s116
    omega
  have hn42 : 0 ≤ 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3)) := Int.mul_nonneg (by decide) hs42
  have hs43 : 0 ≤ (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := by
    have := p.s109
    omega
  have hn43 : 0 ≤ 36 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3)) := Int.mul_nonneg (by decide) hs43
  have htotal : 0 ≤ (((((((((((((((((((((((((((((((((((((((((((3 * (1 - (h 0 0) - (t 0 0)) + 33 * ((h 0 1) + (h 1 0) - (t 0 0))) + 15 * ((h 0 0) - (t 0 1))) + 3 * ((h 0 1) + (h 1 2) - (t 0 2))) + 33 * ((h 0 3) + (h 1 2) - (t 0 2))) + 15 * (1 - (h 0 3) - (t 0 3))) + 18 * ((h 0 3) + (h 0 5) - (t 0 4))) + 18 * ((h 0 5) + (h 1 4) - (t 0 4))) + 36 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 0) + (h 2 0) - 2 * (t 1 0))) + 9 * ((h 2 0) - (t 1 0))) + 15 * ((h 0 2) - (t 1 2))) + 36 * (- (t 1 3))) + 15 * ((h 2 4) - (t 1 4))) + 3 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 30 * ((h 3 0) - (t 2 0))) + 21 * ((h 3 2) - (t 2 2))) + 18 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 12 * (1 - (h 3 0) - (t 3 0))) + 3 * ((h 2 0) + (h 4 0) - (t 3 0))) + 36 * ((h 3 2) - (t 3 1))) + 56 * (- (h 3 2))) + 15 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 18 * ((h 2 3) + (h 3 2) - (t 3 3))) + 15 * ((h 4 4) - (t 3 4))) + 5 * ((h 3 0) + (h 5 0) - (t 4 0))) + 4 * ((h 4 1) + (h 5 0) - (t 4 0))) + 10 * ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0))) + 4 * ((h 4 0) + (h 4 2) + (h 5 1) - 2 * (t 4 1))) + 4 * (1 - (h 4 2) - (t 4 2))) + 5 * ((h 3 2) + (h 4 1) - (t 4 2))) + 12 * ((h 3 2) + (h 4 3) - (t 4 2))) + 36 * ((h 3 4) - (t 4 4))) + 8 * ((h 4 0) + (h 5 1) - (t 5 0))) + 5 * ((h 4 1) + (h 5 0) - (t 5 1))) + 12 * ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1))) + 3 * ((h 5 1) + (h 5 3) - (t 5 2))) + 12 * ((h 5 3))) + 24 * ((h 4 3) + (h 5 2) - (t 5 3))) + 15 * (1 - (t 2 2) - (t 2 3) - (t 3 3))) + 3 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 7 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 36 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) := (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg (Int.add_nonneg hn0 hn1) hn2) hn3) hn4) hn5) hn6) hn7) hn8) hn9) hn10) hn11) hn12) hn13) hn14) hn15) hn16) hn17) hn18) hn19) hn20) hn21) hn22) hn23) hn24) hn25) hn26) hn27) hn28) hn29) hn30) hn31) hn32) hn33) hn34) hn35) hn36) hn37) hn38) hn39) hn40) hn41) hn42) hn43)
  have identity : (((((((((((((((((((((((((((((((((((((((((((3 * (1 - (h 0 0) - (t 0 0)) + 33 * ((h 0 1) + (h 1 0) - (t 0 0))) + 15 * ((h 0 0) - (t 0 1))) + 3 * ((h 0 1) + (h 1 2) - (t 0 2))) + 33 * ((h 0 3) + (h 1 2) - (t 0 2))) + 15 * (1 - (h 0 3) - (t 0 3))) + 18 * ((h 0 3) + (h 0 5) - (t 0 4))) + 18 * ((h 0 5) + (h 1 4) - (t 0 4))) + 36 * ((h 0 7) - (t 0 6))) + 3 * ((h 0 0) + (h 2 0) - 2 * (t 1 0))) + 9 * ((h 2 0) - (t 1 0))) + 15 * ((h 0 2) - (t 1 2))) + 36 * (- (t 1 3))) + 15 * ((h 2 4) - (t 1 4))) + 3 * ((h 1 0) + (h 3 0) - 2 * (t 2 0))) + 30 * ((h 3 0) - (t 2 0))) + 21 * ((h 3 2) - (t 2 2))) + 18 * ((h 1 4) + (h 2 3) - 2 * (t 2 4))) + 12 * (1 - (h 3 0) - (t 3 0))) + 3 * ((h 2 0) + (h 4 0) - (t 3 0))) + 36 * ((h 3 2) - (t 3 1))) + 56 * (- (h 3 2))) + 15 * (- 3 + (h 2 2) + (h 3 1) + (h 3 3) + (h 4 2))) + 18 * ((h 2 3) + (h 3 2) - (t 3 3))) + 15 * ((h 4 4) - (t 3 4))) + 5 * ((h 3 0) + (h 5 0) - (t 4 0))) + 4 * ((h 4 1) + (h 5 0) - (t 4 0))) + 10 * ((h 3 0) + (h 4 1) + (h 5 0) - 2 * (t 4 0))) + 4 * ((h 4 0) + (h 4 2) + (h 5 1) - 2 * (t 4 1))) + 4 * (1 - (h 4 2) - (t 4 2))) + 5 * ((h 3 2) + (h 4 1) - (t 4 2))) + 12 * ((h 3 2) + (h 4 3) - (t 4 2))) + 36 * ((h 3 4) - (t 4 4))) + 8 * ((h 4 0) + (h 5 1) - (t 5 0))) + 5 * ((h 4 1) + (h 5 0) - (t 5 1))) + 12 * ((h 4 1) + (h 5 0) + (h 5 2) - 2 * (t 5 1))) + 3 * ((h 5 1) + (h 5 3) - (t 5 2))) + 12 * ((h 5 3))) + 24 * ((h 4 3) + (h 5 2) - (t 5 3))) + 15 * (1 - (t 2 2) - (t 2 3) - (t 3 3))) + 3 * (1 - (t 3 3) - (t 4 2) - (t 4 3))) + 7 * (2 - (t 4 0) - (t 4 1) - (t 5 0) - (t 5 1))) + 12 * (2 - (t 4 2) - (t 4 3) - (t 5 2) - (t 5 3))) + 36 * (- 1 - (h 0 1) - (h 0 3) - (h 0 5) - (h 0 7) - (h 1 0) - (h 1 2) - (h 1 4) - (h 2 3) - (h 3 0) - (h 3 2) - (h 3 4) - (h 4 1) - (h 4 3) - (h 5 0) - (h 5 2) + (t 0 0) + (t 0 2) + (t 0 4) + (t 0 6) + (t 1 3) + (t 2 0) + (t 2 2) + (t 2 4) + (t 3 1) + (t 3 3) + (t 4 0) + (t 4 2) + (t 4 4) + (t 5 1) + (t 5 3))) = 9 - 15 * (- (h 0 0) - (h 0 2) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) := by omega
  rw [identity] at htotal
  omega

theorem switch_local_budget (t h : Nat → Nat → Int) (p : SwitchSlacks t h)
    (bit_h00 : 0 ≤ h 0 0 ∧ h 0 0 ≤ 1)
    (bit_h03 : 0 ≤ h 0 3 ∧ h 0 3 ≤ 1)
    (bit_h13 : 0 ≤ h 1 3 ∧ h 1 3 ≤ 1)
    (bit_h23 : 0 ≤ h 2 3 ∧ h 2 3 ≤ 1)
    (bit_t32 : 0 ≤ t 3 2 ∧ t 3 2 ≤ 1)
    (bit_t41 : 0 ≤ t 4 1 ∧ t 4 1 ≤ 1)
    : (- (h 0 0) - (h 0 2) - (h 1 3) - (h 2 0) - (h 2 2) - (h 2 4) - (h 3 1) - (h 3 3) - (h 4 0) - (h 4 2) - (h 4 4) - (h 5 1) - (h 5 3) + (t 0 1) + (t 0 3) + (t 1 0) + (t 1 2) + (t 1 4) + (t 2 3) + (t 3 0) + (t 3 2) + (t 3 4) + (t 4 1) + (t 4 3) + (t 5 0) + (t 5 2)) ≤ 0 := by
  have split_t32 : t 3 2 = 0 ∨ t 3 2 = 1 := by omega
  rcases split_t32 with fix_t32 | fix_t32
  ·
    have split_t41 : t 4 1 = 0 ∨ t 4 1 = 1 := by omega
    rcases split_t41 with fix_t41 | fix_t41
    ·
      have split_h00 : h 0 0 = 0 ∨ h 0 0 = 1 := by omega
      rcases split_h00 with fix_h00 | fix_h00
      ·
        exact switch_case_1 t h p fix_t32 fix_t41 fix_h00
      ·
        exact switch_case_2 t h p fix_t32 fix_t41 fix_h00
    ·
      have split_h23 : h 2 3 = 0 ∨ h 2 3 = 1 := by omega
      rcases split_h23 with fix_h23 | fix_h23
      ·
        exact switch_case_3 t h p fix_t32 fix_t41 fix_h23
      ·
        exact switch_case_4 t h p fix_t32 fix_t41 fix_h23
  ·
    have split_h13 : h 1 3 = 0 ∨ h 1 3 = 1 := by omega
    rcases split_h13 with fix_h13 | fix_h13
    ·
      have split_h03 : h 0 3 = 0 ∨ h 0 3 = 1 := by omega
      rcases split_h03 with fix_h03 | fix_h03
      ·
        exact switch_case_5 t h p fix_t32 fix_h13 fix_h03
      ·
        exact switch_case_6 t h p fix_t32 fix_h13 fix_h03
    ·
      exact switch_case_7 t h p fix_t32 fix_h13

/-- Five remaining white selections have an injection into eight black holes.
    The written proof establishes Hall by subfamily size. This kernel checks
    its numerical conclusion directly from the same local degree premises. -/
theorem five_white_hole_budget
    (a b c d e u v w x y z q r : Int)
    (ha : 0≤a ∧ a≤1) (hb : 0≤b ∧ b≤1) (hc : 0≤c ∧ c≤1)
    (hd : 0≤d ∧ d≤1) (he : 0≤e ∧ e≤1)
    (hu : 0≤u ∧ u≤1) (hv : 0≤v ∧ v≤1) (_hw : 0≤w ∧ w≤1)
    (hx : 0≤x ∧ x≤1) (hy : 0≤y ∧ y≤1) (hz : 0≤z ∧ z≤1)
    (_hq : 0≤q ∧ q≤1) (hr : 0≤r ∧ r≤1)
    (h30 : 2*a≤u+v+w) (h32 : 3*b≤x+v+y+z)
    (h41 : 3*c≤v+w+z+q) (h50 : d≤w+q) (h52 : 2*e≤z+q+r)
    : a+b+c+d+e≤u+v+w+x+y+z+q+r := by
  have sa : a=0 ∨ a=1 := by omega
  have sb : b=0 ∨ b=1 := by omega
  have sc : c=0 ∨ c=1 := by omega
  have sd : d=0 ∨ d=1 := by omega
  have se : e=0 ∨ e=1 := by omega
  rcases sa with ha0 | ha1 <;> rcases sb with hb0 | hb1 <;>
    rcases sc with hc0 | hc1 <;> rcases sd with hd0 | hd1 <;>
    rcases se with he0 | he1 <;> omega

/-- Matching endpoints and selected-white hole targets have disjoint images.
    The coordinate/Hall adapters supply the two injections and cardinalities. -/
theorem disjoint_injections_capacity
    (tQ pQ hQ tN pN hN Qsize Nsize : Int)
    (hq : Qsize=tQ+pQ+hQ) (hn : Nsize=tN+pN+hN)
    (selected_injection : tQ≤hN) (mate_injection : pQ≤pN) :
    tN≤Nsize-Qsize+hQ := by omega

/-- Switching colour uses the boundary hole only to determine its state;
    that hole is never added to both payment ledgers. -/
theorem global_colour_switch
    (D deltaB deltaW h54 t54 : Int)
    (black_budget : D≤deltaB) (white_budget : D≤deltaW+t54)
    (local_black : deltaB≤h54) (local_switch : 1≤deltaB → deltaW≤0)
    (h_nonnegative : 0≤h54) (_t_nonnegative : 0≤t54)
    (hole_bit : h54≤1) (disjoint : h54+t54≤1) : D≤0 := by
  by_cases positive : 1≤deltaB
  · have := local_switch positive
    omega
  · omega

/-- The exact half-area value follows from the two-colour count. -/
theorem objective_half_area (J half D : Int) (count : J=half+D)
    (budget : D≤0) : J≤half := by omega

end SubQuorum.ColourSwitchBudget
#print axioms SubQuorum.ColourSwitchBudget.black_case_1
#print axioms SubQuorum.ColourSwitchBudget.black_case_2
#print axioms SubQuorum.ColourSwitchBudget.black_case_3
#print axioms SubQuorum.ColourSwitchBudget.black_case_4
#print axioms SubQuorum.ColourSwitchBudget.black_case_5
#print axioms SubQuorum.ColourSwitchBudget.black_case_6
#print axioms SubQuorum.ColourSwitchBudget.black_local_budget
#print axioms SubQuorum.ColourSwitchBudget.switch_case_1
#print axioms SubQuorum.ColourSwitchBudget.switch_case_2
#print axioms SubQuorum.ColourSwitchBudget.switch_case_3
#print axioms SubQuorum.ColourSwitchBudget.switch_case_4
#print axioms SubQuorum.ColourSwitchBudget.switch_case_5
#print axioms SubQuorum.ColourSwitchBudget.switch_case_6
#print axioms SubQuorum.ColourSwitchBudget.switch_case_7
#print axioms SubQuorum.ColourSwitchBudget.switch_local_budget
#print axioms SubQuorum.ColourSwitchBudget.five_white_hole_budget
#print axioms SubQuorum.ColourSwitchBudget.disjoint_injections_capacity
#print axioms SubQuorum.ColourSwitchBudget.global_colour_switch
#print axioms SubQuorum.ColourSwitchBudget.objective_half_area
