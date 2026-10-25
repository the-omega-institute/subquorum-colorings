-- General freezing-preserving matched-edge ear insertion.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.FrozenEarRematching

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

/-- Four new endpoints and two selected guards. -/
inductive Vertex (V : Type) where
  | old : V → Vertex V
  | a | b | d | e | leftGuard | rightGuard

open Vertex

variable {V : Type} [DecidableEq V]

def newP (P : V → Prop) : Vertex V → Prop
  | old x => P x
  | a | b | d | e => True
  | _ => False

def newT (T : V → Prop) : Vertex V → Prop
  | old x => T x
  | leftGuard | rightGuard => True
  | _ => False

def newMate (mate : V → V) (u v : V) : Vertex V → Vertex V
  | old x => if x = u then a else if x = v then b else old (mate x)
  | a => old u
  | b => old v
  | d => e
  | e => d
  | leftGuard => leftGuard
  | rightGuard => rightGuard

def newRank (rank : V → Nat) (u v : V) : Vertex V → Nat
  | old x => 3 * rank x
  | a => 3 * rank v + 2
  | b => 3 * rank u + 2
  | d => 3 * rank u + 1
  | e => 3 * rank v + 1
  | _ => 0

/-- The graph contains the displayed ear and any retained old adjacency. -/
inductive NewAdj (adj : V → V → Prop) (u v : V) : Vertex V → Vertex V → Prop where
  | oldEdge {x y} : adj x y → NewAdj adj u v (old x) (old y)
  | ua : NewAdj adj u v (old u) a
  | au : NewAdj adj u v a (old u)
  | vb : NewAdj adj u v (old v) b
  | bv : NewAdj adj u v b (old v)
  | ab : NewAdj adj u v a b
  | ba : NewAdj adj u v b a
  | ad : NewAdj adj u v a d
  | da : NewAdj adj u v d a
  | be : NewAdj adj u v b e
  | eb : NewAdj adj u v e b
  | de : NewAdj adj u v d e
  | ed : NewAdj adj u v e d
  | dl : NewAdj adj u v d leftGuard
  | ld : NewAdj adj u v leftGuard d
  | er : NewAdj adj u v e rightGuard
  | re : NewAdj adj u v rightGuard e

abbrev Certificate {W : Type} (P T : W → Prop) (mate : W → W)
    (adj : W → W → Prop) (rank : W → Nat) : Prop :=
  ∀ x, P x → ∃ s t, s ≠ t ∧ adj x s ∧ adj x t ∧
    (T s ∨ (P s ∧ rank (mate s) < rank x)) ∧
    (T t ∨ (P t ∧ rank (mate t) < rank x))

/-- Old dependencies are delayed by at most two units after scaling by three. -/
theorem mate_rank_bound (mate : V → V) (rank : V → Nat) (u v : V)
    (hu : mate u = v) (hv : mate v = u) (x : V) :
    newRank rank u v (newMate mate u v (old x)) ≤ 3 * rank (mate x) + 2 := by
  by_cases xu : x = u
  · subst x
    simp [newMate, newRank, hu]
  · by_cases xv : x = v
    · subst x
      simp [newMate, newRank, xu, hv]
    · simp [newMate, newRank, xu, xv]

/-- An old retained witness remains retained at the scaled endpoint rank. -/
theorem lift_retained {P T : V → Prop} {mate : V → V} {rank : V → Nat}
    {u v x y : V} (hu : mate u = v) (hv : mate v = u)
    (h : T y ∨ (P y ∧ rank (mate y) < rank x)) :
    newT T (old y) ∨
      (newP P (old y) ∧ newRank rank u v (newMate mate u v (old y)) <
        newRank rank u v (old x)) := by
  rcases h with ty | ⟨py, lower⟩
  · exact Or.inl ty
  · have bound := mate_rank_bound mate rank u v hu hv y
    apply Or.inr
    refine ⟨py, ?_⟩
    change newRank rank u v (newMate mate u v (old y)) < 3 * rank x
    omega

/-- The displayed four-endpoint ear lifts every old strict freezing certificate. -/
theorem ear_lifts_certificate (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (rank : V → Nat) (u v : V)
    (hu : mate u = v) (hv : mate v = u)
    (certificate : Certificate P T mate adj rank) :
    Certificate (newP P) (newT T) (newMate mate u v)
      (NewAdj adj u v) (newRank rank u v) := by
  intro x px
  cases x with
  | old x =>
    obtain ⟨s, t, distinct, xs, xt, hs, ht⟩ := certificate x px
    refine ⟨old s, old t, ?_, NewAdj.oldEdge xs, NewAdj.oldEdge xt,
      lift_retained hu hv hs, lift_retained hu hv ht⟩
    intro eq
    cases eq
    exact distinct rfl
  | a =>
    refine ⟨b, d, (by intro h; cases h), NewAdj.ab, NewAdj.ad, ?_, ?_⟩
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
  | b =>
    refine ⟨a, e, (by intro h; cases h), NewAdj.ba, NewAdj.be, ?_, ?_⟩
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
  | d =>
    refine ⟨leftGuard, a, (by intro h; cases h), NewAdj.dl, NewAdj.da, ?_, ?_⟩
    · exact Or.inl True.intro
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
  | e =>
    refine ⟨rightGuard, b, (by intro h; cases h), NewAdj.er, NewAdj.eb, ?_, ?_⟩
    · exact Or.inl True.intro
    · exact Or.inr ⟨True.intro, by simp [newRank, newMate]⟩
  | leftGuard => exact False.elim px
  | rightGuard => exact False.elim px

theorem new_mate_closed (P : V → Prop) (mate : V → V) (u v : V)
    (pu : P u) (pv : P v) (closed : ∀ x, P x → P (mate x)) :
    ∀ x, newP P x → newP P (newMate mate u v x) := by
  intro x px
  cases x with
  | old x =>
    simp only [newMate]
    split
    · exact True.intro
    · split
      · exact True.intro
      · exact closed x px
  | a => exact pu
  | b => exact pv
  | d => exact True.intro
  | e => exact True.intro
  | leftGuard => exact False.elim px
  | rightGuard => exact False.elim px

/-- Complete freezing is preserved for arbitrary old graph size and ranks. -/
theorem ear_completely_frozen (P T : V → Prop) (mate : V → V)
    (adj : V → V → Prop) (rank : V → Nat) (u v : V)
    (pu : P u) (pv : P v) (hu : mate u = v) (hv : mate v = u)
    (closed : ∀ x, P x → P (mate x))
    (certificate : Certificate P T mate adj rank) :
    ∀ x, newP P x → Frozen (newP P) (newT T) (newMate mate u v) (NewAdj adj u v) x :=
  strict_rank_complete _ _ _ _ _
    (new_mate_closed P mate u v pu pv closed)
    (ear_lifts_certificate P T mate adj rank u v hu hv certificate)

/-- The enlarged mate function is a genuine involution. -/
theorem new_mate_involution (mate : V → V) (u v : V)
    (different : u ≠ v) (hu : mate u = v) (hv : mate v = u)
    (inv : ∀ x, mate (mate x) = x) :
    ∀ x, newMate mate u v (newMate mate u v x) = x := by
  intro x
  cases x with
  | old x =>
    by_cases xu : x = u
    · simp [newMate, xu]
    · by_cases xv : x = v
      · simp [newMate, xv, different.symm]
      · have mu : mate x ≠ u := by
          intro h
          have : x = v := by calc x = mate (mate x) := (inv x).symm
                                 _ = v := by rw [h, hu]
          exact xv this
        have mv : mate x ≠ v := by
          intro h
          have : x = u := by calc x = mate (mate x) := (inv x).symm
                                 _ = u := by rw [h, hv]
          exact xu this
        simp [newMate, xu, xv, mu, mv, inv]
  | a => simp [newMate]
  | b => simp [newMate, different.symm]
  | d => rfl
  | e => rfl
  | leftGuard => rfl
  | rightGuard => rfl

/-- This surgery consumes four old intervals rather than creating resource credit. -/
theorem ear_resource_ledger (I b k q h f : Int) :
    (I-4*h)+b-k = (I+b-k)-4*h ∧
    ((I-4*h)-(2*q-f))+(b-f)-(k-2*q) = (I+b-k)-4*h := by omega

#print axioms mate_rank_bound
#print axioms lift_retained
#print axioms ear_lifts_certificate
#print axioms new_mate_closed
#print axioms ear_completely_frozen
#print axioms new_mate_involution
#print axioms ear_resource_ledger

end SubQuorum.FrozenEarRematching
