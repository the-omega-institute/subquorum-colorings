import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenFourOriginalReturnObstruction

abbrev Point := Int × Int

def blocked (point : Point) : Prop :=
  (point.2 = -1 ∧ 23 ≤ point.1 ∧ point.1 ≤ 33) ∨
  (point.2 = 1 ∧ 25 ≤ point.1 ∧ point.1 ≤ 31) ∨
  point = (22,0) ∨ point = (31,0)

def avoids (fresh : Point → Prop) : Prop :=
  ∀ point, blocked point → ¬fresh point

def adjacent (point other : Point) : Prop :=
  other = (point.1-1,point.2) ∨ other = (point.1+1,point.2) ∨
  other = (point.1,point.2-1) ∨ other = (point.1,point.2+1)

theorem cap_forces_interval (fresh : Point → Prop) (lower upper : Int)
    (hcontains : lower ≤ 25 ∧ 25 ≤ upper)
    (hline : ∀ row, lower ≤ row → row ≤ upper → fresh (row,0))
    (havoid : avoids fresh) : 23 ≤ lower ∧ upper ≤ 30 := by
  have htop : ¬fresh (22,0) := havoid (22,0) (by simp [blocked])
  have hbottom : ¬fresh (31,0) := havoid (31,0) (by simp [blocked])
  constructor
  · by_cases hbound : 23 ≤ lower
    · exact hbound
    · exact False.elim (htop (hline 22 (by omega) (by omega)))
  · by_cases hbound : upper ≤ 30
    · exact hbound
    · exact False.elim (hbottom (hline 31 (by omega) (by omega)))

theorem vertical_leg_normalization (fresh : Point → Prop) (bar depth : Int)
    (south east : Bool) (hdepth : 4 ≤ depth) (heven : depth % 2 = 0)
    (hcontains : min bar (if south then bar+depth else bar-depth) ≤ 25 ∧
      25 ≤ max bar (if south then bar+depth else bar-depth))
    (hline : ∀ row, min bar (if south then bar+depth else bar-depth) ≤ row →
      row ≤ max bar (if south then bar+depth else bar-depth) → fresh (row,0))
    (houter : fresh (bar,if east then 1 else -1))
    (hinner : fresh (bar+(if south then 1 else -1),if east then 1 else -1))
    (havoid : avoids fresh) :
    bar = 23 ∧ south = true ∧ east = true ∧ (depth = 4 ∨ depth = 6) := by
  have hinterval := cap_forces_interval fresh _ _ hcontains hline havoid
  have hbarlower : 23 ≤ bar := by omega
  have hbarupper : bar ≤ 30 := by omega
  cases east with
  | false =>
    have hblocked : blocked (bar,-1) := by simp [blocked]; omega
    exact False.elim (havoid (bar,-1) hblocked houter)
  | true =>
    have hbarshort : bar ≤ 24 := by
      by_cases hbound : bar ≤ 24
      · exact hbound
      · have hblocked : blocked (bar,1) := by simp [blocked]; omega
        exact False.elim (havoid (bar,1) hblocked houter)
    cases south with
    | false =>
      simp only [Bool.false_eq_true, if_false] at hcontains
      omega
    | true =>
      have hbar : bar = 23 := by
        by_cases hbound : bar = 23
        · exact hbound
        · have hbar24 : bar = 24 := by omega
          have hblocked : blocked (25,1) := by simp [blocked]
          have hcollision : fresh (25,1) := by simpa [hbar24] using hinner
          exact False.elim (havoid (25,1) hblocked hcollision)
      have hterminal : bar+depth ≤ 30 := by
        simp only [if_true] at hinterval
        omega
      exact ⟨hbar,rfl,rfl,by omega⟩

theorem first_rotor_terminal_excluded (fresh : Point → Prop) (south : Bool)
    (hfork : fresh (25+(if south then 2 else -2),-1))
    (havoid : avoids fresh) : False := by
  cases south with
  | false => exact havoid (23,-1) (by simp [blocked]) hfork
  | true => exact havoid (27,-1) (by simp [blocked]) hfork

theorem corner_axial_support_cases (depth : Int)
    (hdepth : depth = 4 ∨ depth = 6) : 24+depth = 28 ∨ 24+depth = 30 := by
  omega

theorem three_gate_matching_forces_south (fresh : Point → Prop)
    (hnorth : ¬fresh (27,0)) (hwest : ¬fresh (28,-1)) (heast : ¬fresh (28,1))
    (hmatched : ∃ other, adjacent (28,0) other ∧ fresh other) : fresh (29,0) := by
  rcases hmatched with ⟨other, hneighbour, hother⟩
  simp only [adjacent] at hneighbour
  rcases hneighbour with hfirst | hsecond | hthird | hfourth
  · exact False.elim (hnorth (hfirst ▸ hother))
  · exact hsecond ▸ hother
  · exact False.elim (hwest (hthird ▸ hother))
  · exact False.elim (heast (hfourth ▸ hother))

theorem south_U_terminal_excluded (fresh : Point → Prop) (depth : Int)
    (hdepth : 4 ≤ depth)
    (hstem : ∀ step, 0 ≤ step → step ≤ depth → fresh (28+step,0))
    (havoid : avoids fresh) : False := by
  exact havoid (31,0) (by simp [blocked]) (hstem 3 (by omega) (by omega))

theorem south_rotor_terminal_excluded (fresh : Point → Prop)
    (hfork : fresh (30,-1)) (havoid : avoids fresh) : False := by
  exact havoid (30,-1) (by simp [blocked]) hfork

theorem four_gate_matching_excluded (fresh : Point → Prop)
    (hnorth : ¬fresh (29,0)) (havoid : avoids fresh)
    (hmatched : ∃ other, adjacent (30,0) other ∧ fresh other) : False := by
  rcases hmatched with ⟨other, hneighbour, hother⟩
  simp only [adjacent] at hneighbour
  rcases hneighbour with hfirst | hsecond | hthird | hfourth
  · exact hnorth (hfirst ▸ hother)
  · exact havoid (31,0) (by simp [blocked]) (hsecond ▸ hother)
  · exact havoid (30,-1) (by simp [blocked]) (hthird ▸ hother)
  · exact havoid (30,1) (by simp [blocked]) (hfourth ▸ hother)

theorem four_depth_owner_excluded (fresh : Point → Prop) (havoid : avoids fresh)
    (hroles : (∃ depth, 4 ≤ depth ∧
      ∀ step, 0 ≤ step → step ≤ depth → fresh (28+step,0)) ∨ fresh (30,-1)) : False := by
  rcases hroles with ⟨depth,hdepth,hstem⟩ | hfork
  · exact south_U_terminal_excluded fresh depth hdepth hstem havoid
  · exact south_rotor_terminal_excluded fresh hfork havoid

theorem upward_return_reach_bound (width depth : Int) (hevenWidth : width % 2 = 0)
    (hevenDepth : depth % 2 = 0) (hnoCap : depth < width+6) : depth ≤ width+4 := by
  omega

theorem upward_short_return_receipt (halfDepth : Int) :
    1+2*(halfDepth+1)-(3*halfDepth+1) = 2-halfDepth := by omega

theorem upward_short_group_receipt (halfDepth : Int) :
    4-3+(2-halfDepth) = 3-halfDepth := by omega

end SubQuorum.SecondaryTenFourOriginalReturnObstruction
