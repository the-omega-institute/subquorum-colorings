import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.EvenBarContactObstruction

abbrev Point := Int × Int

def blocked (point : Point) : Prop :=
  ((point.2 = 0 ∨ point.2 = 7) ∧ 0 ≤ point.1 ∧ point.1 ≤ 6) ∨
  ((point.1 = 0 ∨ point.1 = 1 ∨ point.1 = 8 ∨ point.1 = 9) ∧
    1 ≤ point.2 ∧ point.2 ≤ 6) ∨
  ((point.2 = 1 ∨ point.2 = 6) ∧ 0 ≤ point.1 ∧ point.1 ≤ 4)

def leftRotor (upper : Bool) (point : Point) : Prop :=
  point ∈ if upper then
    [(3,2),(4,2),(4,3),(4,4),(5,1),(5,2),(5,3),(6,3)]
  else [(4,3),(5,1),(5,2),(5,3),(6,2),(6,3),(6,4),(7,2)]

def rightRotor (upper : Bool) (point : Point) : Prop :=
  leftRotor upper (point.1,7-point.2)

def southRotor (first : Bool) (point : Point) : Prop :=
  point ∈ if first then
    [(5,1),(6,-1),(6,0),(6,1),(7,0),(7,1),(7,2),(8,0)]
  else [(5,1),(6,1),(6,2),(6,3),(7,0),(7,1),(7,2),(8,2)]

theorem mirror_blocked (point : Point) :
    blocked point ↔ blocked (point.1,7-point.2) := by
  simp only [blocked]
  omega

theorem gates_absent : ¬blocked (5,1) ∧ ¬blocked (5,6) := by simp [blocked]

theorem gates_have_two_blocked_neighbors :
    blocked (4,1) ∧ blocked (5,0) ∧ blocked (4,6) ∧ blocked (5,7) := by simp [blocked]

theorem south_chain_collision (occupied : Point → Prop)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ 3 → occupied (5+step,1)) :
    ∃ point, occupied point ∧ blocked point := by
  exact ⟨(8,1),by simpa using hstem 3 (by omega) (by omega),by simp [blocked]⟩

theorem vertical_bar_collision (occupied : Point → Prop) (breadth : Int)
    (hbreadth : 6 ≤ breadth)
    (hbar : ∀ step : Int, 0 ≤ step → step ≤ breadth-1 → occupied (5+step,1)) :
    ∃ point, occupied point ∧ blocked point := by
  exact ⟨(8,1),by simpa using hbar 3 (by omega) (by omega),by simp [blocked]⟩

theorem east_terminal_collision (occupied : Point → Prop) (depth breadth : Int)
    (hdepth : 4 ≤ depth) (heven : depth % 2 = 0) (hbreadth : 6 ≤ breadth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ depth → occupied (5,1+step))
    (hbar : (∀ row : Int, 6-breadth ≤ row → row ≤ 5 → occupied (row,1+depth)) ∨
      (∀ row : Int, 5 ≤ row → row ≤ 4+breadth → occupied (row,1+depth))) :
    ∃ point, occupied point ∧ blocked point := by
  by_cases hlong : 6 ≤ depth
  · exact ⟨(5,7),by simpa using hstem 6 (by omega) hlong,by simp [blocked]⟩
  · have hfour : depth = 4 := by omega
    rcases hbar with hup | hdown
    · exact ⟨(0,5),by simpa [hfour] using hup 0 (by omega) (by omega),by simp [blocked]⟩
    · exact ⟨(8,5),by simpa [hfour] using hdown 8 (by omega) (by omega),by simp [blocked]⟩

theorem south_rotor_collision (first : Bool) :
    ∃ point, southRotor first point ∧ blocked point := by
  cases first
  · exact ⟨(8,2),by simp [southRotor],by simp [blocked]⟩
  · exact ⟨(6,0),by simp [southRotor],by simp [blocked]⟩

theorem rotor_pair_collision (leftUpper rightUpper : Bool) :
    ∃ point, leftRotor leftUpper point ∧ rightRotor rightUpper point := by
  cases leftUpper <;> cases rightUpper
  · exact ⟨(6,3),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(6,4),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(4,4),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩
  · exact ⟨(4,3),by simp [leftRotor],by simp [rightRotor,leftRotor]⟩

theorem left_rotor_cannot_own_right_gate (upper : Bool) : ¬leftRotor upper (5,6) := by
  cases upper <;> simp [leftRotor]

theorem contact_cycle_identity (vertices edges components cycles : Int)
    (hcycles : cycles = edges-vertices+components) :
    vertices-edges = components-cycles := by omega

theorem nested_budget (amount : Int) : (amount+1)-2*amount = 1-amount := by omega

end SubQuorum.EvenBarContactObstruction
