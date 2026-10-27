import Lean.Elab.Tactic.Omega

/-! Local switch completion for arbitrary labels, and exact conditional cut
arithmetic. The physical fragment adapter, global flow/min-cut theorem and
weighted optimization equivalence remain written, not end-to-end grid Lean. -/
set_option autoImplicit false
namespace SubQuorum.ContactFlowCut

def portCount {α : Type} [DecidableEq α] (k a b : α) : Nat :=
  (if a=k then 1 else 0)+(if b=k then 1 else 0)

theorem two_port_completion {α : Type} [DecidableEq α] (a b c d : α)
    (h : ∀ k, portCount k a b=portCount k c d) :
    (a=c ∧ b=d) ∨ (a=d ∧ b=c) := by
  by_cases hac : a=c
  · subst c
    by_cases hbd : b=d
    · exact Or.inl ⟨rfl,hbd⟩
    · have hh := h b
      simp [portCount, Ne.symm hbd] at hh
  · by_cases had : a=d
    · subst d
      by_cases hbc : b=c
      · exact Or.inr ⟨rfl,hbc⟩
      · have hh := h b
        simp [portCount, Ne.symm hbc] at hh
    · have hh := h a
      simp [portCount, Ne.symm hac, Ne.symm had] at hh

def bit (b : Bool) : Nat := if b then 1 else 0

theorem binary_completion (a b c d : Bool)
    (h : bit a+bit b=bit c+bit d) :
    (a=c ∧ b=d) ∨ (a=d ∧ b=c) := by
  cases a <;> cases b <;> cases c <;> cases d <;> simp_all [bit]

inductive Colour where
  | red | blue | unused
  deriving DecidableEq

theorem three_colour_partition (a b : Colour) :
    portCount .red a b+portCount .blue a b+portCount .unused a b=2 := by
  cases a <;> cases b <;> decide

theorem two_colour_completion (a b c d : Colour)
    (hr : portCount .red a b=portCount .red c d)
    (hb : portCount .blue a b=portCount .blue c d) :
    (a=c ∧ b=d) ∨ (a=d ∧ b=c) := by
  have hp := three_colour_partition a b
  have hq := three_colour_partition c d
  have hu : portCount .unused a b=portCount .unused c d := by omega
  apply two_port_completion
  intro k
  cases k with
  | red => exact hr
  | blue => exact hb
  | unused => exact hu

theorem optimal_TT_from_flow (bt f residual : Nat)
    (hf : f≤bt) (lower : bt-f≤residual) (decoded : residual≤bt-f) :
    residual+f=bt := by omega

theorem cut_deficit_identity (bt isolated untouched touched supply holes outgoing f : Int)
    (hbt : bt=isolated+untouched+touched)
    (hcut : f=untouched+(touched-supply)+holes+outgoing) :
    bt-f=isolated+supply-holes-outgoing := by omega

theorem star_cut_shortage (s delta : Nat) (hs : 1≤s)
    (cut_lower : s-1≤delta) (one_relay_upper : delta+1≤s) :
    delta+1=s := by omega

theorem greedy_cost_gap (L : Nat) :
    (L*L+12*L+80)-(10*L+78)=L*L+2*L+2 := by omega

theorem greedy_linear_bound (L : Nat) (lower : 4≤L) :
    10*L+78≤30*L := by omega

theorem greedy_ratio_bound (L K : Nat) (lower : 4≤L) (large : 30*K<L) :
    K*(10*L+78)<L*L+12*L+80 := by
  have h := greedy_linear_bound L lower
  have hL : 0<L := by omega
  calc
    K*(10*L+78)≤K*(30*L) := Nat.mul_le_mul_left K h
    _ = (30*K)*L := by rw [← Nat.mul_assoc, Nat.mul_comm K 30]
    _ < L*L := Nat.mul_lt_mul_of_pos_right large hL
    _ ≤ L*L+12*L+80 := by omega

theorem greedy_unbounded_ratio (K : Nat) :
    ∃ L : Nat, 4≤L ∧ (∃ n : Nat, L=2*n) ∧
      K*(10*L+78)<L*L+12*L+80 := by
  refine ⟨100*(K+1), by omega, ⟨50*(K+1), by omega⟩, ?_⟩
  exact greedy_ratio_bound _ K (by omega) (by omega)

end SubQuorum.ContactFlowCut
#print axioms SubQuorum.ContactFlowCut.two_port_completion
#print axioms SubQuorum.ContactFlowCut.binary_completion
#print axioms SubQuorum.ContactFlowCut.three_colour_partition
#print axioms SubQuorum.ContactFlowCut.two_colour_completion
#print axioms SubQuorum.ContactFlowCut.optimal_TT_from_flow
#print axioms SubQuorum.ContactFlowCut.cut_deficit_identity
#print axioms SubQuorum.ContactFlowCut.star_cut_shortage
#print axioms SubQuorum.ContactFlowCut.greedy_cost_gap
#print axioms SubQuorum.ContactFlowCut.greedy_linear_bound
#print axioms SubQuorum.ContactFlowCut.greedy_ratio_bound
#print axioms SubQuorum.ContactFlowCut.greedy_unbounded_ratio
