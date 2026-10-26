import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.NewBetaRetention

/-- A residual walk whose every edge has nonnegative reduced cost for pi.
Costs may be negative on reverse arcs. No acyclicity assumption is made. -/
inductive ResidualWalk {V : Type} (pi : V → Int) : V → V → Int → Nat → Prop where
  | nil (u : V) : ResidualWalk pi u u 0 0
  | cons {u v z : V} {edge rest : Int} {n : Nat}
      (reduced : 0 ≤ edge + pi u - pi v)
      (tail : ResidualWalk pi v z rest n) :
      ResidualWalk pi u z (edge + rest) (n + 1)

/-- Telescoping reduced costs along an arbitrary finite residual walk. -/
theorem walk_reduced_cost_nonnegative {V : Type} {pi : V → Int}
    {u v : V} {cost : Int} {n : Nat} (walk : ResidualWalk pi u v cost n) :
    0 ≤ cost + pi u - pi v := by
  induction walk with
  | nil u => omega
  | cons reduced tail ih => omega

/-- If a used resource has its zero-cost return edge to the source,
no residual source-to-resource prefix has negative cost. -/
theorem used_resource_prefix_nonnegative {V : Type} {pi : V → Int}
    {source resource : V} {cost : Int} {n : Nat}
    (walk : ResidualWalk pi source resource cost n)
    (return_edge : 0 ≤ pi resource - pi source) : 0 ≤ cost := by
  have bound := walk_reduced_cost_nonnegative walk
  omega

/-- A zero-cost one-edge private-beta entrance strictly improves the
(cost, residual-arc-count) key over any >=two-edge nonnegative-cost prefix,
with the same suffix. This is a local path choice, not a global fourth cost. -/
theorem private_shortcut_strictly_better
    (prefixCost suffix : Int) (prefixLength suffixLength : Nat)
    (nonnegative : 0 ≤ prefixCost) (long : 2 ≤ prefixLength) :
    suffix < prefixCost + suffix ∨
      (suffix = prefixCost + suffix ∧ 1 + suffixLength < prefixLength + suffixLength) := by
  by_cases zero : prefixCost = 0
  · right; constructor <;> omega
  · left; omega

/-- Once initial interval and beta sets are retained, net gain is precisely
fresh original intervals plus fresh whole-beta resources. In particular,
new beta credits cannot also be charged as fresh interval gains. -/
theorem fresh_resource_ledger
    (oldIntervals oldBetas freshIntervals freshBetas oldValue finalValue gain : Nat)
    (old_balance : oldValue = oldIntervals + oldBetas)
    (final_balance : finalValue = (oldIntervals + freshIntervals) + (oldBetas + freshBetas))
    (value_gain : finalValue = oldValue + gain) :
    gain = freshIntervals + freshBetas ∧ freshBetas ≤ gain := by
  omega

end SubQuorum.NewBetaRetention

#print axioms SubQuorum.NewBetaRetention.walk_reduced_cost_nonnegative
#print axioms SubQuorum.NewBetaRetention.used_resource_prefix_nonnegative
#print axioms SubQuorum.NewBetaRetention.private_shortcut_strictly_better
#print axioms SubQuorum.NewBetaRetention.fresh_resource_ledger
