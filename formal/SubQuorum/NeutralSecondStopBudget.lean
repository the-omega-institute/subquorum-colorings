import SubQuorum.ClosedNeutralReceivers

set_option autoImplicit false

namespace SubQuorum.NeutralSecondStopBudget

open ClosedNeutralReceivers

theorem original_pairs_in_nonfull_tile_have_same_owner
    (owner : Corner → Option Nat) (missing : Corner)
    (first second : Corner × Corner) (firstOwner secondOwner : Nat)
    (hfirst : first ∈ adjacentPairs) (hsecond : second ∈ adjacentPairs)
    (hmissing : owner missing = none)
    (hfirstLeft : owner first.1 = some firstOwner)
    (hfirstRight : owner first.2 = some firstOwner)
    (hsecondLeft : owner second.1 = some secondOwner)
    (hsecondRight : owner second.2 = some secondOwner) :
    firstOwner = secondOwner := by
  have hmissingCases : missing = 0 ∨ missing = 1 ∨ missing = 2 ∨ missing = 3 := by
    have hbound : missing.val < 4 := missing.isLt
    simp only [Fin.ext_iff]
    omega
  simp only [adjacentPairs, List.mem_cons, List.not_mem_nil, or_false] at hfirst hsecond
  rcases hfirst with rfl | rfl | rfl | rfl
  all_goals rcases hsecond with rfl | rfl | rfl | rfl
  all_goals rcases hmissingCases with rfl | rfl | rfl | rfl
  all_goals simp_all

theorem nonfull_first_and_second_receivers_are_injective
    {Event Tile Point : Type}
    (receiver : Event → Tile) (active : Event → Nat) (point : Event → Point)
    (pair : Event → Corner × Corner) (owner : Tile → Corner → Option Nat)
    (missing : Tile → Corner) (supportAt : Nat → Tile → Point)
    (hpair : ∀ event, pair event ∈ adjacentPairs)
    (hmissing : ∀ tile, owner tile (missing tile) = none)
    (hleft : ∀ event, owner (receiver event) (pair event).1 = some (active event))
    (hright : ∀ event, owner (receiver event) (pair event).2 = some (active event))
    (hsupport : ∀ event, point event = supportAt (active event) (receiver event))
    (hpoint : ∀ earlier later, point earlier = point later → earlier = later) :
    ∀ earlier later, receiver earlier = receiver later → earlier = later := by
  intro earlier later hequal
  have hsameOwner := original_pairs_in_nonfull_tile_have_same_owner
    (owner (receiver earlier)) (missing (receiver earlier)) (pair earlier) (pair later)
    (active earlier) (active later) (hpair earlier) (hpair later)
    (hmissing (receiver earlier)) (hleft earlier) (hright earlier)
    (by simpa only [hequal] using hleft later)
    (by simpa only [hequal] using hright later)
  apply hpoint earlier later
  rw [hsupport earlier,hsupport later,hsameOwner,hequal]

theorem different_original_pair_owners_separate_nonfull_stops
    (owner : Corner → Option Nat) (missing : Corner)
    (first second : Corner × Corner) (firstOwner secondOwner : Nat)
    (hfirst : first ∈ adjacentPairs) (hsecond : second ∈ adjacentPairs)
    (hmissing : owner missing = none)
    (hfirstLeft : owner first.1 = some firstOwner)
    (hfirstRight : owner first.2 = some firstOwner)
    (hsecondLeft : owner second.1 = some secondOwner)
    (hsecondRight : owner second.2 = some secondOwner)
    (hdifferent : firstOwner ≠ secondOwner) : False := by
  exact hdifferent (original_pairs_in_nonfull_tile_have_same_owner owner missing
    first second firstOwner secondOwner hfirst hsecond hmissing
    hfirstLeft hfirstRight hsecondLeft hsecondRight)

theorem second_stops_share_the_corner_budget
    (counted direct unactivatedCorner activatedCorner terminal firstStop secondStop
      activation boundary : Nat)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hdefects : direct+unactivatedCorner+firstStop+secondStop ≤ boundary)
    (hcorner : activatedCorner ≤ activation) (hterminal : terminal ≤ activation) :
    counted+firstStop+secondStop ≤ 2*activation+boundary := by omega

theorem closed_turns_with_first_and_second_stops
    (components phase01 phase10 passive10 allPassive firstStop secondStop
      activation boundary : Nat)
    (hcurves : 4*components+phase10 ≤ phase01+2*passive10)
    (hsubset : passive10 ≤ allPassive)
    (hbudget : allPassive+firstStop+secondStop ≤ 2*activation+boundary) :
    4*components+phase10+2*(firstStop+secondStop) ≤ phase01+4*activation+2*boundary := by omega

theorem shared_stops_in_existing_reserve
    (counted firstStop secondStop activation unfilled rotor boundary reserve : Nat)
    (hbudget : counted+firstStop+secondStop ≤ 2*activation+boundary)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    counted+firstStop+secondStop+unfilled+rotor ≤ 2*reserve+activation := by omega

theorem AA_first_and_second_stops_vanish
    (direct unactivatedCorner firstStop secondStop boundary : Nat)
    (hbudget : direct+unactivatedCorner+firstStop+secondStop ≤ boundary)
    (hboundary : boundary = 0) :
    direct = 0 ∧ unactivatedCorner = 0 ∧ firstStop = 0 ∧ secondStop = 0 := by omega

end SubQuorum.NeutralSecondStopBudget
