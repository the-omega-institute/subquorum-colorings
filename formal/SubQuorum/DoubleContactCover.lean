import Lean.Elab.Tactic.Omega

/-! Ordered prefix-credit and disjoint-batch count kernels.
The geometric prefix adapter, actual disjoint ownership, optimal range query,
Hall coverage and min-cost matching theorem remain written. -/
set_option autoImplicit false
namespace SubQuorum.DoubleContactCover

theorem strict_prefix_credit (x₁ x₂ y₁ y₂ : Nat)
    (hx : x₁ < x₂) (hy : y₂ < y₁) :
    2 ≤ (x₂-x₁)+(y₁-y₂) := by omega

theorem prefix_credit_identity (x₁ x₂ y₁ y₂ : Nat)
    (hx : x₁ ≤ x₂) (hy : y₂ ≤ y₁) :
    (((x₂-x₁)+(y₁-y₂) : Nat) : Int) =
      ((x₂ : Int)-y₂)-((x₁ : Int)-y₁) := by omega

theorem inner_credit_bound (x₁ x₂ y₁ y₂ a b : Nat)
    (hx : x₂ ≤ a) (hy : y₁ ≤ b) :
    (x₂-x₁)+(y₁-y₂) ≤ a+b := by omega

structure Account where
  total : Nat
  credit : Nat
  bounded : credit ≤ total

def cost (a : Account) : Nat := a.total-a.credit

theorem local_cost_exact (a : Account) : cost a+a.credit=a.total := by
  have h := a.bounded
  simp only [cost]
  omega

def oldSum : List Account → Nat
  | [] => 0
  | a :: rest => a.total + oldSum rest

def costSum : List Account → Nat
  | [] => 0
  | a :: rest => cost a + costSum rest

def creditSum : List Account → Nat
  | [] => 0
  | a :: rest => a.credit + creditSum rest

theorem sum_batch_balance (accounts : List Account) :
    costSum accounts+creditSum accounts=oldSum accounts := by
  induction accounts with
  | nil => rfl
  | cons a rest ih =>
      have h := local_cost_exact a
      simp only [costSum, creditSum, oldSum]
      omega

theorem zero_cost_iff (a : Account) : cost a=0 ↔ a.credit=a.total := by
  have h := a.bounded
  simp only [cost]
  omega

theorem batch_saving (accounts : List Account) :
    (oldSum accounts : Int)-costSum accounts=creditSum accounts := by
  have h := sum_batch_balance accounts
  omega

end SubQuorum.DoubleContactCover
#print axioms SubQuorum.DoubleContactCover.strict_prefix_credit
#print axioms SubQuorum.DoubleContactCover.prefix_credit_identity
#print axioms SubQuorum.DoubleContactCover.inner_credit_bound
#print axioms SubQuorum.DoubleContactCover.local_cost_exact
#print axioms SubQuorum.DoubleContactCover.sum_batch_balance
#print axioms SubQuorum.DoubleContactCover.zero_cost_iff
#print axioms SubQuorum.DoubleContactCover.batch_saving
