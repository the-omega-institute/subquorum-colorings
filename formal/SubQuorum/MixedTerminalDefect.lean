import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.MixedTerminalDefect

def bit (x : Bool) : Nat := if x then 1 else 0

theorem degree_three_absent_normal (l r : Bool)
    (degree : 1+bit false+bit l+bit r=3) : l=true ∧ r=true := by
  cases l <;> cases r <;> simp [bit] at *

theorem degree_three_present_normal (l r : Bool)
    (degree : 1+bit true+bit l+bit r=3) :
    (l=false ∧ r=true) ∨ (l=true ∧ r=false) := by
  cases l <;> cases r <;> simp [bit] at *

theorem degree_four (n l r : Bool)
    (degree : 1+bit n+bit l+bit r=4) : n=true ∧ l=true ∧ r=true := by
  cases n <;> cases l <;> cases r <;> simp [bit] at *

/-- The positive flag means the sole axis gap is an available positive
original forest inside the local band. It is false for a balanced forest
or a gap outside that band's axis boundary. -/
def zeroIncidence (l r positive : Bool) : Nat :=
  if ((!l || !r) && positive) then 0 else 1
def fourDefect (n l r : Bool) : Nat := bit (n && l && r)
def seamDefect (n : Bool) : Nat := bit (!n)
def boundaryDefect (n l r positive : Bool) : Nat :=
  bit (n && (!l || !r) && !positive)

theorem local_zero_identity (n l r positive : Bool)
    (degree : 3≤1+bit n+bit l+bit r) :
    zeroIncidence l r positive = fourDefect n l r + seamDefect n + boundaryDefect n l r positive := by
  cases n <;> cases l <;> cases r <;> cases positive <;>
    simp [bit,zeroIncidence,fourDefect,seamDefect,boundaryDefect] at *

/-- Selecting N(v) forbids the N partner of a parallel actual mate when
those two partners are adjacent in the same auxiliary phase. -/
theorem parallel_partner_blank (Site : Type) (P T : Site → Prop)
    (N : Site → Site) (Adj : Site → Site → Prop) (v p : Site)
    (feasible : ∀ x, T x → ∀ a b, (P a ∨ T a) → (P b ∨ T b) →
      Adj x a → Adj x b → a=b)
    (anchor : P v) (selected : T (N v)) (ownAnchor : Adj (N v) v)
    (parallel : Adj (N v) (N p)) (different : v≠N p) :
    ¬ (P (N p) ∨ T (N p)) := by
  intro occupied
  exact different (feasible (N v) selected v (N p) (Or.inl anchor) occupied ownAnchor parallel)

/-- On an actual matching edge the opposite endpoint cannot also be a seam
terminal: its opposite N-normal neighbour is the first endpoint in P. -/
theorem charge_injective (Site Edge : Type) (mate : Site → Site)
    (edge : Site → Edge) (Seam : Site → Prop)
    (sameEdge : ∀ u v, edge u=edge v → u=v ∨ u=mate v)
    (noOpposite : ∀ v, Seam v → ¬ Seam (mate v)) :
    ∀ u v, Seam u → Seam v → edge u=edge v → u=v := by
  intro u v hu hv he
  rcases sameEdge u v he with equal | opposite
  · exact equal
  · exact False.elim (noOpposite v hv (opposite ▸ hu))

theorem joint_seam_tax (D d4 b s eHV h : Int)
    (zeroIdentity : h=d4+b+s) (deficientPaths : 2*D≤h)
    (injectiveCharge : s≤eHV) : 2*D≤d4+b+s ∧ 2*D≤d4+b+eHV := by omega

theorem one_seam_no_failure (D s eHV : Int)
    (nonnegative : 0≤D) (portTax : 2*D≤s)
    (injectiveCharge : s≤eHV) (oneEdge : eHV≤1) : D=0 := by omega

/-- Count original interval units once; beta is used once in the exact
objective ledger, rather than being added again to the port assignment. -/
theorem coefficient_one (S L beta alpha D tax : Int)
    (ledger : S=L+beta-alpha) (allocation : alpha-D≤L)
    (portTax : 2*D≤tax) (criterion : tax≤2*beta+1) : 0≤S := by omega

def paid : List Nat → Nat
  | [] => 0
  | h::hs => (if h=0 then 0 else 1)+paid hs
def unpaid : List Nat → Nat
  | [] => 0
  | h::hs => (if h=0 then 1 else 0)+unpaid hs

/-- Arbitrarily many private source supports: each nonempty support costs
at least one distinct cap loss. -/
theorem sum_ge_paid (hs : List Nat) : paid hs≤hs.sum := by
  induction hs with
  | nil => simp [paid]
  | cons h hs ih =>
      by_cases empty : h=0
      · simp only [paid,if_pos empty,List.sum_cons]
        omega
      · have positive : 1≤h := by omega
        simp only [paid,if_neg empty,List.sum_cons]
        omega

theorem partition_counts (hs : List Nat) : paid hs+unpaid hs=hs.length := by
  induction hs with
  | nil => rfl
  | cons h hs ih =>
      by_cases empty : h=0 <;> simp [paid,unpaid,empty] at * <;> omega

theorem private_frontier (hs : List Nat) (ell : Nat) (coverBudget : hs.sum≤ell) :
    hs.length≤ell+unpaid hs := by
  have h := sum_ge_paid hs
  have p := partition_counts hs
  omega

theorem every_frozen_maximum (hs : List Nat) (ell : Nat)
    (coverBudget : hs.sum≤ell) (maximum : ell=0) : unpaid hs=hs.length := by
  have h := private_frontier hs ell coverBudget
  have p := partition_counts hs
  omega

theorem pareto_upper (tau size D d k : Int)
    (frontier : k≤tau-size+D) (threshold : D≤d) : size≤tau-k+d := by omega

theorem sharp_attainer (tau k d : Int) (range : 0≤d ∧ d≤k) :
    let opened := k-d
    0≤opened ∧ opened≤k ∧ k-opened=d ∧ tau-opened=tau-k+d := by omega

theorem sharp_seam_counts (k : Int) :
    let deficit := k
    let seams := 2*k
    let eHV := 2*k
    2*deficit=seams ∧ seams=eHV := by omega

end SubQuorum.MixedTerminalDefect

#print axioms SubQuorum.MixedTerminalDefect.degree_three_absent_normal
#print axioms SubQuorum.MixedTerminalDefect.degree_three_present_normal
#print axioms SubQuorum.MixedTerminalDefect.degree_four
#print axioms SubQuorum.MixedTerminalDefect.local_zero_identity
#print axioms SubQuorum.MixedTerminalDefect.parallel_partner_blank
#print axioms SubQuorum.MixedTerminalDefect.charge_injective
#print axioms SubQuorum.MixedTerminalDefect.joint_seam_tax
#print axioms SubQuorum.MixedTerminalDefect.one_seam_no_failure
#print axioms SubQuorum.MixedTerminalDefect.coefficient_one
#print axioms SubQuorum.MixedTerminalDefect.sum_ge_paid
#print axioms SubQuorum.MixedTerminalDefect.partition_counts
#print axioms SubQuorum.MixedTerminalDefect.private_frontier
#print axioms SubQuorum.MixedTerminalDefect.every_frozen_maximum
#print axioms SubQuorum.MixedTerminalDefect.pareto_upper
#print axioms SubQuorum.MixedTerminalDefect.sharp_attainer
#print axioms SubQuorum.MixedTerminalDefect.sharp_seam_counts
