import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace SubQuorum.ShortBetaDeletion

abbrev Point := Nat × Nat
abbrev Matching := List (Point × Point)

def neighbours (p : Point) : List Point :=
  [(p.1+1,p.2),(p.1,p.2+1)] ++
  (if p.1=0 then [] else [(p.1-1,p.2)]) ++
  (if p.2=0 then [] else [(p.1,p.2-1)])

def endpoints (M : Matching) : List Point := M.flatMap (fun e => [e.1,e.2])

def mate (M : Matching) (p : Point) : Point :=
  match M with
  | [] => p
  | (a,b)::rest => if p=a then b else if p=b then a else mate rest p

def Retained (T : List Point) (M : Matching) (rank : Point → Nat) (p w : Point) : Prop :=
  w ∈ T ∨ (w ∈ endpoints M ∧ rank (mate M w)<rank p)

def FrozenBy (T : List Point) (M : Matching) (rank : Point → Nat) : Prop :=
  ∀ p ∈ endpoints M, ∃ x ∈ neighbours p, ∃ y ∈ neighbours p,
    x≠y ∧ x≠mate M p ∧ y≠mate M p ∧ Retained T M rank p x ∧ Retained T M rank p y

def AvailableOutside (T : List Point) (M : Matching) (C : List Point) (w : Point) : Prop :=
  w ∈ T ∨ (w ∈ endpoints M ∧ mate M w ∉ C)

def ClosedCore (T : List Point) (M : Matching) (C : List Point) : Prop :=
  ∀ p ∈ C, ∀ x ∈ neighbours p, ∀ y ∈ neighbours p,
    x≠mate M p → y≠mate M p →
    AvailableOutside T M C x → AvailableOutside T M C y → x=y

theorem minimum_on_list {V : Type} (rank : V → Nat) (C : List V) (nonempty : C≠[]) :
    ∃ p ∈ C, ∀ q ∈ C, rank p≤rank q := by
  induction C with
  | nil => exact False.elim (nonempty rfl)
  | cons a rest ih =>
    by_cases empty : rest=[]
    · subst rest
      exact ⟨a,by simp,by simp⟩
    · obtain ⟨b,hb,least⟩ := ih empty
      by_cases small : rank a≤rank b
      · refine ⟨a,by simp,?_⟩
        intro q hq
        rcases List.mem_cons.mp hq with eq | hr
        · subst q; exact Nat.le_refl _
        · exact Nat.le_trans small (least q hr)
      · refine ⟨b,by simp [hb],?_⟩
        intro q hq
        rcases List.mem_cons.mp hq with eq | hr
        · subst q; omega
        · exact least q hr

/-- A nonempty actual dependency core has no first strictly frozen endpoint. -/
theorem closed_core_excludes_certificate (T : List Point) (M : Matching) (C : List Point)
    (nonempty : C≠[]) (inside : ∀ p ∈ C, p ∈ endpoints M)
    (closed : ClosedCore T M C) (rank : Point → Nat) : ¬FrozenBy T M rank := by
  intro frozen
  obtain ⟨p,hp,least⟩ := minimum_on_list rank C nonempty
  obtain ⟨x,nx,y,ny,different,mx,my,rx,ry⟩ := frozen p (inside p hp)
  have outside : ∀ w, Retained T M rank p w → AvailableOutside T M C w := by
    intro w retained
    rcases retained with selected | ⟨ep,earlier⟩
    · exact Or.inl selected
    · refine Or.inr ⟨ep,?_⟩
      intro inCore
      have bound := least (mate M w) inCore
      omega
  exact different (closed p hp x nx y ny mx my (outside x rx) (outside y ry))

def selected : List Point := [(1,1), (1,7), (1,9), (1,11), (2,12), (4,11), (6,11), (7,12), (8,11), (9,4), (9,7), (9,10), (9,12), (11,9), (12,10), (13,1), (14,3), (14,8)]

def original : Matching := [((2,1), (2,2)), ((2,3), (2,4)), ((2,5), (3,5)), ((2,6), (2,7)), ((2,8), (2,9)), ((2,10), (2,11)), ((3,1), (4,1)), ((3,2), (3,3)), ((3,4), (4,4)), ((3,6), (3,7)), ((3,8), (3,9)), ((3,10), (4,10)), ((4,2), (5,2)), ((4,5), (5,5)), ((4,6), (5,6)), ((4,7), (4,8)), ((4,9), (5,9)), ((5,1), (6,1)), ((5,3), (6,3)), ((5,4), (6,4)), ((5,7), (6,7)), ((5,8), (6,8)), ((6,2), (7,2)), ((6,5), (7,5)), ((6,6), (7,6)), ((6,9), (6,10)), ((7,1), (8,1)), ((7,3), (8,3)), ((7,4), (8,4)), ((7,7), (8,7)), ((7,8), (7,9)), ((7,10), (8,10)), ((8,2), (9,2)), ((8,5), (8,6)), ((8,8), (8,9)), ((9,1), (10,1)), ((10,2), (11,2)), ((11,1), (12,1)), ((12,2), (12,3)), ((12,4), (12,5)), ((12,6), (12,7)), ((12,8), (12,9)), ((13,3), (13,4)), ((13,5), (13,6)), ((13,7), (13,8))]

def rankTable : List (Point × Nat) := [((2,1), 16), ((2,2), 16), ((2,3), 17), ((2,4), 14), ((2,5), 18), ((2,6), 14), ((2,7), 2), ((2,8), 15), ((2,9), 1), ((2,10), 16), ((2,11), 0), ((3,1), 17), ((3,2), 16), ((3,3), 15), ((3,4), 18), ((3,5), 13), ((3,6), 19), ((3,7), 7), ((3,8), 20), ((3,9), 6), ((3,10), 21), ((4,1), 15), ((4,2), 18), ((4,4), 13), ((4,5), 19), ((4,6), 8), ((4,7), 26), ((4,8), 5), ((4,9), 22), ((4,10), 5), ((5,1), 19), ((5,2), 14), ((5,3), 19), ((5,4), 20), ((5,5), 12), ((5,6), 25), ((5,7), 6), ((5,8), 26), ((5,9), 4), ((6,1), 13), ((6,2), 20), ((6,3), 21), ((6,4), 12), ((6,5), 21), ((6,6), 9), ((6,7), 25), ((6,8), 3), ((6,9), 27), ((6,10), 1), ((7,1), 21), ((7,2), 12), ((7,3), 20), ((7,4), 22), ((7,5), 11), ((7,6), 24), ((7,7), 7), ((7,8), 27), ((7,9), 2), ((7,10), 28), ((8,1), 11), ((8,2), 21), ((8,3), 23), ((8,4), 11), ((8,5), 23), ((8,6), 10), ((8,7), 24), ((8,8), 8), ((8,9), 29), ((8,10), 0), ((9,1), 22), ((9,2), 10), ((10,1), 9), ((10,2), 23), ((11,1), 24), ((11,2), 8), ((12,1), 7), ((12,2), 25), ((12,3), 6), ((12,4), 27), ((12,5), 4), ((12,6), 29), ((12,7), 2), ((12,8), 31), ((12,9), 0), ((13,3), 26), ((13,4), 5), ((13,5), 28), ((13,6), 3), ((13,7), 30), ((13,8), 1)]


def witnessTable : List (Point × Point × Point) := [((2,1), (1,1), (3,1)), ((2,2), (2,3), (3,2)), ((2,3), (2,2), (3,3)), ((2,4), (2,5), (3,4)), ((2,5), (2,4), (2,6)), ((2,6), (2,5), (3,6)), ((2,7), (1,7), (2,8)), ((2,8), (2,7), (3,8)), ((2,9), (1,9), (2,10)), ((2,10), (2,9), (3,10)), ((2,11), (1,11), (2,12)), ((3,1), (2,1), (3,2)), ((3,2), (3,1), (4,2)), ((3,3), (2,3), (3,4)), ((3,4), (2,4), (3,3)), ((3,5), (3,6), (4,5)), ((3,6), (2,6), (3,5)), ((3,7), (3,8), (4,7)), ((3,8), (2,8), (3,7)), ((3,9), (3,10), (4,9)), ((3,10), (2,10), (3,9)), ((4,1), (4,2), (5,1)), ((4,2), (3,2), (4,1)), ((4,4), (4,5), (5,4)), ((4,5), (3,5), (4,4)), ((4,6), (3,6), (4,7)), ((4,7), (3,7), (4,6)), ((4,8), (4,9), (5,8)), ((4,9), (3,9), (4,10)), ((4,10), (4,9), (4,11)), ((5,1), (4,1), (5,2)), ((5,2), (5,1), (6,2)), ((5,3), (5,2), (5,4)), ((5,4), (4,4), (5,5)), ((5,5), (5,6), (6,5)), ((5,6), (5,5), (6,6)), ((5,7), (4,7), (5,8)), ((5,8), (5,7), (5,9)), ((5,9), (5,8), (6,9)), ((6,1), (6,2), (7,1)), ((6,2), (5,2), (6,1)), ((6,3), (6,2), (6,4)), ((6,4), (6,5), (7,4)), ((6,5), (5,5), (6,4)), ((6,6), (5,6), (6,7)), ((6,7), (6,6), (7,7)), ((6,8), (6,9), (7,8)), ((6,9), (5,9), (6,8)), ((6,10), (6,11), (7,10)), ((7,1), (6,1), (7,2)), ((7,2), (7,1), (8,2)), ((7,3), (6,3), (7,4)), ((7,4), (6,4), (7,5)), ((7,5), (7,6), (8,5)), ((7,6), (7,5), (8,6)), ((7,7), (6,7), (7,8)), ((7,8), (6,8), (7,7)), ((7,9), (6,9), (7,10)), ((7,10), (6,10), (7,9)), ((8,1), (8,2), (9,1)), ((8,2), (7,2), (8,3)), ((8,3), (8,2), (8,4)), ((8,4), (8,5), (9,4)), ((8,5), (7,5), (8,4)), ((8,6), (7,6), (8,7)), ((8,7), (8,6), (9,7)), ((8,8), (7,8), (8,7)), ((8,9), (7,9), (8,10)), ((8,10), (8,11), (9,10)), ((9,1), (8,1), (9,2)), ((9,2), (9,1), (10,2)), ((10,1), (10,2), (11,1)), ((10,2), (9,2), (10,1)), ((11,1), (10,1), (11,2)), ((11,2), (11,1), (12,2)), ((12,1), (12,2), (13,1)), ((12,2), (11,2), (12,1)), ((12,3), (12,4), (13,3)), ((12,4), (12,3), (13,4)), ((12,5), (12,6), (13,5)), ((12,6), (12,5), (13,6)), ((12,7), (12,8), (13,7)), ((12,8), (12,7), (13,8)), ((12,9), (11,9), (12,10)), ((13,3), (12,3), (14,3)), ((13,4), (12,4), (13,5)), ((13,5), (12,5), (13,4)), ((13,6), (12,6), (13,7)), ((13,7), (12,7), (13,6)), ((13,8), (12,8), (14,8))]

def witnesses (p : Point) : Point × Point := ((witnessTable.find? (fun x => x.1=p)).map Prod.snd).getD ((0,0),(0,0))

def originalRank (p : Point) : Nat := ((rankTable.find? (fun x => x.1=p)).map Prod.snd).getD 0

def afterDeletion : Matching := original.filter (fun e => e≠((8,5),(8,6)))

def core : List Point := [(5,3),(6,4),(7,3),(8,4)]

def InBoard (p : Point) : Prop := p.1<16 ∧ p.2<14

def Feasible (T : List Point) (M : Matching) : Prop :=
  (endpoints M).Pairwise (fun a b => a≠b) ∧
  (∀ p ∈ T, InBoard p ∧ p ∉ endpoints M) ∧
  (∀ p ∈ endpoints M, InBoard p) ∧
  (∀ e ∈ M, e.2 ∈ neighbours e.1) ∧
  (∀ p ∈ T, ((neighbours p).filter (fun w => decide (w ∈ T ++ endpoints M))).length≤1)

/-- Concrete geometry checked by kernel reduction, without native evaluation. -/
theorem original_feasible : Feasible selected original := by
  unfold Feasible InBoard
  decide

theorem original_frozen : FrozenBy selected original originalRank := by
  have checked : ∀ p ∈ endpoints original,
      (witnesses p).1 ∈ neighbours p ∧ (witnesses p).2 ∈ neighbours p ∧
      (witnesses p).1≠(witnesses p).2 ∧
      (witnesses p).1≠mate original p ∧ (witnesses p).2≠mate original p ∧
      Retained selected original originalRank p (witnesses p).1 ∧
      Retained selected original originalRank p (witnesses p).2 := by
    unfold Retained
    decide
  intro p hp
  obtain ⟨nx,ny,different,mx,my,rx,ry⟩ := checked p hp
  exact ⟨(witnesses p).1,nx,(witnesses p).2,ny,different,mx,my,rx,ry⟩

theorem deletion_feasible : Feasible selected afterDeletion := by
  unfold Feasible InBoard
  decide

theorem actual_core_closed : ClosedCore selected afterDeletion core := by
  unfold ClosedCore AvailableOutside
  decide

theorem actual_core_inside : ∀ p ∈ core, p ∈ endpoints afterDeletion := by decide

/-- No alternative ranks can repair freezing after the actual beta deletion. -/
theorem deletion_has_no_freezing_certificate (rank : Point → Nat) :
    ¬FrozenBy selected afterDeletion rank :=
  closed_core_excludes_certificate selected afterDeletion core (by decide)
    actual_core_inside actual_core_closed rank

#print axioms minimum_on_list
#print axioms closed_core_excludes_certificate
#print axioms original_feasible
#print axioms original_frozen
#print axioms deletion_feasible
#print axioms actual_core_closed
#print axioms actual_core_inside
#print axioms deletion_has_no_freezing_certificate

end SubQuorum.ShortBetaDeletion
