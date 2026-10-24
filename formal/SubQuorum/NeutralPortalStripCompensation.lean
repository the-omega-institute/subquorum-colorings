import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NeutralPortalStripCompensation

def bit (mask : Fin 16) (position : Fin 4) : Bool :=
  decide (mask.val / 2 ^ position.val % 2 = 1)

def selectedCount (mask : Fin 16) : Nat :=
  ([0, 1, 2, 3] : List (Fin 4)).countP (bit mask)

def westBlank (mask : Fin 16) : Prop := bit mask 0 = false ∧ bit mask 2 = false

instance (mask : Fin 16) : Decidable (westBlank mask) :=
  inferInstanceAs (Decidable (bit mask 0 = false ∧ bit mask 2 = false))

def onSide (side corner : Fin 4) : Bool :=
  if side = 0 then corner == 0 || corner == 2
  else if side = 1 then corner == 1 || corner == 3
  else if side = 2 then corner == 0 || corner == 1
  else corner == 2 || corner == 3

def blankArrivalSides (selection claims : Fin 16) : Prop :=
  ∀ side corner : Fin 4, bit claims side = true →
    onSide side corner = true → bit selection corner = false

instance (selection claims : Fin 16) : Decidable (blankArrivalSides selection claims) :=
  inferInstanceAs (Decidable (∀ side corner : Fin 4, bit claims side = true →
    onSide side corner = true → bit selection corner = false))

theorem saturated_entry_forces_exit (mask : Fin 16)
    (hentry : westBlank mask) (hsaturated : selectedCount mask = 2) : mask = 10 := by
  have checked : ∀ mask : Fin 16,
      westBlank mask → selectedCount mask = 2 → mask = 10 := by decide
  exact checked mask hentry hsaturated

theorem positive_stop_forces_unit (mask : Fin 16)
    (hdeficient : selectedCount mask < 2) : 1 ≤ 2 - selectedCount mask := by omega

theorem mixed_stop_capacity (selection claims : Fin 16)
    (hcapacity : selectedCount selection ≤ 2)
    (hstop : 0 < selectedCount claims → selectedCount selection < 2)
    (hsides : blankArrivalSides selection claims) :
    selectedCount claims ≤ 2 * (2 - selectedCount selection) := by
  have checked : ∀ selection claims : Fin 16,
      selectedCount selection ≤ 2 →
      (0 < selectedCount claims → selectedCount selection < 2) →
      blankArrivalSides selection claims →
      selectedCount claims ≤ 2 * (2 - selectedCount selection) := by decide
  exact checked selection claims hcapacity hstop hsides

theorem parallel_stop_capacity (selection claims : Fin 16)
    (hcapacity : selectedCount selection ≤ 2)
    (hstop : 0 < selectedCount claims → selectedCount selection < 2)
    (hsides : blankArrivalSides selection claims)
    (hparallel : bit claims 2 = false ∧ bit claims 3 = false) :
    selectedCount claims ≤ 2 - selectedCount selection := by
  have checked : ∀ selection claims : Fin 16,
      selectedCount selection ≤ 2 →
      (0 < selectedCount claims → selectedCount selection < 2) →
      blankArrivalSides selection claims →
      (bit claims 2 = false ∧ bit claims 3 = false) →
      selectedCount claims ≤ 2 - selectedCount selection := by decide
  exact checked selection claims hcapacity hstop hsides hparallel

theorem arbitrary_length_corridor_has_deficit
    (length : Nat) (hpositive : 0 < length) (mask : Nat → Fin 16)
    (hcapacity : ∀ index, index < length → selectedCount (mask index) ≤ 2)
    (hentry : westBlank (mask 0))
    (hnext : ∀ index, index + 1 < length →
      mask index = 10 → westBlank (mask (index + 1)))
    (hexit : mask (length - 1) ≠ 10) :
    ∃ index, index < length ∧ selectedCount (mask index) < 2 := by
  classical
  apply Classical.byContradiction
  intro hnone
  have hsaturated : ∀ index, index < length → selectedCount (mask index) = 2 := by
    intro index hindex
    have hnot : ¬ selectedCount (mask index) < 2 := by
      intro hsmall
      exact hnone ⟨index, hindex, hsmall⟩
    have hbound := hcapacity index hindex
    omega
  have allMasks : ∀ index, index < length → mask index = 10 := by
    intro index
    induction index with
    | zero =>
      intro hindex
      exact saturated_entry_forces_exit (mask 0) hentry (hsaturated 0 hindex)
    | succ index ih =>
      intro hindex
      have hprevious : index < length := by omega
      have hblank := hnext index hindex (ih hprevious)
      exact saturated_entry_forces_exit (mask (index + 1)) hblank
        (hsaturated (index + 1) hindex)
  exact hexit (allMasks (length - 1) (by omega))

theorem shifted_square_capacity
    (length selections interiorSelections finalSelections : Int)
    (hcount : selections = interiorSelections + finalSelections)
    (hinterior : interiorSelections ≤ 2 * (length - 1))
    (hcorner : finalSelections ≤ 1) : 1 ≤ 2 * length - selections := by omega

theorem sealed_square_capacity
    (length selections interiorSelections : Int)
    (hcount : selections = interiorSelections)
    (hinterior : interiorSelections ≤ 2 * (length - 1)) :
    2 ≤ 2 * length - selections := by omega

theorem mixed_coefficient_nineteen_twentieths
    (halfArea selected matching deficit sources negativeSurplus : Int)
    (hledger : halfArea - selected - matching = deficit - sources + negativeSurplus)
    (hphysical : sources ≤ 2 * deficit) (hsize : 10 * sources ≤ matching) :
    20 * selected + 19 * matching ≤ 20 * halfArea - 20 * negativeSurplus := by omega

theorem parallel_coefficient_one
    (halfArea selected matching deficit sources negativeSurplus : Int)
    (hledger : halfArea - selected - matching = deficit - sources + negativeSurplus)
    (hphysical : sources ≤ deficit) (hnegative : 0 ≤ negativeSurplus) :
    selected + matching ≤ halfArea := by omega

theorem collision_surplus_payment
    (halfArea selected matching deficit sources negativeSurplus shortage : Int)
    (hledger : halfArea - selected - matching = deficit - sources + negativeSurplus)
    (hpaid : sources - shortage ≤ deficit) (hcompensation : shortage ≤ negativeSurplus) :
    selected + matching ≤ halfArea := by omega

theorem transverse_local_sharpness :
    selectedCount (8 : Fin 16) = 1 ∧ selectedCount (5 : Fin 16) = 2 ∧
    blankArrivalSides 8 5 ∧ ¬ selectedCount (5 : Fin 16) ≤ 2 - selectedCount (8 : Fin 16) := by
  decide

end SubQuorum.NeutralPortalStripCompensation

#print axioms SubQuorum.NeutralPortalStripCompensation.saturated_entry_forces_exit
#print axioms SubQuorum.NeutralPortalStripCompensation.positive_stop_forces_unit
#print axioms SubQuorum.NeutralPortalStripCompensation.mixed_stop_capacity
#print axioms SubQuorum.NeutralPortalStripCompensation.parallel_stop_capacity
#print axioms SubQuorum.NeutralPortalStripCompensation.arbitrary_length_corridor_has_deficit
#print axioms SubQuorum.NeutralPortalStripCompensation.shifted_square_capacity
#print axioms SubQuorum.NeutralPortalStripCompensation.sealed_square_capacity
#print axioms SubQuorum.NeutralPortalStripCompensation.mixed_coefficient_nineteen_twentieths
#print axioms SubQuorum.NeutralPortalStripCompensation.parallel_coefficient_one
#print axioms SubQuorum.NeutralPortalStripCompensation.collision_surplus_payment
#print axioms SubQuorum.NeutralPortalStripCompensation.transverse_local_sharpness
