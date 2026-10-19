import Std

set_option autoImplicit false
set_option maxHeartbeats 0

namespace SubQuorum.LadderReduction

def interior (width row column : Int) : Prop :=
  (row = 0 ∨ row = 1) ∧ 1 ≤ column ∧ column ≤ width-2

def guard (width row column : Int) : Prop :=
  (row = -1 ∨ row = 2) ∧ (column = 1 ∨ column = width-2)

def retained (width color row column : Int) : Prop :=
  ¬(guard width row column ∧ (row+column)%2 ≠ color) ∧
    (¬interior width row column ∨ (row+column)%2 = color)

def adjacent (row column otherRow otherColumn : Int) : Prop :=
  (otherRow = row-1 ∧ otherColumn = column) ∨
  (otherRow = row+1 ∧ otherColumn = column) ∨
  (otherRow = row ∧ otherColumn = column-1) ∨
  (otherRow = row ∧ otherColumn = column+1)

theorem promoted_unique_neighbor (width color row column firstRow firstColumn
    secondRow secondColumn : Int)
    (hwidth : 4 ≤ width) (hinterior : interior width row column)
    (hcolor : (row+column)%2 = color)
    (hfirstAdjacent : adjacent row column firstRow firstColumn)
    (hsecondAdjacent : adjacent row column secondRow secondColumn)
    (hfirstRetained : retained width color firstRow firstColumn)
    (hsecondRetained : retained width color secondRow secondColumn) :
    firstRow = secondRow ∧ firstColumn = secondColumn := by
  simp only [interior] at hinterior
  rcases hinterior with ⟨hrow, hleft, hright⟩
  rcases hrow with hrow | hrow <;> subst row <;>
    rcases hfirstAdjacent with hfirst | hfirst | hfirst | hfirst <;>
    rcases hsecondAdjacent with hsecond | hsecond | hsecond | hsecond <;>
    simp only [retained, guard, interior] at hfirstRetained hsecondRetained <;>
    omega

theorem width_three_failure : retained 3 1 0 0 ∧ retained 3 1 0 2 ∧
    adjacent 0 1 0 0 ∧ adjacent 0 1 0 2 ∧ ¬((0 : Int) = 2) := by
  unfold retained guard interior adjacent
  decide

def mixedSelected (left right row column : Int) : Prop :=
  ((row = -1 ∨ row = 2) ∧ 0 ≤ column ∧ column ≤ 2*left+2*right ∧ column%2 = 0) ∨
    (row = 0 ∧ column = -1) ∨ (row = 1 ∧ column = 2*left+2*right+1)

def mixedPromoted (left right row column : Int) : Prop :=
  (row = 0 ∨ row = 1) ∧
    ((0 ≤ column ∧ column < 2*left ∧ (row+column)%2 = 1) ∨
     (2*left < column ∧ column ≤ 2*left+2*right ∧ (row+column)%2 = 0))

def mixedRetained (left right row column : Int) : Prop :=
  mixedSelected left right row column ∨ mixedPromoted left right row column ∨
    ((row = 0 ∨ row = 1) ∧ column = 2*left)

theorem mixed_promoted_unique_neighbor (left right row column firstRow firstColumn
    secondRow secondColumn : Int)
    (hleft : 1 ≤ left) (hright : 1 ≤ right)
    (hpromoted : mixedPromoted left right row column)
    (hfirstAdjacent : adjacent row column firstRow firstColumn)
    (hsecondAdjacent : adjacent row column secondRow secondColumn)
    (hfirstRetained : mixedRetained left right firstRow firstColumn)
    (hsecondRetained : mixedRetained left right secondRow secondColumn) :
    firstRow = secondRow ∧ firstColumn = secondColumn := by
  simp only [mixedPromoted] at hpromoted
  rcases hpromoted with ⟨hrow, hposition⟩
  rcases hrow with hrow | hrow <;> subst row <;>
    rcases hfirstAdjacent with hfirst | hfirst | hfirst | hfirst <;>
    rcases hsecondAdjacent with hsecond | hsecond | hsecond | hsecond <;>
    simp only [mixedRetained, mixedSelected, mixedPromoted] at hfirstRetained hsecondRetained <;>
    omega

end SubQuorum.LadderReduction
