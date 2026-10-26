-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- Universal mixed endpoint/selection weighted certificate and strict-rank exclusions.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.EndpointInvasionSharpStrips

/-- Endpoint freezing with two distinct retained neighbours. -/
inductive Frozen {V : Type} (P T : V → Prop) (mate : V → V) (adj : V → V → Prop) :
    V → Prop where
  | ss {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      T a → T b → Frozen P T mate adj v
  | sp {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      T a → P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v
  | ps {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) → T b → Frozen P T mate adj v
  | pp {v a b : V} : P v → a ≠ b → adj v a → adj v b →
      P a → Frozen P T mate adj (mate a) →
      P b → Frozen P T mate adj (mate b) → Frozen P T mate adj v

theorem Frozen.step {V : Type} {P T : V → Prop} {mate : V → V}
    {adj : V → V → Prop} {v a b : V} (pv : P v) (distinct : a ≠ b)
    (va : adj v a) (vb : adj v b)
    (ha : T a ∨ (P a ∧ Frozen P T mate adj (mate a)))
    (hb : T b ∨ (P b ∧ Frozen P T mate adj (mate b))) : Frozen P T mate adj v := by
  rcases ha with ta | ⟨pa, fa⟩
  · rcases hb with tb | ⟨pb, fb⟩
    · exact Frozen.ss pv distinct va vb ta tb
    · exact Frozen.sp pv distinct va vb ta pb fb
  · rcases hb with tb | ⟨pb, fb⟩
    · exact Frozen.ps pv distinct va vb pa fa tb
    · exact Frozen.pp pv distinct va vb pa fa pb fb

/-- Strict ranks certify the actual inductive freezing process. -/
theorem strict_rank_complete {V : Type} (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (rank : V → Nat)
    (closed : ∀ v, P v → P (mate v))
    (certificate : ∀ v, P v → ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ rank (mate a) < rank v)) ∧
      (T b ∨ (P b ∧ rank (mate b) < rank v))) :
    ∀ v, P v → Frozen P T mate adj v := by
  have complete : ∀ n, ∀ v, rank v = n → P v → Frozen P T mate adj v := by
    intro n
    induction n using Nat.strongRecOn with
    | ind n ih =>
      intro v hv pv
      obtain ⟨a, b, distinct, va, vb, ha, hb⟩ := certificate v pv
      apply Frozen.step pv distinct va vb
      · rcases ha with selected | ⟨endpoint, lower⟩
        · exact Or.inl selected
        · exact Or.inr ⟨endpoint, ih (rank (mate a)) (by omega) (mate a) rfl
            (closed a endpoint)⟩
      · rcases hb with selected | ⟨endpoint, lower⟩
        · exact Or.inl selected
        · exact Or.inr ⟨endpoint, ih (rank (mate b)) (by omega) (mate b) rfl
            (closed b endpoint)⟩
  intro v pv
  exact complete (rank v) v rfl pv

abbrev Point := Nat × Nat

def adjacent (a b : Point) : Prop :=
  (a.1 = b.1 ∧ (a.2 + 1 = b.2 ∨ b.2 + 1 = a.2)) ∨
  (a.2 = b.2 ∧ (a.1 + 1 = b.1 ∨ b.1 + 1 = a.1))
instance (a b : Point) : Decidable (adjacent a b) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))


def Feasible (P T : Point → Prop) : Prop :=
  (∀ v, P v → ¬T v) ∧
  (∀ v a b, T v → adjacent v a → adjacent v b →
    (P a ∨ T a) → (P b ∨ T b) → a=b)

/-- A selected centre cannot have two distinct occupied neighbours. -/
theorem feasible_wedge {P T : Point → Prop} [DecidablePred P] [DecidablePred T]
    (h : Feasible P T) (v a b : Point) (ha : adjacent v a)
    (hb : adjacent v b) (distinct : a ≠ b) :
    (if T v then 1 else 0) + (if P a ∨ T a then 1 else 0) +
      (if P b ∨ T b then 1 else 0) ≤ (2 : Nat) := by
  by_cases hv : T v
  · have noBoth : ¬ ((P a ∨ T a) ∧ (P b ∨ T b)) := by
      intro ⟨oa, ob⟩
      exact distinct (h.2 v a b hv ha hb oa ob)
    by_cases oa : P a ∨ T a <;> by_cases ob : P b ∨ T b <;> simp_all
  · by_cases oa : P a ∨ T a <;> by_cases ob : P b ∨ T b <;> simp_all

/-- A strict witness cannot be the endpoint's own mate. -/
theorem strict_witness_not_mate {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (v w : V) (inv : mate (mate v) = v)
    (pm : P (mate v)) (disjoint : ∀ u, P u → ¬T u)
    (witness : T w ∨ (P w ∧ rank (mate w) < rank v)) : w ≠ mate v := by
  intro eq
  subst w
  rcases witness with selected | ⟨_, lower⟩
  · exact disjoint (mate v) pm selected
  · rw [inv] at lower
    omega

/-- Mate plus at most one other occupied neighbour cannot supply strict witnesses. -/
theorem mate_plus_one_exclusion {V : Type} (P T : V → Prop) (mate : V → V)
    (rank : V → Nat) (adj : V → V → Prop) (v p : V)
    (inv : mate (mate v) = v) (pm : P (mate v))
    (disjoint : ∀ u, P u → ¬T u)
    (only : ∀ u, adj v u → (P u ∨ T u) → u = mate v ∨ u = p) :
    ¬ ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧
      (T a ∨ (P a ∧ rank (mate a) < rank v)) ∧
      (T b ∨ (P b ∧ rank (mate b) < rank v)) := by
  rintro ⟨a,b,distinct,ha,hb,wa,wb⟩
  have na := strict_witness_not_mate P T mate rank v a inv pm disjoint wa
  have nb := strict_witness_not_mate P T mate rank v b inv pm disjoint wb
  have oa : P a ∨ T a := by
    rcases wa with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have ob : P b ∨ T b := by
    rcases wb with ht | ⟨hp,_⟩
    · exact Or.inr ht
    · exact Or.inl hp
  have ap : a = p := (only a ha oa).resolve_left na
  have bp : b = p := (only b hb ob).resolve_left nb
  exact distinct (ap.trans bp.symm)

def pocketPoints : List Point := [(2,3), (2,5), (3,3), (3,4), (3,5), (4,0), (4,2), (4,3), (4,4), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5)]
def pocketEdges : List (Nat × Nat) := [(0,2), (1,4), (2,3), (2,7), (3,4), (3,8), (5,9), (6,7), (6,11), (7,8), (7,12), (8,13), (9,10), (10,11), (11,12), (12,13), (13,14)]
theorem pocket_edge_geometry :
    pocketEdges.all (fun e => decide (adjacent (pocketPoints[e.1]!) (pocketPoints[e.2]!))) = true := by
  decide

/-- Occupancy is selection plus incidence of NEW matching edges; old endpoints
    are outside this pocket. Actual matchings make these values indicators. -/
def occ (t m : Nat → Nat) : Nat → Nat
  | 0 => t 0 + m 0
  | 1 => t 1 + m 1
  | 2 => t 2 + m 0 + m 2 + m 3
  | 3 => t 3 + m 2 + m 4 + m 5
  | 4 => t 4 + m 1 + m 4
  | 5 => t 5 + m 6
  | 6 => t 6 + m 7 + m 8
  | 7 => t 7 + m 3 + m 7 + m 9 + m 10
  | 8 => t 8 + m 5 + m 9 + m 11
  | 9 => t 9 + m 6 + m 12
  | 10 => t 10 + m 12 + m 13
  | 11 => t 11 + m 8 + m 13 + m 14
  | 12 => t 12 + m 10 + m 14 + m 15
  | 13 => t 13 + m 11 + m 15 + m 16
  | 14 => t 14 + m 16
  | _ => 0

def sumT (t : Nat → Nat) : Nat := t 0 + t 1 + t 2 + t 3 + t 4 + t 5 + t 6 + t 7 + t 8 + t 9 + t 10 + t 11 + t 12 + t 13 + t 14
def sumM (m : Nat → Nat) : Nat := m 0 + m 1 + m 2 + m 3 + m 4 + m 5 + m 6 + m 7 + m 8 + m 9 + m 10 + m 11 + m 12 + m 13 + m 14 + m 15 + m 16
def costly (m : Nat → Nat) : Nat := m 3 + m 9 + m 10 + m 13 + m 14
def weightedLHS (t m : Nat → Nat) : Nat := 3*t 0 + 3*t 1 +
  2*(t 3+occ t m 2+occ t m 4) +
  1*(t 3+occ t m 4+occ t m 8) +
  2*(t 6+occ t m 7+occ t m 11) +
  1*(t 7+occ t m 2+occ t m 8) +
  3*(t 9+occ t m 5+occ t m 10) +
  1*(t 11+occ t m 6+occ t m 12) +
  1*(t 13+occ t m 8+occ t m 14) +
  2*(t 13+occ t m 12+occ t m 14)

/-- Each selected site has coefficient three. Each actual new edge has
    coefficient three or five, never an unaccounted reuse of an endpoint. -/
theorem weighted_identity (t m : Nat → Nat) :
    weightedLHS t m = 3*sumT t + 3*sumM m + 2*costly m := by
  simp only [weightedLHS, occ, sumT, sumM, costly]
  omega

theorem pocket_bound (t m : Nat → Nat) (cap : t 0 ≤ 1) (blocked : t 1 = 0)
    (h0 : t 3+occ t m 2+occ t m 4 ≤ 2)
    (h1 : t 3+occ t m 4+occ t m 8 ≤ 2)
    (h2 : t 6+occ t m 7+occ t m 11 ≤ 2)
    (h3 : t 7+occ t m 2+occ t m 8 ≤ 2)
    (h4 : t 9+occ t m 5+occ t m 10 ≤ 2)
    (h5 : t 11+occ t m 6+occ t m 12 ≤ 2)
    (h6 : t 13+occ t m 8+occ t m 14 ≤ 2)
    (h7 : t 13+occ t m 12+occ t m 14 ≤ 2)
    : sumT t + sumM m ≤ 9 := by
  have hb : weightedLHS t m ≤ 29 := by
    unfold weightedLHS
    omega
  have hi := weighted_identity t m
  omega

/-- Repeated gate: upper site is forbidden, and matching excludes lower T. -/
theorem gate_bound (top low edges : Nat) (ht : top = 0)
    (hl : low+edges ≤ 1) : top+low+edges ≤ 1 := by omega

/-- One star has at most one edge. With that edge at most two leaves remain;
    with its centre selected at most one leaf may be selected. -/
theorem star_bound (centre leaves edges : Nat) (hc : centre+edges ≤ 1)
    (hl : leaves ≤ 3) (hm : edges=1 → leaves ≤ 2)
    (hs : centre=1 → leaves ≤ 1) : centre+leaves+edges ≤ 3 := by
  by_cases he : edges=1
  · have h := hm he
    omega
  · by_cases ht : centre=1
    · have h := hs ht
      omega
    · omega

/-- Component capacities aggregate once each, for every parameter k>=1. -/
theorem global_count (k pocket gates stars isolated extra : Nat)
    (hk : 1 ≤ k) (hp : pocket ≤ 9) (hg : gates ≤ k-1)
    (hs : stars ≤ 3*(k-1)) (hi : isolated ≤ k+1)
    (partition : extra=pocket+gates+stars+isolated) : extra ≤ 5*k+6 := by omega

theorem whole_surplus (k extra total : Nat) (bound : extra ≤ 5*k+6)
    (oldCount : total=12*k+6+extra) : total+k ≤ 18*k+12 := by omega

#print axioms feasible_wedge
#print axioms strict_witness_not_mate
#print axioms mate_plus_one_exclusion
#print axioms pocket_edge_geometry
#print axioms weighted_identity
#print axioms pocket_bound
#print axioms gate_bound
#print axioms star_bound
#print axioms global_count
#print axioms whole_surplus

end SubQuorum.EndpointInvasionSharpStrips
