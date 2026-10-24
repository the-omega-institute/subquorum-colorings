import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SimultaneousIntervalRelease

/-- The counting part of the exact release theorem. The network proof must
separately supply the outside-capacity bound and a saturating extension.
`used` counts different candidate intervals; `outside` counts all other
terminal units, including whole betas. All feasible flows pay the fixed P. -/
theorem exact_release_capacity (p candidates outsideMax : Nat)
    (feasible : Nat → Nat → Prop)
    (conservation : ∀ used outside, feasible used outside → used+outside=p)
    (available : ∀ used outside, feasible used outside → used≤candidates)
    (outsideBound : ∀ used outside, feasible used outside → outside≤outsideMax)
    (extension : ∃ used, feasible used outsideMax) :
    (∃ used outside, feasible used outside ∧ candidates-used=candidates+outsideMax-p) ∧
    (∀ used outside, feasible used outside → candidates-used≤candidates+outsideMax-p) := by
  rcases extension with ⟨used, witness⟩
  have conserved := conservation used outsideMax witness
  have capacity := available used outsideMax witness
  constructor
  · exact ⟨used, outsideMax, witness, by omega⟩
  · intro u o admissible
    have h₁ := conservation u o admissible
    have h₂ := outsideBound u o admissible
    have h₃ := available u o admissible
    omega

/-- If a minimizing deleted cut still omits one member of a minimal
obstruction, restoring that member leaves the same deficient cut. -/
theorem minimal_obstruction_cut_contains_every_deleted (p capacity hit : Int)
    (deficient : capacity-hit=p-1)
    (restoreMissingWouldSuffice : capacity-hit≥p) : False := by omega

theorem minimal_obstruction_cut_capacity (p capacity deleted : Int)
    (deficient : capacity-deleted=p-1) :
    capacity=p+deleted-1 := by omega

/-- The eleven physical identities allow ten simultaneous releases by
value, while the optimal-link face requires two distinct used units. -/
theorem eleven_unit_release_counts (unused used : Nat)
    (partition : unused+used=11) (oneNeeded : 1≤used) :
    unused≤10 ∧ (used=1 → unused=10) ∧ (2≤used → unused≤9) := by omega

/-- Two distinct original C-pocket identities cannot both be released
when at least one must remain used in every one-link certificate. -/
theorem two_unit_cost_obstruction (remaining released : Nat)
    (partition : remaining+released=2) (oneNeeded : 1≤remaining) :
    released≤1 := by omega

/-- Exact local lower/upper bookkeeping, after the geometric proof has
identified copies with an entirely blocked eleven-unit sector. -/
theorem stack_table_ledger (q zero aEmpty cEmpty paid links : Int)
    (payment : paid=3*q-zero)
    (cost : links=q+aEmpty+cEmpty-zero) :
    3*q-paid=zero ∧ links-q=aEmpty+cEmpty-zero := by omega

theorem stacked_release_capacity (q : Nat) :
    11*q+2*q-3*q=10*q ∧ 11*q-2*q=9*q := by omega

/-- With all sources still paid, doubly reserved C pockets contribute
exactly one additional link per copy; singleton reservations add none. -/
theorem c_pocket_extra_links (q doubleDeleted links : Nat)
    (exactCost : links=q+doubleDeleted) :
    links-q=doubleDeleted ∧ (links=q ↔ doubleDeleted=0) := by omega

#print axioms exact_release_capacity
#print axioms minimal_obstruction_cut_contains_every_deleted
#print axioms minimal_obstruction_cut_capacity
#print axioms eleven_unit_release_counts
#print axioms two_unit_cost_obstruction
#print axioms stack_table_ledger
#print axioms stacked_release_capacity
#print axioms c_pocket_extra_links

end SubQuorum.SimultaneousIntervalRelease
