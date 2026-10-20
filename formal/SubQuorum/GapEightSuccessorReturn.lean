import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.GapEightSuccessorReturn

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.2,point.1-1)

def returnEndpoint (width near far crossWidth height incident : Int)
    (point : Point) : Prop :=
  endpoint width near far (height+near-incident-point.2,crossWidth+2-point.1)

theorem forced_third_source_and_cross_share_an_endpoint
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hincident : 4 ≤ incident) (hnear : incident+2 ≤ returnNear) :
    crossEndpoint width height far (width+1,height+1) ∧
      returnEndpoint returnWidth returnNear returnFar width height incident
        (width+1,height+1) := by
  unfold crossEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem equal_endpoint_sets_force_the_return_length_identity
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hfar : 4 ≤ far) (hincident : 4 ≤ incident)
    (hnear : incident+2 ≤ returnNear)
    (hsame : ∀ point, crossEndpoint width height far point ↔
      returnEndpoint returnWidth returnNear returnFar width height incident point) :
    returnNear = incident+2 ∧ far = incident+2 := by
  have htop := (hsame (width+1,height+returnNear-incident)).mpr
  have hbottom := (hsame (width+1,height-incident)).mpr
  have hcrossbottom := (hsame (width+1,height+2-far)).mp
  unfold crossEndpoint returnEndpoint endpoint at htop hbottom hcrossbottom
  dsimp at htop hbottom hcrossbottom
  omega

theorem unequal_return_lengths_exclude_equal_endpoint_sets
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hfar : 4 ≤ far) (hincident : 4 ≤ incident)
    (hnear : incident+2 ≤ returnNear) (hunmatched : far ≠ incident+2) :
    ¬(∀ point, crossEndpoint width height far point ↔
      returnEndpoint returnWidth returnNear returnFar width height incident point) := by
  intro hsame
  exact hunmatched (equal_endpoint_sets_force_the_return_length_identity
    width height far returnWidth returnNear returnFar incident
    hwidth hreturn hfar hincident hnear hsame).2

theorem a_short_cross_far_leg_cannot_match_the_positive_successor
    (far incident other : Int) (hfar : far ≤ other+4)
    (hgrowth : other+4 ≤ incident) : far ≠ incident+2 := by
  omega

theorem the_new_axial_support_has_three_original_endpoint_neighbors
    (width height far : Int) (hwidth : 10 ≤ width) :
    crossEndpoint width height far (width-1,height+1) ∧
      crossEndpoint width height far (width+1,height+1) ∧
      crossEndpoint width height far (width,height+2) ∧
      ¬crossEndpoint width height far (width,height) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem the_new_lateral_support_has_two_straight_original_neighbors
    (width height far : Int) (hwidth : 10 ≤ width) (hfar : 4 ≤ far) :
    crossEndpoint width height far (width+1,height-1) ∧
      crossEndpoint width height far (width+1,height+1) ∧
      ¬crossEndpoint width height far (width,height) ∧
      ¬crossEndpoint width height far (width+2,height) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem the_old_tight_axial_role_has_two_straight_original_neighbors
    (width near far : Int) (hwidth : 6 ≤ width) (hnear : 4 ≤ near) :
    endpoint width near far (1,1) ∧ endpoint width near far (3,1) ∧
      ¬endpoint width near far (2,0) ∧ ¬endpoint width near far (2,2) := by
  unfold endpoint
  dsimp
  omega

theorem the_old_singleton_collision_has_a_self_owner_exclusion
    (width height far oldWidth oldNear oldFar : Int)
    (hwidth : 10 ≤ width) (hold : 6 ≤ oldWidth) :
    endpoint oldWidth oldNear oldFar (1,1) ∧
      endpoint oldWidth oldNear oldFar (0,1) ∧
      crossEndpoint width height far (width-1,height+2) ∧
      ¬crossEndpoint width height far (width-1,height+3) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem the_old_east_collision_has_a_self_owner_exclusion
    (width height far oldWidth oldNear oldFar : Int)
    (hwidth : 10 ≤ width) (hold : 6 ≤ oldWidth) (hnear : 4 ≤ oldNear) :
    endpoint oldWidth oldNear oldFar (2,1) ∧
      endpoint oldWidth oldNear oldFar (0,1) ∧
      crossEndpoint width height far (width+1,height+2) ∧
      ¬crossEndpoint width height far (width+3,height+2) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem the_old_south_collision_has_a_self_owner_exclusion
    (width height far oldWidth oldNear oldFar : Int)
    (hwidth : 10 ≤ width) (hold : 6 ≤ oldWidth) :
    endpoint oldWidth oldNear oldFar (1,2) ∧
      endpoint oldWidth oldNear oldFar (0,1) ∧
      crossEndpoint width height far (width+1,height+2) ∧
      ¬crossEndpoint width height far (width+2,height+3) := by
  unfold crossEndpoint endpoint
  dsimp
  omega

theorem the_joint_ledger_counts_each_new_channel_once
    (positive reserve demand unmarked oldClaims bandClaims successorClaims surplus
      capClaims pairClaims oldRemainder lowerPairs upperPairs receipts activations : Int)
    (hpartition : demand = oldClaims+capClaims+pairClaims+oldRemainder)
    (hmarked : demand ≤ 2*(positive-unmarked))
    (hinjection : oldClaims+bandClaims+successorClaims+surplus ≤ activations)
    (hinventory : activations+receipts+capClaims+2*lowerPairs+2*upperPairs ≤ 2*reserve) :
    2*unmarked+2*upperPairs+2*lowerPairs+receipts-pairClaims-oldRemainder+
      bandClaims+successorClaims+surplus ≤ 2*(positive+reserve-demand) := by
  omega

theorem the_joint_threshold_suffices_for_allocation
    (margin unmarked upperPairs lowerPairs receipts pairClaims oldRemainder
      bandClaims successorClaims surplus : Int)
    (hfloor : 2*unmarked+2*upperPairs+2*lowerPairs+receipts-pairClaims-oldRemainder+
      bandClaims+successorClaims+surplus ≤ 2*margin)
    (hthreshold : pairClaims+oldRemainder ≤
      2*unmarked+2*upperPairs+2*lowerPairs+receipts+surplus+
        bandClaims+successorClaims+1) : 0 ≤ margin := by
  omega

def ceilHalf (value : Int) : Int := -((-value)/2)

theorem two_new_claims_give_exactly_one_integer_gain (base : Int) :
    ceilHalf (base+2) = ceilHalf base+1 := by
  unfold ceilHalf
  omega

theorem one_new_claim_has_zero_or_one_integer_gain (base : Int) :
    ceilHalf (base+1)-ceilHalf base = 0 ∨
      ceilHalf (base+1)-ceilHalf base = 1 := by
  unfold ceilHalf
  omega

end SubQuorum.GapEightSuccessorReturn
