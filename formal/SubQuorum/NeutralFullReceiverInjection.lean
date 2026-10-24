import SubQuorum.NeutralSupportInjection
import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.NeutralFullReceiverInjection

open NeutralSupportInjection

def addPoint (first second : Point) : Point :=
  (first.1+second.1,first.2+second.2)

def tileSites (frame : Frame) : List Point :=
  [(0,0),frame.1,(-frame.2.1,-frame.2.2),
   (frame.1.1-frame.2.1,frame.1.2-frame.2.2)]

def extendedActiveSites (frame : Frame) : List Point :=
  [(-frame.1.1-frame.2.1,-frame.1.2-frame.2.2),
   (-frame.2.1,-frame.2.2),
   (frame.1.1-frame.2.1,frame.1.2-frame.2.2),
   (2*frame.1.1-frame.2.1,2*frame.1.2-frame.2.2)]

theorem regular_receiver_has_four_original_endpoints
    (width left right row : Int) (hwidth : 6 ≤ width)
    (hrow : 3 ≤ row) (hupper : row+1 ≤ left) :
    WidthSixBottomOwner.endpoint width left right (row+1,1) ∧
    WidthSixBottomOwner.endpoint width left right (row,1) ∧
    WidthSixBottomOwner.endpoint width left right (row-1,1) ∧
    WidthSixBottomOwner.endpoint width left right (row-2,1) := by
  repeat' apply And.intro
  all_goals simp [WidthSixBottomOwner.endpoint] <;> omega

theorem first_receiver_has_four_original_endpoints
    (width left right : Int) (hwidth : 6 ≤ width) (hleft : 4 ≤ left) :
    WidthSixBottomOwner.endpoint width left right (left,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-1,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-2,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-3,1) := by
  repeat' apply And.intro
  all_goals simp [WidthSixBottomOwner.endpoint] <;> omega

theorem long_receiver_has_four_original_endpoints
    (width left right incomingWidth : Int) (hwidth : 6 ≤ width)
    (hincoming : 6 ≤ incomingWidth) (hlong : incomingWidth+4 ≤ left) :
    WidthSixBottomOwner.endpoint width left right (left-incomingWidth,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-incomingWidth-1,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-incomingWidth-2,1) ∧
    WidthSixBottomOwner.endpoint width left right (left-incomingWidth-3,1) := by
  repeat' apply And.intro
  all_goals simp [WidthSixBottomOwner.endpoint] <;> omega

set_option maxHeartbeats 2000000 in
theorem phase_zero_one_forced_owner_is_terminal
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : WidthSixBottomOwner.endpoint width left right anchor)
    (hwest : ¬ WidthSixBottomOwner.endpoint width left right
      (WidthSixBottomOwner.pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouth : ¬ WidthSixBottomOwner.endpoint width left right
      (WidthSixBottomOwner.pull transpose flipRow flipColumn anchor (1,0)))
    (hnorthwest : ¬ WidthSixBottomOwner.endpoint width left right
      (WidthSixBottomOwner.pull transpose flipRow flipColumn anchor (-1,-1)))
    (hsoutheast : ¬ WidthSixBottomOwner.endpoint width left right
      (WidthSixBottomOwner.pull transpose flipRow flipColumn anchor (1,1)))
    (hrow : (anchor.1-(if flipRow then 0 else 1))%2 = 0)
    (hcolumn : (anchor.2-(if flipColumn then 0 else 1))%2 = 1) :
    anchor = (left,1) ∨ anchor = (right,width) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [WidthSixBottomOwner.endpoint, WidthSixBottomOwner.pull, Prod.mk.injEq]
        at hwest hsouth hnorthwest hsoutheast hrow hcolumn ⊢ <;> omega

set_option maxHeartbeats 2000000 in
theorem shared_tile_stencils_have_same_forced_point
    (tag : Point → Option Point) (first second : Frame) (point : Point)
    (hfirst : first ∈ frames) (hsecond : second ∈ frames)
    (hpoint : point ∈ tileSites first)
    (htile : ∀ site ∈ tileSites second, addPoint point site ∈ tileSites first)
    (hfirstActive : ∀ site ∈ extendedActiveSites first, tag site = some first.1)
    (hfirstPassive : ∀ site ∈ passiveSites first,
      tag site = none ∨ tag site = some first.2)
    (hsecondActive : ∀ site ∈ extendedActiveSites second,
      tag (addPoint point site) = some second.1)
    (hsecondPassive : ∀ site ∈ passiveSites second,
      tag (addPoint point site) = none ∨ tag (addPoint point site) = some second.2) :
    point = (0,0) := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hfirst hsecond
  rcases hfirst with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals
    simp only [tileSites, List.mem_cons, List.not_mem_nil, or_false] at hpoint
    rcases hpoint with rfl | rfl | rfl | rfl
  all_goals first
    | rfl
    | (rcases hsecond with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl)
  all_goals simp [tileSites, addPoint, extendedActiveSites, passiveSites, baseFrame]
    at htile hfirstActive hfirstPassive hsecondActive hsecondPassive
  all_goals simp_all

theorem first_and_long_receiver_map_is_injective
    {Event Tile : Type} (receiver : Event → Tile) (point : Event → Point)
    (frame : Event → Frame) (tag : Point → Option Point)
    (hframe : ∀ event, frame event ∈ frames)
    (hactive : ∀ event site, site ∈ extendedActiveSites (frame event) →
      tag (addPoint (point event) site) = some (frame event).1)
    (hpassive : ∀ event site, site ∈ passiveSites (frame event) →
      tag (addPoint (point event) site) = none ∨
      tag (addPoint (point event) site) = some (frame event).2)
    (hreceiver : ∀ earlier later, receiver earlier = receiver later →
      ((point later).1-(point earlier).1,
        (point later).2-(point earlier).2) ∈ tileSites (frame earlier))
    (htile : ∀ earlier later, receiver earlier = receiver later →
      ∀ site ∈ tileSites (frame later),
        addPoint ((point later).1-(point earlier).1,
          (point later).2-(point earlier).2) site ∈ tileSites (frame earlier))
    (hpoint : ∀ earlier later, point earlier = point later → earlier = later) :
    ∀ earlier later, receiver earlier = receiver later → earlier = later := by
  intro earlier later hequal
  have htranslate : ∀ site, addPoint (point earlier)
      (addPoint ((point later).1-(point earlier).1,
        (point later).2-(point earlier).2) site) = addPoint (point later) site := by
    intro site
    apply Prod.ext <;> simp only [addPoint] <;> omega
  have hzero := shared_tile_stencils_have_same_forced_point
    (fun site => tag (addPoint (point earlier) site)) (frame earlier) (frame later)
    ((point later).1-(point earlier).1,(point later).2-(point earlier).2)
    (hframe earlier) (hframe later) (hreceiver earlier later hequal)
    (htile earlier later hequal) (hactive earlier) (hpassive earlier)
    (by
      intro site hsite
      simpa only [htranslate] using hactive later site hsite)
    (by
      intro site hsite
      simpa only [htranslate] using hpassive later site hsite)
  apply hpoint earlier later
  have hcoordinates := Prod.mk.inj hzero
  exact Prod.ext (by omega) (by omega)

theorem additional_endpoint_count_for_first_and_long_receivers
    (contacts long nonfull full additional : Nat)
    (hpartition : contacts+long = nonfull+full)
    (hcount : additional = nonfull+2*full) :
    additional+nonfull = 2*(contacts+long) := by omega

theorem joint_receivers_in_the_shared_corner_budget
    (contacts long nonfull additional passive activation boundary : Nat)
    (hcount : additional+nonfull = 2*(contacts+long))
    (hbudget : passive+nonfull ≤ 2*activation+boundary) :
    2*(contacts+long)+passive ≤ additional+2*activation+boundary := by omega

theorem AA_closed_receivers_with_long_exits
    (components phase01 phase10 contacts long additional nonfull : Nat)
    (hphase : contacts+phase10 = phase01)
    (hturn : 4*components+phase10 ≤ phase01)
    (hcount : additional+nonfull = 2*(contacts+long)) (hstops : nonfull = 0) :
    8*components+2*long ≤ additional := by omega

end SubQuorum.NeutralFullReceiverInjection
