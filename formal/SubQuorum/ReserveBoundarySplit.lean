-- Actual private-boundary split and nonduplicating shared-resource allocation.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.ReserveBoundarySplit

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

def baseSelected : List Point := [(1, 8), (1, 13), (1, 14), (2, 1), (2, 3), (2, 7), (2, 10), (2, 15), (3, 4), (3, 9), (3, 16), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14), (5, 16), (7, 16), (8, 1), (9, 4), (9, 12), (9, 15), (10, 6), (10, 11), (11, 7), (11, 9)]

def baseMatching : List (Point × Point) := [
  ((2, 8), (2, 9)),
  ((3, 1), (4, 1)),
  ((3, 2), (3, 3)),
  ((3, 15), (4, 15)),
  ((4, 2), (5, 2)),
  ((5, 1), (6, 1)),
  ((5, 6), (6, 6)),
  ((5, 7), (5, 8)),
  ((5, 9), (5, 10)),
  ((5, 11), (5, 12)),
  ((5, 15), (6, 15)),
  ((6, 2), (6, 3)),
  ((6, 4), (6, 5)),
  ((6, 7), (7, 7)),
  ((6, 8), (7, 8)),
  ((6, 9), (6, 10)),
  ((6, 11), (6, 12)),
  ((6, 13), (6, 14)),
  ((7, 1), (7, 2)),
  ((7, 3), (7, 4)),
  ((7, 5), (7, 6)),
  ((7, 9), (8, 9)),
  ((7, 10), (7, 11)),
  ((7, 12), (7, 13)),
  ((7, 14), (7, 15)),
  ((8, 4), (8, 5)),
  ((8, 6), (8, 7)),
  ((8, 8), (9, 8)),
  ((8, 10), (8, 11)),
  ((8, 12), (8, 13)),
  ((8, 14), (8, 15)),
  ((9, 9), (10, 9)),
  ((10, 7), (10, 8))]

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
  ⟨(3, 3), 0, (2, 3), (3, 4)⟩,
  ⟨(3, 15), 0, (2, 15), (3, 16)⟩,
  ⟨(10, 7), 0, (10, 6), (11, 7)⟩,
  ⟨(3, 1), 1, (2, 1), (3, 2)⟩,
  ⟨(5, 15), 1, (4, 15), (5, 16)⟩,
  ⟨(10, 9), 1, (10, 8), (11, 9)⟩,
  ⟨(4, 2), 2, (3, 2), (4, 1)⟩,
  ⟨(7, 15), 2, (6, 15), (7, 16)⟩,
  ⟨(9, 8), 2, (9, 9), (10, 8)⟩,
  ⟨(5, 1), 3, (4, 1), (5, 2)⟩,
  ⟨(6, 14), 3, (6, 15), (7, 14)⟩,
  ⟨(8, 9), 3, (8, 8), (9, 9)⟩,
  ⟨(6, 2), 4, (5, 2), (6, 1)⟩,
  ⟨(7, 1), 4, (6, 1), (8, 1)⟩,
  ⟨(7, 8), 4, (7, 9), (8, 8)⟩,
  ⟨(7, 13), 4, (6, 13), (7, 14)⟩,
  ⟨(5, 8), 5, (4, 8), (6, 8)⟩,
  ⟨(6, 9), 5, (6, 8), (7, 9)⟩,
  ⟨(6, 12), 5, (6, 13), (7, 12)⟩,
  ⟨(7, 3), 5, (6, 3), (7, 2)⟩,
  ⟨(8, 12), 5, (7, 12), (9, 12)⟩,
  ⟨(5, 6), 6, (4, 6), (5, 7)⟩,
  ⟨(5, 10), 6, (4, 10), (6, 10)⟩,
  ⟨(6, 4), 6, (6, 3), (7, 4)⟩,
  ⟨(6, 7), 6, (5, 7), (6, 8)⟩,
  ⟨(7, 10), 6, (6, 10), (7, 9)⟩,
  ⟨(7, 11), 6, (6, 11), (7, 12)⟩,
  ⟨(8, 4), 6, (7, 4), (9, 4)⟩,
  ⟨(8, 14), 6, (7, 14), (8, 13)⟩,
  ⟨(6, 10), 7, (6, 11), (7, 10)⟩,
  ⟨(6, 11), 7, (6, 10), (7, 11)⟩,
  ⟨(7, 5), 7, (6, 5), (7, 4)⟩,
  ⟨(7, 6), 7, (6, 6), (7, 7)⟩,
  ⟨(8, 7), 7, (7, 7), (8, 8)⟩,
  ⟨(5, 12), 8, (4, 12), (6, 12)⟩,
  ⟨(6, 5), 8, (6, 6), (7, 5)⟩,
  ⟨(6, 6), 8, (6, 5), (7, 6)⟩,
  ⟨(7, 9), 8, (6, 9), (7, 10)⟩,
  ⟨(7, 12), 8, (6, 12), (7, 11)⟩,
  ⟨(8, 5), 8, (7, 5), (8, 6)⟩,
  ⟨(8, 6), 8, (7, 6), (8, 5)⟩,
  ⟨(6, 13), 9, (6, 12), (7, 13)⟩,
  ⟨(7, 4), 9, (6, 4), (7, 5)⟩,
  ⟨(7, 7), 9, (7, 6), (8, 7)⟩,
  ⟨(8, 8), 9, (8, 7), (8, 9)⟩,
  ⟨(8, 10), 9, (7, 10), (8, 9)⟩,
  ⟨(5, 7), 10, (5, 6), (6, 7)⟩,
  ⟨(6, 3), 10, (6, 4), (7, 3)⟩,
  ⟨(6, 8), 10, (6, 7), (6, 9)⟩,
  ⟨(7, 14), 10, (6, 14), (7, 13)⟩,
  ⟨(9, 9), 10, (8, 9), (9, 8)⟩,
  ⟨(5, 9), 11, (5, 8), (6, 9)⟩,
  ⟨(6, 15), 11, (6, 14), (7, 15)⟩,
  ⟨(7, 2), 11, (6, 2), (7, 3)⟩,
  ⟨(8, 15), 11, (7, 15), (9, 15)⟩,
  ⟨(10, 8), 11, (9, 8), (10, 9)⟩,
  ⟨(4, 15), 12, (4, 14), (5, 15)⟩,
  ⟨(5, 11), 12, (5, 10), (6, 11)⟩,
  ⟨(6, 1), 12, (6, 2), (7, 1)⟩,
  ⟨(8, 13), 12, (7, 13), (8, 14)⟩,
  ⟨(5, 2), 13, (5, 1), (6, 2)⟩,
  ⟨(8, 11), 13, (7, 11), (8, 12)⟩,
  ⟨(4, 1), 14, (4, 2), (5, 1)⟩,
  ⟨(3, 2), 15, (3, 1), (4, 2)⟩]

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

theorem all_four_rematched_boards_frozen (s : Fin 4) : ∀ v∈endpoints s,
    Frozen (fun x => x∈endpoints s) (fun x => x∈selected s) (mate s) adjacent v := by
  apply strict_rank_complete (fun x => x∈endpoints s) (fun x => x∈selected s)
    (mate s) adjacent (rank s) (mate_closed s)
  intro v pv
  exact ⟨(record s v).left,(record s v).right,certificate_valid s v pv⟩

def rightAlpha : List Point := [(3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (7, 14), (6, 14), (6, 13), (7, 13), (7, 12), (6, 12), (6, 11), (7, 11), (7, 10), (6, 10), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9)]

def partner (v : Point) : Point :=
  if v.1 % 2 = 0 then (v.1+1,v.2) else (v.1-1,v.2)

def alternating (s : Fin 4) : List Point → Bool
  | [] => true
  | [_] => false
  | u::v::rest => (mate s u==v) && (match rest with
      | [] => true
      | w::tail => (partner v==w) && alternating s (w::tail))

def TP (s : Fin 4) (v : Point) : Prop := v∈endpoints s ∧ partner v∈selected s
def BP (s : Fin 4) (v : Point) : Prop :=
  v∈endpoints s ∧ partner v∉selected s ∧ partner v∉endpoints s
instance (s : Fin 4) (v : Point) : Decidable (TP s v) := inferInstanceAs (Decidable (_ ∧ _))
instance (s : Fin 4) (v : Point) : Decidable (BP s v) := inferInstanceAs (Decidable (_ ∧ _ ∧ _))

theorem changed_boundary_strands : ∀ s : Fin 4,
    rightAlpha.Nodup ∧ rightAlpha.length=20 ∧
    (∀ v∈rightAlpha, v∈endpoints s) ∧ alternating s rightAlpha=true ∧
    TP s (3,15) ∧ TP s (10,9) ∧
    mate s (5,12)=(5,11) ∧ TP s (5,12) ∧ BP s (5,11) ∧
    (4,15)∈rightAlpha ∧ (5,15)∈rightAlpha := by decide

theorem original_singleton_geometry : ∀ s : Fin 4,
    (4,13)∉selected s ++ endpoints s ∧ (5,13)∉selected s ++ endpoints s ∧
    (4,14)∈selected s ∧ (5,14)∉selected s ++ endpoints s ∧
    (4,15)∈endpoints s ∧ (5,15)∈endpoints s := by decide

theorem three_actual_chain_links : ∀ s : Fin 4,
    TP s (5,6) ∧ BP s (5,7) ∧ TP s (5,8) ∧ BP s (5,9) ∧
    TP s (5,10) ∧ BP s (5,11) ∧ TP s (5,12) ∧
    mate s (5,7)=(5,8) ∧ mate s (5,9)=(5,10) ∧ mate s (5,11)=(5,12) ∧
    adjacent (5,6) (5,7) ∧ adjacent (5,8) (5,9) ∧ adjacent (5,10) (5,11) := by decide

inductive Choice where
  | skip | localPay | shared
  deriving DecidableEq

def Allowed (p : Option Nat) (j : Bool) : Choice → Prop
  | .skip => True
  | .localPay => ∃ c, p=some c
  | .shared => j=true

def Paid : Choice → Nat
  | .skip => 0
  | _ => 1

def Charge (p : Option Nat) (h : Nat) : Choice → Nat
  | .skip => 0
  | .localPay => p.getD 0
  | .shared => h

def Joint (L R : Option Nat) (j : Bool) (x y : Choice) : Prop :=
  Allowed L j x ∧ Allowed R j y ∧ ¬ (x=.shared ∧ y=.shared)

/-- Full payment has precisely three resource-distinct alternatives. -/
theorem full_payment_budget (L R : Option Nat) (j : Bool) (h B : Nat) :
    (∃ x y, Joint L R j x y ∧ Paid x+Paid y=2 ∧ Charge L h x+Charge R 0 y≤B) ↔
    (∃ l r, L=some l ∧ R=some r ∧ l+r≤B) ∨
    (j=true ∧ ∃ l, L=some l ∧ l≤B) ∨
    (j=true ∧ ∃ r, R=some r ∧ h+r≤B) := by
  constructor
  · rintro ⟨x,y,⟨ax,ay,noReuse⟩,paid,budget⟩
    cases x with
    | skip => cases y <;> simp [Paid] at paid
    | localPay =>
      obtain ⟨l,hl⟩ := ax
      cases y with
      | skip => simp [Paid] at paid
      | localPay =>
        obtain ⟨r,hr⟩ := ay
        exact Or.inl ⟨l,r,hl,hr,by simpa [Charge,hl,hr] using budget⟩
      | shared =>
        exact Or.inr (Or.inl ⟨ay,l,hl,by simpa [Charge,hl] using budget⟩)
    | shared =>
      cases y with
      | skip => simp [Paid] at paid
      | localPay =>
        obtain ⟨r,hr⟩ := ay
        exact Or.inr (Or.inr ⟨ax,r,hr,by simpa [Charge,hr] using budget⟩)
      | shared => exact False.elim (noReuse ⟨rfl,rfl⟩)
  · intro alternatives
    rcases alternatives with ⟨l,r,hl,hr,budget⟩ | ⟨jyes,l,hl,budget⟩ | ⟨jyes,r,hr,budget⟩
    · refine ⟨.localPay,.localPay,?_,rfl,?_⟩
      · exact ⟨⟨l,hl⟩,⟨r,hr⟩,by intro h; cases h.1⟩
      · simpa [Charge,hl,hr] using budget
    · refine ⟨.localPay,.shared,?_,rfl,?_⟩
      · exact ⟨⟨l,hl⟩,jyes,by intro h; cases h.1⟩
      · simpa [Charge,hl] using budget
    · refine ⟨.shared,.localPay,?_,rfl,?_⟩
      · exact ⟨jyes,⟨r,hr⟩,by intro h; cases h.2⟩
      · simpa [Charge,hr] using budget

/-- One original shared interval cannot simultaneously pay two sources. -/
theorem sole_shared_capacity (x y : Choice) (h : Joint none none true x y) :
    Paid x+Paid y≤1 := by
  rcases h with ⟨ax,ay,distinct⟩
  cases x <;> cases y <;> simp_all [Allowed,Paid]

abbrev Repairs := List (Bool × Bool)
def fills : Repairs → Nat
  | [] => 0
  | (f,_)::xs => (if f then 1 else 0)+fills xs
def releases : Repairs → Nat
  | [] => 0
  | (_,e)::xs => (if e then 1 else 0)+releases xs
def overlap : Repairs → Nat
  | [] => 0
  | (f,e)::xs => (if f && e then 1 else 0)+overlap xs
def totalPaid : Repairs → Nat
  | [] => 0
  | (f,e)::xs => (if f || e then 2 else 1)+totalPaid xs
def totalCost : Repairs → Nat
  | [] => 0
  | (f,e)::xs => (if f then 1 else if e then 3 else 0)+totalCost xs

/-- Arbitrarily many simultaneous repairs count overlap once, with actual toll3. -/
theorem all_copy_repair_ledger (xs : Repairs) :
    overlap xs≤releases xs ∧
    totalPaid xs+overlap xs=xs.length+fills xs+releases xs ∧
    totalCost xs+3*overlap xs=fills xs+3*releases xs := by
  induction xs with
  | nil => simp [overlap,releases,totalPaid,fills,totalCost]
  | cons p xs ih =>
      rcases p with ⟨f,e⟩
      cases f <;> cases e <;>
        simp [overlap,releases,totalPaid,fills,totalCost] at * <;> omega

theorem all_copy_exact_repair_cost (xs : Repairs) :
    totalPaid xs=xs.length+fills xs+releases xs-overlap xs ∧
    totalCost xs=fills xs+3*(releases xs-overlap xs) := by
  have h := all_copy_repair_ledger xs
  omega

#print axioms four_geometries_valid
#print axioms all_four_rematched_boards_frozen
#print axioms changed_boundary_strands
#print axioms original_singleton_geometry
#print axioms three_actual_chain_links
#print axioms full_payment_budget
#print axioms sole_shared_capacity
#print axioms all_copy_repair_ledger
#print axioms all_copy_exact_repair_cost

end SubQuorum.ReserveBoundarySplit
