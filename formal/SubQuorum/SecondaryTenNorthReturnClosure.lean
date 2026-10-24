import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenNorthReturnClosure

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

def returning (origin width stage : Int) (point : Point) : Prop :=
  endpoint (width+6+2*stage) (6+2*stage) 4
    (point.1-origin+4+2*stage,width+11+stage-point.2)

def fixed (origin width : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,origin+11-point.1) ∨
  endpoint (width+4) 10 4 (point.1-origin+2,point.2-5) ∨
  endpoint width 4 6 (point.1-origin,point.2-6) ∨
  endpoint 8 6 4 (origin+6-point.1,point.2-width-6) ∨
  endpoint 6 4 4 (origin+4-point.1,point.2-width-7) ∨
  endpoint 6 4 4 (point.2-width-1,point.1-origin-1)

def cavity (origin width : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-width-7)

theorem nested_distinct (origin width first second : Int) (point : Point)
    (hwidth : 12 ≤ width) (hfirst : 0 ≤ first) (horder : first < second)
    (hsecond : second ≤ 2) :
    ¬(returning origin width first point ∧ returning origin width second point) := by
  unfold returning endpoint
  dsimp
  omega

theorem nested_avoids_fixed (origin width stage : Int) (point : Point)
    (hwidth : 12 ≤ width) (hstage : 0 ≤ stage) (hmax : stage ≤ 2) :
    ¬(returning origin width stage point ∧ fixed origin width point) := by
  unfold returning fixed endpoint
  dsimp
  omega

theorem next_terminal_consumed (origin width : Int) :
    returning origin width 2 (origin+2,width+12) ∧
      cavity origin width (origin+2,width+13) ∧
      support (width+10) 10 4 (10,0) := by
  unfold returning cavity endpoint support
  dsimp
  omega

theorem fourth_pattern_collides (origin width : Int) :
    returning origin width 3 (origin+2,width+13) ∧
      cavity origin width (origin+2,width+13) := by
  unfold returning cavity endpoint
  dsimp
  omega

theorem next_cavity_support_absent (origin width : Int) (hwidth : 12 ≤ width) :
    ¬fixed origin width (origin-1,width+13) ∧
      ∀ stage : Int, 0 ≤ stage → stage ≤ 2 →
        ¬returning origin width stage (origin-1,width+13) := by
  unfold fixed returning endpoint
  dsimp
  constructor
  · omega
  · intro stage hstage hmax
    omega

theorem next_cavity_support_anchors (origin width : Int) :
    support 6 4 4 (5,6) ∧
      returning origin width 2 (origin-1,width+12) ∧
      cavity origin width (origin,width+13) := by
  unfold support returning cavity endpoint
  dsimp
  omega

theorem far_supports_absent (origin width stage : Int) (hwidth : 12 ≤ width)
    (hstage : 0 ≤ stage) (hmax : stage ≤ 2) :
    ¬fixed origin width (origin+1-2*stage,5-stage) ∧
      ∀ other : Int, 0 ≤ other → other ≤ 2 →
        ¬returning origin width other (origin+1-2*stage,5-stage) := by
  unfold fixed returning endpoint
  dsimp
  constructor
  · omega
  · intro other hother hothermax
    omega

theorem far_support_and_anchor (origin width stage : Int) :
    support (width+6+2*stage) (6+2*stage) 4 (5,width+6+2*stage) ∧
      returning origin width stage (origin-2*stage,5-stage) := by
  unfold support returning endpoint
  dsimp
  omega

theorem preceding_far_anchor (origin width stage : Int) :
    returning origin width (stage-1) (origin+1-2*stage,6-stage) := by
  unfold returning endpoint
  dsimp
  omega

theorem first_far_east_anchor (width : Int) :
    endpoint (width+4) 10 4 (3,1) := by
  unfold endpoint
  dsimp
  omega

theorem branching_blockers (origin width : Int) (hwidth : 12 ≤ width) :
    returning origin width 0 (origin,width+10) ∧
      cavity origin width (origin+1,width+13) ∧
      endpoint 8 6 4 (4,8) := by
  unfold returning cavity endpoint
  dsimp
  omega

end SubQuorum.SecondaryTenNorthReturnClosure
