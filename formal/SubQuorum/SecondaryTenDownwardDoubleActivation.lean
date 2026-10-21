import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenDownwardDoubleActivation

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 10 far (point.1-bottom+11,point.2-5)

def east (bottom level incident : Int) (point : Point) : Point :=
  (bottom-6-level+point.2,incident+7-point.1)

def parentH (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (point.1-bottom+1+incident,point.2-4)

def originalX (bottom near : Int) (point : Point) : Prop :=
  endpoint (bottom-2) near 6 (point.2-3,point.1-2)

theorem all_four_west_blockers_are_original_endpoints
    (bottom width far level : Int) (hlevel : 1 ≤ level) (hupper : level ≤ 4) :
    secondary bottom width far (bottom-5-level,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem all_four_supports_are_absent_from_D
    (bottom width far level : Int) (hwidth : 6 ≤ width)
    (hlevel : 1 ≤ level) (hupper : level ≤ 4) :
    ¬secondary bottom width far (bottom-5-level,7) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_north_bar_blocker_is_within_four_steps
    (bottom width far level : Int) (hwidth : 6 ≤ width)
    (hlevel : 1 ≤ level) (hupper : level ≤ 4) :
    secondary bottom width far (bottom-10,7) ∧
    1 ≤ (bottom-5-level)-(bottom-10) ∧
    (bottom-5-level)-(bottom-10) ≤ 4 := by
  unfold secondary endpoint
  dsimp
  omega

theorem both_north_rotor_blockers_are_original_endpoints
    (bottom width far level : Int) (hwidth : 6 ≤ width)
    (hlevel : 1 ≤ level) (hupper : level ≤ 4) :
    secondary bottom width far (bottom-7-level,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_far_fence_exists_at_every_stage
    (bottom width far level : Int) (hfar : 6 ≤ far)
    (hlevel : 0 ≤ level) (hupper : level ≤ 4) :
    secondary bottom width far (bottom-5-level,width+5) := by
  unfold secondary endpoint
  dsimp
  omega

theorem upward_bars_hit_the_lower_bar
    (bottom width far incident level : Int) (hlower : 6 ≤ incident)
    (hupper : incident ≤ width-4) :
    secondary bottom width far (bottom-10,incident+7) ∧
    east bottom level incident (0,level-4) = (bottom-10,incident+7) := by
  unfold secondary endpoint east
  simp only [Prod.ext_iff]
  omega

theorem each_preceding_owner_is_absent_at_the_next_target
    (bottom previous level row column : Int) (hprevious : previous < level)
    (hcolumn : 1 ≤ column) :
    (east bottom previous row (0,column)).1 > bottom-5-level := by
  unfold east
  omega

theorem insufficient_incident_growth_hits_the_preceding_stem
    (bottom level incident previous : Int) (hlower : 6 ≤ incident)
    (hupper : incident ≤ previous) :
    east bottom level incident (0,2) =
      east bottom (level-1) previous (previous-incident,1) ∧
    0 ≤ previous-incident ∧ previous-incident ≤ previous := by
  unfold east
  simp only [Prod.ext_iff]
  omega

theorem even_noncollision_requires_two_units
    (incident previous : Int) (heven : incident % 2 = 0)
    (hpreviousEven : previous % 2 = 0) (hnot : ¬incident ≤ previous) :
    previous+2 ≤ incident := by omega

theorem five_successive_incidents_force_width_eighteen
    (width first second third fourth fifth : Int)
    (hfirst : 6 ≤ first) (hsecond : first+2 ≤ second)
    (hthird : second+2 ≤ third) (hfourth : third+2 ≤ fourth)
    (hfifth : fourth+2 ≤ fifth) (hfence : fifth ≤ width-4) :
    first+8 ≤ fifth ∧ 18 ≤ width := by omega

theorem actual_B_fences_strengthen_the_secondary_width
    (width first fifth producerWidth : Int)
    (hfirst : 8 ≤ first)
    (hlarge : 14 ≤ producerWidth → 10 ≤ first)
    (hsteps : first+8 ≤ fifth) (hfence : fifth ≤ width-4) :
    20 ≤ width ∧ (14 ≤ producerWidth → 22 ≤ width) := by omega

theorem first_and_last_target_tiles_have_three_D_E_endpoints
    (bottom width far first second last : Int)
    (hwidth : 6 ≤ width) (hfar : 6 ≤ far) :
    secondary bottom width far (bottom-6,6) ∧
    secondary bottom width far (bottom-5,6) ∧
    east bottom 1 second (second,1) = (bottom-6,7) ∧
    east bottom 0 first (first,1) = (bottom-5,7) ∧
    secondary bottom width far (bottom-10,6) ∧
    secondary bottom width far (bottom-10,7) ∧
    secondary bottom width far (bottom-9,6) ∧
    east bottom 4 last (last,1) = (bottom-9,7) := by
  unfold secondary endpoint east
  simp only [Prod.ext_iff]
  dsimp
  omega

def oldS (incident : Int) (point : Point) : Point := (incident+3-point.1,3-point.2)
def oldP (point : Point) : Point := (point.2+2,point.1+2)
def oldEComp (incident : Int) (point : Point) : Point := (point.2+2,incident+3-point.1)
def oldSComp (incident : Int) (point : Point) : Point := (incident+3-point.1,point.2+2)
def frameS (bottom level : Int) (point : Point) : Point := (bottom-3-level-point.2,point.1+4)
def frameP (bottom level incident : Int) (point : Point) : Point :=
  (bottom-8-level+point.1,incident+9-point.2)
def frameEComp (bottom level : Int) (point : Point) : Point := (bottom-8-level+point.1,point.2+4)
def frameSComp (bottom level : Int) (point : Point) : Point := (bottom-8-level+point.2,point.1+4)

theorem all_four_old_charts_compose_to_the_whole_recipient
    (bottom level incident : Int) (point : Point) :
    frameS bottom level (oldS incident point) = east bottom level incident point ∧
    frameP bottom level incident (oldP point) = east bottom level incident point ∧
    frameEComp bottom level (oldEComp incident point) = east bottom level incident point ∧
    frameSComp bottom level (oldSComp incident point) = east bottom level incident point := by
  unfold frameS frameP frameEComp frameSComp oldS oldP oldEComp oldSComp east
  simp only [Prod.ext_iff]
  omega

theorem first_S_E_Scomp_and_last_S_have_actual_X_H_witnesses
    (bottom width incident far near : Int) (hbottom : 18 ≤ bottom)
    (hwidth : 6 ≤ width) (hincident : 12 ≤ incident) :
    originalX bottom near (bottom-4,4) ∧ parentH bottom width incident far (bottom-4,5) ∧
    parentH bottom width incident far (bottom-8,5) ∧
    originalX bottom near (bottom-7,4) ∧ parentH bottom width incident far (bottom-7,5) ∧
    originalX bottom near (bottom-8,4) := by
  unfold originalX parentH endpoint
  dsimp
  omega

theorem first_P_has_D_and_E2_witnesses
    (bottom width far incident : Int) :
    secondary bottom width far (bottom-8,6) ∧
    east bottom 2 incident (incident,1) = (bottom-7,7) := by
  unfold secondary endpoint east
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem last_P_hits_D_and_a_point_above_its_bar
    (bottom width far incident : Int) (hwidth : 6 ≤ width) :
    frameP bottom 4 incident (1,incident+3) = (bottom-11,6) ∧
    frameP bottom 4 incident (0,incident+3) = (bottom-12,6) ∧
    secondary bottom width far (bottom-11,6) ∧
    ¬secondary bottom width far (bottom-12,6) := by
  unfold frameP secondary endpoint
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem old_P_width_supplies_both_mandatory_bar_endpoints
    (width incident near far : Int) (hincident : 6 ≤ incident) (hwidth : incident+4 ≤ width) :
    endpoint width near far (0,incident+3) ∧
    endpoint width near far (1,incident+2) ∧
    endpoint width near far (1,incident+3) := by
  unfold endpoint
  dsimp
  omega

def equalLengthFrame (bottom : Int) (point : Point) : Point := (bottom+1-point.2,point.1+4)

theorem tight_and_near_Q2_h10_transport_recipient_and_both_old_X_points
    (bottom incident : Int) (point : Point) :
    equalLengthFrame bottom (incident+3-point.1,11-point.2) = east bottom 4 incident point ∧
    equalLengthFrame bottom (3,6) = east bottom 0 incident (incident,1) ∧
    equalLengthFrame bottom (3,7) = east bottom 1 incident (incident,1) := by
  unfold equalLengthFrame east
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem both_old_negative_Vcorners_supply_depth_three_and_four
    (width near far : Int) (hnear : near = 4 ∨ near = 6) :
    endpoint width near far (3,1) ∧ endpoint width near far (4,1) := by
  unfold endpoint
  dsimp
  omega

theorem unique_ownership_excludes_a_single_source_at_two_distinct_owners
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

theorem same_and_distinct_ordered_support_owner_profiles_cannot_coincide
    (Owner : Type) (first second : Owner) (hdifferent : first ≠ second) :
    ¬∃ common, first = common ∧ second = common := by
  rintro ⟨common,hfirst,hsecond⟩
  exact hdifferent (hfirst.trans hsecond.symm)

def bar (width : Int) (point : Point) : Prop :=
  (point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width

def withinRadius (radius : Int) (point candidate : Point) : Prop :=
  -radius ≤ point.1-candidate.1 ∧ point.1-candidate.1 ≤ radius ∧
  -radius ≤ point.2-candidate.2 ∧ point.2-candidate.2 ≤ radius

theorem depth_six_is_separated_from_all_depth_four_and_five_profiles
    (width : Int) (hwidth : 6 ≤ width) :
    (∃ candidate, bar width candidate ∧ withinRadius 4 (4,1) candidate) ∧
    (∃ candidate, bar width candidate ∧ withinRadius 4 (5,1) candidate) ∧
    ¬(∃ candidate, bar width candidate ∧ withinRadius 4 (6,1) candidate) := by
  constructor
  · refine ⟨(1,1),?_⟩
    unfold bar withinRadius
    dsimp
    omega
  · constructor
    · refine ⟨(1,1),?_⟩
      unfold bar withinRadius
      dsimp
      omega
    · rintro ⟨candidate,hbar,hclose⟩
      unfold bar at hbar
      unfold withinRadius at hclose
      dsimp at hclose
      omega

def ceilHalf (value : Int) : Int := (value+1)/2

theorem the_same_inventory_double_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+2*added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+added+ceilHalf (m8-resolved-residual+extra) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem double_activation_gains_exactly_one_per_claim (baseline added : Int) :
    ceilHalf (baseline+2*added)-ceilHalf baseline = added := by
  unfold ceilHalf
  omega

theorem the_double_activation_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+2*added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+2*added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryTenDownwardDoubleActivation
