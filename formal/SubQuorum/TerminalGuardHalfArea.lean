import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- Terminal algebra and count aggregation. Graph-coordinate and chunk-gluing
   arguments are written proofs. No custom axioms or admitted proofs. -/
namespace SubQuorum.TerminalGuardHalfArea

def bit (N : Nat) (b : Bool) : Nat := if b then N else 0

theorem terminal_bound (N A B C L K : Nat) (x y u w h : Bool)
    (hx : x=true → A=N ∧ B=N)
    (hy : y=true → A=N ∧ C=N ∧ L=N)
    (hu : u=true → 2*N ≤ A+B+C)
    (hw : w=true → N ≤ C+L)
    (hh : h=true → K=N ∧ L=N) :
    bit N x+bit N y+bit N u+bit N w+bit N h ≤ A+B+C+L+K := by
  cases x <;> cases y <;> cases u <;> cases w <;> cases h <;>
    simp_all [bit] <;> omega

theorem saturated_input_state (N A B C L K : Nat) (y u w h : Bool)
    (hN : 0<N) (hB : B=N)
    (hy : y=true → A=N ∧ C=N ∧ L=N)
    (hu : u=true → 2*N ≤ A+B+C)
    (hw : w=true → N ≤ C+L)
    (hh : h=true → K=N ∧ L=N)
    (heq : A+B+C+L+K=bit N y+bit N u+bit N w+bit N h) :
    y=false ∧ u=true ∧ w=true ∧ h=false ∧ A=0 ∧ C=N ∧ L=0 ∧ K=0 := by
  cases y <;> cases u <;> cases w <;> cases h <;>
    simp_all [bit] <;> omega

theorem whole_board_bound (m J L pairs blocks e : Nat)
    (hL : L≤10) (hpairs : pairs≤2*m) (hb : blocks≤7*m) (he : e≤5)
    (hcolour : J=9*m+15+L+pairs+blocks+e) : J≤18*m+30 := by omega

theorem equality_capacities (m J L pairs blocks e : Nat)
    (hL : L≤10) (hpairs : pairs≤2*m) (hb : blocks≤7*m) (he : e≤5)
    (hcolour : J=9*m+15+L+pairs+blocks+e) (heq : J=18*m+30) :
    L=10 ∧ pairs=2*m ∧ blocks=7*m ∧ e=5 := by omega

theorem chunk_counts (m : Nat) (hm : 2≤m) :
    14+9*(m-1)+15=9*m+20 ∧ 4+9*(m-1)+15=9*m+10 ∧
    (9*m+20)+(9*m+10)=18*m+30 := by omega

theorem physical_token_budget (m J plus minus : Nat)
    (hJ : J≤18*m+30) (hcharge : plus+2*J=minus+37*m+60) :
    minus+m≤plus := by omega

theorem no_reserve_at_equality (m J plus minus : Nat)
    (hJ : J=18*m+30) (hcharge : plus+2*J=minus+37*m+60) :
    plus=minus+m := by omega

#print axioms terminal_bound
#print axioms saturated_input_state
#print axioms whole_board_bound
#print axioms equality_capacities
#print axioms chunk_counts
#print axioms physical_token_budget
#print axioms no_reserve_at_equality
end SubQuorum.TerminalGuardHalfArea
