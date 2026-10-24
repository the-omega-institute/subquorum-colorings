import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WideMatchedReturnObstruction

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def fixedEndpoint (point : Point) : Prop :=
  endpoint 10 8 4 (11-point.1,point.2-1) ∨
  endpoint 18 20 10 (22-point.2,point.1-1) ∨
  endpoint 6 12 4 (point.2-3,point.1-2) ∨
  endpoint 14 4 4 (20-point.2,point.1-2) ∨
  endpoint 6 6 4 (point.2-14,18-point.1) ∨
  endpoint 8 8 4 (point.2-12,19-point.1)

def forcedEndpoint (point : Point) : Prop := endpoint 6 6 4 (9-point.2,10-point.1)

def eastEndpoint (incident far : Int) (point : Point) : Prop :=
  endpoint 6 incident far (incident+10-point.2,point.1-3)

def finalEndpoint (far : Int) (point : Point) : Prop :=
  endpoint 6 4 far (point.2-12,point.1-4)

def lateEndpoint (far : Int) (point : Point) : Prop :=
  fixedEndpoint point ∨ forcedEndpoint point ∨
  eastEndpoint 8 4 point ∨ finalEndpoint far point

theorem the_first_forced_support_has_three_fixed_neighbors :
    support 6 12 4 (0,7) ∧ ¬fixedEndpoint (9,3) ∧
      fixedEndpoint (8,3) ∧ fixedEndpoint (9,2) ∧ fixedEndpoint (10,3) := by
  simp [support, fixedEndpoint, endpoint]

theorem an_overwide_first_consumer_hits_the_original_near_stem
    (width far : Int) (hwidth : 8 ≤ width) :
    endpoint width 6 far (0,7) ∧ fixedEndpoint (3,9) := by
  unfold fixedEndpoint endpoint
  dsimp
  omega

theorem an_overlong_first_far_leg_hits_the_corner_bar
    (far : Int) (hfar : 6 ≤ far) :
    endpoint 6 6 far (5,6) ∧ fixedEndpoint (4,4) := by
  unfold fixedEndpoint endpoint
  dsimp
  omega

theorem the_second_forced_support_has_two_distinct_fixed_neighbors :
    support 6 12 4 (7,2) ∧ ¬fixedEndpoint (4,10) ∧
      ¬forcedEndpoint (4,10) ∧ fixedEndpoint (3,10) ∧ forcedEndpoint (4,9) := by
  simp [support, fixedEndpoint, forcedEndpoint, endpoint]

theorem a_short_horizontal_corner_has_an_unconsumable_support :
    support 6 4 4 (5,1) ∧ ¬fixedEndpoint (9,10) ∧ ¬forcedEndpoint (9,10) ∧
      fixedEndpoint (9,11) ∧ fixedEndpoint (10,10) ∧ forcedEndpoint (9,9) ∧
      endpoint 6 4 4 (4,1) := by
  simp [support, fixedEndpoint, forcedEndpoint, endpoint]

theorem the_late_outer_bar_support_has_two_fixed_neighbors :
    support 8 8 4 (0,9) ∧ ¬fixedEndpoint (10,12) ∧
      ¬forcedEndpoint (10,12) ∧ fixedEndpoint (11,12) ∧ fixedEndpoint (10,11) := by
  unfold support fixedEndpoint forcedEndpoint endpoint
  dsimp
  omega

theorem exactly_the_two_short_other_legs_can_survive_the_last_bound
    (far halfFar : Int) (heven : far = 2*halfFar)
    (hminimum : 4 ≤ far) (hmaximum : far < 8) : far = 4 ∨ far = 6 := by
  omega

theorem the_last_corner_fills_the_missing_boundary_point
    (far : Int) (hfar : 4 ≤ far) : finalEndpoint far (10,16) := by
  unfold finalEndpoint endpoint
  dsimp
  omega

theorem the_entire_rectangle_boundary_is_original_endpoints
    (far row column : Int) (hfar : 4 ≤ far)
    (hrow : 9 ≤ row ∧ row ≤ 12) (hcolumn : 16 ≤ column ∧ column ≤ 19)
    (hboundary : row = 9 ∨ row = 12 ∨ column = 16 ∨ column = 19) :
    lateEndpoint far (row,column) := by
  have hright : ∀ boundaryRow, 9 ≤ boundaryRow → boundaryRow ≤ 12 →
      lateEndpoint far (boundaryRow,19) := by
    intro boundaryRow hlower hupper
    unfold lateEndpoint
    left
    unfold fixedEndpoint
    right; right; right; left
    unfold endpoint
    dsimp
    omega
  by_cases htop : row = 9
  · subst row
    by_cases hcorner : column = 19
    · subst column
      exact hright 9 (by omega) (by omega)
    · unfold lateEndpoint
      right; right; left
      unfold eastEndpoint endpoint
      dsimp
      omega
  by_cases hbottom : row = 12
  · subst row
    by_cases hcorner : column = 19
    · subst column
      exact hright 12 (by omega) (by omega)
    · unfold lateEndpoint
      left
      unfold fixedEndpoint
      right; right; right; right; left
      unfold endpoint
      dsimp
      omega
  by_cases hlast : column = 19
  · subst column
    exact hright row hrow.1 hrow.2
  have hleft : column = 16 := by omega
  subst column
  have hmiddle : row = 10 ∨ row = 11 := by omega
  rcases hmiddle with hmiddle | hmiddle
  · subst row
    unfold lateEndpoint
    right; right; right
    exact the_last_corner_fills_the_missing_boundary_point far hfar
  · subst row
    unfold lateEndpoint
    left
    simp [fixedEndpoint, endpoint]

theorem the_interior_support_is_unowned_and_forced
    (far : Int) :
    support 8 8 4 (5,8) ∧ ¬lateEndpoint far (11,17) ∧
      fixedEndpoint (11,16) ∧ fixedEndpoint (12,17) := by
  unfold support lateEndpoint fixedEndpoint forcedEndpoint eastEndpoint finalEndpoint endpoint
  dsimp
  omega

theorem a_confined_two_by_two_set_cannot_have_a_three_unit_span
    (firstRow firstColumn secondRow secondColumn : Int)
    (hfirst : 10 ≤ firstRow ∧ firstRow ≤ 11 ∧ 17 ≤ firstColumn ∧ firstColumn ≤ 18)
    (hsecond : 10 ≤ secondRow ∧ secondRow ≤ 11 ∧
      17 ≤ secondColumn ∧ secondColumn ≤ 18) :
    ¬(firstRow+3 ≤ secondRow ∨ secondRow+3 ≤ firstRow ∨
      firstColumn+3 ≤ secondColumn ∨ secondColumn+3 ≤ firstColumn) := by
  omega

end SubQuorum.WideMatchedReturnObstruction
