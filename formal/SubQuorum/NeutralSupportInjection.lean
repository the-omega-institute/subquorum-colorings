import Std

set_option autoImplicit false

namespace SubQuorum.NeutralSupportInjection

abbrev Point := Int × Int
abbrev Frame := Point × Point

def baseFrame : Frame := ((-1,0),(0,1))

def frames : List Frame :=
  [baseFrame,((1,0),(0,1)),((1,0),(0,-1)),((0,1),(1,0)),
   ((0,1),(-1,0)),((-1,0),(0,-1)),((0,-1),(1,0)),((0,-1),(-1,0))]

def activeSites (frame : Frame) : List Point :=
  [(-frame.1.1-frame.2.1,-frame.1.2-frame.2.2),
   (-frame.2.1,-frame.2.2),
   (frame.1.1-frame.2.1,frame.1.2-frame.2.2)]

def passiveSites (frame : Frame) : List Point :=
  [(-frame.1.1,-frame.1.2),(-frame.1.1+frame.2.1,-frame.1.2+frame.2.2)]

def directionConflict (other : Frame) : Bool :=
  (activeSites baseFrame).any fun point =>
    ((activeSites other).contains point && decide (baseFrame.1 ≠ other.1)) ||
    ((passiveSites other).contains point && decide (baseFrame.1 ≠ other.2))

theorem exact_orientation_exhaustion :
    frames.filter (fun frame => !directionConflict frame) = [baseFrame] := by decide

theorem normalized_frame_is_unique (tag : Point → Point) (frame : Frame)
    (hframe : frame ∈ frames)
    (hbase : ∀ point ∈ activeSites baseFrame, tag point = baseFrame.1)
    (hactive : ∀ point ∈ activeSites frame, tag point = frame.1)
    (hpassive : ∀ point ∈ passiveSites frame, tag point = frame.2) :
    frame = baseFrame := by
  simp only [frames, List.mem_cons, List.not_mem_nil, or_false] at hframe
  rcases hframe with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rfl
  all_goals
    have htop := hbase (-1,-1) (by decide)
    have hmiddle := hbase (0,-1) (by decide)
    have hbottom := hbase (1,-1) (by decide)
    simp [activeSites, passiveSites] at hactive hpassive
    simp_all [baseFrame]

theorem equal_forced_point_and_frame_fix_active_endpoint
    (first second forced : Point) (frame : Frame)
    (hfirst : first = (forced.1-frame.1.1-frame.2.1,
                       forced.2-frame.1.2-frame.2.2))
    (hsecond : second = (forced.1-frame.1.1-frame.2.1,
                         forced.2-frame.1.2-frame.2.2)) : first = second := by
  exact hfirst.trans hsecond.symm

theorem two_distinct_anchors_force_consumption {Site : Type}
    (support occupied selected : Site → Prop) (point first second : Site)
    (hsupport : support point) (hfirst : occupied first) (hsecond : occupied second)
    (hdistinct : first ≠ second)
    (hretention : support point → ¬occupied point → selected point)
    (hdegree : selected point → occupied first → occupied second → first = second) :
    occupied point := by
  classical
  by_cases hoccupied : occupied point
  · exact hoccupied
  · exact False.elim (hdistinct (hdegree (hretention hsupport hoccupied) hfirst hsecond))

theorem joint_cap_and_pair_pool {Site : Type}
    (caps pairs pool : List Site) (hcaps : caps.Nodup) (hpairs : pairs.Nodup)
    (hseparate : ∀ first ∈ caps, ∀ second ∈ pairs, first ≠ second)
    (hsubset : caps ++ pairs ⊆ pool) : caps.length+pairs.length ≤ pool.length := by
  have hdistinct := List.nodup_append.mpr ⟨hcaps,hpairs,hseparate⟩
  have hcount := hdistinct.length_le_of_subset hsubset
  simpa only [List.length_append] using hcount

theorem any_pair_cap_count
    (phase01 phase10 phase11 negativeCap positiveCap unfilled irregularPair regularPair : Nat)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hpool : negativeCap+irregularPair+regularPair ≤ 2*phase01+2*phase10) :
    2*phase11+irregularPair+regularPair ≤
      2*phase01+2*phase10+positiveCap+unfilled := by omega

theorem any_pair_retained_defects
    (phase01 phase10 phase11 pairReserved positiveCap activation unfilled rotor boundary
      reserve : Nat)
    (hcount : 2*phase11+pairReserved ≤ 2*phase01+2*phase10+positiveCap+unfilled)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2*(phase11 : Int)-2*(phase01+phase10)+pairReserved+
      activation-positiveCap+rotor+boundary ≤ 2*reserve := by omega

theorem exact_unused_slot_identity
    (phase01 phase10 phase11 negativeCap positiveCap activation unfilled rotor boundary
      reserve pairReserved unused : Int)
    (hpool : negativeCap+pairReserved+unused = 2*phase01+2*phase10)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2*reserve = 2*(phase11-phase01-phase10)+pairReserved+
      (activation-positiveCap)+rotor+boundary+unused := by omega

theorem AA_any_pair_census
    (phase01 phase10 phase11 negativeCap irregularPair regularPair : Nat)
    (hcap : negativeCap = 2*phase11)
    (hpool : negativeCap+irregularPair+regularPair ≤ 2*phase01+2*phase10) :
    irregularPair+regularPair+2*phase11 ≤ 2*phase01+2*phase10 := by omega

theorem shared_corner_and_regular_stop_budget
    (counted direct unactivatedCorner activatedCorner terminal regularStop activation boundary : Nat)
    (hpartition : counted = direct+unactivatedCorner+activatedCorner+terminal)
    (hdefects : direct+unactivatedCorner+regularStop ≤ boundary)
    (hcorner : activatedCorner ≤ activation) (hterminal : terminal ≤ activation) :
    counted+regularStop ≤ 2*activation+boundary := by omega

theorem closed_curve_budget_with_regular_stops
    (components phase01 phase10 passive10 allPassive regularStop activation boundary : Nat)
    (hcurves : 4*components+phase10 ≤ phase01+2*passive10)
    (hsubset : passive10 ≤ allPassive)
    (hbudget : allPassive+regularStop ≤ 2*activation+boundary) :
    4*components+phase10+2*regularStop ≤ phase01+4*activation+2*boundary := by omega

end SubQuorum.NeutralSupportInjection
