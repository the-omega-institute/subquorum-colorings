-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- New concrete negative strip and geometric port-budget arithmetic are checked here.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.OccupiedStripDegreeFourBudget

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

def selected : List Point := [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 11), (0, 13), (0, 15), (1, 2), (1, 4), (1, 8), (1, 10), (1, 14), (2, 0), (3, 1), (3, 9), (3, 15), (4, 6), (4, 8), (4, 12), (4, 14)]

def matching : List (Point × Point) := [
  ((1, 5), (1, 6)),
  ((1, 7), (2, 7)),
  ((2, 6), (3, 6)),
  ((3, 7), (3, 8)),
  ((1, 11), (1, 12)),
  ((1, 13), (2, 13)),
  ((2, 12), (3, 12)),
  ((3, 13), (3, 14)),
  ((1, 1), (2, 1))]

def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def witnesses : List Witness := [
  ⟨(1, 5), 0, (0, 5), (1, 4)⟩,
  ⟨(1, 7), 0, (0, 7), (1, 8)⟩,
  ⟨(3, 8), 0, (4, 8), (3, 9)⟩,
  ⟨(2, 6), 1, (1, 6), (2, 7)⟩,
  ⟨(3, 6), 1, (4, 6), (3, 7)⟩,
  ⟨(2, 7), 2, (2, 6), (3, 7)⟩,
  ⟨(3, 7), 2, (3, 6), (2, 7)⟩,
  ⟨(1, 6), 3, (1, 7), (2, 6)⟩,
  ⟨(1, 11), 0, (0, 11), (1, 10)⟩,
  ⟨(1, 13), 0, (0, 13), (1, 14)⟩,
  ⟨(3, 14), 0, (4, 14), (3, 15)⟩,
  ⟨(2, 12), 1, (1, 12), (2, 13)⟩,
  ⟨(3, 12), 1, (4, 12), (3, 13)⟩,
  ⟨(2, 13), 2, (2, 12), (3, 13)⟩,
  ⟨(3, 13), 2, (3, 12), (2, 13)⟩,
  ⟨(1, 12), 3, (1, 13), (2, 12)⟩,
  ⟨(1, 1), 0, (0, 1), (1, 2)⟩,
  ⟨(2, 1), 0, (2, 0), (3, 1)⟩]

def lookupMate (v : Point) : List (Point × Point) → Point
  | [] => v
  | (a,b) :: rest => if v=a then b else if v=b then a else lookupMate v rest

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
    selected.Nodup ∧ endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1 < 6 ∧ v.2 < 16) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

/-- Actual inductive freezing of all 18 endpoints of the q=2 negative strip. -/
theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
      Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

def occupiedDegree (v : Point) : Nat :=
  ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length

theorem actual_degree_four :
    (∀ v ∈ endpoints, occupiedDegree v = 3 ∨ occupiedDegree v = 4) ∧
    (endpoints.filter fun v => occupiedDegree v == 4) = [(1,7),(1,13)] := by
  decide

def region : List Point := (List.range 2).flatMap fun r =>
  (List.range 16).map fun c => (r,c)

theorem concrete_negative_strip :
    region.length = 32 ∧
    (selected.filter fun v => decide (v ∈ region)).length = 13 ∧
    (endpoints.filter fun v => decide (v ∈ region)).length = 7 ∧
    (0,0) ∉ selected ++ endpoints ∧ (1,0) ∉ selected ++ endpoints ∧
    (1,15) ∉ selected ++ endpoints ∧
    (2 * (region.length / 2) : Int) -
      2 * (selected.filter fun v => decide (v ∈ region)).length -
      (endpoints.filter fun v => decide (v ∈ region)).length = -1 := by
  decide

/-- Physical end-incidence counting rewrites the exact strip ledger. -/
theorem port_debit_identity (s K B unused a d4 vacant : Int)
    (oldFlux : s = 2*K+unused-(a+d4))
    (ends : vacant = 2*K-B-a) :
    s = B+unused+vacant-d4 := by omega

/-- After safe exports refund at distinct BP columns, only unported
transverse degree-four TP vertices can consume the boundary lower bound. -/
theorem mixed_union_bound (s B safe unused vacant d4 : Int)
    (identity : s = B+safe+unused+vacant-d4) (vacantNonnegative : 0≤vacant) :
    B+safe+unused-d4 ≤ s := by omega

/-- Outside RAW blocks retain their signed charge; no complete receiver
credit is added on top of its regional part. -/
theorem original_grid_budget (margin s B safe unused vacant d4
    outsideDeficit outsidePositiveTwice outsideNegativeTwice : Int)
    (identity : s = B+safe+unused+vacant-d4)
    (partition : margin = s+2*outsideDeficit-outsidePositiveTwice+outsideNegativeTwice)
    (vacantNonnegative : 0≤vacant)
    (covered : outsidePositiveTwice+d4 ≤
      B+safe+unused+2*outsideDeficit+outsideNegativeTwice) :
    0≤margin := by omega

/-- All-q numerical ledger for the written sharp geometric construction. -/
theorem all_q_sharp_ledger (q B n t p : Int)
    (width : n=6*q+2+2*B) (selections : t=5*q+2+B)
    (endpointsCount : p=3*q+B) : 2*n-2*t-p=B-q := by omega

theorem unbounded_negative_budget (bound B : Int) :
    B-(B+2*bound+1) < -2*bound := by omega

end SubQuorum.OccupiedStripDegreeFourBudget

#print axioms SubQuorum.OccupiedStripDegreeFourBudget.geometry_valid
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.certificate_valid
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.all_endpoints_frozen
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.actual_degree_four
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.concrete_negative_strip
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.port_debit_identity
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.mixed_union_bound
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.original_grid_budget
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.all_q_sharp_ledger
#print axioms SubQuorum.OccupiedStripDegreeFourBudget.unbounded_negative_budget
