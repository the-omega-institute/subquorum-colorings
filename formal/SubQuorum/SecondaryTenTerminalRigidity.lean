import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenTerminalRigidity

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

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def secondary (bottom width : Int) (point : Point) : Prop :=
  endpoint width 10 4 (point.1-(bottom-11),point.2-5)

def upward (bottom width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth (width+2) far (width+9-point.2,bottom-4-point.1)

def successor (bottom width breadth near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (width+7-point.2,bottom-5-point.1)

def rotorA (bottom tip : Int) (point : Point) : Prop :=
  (point.1 = bottom-9 ∧ point.2 = tip-2) ∨
  (point.1 = bottom-8 ∧ tip-2 ≤ point.2 ∧ point.2 ≤ tip) ∨
  (point.1 = bottom-7 ∧ tip-3 ≤ point.2 ∧ point.2 ≤ tip-1) ∨
  (point.1 = bottom-6 ∧ point.2 = tip-1)

def rotorB (bottom tip : Int) (point : Point) : Prop :=
  (point.1 = bottom-9 ∧ point.2 = tip) ∨
  (point.1 = bottom-8 ∧ tip-2 ≤ point.2 ∧ point.2 ≤ tip) ∨
  (point.1 = bottom-7 ∧ tip-1 ≤ point.2 ∧ point.2 ≤ tip+1) ∨
  (point.1 = bottom-6 ∧ point.2 = tip-1)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem short_leg_terminal_bounds (width near : Int)
    (hwidth : width % 2 = 0) (hnear : near % 2 = 0)
    (hlow : 4 ≤ near) (hshort : near < width) :
    9 ≤ width+7-near ∧ width+7-near ≤ width+3 ∧ (width+7-near) % 2 = 1 := by
  omega

theorem the_first_forced_point_is_a_successor_support
    (bottom width breadth near far : Int) (hnear : 4 ≤ near) :
    support breadth near far (near+1,1) ∧
      successor bottom width breadth near far (bottom-6,width+7-near) := by
  unfold support successor endpoint
  dsimp
  omega

theorem the_first_forced_point_has_no_prescribed_owner
    (bottom width breadth near far upwardBreadth upwardFar : Int)
    (hbreadth : 6 ≤ breadth)
    (hupward : 6 ≤ upwardBreadth) (hlow : 4 ≤ near) (hshort : near ≤ width-2) :
    ¬returning bottom (bottom-6,width+6-near) ∧
      ¬secondary bottom width (bottom-6,width+6-near) ∧
      ¬upward bottom width upwardBreadth upwardFar (bottom-6,width+6-near) ∧
      ¬successor bottom width breadth near far (bottom-6,width+6-near) := by
  unfold returning secondary upward successor endpoint
  dsimp
  omega

theorem first_site_north_and_south_blockers
    (bottom width breadth far tip : Int) (hlow : 9 ≤ tip) (hhigh : tip ≤ width+3) :
    secondary bottom width (bottom-10,tip-1) ∧
      upward bottom width breadth far (bottom-5,tip-1) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem west_rotor_bottom_blockers
    (bottom width breadth far tip : Int) (hlow : 9 ≤ tip)
    (hhigh : tip ≤ width+3) (heven : tip % 2 = 1) :
    upward bottom width breadth far (bottom-5,tip-2) ∧
      (secondary bottom width (bottom-5,tip-3) ∨
        upward bottom width breadth far (bottom-5,tip-3)) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem rotor_top_support_sites_are_not_their_own_endpoints (bottom tip : Int) :
    ¬rotorA bottom tip (bottom-9,tip) ∧ ¬rotorB bottom tip (bottom-9,tip-2) := by
  unfold rotorA rotorB
  dsimp
  omega

theorem rotor_top_support_anchors_are_owned (bottom tip : Int) :
    rotorA bottom tip (bottom-8,tip) ∧ rotorB bottom tip (bottom-8,tip-2) := by
  unfold rotorA rotorB
  dsimp
  omega

theorem both_rotor_top_supports_have_a_secondary_north_neighbor
    (bottom width tip : Int) (hlow : 9 ≤ tip) (hhigh : tip ≤ width+3) :
    secondary bottom width (bottom-10,tip) ∧
      secondary bottom width (bottom-10,tip-2) := by
  unfold secondary endpoint
  dsimp
  omega

theorem rotor_top_supports_are_in_the_forbidden_top_interval
    (width tip : Int) (hlow : 9 ≤ tip) (hhigh : tip ≤ width+3) :
    (7 ≤ tip ∧ tip ≤ width+3) ∧ (7 ≤ tip-2 ∧ tip-2 ≤ width+3) := by
  omega

theorem forbidden_top_site_has_no_prescribed_owner
    (bottom width breadth near far upwardBreadth upwardFar column : Int)
    (hbreadth : 6 ≤ breadth) (hupward : 6 ≤ upwardBreadth)
    (hlow : 7 ≤ column) (hhigh : column ≤ width+3) :
    ¬returning bottom (bottom-9,column) ∧
      ¬secondary bottom width (bottom-9,column) ∧
      ¬upward bottom width upwardBreadth upwardFar (bottom-9,column) ∧
      ¬successor bottom width breadth near far (bottom-9,column) := by
  unfold returning secondary upward successor endpoint
  dsimp
  omega

theorem three_top_rotor_blockers_are_secondary_owned
    (bottom width column : Int) (hlow : 7 ≤ column) (hhigh : column ≤ width+3) :
    secondary bottom width (bottom-11,column+1) ∧
      secondary bottom width (bottom-10,column+2) ∧
      secondary bottom width (bottom-11,column-1) := by
  unfold secondary endpoint
  dsimp
  omega

theorem fourth_top_rotor_blocker_is_secondary_owned
    (bottom width column : Int) (hlow : 7 ≤ column) (hhigh : column ≤ width+3) :
    (column = 7 ∧ secondary bottom width (bottom-9,column-1)) ∨
      (8 ≤ column ∧ secondary bottom width (bottom-10,column-2)) := by
  unfold secondary endpoint
  dsimp
  omega

theorem top_U_bar_blockers_are_owned
    (bottom width breadth far column : Int)
    (hlow : 7 ≤ column) (hhigh : column ≤ width+4) :
    secondary bottom width (bottom-10,column) ∧
      upward bottom width breadth far (bottom-5,column) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem every_wide_U_bar_reaches_both_blocker_distances
    (width near far : Int) (hwidth : 6 ≤ width) :
    endpoint width near far (0,2) ∧ endpoint width near far (0,5) := by
  unfold endpoint
  dsimp
  omega

theorem a_top_original_support_must_be_consumed
    (bottom column : Int) (occupied endpointAt : Point → Prop)
    (hnorth : occupied (bottom-10,column))
    (hretain : ¬endpointAt (bottom-9,column) →
      ∀ point, adjacent (bottom-9,column) point → occupied point → point = (bottom-8,column)) :
    endpointAt (bottom-9,column) := by
  by_cases hpoint : endpointAt (bottom-9,column)
  · exact hpoint
  · have hequal := hretain hpoint (bottom-10,column)
      (by unfold adjacent; dsimp; omega) hnorth
    have hrow := congrArg Prod.fst hequal
    dsimp at hrow
    omega

theorem rigid_terminal_and_both_original_supports
    (bottom width breadth far : Int) (hwidth : 6 ≤ width) (heven : width % 2 = 0) :
    successor bottom width breadth width far (bottom-6,7) ∧
      support breadth width far (width+1,1) ∧ support breadth width far (width,0) ∧
      secondary bottom width (bottom-6,6) ∧
      upward bottom width breadth far (bottom-5,7) := by
  unfold successor support secondary upward endpoint
  dsimp
  omega

end SubQuorum.SecondaryTenTerminalRigidity
