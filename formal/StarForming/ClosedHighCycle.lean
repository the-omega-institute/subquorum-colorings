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

theorem architecture_gap_bound (cores blocks order beta star gap : Nat)
    (horder : order = 20 * cores + 14 * blocks)
    (hports : 2 * blocks ≤ 6 * cores)
    (hbeta : 12 * cores + 7 * blocks ≤ beta)
    (hgap : star = beta + gap)
    (hcompensation : 7 * star ≤ 3 * order + 2 * beta) :
    gap ≤ blocks ∧ 62 * gap ≤ 3 * order := by
  omega

theorem two_witness_density (cores blocks order beta : Nat)
    (horder : order = 20 * cores + 14 * blocks)
    (hfirst : 12 * cores + 7 * blocks ≤ beta)
    (hsecond : 9 * cores + 8 * blocks ≤ beta) :
    33 * order ≤ 62 * beta := by
  omega

theorem shared_port_gap_bound (cores blocks order beta star gap : Nat)
    (horder : order = 20 * cores + 14 * blocks)
    (hfirst : 12 * cores + 7 * blocks ≤ beta)
    (hsecond : 9 * cores + 8 * blocks ≤ beta)
    (hgap : star = beta + gap)
    (hcompensation : 7 * star ≤ 3 * order + 2 * beta) :
    gap ≤ blocks ∧ 7 * gap ≤ 15 * cores + 2 * blocks ∧
      62 * gap ≤ 3 * order := by
  have hdensity := two_witness_density cores blocks order beta horder hfirst hsecond
  omega

theorem architecture_equality_balance (cores blocks order beta star gap : Nat)
    (horder : order = 20 * cores + 14 * blocks)
    (hfirst : 12 * cores + 7 * blocks ≤ beta)
    (hsecond : 9 * cores + 8 * blocks ≤ beta)
    (hgap : star = beta + gap)
    (hcompensation : 7 * star ≤ 3 * order + 2 * beta)
    (hequality : 62 * gap = 3 * order) :
    blocks = 3 * cores ∧ beta = 33 * cores ∧ star = 36 * cores ∧
      order = 62 * cores := by
  have hbounds := shared_port_gap_bound cores blocks order beta star gap
    horder hfirst hsecond hgap hcompensation
  omega

theorem architecture_imbalance_deficit (cores blocks order beta star gap : Nat)
    (horder : order = 20 * cores + 14 * blocks)
    (hfirst : 12 * cores + 7 * blocks ≤ beta)
    (hsecond : 9 * cores + 8 * blocks ≤ beta)
    (hgap : star = beta + gap)
    (hcompensation : 7 * star ≤ 3 * order + 2 * beta) :
    (blocks ≤ 3 * cores → 62 * gap + 20 * (3 * cores - blocks) ≤ 3 * order) ∧
    (3 * cores ≤ blocks → 170 * (blocks - 3 * cores) ≤
      7 * (3 * order - 62 * gap)) := by
  have hbounds := shared_port_gap_bound cores blocks order beta star gap
    horder hfirst hsecond hgap hcompensation
  omega

end StarForming.ClosedHighCycle
