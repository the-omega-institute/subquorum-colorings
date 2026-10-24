import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WideGateRotorCompensation

abbrev Point := Int × Int

def blocked (width : Int) (point : Point) : Prop :=
  ((point.2 = 0 ∨ point.2 = width+1) ∧ 0 ≤ point.1 ∧ point.1 ≤ 6) ∨
  ((point.1 = 0 ∨ point.1 = 1 ∨ point.1 = 8 ∨ point.1 = 9) ∧
    1 ≤ point.2 ∧ point.2 ≤ width) ∨
  ((point.2 = 1 ∨ point.2 = width) ∧ 0 ≤ point.1 ∧ point.1 ≤ 4)

def leftRotor (upper : Bool) (point : Point) : Prop :=
  point ∈ if upper then
    [(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)]
  else [(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)]

def leftSupport (upper : Bool) (point : Point) : Prop :=
  point ∈ if upper then
    [(2,2),(3,1),(3,4),(4,5),(5,0),(6,1),(6,4),(7,3)]
  else [(3,3),(4,1),(4,4),(5,0),(6,5),(7,1),(7,4),(8,2)]

def rightRotor (width : Int) (upper : Bool) (point : Point) : Prop :=
  leftRotor upper (point.1,width+1-point.2)

def rightSupport (width : Int) (upper : Bool) (point : Point) : Prop :=
  leftSupport upper (point.1,width+1-point.2)

theorem east_terminal_collision (occupied : Point → Prop) (width depth breadth : Int)
    (hwidth : 6 ≤ width) (hdepth : 4 ≤ depth) (hbreadth : 6 ≤ breadth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ depth → occupied (5,1+step))
    (hbar : (∀ row : Int, 6-breadth ≤ row → row ≤ 5 → occupied (row,1+depth)) ∨
      (∀ row : Int, 5 ≤ row → row ≤ 4+breadth → occupied (row,1+depth))) :
    ∃ point, occupied point ∧ blocked width point := by
  by_cases hlong : width ≤ depth
  · refine ⟨(5,width+1),?_,?_⟩
    · simpa [Int.add_comm] using hstem width (by omega) hlong
    · simp [blocked]
  · rcases hbar with hup | hdown
    · refine ⟨(0,1+depth),hup 0 (by omega) (by omega),?_⟩
      dsimp [blocked]
      omega
    · refine ⟨(8,1+depth),hdown 8 (by omega) (by omega),?_⟩
      dsimp [blocked]
      omega

theorem left_endpoint_bounds (upper : Bool) (point : Point)
    (hpoint : leftRotor upper point) :
    3 ≤ point.1 ∧ point.1 ≤ 7 ∧ 1 ≤ point.2 ∧ point.2 ≤ 4 := by
  rcases point with ⟨row,column⟩
  cases upper <;> simp [leftRotor] at hpoint <;> dsimp <;> omega

theorem opposite_rotors_disjoint (width : Int) (leftUpper rightUpper : Bool)
    (hwidth : 8 ≤ width) (point : Point)
    (hleft : leftRotor leftUpper point) : ¬rightRotor width rightUpper point := by
  intro hright
  have hfirst := left_endpoint_bounds leftUpper point hleft
  have hsecond := left_endpoint_bounds rightUpper (point.1,width+1-point.2) hright
  dsimp at hsecond
  omega

theorem middle_directions_excluded (width row column : Int) (leftUpper rightUpper : Bool)
    (hwidth : 8 ≤ width)
    (hleft : leftRotor leftUpper (row,column))
    (hright : rightRotor width rightUpper (row,column+1)) :
    leftSupport leftUpper (row,column+1) ∧
      rightSupport width rightUpper (row,column) := by
  have hfirst := left_endpoint_bounds leftUpper (row,column) hleft
  have hsecond := left_endpoint_bounds rightUpper (row,width+1-(column+1)) hright
  dsimp at hfirst hsecond
  have hcolumn : column = 4 := by omega
  have hwidthExact : width = 8 := by omega
  subst column
  subst width
  cases leftUpper <;> cases rightUpper <;>
    simp [leftRotor,rightRotor] at hleft hright <;>
    simp_all [leftSupport,rightSupport]

theorem different_gaps_have_disjoint_tile_rows (top first second rowFirst rowSecond : Int)
    (horder : first < second)
    (hfirst : top+8*first+3 ≤ rowFirst ∧ rowFirst ≤ top+8*first+7)
    (hsecond : top+8*second+3 ≤ rowSecond ∧ rowSecond ≤ top+8*second+7) :
    rowFirst/2 < rowSecond/2 := by omega

theorem gate_tile_injection (top first second : Int)
    (htile : (top+8*first+4)/2 = (top+8*second+4)/2) : first = second := by omega

theorem one_rotor_gain (upper : Bool) :
    (if upper then (2 : Int) else 0)+2-(if upper then 1 else 0) =
      2+(if upper then 1 else 0) := by cases upper <;> decide

theorem simultaneous_budget (gaps upperCount total : Int)
    (hledger : total = -gaps+4*gaps+upperCount) (hupper : 0 ≤ upperCount) :
    3*gaps ≤ total := by omega

theorem sharp_budget (gaps total : Int) (hledger : total = -gaps+4*gaps) :
    total = 3*gaps := by omega

end SubQuorum.WideGateRotorCompensation
