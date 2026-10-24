import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.CriticalPhaseOneBarReturns

open WidthSixBottomOwner

set_option maxHeartbeats 2000000 in
theorem phase_zero_one_critical_owner_is_outer_bar_corner
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hnorth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hrow : (anchor.1-(if flipRow then 1 else 0))%2 = 0)
    (hcolumn : (anchor.2-(if flipColumn then 1 else 0))%2 = 1) :
    flipRow = false ∧
      ((flipColumn = false ∧ anchor = (0,1)) ∨
       (flipColumn = true ∧ anchor = (0,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, Prod.mk.injEq] at hnorth hwest hrow hcolumn ⊢ <;> omega

theorem critical_outer_bar_tile_is_originally_full
    (width left right : Int) (anchor : Point)
    (transpose flipColumn : Bool) (hwidth : 6 ≤ width)
    (hrole : (flipColumn = false ∧ anchor = (0,1)) ∨
      (flipColumn = true ∧ anchor = (0,width))) :
    ∀ point ∈ [(0,0),(1,0),(0,1),(1,1)],
      endpoint width left right (pull transpose false flipColumn anchor point) := by
  rcases hrole with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  all_goals
    intro point hpoint
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hpoint
    rcases hpoint with rfl | rfl | rfl | rfl
    all_goals cases transpose <;> simp [endpoint, pull] <;> omega

def outerCorner (width : Int) (far : Bool) : Point :=
  (0,if far then width else 1)

theorem distinct_outer_corners_cannot_share_a_tile
    (width : Int) (first second : Bool) (hwidth : 6 ≤ width)
    (hlower : (outerCorner width first).2-1 ≤ (outerCorner width second).2)
    (hupper : (outerCorner width second).2 ≤ (outerCorner width first).2+1) :
    first = second := by
  cases first <;> cases second <;> simp [outerCorner] at hlower hupper ⊢ <;> omega

theorem full_bar_return_receivers_are_injective
    {Event Owner Tile Site : Type}
    (receiver : Event → Tile) (point : Event → Site) (owner : Event → Owner)
    (inTile : Tile → Site → Prop) (owns : Owner → Site → Prop)
    (hroot : ∀ event, inTile (receiver event) (point event))
    (hfull : ∀ event site, inTile (receiver event) site → owns (owner event) site)
    (hunique : ∀ first second site, owns first site → owns second site → first = second)
    (hcorner : ∀ earlier later, owner earlier = owner later →
      receiver earlier = receiver later → point earlier = point later)
    (hpoint : ∀ earlier later, point earlier = point later → earlier = later) :
    ∀ earlier later, receiver earlier = receiver later → earlier = later := by
  intro earlier later hequal
  have hsameOwner := hunique (owner earlier) (owner later) (point earlier)
    (hfull earlier (point earlier) (hroot earlier))
    (hfull later (point earlier) (by simpa only [hequal] using hroot earlier))
  exact hpoint earlier later (hcorner earlier later hsameOwner hequal)

theorem originally_full_returns_avoid_regular_receivers
    {Regular Return Tile Corner Owner : Type}
    (regularTile : Regular → Tile) (returnTile : Return → Tile)
    (regularOwner : Regular → Owner) (returnOwner : Return → Owner)
    (ownerAt : Tile → Corner → Option Owner) (witness : Regular → Corner)
    (hregular : ∀ event,
      ownerAt (regularTile event) (witness event) = some (regularOwner event))
    (hmissing : ∀ event, ∃ corner,
      ownerAt (regularTile event) corner ≠ some (regularOwner event))
    (hfull : ∀ event corner,
      ownerAt (returnTile event) corner = some (returnOwner event)) :
    ∀ regular returned, regularTile regular ≠ returnTile returned := by
  intro regular returned hequal
  have hsame : regularOwner regular = returnOwner returned := by
    have hfirst := hregular regular
    rw [hequal, hfull] at hfirst
    exact (Option.some.inj hfirst).symm
  obtain ⟨corner,hcorner⟩ := hmissing regular
  apply hcorner
  rw [hequal, hfull, hsame]

def cornerPool {Owner Site : Type} (owners : List Owner)
    (corner : Owner → Bool → Site) : List Site :=
  owners.flatMap fun owner => [corner owner false,corner owner true]

theorem corner_pool_has_two_positions_per_owner
    {Owner Site : Type} (owners : List Owner) (corner : Owner → Bool → Site) :
    (cornerPool owners corner).length = 2*owners.length := by
  induction owners with
  | nil => simp [cornerPool]
  | cons owner rest inductionHypothesis =>
    simp only [cornerPool, List.flatMap_cons, List.length_append,
      List.length_cons, List.length_nil] at inductionHypothesis ⊢
    omega

theorem critical_bar_returns_use_at_most_two_positions_per_owner
    {Owner Site : Type} (owners : List Owner) (corner : Owner → Bool → Site)
    (returned : List Site) (hnodup : returned.Nodup)
    (hsubset : returned ⊆ cornerPool owners corner) :
    returned.length ≤ 2*owners.length := by
  have hbound := hnodup.length_le_of_subset hsubset
  simpa only [corner_pool_has_two_positions_per_owner] using hbound

theorem joint_regular_and_original_full_bar_endpoint_count
    (contacts long nonfull additional barReturns barEndpoints total : Nat)
    (hregular : additional+nonfull = 2*(contacts+long))
    (hbar : barEndpoints = 4*barReturns)
    (hdisjointCount : total = additional+barEndpoints) :
    total+nonfull = 2*(contacts+long)+4*barReturns := by omega

theorem joint_bar_returns_in_the_existing_shared_budget
    (contacts long nonfull barReturns total passive activation boundary : Nat)
    (hcount : total+nonfull = 2*(contacts+long)+4*barReturns)
    (hbudget : passive+nonfull ≤ 2*activation+boundary) :
    2*(contacts+long)+4*barReturns+passive ≤ total+2*activation+boundary := by omega

theorem AA_joint_bar_return_endpoint_requirement
    (curves contacts long nonfull barReturns total : Nat)
    (hcount : total+nonfull = 2*(contacts+long)+4*barReturns)
    (hturn : 4*curves ≤ contacts) (hstop : nonfull = 0) :
    8*curves+2*long+4*barReturns ≤ total := by omega

end SubQuorum.CriticalPhaseOneBarReturns
