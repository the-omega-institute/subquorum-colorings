import Lean.Elab.Tactic.Omega
import Init.Data.List.Perm

set_option autoImplicit false
namespace SubQuorum.FrozenSerialEscape

/-- The physical proof supplies the precise two-site retained-neighbour sets. -/
theorem two_witnesses_force_both {V : Type} (R : V → Prop) (x y : V)
    (two : ∃ a b, a ≠ b ∧ R a ∧ R b)
    (only : ∀ z, R z → z=x ∨ z=y) : R x ∧ R y := by
  obtain ⟨a,b,distinct,ha,hb⟩ := two
  rcases only a ha with ax | ay
  · subst a
    rcases only b hb with bx | byEq
    · exact False.elim (distinct bx.symm)
    · subst b; exact ⟨ha,hb⟩
  · subst a
    rcases only b hb with bx | byEq
    · subst b; exact ⟨hb,ha⟩
    · exact False.elim (distinct byEq.symm)

/-- These strict dependencies arise if the outer site were selected. -/
theorem selected_outer_rank_cycle (rankTipMate rankBeta : Nat)
    (betaNeedsTip : rankTipMate < rankBeta)
    (tipMateNeedsBeta : rankBeta < rankTipMate) : False := by omega

/-- A retained diagonal rules out vertical mating of the outer BP. -/
theorem outer_bp_vertical_rank_cycle (rankOuter rankTipMate : Nat)
    (diagonalRetained : rankOuter < rankTipMate)
    (outerNeedsTip : rankTipMate < rankOuter) : False := by omega

/-- Distinct vertical TP tips cannot choose the same outward-matched BP.
The coordinate proof supplies the opposite-neighbour hypothesis. -/
theorem outward_target_injective {V : Type} (target mate : V → V)
    (verticalTip : V → Prop)
    (oppositeNeighbour : ∀ a b, verticalTip a → verticalTip b →
      a ≠ b → target a = target b → mate (target a) = b)
    (notMatedToTip : ∀ a b, verticalTip a → verticalTip b →
      mate (target a) ≠ b) :
    ∀ a b, verticalTip a → verticalTip b → target a = target b → a=b := by
  intro a b ha hb same
  by_cases eq : a=b
  · exact eq
  · exact False.elim (notMatedToTip a b ha hb
      (oppositeNeighbour a b ha hb eq same))

/-- The inactive BP of a specified beta has the opposite phase. -/
theorem common_phase_excludes_inactive (targetColor activeColor inactiveColor : Bool)
    (targetPhase : targetColor=activeColor)
    (opposite : inactiveColor ≠ activeColor) :
    targetColor ≠ inactiveColor := by
  intro eq
  exact opposite (eq.symm.trans targetPhase)

/-- Actual original units have at most two forced-port users. -/
theorem serial_joint_deficit_bound (q b m h u r : Nat)
    (classes : q=b+m+h+u) (twoUsers : u≤2*r) :
    q-b-r ≤ m+h+u/2 := by omega

theorem full_with_distinct_ports (q b u r : Nat)
    (classes : q=b+u) (distinctPorts : r=u) : q-b-r=0 := by omega

/-- The boundary charge uses different ORIGINAL marked identities. -/
theorem marked_charge_bound {J : Type} (forced marks : List J)
    (distinct : forced.Nodup) (contained : forced ⊆ marks) :
    forced.length ≤ marks.length := distinct.length_le_of_subset contained

theorem serial_certificate_link_count (N q b : Nat) (nonempty : q≤N) :
    N+(N-q)+b=2*N-q+b := by omega

#print axioms two_witnesses_force_both
#print axioms selected_outer_rank_cycle
#print axioms outer_bp_vertical_rank_cycle
#print axioms outward_target_injective
#print axioms common_phase_excludes_inactive
#print axioms serial_joint_deficit_bound
#print axioms full_with_distinct_ports
#print axioms marked_charge_bound
#print axioms serial_certificate_link_count
end SubQuorum.FrozenSerialEscape
