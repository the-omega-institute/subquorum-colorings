import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SharedPocketJointDeficit

/-- The input edge is an actual pair of endpoints, not an independent name
chosen anew for each source. Parallel edges can have different identifiers. -/
def Incident {V E : Type} (ends : E → V × V) (e : E) (v w : V) : Prop :=
  (ends e=(v,w)) ∨ (ends e=(w,v))

/-- The key simultaneous resource check in a multi-source BFS forest:
two different vertices cannot spend the same parent edge. The strict
distance assumption is supplied by the written BFS construction. -/
theorem descending_parent_edges_injective {V E : Type}
    (ends : E → V × V) (distance : V → Nat)
    (parent : V → V) (edge : V → E) (active : V → Prop)
    (inc : ∀ v, active v → Incident ends (edge v) v (parent v))
    (desc : ∀ v, active v → distance (parent v)<distance v) :
    ∀ u v, active u → active v → edge u=edge v → u=v := by
  intro u v hu hv same
  have iu := inc u hu
  have iv := inc v hv
  rw [same] at iu
  rcases iu with iu | iu <;> rcases iv with iv | iv
  · exact congrArg Prod.fst (iu.symm.trans iv)
  · have h := iu.symm.trans iv
    have h₁ : u=parent v := congrArg Prod.fst h
    have h₂ : parent u=v := congrArg Prod.snd h
    have e₁ := congrArg distance h₁
    have e₂ := congrArg distance h₂
    have du := desc u hu
    have dv := desc v hv
    omega
  · have h := iu.symm.trans iv
    have h₁ : parent u=v := congrArg Prod.fst h
    have h₂ : u=parent v := congrArg Prod.snd h
    have e₁ := congrArg distance h₁
    have e₂ := congrArg distance h₂
    have du := desc u hu
    have dv := desc v hv
    omega
  · exact congrArg Prod.snd (iu.symm.trans iv)

/-- Tagged original interval units and whole-beta units cannot alias. -/
theorem original_and_beta_resources_distinct {I B : Type} (i : I) (b : B) :
    (Sum.inl i : Sum I B)≠Sum.inr b := by
  intro h
  cases h

/-- An injective resource identity cannot be repaired by merely giving the
same edge different endpoint names. Empty pockets really have TWO interval
identities; their endpoint-indexed assignments are therefore distinct. -/
theorem empty_pocket_slots_distinct {E : Type} (e : E) :
    (e,false)≠(e,true) := by
  intro h
  have h' := congrArg Prod.snd h
  cases h'

/-- Explicit counting consequence, conditional on the graph theorem's
component allocation and zero-link lower bound. It does not formalize BFS
existence, graph realization or the full geometric theorem. -/
theorem joint_value_and_cost (vertices trees freeCount value cost : Nat)
    (count : value+trees=vertices) (minimumCost : cost+freeCount=value) :
    value=vertices-trees ∧ cost=vertices-trees-freeCount := by
  omega

#print axioms descending_parent_edges_injective
#print axioms original_and_beta_resources_distinct
#print axioms empty_pocket_slots_distinct
#print axioms joint_value_and_cost

end SubQuorum.SharedPocketJointDeficit
