import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PersistentCorridorCapacity

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def barEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.1-2,point.2-1)

def stripEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (point.1-5,point.2-2)

def entryEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.2,point.1-3)

theorem disjoint_bars_force_two_columns_of_clearance
    (width near far stripWidth stripNear stripFar halfWidth halfStrip : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (heven : width = 2*halfWidth) (hstripeven : stripWidth = 2*halfStrip)
    (hdisjoint : ∀ point, barEndpoint width near far point →
      ¬stripEndpoint stripWidth stripNear stripFar point) :
    stripWidth ≤ width-2 := by
  by_cases hbound : stripWidth ≤ width-2
  · exact hbound
  have hbar : barEndpoint width near far (5,width+1) := by
    unfold barEndpoint uEndpoint
    dsimp
    omega
  have hstrip : stripEndpoint stripWidth stripNear stripFar (5,width+1) := by
    unfold stripEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (5,width+1) hbar hstrip)

theorem an_entry_avoiding_both_bars_has_a_strict_width_gap
    (width near far stripWidth stripNear stripFar entryWidth height entryFar
      halfWidth halfStrip halfHeight : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (hentrywidth : 6 ≤ entryWidth)
    (hheight : 4 ≤ height)
    (heven : width = 2*halfWidth) (hstripeven : stripWidth = 2*halfStrip)
    (hheighteven : height = 2*halfHeight)
    (hbaravoid : ∀ point, entryEndpoint entryWidth height entryFar point →
      ¬barEndpoint width near far point)
    (hstripavoid : ∀ point, entryEndpoint entryWidth height entryFar point →
      ¬stripEndpoint stripWidth stripNear stripFar point) :
    stripWidth+2 ≤ height ∧ height ≤ width-4 := by
  have hupper : height ≤ width-4 := by
    by_cases hbound : height ≤ width-4
    · exact hbound
    have hentry : entryEndpoint entryWidth height entryFar (4,width+1) := by
      unfold entryEndpoint uEndpoint
      dsimp
      omega
    have hbar : barEndpoint width near far (4,width+1) := by
      unfold barEndpoint uEndpoint
      dsimp
      omega
    exact False.elim (hbaravoid (4,width+1) hentry hbar)
  have hlower : stripWidth+2 ≤ height := by
    by_cases hbound : stripWidth+2 ≤ height
    · exact hbound
    have hentry : entryEndpoint entryWidth height entryFar (5,height+2) := by
      unfold entryEndpoint uEndpoint
      dsimp
      omega
    have hstrip : stripEndpoint stripWidth stripNear stripFar (5,height+2) := by
      unfold stripEndpoint uEndpoint
      dsimp
      omega
    exact False.elim (hstripavoid (5,height+2) hentry hstrip)
  exact ⟨hlower,hupper⟩

theorem an_admissible_entry_fills_every_corridor_column
    (entryWidth height entryFar stripWidth column : Int)
    (hheight : stripWidth+2 ≤ height)
    (hfirst : 3 ≤ column) (hlast : column ≤ stripWidth+2) :
    entryEndpoint entryWidth height entryFar (4,column) := by
  unfold entryEndpoint uEndpoint
  dsimp
  omega

theorem positive_index_filling_propagates_to_the_left_end
    (endpoint : Nat → Prop)
    (hprevious : ∀ index, endpoint (index+1) → endpoint index)
    (index : Nat) (hendpoint : endpoint index) : endpoint 0 := by
  induction index with
  | zero => exact hendpoint
  | succ index inductionHypothesis =>
    exact inductionHypothesis (hprevious index hendpoint)

theorem a_protected_width_corridor_has_no_endpoints
    (endpoint : Nat → Prop) (width stripWidth : Int)
    (hprotected : width-4 ≤ stripWidth)
    (hprevious : ∀ index, endpoint (index+1) → endpoint index)
    (hentry : endpoint 0 → ∃ height : Int,
      stripWidth+2 ≤ height ∧ height ≤ width-4) :
    ∀ index, ¬endpoint index := by
  intro index hendpoint
  have hleft := positive_index_filling_propagates_to_the_left_end
    endpoint hprevious index hendpoint
  obtain ⟨height,hlower,hupper⟩ := hentry hleft
  omega

theorem a_tile_with_two_fixed_endpoint_neighbors_cannot_be_selected
    (selected : Prop) (degree : Int)
    (hfeasible : selected → degree ≤ 1) (htwo : 2 ≤ degree) : ¬selected := by
  intro hselected
  have hbound := hfeasible hselected
  omega

theorem one_strip_per_owner_covers_both_corner_claims
    (widths : List Nat) (hwidths : ∀ width ∈ widths, 6 ≤ width) :
    2*widths.length ≤ (widths.map (fun width => width/2-1)).sum := by
  induction widths with
  | nil => simp
  | cons width widths inductionHypothesis =>
    have hwidth : 6 ≤ width := hwidths width (by simp)
    have hrest : ∀ entry ∈ widths, 6 ≤ entry := by
      intro entry hentry
      exact hwidths entry (by simp [hentry])
    have hsum := inductionHypothesis hrest
    simp only [List.length_cons, List.map_cons, List.sum_cons]
    omega

def possibleDeltas : List Int → List Int
  | [] => [0]
  | change :: changes => possibleDeltas changes ++
      (possibleDeltas changes).map (fun total => change+total)

def leastDelta : List Int → Int
  | [] => 0
  | change :: changes => min 0 change+leastDelta changes

theorem one_component_subunion_attains_the_total_loss (changes : List Int) :
    leastDelta changes ∈ possibleDeltas changes := by
  induction changes with
  | nil => simp [possibleDeltas, leastDelta]
  | cons change changes inductionHypothesis =>
    by_cases hnegative : change < 0
    · have hminimum : min 0 change = change := by omega
      simp only [possibleDeltas, leastDelta, hminimum, List.mem_append]
      exact Or.inr (List.mem_map.mpr ⟨leastDelta changes,inductionHypothesis,rfl⟩)
    · have hminimum : min 0 change = 0 := by omega
      simp only [possibleDeltas, leastDelta, hminimum, Int.zero_add, List.mem_append]
      exact Or.inl inductionHypothesis

theorem persistent_disjoint_receipts_bound_simultaneous_loss
    (changes : List Int) (reserve activation prior caps upper lower : Int)
    (hfloor : ∀ total, total ∈ possibleDeltas changes →
      activation+prior+caps+2*upper+2*lower ≤ 2*(reserve+total)) :
    -leastDelta changes ≤ reserve-upper-lower-(activation+prior+caps+1)/2 := by
  have hleast := hfloor (leastDelta changes)
    (one_component_subunion_attains_the_total_loss changes)
  omega

theorem the_persistent_floor_pays_demand_in_the_same_minimizing_family
    (changes : List Int) (reserve activation prior caps upper lower marked positive : Int)
    (hfloor : ∀ total, total ∈ possibleDeltas changes →
      activation+prior+caps+2*upper+2*lower ≤ 2*(reserve+total))
    (hdemand : marked-positive ≤ upper+lower+(activation+prior+caps+1)/2) :
    -leastDelta changes ≤ positive+reserve-marked := by
  have hloss := persistent_disjoint_receipts_bound_simultaneous_loss
    changes reserve activation prior caps upper lower hfloor
  omega

theorem certified_negative_gates_reduce_the_uncovered_demand
    (positive marked transferred certified uncovered activation prior upper lower reserve : Int)
    (hmarks : marked ≤ 2*positive)
    (hpartition : marked = transferred+certified+uncovered)
    (hinjection : transferred ≤ activation)
    (hfloor : activation+prior+certified+2*upper+2*lower ≤ 2*reserve) :
    positive+reserve-marked ≥ upper+lower+(prior-uncovered+1)/2 := by
  omega

theorem the_explicit_residual_threshold_implies_allocation
    (positive marked transferred certified uncovered activation prior upper lower reserve : Int)
    (hmarks : marked ≤ 2*positive)
    (hpartition : marked = transferred+certified+uncovered)
    (hinjection : transferred ≤ activation)
    (hfloor : activation+prior+certified+2*upper+2*lower ≤ 2*reserve)
    (hcoverage : uncovered ≤ 2*(upper+lower)+prior+1) :
    0 ≤ positive+reserve-marked := by
  omega

end SubQuorum.PersistentCorridorCapacity
