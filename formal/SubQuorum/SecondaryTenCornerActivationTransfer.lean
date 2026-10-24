import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenCornerActivationTransfer

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  point = (0,0) ∨ point = (0,width+1) ∨
  point = (near+1,1) ∨ point = (far+1,width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.1 % 2 = 0 ∧ point.2 = 0) ∨
  (3 ≤ point.1 ∧ point.1 ≤ near ∧ point.1 % 2 = 1 ∧ point.2 = 2) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.1 % 2 = 0 ∧ point.2 = width+1) ∨
  (3 ≤ point.1 ∧ point.1 ≤ far ∧ point.1 % 2 = 1 ∧ point.2 = width-1)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 10 far (point.1-bottom+11,point.2-5)

def corner (bottom : Int) (point : Point) : Point := (bottom-5-point.1,point.2+6)
def oldS (point : Point) : Point := (7-point.1,3-point.2)
def oldP (point : Point) : Point := (point.2+2,point.1+2)
def frameS (bottom : Int) (point : Point) : Point := (bottom-12+point.1,9-point.2)
def frameP (bottom : Int) (point : Point) : Point := (bottom-3-point.2,point.1+4)

theorem the_near_terminal_and_both_original_supports_exist
    (width far : Int) :
    endpoint width 4 far (4,1) ∧ support width 4 far (5,1) ∧
    support width 4 far (4,0) := by
  constructor
  · exact Or.inr (Or.inl ⟨by decide, by decide, rfl⟩)
  · constructor
    · exact Or.inr (Or.inr (Or.inl rfl))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨by decide, by decide, by decide, rfl⟩))))

theorem both_original_supports_are_consumed_by_D
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    corner bottom (5,1) = (bottom-10,7) ∧
    corner bottom (4,0) = (bottom-9,6) ∧
    secondary bottom width far (bottom-10,7) ∧
    secondary bottom width far (bottom-9,6) := by
  unfold corner secondary endpoint
  simp only [Prod.ext_iff]
  omega

theorem the_axial_original_point_has_exactly_three_neighbors
    (width far : Int) (point : Point) (hwidth : 6 ≤ width) :
    (endpoint width 10 far point ∧ adjacent (1,2) point) ↔
      point = (0,2) ∨ point = (1,1) ∨ point = (1,3) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_lateral_original_point_has_opposite_neighbors
    (width far : Int) (point : Point) (hwidth : 6 ≤ width) :
    (endpoint width 10 far point ∧ adjacent (2,1) point) ↔
      point = (1,1) ∨ point = (3,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_ordered_support_pair_recovers_its_unique_common_original_neighbor
    (width far : Int) (point : Point) (hwidth : 6 ≤ width) :
    (endpoint width 10 far point ∧ adjacent (1,2) point ∧ adjacent (2,1) point) ↔
      point = (1,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem the_target_tile_has_three_original_D_endpoints
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    corner bottom (4,1) = (bottom-9,7) ∧
    secondary bottom width far (bottom-10,6) ∧
    secondary bottom width far (bottom-10,7) ∧
    secondary bottom width far (bottom-9,6) := by
  unfold corner secondary endpoint
  simp only [Prod.ext_iff]
  omega

theorem the_supplied_geometric_counts_give_positive_charge
    (width far : Int) (heven : width % 2 = 0) :
    width-1+(4+far)/2+((4+far)/2+4)-
      2*(width/2+(4+far)/2+1) = 1 := by omega

theorem both_old_recipient_frames_compose_to_the_whole_corner
    (bottom : Int) (point : Point) :
    frameS bottom (oldS point) = corner bottom point ∧
    frameP bottom (oldP point) = corner bottom point := by
  unfold frameS frameP oldS oldP corner
  simp only [Prod.ext_iff]
  omega

theorem old_S_has_one_D_witness_and_one_endpoint_above_its_bar
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    frameS bottom (1,1) = (bottom-11,8) ∧
    frameS bottom (0,1) = (bottom-12,8) ∧
    secondary bottom width far (bottom-11,8) ∧
    ¬secondary bottom width far (bottom-12,8) := by
  unfold frameS secondary endpoint
  simp only [Prod.ext_iff]
  omega

theorem old_P_width_supplies_both_original_bar_endpoints
    (width near far : Int) (hwidth : 8 ≤ width) :
    endpoint width near far (0,7) ∧ endpoint width near far (1,7) := by
  unfold endpoint
  dsimp
  omega

theorem old_P_transports_the_two_required_bar_endpoints
    (bottom : Int) :
    frameP bottom (0,7) = (bottom-10,4) ∧
    frameP bottom (1,7) = (bottom-10,5) := by
  unfold frameP
  simp only [Prod.ext_iff]
  omega

def originalX (bottom near : Int) (point : Point) : Prop :=
  endpoint (bottom-2) near 6 (point.2-3,point.1-2)

def parentH (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.1-bottom+1+incident,point.2-4)

theorem both_P_witnesses_belong_to_the_stated_actual_owners
    (bottom near parentWidth parentIncident parentFar : Int)
    (hbottom : 18 ≤ bottom) (hparent : 12 ≤ parentIncident) :
    originalX bottom near (bottom-10,4) ∧
    parentH bottom parentWidth parentIncident parentFar (bottom-10,5) := by
  unfold originalX parentH endpoint
  dsimp
  omega

theorem the_H_intrusion_is_absent_from_X
    (bottom near : Int) (hbottom : 18 ≤ bottom) :
    ¬originalX bottom near (bottom-1,5) := by
  unfold originalX endpoint
  dsimp
  omega

theorem one_source_cannot_own_endpoints_from_two_distinct_original_owners
    (Owner : Type) (owns : Owner → Point → Prop) (first second producer : Owner)
    (firstPoint secondPoint : Point)
    (hunique : ∀ left right point, owns left point → owns right point → left = right)
    (hdifferent : first ≠ second) (hfirst : owns first firstPoint)
    (hsecond : owns second secondPoint) :
    ¬(owns producer firstPoint ∧ owns producer secondPoint) := by
  intro hproducer
  apply hdifferent
  exact (hunique first producer firstPoint hfirst hproducer.1).trans
    (hunique producer second secondPoint hproducer.2 hsecond)

theorem same_and_distinct_support_owner_profiles_cannot_coincide
    (Owner : Type) (first second : Owner) (hdifferent : first ≠ second) :
    ¬∃ common, first = common ∧ second = common := by
  rintro ⟨common,hfirst,hsecond⟩
  exact hdifferent (hfirst.trans hsecond.symm)

theorem every_nonmatched_upward_target_has_incident_length_at_least_eight
    (far intermediate incident : Int) (hfar : 4 ≤ far)
    (hintermediate : far+2 ≤ intermediate) (hincident : intermediate+2 ≤ incident) :
    8 ≤ incident ∧ incident ≠ 4 := by omega

def bar (width : Int) (point : Point) : Prop :=
  (point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width

def withinThree (point candidate : Point) : Prop :=
  -3 ≤ point.1-candidate.1 ∧ point.1-candidate.1 ≤ 3 ∧
  -3 ≤ point.2-candidate.2 ∧ point.2-candidate.2 ≤ 3

theorem the_new_terminal_is_within_three_of_its_intrinsic_bar
    (width : Int) (hwidth : 6 ≤ width) :
    ∃ candidate, bar width candidate ∧ withinThree (4,1) candidate := by
  refine ⟨(1,1),?_⟩
  unfold bar withinThree
  dsimp
  omega

theorem old_nonmatched_upward_terminals_are_not_within_three_of_their_bar
    (width incident : Int) (hincident : 8 ≤ incident) :
    ¬∃ candidate, bar width candidate ∧ withinThree (incident,1) candidate := by
  rintro ⟨candidate,hbar,hclose⟩
  unfold bar at hbar
  unfold withinThree at hclose
  dsimp at hclose
  omega

def ceilHalf (value : Int) : Int := (value+1)/2

theorem the_same_inventory_single_corner_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+ceilHalf (m8-resolved-residual+extra+added) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem every_two_new_corner_activations_gain_exactly_one (baseline added : Int) :
    ceilHalf (baseline+added+2)-ceilHalf (baseline+added) = 1 := by
  unfold ceilHalf
  omega

theorem one_new_corner_activation_gains_zero_or_one (baseline : Int) :
    ceilHalf (baseline+1)-ceilHalf baseline = 0 ∨
    ceilHalf (baseline+1)-ceilHalf baseline = 1 := by
  unfold ceilHalf
  omega

theorem the_corner_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryTenCornerActivationTransfer
