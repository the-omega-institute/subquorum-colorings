import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ResidualReserveCost

/-- A unit simple residual cycle changes the number of unused candidates
by at most one. Minimum-cost baseline optimality supplies nonnegative
cycle cost, represented here by Nat. The network adapter is separate. -/
structure ExchangeCycle where
  gain : Int
  cost : Nat
  gainBound : gain≤1

def gainSum : List ExchangeCycle → Int
  | [] => 0
  | c::cs => c.gain+gainSum cs

def costSum : List ExchangeCycle → Nat
  | [] => 0
  | c::cs => c.cost+costSum cs

private theorem empty_sublist (cs : List ExchangeCycle) : List.Sublist [] cs := by
  induction cs with
  | nil => exact .slnil
  | cons c cs ih => exact .cons c ih

theorem sublist_cost_bound {small large : List ExchangeCycle}
    (sub : small.Sublist large) : costSum small≤costSum large := by
  induction sub with
  | slnil => simp [costSum]
  | cons c sub ih => simp only [costSum]; omega
  | cons_cons c sub ih => simp only [costSum]; omega

/-- From net gain at least h, extract exactly h positive-gain cycles as a
subsequence. Negative/neutral cycles never have to be retained. -/
theorem positive_cycle_selection (cs : List ExchangeCycle) (h : Nat)
    (enough : (h:Int)≤gainSum cs) :
    ∃ selected : List ExchangeCycle, selected.Sublist cs ∧ selected.length=h ∧
      (∀ c∈selected, c.gain=1) := by
  induction cs generalizing h with
  | nil =>
    have zero : h=0 := by simp only [gainSum] at enough; omega
    subst h
    exact ⟨[], .slnil, rfl, by simp⟩
  | cons c cs ih =>
    cases h with
    | zero => exact ⟨[], empty_sublist _, rfl, by simp⟩
    | succ n =>
      by_cases positive : c.gain=1
      · have tailEnough : (n:Int)≤gainSum cs := by
          simp only [gainSum] at enough
          omega
        rcases ih n tailEnough with ⟨chosen, sub, size, allPositive⟩
        refine ⟨c::chosen, .cons_cons c sub, by simp [size], ?_⟩
        intro item inside
        rcases List.mem_cons.mp inside with same | fromTail
        · simpa only [same] using positive
        · exact allPositive item fromTail
      · have notPositive : c.gain≤0 := by have bound := c.gainBound; omega
        have tailEnough : ((n+1:Nat):Int)≤gainSum cs := by
          simp only [gainSum] at enough
          omega
        rcases ih (n+1) tailEnough with ⟨chosen, sub, size, allPositive⟩
        exact ⟨chosen, .cons c sub, size, allPositive⟩

/-- This is the pruning step used by the reserve-cost reverse inequality:
the h exchange paths selected from g-f do not exceed its total cost. -/
theorem prune_positive_cycles_with_cost (cs : List ExchangeCycle) (h : Nat)
    (enough : (h:Int)≤gainSum cs) :
    ∃ selected : List ExchangeCycle, selected.Sublist cs ∧ selected.length=h ∧
      (∀ c∈selected, c.gain=1) ∧ costSum selected≤costSum cs := by
  rcases positive_cycle_selection cs h enough with ⟨chosen, sub, size, pos⟩
  exact ⟨chosen, sub, size, pos, sublist_cost_bound sub⟩

def amount : List Int → Int
  | [] => 0
  | x::xs => x+amount xs

theorem sum_nonnegative (xs : List Int) (nonnegative : ∀ x∈xs, 0≤x) :
    0≤amount xs := by
  induction xs with
  | nil => simp [amount]
  | cons x xs ih =>
    have hx := nonnegative x (by simp)
    have tail := ih (fun y hy => nonnegative y (List.mem_cons_of_mem x hy))
    simp only [amount]
    omega

/-- A residual circulation has zero original cost exactly when each used
arc has zero reduced cost, after potentials telescope. Nonnegativity
must include the represented reverse/forward terminal edges. -/
theorem zero_sum_iff_all_zero (xs : List Int) (nonnegative : ∀ x∈xs, 0≤x) :
    amount xs=0 ↔ ∀ x∈xs, x=0 := by
  induction xs with
  | nil => simp [amount]
  | cons x xs ih =>
    have hx := nonnegative x (by simp)
    have tailNonneg : ∀ y∈xs, 0≤y :=
      fun y hy => nonnegative y (List.mem_cons_of_mem x hy)
    have tailBound := sum_nonnegative xs tailNonneg
    constructor
    · intro total item inside
      simp only [amount] at total
      have headZero : x=0 := by omega
      have tailZero : amount xs=0 := by omega
      rcases List.mem_cons.mp inside with same | fromTail
      · simpa only [same] using headZero
      · exact (ih tailNonneg).mp tailZero item fromTail
    · intro allZero
      have headZero := allZero x (by simp)
      have tailZero := (ih tailNonneg).mpr
        (fun y hy => allZero y (List.mem_cons_of_mem x hy))
      simp only [amount]
      omega

theorem same_endpoint_potential_cost (cost reduced start finish : Int)
    (telescopes : reduced=cost+start-finish) (same : start=finish) :
    reduced=cost := by omega

#print axioms sublist_cost_bound
#print axioms positive_cycle_selection
#print axioms prune_positive_cycles_with_cost
#print axioms sum_nonnegative
#print axioms zero_sum_iff_all_zero
#print axioms same_endpoint_potential_cost

end SubQuorum.ResidualReserveCost
