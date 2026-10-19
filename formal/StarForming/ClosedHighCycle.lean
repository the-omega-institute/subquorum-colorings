import StarForming.LongCoreUpper

namespace StarForming.ClosedHighCycle

open StarForming.LongCoreUpper

theorem zero_hub_score (first middle last : Cell)
    (hfirst : Valid first 0 0) (hmiddle : Valid middle 0 0)
    (hlast : Valid last 0 0) :
    3 + first.weight + middle.weight + last.weight ≤ 12 := by
  have hcapFirst := cell_cap first 0 0 hfirst
  have hcapMiddle := cell_cap middle 0 0 hmiddle
  have hcapLast := cell_cap last 0 0 hlast
  omega

theorem closed_two_hub_score (first middle last : Cell)
    (hfirst : Valid first 1 1) (hmiddle : Valid middle 1 1)
    (hlast : Valid last 1 1) (hfirstAcross : Across first middle)
    (hlastAcross : Across middle last)
    (hclosedHigh : last.highRight + first.highLeft + first.highRight ≤ 2) :
    3 + first.weight + middle.weight + last.weight + 2 ≤ 12 := by
  obtain ⟨hupper, hequality⟩ :=
    two_hub_block first middle last hfirst hmiddle hlast hfirstAcross hlastAcross
  by_cases hequal : 3 + first.weight + middle.weight + last.weight + 2 = 13
  · obtain ⟨htightFirst, _, htightLast⟩ := hequality hequal
    have hshapeFirst := two_hub_tight first hfirst htightFirst
    have hshapeLast := two_hub_tight last hlast htightLast
    omega
  · omega

theorem module_cap (coreSize omitted dense blockSize : Nat)
    (hcore : coreSize + omitted ≤ 12)
    (hdense : dense ≤ omitted) (hblocks : blockSize ≤ 21 + dense) :
    coreSize + blockSize ≤ 33 := by
  omega

theorem sum_module_caps (sizes : List Nat)
    (hsize : ∀ size, size ∈ sizes → size ≤ 33) :
    sizes.sum ≤ 33 * sizes.length := by
  induction sizes with
  | nil => simp
  | cons size rest inductionHypothesis =>
    have hhead := hsize size (by simp)
    have htail : ∀ other, other ∈ rest → other ≤ 33 := by
      intro other hmember
      exact hsize other (by simp [hmember])
    have hbound := inductionHypothesis htail
    simp only [List.sum_cons, List.length_cons]
    omega

theorem exact_parameters (copies beta star : Nat)
    (hbetaUpper : beta ≤ 33 * copies) (hbetaLower : 33 * copies ≤ beta)
    (hstarLower : 36 * copies ≤ star)
    (hcompensation : 7 * star ≤ 186 * copies + 2 * beta) :
    beta = 33 * copies ∧ star = 36 * copies ∧ star - beta = 3 * copies := by
  omega

end StarForming.ClosedHighCycle
