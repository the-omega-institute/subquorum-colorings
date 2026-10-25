import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 3000000

namespace SubQuorum.PersistentMixedCycleBetaCore

def Occupied {V : Type} (T P : V → Prop) (v : V) : Prop := T v ∨ P v

def Feasible {V : Type} (N : V → V → Prop) (T P : V → Prop) : Prop :=
  ∀ t, T t → ∀ x, N t x → Occupied T P x →
    ∀ y, N t y → Occupied T P y → x=y

/-- A retained selected guard already sees an old occupied neighbour. -/
theorem selected_guard_blank {V : Type} (N : V → V → Prop) (T P : V → Prop)
    (feasible : Feasible N T P) (q t w : V) (selected : T t)
    (oldNeighbour : Occupied T P w) (tq : N t q) (tw : N t w)
    (different : q ≠ w) : ¬Occupied T P q := by
  intro occupied
  exact different (feasible t selected q tq occupied w tw oldNeighbour)

/-- Matching cannot enter a closed set of old endpoints from a fresh site. -/
theorem matched_wall_excludes_new_endpoint {V : Type}
    (N : V → V → Prop) (P Wall Blank : V → Prop) (mate : V → V)
    (mateEdge : ∀ v, P v → N v (mate v))
    (mateP : ∀ v, P v → P (mate v))
    (inverse : ∀ v, P v → mate (mate v)=v)
    (wallClosed : ∀ w, Wall w → Wall (mate w))
    (blank : ∀ w, Blank w → ¬P w) (q : V) (fresh : ¬Wall q)
    (boundary : ∀ w, N q w → Wall w ∨ Blank w) : ¬P q := by
  intro pq
  rcases boundary (mate q) (mateEdge q pq) with wall | vacant
  · have back := wallClosed (mate q) wall
    rw [inverse q pq] at back
    exact fresh back
  · exact blank (mate q) vacant (mateP q pq)

/-- The second blank rule excludes T by two retained neighbours and P by
old matching closure. Arbitrary simultaneous additions are allowed. -/
theorem matched_enclosure_blank {V : Type} (N : V → V → Prop)
    (T P Wall Blank : V → Prop) (mate : V → V)
    (feasible : Feasible N T P)
    (mateEdge : ∀ v, P v → N v (mate v)) (mateP : ∀ v, P v → P (mate v))
    (inverse : ∀ v, P v → mate (mate v)=v)
    (wallClosed : ∀ w, Wall w → Wall (mate w))
    (blank : ∀ w, Blank w → ¬P w) (q a b : V) (fresh : ¬Wall q)
    (qa : N q a) (qb : N q b) (pa : Occupied T P a) (pb : Occupied T P b)
    (different : a ≠ b) (boundary : ∀ w, N q w → Wall w ∨ Blank w) :
    ¬Occupied T P q := by
  rintro (tq | pq)
  · exact different (feasible q tq a qa pa b qb pb)
  · exact matched_wall_excludes_new_endpoint N P Wall Blank mate mateEdge mateP
      inverse wallClosed blank q fresh boundary pq

abbrev Point := Int × Int

def neighbours (v : Point) : List Point :=
  [(v.1-1,v.2),(v.1+1,v.2),(v.1,v.2-1),(v.1,v.2+1)]

def Adjacent (v w : Point) : Prop := w ∈ neighbours v

instance (v w : Point) : Decidable (Adjacent v w) :=
  inferInstanceAs (Decidable (w ∈ neighbours v))

structure Guard where
  q : Point
  t : Point
  w : Point
  deriving DecidableEq

def guards : List Guard := [
  ⟨(3,4),(3,5),(2,5)⟩, ⟨(3,19),(2,19),(2,20)⟩,
  ⟨(4,3),(4,4),(5,4)⟩, ⟨(4,5),(3,5),(2,5)⟩,
  ⟨(4,15),(3,15),(3,14)⟩, ⟨(4,16),(4,17),(5,17)⟩,
  ⟨(4,18),(4,17),(5,17)⟩, ⟨(4,20),(4,19),(5,19)⟩,
  ⟨(19,16),(19,15),(18,15)⟩, ⟨(21,16),(20,16),(20,17)⟩,
  ⟨(25,5),(25,4),(24,4)⟩, ⟨(25,18),(25,17),(24,17)⟩]

def directBlanks : List Point := guards.map Guard.q
def guardT : List Point := guards.map Guard.t
def guardMatching : List (Point × Point) := [
  ((2,3),(2,2)), ((3,2),(4,2)), ((2,20),(2,21)), ((3,21),(4,21)),
  ((20,17),(19,17)), ((21,18),(22,18)), ((22,17),(22,16))]
def wall : List Point := guardMatching.flatMap (fun e => [e.1,e.2])
def guardP : List Point := guards.map Guard.w ++ wall

def oldMate (v : Point) : Point :=
  match guardMatching.find? (fun e => decide (v=e.1 ∨ v=e.2)) with
  | none => v
  | some e => if v=e.1 then e.2 else e.1

structure Star where
  q : Point
  a : Point
  b : Point
  deriving DecidableEq

def stars : List Star := [⟨(3,3),(2,3),(3,2)⟩,
  ⟨(3,20),(2,20),(3,21)⟩, ⟨(21,17),(20,17),(21,18)⟩]
def protectedBlanks : List Point := directBlanks ++ stars.map Star.q

theorem direct_coordinate_checks : guards.all (fun g => decide
    (Adjacent g.t g.q ∧ Adjacent g.t g.w ∧ g.q ≠ g.w ∧
      g.t ∈ guardT ∧ g.w ∈ guardP)) = true := by decide

theorem wall_coordinate_checks : wall.all (fun v => decide (oldMate v ∈ wall)) = true := by
  decide

theorem star_coordinate_checks : stars.all (fun s => decide
    (s.q ∉ wall ∧ s.a ∈ guardP ∧ s.b ∈ guardP ∧ s.a ≠ s.b ∧
      Adjacent s.q s.a ∧ Adjacent s.q s.b ∧
      (neighbours s.q).all (fun w => decide (w ∈ wall ∨ w ∈ directBlanks)) = true)) = true := by
  decide

/-- The actual fifteen coordinate blanks are permanent in ANY feasible
extension retaining the listed occupied guards and seven local mate edges.
No bound on the number of added sites or freezing depth is assumed. -/
theorem all_fifteen_blanks_permanent (T P : Point → Prop) (mate : Point → Point)
    (feasible : Feasible Adjacent T P)
    (mateEdge : ∀ v, P v → Adjacent v (mate v))
    (mateP : ∀ v, P v → P (mate v))
    (inverse : ∀ v, P v → mate (mate v)=v)
    (retainT : ∀ v, v ∈ guardT → T v)
    (retainP : ∀ v, v ∈ guardP → P v)
    (retainMate : ∀ v, v ∈ wall → mate v=oldMate v) :
    ∀ q, q ∈ protectedBlanks → ¬Occupied T P q := by
  have direct : ∀ q, q ∈ directBlanks → ¬Occupied T P q := by
    intro q member
    obtain ⟨g, hg, same⟩ := List.mem_map.mp member
    have facts := of_decide_eq_true (List.all_eq_true.mp direct_coordinate_checks g hg)
    exact same ▸ selected_guard_blank Adjacent T P feasible g.q g.t g.w
      (retainT g.t facts.2.2.2.1) (Or.inr (retainP g.w facts.2.2.2.2))
      facts.1 facts.2.1 facts.2.2.1
  have closed : ∀ v, v ∈ wall → mate v ∈ wall := by
    intro v hv
    rw [retainMate v hv]
    exact of_decide_eq_true (List.all_eq_true.mp wall_coordinate_checks v hv)
  intro q member
  rcases List.mem_append.mp member with first | second
  · exact direct q first
  · obtain ⟨s, hs, same⟩ := List.mem_map.mp second
    have facts := of_decide_eq_true (List.all_eq_true.mp star_coordinate_checks s hs)
    have result := matched_enclosure_blank Adjacent T P (fun v => v ∈ wall)
      (fun v => v ∈ directBlanks) mate feasible mateEdge mateP inverse closed
      (fun v hv pv => direct v hv (Or.inr pv)) s.q s.a s.b facts.1
      facts.2.2.2.2.1 facts.2.2.2.2.2.1
      (Or.inr (retainP s.a facts.2.1)) (Or.inr (retainP s.b facts.2.2.1))
      facts.2.2.2.1
      (fun w hw => of_decide_eq_true
        (List.all_eq_true.mp facts.2.2.2.2.2.2 w hw))
    exact same ▸ result

/-- Owner-link reachability. Only horizontal TP--BP links are used by the
physical adapter, but the closure theorem holds for arbitrary directed graphs. -/
inductive Reach {V : Type} (step : V → V → Prop) (root : V) : V → Prop where
  | start : Reach step root root
  | next {u v : V} : Reach step root u → step u v → Reach step root v

theorem outside_path_cannot_enter_closed_core {V : Type}
    (step : V → V → Prop) (core : V → Prop) (root : V)
    (outside : ¬core root)
    (incomingClosed : ∀ u v, step u v → core v → core u) :
    ∀ v, Reach step root v → ¬core v := by
  intro v path
  induction path with
  | start => exact outside
  | @next u v path edge ih => exact fun cv => ih (incomingClosed u v edge cv)

/-- Four different whole beta resources per copy pay four different sources.
No interval identity changes in the residual ledger. -/
theorem residual_ledger (intervals betas sources copies : Int) :
    intervals+betas-sources = intervals+(betas-4*copies)-(sources-4*copies) := by
  omega

end SubQuorum.PersistentMixedCycleBetaCore

#print axioms SubQuorum.PersistentMixedCycleBetaCore.selected_guard_blank
#print axioms SubQuorum.PersistentMixedCycleBetaCore.matched_wall_excludes_new_endpoint
#print axioms SubQuorum.PersistentMixedCycleBetaCore.matched_enclosure_blank
#print axioms SubQuorum.PersistentMixedCycleBetaCore.direct_coordinate_checks
#print axioms SubQuorum.PersistentMixedCycleBetaCore.wall_coordinate_checks
#print axioms SubQuorum.PersistentMixedCycleBetaCore.star_coordinate_checks
#print axioms SubQuorum.PersistentMixedCycleBetaCore.all_fifteen_blanks_permanent
#print axioms SubQuorum.PersistentMixedCycleBetaCore.outside_path_cannot_enter_closed_core
#print axioms SubQuorum.PersistentMixedCycleBetaCore.residual_ledger
