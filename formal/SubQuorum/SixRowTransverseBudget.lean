import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SixRowTransverseBudget

abbrev Point := Int × Int

structure Transverse where
  bar : Int
  facesRight : Bool
  near : Int
  far : Int
  near_min : 4 ≤ near
  far_min : 4 ≤ far

def onBar (source : Transverse) (point : Point) : Prop :=
  0 ≤ point.1 ∧ point.1 ≤ 5 ∧
    (point.2 = source.bar ∨ point.2 = source.bar+1)

def endpoint (source : Transverse) (point : Point) : Prop :=
  onBar source point ∨
  (source.facesRight = true ∧
    ((point.1 = 5 ∧ source.bar+2 ≤ point.2 ∧ point.2 ≤ source.bar+source.near) ∨
     (point.1 = 0 ∧ source.bar+2 ≤ point.2 ∧ point.2 ≤ source.bar+source.far))) ∨
  (source.facesRight = false ∧
    ((point.1 = 5 ∧ source.bar+1-source.near ≤ point.2 ∧ point.2 ≤ source.bar-1) ∨
     (point.1 = 0 ∧ source.bar+1-source.far ≤ point.2 ∧ point.2 ≤ source.bar-1)))

def disjoint (first second : Transverse) : Prop :=
  ∀ point, endpoint first point → ¬ endpoint second point

def topTip (source : Transverse) : Int :=
  if source.facesRight then source.bar+source.far else source.bar+1-source.far

def topSupport (source : Transverse) : Int :=
  if source.facesRight then topTip source+1 else topTip source-1

theorem bar_owns_all_rows (source : Transverse) (row column : Int)
    (hrow : 0 ≤ row ∧ row ≤ 5)
    (hcolumn : column = source.bar ∨ column = source.bar+1) :
    endpoint source (row,column) := by
  exact Or.inl ⟨hrow.1,hrow.2,hcolumn⟩

theorem endpoints_stay_in_strip (source : Transverse) (point : Point)
    (hpoint : endpoint source point) : 0 ≤ point.1 ∧ point.1 ≤ 5 := by
  simp only [endpoint,onBar] at hpoint
  omega

theorem interior_endpoint_on_bar (source : Transverse) (point : Point)
    (hpoint : endpoint source point) (hrow : 1 ≤ point.1 ∧ point.1 ≤ 4) :
    point.2 = source.bar ∨ point.2 = source.bar+1 := by
  simp only [endpoint,onBar] at hpoint
  omega

theorem ordered_bars_have_two_column_clearance (first second : Transverse)
    (hdisjoint : disjoint first second) (horder : first.bar ≤ second.bar) :
    first.bar+2 ≤ second.bar := by
  by_cases hlarge : first.bar+2 ≤ second.bar
  · exact hlarge
  · have hfirst := bar_owns_all_rows first 0 second.bar (by omega) (by omega)
    have hsecond := bar_owns_all_rows second 0 second.bar (by omega) (Or.inl rfl)
    exact False.elim (hdisjoint (0,second.bar) hfirst hsecond)

theorem touching_bars_face_away (first second : Transverse)
    (hdisjoint : disjoint first second) (htouch : second.bar = first.bar+2) :
    first.facesRight = false ∧ second.facesRight = true := by
  have hnearFirst := first.near_min
  have hnearSecond := second.near_min
  constructor
  · cases hface : first.facesRight with
    | false => rfl
    | true =>
      have hfirst : endpoint first (5,second.bar) := by
        simp only [endpoint,onBar]
        right
        left
        exact ⟨hface,Or.inl ⟨True.intro,by omega,by omega⟩⟩
      have hsecond := bar_owns_all_rows second 5 second.bar (by omega) (Or.inl rfl)
      exact False.elim (hdisjoint (5,second.bar) hfirst hsecond)
  · cases hface : second.facesRight with
    | true => rfl
    | false =>
      have hfirst := bar_owns_all_rows first 5 (first.bar+1) (by omega) (Or.inr rfl)
      have hsecond : endpoint second (5,first.bar+1) := by
        simp only [endpoint,onBar]
        right
        right
        exact ⟨hface,Or.inl ⟨True.intro,by omega,by omega⟩⟩
      exact False.elim (hdisjoint (5,first.bar+1) hfirst hsecond)

theorem no_touching_bar_chain (first middle last : Transverse)
    (hfirst : disjoint first middle) (hlast : disjoint middle last)
    (htouchFirst : middle.bar = first.bar+2)
    (htouchLast : last.bar = middle.bar+2) : False := by
  have hmiddleRight := (touching_bars_face_away first middle hfirst htouchFirst).2
  have hmiddleLeft := (touching_bars_face_away middle last hlast htouchLast).1
  simp_all

theorem no_vertical_foreign_adjacency (first second : Transverse)
    (hdisjoint : disjoint first second) (row column : Int)
    (hfirst : endpoint first (row,column))
    (hsecond : endpoint second (row+1,column)) : False := by
  have hfirstRows := endpoints_stay_in_strip first (row,column) hfirst
  have hsecondRows := endpoints_stay_in_strip second (row+1,column) hsecond
  by_cases hfirstInterior : 1 ≤ row ∧ row ≤ 4
  · have hcolumn := interior_endpoint_on_bar first (row,column) hfirst hfirstInterior
    exact hdisjoint (row+1,column)
      (bar_owns_all_rows first (row+1) column hsecondRows hcolumn) hsecond
  · have hsecondInterior : 1 ≤ row+1 ∧ row+1 ≤ 4 := by omega
    have hcolumn := interior_endpoint_on_bar second (row+1,column) hsecond hsecondInterior
    exact hdisjoint (row,column) hfirst
      (bar_owns_all_rows second row column hfirstRows hcolumn)

theorem top_tip_is_endpoint (source : Transverse) :
    endpoint source (0,topTip source) := by
  have hfar := source.far_min
  cases hface : source.facesRight <;>
    simp [endpoint,onBar,topTip,hface] <;> omega

theorem top_support_is_not_own_endpoint (source : Transverse) :
    ¬ endpoint source (0,topSupport source) := by
  have hfar := source.far_min
  cases hface : source.facesRight <;>
    simp [endpoint,onBar,topSupport,topTip,hface] <;> omega

theorem point_below_top_tip_is_not_own_endpoint (source : Transverse) :
    ¬ endpoint source (1,topTip source) := by
  have hfar := source.far_min
  cases hface : source.facesRight <;>
    simp [endpoint,onBar,topTip,hface] <;> omega

theorem singleton_pocket_obstruction (source : Transverse) (width : Int)
    (htip : 0 ≤ topTip source ∧ topTip source < width)
    (hconsume : 0 ≤ topSupport source ∧ topSupport source < width →
      endpoint source (0,topSupport source))
    (hwallSupport : topTip source = 0 ∨ topTip source = width-1 →
      endpoint source (1,topTip source)) : False := by
  have hnotInside : ¬ (0 ≤ topSupport source ∧ topSupport source < width) := by
    intro hinside
    exact top_support_is_not_own_endpoint source (hconsume hinside)
  have hside : topTip source = 0 ∨ topTip source = width-1 := by
    cases hface : source.facesRight <;>
      simp only [topSupport,hface,Bool.false_eq_true,if_false,if_true] at hnotInside <;> omega
  exact point_below_top_tip_is_not_own_endpoint source (hwallSupport hside)

theorem exact_budget_lower_bound (aligned oddBars pairs otherEvents : Int)
    (hpairs : 2*pairs ≤ oddBars)
    (hevents : otherEvents ≤ 2*(oddBars-2*pairs)) :
    aligned+5*oddBars-6*pairs-otherEvents ≥ aligned+2*oddBars := by
  omega

theorem source_count_lower_bound (aligned oddBars pairs otherEvents : Int)
    (hodd : 0 ≤ oddBars) (hpairs : 2*pairs ≤ oddBars)
    (hevents : otherEvents ≤ 2*(oddBars-2*pairs)) :
    aligned+5*oddBars-6*pairs-otherEvents ≥ aligned+oddBars := by
  have hbound := exact_budget_lower_bound aligned oddBars pairs otherEvents hpairs hevents
  omega

theorem nonempty_complete_pocket_gain (sources pocketBudget : Int)
    (hcount : 2 ≤ sources) (hbudget : sources ≤ pocketBudget) :
    7 ≤ 5+pocketBudget := by omega

theorem opposed_depths_are_legal (width lower upper : Int)
    (hlower : 4 ≤ lower ∧ lower ≤ width-6)
    (hupper : 4 ≤ upper ∧ upper ≤ width-6) :
    4 ≤ width-2-lower ∧ 4 ≤ width-2-upper := by omega

theorem opposed_top_tips_meet (width upper : Int) :
    width-1-(width-2-upper) = upper+1 := by omega

theorem opposed_pair_exact_gain : (5 : Int)+1+1 = 7 := by omega

end SubQuorum.SixRowTransverseBudget

#print axioms SubQuorum.SixRowTransverseBudget.Point
#print axioms SubQuorum.SixRowTransverseBudget.Transverse
#print axioms SubQuorum.SixRowTransverseBudget.onBar
#print axioms SubQuorum.SixRowTransverseBudget.endpoint
#print axioms SubQuorum.SixRowTransverseBudget.disjoint
#print axioms SubQuorum.SixRowTransverseBudget.topTip
#print axioms SubQuorum.SixRowTransverseBudget.topSupport
#print axioms SubQuorum.SixRowTransverseBudget.bar_owns_all_rows
#print axioms SubQuorum.SixRowTransverseBudget.endpoints_stay_in_strip
#print axioms SubQuorum.SixRowTransverseBudget.interior_endpoint_on_bar
#print axioms SubQuorum.SixRowTransverseBudget.ordered_bars_have_two_column_clearance
#print axioms SubQuorum.SixRowTransverseBudget.touching_bars_face_away
#print axioms SubQuorum.SixRowTransverseBudget.no_touching_bar_chain
#print axioms SubQuorum.SixRowTransverseBudget.no_vertical_foreign_adjacency
#print axioms SubQuorum.SixRowTransverseBudget.top_tip_is_endpoint
#print axioms SubQuorum.SixRowTransverseBudget.top_support_is_not_own_endpoint
#print axioms SubQuorum.SixRowTransverseBudget.point_below_top_tip_is_not_own_endpoint
#print axioms SubQuorum.SixRowTransverseBudget.singleton_pocket_obstruction
#print axioms SubQuorum.SixRowTransverseBudget.exact_budget_lower_bound
#print axioms SubQuorum.SixRowTransverseBudget.source_count_lower_bound
#print axioms SubQuorum.SixRowTransverseBudget.nonempty_complete_pocket_gain
#print axioms SubQuorum.SixRowTransverseBudget.opposed_depths_are_legal
#print axioms SubQuorum.SixRowTransverseBudget.opposed_top_tips_meet
#print axioms SubQuorum.SixRowTransverseBudget.opposed_pair_exact_gain
