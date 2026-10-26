-- Generic inductive freezing/rank infrastructure reused from FrozenSharedMixedGate.lean.
-- Universal local cover bounds and a sharp fully frozen completion are checked here.
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 1600000

namespace SubQuorum.FrozenStripCompletionReserves

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

def countSelected (T : Point → Prop) [DecidablePred T] : List Point → Nat
  | [] => 0
  | v::vs => (if T v then 1 else 0)+countSelected T vs

theorem count_append (T : Point → Prop) [DecidablePred T] (xs ys : List Point) :
    countSelected T (xs++ys) = countSelected T xs+countSelected T ys := by
  induction xs with
  | nil => simp [countSelected]
  | cons a xs ih => simp [countSelected,ih,Nat.add_assoc]

theorem count_zero (T : Point → Prop) [DecidablePred T] (xs : List Point)
    (h : ∀ v ∈ xs, ¬T v) : countSelected T xs=0 := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    have ha : ¬T a := h a (by simp)
    have hs : ∀ v ∈ xs, ¬T v := by
      intro v hv
      exact h v (by simp [hv])
    have hz := ih hs
    simp [countSelected,ha,hz]

def face (r c : Nat) : List Point := [(r,c),(r,c+1),(r+1,c),(r+1,c+1)]

theorem pair_limit {P T : Point → Prop} [DecidablePred T] (h : Feasible P T)
    (a b p : Point) (hp : P p) (hab : adjacent a b) (hap : adjacent a p)
    (distinct : p ≠ b) : countSelected T [a,b] ≤ 1 := by
  have noBoth : ¬(T a ∧ T b) := by
    intro ⟨ha,hb⟩
    exact distinct (h.2 a p b ha hap hab (Or.inl hp) (Or.inr hb))
  by_cases ha : T a <;> by_cases hb : T b <;> simp_all [countSelected]

theorem forced_blank {P T : Point → Prop} (h : Feasible P T)
    (v a b : Point) (pa : P a) (pb : P b)
    (va : adjacent v a) (vb : adjacent v b) (distinct : a ≠ b) : ¬T v := by
  intro tv
  exact distinct (h.2 v a b tv va vb (Or.inl pa) (Or.inl pb))

theorem face_limit {P T : Point → Prop} [DecidablePred T]
    (h : Feasible P T) (r c : Nat) : countSelected T (face r c) ≤ 2 := by
  have noABC : ¬(T (r,c) ∧ T (r,c+1) ∧ T (r+1,c)) := by
    rintro ⟨ha,hb,hc⟩
    have eq := h.2 (r,c) (r,c+1) (r+1,c) ha (by simp [adjacent])
      (by simp [adjacent]) (Or.inr hb) (Or.inr hc)
    have e := congrArg Prod.fst eq
    omega
  have noABD : ¬(T (r,c) ∧ T (r,c+1) ∧ T (r+1,c+1)) := by
    rintro ⟨ha,hb,hd⟩
    have eq := h.2 (r,c+1) (r,c) (r+1,c+1) hb (by simp [adjacent])
      (by simp [adjacent]) (Or.inr ha) (Or.inr hd)
    have e := congrArg Prod.fst eq
    omega
  have noACD : ¬(T (r,c) ∧ T (r+1,c) ∧ T (r+1,c+1)) := by
    rintro ⟨ha,hc,hd⟩
    have eq := h.2 (r+1,c) (r,c) (r+1,c+1) hc (by simp [adjacent])
      (by simp [adjacent]) (Or.inr ha) (Or.inr hd)
    have e := congrArg Prod.fst eq
    omega
  have noBCD : ¬(T (r,c+1) ∧ T (r+1,c) ∧ T (r+1,c+1)) := by
    rintro ⟨hb,hc,hd⟩
    have eq := h.2 (r+1,c+1) (r,c+1) (r+1,c) hd (by simp [adjacent])
      (by simp [adjacent]) (Or.inr hb) (Or.inr hc)
    have e := congrArg Prod.fst eq
    omega
  by_cases ha : T (r,c) <;> by_cases hb : T (r,c+1) <;>
    by_cases hc : T (r+1,c) <;> by_cases hd : T (r+1,c+1) <;>
    simp_all [countSelected,face]

def moduleP : List Point := [(1,1),(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(3,4)]
def moduleForbidden : List Point := [(2,1),(2,4)]
def moduleCells : List Point := moduleP ++ moduleForbidden ++ face 0 4 ++ face 4 0 ++ face 4 4 ++ [(3,1),(3,0)] ++ [(4,3),(5,3)] ++ [(0,3),(0,2)] ++ [(0,1),(0,0)] ++ [(1,0),(2,0)] ++ [(3,5),(2,5)] ++ [(4,2),(5,2)]
theorem module_partition :
    moduleCells.Nodup ∧ moduleCells.length = 36 ∧
    (∀ r ∈ List.range 6, ∀ c ∈ List.range 6, (r,c) ∈ moduleCells) ∧
    (∀ v ∈ moduleCells, v.1<6 ∧ v.2<6) := by decide

theorem module_upper_bound (T : Point → Prop) [DecidablePred T]
    (h : Feasible (fun v => v ∈ moduleP) T) :
    countSelected T moduleCells ≤ 13 := by
  have z0 : ¬T (2,1) := forced_blank h (2,1) (1,1) (2,2) (by decide) (by decide) (by decide) (by decide) (by decide)
  have z1 : ¬T (2,4) := forced_blank h (2,4) (2,3) (3,4) (by decide) (by decide) (by decide) (by decide) (by decide)
  have f0 := face_limit h 0 4
  have f1 := face_limit h 4 0
  have f2 := face_limit h 4 4
  have e0 := pair_limit h (3,1) (3,0) (3,2) (by decide) (by decide) (by decide) (by decide)
  have e1 := pair_limit h (4,3) (5,3) (3,3) (by decide) (by decide) (by decide) (by decide)
  have e2 := pair_limit h (0,3) (0,2) (1,3) (by decide) (by decide) (by decide) (by decide)
  have e3 := pair_limit h (0,1) (0,0) (1,1) (by decide) (by decide) (by decide) (by decide)
  have e4 := pair_limit h (1,0) (2,0) (1,1) (by decide) (by decide) (by decide) (by decide)
  have e5 := pair_limit h (3,5) (2,5) (3,4) (by decide) (by decide) (by decide) (by decide)
  have e6 := pair_limit h (4,2) (5,2) (3,2) (by decide) (by decide) (by decide) (by decide)

  have zeroP : countSelected T moduleP=0 := count_zero T moduleP (fun v hv => h.1 v hv)
  have zeroF : countSelected T moduleForbidden=0 := by simp [moduleForbidden,countSelected,z0,z1]
  simp only [moduleCells,count_append,zeroP,zeroF,Nat.zero_add]
  generalize hf0 : countSelected T (face 0 4)=nf0 at f0 ⊢
  generalize hf1 : countSelected T (face 4 0)=nf1 at f1 ⊢
  generalize hf2 : countSelected T (face 4 4)=nf2 at f2 ⊢
  generalize he0 : countSelected T [(3,1),(3,0)]=ne0 at e0 ⊢
  generalize he1 : countSelected T [(4,3),(5,3)]=ne1 at e1 ⊢
  generalize he2 : countSelected T [(0,3),(0,2)]=ne2 at e2 ⊢
  generalize he3 : countSelected T [(0,1),(0,0)]=ne3 at e3 ⊢
  generalize he4 : countSelected T [(1,0),(2,0)]=ne4 at e4 ⊢
  generalize he5 : countSelected T [(3,5),(2,5)]=ne5 at e5 ⊢
  generalize he6 : countSelected T [(4,2),(5,2)]=ne6 at e6 ⊢
  omega

def capP : List Point := [(1,1),(2,1)]
def capForbidden : List Point := []
def capCells : List Point := capP ++ capForbidden ++ face 0 2 ++ face 2 2 ++ face 4 0 ++ face 4 2 ++ [(0,1),(0,0)] ++ [(3,1),(3,0)] ++ [(1,0),(2,0)]
theorem cap_partition :
    capCells.Nodup ∧ capCells.length = 24 ∧
    (∀ r ∈ List.range 6, ∀ c ∈ List.range 4, (r,c) ∈ capCells) ∧
    (∀ v ∈ capCells, v.1<6 ∧ v.2<4) := by decide

theorem cap_upper_bound (T : Point → Prop) [DecidablePred T]
    (h : Feasible (fun v => v ∈ capP) T) :
    countSelected T capCells ≤ 11 := by
  have f0 := face_limit h 0 2
  have f1 := face_limit h 2 2
  have f2 := face_limit h 4 0
  have f3 := face_limit h 4 2
  have e0 := pair_limit h (0,1) (0,0) (1,1) (by decide) (by decide) (by decide) (by decide)
  have e1 := pair_limit h (3,1) (3,0) (2,1) (by decide) (by decide) (by decide) (by decide)
  have e2 := pair_limit h (1,0) (2,0) (1,1) (by decide) (by decide) (by decide) (by decide)

  have zeroP : countSelected T capP=0 := count_zero T capP (fun v hv => h.1 v hv)
  have zeroF : countSelected T capForbidden=0 := rfl
  simp only [capCells,count_append,zeroP,zeroF,Nat.zero_add]
  generalize hf0 : countSelected T (face 0 2)=nf0 at f0 ⊢
  generalize hf1 : countSelected T (face 2 2)=nf1 at f1 ⊢
  generalize hf2 : countSelected T (face 4 0)=nf2 at f2 ⊢
  generalize hf3 : countSelected T (face 4 2)=nf3 at f3 ⊢
  generalize he0 : countSelected T [(0,1),(0,0)]=ne0 at e0 ⊢
  generalize he1 : countSelected T [(3,1),(3,0)]=ne1 at e1 ⊢
  generalize he2 : countSelected T [(1,0),(2,0)]=ne2 at e2 ⊢
  omega

theorem sum_module_bounds (xs : List Nat) (h : ∀ x ∈ xs, x ≤ 13) :
    xs.sum ≤ 13*xs.length := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
    have ha : a ≤ 13 := h a (by simp)
    have hs : xs.sum ≤ 13*xs.length := ih (by intro x hx; exact h x (by simp [hx]))
    simp only [List.sum_cons,List.length_cons]
    omega

theorem global_cover_bound (k cap : Nat) (xs : List Nat)
    (hc : cap ≤ 11) (hl : xs.length=k) (hx : ∀ x ∈ xs, x ≤ 13) :
    cap+xs.sum ≤ 13*k+11 := by
  have hs := sum_module_bounds xs hx
  omega

def selected : List Point := [(0,1),(0,3),(0,5),(0,7),(0,9),(0,11),(0,13),(0,15),(1,2),(1,4),(1,8),(1,10),(1,14),(2,0),(2,3),(3,1),(3,3),(3,5),(3,9),(3,11),(3,15),(4,0),(4,2),(4,4),(4,6),(4,8),(4,10),(4,12),(4,14),(5,0),(5,3),(5,5),(5,7),(5,9),(5,11),(5,13),(5,15)]

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

def region : List Point := (List.range 2).flatMap fun r =>
  (List.range 16).map fun c => (r,c)

def tileCorners (q : Point) : List Point := face (2*q.1) (2*q.2)
def rawSurplusTwice (q : Point) : Int :=
  4-2*((tileCorners q).filter fun v => decide (v ∈ selected)).length-
    ((tileCorners q).filter fun v => decide (v ∈ endpoints)).length

theorem sharp_concrete_counts :
    selected.length=37 ∧ matching.length=9 ∧ endpoints.length=18 ∧
    (selected.filter fun v => decide (v ∈ region)).length=13 ∧
    (endpoints.filter fun v => decide (v ∈ region)).length=7 ∧
    (48 : Int)-selected.length-matching.length=2 ∧
    (32 : Int)-2*(selected.filter fun v => decide (v ∈ region)).length-
      (endpoints.filter fun v => decide (v ∈ region)).length = -1 := by decide

theorem distinct_physical_reserves :
    rawSurplusTwice (1,2)=2 ∧ rawSurplusTwice (1,5)=2 ∧
    rawSurplusTwice (1,4)=1 ∧ rawSurplusTwice (1,7)=1 ∧
    rawSurplusTwice (1,0)= -1 ∧
    (∀ q ∈ [(1,2),(1,5)], ∀ v ∈ tileCorners q, v ∉ endpoints) ∧
    ([(1,2),(1,5),(1,4),(1,7),(1,0)] : List Point).Nodup := by decide

#print axioms pair_limit
#print axioms forced_blank
#print axioms face_limit
#print axioms module_partition
#print axioms module_upper_bound
#print axioms cap_partition
#print axioms cap_upper_bound
#print axioms sum_module_bounds
#print axioms global_cover_bound
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms sharp_concrete_counts
#print axioms distinct_physical_reserves

end SubQuorum.FrozenStripCompletionReserves
