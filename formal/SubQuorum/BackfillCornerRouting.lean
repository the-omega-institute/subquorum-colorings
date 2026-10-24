import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.BackfillCornerRouting

open WidthSixBottomOwner

def cornerBlockers : List Point :=
  [(-1,0),(-1,-1),(-1,-2),(-1,-3),(-1,1),(0,1),(1,1),(2,1)]

theorem backfill_corner_has_no_rotor_owner : rotorOwners cornerBlockers = [] := by decide

set_option maxHeartbeats 2000000 in
theorem north_east_blocked_U_role_catalogue
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (heast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,1))) :
    (transpose = false ∧ flipRow = false ∧
      ((flipColumn = true ∧ anchor = (0,1)) ∨
       (flipColumn = false ∧ anchor = (0,width)))) ∨
    (transpose = true ∧ flipRow = true ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width)))) ∨
    (transpose = false ∧ flipRow = true ∧
      (anchor = (left,1) ∨ anchor = (right,width))) ∨
    (transpose = true ∧ flipRow = false ∧
      (anchor = (left,1) ∨ anchor = (right,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals cases transpose <;> cases flipRow <;> cases flipColumn <;>
    simp [endpoint, pull, Prod.mk.injEq] at hnorth heast ⊢ <;> omega

def companionBarrier (width incident : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ -incident-1 ≤ point.2 ∧ point.2 ≤ -1) ∨
  (0 ≤ point.1 ∧ point.1 ≤ width-1 ∧
    (point.2 = -incident-1 ∨ point.2 = -incident))

def rootBarrier (width incident : Int) (point : Point) : Prop :=
  (point.2 = 0 ∧ 0 ≤ point.1 ∧ point.1 ≤ incident) ∨
  ((point.1 = incident-1 ∨ point.1 = incident) ∧
    1-width ≤ point.2 ∧ point.2 ≤ 0)

theorem companion_barrier_is_original
    (width incident far : Int) (point : Point)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hbarrier : companionBarrier width incident point) :
    endpoint width incident far (point.2+incident+1,point.1+1) := by
  simp [companionBarrier, endpoint] at hbarrier ⊢
  omega

theorem root_barrier_is_original
    (width far incident : Int) (point : Point)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident)
    (hbarrier : rootBarrier width incident point) :
    endpoint width far incident (incident-point.1,point.2+width) := by
  simp [rootBarrier, endpoint] at hbarrier ⊢
  omega

theorem horizontal_bar_corner_has_south_run
    (width left incident row : Int)
    (hwidth : 6 ≤ width) (hrow : 1 ≤ row) (hend : row ≤ incident+1) :
    endpoint width left incident (row-1,width) := by
  simp [endpoint]
  omega

theorem vertical_bar_corner_has_south_run
    (width left right row : Int)
    (hrow : 1 ≤ row) (hend : row ≤ width) :
    endpoint width left right (0,row) := by
  simp [endpoint]
  omega

theorem south_terminal_has_complete_run
    (width far incident row : Int)
    (hwidth : 6 ≤ width) (hrow : 1 ≤ row) (hend : row ≤ incident+1) :
    endpoint width far incident (incident+1-row,width) := by
  simp [endpoint]
  omega

theorem west_terminal_has_complete_run_and_bar
    (width incident far row column : Int)
    (hwidth : 6 ≤ width) (hcolumn : -incident-1 ≤ column) (hend : column ≤ -1)
    (hrow : 1 ≤ row) (hbarEnd : row ≤ width) :
    endpoint width incident far (column+incident+1,1) ∧
    endpoint width incident far (1,row) := by
  simp [endpoint]
  omega

theorem horizontal_bar_corner_has_original_cap
    (width left right : Int)
    (hwidth : 6 ≤ width) (hright : 4 ≤ right) :
    endpoint width left right (1,width-1) ∧
    endpoint width left right (1,width) ∧
    endpoint width left right (2,width) ∧
    ¬ endpoint width left right (2,width-1) ∧
    ¬ support width left right (2,width-1) := by
  simp [endpoint, support]
  omega

theorem south_terminal_cannot_open_right
    (owns : Point → Prop) (rootWidth rootHeight incident : Int)
    (hwidth : 6 ≤ rootWidth) (hheight : 4 ≤ rootHeight)
    (hincident : 4 ≤ incident)
    (hrun : ∀ row, 1 ≤ row → row ≤ incident+1 → owns (row,-1))
    (hbar : owns (incident,0))
    (hdisjoint : ∀ point, rootBarrier rootWidth rootHeight point → ¬ owns point) : False := by
  by_cases hlong : rootHeight-1 ≤ incident+1
  · exact hdisjoint (rootHeight-1,-1)
      (by simp [rootBarrier]; omega)
      (hrun (rootHeight-1) (by omega) hlong)
  · exact hdisjoint (incident,0)
      (by simp [rootBarrier]; omega) hbar

theorem west_terminal_cannot_open_up
    (owns : Point → Prop) (companionWidth companionHeight incident : Int)
    (hwidth : 6 ≤ companionWidth) (hheight : 4 ≤ companionHeight)
    (hincident : 4 ≤ incident)
    (hrun : ∀ column, -incident-1 ≤ column → column ≤ -1 → owns (1,column))
    (hbar : owns (0,-incident))
    (hdisjoint : ∀ point, companionBarrier companionWidth companionHeight point →
      ¬ owns point) : False := by
  by_cases hlong : companionHeight ≤ incident+1
  · exact hdisjoint (1,-companionHeight)
      (by simp [companionBarrier]; omega)
      (hrun (-companionHeight) (by omega) (by omega))
  · exact hdisjoint (0,-incident)
      (by simp [companionBarrier]; omega) hbar

theorem south_run_has_strict_depth_drop
    (owns : Point → Prop) (rootWidth rootHeight incident : Int)
    (hwidth : 6 ≤ rootWidth) (hheight : 4 ≤ rootHeight)
    (hevenRoot : rootHeight%2 = 0) (hevenIncident : incident%2 = 0)
    (hrun : ∀ row, 1 ≤ row → row ≤ incident+1 → owns (row,-1))
    (hdisjoint : ∀ point, rootBarrier rootWidth rootHeight point → ¬ owns point) :
    incident ≤ rootHeight-4 := by
  have hshort : incident+1 < rootHeight-1 := by
    by_cases hshort : incident+1 < rootHeight-1
    · exact hshort
    · exact False.elim (hdisjoint (rootHeight-1,-1)
        (by simp [rootBarrier]; omega)
        (hrun (rootHeight-1) (by omega) (by omega)))
  omega

theorem vertical_bar_has_strict_width_drop
    (owns : Point → Prop) (rootWidth rootHeight width : Int)
    (hrootWidth : 6 ≤ rootWidth) (hrootHeight : 4 ≤ rootHeight)
    (hbar : ∀ row, 1 ≤ row → row ≤ width → owns (row,-1))
    (hdisjoint : ∀ point, rootBarrier rootWidth rootHeight point → ¬ owns point) :
    width ≤ rootHeight-2 := by
  by_cases hbound : width ≤ rootHeight-2
  · exact hbound
  · exact False.elim (hdisjoint (rootHeight-1,-1)
      (by simp [rootBarrier]; omega)
      (hbar (rootHeight-1) (by omega) (by omega)))

theorem west_run_has_strict_incident_drop
    (owns : Point → Prop) (companionWidth companionHeight incident : Int)
    (hwidth : 6 ≤ companionWidth) (hheight : 4 ≤ companionHeight)
    (hrun : ∀ column, -incident-1 ≤ column → column ≤ -1 → owns (1,column))
    (hdisjoint : ∀ point, companionBarrier companionWidth companionHeight point →
      ¬ owns point) : incident ≤ companionHeight-2 := by
  by_cases hbound : incident ≤ companionHeight-2
  · exact hbound
  · exact False.elim (hdisjoint (1,-companionHeight)
      (by simp [companionBarrier]; omega)
      (hrun (-companionHeight) (by omega) (by omega)))

theorem west_bar_root_bar_tradeoff
    (owns : Point → Prop) (rootWidth rootHeight width incident : Int)
    (hrootHeight : 4 ≤ rootHeight) (hincident : 4 ≤ incident)
    (hbar : ∀ row, 1 ≤ row → row ≤ width → owns (row,-incident))
    (hdisjoint : ∀ point, rootBarrier rootWidth rootHeight point → ¬ owns point) :
    width ≤ rootHeight-2 ∨ rootWidth ≤ incident := by
  by_cases hshort : width ≤ rootHeight-2
  · exact Or.inl hshort
  · right
    by_cases hwide : rootWidth ≤ incident
    · exact hwide
    · exact False.elim (hdisjoint (rootHeight-1,-incident)
        (by simp [rootBarrier]; omega)
        (hbar (rootHeight-1) (by omega) (by omega)))

theorem shallow_root_excludes_other_role_bounds
    (rootHeight width incident : Int)
    (hshallow : rootHeight ≤ 6) (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    ¬ incident ≤ rootHeight-4 ∧ ¬ width ≤ rootHeight-2 := by omega

theorem shallow_west_terminal_requires_wider_companion
    (rootWidth rootHeight companionHeight width incident : Int)
    (hshallow : rootHeight ≤ 6) (hwidth : 6 ≤ width)
    (hdrop : incident ≤ companionHeight-2)
    (htradeoff : width ≤ rootHeight-2 ∨ rootWidth ≤ incident) :
    rootWidth+2 ≤ companionHeight := by omega

theorem horizontal_bar_clears_companion_width
    (owns : Point → Prop) (companionWidth companionHeight width : Int)
    (hwidth : 6 ≤ companionWidth) (hheight : 4 ≤ companionHeight)
    (hbar : ∀ column, -width ≤ column → column ≤ -1 → owns (1,column))
    (hdisjoint : ∀ point, companionBarrier companionWidth companionHeight point →
      ¬ owns point) : width ≤ companionHeight-2 ∨ width = companionHeight-1 := by
  by_cases hshort : width ≤ companionHeight-2
  · exact Or.inl hshort
  · by_cases hedge : width = companionHeight-1
    · exact Or.inr hedge
    · exact False.elim (hdisjoint (1,-companionHeight)
        (by simp [companionBarrier]; omega)
        (hbar (-companionHeight) (by omega) (by omega)))

theorem horizontal_even_bar_clears_companion_width
    (width companionHeight : Int)
    (hevenWidth : width%2 = 0) (hevenCompanion : companionHeight%2 = 0)
    (hbound : width ≤ companionHeight-2 ∨ width = companionHeight-1) :
    width ≤ companionHeight-2 := by omega

theorem south_bar_clears_companion_height
    (owns : Point → Prop) (companionWidth companionHeight width incident : Int)
    (hheight : 4 ≤ companionHeight) (hincident : 4 ≤ incident)
    (hbar : ∀ column, -width ≤ column → column ≤ -1 → owns (incident,column))
    (hdisjoint : ∀ point, companionBarrier companionWidth companionHeight point →
      ¬ owns point) : width ≤ companionHeight-1 ∨ companionWidth ≤ incident := by
  by_cases hshort : width ≤ companionHeight-1
  · exact Or.inl hshort
  · right
    by_cases hbelow : companionWidth ≤ incident
    · exact hbelow
    · exact False.elim (hdisjoint (incident,-companionHeight)
        (by simp [companionBarrier]; omega)
        (hbar (-companionHeight) (by omega) (by omega)))

def farRootStem (width incident far : Int) (point : Point) : Prop :=
  point.2 = 1-width ∧ incident-far ≤ point.1 ∧ point.1 ≤ incident

theorem far_root_stem_is_original
    (width incident far : Int) (point : Point)
    (hwidth : 6 ≤ width) (hbarrier : farRootStem width incident far point) :
    endpoint width far incident (incident-point.1,point.2+width) := by
  simp [farRootStem, endpoint] at hbarrier ⊢
  omega

theorem endpoint_at_minus_five_clears_width_six_far_stem
    (owns : Point → Prop) (rootHeight farHeight row : Int)
    (hrow : row ≤ rootHeight) (hown : owns (row,-5))
    (hdisjoint : ∀ point, farRootStem 6 rootHeight farHeight point → ¬ owns point) :
    row < rootHeight-farHeight := by
  by_cases hclear : row < rootHeight-farHeight
  · exact hclear
  · exact False.elim (hdisjoint (row,-5)
      (by simp [farRootStem]; omega) hown)

theorem width_six_low_point_requires_height_twelve
    (rootHeight farHeight row : Int)
    (hevenRoot : rootHeight%2 = 0) (hfar : 4 ≤ farHeight) (hrow : 6 ≤ row)
    (hclear : row < rootHeight-farHeight) : 12 ≤ rootHeight := by omega

end SubQuorum.BackfillCornerRouting
