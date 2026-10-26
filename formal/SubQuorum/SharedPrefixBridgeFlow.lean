import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SharedPrefixBridgeFlow

/-- In a deficient n-request tree, outgoing bridge paths remove that many
internal requests. If h receivers paid both sources, discarding h-1 extra
receiver slots is absorbed by the n-1 old internal payment baseline. This
is the per-tree upper bound permitting one actual bridge per donor tree. -/
theorem redundant_bridge_slots_absorbed
    (n inside outgoing doubled : Nat)
    (positive : 1 ≤ n)
    (source_count : inside + outgoing ≤ n)
    (resource_count : inside ≤ n - 1)
    (doubles_le : doubled ≤ outgoing) :
    inside + (doubled - 1) ≤ n - 1 := by
  omega

/-- A source-to-sink augmenting path that never returns to source or leaves
sink cannot reverse a previously saturated source or sink boundary arc.
Applied to original-unit source arcs and old-request baseline sink arcs,
this preserves both identities and baseline coverage through fee swaps. -/
theorem boundary_reverse_exclusion
    {Vertex Edge : Type} (tail head : Edge → Vertex) (reverse : Edge → Edge)
    (reverse_head : ∀ e, head (reverse e) = tail e)
    (reverse_tail : ∀ e, tail (reverse e) = head e)
    (source sink : Vertex) (onPath : Edge → Prop)
    (no_return : ∀ e, onPath e → head e ≠ source)
    (no_depart : ∀ e, onPath e → tail e ≠ sink)
    (e : Edge) (boundary : tail e = source ∨ head e = sink) :
    ¬ onPath (reverse e) := by
  intro used
  cases boundary with
  | inl hs => exact no_return (reverse e) used ((reverse_head e).trans hs)
  | inr ht => exact no_depart (reverse e) used ((reverse_tail e).trans ht)

end SubQuorum.SharedPrefixBridgeFlow

#print axioms SubQuorum.SharedPrefixBridgeFlow.redundant_bridge_slots_absorbed
#print axioms SubQuorum.SharedPrefixBridgeFlow.boundary_reverse_exclusion
