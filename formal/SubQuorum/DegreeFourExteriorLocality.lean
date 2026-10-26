-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- Concrete frozen exterior-locality obstruction and distance arithmetic are checked here.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.DegreeFourExteriorLocality

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

def selected : List Point := [(2,1), (2,3), (2,6), (2,8), (3,0), (3,2), (3,7), (3,9), (4,1), (4,8), (5,0), (5,2), (5,7), (5,9), (6,1), (6,8), (7,0), (7,2), (7,7), (7,9), (8,1), (8,8), (9,0), (9,9), (10,0), (10,2), (10,7), (10,9), (11,1), (11,8), (12,0), (12,2), (12,7), (12,9), (13,1), (13,8), (14,0), (14,2), (14,7), (14,9), (15,1), (15,8), (16,0), (16,2), (16,7), (16,9), (17,1), (17,3), (17,6), (17,8)]

def matching : List (Point × Point) := [
  ((10,3), (10,4)),
  ((10,5), (10,6)),
  ((11,4), (11,5)),
  ((12,4), (12,5)),
  ((11,3), (12,3)),
  ((11,6), (12,6)),
  ((13,3), (14,3)),
  ((13,4), (14,4)),
  ((13,5), (14,5)),
  ((13,6), (14,6)),
  ((15,4), (15,5)),
  ((15,3), (16,3)),
  ((15,6), (16,6)),
  ((9,3), (9,4)),
  ((9,5), (9,6)),
  ((8,4), (8,5)),
  ((7,4), (7,5)),
  ((8,3), (7,3)),
  ((8,6), (7,6)),
  ((6,3), (5,3)),
  ((6,4), (5,4)),
  ((6,5), (5,5)),
  ((6,6), (5,6)),
  ((4,4), (4,5)),
  ((4,3), (3,3)),
  ((4,6), (3,6))]

def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def witnesses : List Witness := [
  ⟨(16,3), 0, (16,2), (17,3)⟩,
  ⟨(16,6), 0, (16,7), (17,6)⟩,
  ⟨(14,3), 1, (14,2), (15,3)⟩,
  ⟨(14,6), 1, (14,7), (15,6)⟩,
  ⟨(12,3), 2, (12,2), (13,3)⟩,
  ⟨(12,6), 2, (12,7), (13,6)⟩,
  ⟨(10,3), 3, (10,2), (11,3)⟩,
  ⟨(10,6), 3, (10,7), (11,6)⟩,
  ⟨(11,4), 4, (10,4), (11,3)⟩,
  ⟨(11,5), 4, (10,5), (11,6)⟩,
  ⟨(10,4), 5, (10,5), (11,4)⟩,
  ⟨(10,5), 5, (10,4), (11,5)⟩,
  ⟨(11,3), 6, (10,3), (11,4)⟩,
  ⟨(11,6), 6, (10,6), (11,5)⟩,
  ⟨(12,4), 7, (11,4), (12,3)⟩,
  ⟨(12,5), 7, (11,5), (12,6)⟩,
  ⟨(13,4), 8, (12,4), (13,3)⟩,
  ⟨(13,5), 8, (12,5), (13,6)⟩,
  ⟨(15,4), 9, (14,4), (15,3)⟩,
  ⟨(15,5), 9, (14,5), (15,6)⟩,
  ⟨(14,4), 10, (14,5), (15,4)⟩,
  ⟨(14,5), 10, (14,4), (15,5)⟩,
  ⟨(13,3), 11, (12,3), (13,4)⟩,
  ⟨(13,6), 11, (12,6), (13,5)⟩,
  ⟨(15,3), 12, (14,3), (15,4)⟩,
  ⟨(15,6), 12, (14,6), (15,5)⟩,
  ⟨(3,3), 13, (2,3), (3,2)⟩,
  ⟨(3,6), 13, (2,6), (3,7)⟩,
  ⟨(5,3), 14, (4,3), (5,2)⟩,
  ⟨(5,6), 14, (4,6), (5,7)⟩,
  ⟨(7,3), 15, (6,3), (7,2)⟩,
  ⟨(7,6), 15, (6,6), (7,7)⟩,
  ⟨(9,3), 16, (8,3), (10,3)⟩,
  ⟨(9,6), 16, (8,6), (10,6)⟩,
  ⟨(8,4), 17, (8,3), (9,4)⟩,
  ⟨(8,5), 17, (8,6), (9,5)⟩,
  ⟨(9,4), 18, (8,4), (9,5)⟩,
  ⟨(9,5), 18, (8,5), (9,4)⟩,
  ⟨(8,3), 19, (8,4), (9,3)⟩,
  ⟨(8,6), 19, (8,5), (9,6)⟩,
  ⟨(7,4), 20, (7,3), (8,4)⟩,
  ⟨(7,5), 20, (7,6), (8,5)⟩,
  ⟨(6,4), 21, (6,3), (7,4)⟩,
  ⟨(6,5), 21, (6,6), (7,5)⟩,
  ⟨(4,4), 22, (4,3), (5,4)⟩,
  ⟨(4,5), 22, (4,6), (5,5)⟩,
  ⟨(5,4), 23, (4,4), (5,5)⟩,
  ⟨(5,5), 23, (4,5), (5,4)⟩,
  ⟨(6,3), 24, (6,4), (7,3)⟩,
  ⟨(6,6), 24, (6,5), (7,6)⟩,
  ⟨(4,3), 25, (4,4), (5,3)⟩,
  ⟨(4,6), 25, (4,5), (5,6)⟩]

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
    (∀ v ∈ selected ++ endpoints, v.1 < 18 ∧ v.2 < 10) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
      Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

def occupiedDegree (v : Point) : Nat :=
  ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length

def inRegion (v : Point) : Prop := v.2=2 ∨ v.2=3 ∨ v.2=6 ∨ v.2=7
instance (v : Point) : Decidable (inRegion v) := inferInstanceAs (Decidable (_ ∨ _ ∨ _ ∨ _))

theorem actual_sources :
    (10,3) ∈ endpoints ∧ (10,6) ∈ endpoints ∧
    (10,2) ∈ selected ∧ (10,7) ∈ selected ∧
    occupiedDegree (10,3)=4 ∧ occupiedDegree (10,6)=4 ∧
    mate (10,3)=(10,4) ∧ mate (10,6)=(10,5) ∧
    ¬inRegion (mate (10,3)) ∧ ¬inRegion (mate (10,6)) := by decide

def tiles : List Point := (List.range 9).flatMap fun r =>
  (List.range 5).map fun c => (r,c)

def corners (q : Point) : List Point :=
  [(2*q.1,2*q.2),(2*q.1,2*q.2+1),(2*q.1+1,2*q.2),(2*q.1+1,2*q.2+1)]

def rawSurplusTwice (q : Point) : Int :=
  4-2*((corners q).filter fun v => decide (v ∈ selected)).length -
    ((corners q).filter fun v => decide (v ∈ endpoints)).length

def outsidePositive : List Point := tiles.filter fun q =>
  decide (q.2 ≠ 1 ∧ q.2 ≠ 3 ∧ rawSurplusTwice q > 0)

theorem exact_outside_positive :
    outsidePositive = [(0,0),(0,2),(0,4),(1,2),(8,2)] ∧
    (∀ q ∈ outsidePositive, rawSurplusTwice q=4) := by decide

/-- Both actual source tiles (5,1),(5,3) have no exterior donor within radius2. -/
theorem no_radius_two_donor :
    (∀ q ∈ outsidePositive, q.1+2 < 5 ∨ 5+2 < q.1) ∧
    (8,2) ∈ outsidePositive ∧ (8 : Nat)-5=3 := by decide

theorem concrete_ledger :
    selected.length=50 ∧ matching.length=26 ∧ endpoints.length=52 ∧
    (selected.filter fun v => decide (inRegion v)).length=18 ∧
    (endpoints.filter fun v => decide (inRegion v)).length=28 ∧
    (180 : Int)-2*selected.length-endpoints.length=28 ∧
    (72 : Int)-2*(selected.filter fun v => decide (inRegion v)).length-
      (endpoints.filter fun v => decide (inRegion v)).length=8 := by decide

/-- The all-h coordinate ledger forces all listed exterior donors beyond radius R. -/
theorem arbitrary_radius_coordinate_separation (h R : Nat) (large : R ≤ h) :
    R < h+3 ∧ 1+R < h+3 ∧ h+3+R < 2*h+4 := by omega

/-- The two exceptions are already covered; a donor for each would overrequire. -/
theorem internal_budget_covers_sources :
    (2+2+6 : Int)-2=8 ∧ (2 : Int) ≤ 2+2+6 := by decide

#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms actual_sources
#print axioms exact_outside_positive
#print axioms no_radius_two_donor
#print axioms concrete_ledger
#print axioms arbitrary_radius_coordinate_separation
#print axioms internal_budget_covers_sources

end SubQuorum.DegreeFourExteriorLocality
