import SubQuorum.NeutralSupportInjection

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseElevenInjection

open NeutralSupportInjection

theorem second_forced_frame_is_unique
    (tag : Point → Option Point) (first second : Frame)
    (hfirst : first ∈ frames) (hsecond : second ∈ frames)
    (hfirstActive : ∀ point ∈ activeSites first, tag point = some first.1)
    (hfirstCorner : ∀ point ∈ passiveSites first, tag point = none)
    (hsecondActive : ∀ point ∈ activeSites second, tag point = some second.1)
    (hsecondCorner : ∀ point ∈ passiveSites second, tag point = none) :
    first = second := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hfirst hsecond
  rcases hfirst with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals rcases hsecond with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals first
    | rfl
    | (simp [activeSites, passiveSites, baseFrame] at hfirstActive hfirstCorner hsecondActive hsecondCorner; simp_all)

theorem first_and_second_forced_stencils_are_disjoint
    (tag : Point → Option Point) (first second : Frame)
    (hfirst : first ∈ frames) (hsecond : second ∈ frames)
    (hfirstActive : ∀ point ∈ activeSites first, tag point = some first.1)
    (hfirstPassive : ∀ point ∈ passiveSites first, tag point = some first.2)
    (hsecondActive : ∀ point ∈ activeSites second, tag point = some second.1)
    (hsecondCorner : ∀ point ∈ passiveSites second, tag point = none) : False := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hfirst hsecond
  rcases hfirst with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals rcases hsecond with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [activeSites, passiveSites, baseFrame] at hfirstActive hfirstPassive hsecondActive hsecondCorner
  all_goals simp_all

theorem second_forced_points_are_injective
    {Event Owner : Type} (second first : Event → Point) (frame : Event → Frame)
    (owner : Event → Owner) (width : Owner → Int) (owns : Owner → Point → Prop)
    (tag : Point → Option Point)
    (hframe : ∀ event, frame event ∈ frames)
    (hactive : ∀ event point, point ∈ activeSites (frame event) →
      tag ((second event).1+point.1,(second event).2+point.2) = some (frame event).1)
    (hcorner : ∀ event point, point ∈ passiveSites (frame event) →
      tag ((second event).1+point.1,(second event).2+point.2) = none)
    (howner : ∀ event, owns (owner event)
      ((second event).1-(frame event).1.1,(second event).2-(frame event).1.2))
    (hunique : ∀ firstOwner secondOwner point,
      owns firstOwner point → owns secondOwner point → firstOwner = secondOwner)
    (hrecover : ∀ event, first event =
      ((second event).1-width (owner event)*(frame event).1.1,
       (second event).2-width (owner event)*(frame event).1.2))
    (hfirstInjective : ∀ earlier later, first earlier = first later → earlier = later) :
    ∀ earlier later, second earlier = second later → earlier = later := by
  intro earlier later hequal
  have hsameFrame := second_forced_frame_is_unique
    (fun point => tag ((second earlier).1+point.1,(second earlier).2+point.2))
    (frame earlier) (frame later) (hframe earlier) (hframe later)
    (hactive earlier) (hcorner earlier)
    (by simpa only [hequal] using hactive later)
    (by simpa only [hequal] using hcorner later)
  have hsameOwner : owner earlier = owner later := by
    apply hunique (owner earlier) (owner later)
      ((second earlier).1-(frame earlier).1.1,(second earlier).2-(frame earlier).1.2)
      (howner earlier)
    simpa only [hequal,hsameFrame] using howner later
  apply hfirstInjective earlier later
  rw [hrecover earlier,hrecover later,hequal,hsameFrame,hsameOwner]

theorem first_and_second_point_sets_are_disjoint
    {FirstEvent SecondEvent : Type}
    (first : FirstEvent → Point) (firstFrame : FirstEvent → Frame)
    (second : SecondEvent → Point) (secondFrame : SecondEvent → Frame)
    (tag : Point → Option Point)
    (hfirstFrame : ∀ event, firstFrame event ∈ frames)
    (hsecondFrame : ∀ event, secondFrame event ∈ frames)
    (hfirstActive : ∀ event point, point ∈ activeSites (firstFrame event) →
      tag ((first event).1+point.1,(first event).2+point.2) = some (firstFrame event).1)
    (hfirstPassive : ∀ event point, point ∈ passiveSites (firstFrame event) →
      tag ((first event).1+point.1,(first event).2+point.2) = some (firstFrame event).2)
    (hsecondActive : ∀ event point, point ∈ activeSites (secondFrame event) →
      tag ((second event).1+point.1,(second event).2+point.2) = some (secondFrame event).1)
    (hsecondCorner : ∀ event point, point ∈ passiveSites (secondFrame event) →
      tag ((second event).1+point.1,(second event).2+point.2) = none) :
    ∀ firstEvent secondEvent, first firstEvent ≠ second secondEvent := by
  intro firstEvent secondEvent hequal
  exact first_and_second_forced_stencils_are_disjoint
    (fun point => tag ((first firstEvent).1+point.1,(first firstEvent).2+point.2))
    (firstFrame firstEvent) (secondFrame secondEvent)
    (hfirstFrame firstEvent) (hsecondFrame secondEvent)
    (hfirstActive firstEvent) (hfirstPassive firstEvent)
    (by simpa only [hequal] using hsecondActive secondEvent)
    (by simpa only [hequal] using hsecondCorner secondEvent)

theorem combined_forced_points_count
    (first second : List Point) (hfirst : first.Nodup) (hsecond : second.Nodup)
    (hseparate : ∀ earlier ∈ first, ∀ later ∈ second, earlier ≠ later) :
    (first ++ second).Nodup ∧ (first ++ second).length = first.length+second.length := by
  exact ⟨List.nodup_append.mpr ⟨hfirst,hsecond,hseparate⟩,List.length_append⟩

end SubQuorum.NeutralPhaseElevenInjection
