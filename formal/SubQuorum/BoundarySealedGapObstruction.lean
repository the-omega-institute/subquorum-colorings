import SubQuorum.BTColumnCorridorObstruction

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2400000

namespace SubQuorum.BoundarySealedGapObstruction

abbrev Point := BTColumnCorridorObstruction.Point

def selected : List Point := BTColumnCorridorObstruction.selected.filter fun v => v.2 != 9
abbrev endpoints := BTColumnCorridorObstruction.endpoints
abbrev matching := BTColumnCorridorObstruction.matching
abbrev mate := BTColumnCorridorObstruction.mate
abbrev adjacent := BTColumnCorridorObstruction.adjacent
abbrev nonmateAdjacent := BTColumnCorridorObstruction.nonmateAdjacent
abbrev verticalPartner := BTColumnCorridorObstruction.verticalPartner
abbrev rank := BTColumnCorridorObstruction.rank
abbrev record := BTColumnCorridorObstruction.record

def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a ≠ b ∧ nonmateAdjacent v a ∧ nonmateAdjacent v b ∧
    (a ∈ selected ∨ (a ∈ endpoints ∧ rank (mate a) < rank v)) ∧
    (b ∈ selected ∨ (b ∈ endpoints ∧ rank (mate b) < rank v))
instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem geometry_valid :
    selected.Nodup ∧ endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1 < 18 ∧ v.2 < 10) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    BTColumnCorridorObstruction.Frozen (fun x => x ∈ endpoints)
      (fun x => x ∈ selected) mate nonmateAdjacent v := by
  apply BTColumnCorridorObstruction.strict_rank_complete
    (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate nonmateAdjacent rank BTColumnCorridorObstruction.mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

theorem original_tip_labels_unchanged : ∀ v ∈ endpoints,
    (verticalPartner v ∈ selected ↔
      verticalPartner v ∈ BTColumnCorridorObstruction.selected) := by decide

def blank (v : Point) : Prop := v ∉ selected ∧ v ∉ endpoints
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))
def bb (v : Point) : Prop := blank v ∧ blank (verticalPartner v)
instance (v : Point) : Decidable (bb v) := inferInstanceAs (Decidable (_ ∧ _))

theorem no_tt_columns : ∀ b ∈ List.range 9, ∀ c ∈ List.range 10,
    ¬ ((2*b,c) ∈ selected ∧ (2*b+1,c) ∈ selected) := by decide

/-- TT is absent, so each BB column is one original interval unit. -/
def unmarkedUnits : List Point :=
  ((List.range 9).flatMap fun b => (List.range 10).map fun c => (2*b,c)).filter
    fun v => decide (0 < v.2 ∧ v.2 < 9 ∧ bb v)

/-- Full endpoint-free access; the source P column itself is excluded. -/
def sameGap (v target : Point) : Prop :=
  v.1/2 = target.1/2 ∧
  ∀ c ∈ List.range 10,
    ((v.2 < c ∧ c ≤ target.2) ∨ (target.2 ≤ c ∧ c < v.2)) →
      (2*(v.1/2),c) ∉ endpoints ∧ (2*(v.1/2)+1,c) ∉ endpoints
instance (v target : Point) : Decidable (sameGap v target) :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem no_units_in_terminal_bands : ∀ j ∈ unmarkedUnits, j.1 ≠ 4 ∧ j.1 ≠ 10 := by decide

theorem no_full_gap_exit_at_reachable_tip :
    ∀ v ∈ BTColumnCorridorObstruction.reachableTips,
      ∀ j ∈ unmarkedUnits, ¬ sameGap v j := by decide

theorem no_reachable_full_gap_exit {v : Point}
    (reachable : BTColumnCorridorObstruction.RelayReach v) :
    ∀ j ∈ unmarkedUnits, ¬ sameGap v j := by
  exact no_full_gap_exit_at_reachable_tip v
    (BTColumnCorridorObstruction.all_routes_stay_inside reachable)

theorem interior_support_witness :
    (6,3) ∈ BTColumnCorridorObstruction.alphaPath ∧
    (7,3) ∈ BTColumnCorridorObstruction.alphaPath ∧
    verticalPartner (6,3) = (7,3) ∧
    (6,2) ∈ unmarkedUnits ∧ sameGap (6,3) (6,2) := by decide

theorem exact_counts_and_positive_margins :
    selected.length = 15 ∧ matching.length = 10 ∧ endpoints.length = 20 ∧
    unmarkedUnits.length = 48 ∧
    (unmarkedUnits.filter fun v => decide (4 ≤ v.1 ∧ v.1 < 12)).length = 8 ∧
    8*10/2-15-20/2-8 = (7 : Nat) ∧
    18*10/2-15-20/2-18 = (47 : Nat) := by decide

/-- The physical support adapter must establish that every eligible alpha
owns one of the two boundary columns. This lemma checks the two-owner bound. -/
theorem at_most_two_support_owners {A : Type} (owner : Bool → Option A)
    (eligible : A → Prop)
    (witness : ∀ a, eligible a → ∃ s, owner s = some a)
    (a b c : A) (ha : eligible a) (hb : eligible b) (hc : eligible c) :
    a = b ∨ a = c ∨ b = c := by
  obtain ⟨sa, ea⟩ := witness a ha
  obtain ⟨sb, eb⟩ := witness b hb
  obtain ⟨sc, ec⟩ := witness c hc
  cases sa <;> cases sb <;> cases sc <;> simp_all

end SubQuorum.BoundarySealedGapObstruction

#print axioms SubQuorum.BoundarySealedGapObstruction.geometry_valid
#print axioms SubQuorum.BoundarySealedGapObstruction.certificate_valid
#print axioms SubQuorum.BoundarySealedGapObstruction.all_endpoints_frozen
#print axioms SubQuorum.BoundarySealedGapObstruction.original_tip_labels_unchanged
#print axioms SubQuorum.BoundarySealedGapObstruction.no_tt_columns
#print axioms SubQuorum.BoundarySealedGapObstruction.no_units_in_terminal_bands
#print axioms SubQuorum.BoundarySealedGapObstruction.no_full_gap_exit_at_reachable_tip
#print axioms SubQuorum.BoundarySealedGapObstruction.no_reachable_full_gap_exit
#print axioms SubQuorum.BoundarySealedGapObstruction.interior_support_witness
#print axioms SubQuorum.BoundarySealedGapObstruction.exact_counts_and_positive_margins
#print axioms SubQuorum.BoundarySealedGapObstruction.at_most_two_support_owners
