-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- New concrete board and arbitrary-length row assignment are independently checked here.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.MergerCompletionReserves

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

def baseSelected : List Point := [(1, 8), (1, 13), (1, 14), (2, 1), (2, 3), (2, 7), (2, 10), (2, 15), (3, 4), (3, 9), (3, 16), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14), (5, 16), (7, 16), (8, 1), (9, 4), (9, 12), (10, 6), (10, 11), (11, 7), (11, 9)]

def baseMatching : List (Point × Point) := [
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

/-- 0 empty, 1 central selection, 2 pure cycle, 3 cycle and beta. -/
def selected (s : Fin 4) : List Point := baseSelected ++ if s.val=1 then [(5,4)] else []
def matching (s : Fin 4) : List (Point × Point) := baseMatching ++
  (if 2≤s.val then [((4,3),(5,3))] else []) ++
  (if s.val=3 then [((5,4),(5,5))] else [])

structure Witness where
  point : Point
  rank : Nat
  left : Point
  right : Point
  deriving Inhabited

def baseWitnesses : List Witness := [
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

def witnesses (s : Fin 4) : List Witness := baseWitnesses ++
  (if 2≤s.val then [⟨(4,3),16,(3,3),(4,2)⟩, ⟨(5,3),16,(5,2),(6,3)⟩] else []) ++
  (if s.val=3 then [⟨(5,5),16,(5,6),(6,5)⟩, ⟨(5,4),17,(5,3),(6,4)⟩] else [])

def endpoints (s : Fin 4) : List Point := (matching s).flatMap fun e => [e.1,e.2]
def lookupMate (v : Point) : List (Point × Point) → Point
  | [] => v
  | (a,b)::rest => if v=a then b else if v=b then a else lookupMate v rest

def mate (s : Fin 4) (v : Point) : Point := lookupMate v (matching s)
def record (s : Fin 4) (v : Point) : Witness :=
  ((witnesses s).find? fun w => w.point==v).getD default

def rank (s : Fin 4) (v : Point) : Nat := (record s v).rank

def validAt (s : Fin 4) (v : Point) : Prop :=
  let a := (record s v).left
  let b := (record s v).right
  a≠b ∧ adjacent v a ∧ adjacent v b ∧
    (a∈selected s ∨ (a∈endpoints s ∧ rank s (mate s a)<rank s v)) ∧
    (b∈selected s ∨ (b∈endpoints s ∧ rank s (mate s b)<rank s v))
instance (s : Fin 4) (v : Point) : Decidable (validAt s v) :=
  inferInstanceAs (Decidable (_≠_ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem four_geometries_valid : ∀ s : Fin 4,
    (endpoints s).Nodup ∧ (selected s).Nodup ∧
    (∀ e∈matching s, adjacent e.1 e.2) ∧
    (∀ v∈endpoints s, v∉selected s) ∧
    (∀ v∈selected s ++ endpoints s, v.1<14 ∧ v.2<18) ∧
    (∀ v∈selected s,
      ((selected s ++ endpoints s).filter fun w => decide (adjacent v w)).length≤1) := by decide

theorem mate_closed : ∀ s : Fin 4, ∀ v∈endpoints s, mate s v∈endpoints s := by decide
theorem certificate_valid : ∀ s : Fin 4, ∀ v∈endpoints s, validAt s v := by decide

theorem all_four_completions_frozen (s : Fin 4) : ∀ v∈endpoints s,
    Frozen (fun x => x∈endpoints s) (fun x => x∈selected s) (mate s) adjacent v := by
  apply strict_rank_complete (fun x => x∈endpoints s) (fun x => x∈selected s)
    (mate s) adjacent (rank s) (mate_closed s)
  intro v pv
  exact ⟨(record s v).left,(record s v).right,certificate_valid s v pv⟩

/-- The two feasible but nonfrozen local fillings both leave (5,4) with
    at most one occupied nonmate neighbor, independently of the ranks. -/
def badMatching (outer : Bool) : List (Point × Point) := baseMatching ++
  (if outer then [((5,4),(5,5))] else [((5,3),(5,4))])
def badEndpoints (outer : Bool) : List Point := (badMatching outer).flatMap fun e => [e.1,e.2]
def badMate (outer : Bool) (v : Point) : Point := lookupMate v (badMatching outer)
def badUniverse (outer : Bool) : List Point := baseSelected ++ badEndpoints outer

theorem bad_nonmate_unique : ∀ outer : Bool,
    ∀ a∈badUniverse outer, ∀ b∈badUniverse outer,
      adjacent (5,4) a → adjacent (5,4) b →
      a≠badMate outer (5,4) → b≠badMate outer (5,4) → a=b := by decide

theorem bad_mate_facts : ∀ outer : Bool,
    badMate outer (5,4)∉baseSelected ∧
    badMate outer (badMate outer (5,4))=(5,4) := by decide

def badRetained (outer : Bool) (rho : Point → Nat) (w : Point) : Prop :=
  w∈baseSelected ∨ (w∈badEndpoints outer ∧ rho (badMate outer w)<rho (5,4))

theorem no_strict_certificate_in_bad_completion (outer : Bool) (rho : Point → Nat) :
    ¬ ∃ a b : Point, a≠b ∧ adjacent (5,4) a ∧ adjacent (5,4) b ∧
      badRetained outer rho a ∧ badRetained outer rho b := by
  have facts := bad_mate_facts outer
  have notMate : ∀ w, badRetained outer rho w → w≠badMate outer (5,4) := by
    intro w retained same
    subst w
    rcases retained with selected | ⟨_,lower⟩
    · exact facts.1 selected
    · rw [facts.2] at lower
      omega
  have member : ∀ w, badRetained outer rho w → w∈badUniverse outer := by
    intro w retained
    rcases retained with selected | ⟨endpoint,_⟩
    · exact List.mem_append_left _ selected
    · exact List.mem_append_right _ endpoint
  rintro ⟨a,b,distinct,aa,ab,ra,rb⟩
  exact distinct (bad_nonmate_unique outer a (member a ra) b (member b rb)
    aa ab (notMate a ra) (notMate b rb))

/-- Once the geometric adapter proves the three possible new edges and
    excludes the degree-two states, precisely four frozen local states remain. -/
theorem four_state_classification (cycle middle outer selected : Bool)
    (noMiddle : middle=false) (outerNeedsCycle : outer=true → cycle=true)
    (selectedNoCycle : selected=true → cycle=false)
    (selectedNoOuter : selected=true → outer=false) :
    (cycle=false ∧ outer=false ∧ selected=false) ∨
    (cycle=false ∧ outer=false ∧ selected=true) ∨
    (cycle=true ∧ outer=false ∧ selected=false) ∨
    (cycle=true ∧ outer=true ∧ selected=false) := by
  revert cycle middle outer selected
  decide

theorem exact_elimination_ledger (k q filled value residual cost residualCost : Nat)
    (_enough : 2*q≤k) (_bounded : filled≤q)
    (v : value=2*q+residual) (c : cost=filled+residualCost)
    (_paid : residual≤k-2*q) :
    k-value=(k-2*q)-residual ∧ cost-residualCost=filled := by omega

/-- Remove one actual interval or whole beta with each settled source;
    there is no extra reserve to add to the remaining packet surplus. -/
theorem no_extra_surplus_ledger (intervals betas alphas q filled : Nat)
    (few : filled≤q) (units : 2*q-filled≤intervals)
    (betaUnits : filled≤betas) (sources : 2*q≤alphas) :
    intervals+betas+(alphas-2*q) =
      (intervals-(2*q-filled))+(betas-filled)+alphas := by omega

#print axioms four_geometries_valid
#print axioms all_four_completions_frozen
#print axioms bad_nonmate_unique
#print axioms no_strict_certificate_in_bad_completion
#print axioms four_state_classification
#print axioms exact_elimination_ledger
#print axioms no_extra_surplus_ledger

end SubQuorum.MergerCompletionReserves
