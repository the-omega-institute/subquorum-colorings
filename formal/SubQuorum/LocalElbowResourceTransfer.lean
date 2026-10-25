import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.LocalElbowResourceTransfer

theorem local_delta (selections : Nat) (feasible : selections≤1) :
    2-selections=1 ∨ 2-selections=2 := by omega

/-- Losses are indexed by DISTINCT old witness owners. Each can use at
most one interval in a normal pack; dropping one fork arm loses only one. -/
theorem distinct_witness_losses (xs : List Nat)
    (unitBound : ∀ x, x∈xs → x≤1) : xs.sum≤xs.length := by
  induction xs with
  | nil => simp
  | cons h hs ih =>
      have head := unitBound h (by simp)
      have tail : ∀ x, x∈hs → x≤1 := by
        intro x hx
        exact unitBound x (by simp [hx])
      have bound := ih tail
      simp only [List.sum_cons,List.length_cons]
      omega

theorem joint_exact_value (p q p0 r newV : Int)
    (definition : r=p-p0) (adapter : newV=q+p0) :
    newV=p+q-r := by omega

theorem joint_nondecrease (p q p0 r z newV : Int)
    (definition : r=p-p0) (adapter : newV=q+p0)
    (lossBound : 0≤r ∧ r≤z) (distinctWitnesses : z≤q) :
    p≤newV ∧ newV≤p+q ∧ p+q-z≤newV := by omega

theorem strict_gain_criterion (p q r newV : Int)
    (formula : newV=p+q-r) : newV=p+q ↔ r=0 := by omega

theorem single_unpaid_gain (p p0 r newV : Int)
    (definition : r=p-p0) (unitLoss : 0≤r ∧ r≤1)
    (adapter : newV=1+p0) : newV=p ∨ newV=p+1 := by omega

theorem no_unpaid_hypothesis_no_monotonicity (p pminus p0 r e newV : Int)
    (oldEssential : e=p-pminus) (oldUnit : 0≤e ∧ e≤1)
    (oldLoss : r=pminus-p0) (lossUnit : 0≤r ∧ r≤1)
    (adapter : newV=1+p0) :
    newV-p=1-r-e ∧ p-1≤newV ∧ newV≤p+1 := by omega

theorem residual_deficit (alpha oldV newV q r : Int)
    (formula : newV=oldV+q-r) :
    alpha-newV=alpha-oldV-q+r := by omega

theorem all_residual_paid (alpha oldV newV q r : Int)
    (residual : q=alpha-oldV) (zeroJointLoss : r=0)
    (formula : newV=oldV+q-r) : newV=alpha := by omega

/-- beta forks use one original interval and one whole-beta credit for
two payments. The resource ledger is supplied once, without extra beta. -/
theorem coefficient_one (S L beta alpha : Int)
    (ledger : S=L+beta-alpha) (completePack : alpha≤L+beta) : 0≤S := by omega

def oldPayment (keep1 keep2 : Bool) : Nat := if keep1 || keep2 then 1 else 0

/-- Two individually harmless withdrawals have a harmful union. This is
an abstract incidence example, with no claimed frozen-grid embedding. -/
theorem joint_withdrawal_not_sum_of_marginals :
    oldPayment true true-oldPayment false true=0 ∧
    oldPayment true true-oldPayment true false=0 ∧
    oldPayment true true-oldPayment false false=1 := by decide

def capLoss : List (Nat × Bool) → Nat
  | [] => 0
  | x::xs => x.1+capLoss xs
def hitCount : List (Nat × Bool) → Nat
  | [] => 0
  | x::xs => (if x.2 then 1 else 0)+hitCount xs
def unpaid : List (Nat × Bool) → Nat
  | [] => 0
  | x::xs => (if x.1=0 ∧ x.2=false then 1 else 0)+unpaid xs

theorem arbitrary_module_budget (xs : List (Nat × Bool)) :
    xs.length≤capLoss xs+unpaid xs+hitCount xs := by
  induction xs with
  | nil => simp [capLoss,unpaid,hitCount]
  | cons h hs ih =>
      rcases h with ⟨loss,hit⟩
      cases hit <;> by_cases zero : loss=0 <;>
        simp [capLoss,unpaid,hitCount,zero] <;> omega

theorem physical_module_budget (xs : List (Nat × Bool)) (ell actions : Nat)
    (cover : capLoss xs≤ell) (distinctModules : hitCount xs≤actions) :
    xs.length≤ell+unpaid xs+actions := by
  have h := arbitrary_module_budget xs
  omega

theorem quota_upper (tau size k d j : Int)
    (allT : size≤tau) (budget : k≤tau-size+d+j) :
    size≤tau-max 0 (k-d-j) := by omega

theorem quota_attainer (k d j : Nat) (threshold : d≤k) :
    let q := min j (k-d)
    let ell := k-d-q
    q≤j ∧ q+ell+d=k ∧ (ell : Int)=max 0 ((k : Int)-d-j) := by
  simp only
  omega

theorem two_tiles_independent_of_height (q : Nat) :
    2*q=q+q := by omega

theorem single_tile_tax_transfer (b s tax : Int) (hasSeam : 1≤s)
    (oldTax : tax=b+s) : 0≤s-1 ∧ (b+1)+(s-1)=tax := by omega

end SubQuorum.LocalElbowResourceTransfer

#print axioms SubQuorum.LocalElbowResourceTransfer.local_delta
#print axioms SubQuorum.LocalElbowResourceTransfer.distinct_witness_losses
#print axioms SubQuorum.LocalElbowResourceTransfer.joint_exact_value
#print axioms SubQuorum.LocalElbowResourceTransfer.joint_nondecrease
#print axioms SubQuorum.LocalElbowResourceTransfer.strict_gain_criterion
#print axioms SubQuorum.LocalElbowResourceTransfer.single_unpaid_gain
#print axioms SubQuorum.LocalElbowResourceTransfer.no_unpaid_hypothesis_no_monotonicity
#print axioms SubQuorum.LocalElbowResourceTransfer.residual_deficit
#print axioms SubQuorum.LocalElbowResourceTransfer.all_residual_paid
#print axioms SubQuorum.LocalElbowResourceTransfer.coefficient_one
#print axioms SubQuorum.LocalElbowResourceTransfer.joint_withdrawal_not_sum_of_marginals
#print axioms SubQuorum.LocalElbowResourceTransfer.arbitrary_module_budget
#print axioms SubQuorum.LocalElbowResourceTransfer.physical_module_budget
#print axioms SubQuorum.LocalElbowResourceTransfer.quota_upper
#print axioms SubQuorum.LocalElbowResourceTransfer.quota_attainer
#print axioms SubQuorum.LocalElbowResourceTransfer.two_tiles_independent_of_height
#print axioms SubQuorum.LocalElbowResourceTransfer.single_tile_tax_transfer
