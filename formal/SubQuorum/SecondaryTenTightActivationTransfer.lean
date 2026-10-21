import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenTightActivationTransfer

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def squareAt (width near far : Int) (corner : Point) : Prop :=
  endpoint width near far corner ∧
  endpoint width near far (corner.1+1,corner.2) ∧
  endpoint width near far (corner.1,corner.2+1) ∧
  endpoint width near far (corner.1+1,corner.2+1)

def bar (width : Int) (point : Point) : Prop :=
  (point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width

def withinThree (point candidate : Point) : Prop :=
  -3 ≤ point.1-candidate.1 ∧ point.1-candidate.1 ≤ 3 ∧
  -3 ≤ point.2-candidate.2 ∧ point.2-candidate.2 ≤ 3

def withinRadius (radius : Int) (point candidate : Point) : Prop :=
  -radius ≤ point.1-candidate.1 ∧ point.1-candidate.1 ≤ radius ∧
  -radius ≤ point.2-candidate.2 ∧ point.2-candidate.2 ≤ radius

theorem all_original_endpoint_squares_are_in_the_bar
    (width near far : Int) (corner : Point) (hwidth : 6 ≤ width) :
    squareAt width near far corner ↔
      corner.1 = 0 ∧ 1 ≤ corner.2 ∧ corner.2 < width := by
  unfold squareAt endpoint
  dsimp
  omega

theorem square_vertices_recover_the_whole_original_bar
    (width near far : Int) (point : Point) (hwidth : 6 ≤ width) :
    (∃ corner, squareAt width near far corner ∧
      (point = corner ∨ point = (corner.1+1,corner.2) ∨
        point = (corner.1,corner.2+1) ∨ point = (corner.1+1,corner.2+1))) ↔
      bar width point := by
  constructor
  · rintro ⟨corner, hsquare, hpoint⟩
    have hcorner := (all_original_endpoint_squares_are_in_the_bar width near far corner hwidth).mp hsquare
    unfold bar
    rcases hpoint with hpoint | hpoint | hpoint | hpoint
    all_goals subst point; try dsimp at *
    all_goals omega
  · intro hbar
    unfold bar at hbar
    by_cases hcolumn : point.2 < width
    · refine ⟨(0,point.2), ?_, ?_⟩
      · apply (all_original_endpoint_squares_are_in_the_bar width near far _ hwidth).mpr
        dsimp
        omega
      · rcases hbar.1 with hrow | hrow
        · exact Or.inl (Prod.ext hrow rfl)
        · right
          left
          apply Prod.ext <;> dsimp <;> omega
    · refine ⟨(0,width-1), ?_, ?_⟩
      · apply (all_original_endpoint_squares_are_in_the_bar width near far _ hwidth).mpr
        dsimp
        omega
      · rcases hbar.1 with hrow | hrow
        · right
          right
          left
          apply Prod.ext <;> dsimp <;> omega
        · right
          right
          right
          apply Prod.ext <;> dsimp <;> omega

theorem depth_four_is_close_to_the_intrinsic_bar (width : Int) (hwidth : 6 ≤ width) :
    ∃ candidate, bar width candidate ∧ withinThree (4,1) candidate := by
  refine ⟨(1,1), ?_⟩
  unfold bar withinThree
  dsimp
  omega

theorem depth_five_is_not_close_to_the_intrinsic_bar (width : Int) :
    ¬∃ candidate, bar width candidate ∧ withinThree (5,1) candidate := by
  rintro ⟨candidate, hbar, hclose⟩
  unfold bar at hbar
  unfold withinThree at hclose
  dsimp at hclose
  omega

theorem arbitrary_depth_has_the_exact_intrinsic_bar_distance
    (width depth column radius : Int) (hdepth : 2 ≤ depth)
    (hcolumn : 1 ≤ column) (hupper : column ≤ width) :
    (∃ candidate, bar width candidate ∧ withinRadius radius (depth,column) candidate) ↔
      depth-1 ≤ radius := by
  constructor
  · rintro ⟨candidate, hbar, hclose⟩
    unfold bar at hbar
    unfold withinRadius at hclose
    dsimp at hclose
    omega
  · intro hbound
    refine ⟨(1,column), ?_⟩
    unfold bar withinRadius
    dsimp
    omega

theorem within_three_preserved_by_translation (point candidate offset : Point) :
    withinThree (point.1+offset.1,point.2+offset.2)
      (candidate.1+offset.1,candidate.2+offset.2) ↔ withinThree point candidate := by
  unfold withinThree
  dsimp
  omega

theorem within_three_preserved_by_row_reflection (point candidate : Point) :
    withinThree (-point.1,point.2) (-candidate.1,candidate.2) ↔ withinThree point candidate := by
  unfold withinThree
  dsimp
  omega

theorem within_three_preserved_by_column_reflection (point candidate : Point) :
    withinThree (point.1,-point.2) (candidate.1,-candidate.2) ↔ withinThree point candidate := by
  unfold withinThree
  dsimp
  omega

theorem within_three_preserved_by_transposition (point candidate : Point) :
    withinThree (point.2,point.1) (candidate.2,candidate.1) ↔ withinThree point candidate := by
  unfold withinThree
  dsimp
  omega

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem the_depth_five_axial_point_has_opposite_original_neighbors
    (width : Int) (point : Point) (hwidth : 6 ≤ width) :
    (endpoint width 10 4 point ∧ adjacent (5,1) point) ↔
      point = (4,1) ∨ point = (6,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_short_other_leg_cannot_supply_depth_five (width : Int) (hwidth : 6 ≤ width) :
    ¬endpoint width 10 4 (5,width) := by
  unfold endpoint
  dsimp
  omega

def target (bottom incident : Int) (point : Point) : Point :=
  (bottom-5-point.2,incident+7-point.1)

def oldS (incident : Int) (point : Point) : Point := (incident+3-point.1,3-point.2)
def oldP (point : Point) : Point := (point.2+2,point.1+2)
def companionE (incident : Int) (point : Point) : Point := (point.2+2,incident+3-point.1)
def companionS (incident : Int) (point : Point) : Point := (incident+3-point.1,point.2+2)

theorem all_four_old_frame_compositions (bottom incident : Int) (point : Point) :
    (bottom-8+(oldS incident point).2,(oldS incident point).1+4) = target bottom incident point ∧
    (bottom-3-(oldP point).1,incident+9-(oldP point).2) = target bottom incident point ∧
    (bottom-3-(companionE incident point).1,(companionE incident point).2+4) = target bottom incident point ∧
    (bottom-3-(companionS incident point).2,(companionS incident point).1+4) = target bottom incident point := by
  simp only [Prod.ext_iff]
  dsimp [oldS, oldP, companionE, companionS, target]
  omega

theorem both_old_pair_witnesses_exist
    (width incident near far : Int) (hlength : 6 ≤ incident) (hwidth : incident+4 ≤ width) :
    endpoint width near far (0,incident+3) ∧ endpoint width near far (1,incident+2) := by
  unfold endpoint
  dsimp
  omega

def cornerX (bottom near : Int) (point : Point) : Prop :=
  endpoint (bottom-2) near 6 (point.2-3,point.1-2)

def parentH (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.1-(bottom-1-incident),point.2-4)

def secondary (bottom width : Int) (point : Point) : Prop :=
  endpoint width 10 4 (point.1-(bottom-11),point.2-5)

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def upward (bottom width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth (width+2) far (width+9-point.2,bottom-4-point.1)

theorem every_two_owner_witness_is_an_actual_chain_endpoint
    (bottom near parentWidth parentIncident parentFar width : Int)
    (hbottom : 18 ≤ bottom) (hparent : 12 ≤ parentIncident) :
    cornerX bottom near (bottom-7,4) ∧
      parentH bottom parentWidth parentIncident parentFar (bottom-7,5) ∧
      parentH bottom parentWidth parentIncident parentFar (bottom-3,5) ∧
      secondary bottom width (bottom-3,6) ∧
      returning bottom (bottom-4,7) ∧
      cornerX bottom near (bottom-4,4) ∧
      parentH bottom parentWidth parentIncident parentFar (bottom-4,5) := by
  unfold cornerX parentH secondary returning endpoint
  dsimp
  omega

theorem lower_intrusion_and_secondary_tip_exclude_old_owner_identifications
    (bottom near parentWidth parentIncident parentFar : Int)
    (hbottom : 18 ≤ bottom) (hwidth : 6 ≤ parentWidth) (hparent : 12 ≤ parentIncident) :
    ¬cornerX bottom near (bottom-1,5) ∧
      ¬parentH bottom parentWidth parentIncident parentFar (bottom-1,6) ∧
      ¬parentH bottom parentWidth parentIncident parentFar (bottom-6,7) ∧
      ¬parentH bottom parentWidth parentIncident parentFar (bottom-5,7) := by
  unfold cornerX parentH endpoint
  dsimp
  omega

theorem rigid_terminal_tile_has_three_prescribed_endpoints
    (bottom width breadth far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width (bottom-6,6) ∧
      secondary bottom width (bottom-5,6) ∧
      upward bottom width breadth far (bottom-5,7) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem a_single_original_owner_cannot_contain_two_different_owner_witnesses
    (Owner : Type) (owner : Point → Owner) (original first second : Owner)
    (firstPoint secondPoint : Point)
    (hfirst : owner firstPoint = first) (hsecond : owner secondPoint = second)
    (hdifferent : first ≠ second) (horiginalFirst : owner firstPoint = original)
    (horiginalSecond : owner secondPoint = original) : False := by
  exact hdifferent (hfirst.symm.trans (horiginalFirst.trans (horiginalSecond.symm.trans hsecond)))

def successor (bottom width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth width far (width+7-point.2,bottom-5-point.1)

theorem short_parents_force_the_parent_width_past_the_secondary_bar
    (bottom width parentWidth parentIncident parentFar : Int)
    (hparentWidth : 6 ≤ parentWidth) (hfar : 4 ≤ parentFar)
    (hparent : parentIncident = 12 ∨ parentIncident = 14)
    (heven : width % 2 = 0) (hparentEven : parentWidth % 2 = 0)
    (hdisjoint : ∀ point, parentH bottom parentWidth parentIncident parentFar point →
      secondary bottom width point → False) :
    width+2 ≤ parentWidth := by
  by_cases hlarge : width+2 ≤ parentWidth
  · exact hlarge
  · have hsmall : parentWidth ≤ width := by omega
    exact False.elim (hdisjoint (bottom-11,parentWidth+4)
      (by unfold parentH endpoint; dsimp; omega)
      (by unfold secondary endpoint; dsimp; omega))

theorem parent_twelve_hits_the_new_successor_bar
    (bottom width parentWidth parentFar breadth far : Int)
    (hwidth : 6 ≤ width) (hlarge : width+2 ≤ parentWidth) (hbreadth : 8 ≤ breadth) :
    parentH bottom parentWidth 12 parentFar (bottom-13,width+6) ∧
      successor bottom width breadth far (bottom-13,width+6) := by
  unfold parentH successor endpoint
  dsimp
  omega

theorem parent_fourteen_next_width_hits_the_successor_bar
    (bottom width parentFar breadth far : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ parentFar) (hbreadth : 8 ≤ breadth) :
    parentH bottom (width+2) 14 parentFar (bottom-13,width+6) ∧
      successor bottom width breadth far (bottom-13,width+6) := by
  unfold parentH successor endpoint
  dsimp
  omega

theorem parent_fourteen_larger_width_hits_the_upward_bar
    (bottom width parentWidth parentFar breadth far : Int)
    (hwidth : 6 ≤ width) (hlarge : width+4 ≤ parentWidth) (hbreadth : 10 ≤ breadth) :
    parentH bottom parentWidth 14 parentFar (bottom-14,width+8) ∧
      upward bottom width breadth far (bottom-14,width+8) := by
  unfold parentH upward endpoint
  dsimp
  omega

theorem neither_parent_twelve_nor_fourteen_has_disjoint_prescribed_sources
    (bottom width parentWidth parentIncident parentFar breadth far upwardBreadth upwardFar : Int)
    (hwidth : 6 ≤ width) (hparentWidth : 6 ≤ parentWidth) (hfar : 4 ≤ parentFar)
    (hparent : parentIncident = 12 ∨ parentIncident = 14)
    (heven : width % 2 = 0) (hparentEven : parentWidth % 2 = 0)
    (hbreadth : 8 ≤ breadth) (hupward : 10 ≤ upwardBreadth)
    (hdisjointD : ∀ point, parentH bottom parentWidth parentIncident parentFar point →
      secondary bottom width point → False)
    (hdisjointC : ∀ point, parentH bottom parentWidth parentIncident parentFar point →
      successor bottom width breadth far point → False)
    (hdisjointE : ∀ point, parentH bottom parentWidth parentIncident parentFar point →
      upward bottom width upwardBreadth upwardFar point → False) : False := by
  have hlarge := short_parents_force_the_parent_width_past_the_secondary_bar
    bottom width parentWidth parentIncident parentFar hparentWidth hfar
    hparent heven hparentEven hdisjointD
  rcases hparent with hparent | hparent
  · subst parentIncident
    have hcollision := parent_twelve_hits_the_new_successor_bar
      bottom width parentWidth parentFar breadth far hwidth hlarge hbreadth
    exact hdisjointC _ hcollision.1 hcollision.2
  · subst parentIncident
    by_cases hnext : parentWidth = width+2
    · subst parentWidth
      have hcollision := parent_fourteen_next_width_hits_the_successor_bar
        bottom width parentFar breadth far hwidth hfar hbreadth
      exact hdisjointC _ hcollision.1 hcollision.2
    · have hlargeNext : width+4 ≤ parentWidth := by omega
      have hcollision := parent_fourteen_larger_width_hits_the_upward_bar
        bottom width parentWidth parentFar upwardBreadth upwardFar hwidth hlargeNext hupward
      exact hdisjointE _ hcollision.1 hcollision.2

def ceilHalf (value : Int) : Int := (value+1)/2

theorem the_same_inventory_single_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+ceilHalf (m8-resolved-residual+extra+added) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem every_two_new_single_activations_gain_one (baseline added : Int) :
    ceilHalf (baseline+added+2)-ceilHalf (baseline+added) = 1 := by
  unfold ceilHalf
  omega

theorem one_new_single_activation_gains_zero_or_one (baseline : Int) :
    ceilHalf (baseline+1)-ceilHalf baseline = 0 ∨
      ceilHalf (baseline+1)-ceilHalf baseline = 1 := by
  unfold ceilHalf
  omega

theorem the_new_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryTenTightActivationTransfer
