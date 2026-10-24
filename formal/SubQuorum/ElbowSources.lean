import SubQuorum.MixedCavitySources

set_option autoImplicit false

namespace SubQuorum.ElbowSources

open OwnedDonorCompensation LongBentTerminalStrips FrozenPromotion

theorem retained_mate_zigzag {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (selected : Vertex → Prop)
    (mate : Vertex → Vertex) (first second : Nat → Vertex) (length : Nat)
    (hinvolution : ∀ vertex, mate (mate vertex) = vertex)
    (hfirst : Frozen adjacent selected mate (first 0))
    (hsecond : Frozen adjacent selected mate (second 0))
    (hfirstAdjacent : ∀ index, index < length →
      adjacent (first (index+1)) (mate (first index)) ∧
      adjacent (first (index+1)) (mate (second index)))
    (hfirstDistinct : ∀ index, index < length → mate (first index) ≠ mate (second index))
    (hsecondAdjacent : ∀ index, index < length →
      adjacent (second (index+1)) (mate (first (index+1))) ∧
      adjacent (second (index+1)) (mate (second index)))
    (hsecondDistinct : ∀ index, index < length →
      mate (first (index+1)) ≠ mate (second index)) :
    ∀ index, index ≤ length →
      Frozen adjacent selected mate (first index) ∧
      Frozen adjacent selected mate (second index) := by
  intro index
  induction index with
  | zero => exact fun _ => ⟨hfirst, hsecond⟩
  | succ index inductionHypothesis =>
      intro hbound
      have hstep : index < length := by omega
      obtain ⟨hpreviousFirst, hpreviousSecond⟩ := inductionHypothesis (by omega)
      have hnextFirst : Frozen adjacent selected mate (first (index+1)) := by
        apply Frozen.two_frozen _ (mate (first index)) (mate (second index))
        · exact (hfirstAdjacent index hstep).1
        · exact (hfirstAdjacent index hstep).2
        · exact hfirstDistinct index hstep
        · simpa only [hinvolution] using hpreviousFirst
        · simpa only [hinvolution] using hpreviousSecond
      constructor
      · exact hnextFirst
      · apply Frozen.two_frozen _ (mate (first (index+1))) (mate (second index))
        · exact (hsecondAdjacent index hstep).1
        · exact (hsecondAdjacent index hstep).2
        · exact hsecondDistinct index hstep
        · simpa only [hinvolution] using hnextFirst
        · simpa only [hinvolution] using hpreviousSecond

theorem three_endpoint_junction_blank (state : Int → Int → Label)
    (hupper : state 0 0 = .endpoint) (hright : state 1 1 = .endpoint)
    (hnotEndpoint : state 1 0 ≠ .endpoint) (hfeasible : feasibleAt state 1 0) :
    state 1 0 = .blank := by
  cases hcorner : state 1 0 <;>
    simp_all [feasibleAt, degree, occupied] <;> omega

theorem transition_band_gain
    (physicalRaw topRaw junctionRaw middleRaw bottomRaw optional gainTwice : Int)
    (hphysical : physicalRaw = 0) (htop : topRaw = 2*optional-2)
    (hjunction : junctionRaw = -1) (hmiddle : middleRaw = 0)
    (hbottom : bottomRaw = -1) (hoptional : 0 ≤ optional ∧ optional ≤ 1)
    (hgain : gainTwice = physicalRaw-(topRaw+junctionRaw+middleRaw+bottomRaw)) :
    gainTwice = 4-2*optional ∧ 2 ≤ gainTwice := by
  omega

theorem extra_source_residual_compensation
    (deficit flux extraSources sourcePhase shifted single remainder weightedPayment
      channelLowerBound : Int)
    (hledger : 2*deficit = flux+sourcePhase+shifted+single+2*remainder-2*extraSources)
    (hphase : 0 ≤ sourcePhase) (hshifted : 0 ≤ shifted)
    (hcapacity : weightedPayment ≤ single+2*remainder)
    (hchannels : channelLowerBound ≤ weightedPayment) :
    flux-2*extraSources+channelLowerBound ≤ 2*deficit ∧
      (-1 ≤ flux-2*extraSources+channelLowerBound → 0 ≤ deficit) := by
  omega

end SubQuorum.ElbowSources
