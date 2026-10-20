import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.CapContinuationBudget

open WidthSixBottomOwner

set_option maxHeartbeats 1000000 in
theorem U_triple_arm_extends
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hroot : endpoint width left right anchor)
    (hnorth : endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,0)))
    (hwest : endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hmissing : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,-1))) :
    endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-2)) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull] at hnorth hwest hmissing ⊢ <;> omega

def capBlockers : List Point :=
  [(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),
   (-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),(-1,4),
   (0,-1),(1,-1),(2,-1)]

theorem phase11_cap_has_no_rotor_filler : rotorOwners capBlockers = [] := by decide

theorem different_pairs_cannot_reuse_point {Site : Type}
    (first second third fourth : Site) (otherCorners : List Site)
    (hdistinct : [first,second,third,fourth].Nodup)
    (hsubset : [first,second,third,fourth] ⊆ otherCorners)
    (hsize : otherCorners.length ≤ 3) : False := by
  have hcount := hdistinct.length_le_of_subset hsubset
  simp only [List.length_cons, List.length_nil] at hcount
  omega

theorem simultaneous_original_occurrence_budget {Site : Type}
    (capSlots continuationSlots indirectSlots pool : List Site)
    (hcap : capSlots.Nodup) (hcontinuation : continuationSlots.Nodup)
    (hindirect : indirectSlots.Nodup)
    (hcapContinuation : ∀ first ∈ capSlots, ∀ second ∈ continuationSlots, first ≠ second)
    (hcapIndirect : ∀ first ∈ capSlots, ∀ second ∈ indirectSlots, first ≠ second)
    (hcontinuationIndirect : ∀ first ∈ continuationSlots,
      ∀ second ∈ indirectSlots, first ≠ second)
    (hsubset : capSlots ++ (continuationSlots ++ indirectSlots) ⊆ pool) :
    capSlots.length+continuationSlots.length+indirectSlots.length ≤ pool.length := by
  have hsecond : (continuationSlots ++ indirectSlots).Nodup :=
    List.nodup_append.mpr ⟨hcontinuation,hindirect,hcontinuationIndirect⟩
  have hseparate : ∀ first ∈ capSlots, ∀ second ∈ continuationSlots ++ indirectSlots,
      first ≠ second := by
    intro first hfirst second hsecond
    rcases List.mem_append.mp hsecond with hcontinuation | hindirect
    · exact hcapContinuation first hfirst second hcontinuation
    · exact hcapIndirect first hfirst second hindirect
  have hdistinct := List.nodup_append.mpr ⟨hcap,hsecond,hseparate⟩
  have hcount := hdistinct.length_le_of_subset hsubset
  simpa only [List.length_append, Nat.add_assoc] using hcount

theorem cap_continuation_count
    (phase01 phase10 phase11 unfilled activation paired indirect negativeCap positiveCap : Nat)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hpositive : positiveCap ≤ activation)
    (hpool : negativeCap+2*paired+2*indirect ≤ 2*phase10+2*phase01) :
    2*phase11+2*paired+2*indirect ≤ 2*phase10+2*phase01+activation+unfilled := by omega

theorem all_pair_reserved_count
    (phase01 phase10 phase11 unfilled pairReserved negativeCap positiveCap : Nat)
    (hcap : negativeCap+positiveCap+unfilled = 2*phase11)
    (hpool : negativeCap+pairReserved ≤ 2*phase10+2*phase01) :
    2*phase11+pairReserved ≤ 2*phase10+2*phase01+positiveCap+unfilled := by omega

theorem all_pair_reserved_defect_budget
    (phase01 phase10 phase11 pairReserved positiveCap activation unfilled rotor boundary
      reserve : Nat)
    (hcount : 2*phase11+pairReserved ≤ 2*phase10+2*phase01+positiveCap+unfilled)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2*(phase11 : Int)-2*(phase10+phase01)+pairReserved+
      activation-positiveCap+rotor+boundary ≤ 2*reserve := by omega

theorem all_pair_reserved_AA_census
    (phase01 phase10 phase11 pairReserved negativeCap : Nat)
    (hcap : negativeCap = 2*phase11)
    (hpool : negativeCap+pairReserved ≤ 2*phase10+2*phase01) :
    pairReserved ≤ 2*(phase10+phase01-phase11) := by omega

theorem cap_continuation_reserve
    (phase01 phase10 phase11 paired indirect activation unfilled rotor boundary reserve : Nat)
    (hcount : 2*phase11+2*paired+2*indirect ≤
      2*phase10+2*phase01+activation+unfilled)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    phase11+paired+indirect ≤ phase10+phase01+reserve := by omega

theorem retained_defect_budget
    (phase01 phase10 phase11 paired indirect positiveCap activation unfilled rotor boundary
      reserve : Nat)
    (hcount : 2*phase11+2*paired+2*indirect ≤
      2*phase10+2*phase01+positiveCap+unfilled)
    (hidentity : 2*reserve = activation+unfilled+rotor+boundary) :
    2*(phase11+paired+indirect : Int)-2*(phase10+phase01)+
      activation-positiveCap+rotor+boundary ≤ 2*reserve := by omega

theorem saturated_without_positive_cap_fillers
    (phase01 phase10 phase11 paired indirect negativeCap positiveCap : Nat)
    (hcap : negativeCap+positiveCap = 2*phase11)
    (hpositive : positiveCap = 0)
    (hpool : negativeCap+2*paired+2*indirect ≤ 2*phase10+2*phase01) :
    phase11+paired+indirect ≤ phase10+phase01 := by omega

theorem paired_intermediates_are_limited
    (phase01 phase10 phase11 paired indirect : Nat)
    (hcount : phase11+paired+indirect ≤ phase10+phase01)
    (hindirect : indirect ≤ paired) :
    2*indirect ≤ phase10+phase01-phase11 := by omega

theorem balanced_census_has_no_paired_intermediate
    (phase01 phase10 phase11 paired indirect : Nat)
    (hcount : phase11+paired+indirect ≤ phase10+phase01)
    (hbalance : phase10+phase01 = phase11) : paired = 0 ∧ indirect = 0 := by omega

theorem incoming_owner_contains_collision (width incident far short : Int)
    (hwidth : 6 ≤ width) (hshort : 4 ≤ short) (hincident : short ≤ incident) :
    endpoint width incident far (incident+1-short,1) ∧
      ¬ endpoint width incident far (incident+2-short,3) := by
  simp [endpoint]
  omega

theorem reserve_bounds_combine_by_maximum (reserve first second : Nat)
    (hfirst : first ≤ reserve) (hsecond : second ≤ reserve) :
    max first second ≤ reserve := by omega

end SubQuorum.CapContinuationBudget
