import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false

namespace SubQuorum.LiveGateCertificateTradeoff

def bit (b : Bool) : Nat := if b then 1 else 0

/-- The actual local three-edge path has a direct A->B edge, an M->B
edge sharing its BP, and an A->N edge sharing its TP. -/
def localLegal (direct fromM toN : Bool) : Prop :=
  ¬ (direct=true ∧ fromM=true) ∧ ¬ (direct=true ∧ toN=true)

theorem local_matching_capacity (direct fromM toN : Bool)
    (legal : localLegal direct fromM toN) :
    bit direct+bit fromM+bit toN+bit direct≤2 := by
  cases direct <;> cases fromM <;> cases toN <;>
    simp [localLegal,bit] at *

abbrev Local := Bool × Bool × Bool

def localSize (x : Local) : Nat := bit x.1+bit x.2.1+bit x.2.2
def localTotal (xs : List Local) : Nat := (xs.map localSize).sum
def directTotal (xs : List Local) : Nat := (xs.map fun x => bit x.1).sum

theorem local_group_capacity (xs : List Local)
    (legal : ∀ x ∈ xs, localLegal x.1 x.2.1 x.2.2) :
    localTotal xs+directTotal xs≤2*xs.length := by
  induction xs with
  | nil => simp [localTotal,directTotal]
  | cons x rest ih =>
    have first := local_matching_capacity x.1 x.2.1 x.2.2 (legal x (by simp))
    have next := ih (by
      intro y hy
      exact legal y (by simp [hy]))
    simp only [localTotal,directTotal,List.map_cons,List.sum_cons,
      List.length_cons,localSize] at *
    omega

/-- An actual injective list of routed gate identities, all equal to the
one original mixed root, has at most one element. The directed tree adapter
supplies that every indirect route uses this root. -/
theorem unique_gate_capacity {G : Type} (gate : G) (used : List G)
    (distinct : used.Nodup) (same : ∀ x ∈ used, x=gate) : used.length≤1 := by
  have included : ∀ x ∈ used, x ∈ [gate] := by
    intro x hx
    simp [same x hx]
  have cap := distinct.length_le_of_subset included
  simpa using cap

/-- Each merger and splitter contributes at most one selected link. Their
q-1 counts and the actual local capacity imply the global assignment bound.
This theorem does not formalize the graph/tree decomposition itself. -/
theorem global_assignment_bound (q m merge split : Nat) (xs : List Local)
    (positive : 1≤q) (groups : xs.length=q)
    (legal : ∀ x ∈ xs, localLegal x.1 x.2.1 x.2.2)
    (mergeCap : merge≤q-1) (splitCap : split≤q-1)
    (count : m=localTotal xs+merge+split) :
    m+directTotal xs≤4*q-2 := by
  have capacity := local_group_capacity xs legal
  omega

theorem frontier_upper_bound (q m direct paid : Nat)
    (positive : 1≤q) (assignment : m+direct≤4*q-2)
    (gate : paid≤direct+1) : m+paid≤4*q-1 := by omega

theorem every_maximum_pays_at_most_one (q m direct paid : Nat)
    (_positive : 1≤q) (assignment : m+direct≤4*q-2)
    (maximum : m=4*q-2) (gate : paid≤direct+1) : paid≤1 := by omega

theorem full_payment_cardinality_bound (q m direct : Nat)
    (positive : 1≤q) (assignment : m+direct≤4*q-2)
    (gate : q≤direct+1) : m≤3*q-1 := by omega

theorem exact_frontier_arithmetic (q paid : Nat)
    (positive : 1≤paid) (possible : paid≤q) :
    (paid-1)+2*(q-(paid-1))+2*(q-1)=4*q-1-paid ∧
    (4*q-2)-(4*q-1-paid)=paid-1 := by omega

theorem full_payment_exact_gap (q : Nat) (positive : 1≤q) :
    (4*q-2)-(3*q-1)=q-1 := by omega

#print axioms local_matching_capacity
#print axioms local_group_capacity
#print axioms unique_gate_capacity
#print axioms global_assignment_bound
#print axioms frontier_upper_bound
#print axioms every_maximum_pays_at_most_one
#print axioms full_payment_cardinality_bound
#print axioms exact_frontier_arithmetic
#print axioms full_payment_exact_gap

end SubQuorum.LiveGateCertificateTradeoff
