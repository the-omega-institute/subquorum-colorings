import Std

set_option autoImplicit false

namespace SubQuorum.EndpointComponentReserve

structure Component where
  unmarked : Int
  doubleMarked : Int
  exceptional : Int
  nonexceptionalDouble : Int
  reserve : Int

def qualifies (component : Component) : Prop :=
  0 < component.nonexceptionalDouble

instance (component : Component) : Decidable (qualifies component) :=
  inferInstanceAs (Decidable (0 < component.nonexceptionalDouble))

def componentMargin (component : Component) : Int :=
  component.unmarked+component.reserve-component.doubleMarked

def reserveTotal (components : List Component) : Int :=
  (components.map Component.reserve).sum

def unmarkedTotal (components : List Component) : Int :=
  (components.map Component.unmarked).sum

def doubleTotal (components : List Component) : Int :=
  (components.map Component.doubleMarked).sum

def qualifyingCount (components : List Component) : Int :=
  (components.map fun component => if qualifies component then 1 else 0).sum

def marginTotal (components : List Component) : Int :=
  (components.map componentMargin).sum

theorem qualifying_component_reserve (component : Component)
    (hnonnegative : 0 ≤ component.reserve)
    (hsaturated : component.reserve = 0 → component.nonexceptionalDouble = 0)
    (hqualifies : qualifies component) : 1 ≤ component.reserve := by
  unfold qualifies at hqualifies
  by_cases hzero : component.reserve = 0
  · have hbound := hsaturated hzero
    omega
  · omega

theorem reserve_dominates_indicator (component : Component)
    (hnonnegative : 0 ≤ component.reserve)
    (hsaturated : component.reserve = 0 → component.nonexceptionalDouble = 0) :
    (if qualifies component then 1 else 0) ≤ component.reserve := by
  split
  · exact qualifying_component_reserve component hnonnegative hsaturated ‹_›
  · exact hnonnegative

theorem component_count_reserve (components : List Component)
    (hnonnegative : ∀ component ∈ components, 0 ≤ component.reserve)
    (hsaturated : ∀ component ∈ components, component.reserve = 0 →
      component.nonexceptionalDouble = 0) :
    qualifyingCount components ≤ reserveTotal components := by
  induction components with
  | nil => simp [qualifyingCount, reserveTotal]
  | cons component remaining hypothesis =>
    have hcurrent := reserve_dominates_indicator component
      (hnonnegative component List.mem_cons_self) (hsaturated component List.mem_cons_self)
    have hremainingNonnegative : ∀ current ∈ remaining, 0 ≤ current.reserve := by
      intro current hmember
      exact hnonnegative current (List.mem_cons_of_mem component hmember)
    have hremainingSaturated : ∀ current ∈ remaining, current.reserve = 0 →
        current.nonexceptionalDouble = 0 := by
      intro current hmember
      exact hsaturated current (List.mem_cons_of_mem component hmember)
    have hremaining := hypothesis hremainingNonnegative hremainingSaturated
    simp only [qualifyingCount, reserveTotal, List.map_cons, List.sum_cons] at *
    omega

theorem exact_margin_sum (components : List Component) :
    marginTotal components = unmarkedTotal components+reserveTotal components-
      doubleTotal components := by
  induction components with
  | nil => simp [marginTotal, unmarkedTotal, reserveTotal, doubleTotal]
  | cons component remaining hypothesis =>
    simp only [marginTotal, unmarkedTotal, reserveTotal, doubleTotal,
      List.map_cons, List.sum_cons, componentMargin] at *
    omega

theorem component_count_slack (components : List Component) (slack : Int)
    (hledger : marginTotal components ≤ slack)
    (hnonnegative : ∀ component ∈ components, 0 ≤ component.reserve)
    (hsaturated : ∀ component ∈ components, component.reserve = 0 →
      component.nonexceptionalDouble = 0) :
    unmarkedTotal components-doubleTotal components+qualifyingCount components ≤ slack := by
  have hreserve := component_count_reserve components hnonnegative hsaturated
  have hmargin := exact_margin_sum components
  omega

theorem joint_from_component_count (components : List Component)
    (hnonnegative : ∀ component ∈ components, 0 ≤ component.reserve)
    (hsaturated : ∀ component ∈ components, component.reserve = 0 →
      component.nonexceptionalDouble = 0)
    (hcount : doubleTotal components-unmarkedTotal components ≤ qualifyingCount components) :
    0 ≤ marginTotal components := by
  have hreserve := component_count_reserve components hnonnegative hsaturated
  have hmargin := exact_margin_sum components
  omega

theorem negative_total_has_negative_component (components : List Component)
    (hnegative : marginTotal components < 0) :
    ∃ component ∈ components, componentMargin component < 0 := by
  induction components with
  | nil => simp [marginTotal] at hnegative
  | cons component remaining hypothesis =>
    by_cases hcurrent : componentMargin component < 0
    · exact ⟨component, List.mem_cons_self, hcurrent⟩
    · have hremaining : marginTotal remaining < 0 := by
        simp only [marginTotal, List.map_cons, List.sum_cons] at hnegative
        unfold marginTotal
        omega
      obtain ⟨current, hmember, hmargin⟩ := hypothesis hremaining
      exact ⟨current, List.mem_cons_of_mem component hmember, hmargin⟩

theorem nonexceptional_failure_needs_two_demands (component : Component)
    (hnonnegative : 0 ≤ component.reserve)
    (hexceptional : component.exceptional = 0)
    (hsaturated : component.reserve = 0 → component.doubleMarked ≤ component.exceptional)
    (hnegative : componentMargin component < 0) (hunmarked : 0 ≤ component.unmarked) :
    1 ≤ component.reserve ∧ component.unmarked+component.reserve+1 ≤ component.doubleMarked ∧
      component.unmarked+2 ≤ component.doubleMarked := by
  unfold componentMargin at hnegative
  by_cases hzero : component.reserve = 0
  · have hbound := hsaturated hzero
    omega
  · omega

theorem one_double_per_component_pays (components : List Component)
    (hnonnegative : ∀ component ∈ components, 0 ≤ component.reserve)
    (hunmarked : ∀ component ∈ components, 0 ≤ component.unmarked)
    (hexceptional : ∀ component ∈ components, component.exceptional = 0)
    (hsaturated : ∀ component ∈ components, component.reserve = 0 →
      component.doubleMarked ≤ component.exceptional)
    (hone : ∀ component ∈ components, component.doubleMarked ≤ 1) :
    0 ≤ marginTotal components := by
  by_cases hnonnegativeTotal : 0 ≤ marginTotal components
  · exact hnonnegativeTotal
  · obtain ⟨component, hmember, hnegative⟩ := negative_total_has_negative_component components
      (by omega)
    have htwo := nonexceptional_failure_needs_two_demands component
      (hnonnegative component hmember) (hexceptional component hmember)
      (hsaturated component hmember) hnegative (hunmarked component hmember)
    have hsingle := hone component hmember
    have hunmarkedCurrent := hunmarked component hmember
    omega

theorem component_defect_parity (reserve defect : Int) (hidentity : defect = 2*reserve) :
    defect%2 = 0 := by omega

theorem one_reserve_concentrates (first rest : Int)
    (hfirst : 1 ≤ first) (hrest : 0 ≤ rest) (htotal : first+rest = 1) :
    first = 1 ∧ rest = 0 := by omega

theorem integer_sum_nonnegative (values : List Int)
    (hnonnegative : ∀ value ∈ values, 0 ≤ value) : 0 ≤ values.sum := by
  induction values with
  | nil => simp
  | cons value remaining hypothesis =>
    have hhead := hnonnegative value List.mem_cons_self
    have htail : ∀ current ∈ remaining, 0 ≤ current := by
      intro current hmember
      exact hnonnegative current (List.mem_cons_of_mem value hmember)
    have hremaining := hypothesis htail
    simp only [List.sum_cons]
    omega

theorem nonnegative_remainder_sum (values : List Int)
    (hnonnegative : ∀ value ∈ values, 0 ≤ value) (hzero : values.sum = 0) :
    ∀ value ∈ values, value = 0 := by
  induction values with
  | nil => simp
  | cons value remaining hypothesis =>
    have hhead := hnonnegative value List.mem_cons_self
    have hremainingNonnegative : ∀ current ∈ remaining, 0 ≤ current := by
      intro current hmember
      exact hnonnegative current (List.mem_cons_of_mem value hmember)
    have hremainingSum := integer_sum_nonnegative remaining hremainingNonnegative
    have hheadZero : value = 0 := by simp only [List.sum_cons] at hzero; omega
    have htailZero : remaining.sum = 0 := by simp only [List.sum_cons] at hzero; omega
    intro current hmember
    rcases List.mem_cons.mp hmember with hequal | htail
    · simpa [hequal] using hheadZero
    · exact hypothesis hremainingNonnegative htailZero current htail

end SubQuorum.EndpointComponentReserve
