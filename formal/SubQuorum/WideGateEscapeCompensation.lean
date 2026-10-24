import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WideGateEscapeCompensation

abbrev Point := Int × Int

def endpoint (depth far : Int) (point : Point) : Prop :=
  (point.1 = 2 ∧ 2 ≤ point.2 ∧ point.2 ≤ depth+2) ∨
  (2 ≤ point.1 ∧ point.1 ≤ 7 ∧ point.2 = depth+2) ∨
  (3 ≤ point.1 ∧ point.1 ≤ 6 ∧ point.2 = depth+1) ∨
  (point.1 = 7 ∧ depth+2-far ≤ point.2 ∧ point.2 ≤ depth+2)

def support (depth far : Int) (point : Point) : Prop :=
  (point.1 = 1 ∧ 2 ≤ point.2 ∧ point.2 ≤ depth+2 ∧ point.2 % 2 = 0) ∨
  (point.1 = 8 ∧ depth+2-far ≤ point.2 ∧ point.2 ≤ depth+2 ∧ point.2 % 2 = 0) ∨
  point = (2,1) ∨ point = (7,depth+1-far) ∨
  (point.1 = 3 ∧ 3 ≤ point.2 ∧ point.2 ≤ depth-1 ∧ point.2 % 2 = 1) ∨
  (point.1 = 6 ∧ depth+3-far ≤ point.2 ∧ point.2 ≤ depth-1 ∧ point.2 % 2 = 1)

def rightEndpoint (width depth far : Int) (point : Point) : Prop :=
  endpoint depth far (point.1,width+1-point.2)

def rightSupport (width depth far : Int) (point : Point) : Prop :=
  support depth far (point.1,width+1-point.2)

theorem north_terminal_collision (occupied : Point → Prop) (depth : Int)
    (hdepth : 4 ≤ depth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ depth → occupied (7-step,1)) :
    occupied (4,1) := by
  exact hstem 3 (by omega) (by omega)

theorem escape_endpoint_bounds (depth far : Int) (point : Point)
    (hdepth : 6 ≤ depth) (hfar : far ≤ depth-2) (hpoint : endpoint depth far point) :
    2 ≤ point.1 ∧ point.1 ≤ 7 ∧ 2 ≤ point.2 ∧ point.2 ≤ depth+2 := by
  dsimp [endpoint] at hpoint
  omega

theorem escape_support_column_bound (depth far : Int) (point : Point)
    (hdepth : 6 ≤ depth) (hfar : 4 ≤ far) (hpoint : support depth far point) :
    point.2 ≤ depth+2 := by
  rcases point with ⟨row,column⟩
  simp only [support, Prod.mk.injEq] at hpoint
  dsimp at hpoint ⊢
  omega

theorem minimum_near_depth (depth far : Int)
    (hfar : 4 ≤ far) (hstrict : far ≤ depth-2) : 6 ≤ depth := by omega

theorem pair_width_frontier (width leftDepth rightDepth : Int)
    (hleft : 6 ≤ leftDepth) (hright : 6 ≤ rightDepth)
    (hseparation : leftDepth+rightDepth ≤ width-4) : 16 ≤ width := by omega

theorem actual_pair_avoids_opposite_boundary (width leftDepth rightDepth : Int)
    (hleft : 6 ≤ leftDepth) (hright : 6 ≤ rightDepth)
    (hseparation : leftDepth+rightDepth ≤ width-4) :
    leftDepth ≤ width-10 ∧ rightDepth ≤ width-10 := by omega

theorem near_stem_separation (width leftDepth rightDepth : Int) :
    leftDepth+2 < width-1-rightDepth ↔ leftDepth+rightDepth ≤ width-4 := by omega

theorem opposite_escapes_disjoint (width leftDepth leftFar rightDepth rightFar : Int)
    (hleftDepth : 6 ≤ leftDepth) (hrightDepth : 6 ≤ rightDepth)
    (hleftFar : leftFar ≤ leftDepth-2) (hrightFar : rightFar ≤ rightDepth-2)
    (hseparation : leftDepth+rightDepth ≤ width-4) (point : Point)
    (hleft : endpoint leftDepth leftFar point) :
    ¬rightEndpoint width rightDepth rightFar point := by
  intro hright
  have hfirst := escape_endpoint_bounds leftDepth leftFar point hleftDepth hleftFar hleft
  have hsecond := escape_endpoint_bounds rightDepth rightFar
    (point.1,width+1-point.2) hrightDepth hrightFar hright
  dsimp at hsecond
  omega

theorem tight_bar_endpoints (width leftDepth leftFar rightDepth rightFar row : Int)
    (htight : leftDepth+rightDepth = width-4) (hrow : 2 ≤ row ∧ row ≤ 7) :
    endpoint leftDepth leftFar (row,leftDepth+2) ∧
      rightEndpoint width rightDepth rightFar (row,leftDepth+3) := by
  constructor
  · exact Or.inr (Or.inl ⟨hrow.1,hrow.2,rfl⟩)
  · dsimp [rightEndpoint,endpoint]
    omega

theorem tight_cross_directions_not_supports
    (width leftDepth leftFar rightDepth rightFar row : Int)
    (htight : leftDepth+rightDepth = width-4)
    (hleft : 6 ≤ leftDepth) (hright : 6 ≤ rightDepth)
    (hleftFar : 4 ≤ leftFar) (hrightFar : 4 ≤ rightFar) :
    ¬support leftDepth leftFar (row,leftDepth+3) ∧
      ¬rightSupport width rightDepth rightFar (row,leftDepth+2) := by
  constructor
  · intro hsupport
    have hbound := escape_support_column_bound leftDepth leftFar
      (row,leftDepth+3) hleft hleftFar hsupport
    dsimp at hbound
    omega
  · intro hsupport
    have hbound := escape_support_column_bound rightDepth rightFar
      (row,width+1-(leftDepth+2)) hright hrightFar hsupport
    dsimp at hbound
    omega

theorem separate_gaps_separate_tile_rows (top first second rowFirst rowSecond : Int)
    (horder : first < second)
    (hfirst : top+8*first+2 ≤ rowFirst ∧ rowFirst ≤ top+8*first+7)
    (hsecond : top+8*second+2 ≤ rowSecond ∧ rowSecond ≤ top+8*second+7) :
    rowFirst/2 < rowSecond/2 := by omega

theorem escape_charge (halfLegSum : Int) :
    (5+halfLegSum)+(halfLegSum-2)-2*(4+halfLegSum) = -5 := by omega

theorem one_escape_gain (boundary : Bool) :
    (5 : Int)-(1+if boundary then 1 else 0) =
      4-(if boundary then 1 else 0) := by cases boundary <;> decide

theorem tight_pair_correction : (2 : Int)*3-12 = -6 := by decide

theorem pair_gain (tight : Bool) :
    (10 : Int)+2*(if tight then 3 else 0)-(2+if tight then 12 else 0) =
      8-(if tight then 6 else 0) := by cases tight <;> decide

theorem simultaneous_selected_budget (gaps tightCount total : Int)
    (hcount : tightCount ≤ gaps) (hledger : total = 13*gaps-6*tightCount) :
    7*gaps ≤ total := by omega

theorem tight_selected_equality (gaps total : Int)
    (hledger : total = 13*gaps-6*gaps) : total = 7*gaps := by omega

theorem west_terminal_collision (occupied : Point → Prop) (depth : Int)
    (hdepth : 4 ≤ depth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ depth → occupied (7,3-step)) :
    occupied (7,0) := by
  exact hstem 3 (by omega) (by omega)

theorem strict_far_frontier (depth far : Int)
    (hdepthEven : depth % 2 = 0) (hfarEven : far % 2 = 0)
    (hprevious : far ≤ depth-2) (hexclusion : far ≠ depth-2) :
    far ≤ depth-4 := by omega

theorem strengthened_pair_width (width leftDepth leftFar rightDepth rightFar : Int)
    (hleftFar : 4 ≤ leftFar) (hrightFar : 4 ≤ rightFar)
    (hleft : leftFar ≤ leftDepth-4) (hright : rightFar ≤ rightDepth-4)
    (hseparation : leftDepth+rightDepth ≤ width-4) :
    8 ≤ leftDepth ∧ 8 ≤ rightDepth ∧ 20 ≤ width := by omega

end SubQuorum.WideGateEscapeCompensation
