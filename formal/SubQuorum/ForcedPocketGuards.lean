import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ForcedPocketGuards

def Occupied {V : Type} (T P : V → Prop) (v : V) : Prop := T v ∨ P v

def Witness {V : Type} (N : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (rank : V → Nat) (p w : V) : Prop :=
  N p w ∧ w≠mate p ∧ (T w ∨ (P w ∧ rank (mate w)<rank p))

def FrozenCertificate {V : Type} (N : V → V → Prop) (T P : V → Prop)
    (mate : V → V) (rank : V → Nat) : Prop :=
  ∀ p, P p → ∃ x y, x≠y ∧ Witness N T P mate rank p x ∧ Witness N T P mate rank p y

/-- Two distinct witnesses restricted to two candidates must use both.
The grid-neighbor adapters are explicit inputs to the main theorem. -/
theorem forced_candidate {V : Type} (R : V → Prop) (a b : V)
    (two : ∃ x y, x≠y ∧ R x ∧ R y)
    (options : ∀ w, R w → w=a ∨ w=b) : R b := by
  rcases two with ⟨x,y,different,hx,hy⟩
  rcases options x hx with xa | xb
  · rcases options y hy with ya | yb
    · exact False.elim (different (xa.trans ya.symm))
    · simpa only [yb] using hy
  · simpa only [xb] using hx

/-- Feasibility excludes either guard selection when it sees two distinct
occupied vertices. This also excludes a T partner of a guard using the
adjacent alpha's occupied PP/TP partner in the next band. -/
theorem two_neighbours_exclude_selection {V : Type} (N : V → V → Prop)
    (T P : V → Prop) (t x y : V)
    (feasible : ∀ v, T v → ∀ a, N v a → Occupied T P a →
      ∀ b, N v b → Occupied T P b → a=b)
    (nx : N t x) (ny : N t y) (ox : Occupied T P x) (oy : Occupied T P y)
    (distinct : x≠y) : ¬T t := by
  intro selected
  exact distinct (feasible t selected x nx ox y ny oy)

/-- Left PP guard of an actual horizontal beta u--v. If the guard's
band partner hp were blank, matching uniqueness forces h--k and the
strict certificate requires h before v and v before h.

The hypotheses are local actual-neighbor lists. P h/P k and notT hp
are derived by the written grid feasibility argument above; no artificial
rank inequality is assumed. Reflection gives the right guard theorem. -/
theorem guard_partner_is_endpoint {V : Type} (N : V → V → Prop)
    (T P : V → Prop) (mate : V → V) (rank : V → Nat)
    (u v a ap b h k hp dv : V)
    (certificate : FrozenCertificate N T P mate rank)
    (disjoint : ∀ w, P w → ¬T w)
    (range : ∀ w, P w → P (mate w))
    (inverse : ∀ w, P w → mate (mate w)=w)
    (edge : ∀ w, P w → N w (mate w))
    (pu : P u) (pv : P v) (ph : P h) (pk : P k)
    (uv : mate u=v) (vu : mate v=u) (apa : mate ap=a)
    (vh : v≠h) (ah : a≠h)
    (notSelectedPartner : ¬T hp) (blankVPartner : ¬Occupied T P dv)
    (vNeighbours : ∀ w, N v w → w=u ∨ w=b ∨ w=k ∨ w=dv)
    (hNeighbours : ∀ w, N h w → w=u ∨ w=ap ∨ w=k ∨ w=hp) :
    P hp := by
  by_cases php : P hp
  · exact php
  · have blankHP : ¬Occupied T P hp := by
      intro occupied
      exact occupied.elim notSelectedPartner php
    have hk : mate h=k := by
      rcases hNeighbours (mate h) (edge h ph) with eq | eq | eq | eq
      · have inv := inverse h ph
        rw [eq,uv] at inv
        exact False.elim (vh inv)
      · have inv := inverse h ph
        rw [eq,apa] at inv
        exact False.elim (ah inv)
      · exact eq
      · have ep := range h ph
        rw [eq] at ep
        exact False.elim (php ep)
    have kh : mate k=h := by
      have inv := inverse h ph
      simpa only [hk] using inv
    have retainedK : Witness N T P mate rank v k := by
      apply forced_candidate (Witness N T P mate rank v) b k
      · exact certificate v pv
      · intro w hw
        rcases vNeighbours w hw.1 with eq | eq | eq | eq
        · have bad := hw.2.1
          rw [eq,vu] at bad
          exact False.elim (bad rfl)
        · exact Or.inl eq
        · exact Or.inr eq
        · have occupied : Occupied T P w := hw.2.2.elim Or.inl (fun h => Or.inr h.1)
          rw [eq] at occupied
          exact False.elim (blankVPartner occupied)
    have retainedU : Witness N T P mate rank h u := by
      apply forced_candidate (Witness N T P mate rank h) ap u
      · exact certificate h ph
      · intro w hw
        rcases hNeighbours w hw.1 with eq | eq | eq | eq
        · exact Or.inr eq
        · exact Or.inl eq
        · have bad := hw.2.1
          rw [eq,hk] at bad
          exact False.elim (bad rfl)
        · have occupied : Occupied T P w := hw.2.2.elim Or.inl (fun h => Or.inr h.1)
          rw [eq] at occupied
          exact False.elim (blankHP occupied)
    have hBeforeV : rank h<rank v := by
      rcases retainedK.2.2 with selected | kept
      · exact False.elim (disjoint k pk selected)
      · simpa only [kh] using kept.2
    have vBeforeH : rank v<rank h := by
      rcases retainedU.2.2 with selected | kept
      · exact False.elim (disjoint u pu selected)
      · simpa only [uv] using kept.2
    omega

#print axioms forced_candidate
#print axioms two_neighbours_exclude_selection
#print axioms guard_partner_is_endpoint

end SubQuorum.ForcedPocketGuards
