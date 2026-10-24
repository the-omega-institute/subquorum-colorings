import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PairedHoleCertificates

/-- The application supplies actual counts from a connected incidence
multigraph, counting parallel assigned-slot edges separately. Graph
connectedness and the incidence-to-strand adapter are not assumed proved
by this arithmetic theorem. -/
theorem connected_component_exact (alphas resources edges holes : Nat)
    (partition : edges+holes=2*alphas)
    (slotCapacity : edges≤2*resources)
    (connected : alphas+resources≤edges+1) :
    holes≤2 ∧ alphas-resources=holes/2 := by
  omega

def budget (holes : List Nat) : Nat := (holes.map fun h => h/2).sum
def twoHoleCount (holes : List Nat) : Nat :=
  (holes.map fun h => if h=2 then 1 else 0).sum

theorem budget_counts_two_hole_components (holes : List Nat)
    (small : ∀ h ∈ holes, h≤2) : budget holes=twoHoleCount holes := by
  induction holes with
  | nil => simp [budget,twoHoleCount]
  | cons h rest ih =>
    have hh : h≤2 := small h (by simp)
    have hr : budget rest=twoHoleCount rest := ih (by
      intro k hk
      exact small k (by simp [hk]))
    have value : h/2=(if h=2 then 1 else 0) := by
      split <;> omega
    simp only [budget,twoHoleCount,List.map_cons,List.sum_cons] at *
    omega

inductive Kind where
  | alpha | beta | mixed
deriving DecidableEq, Repr

def alphaCount : Kind → Nat
  | .alpha => 1
  | _ => 0

/-- Only the endpoint-admissible cases are used: the TP component is alpha
or mixed; the BP component is beta or mixed. -/
def join : Kind → Kind → Kind
  | .alpha, .mixed => .alpha
  | .mixed, .beta => .beta
  | _, _ => .mixed

theorem direct_join_does_not_increase (tp bp : Kind)
    (tpEnd : tp=Kind.alpha ∨ tp=Kind.mixed)
    (bpEnd : bp=Kind.beta ∨ bp=Kind.mixed) :
    alphaCount (join tp bp)≤alphaCount tp+alphaCount bp := by
  rcases tpEnd with ht | ht <;> rcases bpEnd with hb | hb <;>
    subst tp <;> subst bp <;> decide

/-- Joining the two ends of the same path is admissible only for a mixed
path and leaves a cycle, which contributes no alpha path. -/
theorem closing_mixed_does_not_increase : 0≤alphaCount Kind.mixed := by decide

theorem joins_with_unchanged_components (rest : Nat) (tp bp : Kind)
    (tpEnd : tp=Kind.alpha ∨ tp=Kind.mixed)
    (bpEnd : bp=Kind.beta ∨ bp=Kind.mixed) :
    rest+alphaCount (join tp bp)≤rest+alphaCount tp+alphaCount bp := by
  have h := direct_join_does_not_increase tp bp tpEnd bpEnd
  omega

#print axioms connected_component_exact
#print axioms budget_counts_two_hole_components
#print axioms direct_join_does_not_increase
#print axioms closing_mixed_does_not_increase
#print axioms joins_with_unchanged_components

end SubQuorum.PairedHoleCertificates
