import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.WideGateSealedReturnObstruction

abbrev Point := Int × Int

def stripBlocked (depth : Int) (point : Point) : Prop :=
  (point.1 = 2 ∧ 2 ≤ point.2 ∧ point.2 ≤ depth+2) ∨
  (point.1 = 8 ∧ 1 ≤ point.2 ∧ point.2 ≤ depth+2) ∨
  (point.1 = 3 ∧ (point.2 = 1 ∨ point.2 = depth+1))

def cornerBlocked (depth side : Int) (point : Point) : Prop :=
  stripBlocked depth point ∨
  (point.1 = 7 ∧ side+1 ≤ point.2 ∧ point.2 ≤ depth+2) ∨
  (point.2 = side ∧ 3 ≤ point.1 ∧ point.1 ≤ 7)

def horizontalRotor (east upper : Bool) (column : Int) (point : Point) : Prop :=
  (point.1-3, if east then point.2-column else column-point.2) ∈
    if upper then [(-2,1),(-1,1),(-1,2),(-1,3),(0,0),(0,1),(0,2),(1,2)]
    else [(-1,2),(0,0),(0,1),(0,2),(1,1),(1,2),(1,3),(2,1)]

def southRotor (first : Bool) (column : Int) (point : Point) : Prop :=
  point ∈ if first then
    [(6,column-1),(5,column-1),(5,column),(5,column+1),
     (4,column-2),(4,column-1),(4,column),(3,column)]
  else [(6,column+1),(5,column-1),(5,column),(5,column+1),
        (4,column),(4,column+1),(4,column+2),(3,column)]

theorem horizontal_U_collision (occupied : Point → Prop) (depth column bar breadth : Int)
    (hcolumn : 2 ≤ column ∧ column ≤ depth)
    (hbreadth : 6 ≤ breadth)
    (hstem : ∀ target : Int,
      ((bar ≤ target ∧ target ≤ column) ∨ (column ≤ target ∧ target ≤ bar)) →
        occupied (3,target))
    (hbar : (∀ row : Int, 4-breadth ≤ row → row ≤ 3 → occupied (row,bar)) ∨
      (∀ row : Int, 3 ≤ row → row ≤ 2+breadth → occupied (row,bar))) :
    ∃ point, occupied point ∧ stripBlocked depth point := by
  by_cases hleft : bar ≤ 1
  · refine ⟨(3,1),hstem 1 (by omega),?_⟩
    simp [stripBlocked]
  · by_cases hright : depth+1 ≤ bar
    · refine ⟨(3,depth+1),hstem (depth+1) (by omega),?_⟩
      simp [stripBlocked]
    · rcases hbar with hup | hdown
      · refine ⟨(2,bar),hup 2 (by omega) (by omega),?_⟩
        dsimp [stripBlocked]
        omega
      · refine ⟨(8,bar),hdown 8 (by omega) (by omega),?_⟩
        dsimp [stripBlocked]
        omega

theorem horizontal_rotor_collision (depth column : Int) (east upper : Bool)
    (hcolumn : 4 ≤ column ∧ column ≤ depth-2) :
    ∃ point, horizontalRotor east upper column point ∧ stripBlocked depth point := by
  cases east <;> cases upper
  · refine ⟨(2,column-2),?_,?_⟩
    · simp [horizontalRotor]
      omega
    · dsimp [stripBlocked]
      omega
  · refine ⟨(2,column-1),?_,?_⟩
    · simp [horizontalRotor]
      omega
    · dsimp [stripBlocked]
      omega
  · refine ⟨(2,column+2),?_,?_⟩
    · simp [horizontalRotor]
      omega
    · dsimp [stripBlocked]
      omega
  · refine ⟨(2,column+1),?_,?_⟩
    · simp [horizontalRotor]
      omega
    · dsimp [stripBlocked]
      omega

theorem far_rotor_gate_bounds (depth side : Int) (first : Bool)
    (hside : 5 ≤ side ∧ side ≤ depth-3) :
    4 ≤ (if first then side-1 else side+1) ∧
      (if first then side-1 else side+1) ≤ depth-2 := by
  cases first <;> omega

theorem east_terminal_collision (occupied : Point → Prop) (depth side near breadth : Int)
    (hside : 5 ≤ side ∧ side ≤ depth-3)
    (hnear : 4 ≤ near) (hbreadth : 6 ≤ breadth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ near → occupied (3,side+1+step))
    (hbar : (∀ row : Int, 4-breadth ≤ row → row ≤ 3 → occupied (row,side+1+near)) ∨
      (∀ row : Int, 3 ≤ row → row ≤ 2+breadth → occupied (row,side+1+near))) :
    ∃ point, occupied point ∧ stripBlocked depth point := by
  by_cases hlong : depth-side ≤ near
  · refine ⟨(3,depth+1),?_,?_⟩
    · have hequal : side+1+(depth-side) = depth+1 := by omega
      simpa only [hequal] using hstem (depth-side) (by omega) hlong
    · simp [stripBlocked]
  · rcases hbar with hup | hdown
    · refine ⟨(2,side+1+near),hup 2 (by omega) (by omega),?_⟩
      dsimp [stripBlocked]
      omega
    · refine ⟨(8,side+1+near),hdown 8 (by omega) (by omega),?_⟩
      dsimp [stripBlocked]
      omega

theorem south_stem_collision (occupied : Point → Prop) (depth side near : Int)
    (hside : 5 ≤ side ∧ side ≤ depth-3) (hnear : 4 ≤ near)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ near → occupied (3+step,side+1)) :
    ∃ point, occupied point ∧ cornerBlocked depth side point := by
  refine ⟨(7,side+1),hstem 4 (by omega) hnear,?_⟩
  dsimp [cornerBlocked]
  omega

theorem south_bar_collision (occupied : Point → Prop) (depth side breadth : Int)
    (hside : 5 ≤ side ∧ side ≤ depth-3) (hbreadth : 6 ≤ breadth)
    (hbar : ∀ step : Int, 0 ≤ step → step < breadth → occupied (3+step,side+1)) :
    ∃ point, occupied point ∧ stripBlocked depth point := by
  refine ⟨(8,side+1),hbar 5 (by omega) (by omega),?_⟩
  dsimp [stripBlocked]
  omega

theorem south_rotor_collision (depth side : Int) (first : Bool) :
    southRotor first (side+1) (5,side) ∧ cornerBlocked depth side (5,side) := by
  constructor
  · cases first <;> simp [southRotor]
  · simp [cornerBlocked]

theorem short_U_frontier (side breadth : Int) (hbreadth : 6 ≤ breadth)
    (hleft : 6 ≤ side+1-breadth) : breadth ≤ side-5 ∧ 11 ≤ side := by omega

theorem north_stem_depth_four (depth : Int) (hmin : 4 ≤ depth)
    (hmax : depth < 6) (heven : depth % 2 = 0) : depth = 4 := by omega

theorem all_width_nested_seed_has_three_sources (amount : Nat) (hamount : 2 ≤ amount) :
    1 < amount ∧ 3 ≤ amount+1 := by omega

def sixRowBlocked (width : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 6) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  ((point.2 = 0 ∨ point.2 = width+1) ∧ 0 ≤ point.1 ∧ point.1 ≤ 10)

theorem six_row_east_terminal_collision
    (occupied : Point → Prop) (width depth breadth : Int)
    (hwidth : 6 ≤ width) (hdepth : 4 ≤ depth) (hbreadth : 6 ≤ breadth)
    (hstem : ∀ step : Int, 0 ≤ step → step ≤ depth → occupied (5,1+step))
    (hbar : (∀ row : Int, 6-breadth ≤ row → row ≤ 5 → occupied (row,1+depth)) ∨
      (∀ row : Int, 5 ≤ row → row ≤ 4+breadth → occupied (row,1+depth))) :
    ∃ point, occupied point ∧ sixRowBlocked width point := by
  by_cases hlong : width ≤ depth
  · refine ⟨(5,width+1),?_,?_⟩
    · simpa [Int.add_comm] using hstem width (by omega) hlong
    · simp [sixRowBlocked]
  · rcases hbar with hup | hdown
    · refine ⟨(0,1+depth),hup 0 (by omega) (by omega),?_⟩
      dsimp [sixRowBlocked]
      omega
    · refine ⟨(6,1+depth),hdown 6 (by omega) (by omega),?_⟩
      dsimp [sixRowBlocked]
      omega

def sixRowRotor (upper : Bool) (point : Point) : Prop :=
  horizontalRotor true upper 1 (point.1-2,point.2)

theorem six_row_rotor_collision (width : Int) (upper : Bool) (hwidth : 6 ≤ width) :
    sixRowRotor upper (6,3) ∧ sixRowBlocked width (6,3) := by
  constructor
  · cases upper <;> simp [sixRowRotor,horizontalRotor] <;> omega
  · dsimp [sixRowBlocked]
    omega

theorem minimum_even_bar_spacing (spacing : Int)
    (hdisjoint : 6 ≤ spacing) (heven : spacing % 2 = 0)
    (hsix : spacing ≠ 6) (height : spacing ≠ 8) : 10 ≤ spacing := by omega

end SubQuorum.WideGateSealedReturnObstruction
