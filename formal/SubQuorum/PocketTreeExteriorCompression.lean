import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PocketTreeExteriorCompression

def routeCost : List Nat → Nat
  | [] => 0
  | c::cs => c+routeCost cs

/-- Unsupported alpha sources force every exterior route to start with
at least one real link. This lemma sums the routewise lower bounds. -/
theorem positive_routes_pay_their_count (cs : List Nat)
    (positive : ∀ c∈cs, 1≤c) : cs.length≤routeCost cs := by
  induction cs with
  | nil => simp [routeCost]
  | cons c cs ih =>
    have hc := positive c (by simp)
    have ht := ih (fun x hx => positive x (List.mem_cons_of_mem c hx))
    simp only [List.length_cons,routeCost]
    omega

/-- Retain one exterior representative and replace all other exterior
routes with internal tree stems of cost one. The root/parent-edge
construction itself is the separate written graph adapter. -/
theorem prune_to_one_exterior (n head : Nat) (tail : List Nat)
    (fits : tail.length+1≤n) (positive : ∀ c∈tail, 1≤c) :
    head+(n-1)≤routeCost (head::tail)+(n-(tail.length+1)) := by
  have bound := positive_routes_pay_their_count tail positive
  simp only [routeCost]
  omega

/-- Exact local ledger for any selected exterior root set of size x,
including the unpaid-root case x=0. Distinct parent edges pay all others. -/
theorem local_payment_ledger (n x : Nat) (nonempty : 1≤n) (fits : x≤n) :
    (n-max 1 x)+x=(n-1)+(if x=0 then 0 else 1) ∧
    n-max 1 x=(n-1)-(x-1) := by
  by_cases hx : x=0
  · subst x
    simp
  · have hm : max 1 x=x := Nat.max_eq_right (by omega)
    rw [hm,if_neg hx]
    omega

/-- The finite reward penalty strictly prioritizes covered residual
sources over the entire possible cost-discount range [-B,L]. This is
the lexicographic step for the discounted circulation, not a proof of
integral min-cost circulation or the geometric compression. -/
theorem coverage_reward_dominates (B L M a b cA cB : Int)
    (penalty : L+B<M) (nonnegative : 0≤M)
    (higher : b<a) (upper : cA≤L) (lower : -B≤cB) :
    cA-M*a<cB-M*b := by
  have gap : M*(b+1)≤M*a :=
    Int.mul_le_mul_of_nonneg_left (by omega) nonnegative
  rw [Int.mul_add,Int.mul_one] at gap
  omega

#print axioms positive_routes_pay_their_count
#print axioms prune_to_one_exterior
#print axioms local_payment_ledger
#print axioms coverage_reward_dominates

end SubQuorum.PocketTreeExteriorCompression
