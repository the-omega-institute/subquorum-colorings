import SubQuorum.NeutralPhaseElevenInjection

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseElevenCriticalInjection

open NeutralSupportInjection

def criticalActiveSites (frame : Frame) : List Point :=
  [(frame.1.1-frame.2.1,frame.1.2-frame.2.2),frame.1,
   (frame.1.1+frame.2.1,frame.1.2+frame.2.2)]

def criticalCornerSites (frame : Frame) : List Point :=
  [(-frame.2.1,-frame.2.2),(-2*frame.2.1,-2*frame.2.2)]

def criticalDiagonal (frame : Frame) : Point :=
  (frame.2.1-frame.1.1,frame.2.2-frame.1.2)

def ordinaryDiagonal (frame : Frame) : Point :=
  (frame.1.1-frame.2.1,frame.1.2-frame.2.2)

theorem critical_frame_is_unique
    (tag : Point → Option Point) (first second : Frame)
    (hfirst : first ∈ frames) (hsecond : second ∈ frames)
    (hdiagonal : criticalDiagonal first = criticalDiagonal second)
    (hfirstActive : ∀ point ∈ criticalActiveSites first, tag point = some first.1)
    (hfirstCorner : ∀ point ∈ criticalCornerSites first, tag point = none)
    (hsecondActive : ∀ point ∈ criticalActiveSites second, tag point = some second.1)
    (hsecondCorner : ∀ point ∈ criticalCornerSites second, tag point = none) :
    first = second := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hfirst hsecond
  rcases hfirst with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals rcases hsecond with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals first
    | rfl
    | (simp [criticalDiagonal, criticalActiveSites, criticalCornerSites, baseFrame] at hdiagonal hfirstActive hfirstCorner hsecondActive hsecondCorner <;> simp_all)

theorem critical_and_first_stencils_are_disjoint
    (tag : Point → Option Point) (critical first : Frame)
    (hcritical : critical ∈ frames) (hfirst : first ∈ frames)
    (hdiagonal : criticalDiagonal critical = ordinaryDiagonal first)
    (hcriticalActive : ∀ point ∈ criticalActiveSites critical, tag point = some critical.1)
    (hcriticalCorner : ∀ point ∈ criticalCornerSites critical, tag point = none)
    (hfirstActive : ∀ point ∈ activeSites first, tag point = some first.1)
    (hfirstPassive : ∀ point ∈ passiveSites first, tag point = some first.2) : False := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hcritical hfirst
  rcases hcritical with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals rcases hfirst with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [criticalDiagonal, ordinaryDiagonal, criticalActiveSites,
    criticalCornerSites, activeSites, passiveSites, baseFrame] at hdiagonal hcriticalActive hcriticalCorner hfirstActive hfirstPassive
  all_goals simp_all

theorem critical_and_long_stencils_are_disjoint
    (tag : Point → Option Point) (critical long : Frame)
    (hcritical : critical ∈ frames) (hlong : long ∈ frames)
    (hdiagonal : criticalDiagonal critical = ordinaryDiagonal long)
    (hcriticalActive : ∀ point ∈ criticalActiveSites critical, tag point = some critical.1)
    (hcriticalCorner : ∀ point ∈ criticalCornerSites critical, tag point = none)
    (hlongActive : ∀ point ∈ activeSites long, tag point = some long.1)
    (hlongCorner : ∀ point ∈ passiveSites long, tag point = none) : False := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hcritical hlong
  rcases hcritical with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals rcases hlong with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals simp [criticalDiagonal, ordinaryDiagonal, criticalActiveSites,
    criticalCornerSites, activeSites, passiveSites, baseFrame] at hdiagonal hcriticalActive hcriticalCorner hlongActive hlongCorner
  all_goals simp_all

theorem critical_forced_points_are_injective
    {Event Owner : Type} (critical first : Event → Point) (frame : Event → Frame)
    (owner : Event → Owner) (width : Owner → Int)
    (terminalHeight : Owner → Point → Int) (owns : Owner → Point → Prop)
    (tag : Point → Option Point) (diagonal : Point → Point)
    (hframe : ∀ event, frame event ∈ frames)
    (hdiagonal : ∀ event, diagonal (critical event) = criticalDiagonal (frame event))
    (hactive : ∀ event point, point ∈ criticalActiveSites (frame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = some (frame event).1)
    (hcorner : ∀ event point, point ∈ criticalCornerSites (frame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = none)
    (howner : ∀ event, owns (owner event)
      ((critical event).1-(frame event).2.1,(critical event).2-(frame event).2.2))
    (hunique : ∀ firstOwner secondOwner point,
      owns firstOwner point → owns secondOwner point → firstOwner = secondOwner)
    (hrecover : ∀ event, first event =
      (let height := terminalHeight (owner event)
         ((critical event).1-(frame event).2.1,(critical event).2-(frame event).2.2)
       ((critical event).1-(width (owner event)-1)*(frame event).1.1-(height+1)*(frame event).2.1,
        (critical event).2-(width (owner event)-1)*(frame event).1.2-(height+1)*(frame event).2.2)))
    (hfirstInjective : ∀ earlier later, first earlier = first later → earlier = later) :
    ∀ earlier later, critical earlier = critical later → earlier = later := by
  intro earlier later hequal
  have hsameFrame := critical_frame_is_unique
    (fun point => tag ((critical earlier).1+point.1,(critical earlier).2+point.2))
    (frame earlier) (frame later) (hframe earlier) (hframe later)
    (by rw [← hdiagonal earlier,← hdiagonal later,hequal])
    (hactive earlier) (hcorner earlier)
    (by simpa only [hequal] using hactive later)
    (by simpa only [hequal] using hcorner later)
  have hsameOwner : owner earlier = owner later := by
    apply hunique (owner earlier) (owner later)
      ((critical earlier).1-(frame earlier).2.1,(critical earlier).2-(frame earlier).2.2)
      (howner earlier)
    simpa only [hequal,hsameFrame] using howner later
  apply hfirstInjective earlier later
  rw [hrecover earlier,hrecover later,hequal,hsameFrame,hsameOwner]

theorem critical_and_first_point_sets_are_disjoint
    {CriticalEvent FirstEvent : Type}
    (critical : CriticalEvent → Point) (criticalFrame : CriticalEvent → Frame)
    (first : FirstEvent → Point) (firstFrame : FirstEvent → Frame)
    (tag : Point → Option Point) (diagonal : Point → Point)
    (hcriticalFrame : ∀ event, criticalFrame event ∈ frames)
    (hfirstFrame : ∀ event, firstFrame event ∈ frames)
    (hcriticalDiagonal : ∀ event, diagonal (critical event) = criticalDiagonal (criticalFrame event))
    (hfirstDiagonal : ∀ event, diagonal (first event) = ordinaryDiagonal (firstFrame event))
    (hcriticalActive : ∀ event point, point ∈ criticalActiveSites (criticalFrame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = some (criticalFrame event).1)
    (hcriticalCorner : ∀ event point, point ∈ criticalCornerSites (criticalFrame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = none)
    (hfirstActive : ∀ event point, point ∈ activeSites (firstFrame event) →
      tag ((first event).1+point.1,(first event).2+point.2) = some (firstFrame event).1)
    (hfirstPassive : ∀ event point, point ∈ passiveSites (firstFrame event) →
      tag ((first event).1+point.1,(first event).2+point.2) = some (firstFrame event).2) :
    ∀ criticalEvent firstEvent, critical criticalEvent ≠ first firstEvent := by
  intro criticalEvent firstEvent hequal
  exact critical_and_first_stencils_are_disjoint
    (fun point => tag ((critical criticalEvent).1+point.1,(critical criticalEvent).2+point.2))
    (criticalFrame criticalEvent) (firstFrame firstEvent)
    (hcriticalFrame criticalEvent) (hfirstFrame firstEvent)
    (by rw [← hcriticalDiagonal criticalEvent,← hfirstDiagonal firstEvent,hequal])
    (hcriticalActive criticalEvent) (hcriticalCorner criticalEvent)
    (by simpa only [hequal] using hfirstActive firstEvent)
    (by simpa only [hequal] using hfirstPassive firstEvent)

theorem critical_and_long_point_sets_are_disjoint
    {CriticalEvent LongEvent : Type}
    (critical : CriticalEvent → Point) (criticalFrame : CriticalEvent → Frame)
    (long : LongEvent → Point) (longFrame : LongEvent → Frame)
    (tag : Point → Option Point) (diagonal : Point → Point)
    (hcriticalFrame : ∀ event, criticalFrame event ∈ frames)
    (hlongFrame : ∀ event, longFrame event ∈ frames)
    (hcriticalDiagonal : ∀ event, diagonal (critical event) = criticalDiagonal (criticalFrame event))
    (hlongDiagonal : ∀ event, diagonal (long event) = ordinaryDiagonal (longFrame event))
    (hcriticalActive : ∀ event point, point ∈ criticalActiveSites (criticalFrame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = some (criticalFrame event).1)
    (hcriticalCorner : ∀ event point, point ∈ criticalCornerSites (criticalFrame event) →
      tag ((critical event).1+point.1,(critical event).2+point.2) = none)
    (hlongActive : ∀ event point, point ∈ activeSites (longFrame event) →
      tag ((long event).1+point.1,(long event).2+point.2) = some (longFrame event).1)
    (hlongCorner : ∀ event point, point ∈ passiveSites (longFrame event) →
      tag ((long event).1+point.1,(long event).2+point.2) = none) :
    ∀ criticalEvent longEvent, critical criticalEvent ≠ long longEvent := by
  intro criticalEvent longEvent hequal
  exact critical_and_long_stencils_are_disjoint
    (fun point => tag ((critical criticalEvent).1+point.1,(critical criticalEvent).2+point.2))
    (criticalFrame criticalEvent) (longFrame longEvent)
    (hcriticalFrame criticalEvent) (hlongFrame longEvent)
    (by rw [← hcriticalDiagonal criticalEvent,← hlongDiagonal longEvent,hequal])
    (hcriticalActive criticalEvent) (hcriticalCorner criticalEvent)
    (by simpa only [hequal] using hlongActive longEvent)
    (by simpa only [hequal] using hlongCorner longEvent)

theorem three_forced_point_sets_count
    (first long critical : List Point)
    (hfirst : first.Nodup) (hlong : long.Nodup) (hcritical : critical.Nodup)
    (hfirstLong : ∀ earlier ∈ first, ∀ later ∈ long, earlier ≠ later)
    (hfirstCritical : ∀ earlier ∈ first, ∀ later ∈ critical, earlier ≠ later)
    (hlongCritical : ∀ earlier ∈ long, ∀ later ∈ critical, earlier ≠ later) :
    ((first ++ long) ++ critical).Nodup ∧
      ((first ++ long) ++ critical).length = first.length+long.length+critical.length := by
  have hcombined := List.nodup_append.mpr ⟨hfirst,hlong,hfirstLong⟩
  have hseparate : ∀ earlier ∈ first ++ long, ∀ later ∈ critical, earlier ≠ later := by
    intro earlier hmember later hlater
    rcases List.mem_append.mp hmember with hbefore | hafter
    · exact hfirstCritical earlier hbefore later hlater
    · exact hlongCritical earlier hafter later hlater
  exact ⟨List.nodup_append.mpr ⟨hcombined,hcritical,hseparate⟩,
    by simp only [List.length_append]⟩

theorem all_phase_eleven_endpoint_count
    (contacts phaseEleven long critical endpoints : Nat)
    (hpartition : phaseEleven = long+critical)
    (hcount : endpoints = contacts+long+critical) :
    endpoints = contacts+phaseEleven := by omega

end SubQuorum.NeutralPhaseElevenCriticalInjection
