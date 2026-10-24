import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.GuardedPocketForkReplacement

/-- A new endpoint has four possible grid neighbors. Two already have fixed
old mates, and a saturated selected guard forbids the lower neighbor from
being occupied. Its only possible mate is the other top pocket vertex. -/
theorem forced_horizontal_mate {V : Type} (endpoint : V → Prop) (mate : V → V)
    (u v oldLeft oldAbove lower : V)
    (eu : endpoint u)
    (mateEndpoint : ∀ x, endpoint x → endpoint (mate x))
    (inverse : ∀ x, endpoint x → mate (mate x)=x)
    (fourNeighbors : mate u=oldLeft ∨ mate u=oldAbove ∨ mate u=v ∨ mate u=lower)
    (oldLeftFixed : mate oldLeft≠u) (oldAboveFixed : mate oldAbove≠u)
    (lowerForbidden : ¬endpoint lower) :
    mate u=v ∧ endpoint v ∧ mate v=u := by
  have forced : mate u=v := by
    rcases fourNeighbors with h | h | h | h
    · have inv := inverse u eu
      rw [h] at inv
      exact False.elim (oldLeftFixed inv)
    · have inv := inverse u eu
      rw [h] at inv
      exact False.elim (oldAboveFixed inv)
    · exact h
    · have ep := mateEndpoint u eu
      rw [h] at ep
      exact False.elim (lowerForbidden ep)
  refine ⟨forced, ?_, ?_⟩
  · simpa only [forced] using mateEndpoint u eu
  · simpa only [forced] using inverse u eu

/-- Either top endpoint forces the other one, so there is no feasible
partially filled pocket. The absence of selections is supplied by the
separate two-old-neighbor feasibility argument. -/
theorem empty_or_paired_endpoints {V : Type} (endpoint : V → Prop) (u v : V)
    (uv : endpoint u → endpoint v) (vu : endpoint v → endpoint u) :
    (¬endpoint u ∧ ¬endpoint v) ∨ (endpoint u ∧ endpoint v) := by
  by_cases eu : endpoint u
  · exact Or.inr ⟨eu, uv eu⟩
  · exact Or.inl ⟨eu, fun ev => eu (vu ev)⟩

/-- A beta whose every entering certificate uses C cannot have been
reserved by another owner-disjoint certificate while C belongs to the
fork being replaced. This is the actual reason the new beta is free. -/
theorem exclusive_beta_not_used_outside {Cert : Type}
    (usesC usesBeta : Cert → Prop) (fork : Cert)
    (inside : usesC fork)
    (sourceDisjoint : ∀ p, p≠fork → usesC p → ¬usesC fork)
    (exclusive : ∀ p, usesBeta p → usesC p) :
    ∀ p, p≠fork → ¬usesBeta p := by
  intro p other paid
  exact sourceDisjoint p other (exclusive p paid) inside

/-- Private beta replacements for distinct old alpha roots are different
resources. No simultaneous replacement may count the same beta twice. -/
theorem distinct_private_betas {Index Source Beta : Type}
    (root : Index → Source) (sink : Index → Beta)
    (access : Source → Beta → Prop)
    (distinctRoots : Function.Injective root)
    (own : ∀ i, access (root i) (sink i))
    (privateSink : ∀ b x y, access x b → access y b → x=y) :
    Function.Injective sink := by
  intro i j same
  apply distinctRoots
  have ai := own i
  have aj := own j
  rw [←same] at aj
  exact privateSink (sink i) (root i) (root j) ai aj

#print axioms forced_horizontal_mate
#print axioms empty_or_paired_endpoints
#print axioms exclusive_beta_not_used_outside
#print axioms distinct_private_betas

end SubQuorum.GuardedPocketForkReplacement
