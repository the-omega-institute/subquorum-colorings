import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

/- Generic strict-rank induction and all-length certificate arithmetic.
   The coordinate/matching adapter is a written proof with independent checks. -/
namespace SubQuorum.FrozenHalfAreaAttainers
universe u

def Supported {V : Type u} (Adj : V → V → Prop) (T P F : V → Prop)
    (mate : V → V) (v : V) : Prop :=
  ∃ a b, a≠b ∧ Adj v a ∧ Adj v b ∧
    (T a ∨ P a ∧ F (mate a)) ∧ (T b ∨ P b ∧ F (mate b))

def RankSupported {V : Type u} (Adj : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (rank : V → Nat) (v : V) : Prop :=
  ∃ a b, a≠b ∧ Adj v a ∧ Adj v b ∧
    (T a ∨ P a ∧ rank (mate a)<rank v) ∧
    (T b ∨ P b ∧ rank (mate b)<rank v)

/-- Every endpoint lies in every freezing-closed set, by strict rank induction. -/
theorem rank_forces_closed {V : Type u} (Adj : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (rank : V → Nat)
    (hmate : ∀ v, P v → P (mate v))
    (hcert : ∀ v, P v → RankSupported Adj T P mate rank v)
    (F : V → Prop)
    (hclosed : ∀ v, P v → Supported Adj T P F mate v → F v) :
    ∀ v, P v → F v := by
  have aux : ∀ n v, rank v=n → P v → F v := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v heq hp
      obtain ⟨a,b,hab,hva,hvb,ha,hb⟩ := hcert v hp
      apply hclosed v hp
      refine ⟨a,b,hab,hva,hvb,?_,?_⟩
      · rcases ha with ht | ⟨hpa,hr⟩
        · exact Or.inl ht
        · exact Or.inr ⟨hpa, ih (rank (mate a)) (by omega) (mate a) rfl (hmate a hpa)⟩
      · rcases hb with ht | ⟨hpb,hr⟩
        · exact Or.inl ht
        · exact Or.inr ⟨hpb, ih (rank (mate b)) (by omega) (mate b) rfl (hmate b hpb)⟩
  intro v hp
  exact aux (rank v) v rfl hp

/-- Least freezing closure, expressed as the intersection of closed predicates. -/
def Frozen {V : Type u} (Adj : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (v : V) : Prop :=
  ∀ F : V → Prop,
    (∀ w, P w → Supported Adj T P F mate w → F w) → F v

theorem certificate_implies_frozen {V : Type u}
    (Adj : V → V → Prop) (T P : V → Prop) (mate : V → V) (rank : V → Nat)
    (hmate : ∀ v, P v → P (mate v))
    (hcert : ∀ v, P v → RankSupported Adj T P mate rank v) :
    ∀ v, P v → Frozen Adj T P mate v := by
  intro v hp F hc
  exact rank_forces_closed Adj T P mate rank hmate hcert F hc v hp

/-- A set with no possible pair of outside-mate/selected witnesses is excluded
    from the least freezing closure. This covers the terminal singleton,
    two-endpoint, three-endpoint and four-endpoint traps in the written proof. -/
theorem trap_excludes_frozen {V : Type u}
    (Adj : V → V → Prop) (T P S : V → Prop) (mate : V → V)
    (htrap : ∀ v, P v → S v →
      ¬ Supported Adj T P (fun w => ¬ S w) mate v) :
    ∀ v, P v → S v → ¬ Frozen Adj T P mate v := by
  intro v hp hs hf
  have closed : ∀ w, P w →
      Supported Adj T P (fun z => ¬ S z) mate w → ¬ S w := by
    intro w hw hsup hsw
    exact htrap w hw hsw hsup
  exact (hf (fun w => ¬ S w) closed) hs

def n (m : Nat) : Nat := 3*m+2
def h (m j : Nat) : Nat := n m+1+6*(m-j)
def blackRank (m l : Nat) : Nat := n m+3-l
def bridgeRank (m i : Nat) : Nat := n m+6*(m-i)

theorem early_ranks : 0<1 ∧ 0<2 ∧ 1<2 ∧ 2<3 ∧ 3<4 ∧ 1<4 := by omega

theorem lower_white_step (m l : Nat) (hl : 0<l) (_hb : l<n m) :
    l-1<l := by omega

theorem lower_white_terminal (m : Nat) : n m-1<n m := by unfold n; omega

theorem lower_black_early (m l : Nat) (hl : l<n m) :
    3<blackRank m l := by unfold blackRank; omega

theorem lower_black_step (m l : Nat) (hl : l+1<n m) :
    blackRank m (l+1)<blackRank m l := by unfold blackRank; omega

theorem lower_black_terminal (m : Nat) : blackRank m (n m-1)=4 := by
  unfold blackRank n
  omega

theorem left_port_step (m : Nat) : 1<n m+4 ∧ blackRank m 0<n m+4 := by
  unfold blackRank n
  omega

theorem right_return_start (m : Nat) : n m<h m m := by unfold h; omega

theorem bridge_precedes_H (m j : Nat) (_hj : j<m) :
    bridgeRank m j+1=h m j := by unfold bridgeRank h; omega

theorem lower_whites_precede_H (m j : Nat) (hj : j≤m) :
    3*j<n m ∧ 3*j+1<n m ∧ 3*j+1<h m j := by unfold h n; omega

theorem return_core_steps (m j : Nat) :
    h m j<h m j+1 ∧ h m j<h m j+2 ∧ h m j+1<h m j+2 ∧
    h m j+2<h m j+3 ∧ h m j+1<h m j+3 ∧
    h m j+3<h m j+4 ∧ h m j+1<h m j+4 := by omega

theorem return_bridge_step (m i : Nat) (hi : i<m) :
    h m (i+1)+4+1=bridgeRank m i ∧
    3*i+2<n m ∧ 3*i+2<bridgeRank m i := by
  unfold h bridgeRank n
  omega

theorem old_core_white_max (m j : Nat) (hj : j≤m) :
    h m j+4≤9*m+7 := by unfold h n; omega

theorem last_white_rank (m : Nat) : h m 0+4=9*m+7 := by unfold h n; omega

theorem lower_and_port_rank_max (m l : Nat) (hl : l<n m) :
    l≤9*m+7 ∧ blackRank m l≤9*m+7 ∧ n m+4≤9*m+7 := by
  simp only [blackRank, n] at *
  omega

theorem bridge_rank_max (m i : Nat) (_hi : i<m) :
    bridgeRank m i≤9*m+7 := by unfold bridgeRank n; omega

theorem construction_counts (m : Nat) :
    (5*m+10)+7+(m+1)+(n m+1)=9*m+21 ∧
    (4*m+5)+(m+1)+m+1+n m=9*m+9 ∧
    (9*m+21)+(9*m+9)=18*m+30 := by unfold n; omega

theorem exact_token_budget (m plus minus : Nat)
    (hplus : plus=m+2) (hminus : minus=2) :
    plus=minus+m ∧ ¬(minus+m+1≤plus) := by omega

theorem full_tile_budget (m : Nat) : 1+2+m=(m+1)+1+1 := by omega

theorem terminal_port_frontier (m J epsilon : Nat)
    (he : epsilon≤1) (hupper : J≤18*m+30)
    (hport : J=18*m+30 → epsilon=1) :
    J≤18*m+29+epsilon := by
  by_cases hh : J=18*m+30
  · have hp := hport hh
    omega
  · omega

theorem terminal_port_token_budget (m J epsilon plus minus : Nat)
    (he : epsilon≤1) (hJ : J≤18*m+29+epsilon)
    (hcharge : plus+2*J=minus+37*m+60) :
    minus+m+2*(1-epsilon)≤plus := by omega

#print axioms rank_forces_closed
#print axioms certificate_implies_frozen
#print axioms trap_excludes_frozen
#print axioms early_ranks
#print axioms lower_white_step
#print axioms lower_white_terminal
#print axioms lower_black_early
#print axioms lower_black_step
#print axioms lower_black_terminal
#print axioms left_port_step
#print axioms right_return_start
#print axioms bridge_precedes_H
#print axioms lower_whites_precede_H
#print axioms return_core_steps
#print axioms return_bridge_step
#print axioms old_core_white_max
#print axioms last_white_rank
#print axioms lower_and_port_rank_max
#print axioms bridge_rank_max
#print axioms construction_counts
#print axioms exact_token_budget
#print axioms full_tile_budget
#print axioms terminal_port_frontier
#print axioms terminal_port_token_budget
end SubQuorum.FrozenHalfAreaAttainers
