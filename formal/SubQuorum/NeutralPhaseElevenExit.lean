import SubQuorum.NeutralPhaseTenDescent

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseElevenExit

open WidthSixBottomOwner NeutralPhaseTenDescent

def phaseElevenAtForcedPoint (flipRow flipColumn : Bool) (anchor : Point) : Prop :=
  anchor.1%2 = (if flipRow then 1 else 0) ∧
  anchor.2%2 = (if flipColumn then 1 else 0)

theorem phase_eleven_parity_of_receiver_origin (flipRow flipColumn : Bool)
    (anchor : Point)
    (hrow : (pulledReceiverOrigin flipRow flipColumn anchor).1%2 = 1)
    (hcolumn : (pulledReceiverOrigin flipRow flipColumn anchor).2%2 = 1) :
    phaseElevenAtForcedPoint flipRow flipColumn anchor := by
  cases flipRow <;> cases flipColumn <;>
    simp [pulledReceiverOrigin, phaseElevenAtForcedPoint] at hrow hcolumn ⊢ <;> omega

set_option maxHeartbeats 2000000 in
theorem phase_eleven_forced_owner_role
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,0)))
    (hnorthwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,-1)))
    (hsoutheast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,1)))
    (hphase : phaseElevenAtForcedPoint flipRow flipColumn anchor) :
    (transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (right,width)) ∨
       (flipColumn = true ∧ anchor = (left,1)))) ∨
    (transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1)))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, phaseElevenAtForcedPoint, Prod.mk.injEq] at hwest hsouth hnorthwest hsoutheast hphase ⊢ <;> omega

theorem west_facing_north_terminal_hits_active_source
    (width left right active : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hactive : 4 ≤ active)
    (hrole : transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (right,width)) ∨
       (flipColumn = true ∧ anchor = (left,1)))) :
    ∃ point : Point,
      (point = (2-active,0) ∨ (point.2 = -1 ∧ 1-active ≤ point.1 ∧ point.1 ≤ 1)) ∧
      endpoint width left right (pull transpose flipRow flipColumn anchor point) := by
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  · by_cases hshort : right ≤ active
    · refine ⟨(1-right,-1),Or.inr ⟨rfl,by omega,by omega⟩,?_⟩
      simp [pull, endpoint]
      omega
    · refine ⟨(2-active,0),Or.inl rfl,?_⟩
      simp [pull, endpoint]
      omega
  · by_cases hshort : left ≤ active
    · refine ⟨(1-left,-1),Or.inr ⟨rfl,by omega,by omega⟩,?_⟩
      simp [pull, endpoint]
      omega
    · refine ⟨(2-active,0),Or.inl rfl,?_⟩
      simp [pull, endpoint]
      omega

theorem physical_phase_eleven_owner_is_corner
    {Owner : Type} (owns : Owner → Point → Prop) (activeOwner passive forced : Owner)
    (width left right active : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hactive : 4 ≤ active)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forced (0,0))
    (hnotActive : ¬ owns activeOwner (0,0)) (hnotPassive : ¬ owns passive (0,0))
    (hmodel : ∀ point, owns forced point ↔
      endpoint width left right (pull transpose flipRow flipColumn anchor point))
    (hwest : owns activeOwner (0,-1)) (hsouth : owns passive (1,0))
    (hnorthwest : owns activeOwner (-1,-1)) (hsoutheast : owns passive (1,1))
    (hactiveBar : owns activeOwner (2-active,0))
    (hactiveStem : ∀ row : Int, 1-active ≤ row → row ≤ 1 → owns activeOwner (row,-1))
    (hrow : (pulledReceiverOrigin flipRow flipColumn anchor).1%2 = 1)
    (hcolumn : (pulledReceiverOrigin flipRow flipColumn anchor).2%2 = 1) :
    transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1))) := by
  have hroot := (hmodel (0,0)).mp hforced
  simp [pull] at hroot
  obtain ⟨hwest',hsouth',hnorthwest',hsoutheast'⟩ :=
    original_owner_excludes_foreign_endpoints owns activeOwner passive forced
      width left right anchor transpose flipRow flipColumn hunique hforced
      hnotActive hnotPassive hmodel hwest hsouth hnorthwest hsoutheast
  have hrole := phase_eleven_forced_owner_role width left right anchor
    transpose flipRow flipColumn hwidth hleft hright hevenWidth hevenLeft hevenRight
    hroot hwest' hsouth' hnorthwest' hsoutheast'
    (phase_eleven_parity_of_receiver_origin flipRow flipColumn anchor hrow hcolumn)
  rcases hrole with hterminal | hcorner
  · obtain ⟨point,hpoint,hendpoint⟩ := west_facing_north_terminal_hits_active_source
      width left right active anchor transpose flipRow flipColumn hwidth hleft hright
      hactive hterminal
    have hactivePoint : owns activeOwner point := by
      rcases hpoint with rfl | ⟨hcolumn,hlower,hupper⟩
      · exact hactiveBar
      · simpa only [← hcolumn] using hactiveStem point.1 hlower hupper
    have hequal := hunique activeOwner forced point hactivePoint ((hmodel point).mpr hendpoint)
    exact False.elim (hnotActive (hequal.symm ▸ hforced))
  · exact hcorner

theorem phase_eleven_corner_exit_geometry
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hrole : transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1)))) :
    endpoint width left right (pull transpose flipRow flipColumn anchor (-1,0)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (0,0)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (-1,1)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (0,1)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (0,2)) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-1,2))) ∧
    (¬ support width left right (pull transpose flipRow flipColumn anchor (-1,1))) ∧
    (¬ support width left right (pull transpose flipRow flipColumn anchor (0,1))) ∧
    (¬ support width left right (pull transpose flipRow flipColumn anchor (0,2))) ∧
    (¬ support width left right (pull transpose flipRow flipColumn anchor (-1,2))) ∧
    support width left right (pull transpose flipRow flipColumn anchor (-width,0)) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-width,0))) ∧
    (∀ row : Int, 1-width ≤ row → row ≤ 0 →
      endpoint width left right (pull transpose flipRow flipColumn anchor (row,0))) := by
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  all_goals repeat' apply And.intro
  all_goals first
    | (intro row hlower hupper; simp [pull, endpoint]; omega)
    | (simp [pull, endpoint, support]; omega)

theorem phase_eleven_corner_width_bound
    (active width : Int) (hactive : 4 ≤ active)
    (hevenActive : active%2 = 0) (hevenWidth : width%2 = 0)
    (hbarDisjoint : ¬ (1-width ≤ 2-active ∧ 2-active ≤ 0)) :
    width+2 ≤ active := by omega

theorem original_corner_disjointness_implies_width_bound
    {Owner : Type} (owns : Owner → Point → Prop) (activeOwner forcedOwner : Owner)
    (active width : Int) (hactive : 4 ≤ active)
    (hevenActive : active%2 = 0) (hevenWidth : width%2 = 0)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forcedOwner (0,0)) (hnotActive : ¬ owns activeOwner (0,0))
    (hbar : owns activeOwner (2-active,0))
    (hrun : ∀ row : Int, 1-width ≤ row → row ≤ 0 → owns forcedOwner (row,0)) :
    width+2 ≤ active := by
  apply phase_eleven_corner_width_bound active width hactive hevenActive hevenWidth
  intro ⟨hlower,hupper⟩
  have hequal := hunique activeOwner forcedOwner (2-active,0) hbar
    (hrun (2-active) hlower hupper)
  exact hnotActive (hequal.symm ▸ hforced)

theorem passive_source_excludes_second_forced_point
    (passiveWidth passiveHeight passiveFar width : Int)
    (hpassiveWidth : 6 ≤ passiveWidth) (hwidth : 6 ≤ width) :
    ¬ endpoint passiveWidth passiveHeight passiveFar (passiveHeight,-width) := by
  simp [endpoint]
  omega

theorem shortest_legs_exclude_phase_eleven (active width : Int)
    (hactive : active = 4 ∨ active = 6) (hwidth : 6 ≤ width)
    (hbound : width+2 ≤ active) : False := by omega

theorem long_corner_continuation_geometry
    (activeWidth active far width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hactiveWidth : 6 ≤ activeWidth) (hwidth : 6 ≤ width)
    (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hlong : width+4 ≤ active)
    (hevenActive : active%2 = 0) (hevenWidth : width%2 = 0)
    (hrole : transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1)))) :
    support activeWidth active far (active-1-width,2) ∧
    endpoint activeWidth active far (active-1-width,1) ∧
    (¬ endpoint activeWidth active far (active-1-width,2)) ∧
    support width left right (pull transpose flipRow flipColumn anchor (-width,0)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (1-width,0)) ∧
    (¬ endpoint width left right (pull transpose flipRow flipColumn anchor (-width,0))) := by
  have hodd : (active-1-width)%2 = 1 := by omega
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  all_goals repeat' apply And.intro
  all_goals simp [pull, endpoint, support, hodd] <;> omega

theorem long_corner_has_tagged_endpoint_stencil
    (activeWidth active far width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hactiveWidth : 6 ≤ activeWidth) (hwidth : 6 ≤ width)
    (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hlong : width+4 ≤ active)
    (hrole : transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1)))) :
    endpoint activeWidth active far (active-2-width,1) ∧
    endpoint activeWidth active far (active-1-width,1) ∧
    endpoint activeWidth active far (active-width,1) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (1-width,0)) ∧
    endpoint width left right (pull transpose flipRow flipColumn anchor (1-width,1)) := by
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  all_goals repeat' apply And.intro
  all_goals simp [pull, endpoint] <;> omega

end SubQuorum.NeutralPhaseElevenExit
