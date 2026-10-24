import SubQuorum.FrozenSharedMixedGate

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000

namespace SubQuorum.UnportedSharedMixedGate

open SubQuorum.FrozenSharedMixedGate (Point Witness adjacent verticalPartner alternating Frozen)

def selected : List Point := [(2, 4), (2, 6), (3, 3), (3, 8), (4, 9), (4, 11), (5, 16), (7, 16), (8, 3), (8, 15), (10, 3), (10, 14), (11, 4), (11, 6), (11, 11), (11, 13), (12, 8)]

def matching : List (Point × Point) := [
  ((3, 4), (3, 5)),
  ((3, 6), (4, 6)),
  ((3, 7), (4, 7)),
  ((4, 5), (5, 5)),
  ((5, 6), (6, 6)),
  ((5, 7), (5, 8)),
  ((5, 9), (6, 9)),
  ((5, 10), (6, 10)),
  ((5, 11), (6, 11)),
  ((5, 12), (5, 13)),
  ((5, 14), (5, 15)),
  ((6, 5), (7, 5)),
  ((6, 7), (6, 8)),
  ((6, 12), (7, 12)),
  ((6, 13), (6, 14)),
  ((6, 15), (7, 15)),
  ((7, 6), (7, 7)),
  ((7, 8), (7, 9)),
  ((7, 10), (8, 10)),
  ((7, 11), (8, 11)),
  ((8, 4), (8, 5)),
  ((8, 6), (8, 7)),
  ((8, 8), (8, 9)),
  ((8, 12), (9, 12)),
  ((9, 4), (10, 4)),
  ((9, 5), (9, 6)),
  ((9, 7), (10, 7)),
  ((9, 8), (10, 8)),
  ((9, 9), (9, 10)),
  ((9, 11), (10, 11)),
  ((10, 9), (10, 10)),
  ((10, 12), (10, 13)),
  ((11, 7), (11, 8))]

def witnesses : List Witness := [
  ⟨(3, 4), 0, (2, 4), (3, 3)⟩,
  ⟨(3, 5), 15, (3, 6), (4, 5)⟩,
  ⟨(3, 6), 1, (2, 6), (3, 5)⟩,
  ⟨(3, 7), 15, (3, 6), (3, 8)⟩,
  ⟨(4, 5), 2, (3, 5), (4, 6)⟩,
  ⟨(4, 6), 14, (4, 5), (5, 6)⟩,
  ⟨(4, 7), 10, (4, 6), (5, 7)⟩,
  ⟨(5, 5), 13, (5, 6), (6, 5)⟩,
  ⟨(5, 6), 3, (4, 6), (5, 5)⟩,
  ⟨(5, 7), 13, (5, 6), (6, 7)⟩,
  ⟨(5, 8), 9, (5, 9), (6, 8)⟩,
  ⟨(5, 9), 10, (4, 9), (5, 10)⟩,
  ⟨(5, 10), 9, (5, 9), (5, 11)⟩,
  ⟨(5, 11), 4, (4, 11), (5, 12)⟩,
  ⟨(5, 12), 6, (5, 11), (6, 12)⟩,
  ⟨(5, 13), 3, (5, 14), (6, 13)⟩,
  ⟨(5, 14), 8, (5, 13), (6, 14)⟩,
  ⟨(5, 15), 1, (5, 16), (6, 15)⟩,
  ⟨(6, 5), 4, (5, 5), (6, 6)⟩,
  ⟨(6, 6), 12, (6, 5), (6, 7)⟩,
  ⟨(6, 7), 6, (6, 6), (7, 7)⟩,
  ⟨(6, 8), 11, (6, 9), (7, 8)⟩,
  ⟨(6, 9), 8, (6, 8), (7, 9)⟩,
  ⟨(6, 10), 9, (6, 11), (7, 10)⟩,
  ⟨(6, 11), 5, (6, 12), (7, 11)⟩,
  ⟨(6, 12), 4, (5, 12), (6, 13)⟩,
  ⟨(6, 13), 7, (5, 13), (6, 12)⟩,
  ⟨(6, 14), 2, (5, 14), (6, 15)⟩,
  ⟨(6, 15), 9, (5, 15), (6, 14)⟩,
  ⟨(7, 5), 11, (7, 6), (8, 5)⟩,
  ⟨(7, 6), 5, (6, 6), (7, 5)⟩,
  ⟨(7, 7), 10, (7, 8), (8, 7)⟩,
  ⟨(7, 8), 7, (6, 8), (7, 7)⟩,
  ⟨(7, 9), 9, (7, 10), (8, 9)⟩,
  ⟨(7, 10), 8, (7, 9), (7, 11)⟩,
  ⟨(7, 11), 5, (6, 11), (7, 12)⟩,
  ⟨(7, 12), 4, (7, 11), (8, 12)⟩,
  ⟨(7, 15), 0, (7, 16), (8, 15)⟩,
  ⟨(8, 4), 1, (8, 3), (9, 4)⟩,
  ⟨(8, 5), 11, (7, 5), (8, 6)⟩,
  ⟨(8, 6), 3, (8, 5), (9, 6)⟩,
  ⟨(8, 7), 10, (7, 7), (8, 8)⟩,
  ⟨(8, 8), 7, (8, 7), (9, 8)⟩,
  ⟨(8, 9), 9, (7, 9), (8, 10)⟩,
  ⟨(8, 10), 8, (8, 9), (8, 11)⟩,
  ⟨(8, 11), 3, (8, 12), (9, 11)⟩,
  ⟨(8, 12), 6, (7, 12), (8, 11)⟩,
  ⟨(9, 4), 14, (8, 4), (9, 5)⟩,
  ⟨(9, 5), 2, (8, 5), (9, 4)⟩,
  ⟨(9, 6), 13, (8, 6), (9, 7)⟩,
  ⟨(9, 7), 4, (8, 7), (9, 6)⟩,
  ⟨(9, 8), 10, (8, 8), (9, 9)⟩,
  ⟨(9, 9), 8, (8, 9), (9, 8)⟩,
  ⟨(9, 10), 9, (8, 10), (9, 11)⟩,
  ⟨(9, 11), 7, (8, 11), (9, 12)⟩,
  ⟨(9, 12), 2, (9, 11), (10, 12)⟩,
  ⟨(10, 4), 0, (10, 3), (11, 4)⟩,
  ⟨(10, 7), 12, (10, 8), (11, 7)⟩,
  ⟨(10, 8), 6, (10, 7), (11, 8)⟩,
  ⟨(10, 9), 11, (9, 9), (10, 8)⟩,
  ⟨(10, 10), 9, (9, 10), (10, 11)⟩,
  ⟨(10, 11), 1, (10, 12), (11, 11)⟩,
  ⟨(10, 12), 8, (9, 12), (10, 11)⟩,
  ⟨(10, 13), 0, (10, 14), (11, 13)⟩,
  ⟨(11, 7), 5, (10, 7), (11, 6)⟩,
  ⟨(11, 8), 11, (10, 8), (12, 8)⟩]

def alphaA : List Point := [(3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (7, 7), (6, 7), (6, 8), (7, 8), (7, 9), (6, 9), (5, 9)]

def alphaB : List Point := [(5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11)]

def mixedG : List Point := [(5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (9, 9), (8, 9), (8, 8), (9, 8), (10, 8), (11, 8), (11, 7), (10, 7), (9, 7), (8, 7), (8, 6), (9, 6), (9, 5), (8, 5), (8, 4), (9, 4), (10, 4)]


def endpoints : List Point := matching.flatMap fun e => [e.1, e.2]

def mate (v : Point) : Point := FrozenSharedMixedGate.lookupMate v matching

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
    (∀ v ∈ selected ++ endpoints, v.1 < 14 ∧ v.2 < 20) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by
  decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide

theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen :
    ∀ v ∈ endpoints,
      Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate adjacent v := by
  apply FrozenSharedMixedGate.strict_rank_complete (fun x => x ∈ endpoints)
    (fun x => x ∈ selected) mate adjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left, (record v).right, certificate_valid v pv⟩

def alternatingPath : Bool → List Point → Prop
  | _, [] => True
  | _, [_] => True
  | matchingStep, a :: b :: rest =>
    (if matchingStep then mate a = b else verticalPartner a = b) ∧
      alternatingPath (!matchingStep) (b :: rest)

instance (matchingStep : Bool) (path : List Point) : Decidable (alternatingPath matchingStep path) :=
  match path with
  | [] => isTrue True.intro
  | [_] => isTrue True.intro
  | _ :: b :: rest =>
    have := instDecidableAlternatingPath (!matchingStep) (b :: rest)
    inferInstanceAs (Decidable ((_ : Prop) ∧ alternatingPath (!matchingStep) (b :: rest)))

def tp (v : Point) : Prop := v ∈ endpoints ∧ verticalPartner v ∈ selected

def bp (v : Point) : Prop :=
  v ∈ endpoints ∧ verticalPartner v ∉ selected ∧ verticalPartner v ∉ endpoints

def blank (v : Point) : Prop := v ∉ selected ∧ v ∉ endpoints

instance (v : Point) : Decidable (tp v) := inferInstanceAs (Decidable (_ ∧ _))
instance (v : Point) : Decidable (bp v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (v : Point) : Decidable (blank v) := inferInstanceAs (Decidable (_ ∧ _))

def bb (row column : Nat) : Prop :=
  blank (row, column) ∧ blank (row ^^^ 1, column)

instance (row column : Nat) : Decidable (bb row column) :=
  inferInstanceAs (Decidable (_ ∧ _))

def leftAccess (v : Point) : Prop :=
  bb v.1 (v.2 - 1) ∨
  ((v.1, v.2 - 1) ∈ selected ∧ blank (v.1 ^^^ 1, v.2 - 1) ∧ bb v.1 (v.2 - 2))

def rightAccess (v : Point) : Prop :=
  bb v.1 (v.2 + 1) ∨
  ((v.1, v.2 + 1) ∈ selected ∧ blank (v.1 ^^^ 1, v.2 + 1) ∧ bb v.1 (v.2 + 2))

instance (v : Point) : Decidable (leftAccess v) :=
  inferInstanceAs (Decidable (_ ∨ (_ ∧ _ ∧ _)))
instance (v : Point) : Decidable (rightAccess v) :=
  inferInstanceAs (Decidable (_ ∨ (_ ∧ _ ∧ _)))

def alphaTips : List Point := [(3,6), (5,9), (5,11), (10,11)]

theorem two_alpha_paths_and_shared_gate :
    alternatingPath true alphaA ∧ alternatingPath true alphaB ∧ alternatingPath true mixedG ∧
    (alphaA ++ alphaB ++ mixedG).Nodup ∧
    (∀ v ∈ alphaA ++ alphaB ++ mixedG, v ∈ endpoints) ∧
    (∀ v ∈ alphaTips, tp v) ∧ bp (5,10) ∧ tp (10,4) ∧
    adjacent (5,9) (5,10) ∧ adjacent (5,11) (5,10) := by
  decide

/-- No adjacent-BB or selected-cap access exists at any of the four original alpha tips. -/
theorem all_four_alpha_tips_unported :
    ∀ v ∈ alphaTips, 2 ≤ v.2 ∧ v.2 + 2 < 20 ∧
      ¬leftAccess v ∧ ¬rightAccess v := by
  decide

theorem two_gate_resources_and_distinct_beta_exits :
    bb 10 2 ∧ bb 10 5 ∧ (10,3) ∈ selected ∧ blank (11,3) ∧
    bp (3,7) ∧ bp (5,8) ∧ bp (5,12) ∧ bp (5,13) ∧
    adjacent (3,6) (3,7) ∧ adjacent (5,11) (5,12) ∧
    mate (3,7) = (4,7) ∧ mate (5,8) = (5,7) ∧ verticalPartner (4,7) = (5,7) ∧
    mate (5,12) = (5,13) := by
  decide

theorem concrete_sizes : selected.length = 17 ∧ matching.length = 33 ∧
    endpoints.length = 66 := by decide

#print axioms all_endpoints_frozen
#print axioms two_alpha_paths_and_shared_gate
#print axioms all_four_alpha_tips_unported
#print axioms two_gate_resources_and_distinct_beta_exits

end SubQuorum.UnportedSharedMixedGate
