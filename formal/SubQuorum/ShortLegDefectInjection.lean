import Std

set_option autoImplicit false

namespace SubQuorum.ShortLegDefectInjection

abbrev Point := Int × Int

structure Donor where
  chosen : Point
  anchor : Point
  gate : Point
  protector : Point
  deriving DecidableEq

def localDonors : List Donor := [
  ⟨(0,0), (-1,0), (0,1), (1,2)⟩,
  ⟨(0,0), (0,-1), (1,0), (2,1)⟩,
  ⟨(0,1), (-1,1), (0,0), (1,-1)⟩,
  ⟨(0,1), (0,2), (1,1), (2,0)⟩,
  ⟨(1,0), (2,0), (1,1), (0,2)⟩,
  ⟨(1,0), (1,-1), (0,0), (-1,1)⟩,
  ⟨(1,1), (2,1), (1,0), (0,-1)⟩,
  ⟨(1,1), (1,2), (0,1), (-1,0)⟩]

def negativeMask : List Point := [(-1,0), (-1,1), (0,0), (0,1), (0,2)]

theorem donor_orientation_exclusion :
    ∀ donor ∈ localDonors,
      donor.chosen = (1,0) ∨ donor.anchor ∈ negativeMask ∨
      donor.anchor = (0,-1) ∨ donor.gate ∈ negativeMask ∨
      donor.protector = (0,-1) := by decide

theorem no_blank_donor (donor : Donor) (hrole : donor ∈ localDonors)
    (hselected : donor.chosen ≠ (1,0))
    (hnegativeAnchor : donor.anchor ∉ negativeMask)
    (hpositiveAnchor : donor.anchor ≠ (0,-1))
    (hblank : donor.gate ∉ negativeMask)
    (hpositiveProtector : donor.protector ≠ (0,-1)) : False := by
  have hexclusion := donor_orientation_exclusion donor hrole
  rcases hexclusion with hchosen | hanchor | hpositive | hgate | hprotector
  · exact hselected hchosen
  · exact hnegativeAnchor hanchor
  · exact hpositiveAnchor hpositive
  · exact hblank hgate
  · exact hpositiveProtector hprotector

theorem short_longitudinal_dimensions (height incoming : Int)
    (hheight : height = 4 ∨ height = 6) (hincoming : 4 ≤ incoming)
    (hclearance : incoming ≤ height-2) : height = 6 ∧ incoming = 4 := by omega

theorem injected_witness_count {Resource : Type} (witnesses pool : List Resource)
    (hnodup : witnesses.Nodup) (hsubset : witnesses ⊆ pool) :
    witnesses.length ≤ pool.length :=
  hnodup.length_le_of_subset hsubset

theorem source_bound_from_injection {Resource : Type}
    (witnesses activations tiles : List Resource) (doubleCount : Nat)
    (hlength : witnesses.length = doubleCount) (hnodup : witnesses.Nodup)
    (hsubset : witnesses ⊆ activations ++ tiles) :
    doubleCount ≤ activations.length+tiles.length := by
  have hcount := injected_witness_count witnesses (activations ++ tiles) hnodup hsubset
  simp only [List.length_append] at hcount
  omega

theorem saturated_pool_covered {Resource : Type} (witnesses pool : List Resource)
    (hnodup : witnesses.Nodup) (hsubset : witnesses ⊆ pool)
    (hlength : witnesses.length = pool.length) : pool ⊆ witnesses := by
  intro resource hmember
  by_cases hused : resource ∈ witnesses
  · exact hused
  · have haugmented : (resource :: witnesses).Nodup := List.nodup_cons.mpr ⟨hused, hnodup⟩
    have haugmentedSubset : resource :: witnesses ⊆ pool := by
      intro current hcurrent
      rcases List.mem_cons.mp hcurrent with hequal | hremaining
      · simpa [hequal] using hmember
      · exact hsubset hremaining
    have hcount := haugmented.length_le_of_subset haugmentedSubset
    simp only [List.length_cons] at hcount
    omega

theorem discarded_defect_bound (doubleCount activation unused rotor lone bar mutualPairs mixed
    defect : Nat)
    (hinjection : doubleCount ≤ activation+bar+mixed)
    (hidentity : defect = activation+unused+rotor+lone+2*bar+2*mutualPairs+mixed) :
    doubleCount+unused+rotor+lone+bar+2*mutualPairs ≤ defect := by omega

theorem exceptional_source_bound (doubleCount nonexceptional exceptional activation unused rotor
    lone bar mutualPairs mixed defect : Nat)
    (hlabels : doubleCount ≤ nonexceptional+exceptional)
    (hinjection : nonexceptional ≤ activation+bar+mixed)
    (hidentity : defect = activation+unused+rotor+lone+2*bar+2*mutualPairs+mixed) :
    doubleCount+unused+rotor+lone+bar+2*mutualPairs ≤ defect+exceptional := by omega

theorem low_reserve_failure_exact (unmarked doubleCount reserve unused rotor lone bar mutualPairs : Nat)
    (hfailure : unmarked+reserve < doubleCount)
    (hbound : doubleCount+unused+rotor+lone+bar+2*mutualPairs ≤ 2*reserve)
    (hreserve : reserve = 1) :
    unmarked = 0 ∧ doubleCount = 2 ∧ unused = 0 ∧ rotor = 0 ∧ lone = 0 ∧
      bar = 0 ∧ mutualPairs = 0 := by omega

theorem D2_excludes_discarded_types (activation unused rotor lone bar mutualPairs mixed : Nat)
    (hinjection : 2 ≤ activation+bar+mixed)
    (hidentity : activation+unused+rotor+lone+2*bar+2*mutualPairs+mixed = 2) :
    unused = 0 ∧ rotor = 0 ∧ lone = 0 ∧ bar = 0 ∧ mutualPairs = 0 ∧ activation+mixed = 2 := by omega

theorem three_remaining_patterns (activation mixed : Nat)
    (hsum : activation+mixed = 2) :
    (activation = 2 ∧ mixed = 0) ∨
    (activation = 1 ∧ mixed = 1) ∨
    (activation = 0 ∧ mixed = 2) := by omega

end SubQuorum.ShortLegDefectInjection
