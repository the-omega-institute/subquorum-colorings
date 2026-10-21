import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenDistinctConsumers

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def support (breadth near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = breadth+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = breadth+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = breadth-1)))

def residual (origin width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+6,width+12-point.2)

def cavity (origin width : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-width-7)

def northTip (handed : Bool) (row column : Int) (point : Point) : Prop :=
  (point.1-row,point.2-column) ∈
    if handed then
      [(-3,1),(-2,-1),(-2,0),(-2,1),(-1,0),(-1,1),(-1,2),(0,0)]
    else
      [(-3,-1),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(0,0)]

def southU (right : Bool) (origin width breadth depth far : Int) (point : Point) : Prop :=
  endpoint breadth depth far (origin+depth-point.1,
    if right then point.2-width-11 else width+13-point.2)

def southRotor (handed : Bool) (origin width : Int) (point : Point) : Prop :=
  northTip handed 0 0 (origin-point.1,point.2-width-12)

def westU (north : Bool) (origin width breadth depth far : Int) (point : Point) : Prop :=
  endpoint breadth depth far (point.2-width-13+depth,
    if north then origin-point.1 else point.1-origin+2)

def westRotor (handed : Bool) (origin width : Int) (point : Point) : Prop :=
  northTip handed 0 0 (point.2-width-13,point.1-origin+1)

def upperLeftRegion (width oldBreadth breadth depth far : Int) : Prop :=
  (breadth ≤ oldBreadth+2 ∧ 12 ≤ depth ∧ far ≤ depth-8) ∨
  (oldBreadth = width+8 ∧ breadth = width+12 ∧ 8 ≤ depth ∧ far ≤ depth+8) ∨
  (width+14 ≤ breadth ∧ 8 ≤ depth)

theorem lower_gap_original_support (breadth far : Int) :
    support breadth 8 far (6,0) := by
  unfold support
  omega

theorem lower_gap_foreign_neighbors (origin width breadth far : Int) :
    residual origin width breadth far (origin,width+11) ∧
      cavity origin width (origin,width+13) ∧
      northTip false origin (width+14) (origin-1,width+12) := by
  constructor
  · unfold residual endpoint
    dsimp
    omega
  constructor
  · unfold cavity endpoint
    dsimp
    omega
  · simp only [northTip, Bool.false_eq_true, ite_false, List.mem_cons, Prod.mk.injEq]
    omega

theorem lower_gap_absent (origin width breadth far : Int) (hbreadth : 6 ≤ breadth) :
    ¬(residual origin width breadth far (origin,width+12) ∨
      cavity origin width (origin,width+12) ∨
      northTip false origin (width+14) (origin,width+12)) := by
  simp [residual, cavity, endpoint, northTip] <;> omega

theorem south_U_hits_cavity (right : Bool) (origin width breadth depth far : Int)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) :
    southU right origin width breadth depth far (origin+3,width+12) ∧
      cavity origin width (origin+3,width+12) := by
  cases right <;> unfold southU cavity endpoint <;> dsimp <;> omega

theorem south_rotor_hits_cavity (handed : Bool) (origin width : Int) :
    ∃ point, southRotor handed origin width point ∧ cavity origin width point := by
  cases handed with
  | false =>
    refine ⟨(origin+2,width+13), ?_⟩
    simp only [southRotor, northTip, Bool.false_eq_true, ite_false,
      List.mem_cons, Prod.mk.injEq, cavity, endpoint]
    omega
  | true =>
    refine ⟨(origin+1,width+13), ?_⟩
    simp only [southRotor, northTip, ite_true, List.mem_cons,
      Prod.mk.injEq, cavity, endpoint]
    omega

theorem side_gap_original_support : support 6 4 4 (5,6) := by
  unfold support
  omega

theorem side_gap_foreign_neighbors (origin width : Int) :
    northTip true origin (width+14) (origin-2,width+13) ∧
      northTip true origin (width+14) (origin-1,width+14) ∧
      cavity origin width (origin,width+13) := by
  simp [northTip, cavity, endpoint] <;> omega

theorem side_gap_absent (origin width : Int) :
    ¬(cavity origin width (origin-1,width+13) ∨
      northTip true origin (width+14) (origin-1,width+13)) := by
  simp [northTip, cavity, endpoint] <;> omega

theorem west_U_hits_residual (north : Bool) (origin width breadth depth far oldBreadth oldFar : Int)
    (hdepth : 4 ≤ depth) :
    westU north origin width breadth depth far (origin-1,width+11) ∧
      residual origin width oldBreadth oldFar (origin-1,width+11) := by
  cases north <;> unfold westU residual endpoint <;> dsimp <;> omega

theorem west_rotor_hits_residual (handed : Bool) (origin width breadth far : Int) :
    westRotor handed origin width (origin-1,width+11) ∧
      residual origin width breadth far (origin-1,width+11) := by
  cases handed <;> simp only [westRotor, northTip, Bool.false_eq_true, ite_false,
    ite_true, List.mem_cons, Prod.mk.injEq, residual, endpoint] <;> omega

theorem depth_eight_escape_pays_contact (width oldBreadth breadth far : Int)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hregion : upperLeftRegion width oldBreadth breadth 8 far) :
    oldBreadth+4 ≤ breadth ∧ 3 ≤ breadth-1-oldBreadth := by
  unfold upperLeftRegion at hregion
  omega

theorem all_upper_consumer_gain (right : Bool) (width oldBreadth breadth depth far : Int)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hbreadth : 6 ≤ breadth)
    (hregion : right = true ∨ upperLeftRegion width oldBreadth breadth depth far) :
    3 ≤ breadth-1-(if right = false ∧ depth = 8 then oldBreadth else 0) := by
  by_cases hexception : right = false ∧ depth = 8
  · have hleft : upperLeftRegion width oldBreadth breadth 8 far := by
      rcases hregion with hright | hleft
      · simp [hexception.1] at hright
      · simpa [hexception.2] using hleft
    have hpay := depth_eight_escape_pays_contact width oldBreadth breadth far hold hleft
    simp only [if_pos hexception]
    omega
  · simp only [if_neg hexception]
    omega

theorem rotor_pair_repairs_deficit (rotorGain upperGain : Int)
    (hrotor : -1 ≤ rotorGain) (hupper : 3 ≤ upperGain) :
    1 ≤ -1+rotorGain+upperGain := by
  omega

theorem east_U_repairs_deficit (breadth : Int) (hbreadth : 6 ≤ breadth) :
    3 ≤ -1+(breadth-2) := by
  omega

end SubQuorum.SecondaryTenDistinctConsumers
