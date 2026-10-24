import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ElbowSourceExclusion

def endpoint (width height row column : Int) : Prop :=
  ((row = 0 ∨ row = 1) ∧ 0 ≤ column ∧ column < width) ∨
  (2 ≤ row ∧ row < height ∧ (column = width-2 ∨ column = width-1)) ∨
  (row = 2 ∧ column = 0) ∨ (row = height ∧ column = width-1)

def square (width height row column : Int) : Prop :=
  endpoint width height row column ∧
  endpoint width height row (column+1) ∧
  endpoint width height (row+1) column ∧
  endpoint width height (row+1) (column+1)

def horizontalBar (width height row column span : Int) : Prop :=
  ∀ rowOffset columnOffset : Int,
    0 ≤ rowOffset → rowOffset ≤ 1 →
    0 ≤ columnOffset → columnOffset < span →
    endpoint width height (row+rowOffset) (column+columnOffset)

def verticalBar (width height row column span : Int) : Prop :=
  ∀ rowOffset columnOffset : Int,
    0 ≤ rowOffset → rowOffset < span →
    0 ≤ columnOffset → columnOffset ≤ 1 →
    endpoint width height (row+rowOffset) (column+columnOffset)

theorem square_location (width height row column : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hsquare : square width height row column) :
    row = 0 ∨ column = width-2 := by
  rcases hsquare with ⟨hfirst, hsecond, hthird, hfourth⟩
  simp only [endpoint] at hfirst hsecond hthird hfourth
  omega

theorem horizontal_bar_location (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 3 ≤ span)
    (hbar : horizontalBar width height row column span) : row = 0 := by
  have hfirst : square width height row column := by
    exact ⟨by simpa using hbar 0 0 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 0 1 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 1 0 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 1 1 (by omega) (by omega) (by omega) (by omega)⟩
  have hlast : square width height row (column+(span-2)) := by
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa using hbar 0 (span-2) (by omega) (by omega) (by omega) (by omega)
    · rw [show column+(span-2)+1 = column+(span-1) by omega]
      simpa using hbar 0 (span-1) (by omega) (by omega) (by omega) (by omega)
    · simpa using hbar 1 (span-2) (by omega) (by omega) (by omega) (by omega)
    · rw [show column+(span-2)+1 = column+(span-1) by omega]
      exact hbar 1 (span-1) (by omega) (by omega) (by omega) (by omega)
  have hleft := square_location width height row column hwidth hheight hfirst
  have hright := square_location width height row (column+(span-2)) hwidth hheight hlast
  omega

theorem vertical_bar_location (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 3 ≤ span)
    (hbar : verticalBar width height row column span) : column = width-2 := by
  have hfirst : square width height row column := by
    exact ⟨by simpa using hbar 0 0 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 0 1 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 1 0 (by omega) (by omega) (by omega) (by omega),
      by simpa using hbar 1 1 (by omega) (by omega) (by omega) (by omega)⟩
  have hlast : square width height (row+(span-2)) column := by
    refine ⟨?_, ?_, ?_, ?_⟩
    · simpa using hbar (span-2) 0 (by omega) (by omega) (by omega) (by omega)
    · simpa using hbar (span-2) 1 (by omega) (by omega) (by omega) (by omega)
    · rw [show row+(span-2)+1 = row+(span-1) by omega]
      simpa using hbar (span-1) 0 (by omega) (by omega) (by omega) (by omega)
    · rw [show row+(span-2)+1 = row+(span-1) by omega]
      exact hbar (span-1) 1 (by omega) (by omega) (by omega) (by omega)
  have htop := square_location width height row column hwidth hheight hfirst
  have hbottom := square_location width height (row+(span-2)) column hwidth hheight hlast
  omega

theorem no_horizontal_down_u (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 6 ≤ span)
    (hbar : horizontalBar width height row column span)
    (hleft : endpoint width height (row+3) column)
    (hright : endpoint width height (row+3) (column+span-1)) : False := by
  have hrow := horizontal_bar_location width height row column span hwidth hheight (by omega) hbar
  simp only [endpoint] at hleft hright
  omega

theorem no_horizontal_up_u (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 6 ≤ span)
    (hbar : horizontalBar width height row column span)
    (hleft : endpoint width height (row-1) column) : False := by
  have hrow := horizontal_bar_location width height row column span hwidth hheight (by omega) hbar
  simp only [endpoint] at hleft
  omega

theorem no_vertical_right_u (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 6 ≤ span)
    (hbar : verticalBar width height row column span)
    (htop : endpoint width height row (column+2)) : False := by
  have hcolumn := vertical_bar_location width height row column span hwidth hheight (by omega) hbar
  simp only [endpoint] at htop
  omega

theorem no_vertical_left_u (width height row column span : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hspan : 6 ≤ span)
    (hbar : verticalBar width height row column span)
    (htop : endpoint width height row (column-2))
    (hbottom : endpoint width height (row+span-1) (column-2)) : False := by
  have hcolumn := vertical_bar_location width height row column span hwidth hheight (by omega) hbar
  simp only [endpoint] at htop hbottom
  omega

theorem no_rotor (width height row column northOffset eastOffset : Int)
    (hwidth : 6 ≤ width) (hheight : 4 ≤ height)
    (hsquare : square width height row column)
    (hnorth : endpoint width height (row-1) (column+northOffset))
    (heast : endpoint width height (row+eastOffset) (column+2)) : False := by
  have hlocation := square_location width height row column hwidth hheight hsquare
  simp only [endpoint] at hnorth heast
  omega

#print axioms endpoint
#print axioms square
#print axioms horizontalBar
#print axioms verticalBar
#print axioms square_location
#print axioms horizontal_bar_location
#print axioms vertical_bar_location
#print axioms no_horizontal_down_u
#print axioms no_horizontal_up_u
#print axioms no_vertical_right_u
#print axioms no_vertical_left_u
#print axioms no_rotor

end SubQuorum.ElbowSourceExclusion
