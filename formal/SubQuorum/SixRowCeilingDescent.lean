import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SixRowCeilingDescent

structure NorthHorizontal where
  left : Int
  right : Int
  down : Bool
  width_min : left+5 ≤ right

def northEndpoint (source : NorthHorizontal) (row column : Int) : Prop :=
  (0 ≤ row ∧ row ≤ 4 ∧ (column = source.left ∨ column = source.right)) ∨
  (source.left ≤ column ∧ column ≤ source.right ∧
    ((source.down = true ∧ (row = 0 ∨ row = 1)) ∨
     (source.down = false ∧ (row = 3 ∨ row = 4))))

structure RightTransverse where
  bar : Int
  near : Int
  far : Int
  near_min : 4 ≤ near
  far_min : 4 ≤ far

def verticalEndpoint (source : RightTransverse) (row column : Int) : Prop :=
  (0 ≤ row ∧ row ≤ 5 ∧ (column = source.bar ∨ column = source.bar+1)) ∨
  (row = 0 ∧ source.bar+2 ≤ column ∧ column ≤ source.bar+source.far) ∨
  (row = 5 ∧ source.bar+2 ≤ column ∧ column ≤ source.bar+source.near)

def disjoint (vertical : RightTransverse) (horizontal : NorthHorizontal) : Prop :=
  ∀ row column, verticalEndpoint vertical row column → ¬ northEndpoint horizontal row column

theorem north_side_is_filled (source : NorthHorizontal) (row : Int)
    (hrow : 0 ≤ row ∧ row ≤ 4) : northEndpoint source row source.left := by
  exact Or.inl ⟨hrow.1,hrow.2,Or.inl rfl⟩

theorem top_stem_clearance (vertical : RightTransverse) (horizontal : NorthHorizontal)
    (hdisjoint : disjoint vertical horizontal) (hleft : vertical.bar+2 ≤ horizontal.left) :
    vertical.bar+vertical.far < horizontal.left := by
  by_cases hclear : vertical.bar+vertical.far < horizontal.left
  · exact hclear
  · have hpoint : verticalEndpoint vertical 0 horizontal.left := by
      exact Or.inr (Or.inl ⟨rfl,hleft,by omega⟩)
    exact False.elim (hdisjoint 0 horizontal.left hpoint
      (north_side_is_filled horizontal 0 (by omega)))

theorem renewed_support_has_bottom_neighbour
    (vertical : RightTransverse) (horizontal : NorthHorizontal)
    (hdisjoint : disjoint vertical horizontal) (hleft : vertical.bar+2 ≤ horizontal.left)
    (hreach : horizontal.left ≤ vertical.bar+vertical.near) :
    verticalEndpoint vertical 5 (horizontal.left-1) := by
  have hclear := top_stem_clearance vertical horizontal hdisjoint hleft
  have hfar := vertical.far_min
  exact Or.inr (Or.inr ⟨rfl,by omega,by omega⟩)

theorem renewed_support_has_right_neighbour (horizontal : NorthHorizontal) :
    northEndpoint horizontal 4 horizontal.left := by
  exact north_side_is_filled horizontal 4 (by omega)

theorem renewed_support_is_not_horizontal_endpoint (horizontal : NorthHorizontal) :
    ¬ northEndpoint horizontal 4 (horizontal.left-1) := by
  have hwidth := horizontal.width_min
  simp only [northEndpoint]
  omega

theorem renewed_support_is_not_vertical_endpoint
    (vertical : RightTransverse) (horizontal : NorthHorizontal)
    (hdisjoint : disjoint vertical horizontal) (hleft : vertical.bar+2 ≤ horizontal.left) :
    ¬ verticalEndpoint vertical 4 (horizontal.left-1) := by
  have hclear := top_stem_clearance vertical horizontal hdisjoint hleft
  have hfar := vertical.far_min
  simp only [verticalEndpoint]
  omega

theorem north_receiver_moves_left (current receiver : NorthHorizontal)
    (hcorner : receiver.right = current.left-1) : receiver.left+6 ≤ current.left := by
  have hwidth := receiver.width_min
  omega

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

theorem rotor_bottom_tip_has_upper_neighbour (reflected : Bool) (top left column : Int)
    (hpoint : rotorEndpoint reflected top left (top+3) column) :
    rotorEndpoint reflected top left (top+2) column := by
  cases reflected <;> simp [rotorEndpoint] at * <;> omega

theorem rotor_cannot_occupy_southeast_corner (reflected : Bool)
    (top left bottom right : Int)
    (hrows : ∀ row column, rotorEndpoint reflected top left row column → row ≤ bottom)
    (hcolumns : ∀ row column, rotorEndpoint reflected top left row column → column ≤ right)
    (hcorner : rotorEndpoint reflected top left bottom right) : False := by
  cases hshape : reflected with
  | false =>
    have hbottom := hrows (top+3) (left+2) (by simp [rotorEndpoint,hshape])
    have hright := hcolumns (top+1) (left+3) (by simp [rotorEndpoint,hshape])
    simp [rotorEndpoint,hshape] at hcorner
    omega
  | true =>
    have hbottom := hrows (top+3) (left+1) (by simp [rotorEndpoint,hshape])
    have hright := hcolumns (top+2) (left+3) (by simp [rotorEndpoint,hshape])
    simp [rotorEndpoint,hshape] at hcorner
    omega

theorem bounded_integer_descent_impossible (predicate : Int → Prop) (bound : Int)
    (hlower : ∀ position, predicate position → bound ≤ position)
    (hstep : ∀ position, predicate position →
      ∃ earlier, predicate earlier ∧ earlier < position) :
    ∀ position, ¬ predicate position := by
  have hgeneral : ∀ index : Nat, ∀ position : Int,
      (position-bound).toNat = index → ¬ predicate position := by
    intro index
    induction index using Nat.strongRecOn with
    | ind index inductionHypothesis =>
      intro position hindex hposition
      obtain ⟨earlier,hearlier,hstrict⟩ := hstep position hposition
      have hcurrentBound := hlower position hposition
      have hearlierBound := hlower earlier hearlier
      have hsmaller : (earlier-bound).toNat < index := by omega
      exact inductionHypothesis (earlier-bound).toNat hsmaller earlier rfl hearlier
  intro position
  exact hgeneral (position-bound).toNat position rfl

end SubQuorum.SixRowCeilingDescent

#print axioms SubQuorum.SixRowCeilingDescent.NorthHorizontal
#print axioms SubQuorum.SixRowCeilingDescent.northEndpoint
#print axioms SubQuorum.SixRowCeilingDescent.RightTransverse
#print axioms SubQuorum.SixRowCeilingDescent.verticalEndpoint
#print axioms SubQuorum.SixRowCeilingDescent.disjoint
#print axioms SubQuorum.SixRowCeilingDescent.north_side_is_filled
#print axioms SubQuorum.SixRowCeilingDescent.top_stem_clearance
#print axioms SubQuorum.SixRowCeilingDescent.renewed_support_has_bottom_neighbour
#print axioms SubQuorum.SixRowCeilingDescent.renewed_support_has_right_neighbour
#print axioms SubQuorum.SixRowCeilingDescent.renewed_support_is_not_horizontal_endpoint
#print axioms SubQuorum.SixRowCeilingDescent.renewed_support_is_not_vertical_endpoint
#print axioms SubQuorum.SixRowCeilingDescent.north_receiver_moves_left
#print axioms SubQuorum.SixRowCeilingDescent.rotorEndpoint
#print axioms SubQuorum.SixRowCeilingDescent.rotor_bottom_tip_has_upper_neighbour
#print axioms SubQuorum.SixRowCeilingDescent.rotor_cannot_occupy_southeast_corner
#print axioms SubQuorum.SixRowCeilingDescent.bounded_integer_descent_impossible
