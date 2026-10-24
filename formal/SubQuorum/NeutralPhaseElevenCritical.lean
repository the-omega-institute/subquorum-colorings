import SubQuorum.NeutralPhaseElevenExit

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseElevenCritical

open WidthSixBottomOwner NeutralPhaseTenDescent

def oddOriginMate (coordinate : Int) : Int :=
  if coordinate%2 = 0 then coordinate-1 else coordinate+1

def cardinal (first second : Point) : Prop :=
  (first.1 = second.1 ∧ (first.2+1 = second.2 ∨ second.2+1 = first.2)) ∨
  (first.2 = second.2 ∧ (first.1+1 = second.1 ∨ second.1+1 = first.1))

theorem canonical_terminal_height_is_unique
    (width left right firstHeight secondHeight : Int) (point : Point)
    (hwidth : 6 ≤ width)
    (hfirst : (point = (left,1) ∧ firstHeight = left) ∨
      (point = (right,width) ∧ firstHeight = right))
    (hsecond : (point = (left,1) ∧ secondHeight = left) ∨
      (point = (right,width) ∧ secondHeight = right)) :
    firstHeight = secondHeight := by
  rcases hfirst with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  all_goals rcases hsecond with ⟨hequal,rfl⟩ | ⟨hequal,rfl⟩
  all_goals simp only [Prod.mk.injEq] at hequal
  all_goals omega

theorem phase_eleven_opposite_leg_profile
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hrole : transpose = true ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,width)) ∨
       (flipColumn = true ∧ anchor = (0,1)))) :
    ∃ height : Int, 4 ≤ height ∧ height%2 = 0 ∧
      (∀ column : Int, 0 ≤ column → column ≤ height →
        endpoint width left right
          (pull transpose flipRow flipColumn anchor (1-width,column))) ∧
      support width left right
        (pull transpose flipRow flipColumn anchor (1-width,height+1)) ∧
      (¬ endpoint width left right
        (pull transpose flipRow flipColumn anchor (1-width,height+1))) := by
  rcases hrole with ⟨rfl,rfl,⟨rfl,rfl⟩ | ⟨rfl,rfl⟩⟩
  · refine ⟨left,hleft,hevenLeft,?_,?_,?_⟩
    · intro column hlower hupper
      simp [pull, endpoint]
      omega
    · simp [pull, support]
      omega
    · simp [pull, endpoint]
      omega
  · refine ⟨right,hright,hevenRight,?_,?_,?_⟩
    · intro column hlower hupper
      simp [pull, endpoint]
      omega
    · simp [pull, support]
      omega
    · simp [pull, endpoint]
      omega

theorem active_far_stem_at_critical_corner
    (activeWidth far width : Int) (hfar : 4 ≤ far) :
    endpoint activeWidth (width+2) far (2,activeWidth) := by
  simp [endpoint]
  omega

theorem original_disjointness_bounds_opposite_leg
    {Owner : Type} (owns : Owner → Point → Prop) (activeOwner forcedOwner : Owner)
    (activeWidth width height : Int)
    (hactiveWidth : 6 ≤ activeWidth) (hevenActiveWidth : activeWidth%2 = 0)
    (hevenHeight : height%2 = 0)
    (hunique : ∀ first second point,
      owns first point → owns second point → first = second)
    (hforced : owns forcedOwner (0,0)) (hnotActive : ¬ owns activeOwner (0,0))
    (hactiveFar : owns activeOwner (1-width,activeWidth-2))
    (hrun : ∀ column : Int, 0 ≤ column → column ≤ height →
      owns forcedOwner (1-width,column)) :
    height+4 ≤ activeWidth := by
  have hshort : height < activeWidth-2 := by
    by_cases hshort : height < activeWidth-2
    · exact hshort
    · have hincoming := hrun (activeWidth-2) (by omega) (by omega)
      have hequal := hunique activeOwner forcedOwner (1-width,activeWidth-2)
        hactiveFar hincoming
      exact False.elim (hnotActive (hequal.symm ▸ hforced))
  omega

theorem critical_active_bar_stencil_and_blank
    (activeWidth width height far : Int)
    (hheight : 4 ≤ height) (hbound : height+4 ≤ activeWidth) :
    endpoint activeWidth (width+2) far (1,height+2) ∧
    endpoint activeWidth (width+2) far (1,height+3) ∧
    endpoint activeWidth (width+2) far (1,height+4) ∧
    (¬ endpoint activeWidth (width+2) far (2,height+3)) := by
  repeat' apply And.intro
  all_goals simp [endpoint] <;> omega

theorem critical_support_forces_occupied
    (occupied selected : Point → Prop) (width height : Int)
    (hretention : ¬ occupied (1-width,height+1) → selected (1-width,height+1))
    (hactive : occupied (-width,height+1))
    (hterminal : occupied (1-width,height))
    (hdegree : ∀ point first second, selected point → occupied first → occupied second →
      cardinal point first → cardinal point second → first = second) :
    occupied (1-width,height+1) := by
  classical
  by_cases hoccupied : occupied (1-width,height+1)
  · exact hoccupied
  · have hequal := hdegree (1-width,height+1) (-width,height+1) (1-width,height)
      (hretention hoccupied) hactive hterminal
      (by simp [cardinal]; omega) (by simp [cardinal])
    have hrow := congrArg Prod.fst hequal
    omega

theorem critical_passive_source_exclusion
    (passiveWidth passiveHeight passiveFar width height : Int)
    (hpassiveWidth : 6 ≤ passiveWidth) (hwidth : 6 ≤ width) :
    ¬ endpoint passiveWidth passiveHeight passiveFar (passiveHeight-height-1,1-width) := by
  simp [endpoint]
  omega

theorem critical_partition_corner (width height : Int)
    (hevenWidth : width%2 = 0) (hevenHeight : height%2 = 0) :
    oddOriginMate (1-width) = 2-width ∧
    oddOriginMate (height+1) = height+2 := by
  have hrow : (1-width)%2 = 1 := by omega
  have hcolumn : (height+1)%2 = 1 := by omega
  simp [oddOriginMate, hrow, hcolumn]
  omega

theorem ordinary_partition_corner (width : Int) (hevenWidth : width%2 = 0) :
    oddOriginMate 0 = -1 ∧ oddOriginMate (-width) = -width-1 := by
  have hnegative : (-width)%2 = 0 := by omega
  simp [oddOriginMate, hnegative]

theorem even_phase_eleven_cases (active width : Int)
    (hevenActive : active%2 = 0) (hevenWidth : width%2 = 0)
    (hbound : width+2 ≤ active) :
    active = width+2 ∨ width+4 ≤ active := by omega

end SubQuorum.NeutralPhaseElevenCritical
