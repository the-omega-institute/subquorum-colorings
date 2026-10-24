import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.FrozenSharedMixedGate

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

def selected : List Point := [(1, 4), (1, 6), (2, 7), (2, 12), (3, 11), (4, 2), (4, 7), (4, 9), (4, 14), (5, 1), (8, 14), (9, 1), (9, 6), (10, 4), (10, 7), (10, 13), (11, 3), (11, 8), (11, 10), (11, 12)]

def matching : List (Point × Point) := [
  ((2, 4), (3, 4)),
  ((2, 5), (2, 6)),
  ((3, 5), (4, 5)),
  ((3, 12), (4, 12)),
  ((4, 4), (5, 4)),
  ((4, 13), (5, 13)),
  ((5, 2), (6, 2)),
  ((5, 5), (5, 6)),
  ((5, 7), (6, 7)),
  ((5, 8), (6, 8)),
  ((5, 9), (6, 9)),
  ((5, 12), (6, 12)),
  ((6, 3), (6, 4)),
  ((6, 5), (6, 6)),
  ((6, 10), (6, 11)),
  ((6, 13), (7, 13)),
  ((7, 2), (7, 3)),
  ((7, 4), (7, 5)),
  ((7, 6), (7, 7)),
  ((7, 8), (8, 8)),
  ((7, 9), (7, 10)),
  ((7, 11), (7, 12)),
  ((8, 2), (9, 2)),
  ((8, 3), (8, 4)),
  ((8, 5), (8, 6)),
  ((8, 9), (9, 9)),
  ((8, 11), (9, 11)),
  ((8, 12), (8, 13)),
  ((9, 3), (10, 3)),
  ((9, 8), (10, 8)),
  ((9, 10), (10, 10)),
  ((10, 11), (10, 12))]

structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def witnesses : List Witness := [
  ⟨(2, 4), 1, (1, 4), (2, 5)⟩,
  ⟨(2, 5), 11, (2, 4), (3, 5)⟩,
  ⟨(2, 6), 0, (1, 6), (2, 7)⟩,
  ⟨(3, 4), 10, (3, 5), (4, 4)⟩,
  ⟨(3, 5), 2, (2, 5), (3, 4)⟩,
  ⟨(3, 12), 0, (2, 12), (3, 11)⟩,
  ⟨(4, 4), 3, (3, 4), (4, 5)⟩,
  ⟨(4, 5), 9, (4, 4), (5, 5)⟩,
  ⟨(4, 12), 10, (4, 13), (5, 12)⟩,
  ⟨(4, 13), 1, (4, 12), (4, 14)⟩,
  ⟨(5, 2), 0, (4, 2), (5, 1)⟩,
  ⟨(5, 4), 8, (5, 5), (6, 4)⟩,
  ⟨(5, 5), 4, (4, 5), (5, 4)⟩,
  ⟨(5, 6), 7, (5, 7), (6, 6)⟩,
  ⟨(5, 7), 5, (4, 7), (5, 6)⟩,
  ⟨(5, 8), 8, (5, 7), (5, 9)⟩,
  ⟨(5, 9), 7, (4, 9), (5, 8)⟩,
  ⟨(5, 12), 2, (4, 12), (5, 13)⟩,
  ⟨(5, 13), 9, (5, 12), (6, 13)⟩,
  ⟨(6, 2), 9, (6, 3), (7, 2)⟩,
  ⟨(6, 3), 3, (6, 2), (7, 3)⟩,
  ⟨(6, 4), 7, (5, 4), (6, 5)⟩,
  ⟨(6, 5), 4, (6, 4), (7, 5)⟩,
  ⟨(6, 6), 6, (5, 6), (6, 7)⟩,
  ⟨(6, 7), 6, (6, 6), (7, 7)⟩,
  ⟨(6, 8), 6, (6, 7), (7, 8)⟩,
  ⟨(6, 9), 7, (6, 10), (7, 9)⟩,
  ⟨(6, 10), 8, (6, 9), (7, 10)⟩,
  ⟨(6, 11), 5, (6, 12), (7, 11)⟩,
  ⟨(6, 12), 8, (6, 13), (7, 12)⟩,
  ⟨(6, 13), 3, (5, 13), (6, 12)⟩,
  ⟨(7, 2), 2, (6, 2), (8, 2)⟩,
  ⟨(7, 3), 8, (6, 3), (7, 4)⟩,
  ⟨(7, 4), 3, (7, 3), (8, 4)⟩,
  ⟨(7, 5), 7, (6, 5), (7, 6)⟩,
  ⟨(7, 6), 5, (6, 6), (7, 5)⟩,
  ⟨(7, 7), 6, (6, 7), (7, 8)⟩,
  ⟨(7, 8), 7, (7, 7), (7, 9)⟩,
  ⟨(7, 9), 4, (7, 8), (8, 9)⟩,
  ⟨(7, 10), 6, (6, 10), (7, 11)⟩,
  ⟨(7, 11), 5, (7, 10), (8, 11)⟩,
  ⟨(7, 12), 4, (6, 12), (7, 13)⟩,
  ⟨(7, 13), 7, (7, 12), (8, 13)⟩,
  ⟨(8, 2), 9, (7, 2), (8, 3)⟩,
  ⟨(8, 3), 2, (8, 2), (9, 3)⟩,
  ⟨(8, 4), 8, (7, 4), (8, 5)⟩,
  ⟨(8, 5), 4, (7, 5), (8, 4)⟩,
  ⟨(8, 6), 7, (7, 6), (9, 6)⟩,
  ⟨(8, 8), 3, (8, 9), (9, 8)⟩,
  ⟨(8, 9), 8, (7, 9), (8, 8)⟩,
  ⟨(8, 11), 5, (7, 11), (8, 12)⟩,
  ⟨(8, 12), 6, (7, 12), (8, 11)⟩,
  ⟨(8, 13), 4, (7, 13), (8, 14)⟩,
  ⟨(9, 2), 1, (9, 1), (9, 3)⟩,
  ⟨(9, 3), 10, (8, 3), (9, 2)⟩,
  ⟨(9, 8), 9, (8, 8), (9, 9)⟩,
  ⟨(9, 9), 2, (9, 8), (9, 10)⟩,
  ⟨(9, 10), 9, (9, 9), (9, 11)⟩,
  ⟨(9, 11), 2, (9, 10), (10, 11)⟩,
  ⟨(10, 3), 0, (10, 4), (11, 3)⟩,
  ⟨(10, 8), 0, (10, 7), (11, 8)⟩,
  ⟨(10, 10), 1, (10, 11), (11, 10)⟩,
  ⟨(10, 11), 10, (9, 11), (10, 10)⟩,
  ⟨(10, 12), 0, (10, 13), (11, 12)⟩]


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
    (∀ v ∈ selected ++ endpoints, v.1 < 14 ∧ v.2 < 16) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

/-- All 64 endpoints of the concrete physical configuration really freeze.
    This is derived from the inductive process, not an assumed rank axiom. -/
theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
      Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply strict_rank_complete (fun x => x ∈ endpoints) (fun x => x ∈ selected)
    mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

theorem concrete_sizes : selected.length = 20 ∧ matching.length = 32 ∧
    endpoints.length = 64 := by decide

def verticalPartner (v : Point) : Point :=
  if v.1 % 2 = 0 then (v.1 + 1, v.2) else (v.1 - 1, v.2)

def alphaA : List Point :=
  [(3,12), (4,12), (5,12), (6,12), (7,12), (7,11),
   (6,11), (6,10), (7,10), (7,9), (6,9), (5,9)]

def alphaB : List Point :=
  [(5,2), (6,2), (7,2), (7,3), (6,3), (6,4), (7,4),
   (7,5), (6,5), (6,6), (7,6), (7,7), (6,7), (5,7)]

def mixedG : List Point :=
  [(5,8), (6,8), (7,8), (8,8), (9,8), (10,8)]

def alternating : Bool → List Point → Prop
  | _, [] => True
  | _, [_] => True
  | useMatching, a :: b :: rest =>
    (if useMatching then mate a = b else verticalPartner a = b) ∧
      alternating (!useMatching) (b :: rest)

instance (useMatching : Bool) (path : List Point) : Decidable (alternating useMatching path) :=
  match path with
  | [] => isTrue True.intro
  | [_] => isTrue True.intro
  | _ :: b :: rest =>
    have := instDecidableAlternating (!useMatching) (b :: rest)
    inferInstanceAs (Decidable ((_ : Prop) ∧ alternating (!useMatching) (b :: rest)))

def tp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∈ selected
def bp (v : Point) : Prop :=
  v ∈ endpoints ∧ verticalPartner v ∉ selected ∧ verticalPartner v ∉ endpoints
def blank (v : Point) : Prop := v ∉ selected ∧ v ∉ endpoints

instance (v : Point) : Decidable (tp v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bp v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))

theorem critical_path_data :
    alternating true alphaA ∧ alternating true alphaB ∧ alternating true mixedG ∧
    (alphaA ++ alphaB ++ mixedG).Nodup ∧
    (∀ v ∈ alphaA ++ alphaB ++ mixedG, v ∈ endpoints) ∧
    tp (3,12) ∧ tp (5,9) ∧ tp (5,2) ∧ tp (5,7) ∧ bp (5,8) ∧ tp (10,8) := by
  decide

theorem shared_entrance_and_two_resources :
    adjacent (5,7) (5,8) ∧ adjacent (5,9) (5,8) ∧
    blank (10,9) ∧ blank (11,9) ∧ blank (10,6) ∧ blank (11,6) ∧
    (10,7) ∈ selected ∧ blank (11,7) ∧
    blank (2,13) ∧ blank (3,13) ∧ blank (4,3) ∧ blank (5,3) := by
  decide

#print axioms strict_rank_complete
#print axioms geometry_valid
#print axioms all_endpoints_frozen
#print axioms critical_path_data

end SubQuorum.FrozenSharedMixedGate
