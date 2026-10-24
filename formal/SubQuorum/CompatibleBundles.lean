import Std

set_option autoImplicit false

namespace SubQuorum.CompatibleBundles

theorem compatible_union_feasible {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop)
    (selected occupied firstPromoted secondPromoted firstRemoved secondRemoved : Vertex → Prop)
    (hfirst : ∀ vertex first second, (selected vertex ∨ firstPromoted vertex) →
      adjacent vertex first → adjacent vertex second →
      (occupied first ∧ ¬firstRemoved first) →
      (occupied second ∧ ¬firstRemoved second) → first = second)
    (hsecond : ∀ vertex first second, (selected vertex ∨ secondPromoted vertex) →
      adjacent vertex first → adjacent vertex second →
      (occupied first ∧ ¬secondRemoved first) →
      (occupied second ∧ ¬secondRemoved second) → first = second) :
    ∀ vertex first second,
      (selected vertex ∨ firstPromoted vertex ∨ secondPromoted vertex) →
      adjacent vertex first → adjacent vertex second →
      (occupied first ∧ ¬firstRemoved first ∧ ¬secondRemoved first) →
      (occupied second ∧ ¬firstRemoved second ∧ ¬secondRemoved second) →
      first = second := by
  intro vertex first second hpromoted hfirstAdjacent hsecondAdjacent hfirstKept hsecondKept
  rcases hpromoted with hselected | hfirstPromoted | hsecondPromoted
  · exact hfirst vertex first second (Or.inl hselected) hfirstAdjacent hsecondAdjacent
      ⟨hfirstKept.1, hfirstKept.2.1⟩ ⟨hsecondKept.1, hsecondKept.2.1⟩
  · exact hfirst vertex first second (Or.inr hfirstPromoted) hfirstAdjacent hsecondAdjacent
      ⟨hfirstKept.1, hfirstKept.2.1⟩ ⟨hsecondKept.1, hsecondKept.2.1⟩
  · exact hsecond vertex first second (Or.inr hsecondPromoted) hfirstAdjacent hsecondAdjacent
      ⟨hfirstKept.1, hfirstKept.2.2⟩ ⟨hsecondKept.1, hsecondKept.2.2⟩

theorem compatible_union_keeps_promoted {Vertex : Type}
    (firstPromoted secondPromoted firstRemoved secondRemoved : Vertex → Prop)
    (hfirstOwn : ∀ vertex, firstPromoted vertex → ¬firstRemoved vertex)
    (hsecondOwn : ∀ vertex, secondPromoted vertex → ¬secondRemoved vertex)
    (hfirstCross : ∀ vertex, firstPromoted vertex → ¬secondRemoved vertex)
    (hsecondCross : ∀ vertex, secondPromoted vertex → ¬firstRemoved vertex) :
    ∀ vertex, (firstPromoted vertex ∨ secondPromoted vertex) →
      ¬firstRemoved vertex ∧ ¬secondRemoved vertex := by
  intro vertex hpromoted
  rcases hpromoted with hfirst | hsecond
  · exact ⟨hfirstOwn vertex hfirst, hfirstCross vertex hfirst⟩
  · exact ⟨hsecondCross vertex hsecond, hsecondOwn vertex hsecond⟩

theorem occupied_contact_owner_unique {Vertex Owner : Type}
    (adjacent : Vertex → Vertex → Prop)
    (selected endpoint : Vertex → Prop) (belongs : Owner → Vertex → Prop)
    (hunique : ∀ first second vertex, belongs first vertex → belongs second vertex →
      first = second)
    (hclosed : ∀ owner first second, belongs owner first → endpoint second →
      adjacent second first → belongs owner second)
    (hselected : ∀ vertex first second, selected vertex → endpoint first → endpoint second →
      adjacent vertex first → adjacent vertex second → first = second)
    (firstOwner secondOwner : Owner) (contact firstEndpoint secondEndpoint : Vertex)
    (hoccupied : selected contact ∨ endpoint contact)
    (hfirstEndpoint : endpoint firstEndpoint) (hsecondEndpoint : endpoint secondEndpoint)
    (hfirstOwner : belongs firstOwner firstEndpoint)
    (hsecondOwner : belongs secondOwner secondEndpoint)
    (hfirstAdjacent : adjacent contact firstEndpoint)
    (hsecondAdjacent : adjacent contact secondEndpoint) : firstOwner = secondOwner := by
  rcases hoccupied with hselectedContact | hendpointContact
  · have hsame := hselected contact firstEndpoint secondEndpoint hselectedContact
      hfirstEndpoint hsecondEndpoint hfirstAdjacent hsecondAdjacent
    subst secondEndpoint
    exact hunique firstOwner secondOwner firstEndpoint hfirstOwner hsecondOwner
  · exact hunique firstOwner secondOwner contact
      (hclosed firstOwner firstEndpoint contact hfirstOwner hendpointContact hfirstAdjacent)
      (hclosed secondOwner secondEndpoint contact hsecondOwner hendpointContact hsecondAdjacent)

theorem upper_lower_equivalence (length : Nat) (upper lower : Nat → Prop)
    (hupper : ∀ index, index < length → upper index →
      lower index ∨ (index+1 < length ∧ upper (index+1)))
    (hlower : ∀ index, index < length → lower index → upper index)
    (hprevious : ∀ index, index+1 < length → lower (index+1) → lower index) :
    ∀ index, index < length → (upper index ↔ lower index) := by
  induction length with
  | zero =>
      intro index hbound
      omega
  | succ length inductionHypothesis =>
      have hlast : upper length → lower length := by
        intro hselected
        rcases hupper length (by omega) hselected with hselectedLower | hnext
        · exact hselectedLower
        · omega
      have hshort : ∀ index, index < length → upper index →
          lower index ∨ (index+1 < length ∧ upper (index+1)) := by
        intro index hbound hselected
        rcases hupper index (by omega) hselected with hselectedLower | hnext
        · exact Or.inl hselectedLower
        · by_cases hnextBound : index+1 < length
          · exact Or.inr ⟨hnextBound, hnext.2⟩
          · have hsame : index+1 = length := by omega
            have hlastUpper : upper length := by simpa [hsame] using hnext.2
            apply Or.inl
            apply hprevious index (by omega)
            simpa [hsame] using hlast hlastUpper
      intro index hbound
      constructor
      · intro hselected
        by_cases hshortBound : index < length
        · exact (inductionHypothesis hshort
            (fun position hposition => hlower position (by omega))
            (fun position hposition => hprevious position (by omega))
            index hshortBound).mp hselected
        · have hsame : index = length := by omega
          subst index
          exact hlast hselected
      · exact hlower index hbound

theorem lower_prefix (length : Nat) (lower : Nat → Prop)
    (hprevious : ∀ index, index+1 < length → lower (index+1) → lower index) :
    ∀ index, index < length → ∀ earlier, earlier ≤ index → lower index → lower earlier := by
  intro index
  induction index with
  | zero =>
      intro hbound earlier hearly hselected
      have hsame : earlier = 0 := by omega
      simpa [hsame] using hselected
  | succ index inductionHypothesis =>
      intro hbound earlier hearly hselected
      by_cases hsame : earlier = index+1
      · simpa [hsame] using hselected
      · exact inductionHypothesis (by omega) earlier (by omega)
          (hprevious index hbound hselected)

theorem blank_block_exists (length : Nat) (left right : Nat → Nat)
    (hpositive : 0 < length) (hfirst : left 0 = 0)
    (hlast : right (length-1) = 0)
    (hlink : ∀ index, index+1 < length → right index+left (index+1) ≤ 1) :
    ∃ index, index < length ∧ left index = 0 ∧ right index = 0 := by
  induction length generalizing left right with
  | zero => omega
  | succ length inductionHypothesis =>
      by_cases hzero : right 0 = 0
      · exact ⟨0, by omega, hfirst, hzero⟩
      · have hlength : 0 < length := by
          by_cases hsame : length = 0
          · subst length
            simp_all
          · omega
        have hnext : left 1 = 0 := by
          have hstep : right 0+left 1 ≤ 1 := by simpa using hlink 0 (by omega)
          omega
        have htailLast : (fun index => right (index+1)) (length-1) = 0 := by
          have hsame : length-1+1 = length := by omega
          simpa [hsame] using hlast
        have htailLink : ∀ index, index+1 < length →
            (fun position => right (position+1)) index+
            (fun position => left (position+1)) (index+1) ≤ 1 := by
          intro index hbound
          exact hlink (index+1) (by omega)
        rcases inductionHypothesis (fun index => left (index+1))
          (fun index => right (index+1)) hlength hnext htailLast htailLink with
          ⟨index, hbound, hleft, hright⟩
        exact ⟨index+1, by omega, hleft, hright⟩

theorem sharp_three_full_promotion_impossible
    (leftTop leftBottom middleTop middleBottom rightTop rightBottom : Nat)
    (hleft : leftTop+leftBottom = 1) (hmiddle : middleTop+middleBottom = 1)
    (hright : rightTop+rightBottom = 1)
    (hleftSeed : leftTop = 0) (hrightSeed : rightBottom = 0)
    (hleftFeasible : leftBottom+middleBottom ≤ 1)
    (hrightFeasible : rightTop+middleTop ≤ 1) : False := by
  omega

end SubQuorum.CompatibleBundles
