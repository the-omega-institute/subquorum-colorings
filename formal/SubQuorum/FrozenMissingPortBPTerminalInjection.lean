import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FrozenMissingPortBPTerminalInjection

theorem no_closed_freezing_dependency (rank : Nat → Nat) (blocked : Nat → Prop)
    (nonempty : ∃ vertex, blocked vertex)
    (needsEarlier : ∀ vertex, blocked vertex →
      ∃ predecessor, blocked predecessor ∧ rank predecessor < rank vertex) : False := by
  have excluded : ∀ height : Nat, ∀ vertex : Nat, rank vertex = height → ¬ blocked vertex := by
    intro height
    refine Nat.strongRecOn (motive := fun current =>
      ∀ vertex : Nat, rank vertex = current → ¬ blocked vertex) height ?_
    intro current inductionHypothesis vertex sameRank member
    obtain ⟨predecessor, predecessorMember, earlier⟩ := needsEarlier vertex member
    exact inductionHypothesis (rank predecessor) (by omega) predecessor rfl predecessorMember
  obtain ⟨vertex, member⟩ := nonempty
  exact excluded (rank vertex) vertex rfl member

theorem no_two_class_freezing_cycle (rank : Nat → Nat) (bp mateOfMissing : Nat → Prop)
    (nonempty : ∃ vertex, bp vertex ∨ mateOfMissing vertex)
    (bpNeedsMate : ∀ vertex, bp vertex →
      ∃ predecessor, mateOfMissing predecessor ∧ rank predecessor < rank vertex)
    (mateNeedsBP : ∀ vertex, mateOfMissing vertex →
      ∃ predecessor, bp predecessor ∧ rank predecessor < rank vertex) : False := by
  apply no_closed_freezing_dependency rank (fun vertex => bp vertex ∨ mateOfMissing vertex) nonempty
  intro vertex member
  rcases member with inBP | inMate
  · obtain ⟨predecessor, member, earlier⟩ := bpNeedsMate vertex inBP
    exact ⟨predecessor, Or.inr member, earlier⟩
  · obtain ⟨predecessor, member, earlier⟩ := mateNeedsBP vertex inMate
    exact ⟨predecessor, Or.inl member, earlier⟩

end SubQuorum.FrozenMissingPortBPTerminalInjection

#print axioms SubQuorum.FrozenMissingPortBPTerminalInjection.no_closed_freezing_dependency
#print axioms SubQuorum.FrozenMissingPortBPTerminalInjection.no_two_class_freezing_cycle
