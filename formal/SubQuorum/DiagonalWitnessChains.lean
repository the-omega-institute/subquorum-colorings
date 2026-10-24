import SubQuorum.BlankWitnessCompensation

set_option autoImplicit false

namespace SubQuorum.DiagonalWitnessChains

def Adjacent (firstRow firstColumn secondRow secondColumn : Int) : Prop :=
  (firstRow = secondRow+1 ∧ firstColumn = secondColumn) ∨
  (firstRow = secondRow-1 ∧ firstColumn = secondColumn) ∨
  (firstRow = secondRow ∧ firstColumn = secondColumn+1) ∨
  (firstRow = secondRow ∧ firstColumn = secondColumn-1)

theorem shared_corner_displacement
    (firstRow firstColumn secondRow secondColumn blankRow blankColumn : Int)
    (hfirst : Adjacent firstRow firstColumn blankRow blankColumn)
    (hsecond : Adjacent secondRow secondColumn blankRow blankColumn)
    (hfirstOutside : firstRow/2 ≠ blankRow/2 ∨ firstColumn/2 ≠ blankColumn/2)
    (hsecondOutside : secondRow/2 ≠ blankRow/2 ∨ secondColumn/2 ≠ blankColumn/2)
    (hdistinct : firstRow/2 ≠ secondRow/2 ∨ firstColumn/2 ≠ secondColumn/2) :
    secondRow/2 = firstRow/2+(if firstRow % 2 = 0 then -1 else 1) ∧
    secondColumn/2 = firstColumn/2+(if firstColumn % 2 = 0 then -1 else 1) ∧
    secondRow % 2 = 1-firstRow % 2 ∧
    secondColumn % 2 = 1-firstColumn % 2 := by
  unfold Adjacent at hfirst hsecond
  rcases hfirst with hfirst | hfirst | hfirst | hfirst <;>
    rcases hsecond with hsecond | hsecond | hsecond | hsecond <;> omega

theorem orientation_propagation
    (firstRow firstColumn secondRow secondColumn : Int)
    (hrow : secondRow % 2 = 1-firstRow % 2)
    (hcolumn : secondColumn % 2 = 1-firstColumn % 2) :
    (firstRow % 2 = firstColumn % 2 ↔ secondRow % 2 = secondColumn % 2) := by
  omega

theorem two_possible_shared_blanks
    (firstRow firstColumn secondRow secondColumn blankRow blankColumn : Int)
    (hfirst : Adjacent firstRow firstColumn blankRow blankColumn)
    (hsecond : Adjacent secondRow secondColumn blankRow blankColumn)
    (hrow : firstRow ≠ secondRow) (hcolumn : firstColumn ≠ secondColumn) :
    (blankRow = firstRow ∧ blankColumn = secondColumn) ∨
    (blankRow = secondRow ∧ blankColumn = firstColumn) := by
  unfold Adjacent at hfirst hsecond
  rcases hfirst with hfirst | hfirst | hfirst | hfirst <;>
    rcases hsecond with hsecond | hsecond | hsecond | hsecond <;> omega

theorem double_link_charge
    (owners links doubleLinks components free privateBlanks unused marked exports surplus : Nat)
    (chargeTwice : Int)
    (hpath : links+components = owners)
    (hfree : free = links+doubleLinks+privateBlanks+unused)
    (hsurplus : surplus = 2*marked+free)
    (hledger : chargeTwice = (owners : Int)+exports-surplus) :
    chargeTwice+2*marked = (exports : Int)+components-doubleLinks-privateBlanks-unused := by
  omega

end SubQuorum.DiagonalWitnessChains
