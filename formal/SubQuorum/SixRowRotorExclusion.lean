import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SixRowRotorExclusion

def rotorEndpoint (reflected : Bool) (top left row column : Int) : Prop :=
  (reflected = false ∧
    ((row = top ∧ column = left+1) ∨
     (row = top+1 ∧ left+1 ≤ column ∧ column ≤ left+3) ∨
     (row = top+2 ∧ left ≤ column ∧ column ≤ left+2) ∨
     (row = top+3 ∧ column = left+2))) ∨
  (reflected = true ∧
    ((row = top ∧ column = left+2) ∨
     (row = top+1 ∧ left ≤ column ∧ column ≤ left+2) ∨
     (row = top+2 ∧ left+1 ≤ column ∧ column ≤ left+3) ∨
     (row = top+3 ∧ column = left+1)))

def topColumn (reflected : Bool) (left : Int) : Int :=
  left + if reflected then 2 else 1

theorem top_endpoint_has_below (reflected : Bool) (top left column : Int)
    (hpoint : rotorEndpoint reflected top left top column) :
    rotorEndpoint reflected top left (top+1) column := by
  cases reflected <;> simp [rotorEndpoint] at * <;> omega

theorem boundary_anchor_blocked (reflected : Bool) (top left column : Int)
    (htop : 0 ≤ top) (_hbottom : top ≤ 2)
    (hcolumn : column = 0 ∨ column = 2 ∨ column = 3)
    (hpoint : rotorEndpoint reflected top left 0 column)
    (hdisjoint : ∀ row currentColumn, rotorEndpoint false 0 0 row currentColumn →
      ¬ rotorEndpoint reflected top left row currentColumn) : False := by
  have hzero : top = 0 := by
    cases reflected <;> simp [rotorEndpoint] at hpoint <;> omega
  subst top
  have hfirst := hdisjoint 1 1
  have hsecond := hdisjoint 1 2
  have hthird := hdisjoint 1 3
  have hfourth := hdisjoint 2 0
  rcases hcolumn with hcolumn | hcolumn | hcolumn <;> subst column <;> cases reflected <;>
    simp [rotorEndpoint] at hpoint hfirst hsecond hthird hfourth <;> omega

theorem bottom_rotor_classification (reflected : Bool) (left : Int)
    (hsupport : rotorEndpoint false 0 0 1 (topColumn reflected left))
    (hdisjoint : ∀ row column, rotorEndpoint false 0 0 row column →
      ¬ rotorEndpoint reflected 2 left row column) :
    reflected = false ∧ left = 2 := by
  have hfirst := hdisjoint 2 1
  have hsecond := hdisjoint 2 2
  have hthird := hdisjoint 3 2
  cases reflected <;>
    simp [rotorEndpoint,topColumn] at hsupport hfirst hsecond hthird ⊢ <;> omega

theorem unique_bottom_endpoint (rowColumn : Int)
    (hpoint : rotorEndpoint false 2 2 5 rowColumn) : rowColumn = 4 := by
  simp [rotorEndpoint] at hpoint
  omega

theorem middle_corner_blocked (firstReflection secondReflection : Bool)
    (left column : Int) (hcolumn : column = 0 ∨ column = 3)
    (hpoint : rotorEndpoint secondReflection 1 left 1 column)
    (hdisjoint : ∀ row currentColumn, rotorEndpoint firstReflection 1 0 row currentColumn →
      ¬ rotorEndpoint secondReflection 1 left row currentColumn) : False := by
  have hfirst := hdisjoint 2 0
  have hsecond := hdisjoint 2 1
  have hthird := hdisjoint 2 3
  have hfourth := hdisjoint 3 0
  have hfifth := hdisjoint 3 3
  cases firstReflection <;> cases secondReflection <;>
    simp [rotorEndpoint] at hpoint hfirst hsecond hthird hfourth hfifth <;> omega

theorem left_bottom_tip_even (bar topDepth bottomDepth : Int)
    (htop : bar+topDepth = 0) (htopEven : topDepth % 2 = 0)
    (hbottomEven : bottomDepth % 2 = 0) : (bar+bottomDepth) % 2 = 0 := by
  omega

theorem right_bottom_tip_even (bar topDepth bottomDepth : Int)
    (htop : bar+1-topDepth = 2) (htopEven : topDepth % 2 = 0)
    (hbottomEven : bottomDepth % 2 = 0) : (bar+1-bottomDepth) % 2 = 0 := by
  omega

theorem forced_bottom_gap (leftTip rightTip : Int)
    (hleft : leftTip % 2 = 0) (hright : rightTip % 2 = 0)
    (hdisjoint : leftTip < rightTip) : leftTip+1 < rightTip ∧ leftTip+1 ≠ 4 := by
  omega

theorem closed_top_row_forbids_new_top_rotor (reflected : Bool) (top left : Int)
    (htop : 0 ≤ top) (hbottom : top ≤ 2)
    (hpoint : rotorEndpoint reflected top left 0 (topColumn reflected left)) : top = 0 := by
  cases reflected <;> simp [rotorEndpoint,topColumn] at hpoint <;> omega

theorem with_horizontal_pocket_bound (aligned odd horizontalMass unused potential : Int)
    (haligned : 0 ≤ aligned) (hodd : 0 ≤ odd) (hunused : 0 ≤ unused)
    (hmass : 5 ≤ horizontalMass)
    (hbudget : aligned+2*odd+horizontalMass+unused ≤ potential) : 5 ≤ potential := by
  omega

theorem with_horizontal_chamber_bound (potential chamber : Int)
    (hpotential : 5 ≤ potential) (hchamber : chamber = 5+potential) : 10 ≤ chamber := by
  omega

end SubQuorum.SixRowRotorExclusion

#print axioms SubQuorum.SixRowRotorExclusion.rotorEndpoint
#print axioms SubQuorum.SixRowRotorExclusion.topColumn
#print axioms SubQuorum.SixRowRotorExclusion.top_endpoint_has_below
#print axioms SubQuorum.SixRowRotorExclusion.boundary_anchor_blocked
#print axioms SubQuorum.SixRowRotorExclusion.bottom_rotor_classification
#print axioms SubQuorum.SixRowRotorExclusion.unique_bottom_endpoint
#print axioms SubQuorum.SixRowRotorExclusion.middle_corner_blocked
#print axioms SubQuorum.SixRowRotorExclusion.left_bottom_tip_even
#print axioms SubQuorum.SixRowRotorExclusion.right_bottom_tip_even
#print axioms SubQuorum.SixRowRotorExclusion.forced_bottom_gap
#print axioms SubQuorum.SixRowRotorExclusion.closed_top_row_forbids_new_top_rotor
#print axioms SubQuorum.SixRowRotorExclusion.with_horizontal_pocket_bound
#print axioms SubQuorum.SixRowRotorExclusion.with_horizontal_chamber_bound
