-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- New concrete board and arbitrary-length row assignment are independently checked here.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.ActiveShortTailMerger

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

def selected : List Point := [(1, 8), (1, 13), (1, 14), (2, 1), (2, 3), (2, 7), (2, 10), (2, 15), (3, 4), (3, 9), (3, 16), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14), (5, 16), (7, 16), (8, 1), (9, 4), (9, 12), (10, 6), (10, 11), (11, 7), (11, 9)]

def matching : List (Point × Point) := [
  ((2, 8), (2, 9)),
  ((3, 1), (4, 1)),
  ((3, 2), (3, 3)),
  ((3, 15), (4, 15)),
  ((4, 2), (5, 2)),
  ((5, 1), (6, 1)),
  ((5, 6), (6, 6)),
  ((5, 7), (5, 8)),
  ((5, 9), (6, 9)),
  ((5, 10), (5, 11)),
  ((5, 12), (6, 12)),
  ((5, 15), (6, 15)),
  ((6, 2), (6, 3)),
  ((6, 4), (6, 5)),
  ((6, 7), (7, 7)),
  ((6, 8), (7, 8)),
  ((6, 11), (7, 11)),
  ((6, 13), (6, 14)),
  ((7, 1), (7, 2)),
  ((7, 3), (7, 4)),
  ((7, 5), (7, 6)),
  ((7, 9), (8, 9)),
  ((7, 10), (8, 10)),
  ((7, 12), (7, 13)),
  ((7, 14), (7, 15)),
  ((8, 4), (8, 5)),
  ((8, 6), (8, 7)),
  ((8, 8), (9, 8)),
  ((8, 11), (8, 12)),
  ((9, 9), (10, 9)),
  ((10, 7), (10, 8))]

structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def witnesses : List Witness := [
  ⟨(2, 8), 0, (1, 8), (2, 7)⟩,
  ⟨(2, 9), 0, (2, 10), (3, 9)⟩,
  ⟨(3, 1), 1, (2, 1), (3, 2)⟩,
  ⟨(3, 2), 15, (3, 1), (4, 2)⟩,
  ⟨(3, 3), 0, (2, 3), (3, 4)⟩,
  ⟨(3, 15), 0, (2, 15), (3, 16)⟩,
  ⟨(4, 1), 14, (4, 2), (5, 1)⟩,
  ⟨(4, 2), 2, (3, 2), (4, 1)⟩,
  ⟨(4, 15), 13, (4, 14), (5, 15)⟩,
  ⟨(5, 1), 3, (4, 1), (5, 2)⟩,
  ⟨(5, 2), 13, (5, 1), (6, 2)⟩,
  ⟨(5, 6), 6, (4, 6), (5, 7)⟩,
  ⟨(5, 7), 10, (5, 6), (6, 7)⟩,
  ⟨(5, 8), 5, (4, 8), (6, 8)⟩,
  ⟨(5, 9), 11, (5, 8), (5, 10)⟩,
  ⟨(5, 10), 6, (4, 10), (5, 9)⟩,
  ⟨(5, 11), 7, (5, 12), (6, 11)⟩,
  ⟨(5, 12), 7, (4, 12), (5, 11)⟩,
  ⟨(5, 15), 1, (4, 15), (5, 16)⟩,
  ⟨(6, 1), 12, (6, 2), (7, 1)⟩,
  ⟨(6, 2), 4, (5, 2), (6, 1)⟩,
  ⟨(6, 3), 10, (6, 4), (7, 3)⟩,
  ⟨(6, 4), 6, (6, 3), (7, 4)⟩,
  ⟨(6, 5), 8, (6, 6), (7, 5)⟩,
  ⟨(6, 6), 8, (6, 5), (7, 6)⟩,
  ⟨(6, 7), 6, (5, 7), (6, 8)⟩,
  ⟨(6, 8), 11, (5, 8), (6, 7)⟩,
  ⟨(6, 9), 5, (6, 8), (7, 9)⟩,
  ⟨(6, 11), 8, (5, 11), (6, 12)⟩,
  ⟨(6, 12), 5, (6, 13), (7, 12)⟩,
  ⟨(6, 13), 10, (6, 12), (7, 13)⟩,
  ⟨(6, 14), 3, (6, 15), (7, 14)⟩,
  ⟨(6, 15), 12, (6, 14), (7, 15)⟩,
  ⟨(7, 1), 4, (6, 1), (8, 1)⟩,
  ⟨(7, 2), 11, (6, 2), (7, 3)⟩,
  ⟨(7, 3), 5, (6, 3), (7, 2)⟩,
  ⟨(7, 4), 9, (6, 4), (7, 5)⟩,
  ⟨(7, 5), 7, (6, 5), (7, 4)⟩,
  ⟨(7, 6), 7, (6, 6), (7, 7)⟩,
  ⟨(7, 7), 9, (7, 6), (8, 7)⟩,
  ⟨(7, 8), 4, (7, 9), (8, 8)⟩,
  ⟨(7, 9), 12, (6, 9), (7, 8)⟩,
  ⟨(7, 10), 9, (7, 9), (7, 11)⟩,
  ⟨(7, 11), 6, (7, 12), (8, 11)⟩,
  ⟨(7, 12), 9, (6, 12), (7, 11)⟩,
  ⟨(7, 13), 4, (6, 13), (7, 14)⟩,
  ⟨(7, 14), 11, (6, 14), (7, 13)⟩,
  ⟨(7, 15), 2, (6, 15), (7, 16)⟩,
  ⟨(8, 4), 6, (7, 4), (9, 4)⟩,
  ⟨(8, 5), 8, (7, 5), (8, 6)⟩,
  ⟨(8, 6), 8, (7, 6), (8, 5)⟩,
  ⟨(8, 7), 7, (7, 7), (8, 8)⟩,
  ⟨(8, 8), 12, (7, 8), (8, 7)⟩,
  ⟨(8, 9), 3, (8, 8), (9, 9)⟩,
  ⟨(8, 10), 13, (8, 9), (8, 11)⟩,
  ⟨(8, 11), 10, (7, 11), (8, 10)⟩,
  ⟨(8, 12), 5, (7, 12), (9, 12)⟩,
  ⟨(9, 8), 2, (9, 9), (10, 8)⟩,
  ⟨(9, 9), 13, (8, 9), (9, 8)⟩,
  ⟨(10, 7), 0, (10, 6), (11, 7)⟩,
  ⟨(10, 8), 14, (9, 8), (10, 9)⟩,
  ⟨(10, 9), 1, (10, 8), (11, 9)⟩]

def endpoints : List Point := matching.flatMap fun e => [e.1, e.2]

def lookupMate (v : Point) : List (Point × Point) → Point
  | [] => v
  | (a, b) :: rest => if v = a then b else if v = b then a else lookupMate v rest

def mate (v : Point) : Point := lookupMate v matching

def record (v : Point) : Witness :=
  (witnesses.find? fun w => w.point == v).getD default

def rank (v : Point) : Nat := (record v).rank

def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a ≠ b ∧ adjacent v a ∧ adjacent v b ∧
    (a ∈ selected ∨ (a ∈ endpoints ∧ rank (mate a) < rank v)) ∧
    (b ∈ selected ∨ (b ∈ endpoints ∧ rank (mate b) < rank v))

instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_ ≠ _ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem geometry_valid :
    endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1 < 14 ∧ v.2 < 18) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

/-- All 62 endpoints of the concrete physical configuration really freeze.
    This is derived from the inductive process, not an assumed rank axiom. -/
theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
      Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

theorem concrete_sizes : selected.length = 25 ∧ matching.length = 31 ∧
    endpoints.length = 62 := by decide


def alpha_left : List Point := [(5, 6), (6, 6), (7, 6), (7, 5), (6, 5), (6, 4), (7, 4), (7, 3), (6, 3), (6, 2), (7, 2), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1)]

def alpha_right : List Point := [(5, 12), (6, 12), (7, 12), (7, 13), (6, 13), (6, 14), (7, 14), (7, 15), (6, 15), (5, 15), (4, 15), (3, 15)]

def mixed_gate : List Point := [(5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9)]

def verticalPartner (v : Point) : Point :=
  if v.1 % 2 = 0 then (v.1+1,v.2) else (v.1-1,v.2)

def alternating : Bool → List Point → Prop
  | _, [] => True
  | _, [_] => True
  | useMatching, a :: b :: rest =>
    (if useMatching then mate a=b else verticalPartner a=b) ∧ alternating (!useMatching) (b::rest)

instance (useMatching : Bool) (path : List Point) : Decidable (alternating useMatching path) :=
  match path with
  | [] => isTrue True.intro
  | [_] => isTrue True.intro
  | _ :: b :: rest =>
    have := instDecidableAlternating (!useMatching) (b::rest)
    inferInstanceAs (Decidable ((_ : Prop) ∧ alternating (!useMatching) (b::rest)))

def tp (v : Point) : Prop := v∈endpoints ∧ verticalPartner v∈selected
def bp (v : Point) : Prop := v∈endpoints ∧ verticalPartner v∉selected ∧ verticalPartner v∉endpoints
instance (v : Point) : Decidable (tp v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bp v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem concrete_distinct_sources_and_gate :
    alternating true alpha_left ∧ alternating true alpha_right ∧
    alternating true mixed_gate ∧ alpha_left.Nodup ∧ alpha_right.Nodup ∧
    mixed_gate.Nodup ∧
    (∀ v∈alpha_left, v∈endpoints ∧ v∉alpha_right ∧ v∉mixed_gate) ∧
    (∀ v∈alpha_right, v∈endpoints ∧ v∉mixed_gate) ∧
    (∀ v∈mixed_gate, v∈endpoints) ∧
    tp (5,6) ∧ tp (3,1) ∧ tp (5,12) ∧ tp (3,15) ∧
    bp (5,9) ∧ tp (10,9) := by decide

theorem concrete_short_tail_merger :
    bp (5,7) ∧ tp (5,8) ∧ mate (5,7)=(5,8) ∧
    tp (5,10) ∧ bp (5,11) ∧ mate (5,11)=(5,10) ∧
    adjacent (5,6) (5,7) ∧ adjacent (5,8) (5,9) ∧
    adjacent (5,12) (5,11) ∧ adjacent (5,10) (5,9) ∧
    mate (5,9)=(6,9) := by decide

def blank (v : Point) : Prop := v∉endpoints ∧ v∉selected
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))

theorem concrete_two_distinct_gap_units :
    blank (10,10) ∧ blank (11,10) ∧
    (10,11)∈selected ∧ blank (11,11) ∧
    blank (10,12) ∧ blank (11,12) := by decide

/-- The retained escape is an actual PP/M two-point cycle; both adjacent
    columns in its band are PP, so there is no adjacent endpoint-free gap. -/
theorem concrete_sealed_retained_escape :
    mate (6,8)=(7,8) ∧ mate (7,8)=(6,8) ∧
    verticalPartner (6,8)=(7,8) ∧ verticalPartner (7,8)=(6,8) ∧
    rank (mate (6,8)) < rank (6,9) ∧ adjacent (6,9) (6,8) ∧
    (6,7)∈endpoints ∧ (7,7)∈endpoints ∧
    (6,9)∈endpoints ∧ (7,9)∈endpoints := by decide

/-- A shared physical BP remains a single entrance regardless of the
    number of different resources beyond it. -/
theorem cannot_use_both_links {V : Type} (u w v : V) (distinct : u≠w)
    (C : List (V × V))
    (targets : ∀ e∈C, ∀ f∈C, e.2=f.2 → e=f)
    (left : (u,v)∈C) (right : (w,v)∈C) : False := by
  have eq := targets (u,v) left (w,v) right rfl
  exact distinct (congrArg Prod.fst eq)

/-- In q separated five-owner restricted gadgets, each common entrance
    admits at most one unit. Combined with the one-route-per-copy witnesses,
    this elementary ledger gives deficit q and exact cost 2q. -/
theorem separated_bottleneck_ledger (q paid : Nat)
    (upper : paid≤q) (witnesses : q≤paid) :
    paid=q ∧ 2*q-paid=q ∧ 2*paid=2*q := by omega

#print axioms geometry_valid
#print axioms all_endpoints_frozen
#print axioms concrete_sizes
#print axioms concrete_distinct_sources_and_gate
#print axioms concrete_short_tail_merger
#print axioms concrete_two_distinct_gap_units
#print axioms concrete_sealed_retained_escape
#print axioms cannot_use_both_links
#print axioms separated_bottleneck_ledger

end SubQuorum.ActiveShortTailMerger
