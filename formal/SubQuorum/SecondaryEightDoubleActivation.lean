import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryEightDoubleActivation

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 8 far (point.1-(bottom-9),point.2-5)

def east (bottom level width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+7-point.2,point.1-(bottom-6-level))

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

theorem q_is_forced_by_two_fixed_neighbors (bottom width far : Int) :
    support 6 8 4 (4,7) ∧ secondary bottom width far (bottom-5,6) ∧
      returning bottom (bottom-4,7) := by
  unfold support secondary returning endpoint
  dsimp
  omega

theorem none_of_the_fixed_sources_owns_any_chain_site
    (bottom width far level : Int) (hwidth : 6 ≤ width)
    (hlow : 0 ≤ level) (hhigh : level ≤ 2) :
    ¬returning bottom (bottom-5-level,7) ∧
      ¬secondary bottom width far (bottom-5-level,7) := by
  unfold returning secondary endpoint
  dsimp
  omega

theorem the_north_U_blocker_is_on_the_lower_bar
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-8,7) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_two_north_rotor_blockers_are_secondary_owned (bottom width far : Int)
    (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-7,6) ∧
      secondary bottom width far (bottom-8,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_first_east_rotor_blockers_are_return_owned (bottom : Int) :
    returning bottom (bottom-4,9) ∧ returning bottom (bottom-4,10) := by
  unfold returning endpoint
  dsimp
  omega

theorem east_sources_have_no_endpoint_above_their_terminal_row
    (bottom level width incident far : Int) (point : Point)
    (hwidth : 1 ≤ width)
    (hpoint : east bottom level width incident far point) :
    bottom-5-level ≤ point.1 := by
  unfold east endpoint at hpoint
  omega

theorem every_chain_stem_is_bounded_by_the_secondary_far_leg
    (bottom level width far breadth incident other : Int)
    (hlow : 0 ≤ level) (hhigh : level ≤ 2) (hwidth : 6 ≤ width)
    (hfar : 4 ≤ far) (hbreadth : 6 ≤ breadth) (hlength : width-2 ≤ incident) :
    secondary bottom width far (bottom-5-level,width+5) ∧
      east bottom level breadth incident other (bottom-5-level,width+5) := by
  unfold secondary east endpoint
  dsimp
  omega

theorem every_upward_bar_hits_the_secondary_lower_bar
    (bottom level width far breadth incident : Int)
    (hlow : 0 ≤ level) (hhigh : level ≤ 2) (hbreadth : 6 ≤ breadth)
    (hlength : 4 ≤ incident) (hupper : incident ≤ width-4) :
    endpoint breadth incident 4 (0,4-level) ∧
      secondary bottom width far (bottom-8,incident+7) := by
  unfold secondary endpoint
  dsimp
  omega

theorem first_length_four_hits_the_return (bottom breadth far : Int)
    (hbreadth : 6 ≤ breadth) :
    east bottom 0 breadth 4 far (bottom-4,10) ∧ returning bottom (bottom-4,10) := by
  unfold east returning endpoint
  dsimp
  omega

theorem n_is_two_original_supports_with_different_anchors
    (width far breadth incident other : Int) (hlength : 6 ≤ incident)
    (heven : incident % 2 = 0) :
    support width 8 far (3,2) ∧ support breadth incident other (incident,0) := by
  unfold support
  omega

theorem n_has_two_fixed_endpoint_neighbors
    (bottom width far breadth incident other : Int) (hlength : 6 ≤ incident) :
    secondary bottom width far (bottom-6,6) ∧
      east bottom 0 breadth incident other (bottom-5,7) := by
  unfold secondary east endpoint
  dsimp
  omega

theorem both_east_rotors_hit_the_preceding_stem
    (bottom level breadth incident other : Int) (hlength : 6 ≤ incident) :
    east bottom level breadth incident other (bottom-5-level,8) ∧
      east bottom level breadth incident other (bottom-5-level,9) := by
  unfold east endpoint
  dsimp
  omega

theorem p_has_three_fixed_endpoint_neighbors
    (bottom width far breadth incident other : Int) (hwidth : 6 ≤ width)
    (hlength : 6 ≤ incident) :
    secondary bottom width far (bottom-7,6) ∧
      secondary bottom width far (bottom-8,7) ∧
      east bottom 1 breadth incident other (bottom-6,7) := by
  unfold secondary east endpoint
  dsimp
  omega

theorem an_insufficient_incident_length_hits_the_preceding_row
    (bottom level firstWidth firstLength firstFar nextWidth nextLength nextFar : Int)
    (_hfirst : 4 ≤ firstLength) (hnext : 4 ≤ nextLength)
    (hwidth : 6 ≤ firstWidth) (hnextWidth : 6 ≤ nextWidth)
    (horder : nextLength ≤ firstLength) :
    east bottom level firstWidth firstLength firstFar (bottom-5-level,nextLength+7) ∧
      east bottom (level+1) nextWidth nextLength nextFar (bottom-5-level,nextLength+7) := by
  unfold east endpoint
  dsimp
  omega

theorem both_final_terminal_supports_are_secondary_endpoints
    (bottom width far breadth incident other : Int) (hwidth : 6 ≤ width)
    (hlength : 6 ≤ incident) (heven : incident % 2 = 0) :
    support breadth incident other (incident+1,1) ∧
      support breadth incident other (incident,0) ∧
      secondary bottom width far (bottom-7,6) ∧
      secondary bottom width far (bottom-8,7) := by
  unfold support secondary endpoint
  dsimp
  omega

theorem final_terminal_tile_has_three_secondary_endpoints
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-8,6) ∧
      secondary bottom width far (bottom-8,7) ∧
      secondary bottom width far (bottom-7,6) := by
  unfold secondary endpoint
  dsimp
  omega

theorem both_axial_supports_have_original_straight_degree_two
    (width far position : Int) (point : Point) (hwidth : 6 ≤ width)
    (hposition : position = 2 ∨ position = 4) :
    (endpoint width 8 far point ∧ adjacent (position,1) point) ↔
      point = (position-1,1) ∨ point = (position+1,1) := by
  unfold endpoint adjacent
  simp only [Prod.ext_iff]
  dsimp
  omega

def target (bottom level incident : Int) (point : Point) : Point :=
  (bottom-6-level+point.2,incident+7-point.1)

def oldS (incident : Int) (point : Point) : Point := (incident+3-point.1,3-point.2)
def oldP (point : Point) : Point := (point.2+2,point.1+2)
def companionE (incident : Int) (point : Point) : Point := (point.2+2,incident+3-point.1)
def companionS (incident : Int) (point : Point) : Point := (incident+3-point.1,point.2+2)

theorem all_four_first_target_frame_compositions
    (bottom incident : Int) (point : Point) :
    (bottom-3-(oldS incident point).2,(oldS incident point).1+4) = target bottom 0 incident point ∧
    (bottom-8+(oldP point).1,incident+9-(oldP point).2) = target bottom 0 incident point ∧
    (bottom-8+(companionE incident point).1,(companionE incident point).2+4) = target bottom 0 incident point ∧
    (bottom-8+(companionS incident point).2,(companionS incident point).1+4) = target bottom 0 incident point := by
  simp only [Prod.ext_iff]
  dsimp [oldS, oldP, companionE, companionS, target]
  omega

theorem final_target_S_P_frame_compositions
    (bottom incident : Int) (point : Point) :
    (bottom-5-(oldS incident point).2,(oldS incident point).1+4) = target bottom 2 incident point ∧
    (bottom-10+(oldP point).1,incident+9-(oldP point).2) = target bottom 2 incident point := by
  simp only [Prod.ext_iff]
  dsimp [oldS, oldP, target]
  omega

theorem both_old_P_first_target_witnesses_exist
    (width incident near far : Int) (hlength : 6 ≤ incident) (hwidth : incident+4 ≤ width) :
    endpoint width near far (0,incident+3) ∧ endpoint width near far (1,incident+2) := by
  unfold endpoint
  dsimp
  omega

theorem final_P_witness_forces_secondary_then_leaves_it
    (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-9,6) ∧ ¬secondary bottom width far (bottom-10,6) := by
  unfold secondary endpoint
  dsimp
  omega

def tightProducer (bottom oldLength : Int) (point : Point) : Point :=
  (bottom+oldLength-7-point.2,point.1+4)

def tightCorner (point : Point) : Point := (point.2+2,point.1+3)

theorem tight_corner_transport_at_length_eight (bottom : Int) (point : Point) :
    tightProducer bottom 8 (tightCorner point) = (bottom-2-point.1,point.2+6) := by
  apply Prod.ext <;> dsimp [tightProducer, tightCorner] <;> omega

theorem tight_corner_has_both_different_owner_witnesses (width far : Int) :
    endpoint width 4 far (3,1) ∧ endpoint width 4 far (4,1) := by
  unfold endpoint
  omega

theorem a_single_original_owner_cannot_contain_the_two_tight_witnesses
    (Owner : Type) (owner : Point → Owner) (original first middle : Owner)
    (q n : Point) (hfirst : owner q = first) (hmiddle : owner n = middle)
    (hdifferent : first ≠ middle) (hq : owner q = original) (hn : owner n = original) : False := by
  exact hdifferent (hfirst.symm.trans (hq.trans (hn.symm.trans hmiddle)))

theorem secondary_eight_cannot_be_secondary_six_or_near_tight
    (oldLength : Int) (hold : oldLength = 6 ∨ 10 ≤ oldLength) (hequal : oldLength = 8) : False := by omega

theorem local_and_actual_width_bounds (first middle last width gate parent : Int)
    (hfirst : 6 ≤ first) (hmiddle : first+2 ≤ middle) (hlast : middle+2 ≤ last)
    (hupper : last ≤ width-4) (hgate : 12 ≤ gate)
    (hfence : 10 ≤ first ∨ gate-4 ≤ first) (hparent : width ≤ parent-2) :
    14 ≤ width ∧ 16 ≤ width ∧ 18 ≤ parent ∧
      (14 ≤ gate → 18 ≤ width ∧ 20 ≤ parent) := by omega

theorem local_width_fourteen (first middle last width : Int)
    (hfirst : 6 ≤ first) (hmiddle : first+2 ≤ middle) (hlast : middle+2 ≤ last)
    (hupper : last ≤ width-4) : 14 ≤ width := by omega

theorem parent_ten_has_only_the_two_covered_lengths (length : Int)
    (hlow : 6 ≤ length) (hhigh : length ≤ 10-2) (heven : length % 2 = 0) :
    length = 6 ∨ length = 8 := by omega

theorem the_intermediate_isolated_charge_is_minus_one
    (width near far : Int) (hwidth : width % 2 = 0)
    (hlegs : (near+far) % 2 = 0) :
    (width-1+(near+far)/2)+(near+far)/2-2*((width+near+far)/2) = -1 := by omega

def ceilHalf (value : Int) : Int := (value+1)/2

theorem same_inventory_double_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldTargets added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldTargets+caps+resolved+residual)
    (hreserve : oldTargets+2*added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+added+ceilHalf (m8-resolved-residual+extra) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem each_double_activation_claim_gains_one (baseline added : Int) :
    ceilHalf (baseline+2*added) = added+ceilHalf baseline := by
  unfold ceilHalf
  omega

theorem the_double_activation_coefficient_one_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldTargets added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldTargets+caps+resolved+residual)
    (hreserve : oldTargets+2*added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+2*added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryEightDoubleActivation
