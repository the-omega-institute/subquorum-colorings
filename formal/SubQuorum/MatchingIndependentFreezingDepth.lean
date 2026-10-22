import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

namespace SubQuorum.MatchingIndependentFreezingDepth

def bit (choice : Bool) : Nat := if choice then 1 else 0

theorem local_entry_cycle (arrival firstEntry interior : Nat)
    (hentry : firstEntry = 1+min arrival interior)
    (hinterior : interior = 1+max firstEntry 1) :
    firstEntry = arrival+1 ∧ interior = arrival+2 := by omega

theorem local_transmission (arrival firstEntry interior outgoing : Nat) (vertical : Bool)
    (hentry : firstEntry = 1+min arrival interior)
    (hinterior : interior = 1+max firstEntry 1)
    (houtgoing : outgoing = 1+max (if vertical then interior else firstEntry) 1) :
    outgoing = arrival+2+bit vertical := by
  have resolved := local_entry_cycle arrival firstEntry interior hentry hinterior
  cases vertical <;> simp only [bit, Bool.false_eq_true, if_false, if_true] at * <;> omega

def verticalCount (choices : Nat → Bool) : Nat → Nat
  | 0 => 0
  | index+1 => verticalCount choices index + bit (choices index)

def arrival (choices : Nat → Bool) : Nat → Nat
  | 0 => 1
  | index+1 => arrival choices index+3+bit (choices index)

theorem exact_prefix_arrival (choices : Nat → Bool) (index : Nat) :
    arrival choices index = 3*index+1+verticalCount choices index := by
  induction index with
  | zero => rfl
  | succ index previous =>
    simp only [arrival, verticalCount]
    omega

theorem unavoidable_arrival (choices : Nat → Bool) (index : Nat) :
    3*index+1 ≤ arrival choices index := by
  have exactTime := exact_prefix_arrival choices index
  omega

theorem all_matching_depth_lower_bound (choices : Nat → Bool) (copies depth : Nat)
    (hpositive : 0 < copies)
    (hdepth : arrival choices (copies-1)+2 ≤ depth) :
    3*copies ≤ depth := by
  have entryBound := unavoidable_arrival choices (copies-1)
  omega

theorem no_uniform_rematching_budget (choices : Nat → Bool) (budget depth : Nat)
    (hdepth : arrival choices budget+2 ≤ depth) :
    budget < depth := by
  have entryBound := unavoidable_arrival choices budget
  omega

#print axioms local_entry_cycle
#print axioms local_transmission
#print axioms exact_prefix_arrival
#print axioms unavoidable_arrival
#print axioms all_matching_depth_lower_bound
#print axioms no_uniform_rematching_budget

end SubQuorum.MatchingIndependentFreezingDepth
