import Std

set_option autoImplicit false

namespace SubQuorum.MultiplePositiveSaturation

structure PositiveSource where
  width : Int
  leftHeight : Int
  rightHeight : Int
  leftMarked : Bool
  rightMarked : Bool

def sideCount (source : PositiveSource) : Int :=
  (if source.leftMarked then 1 else 0)+(if source.rightMarked then 1 else 0)

def unmarkedCount (sources : List PositiveSource) : Int :=
  (sources.map fun source => if source.leftMarked || source.rightMarked then 0 else 1).sum

def singleCount (sources : List PositiveSource) : Int :=
  (sources.map fun source => if source.leftMarked != source.rightMarked then 1 else 0).sum

def doubleCount (sources : List PositiveSource) : Int :=
  (sources.map fun source => if source.leftMarked && source.rightMarked then 1 else 0).sum

def markedTotal (sources : List PositiveSource) : Int :=
  (sources.map sideCount).sum

def Exceptional (source : PositiveSource) : Prop :=
  source.width ≠ 6 ∧ (12 ≤ source.width ∨ 8 ≤ max source.leftHeight source.rightHeight)

instance (source : PositiveSource) : Decidable (Exceptional source) :=
  inferInstanceAs (Decidable (source.width ≠ 6 ∧
    (12 ≤ source.width ∨ 8 ≤ max source.leftHeight source.rightHeight)))

def exceptionalCount (sources : List PositiveSource) : Int :=
  (sources.map fun source => if Exceptional source then 1 else 0).sum

theorem source_census (sources : List PositiveSource) :
    (sources.length : Int) = unmarkedCount sources+singleCount sources+doubleCount sources := by
  induction sources with
  | nil => simp [unmarkedCount, singleCount, doubleCount]
  | cons source remaining hypothesis =>
    rcases source with ⟨width, leftHeight, rightHeight, leftMarked, rightMarked⟩
    cases leftMarked <;> cases rightMarked <;>
      simp_all [unmarkedCount, singleCount, doubleCount] <;> omega

theorem marked_census (sources : List PositiveSource) :
    markedTotal sources = singleCount sources+2*doubleCount sources := by
  induction sources with
  | nil => simp [markedTotal, singleCount, doubleCount]
  | cons source remaining hypothesis =>
    rcases source with ⟨width, leftHeight, rightHeight, leftMarked, rightMarked⟩
    cases leftMarked <;> cases rightMarked <;>
      simp_all [markedTotal, sideCount, singleCount, doubleCount] <;> omega

theorem exact_demand_margin (sources : List PositiveSource) (reserve : Int) :
    (sources.length : Int)+reserve-markedTotal sources =
      unmarkedCount sources+reserve-doubleCount sources := by
  have hsource := source_census sources
  have hmarked := marked_census sources
  omega

theorem joint_iff_shared_defect_count (sources : List PositiveSource) (reserve defect : Int)
    (hidentity : 2*reserve = defect) :
    0 ≤ (sources.length : Int)+reserve-markedTotal sources ↔
      2*doubleCount sources ≤ 2*unmarkedCount sources+defect := by
  have hmargin := exact_demand_margin sources reserve
  omega

theorem failure_iff_double_excess (sources : List PositiveSource) (reserve : Int) :
    (sources.length : Int)+reserve-markedTotal sources < 0 ↔
      unmarkedCount sources+reserve+1 ≤ doubleCount sources := by
  have hmargin := exact_demand_margin sources reserve
  omega

theorem small_dimensions_not_exceptional (source : PositiveSource)
    (hsmall : source.width = 6 ∨
      (source.width ≤ 10 ∧ source.leftHeight ≤ 6 ∧ source.rightHeight ≤ 6)) :
    ¬Exceptional source := by
  unfold Exceptional
  simp only [Int.max_def]
  split <;> omega

theorem saturated_double_count_bound (sources : List PositiveSource)
    (hgeometry : ∀ source ∈ sources, source.leftMarked = true → source.rightMarked = true →
      Exceptional source) : doubleCount sources ≤ exceptionalCount sources := by
  induction sources with
  | nil => simp [doubleCount, exceptionalCount]
  | cons source remaining hypothesis =>
    have hremaining : ∀ current ∈ remaining, current.leftMarked = true →
        current.rightMarked = true → Exceptional current := by
      intro current hmember hleft hright
      exact hgeometry current (List.mem_cons_of_mem source hmember) hleft hright
    have hbound := hypothesis hremaining
    have hcurrent := hgeometry source List.mem_cons_self
    rcases source with ⟨width, leftHeight, rightHeight, leftMarked, rightMarked⟩
    cases leftMarked <;> cases rightMarked <;>
      simp_all [doubleCount, exceptionalCount] <;> split <;> omega

theorem no_exceptional_sources (sources : List PositiveSource)
    (hsmall : ∀ source ∈ sources, source.width = 6 ∨
      (source.width ≤ 10 ∧ source.leftHeight ≤ 6 ∧ source.rightHeight ≤ 6)) :
    exceptionalCount sources = 0 := by
  induction sources with
  | nil => simp [exceptionalCount]
  | cons source remaining hypothesis =>
    have hcurrent := small_dimensions_not_exceptional source
      (hsmall source List.mem_cons_self)
    have hremaining : ∀ current ∈ remaining, current.width = 6 ∨
        (current.width ≤ 10 ∧ current.leftHeight ≤ 6 ∧ current.rightHeight ≤ 6) := by
      intro current hmember
      exact hsmall current (List.mem_cons_of_mem source hmember)
    simpa [exceptionalCount, hcurrent] using hypothesis hremaining

theorem saturated_slack_bound (sources : List PositiveSource) (slack : Int)
    (hledger : (sources.length : Int)-markedTotal sources ≤ slack)
    (hgeometry : ∀ source ∈ sources, source.leftMarked = true → source.rightMarked = true →
      Exceptional source) : unmarkedCount sources-exceptionalCount sources ≤ slack := by
  have hmargin := exact_demand_margin sources 0
  have hbound := saturated_double_count_bound sources hgeometry
  omega

theorem saturated_joint_if_exceptional_paid (sources : List PositiveSource)
    (hgeometry : ∀ source ∈ sources, source.leftMarked = true → source.rightMarked = true →
      Exceptional source)
    (hpaid : exceptionalCount sources ≤ unmarkedCount sources) :
    0 ≤ (sources.length : Int)-markedTotal sources := by
  have hmargin := exact_demand_margin sources 0
  have hbound := saturated_double_count_bound sources hgeometry
  omega

theorem unmarked_count_nonnegative (sources : List PositiveSource) :
    0 ≤ unmarkedCount sources := by
  induction sources with
  | nil => simp [unmarkedCount]
  | cons source remaining hypothesis =>
    simp only [unmarkedCount, List.map_cons, List.sum_cons] at *
    split <;> omega

theorem saturated_small_dimensions_joint (sources : List PositiveSource)
    (hgeometry : ∀ source ∈ sources, source.leftMarked = true → source.rightMarked = true →
      Exceptional source)
    (hsmall : ∀ source ∈ sources, source.width = 6 ∨
      (source.width ≤ 10 ∧ source.leftHeight ≤ 6 ∧ source.rightHeight ≤ 6)) :
    0 ≤ (sources.length : Int)-markedTotal sources := by
  have hzero := no_exceptional_sources sources hsmall
  have hnonnegative := unmarked_count_nonnegative sources
  exact saturated_joint_if_exceptional_paid sources hgeometry (by omega)

theorem saturated_failure_needs_many_exceptional (sources : List PositiveSource)
    (hgeometry : ∀ source ∈ sources, source.leftMarked = true → source.rightMarked = true →
      Exceptional source)
    (hfailure : (sources.length : Int)-markedTotal sources < 0) :
    unmarkedCount sources+1 ≤ exceptionalCount sources := by
  have hmargin := exact_demand_margin sources 0
  have hbound := saturated_double_count_bound sources hgeometry
  omega

theorem separate_rounding_overcharge (defect oddCount localCeilings reserve : Int)
    (hglobal : 2*reserve = defect)
    (hlocal : 2*localCeilings = defect+oddCount) :
    2*(localCeilings-reserve) = oddCount := by omega

theorem distinct_single_defects_do_not_pay_two_double_marks :
    let positive : Int := 2
    let marked : Int := 4
    let defect : Int := 2
    let reserve : Int := 1
    2*reserve = defect ∧ 0 < defect ∧ positive+reserve-marked < 0 := by decide

end SubQuorum.MultiplePositiveSaturation
