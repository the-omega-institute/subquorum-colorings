import Lean.Elab.Tactic.Omega

set_option autoImplicit false

/- The new all-length proof's scalar, time, and induction kernel.
   Coordinate graph/matching-to-premise adapters remain written and executable. -/
namespace SubQuorum.FrozenEqualityMatchingRigidity

/-- The two port-row slacks alone exclude a weight-ten pocket with a blank U. -/
theorem pocket_port_slack (L r q u v H lhs : Nat)
    (hL : L≤10) (hstart : L=10 → r=1 ∧ q=1)
    (hv : q=1 → v=0)
    (hid : lhs+6*r=6*L+H)
    (hslack : lhs+4*(1-(v+u))+2*(2-(v+u+q))≤58) :
    L≤9+u := by
  by_cases hu : u=0
  · by_cases h : L≤9+u
    · exact h
    have hten : L=10 := by omega
    obtain ⟨hr,hq⟩ := hstart hten
    have hzero := hv hq
    omega
  · omega

/-- The mandatory B,D,U dependencies put U strictly later than F. -/
theorem canonical_core_order (B D F H U : Nat)
    (hdF : F<D) (hdH : H<D) (hbD : D<B) (huB : B<U) :
    F<U ∧ H<U := by omega

/-- A site needing two of three witnesses cannot use a later witness. -/
theorem two_of_three_excludes_late (v a b c : Nat) (hlate : v<a)
    (hsupport : (a<v ∧ b<v) ∨ (a<v ∧ c<v) ∨ (b<v ∧ c<v)) :
    b<v ∧ c<v := by omega

/-- The forbidden X--b mate would close this strict time cycle. -/
theorem no_bridge_vertical_cycle (U b ZR : Nat)
    (hUb : U<b) (hbZR : b<ZR) (hZR : ZR<U) : False := by omega

/-- The forbidden Y--H mate would close the next strict time cycle. -/
theorem no_old_H_vertical_cycle (b H L ZR U : Nat)
    (hbH : b<H) (hHL : H<L) (hLZR : L<ZR)
    (hZRU : ZR<U) (hUb : U<b) : False := by omega

/-- The lower neighbour of F cannot pair back to F. -/
theorem no_lower_F_vertical_cycle (F W H : Nat)
    (hFW : F<W) (hWH : W<H) (hHF : H<F) : False := by omega

/-- Arbitrary-length backwards induction, independent of band size. -/
theorem backwards_chain (P : Nat → Prop) (m : Nat)
    (hend : P m) (hstep : ∀ j, j<m → P (j+1) → P j) :
    ∀ j, j≤m → P j := by
  have aux : ∀ d j, j+d=m → P j := by
    intro d
    induction d with
    | zero =>
      intro j heq
      have hj : j=m := by omega
      simpa only [hj] using hend
    | succ d ih =>
      intro j heq
      apply hstep j (by omega)
      exact ih (j+1) (by omega)
  intro j hj
  exact aux (m-j) j (by omega)

/-- A terminal core/lower-edge pair and the local propagation imply all pairs. -/
theorem terminal_pair_propagates (Core Lower : Nat → Prop) (m : Nat)
    (hend : Core m ∧ Lower m)
    (hstep : ∀ j, j<m → Core (j+1) ∧ Lower (j+1) → Core j ∧ Lower j) :
    ∀ j, j≤m → Core j ∧ Lower j :=
  backwards_chain (fun j => Core j ∧ Lower j) m hend hstep

/-- Two endpoints each needing the other earlier cannot both freeze. -/
theorem no_two_endpoint_trap (a z : Nat) (ha : z<a) (hz : a<z) : False := by omega

/-- Matching containment and exclusion of extra edges give actual equality. -/
theorem matching_equality {E : Type} (M prescribed : E → Prop)
    (hsub : ∀ e, prescribed e → M e)
    (hnoextra : ∀ e, M e → ¬prescribed e → False) : M=prescribed := by
  funext e
  apply propext
  constructor
  · intro he
    by_cases hp : prescribed e
    · exact hp
    · exact False.elim (hnoextra e he hp)
  · exact hsub e

theorem forced_matching_count (m : Nat) :
    (4*m+5)+(m+1)+m+1+(3*m+2)=9*m+9 := by omega

theorem equality_selection_count (m T : Nat)
    (h : T+(9*m+9)=18*m+30) : T=9*m+21 := by omega

/-- Rigidity improves the bound by one if any prescribed edge is absent. -/
theorem binary_defect_bound (m J d : Nat)
    (hupper : J≤18*m+30) (hrigid : J=18*m+30 → d=0) :
    J+min 1 d≤18*m+30 := by
  cases d with
  | zero => simp only [Nat.min_zero, Nat.add_zero]; exact hupper
  | succ d =>
    have he : J≠18*m+30 := by
      intro h
      have := hrigid h
      omega
    have hmin : min 1 (d+1)=1 := by omega
    rw [hmin]
    omega

/-- All demand and reserve terms refer to a single original-tile charge. -/
theorem binary_token_budget (m J d plus minus : Nat)
    (hJ : J+min 1 d≤18*m+30)
    (hcharge : plus+2*J=minus+37*m+60) :
    minus+m+2*(min 1 d)≤plus := by omega

/-- The all-g family misses arbitrarily many edges but has margin only one. -/
theorem nonadditive_counterexample (m : Nat) :
    (18*m+29)+(3*m+4)>18*m+30 := by omega

theorem no_repeated_token_reserve (m plus minus : Nat)
    (h : plus=minus+m+2) : ¬(minus+m+2*(3*m+4)≤plus) := by omega

#print axioms pocket_port_slack
#print axioms canonical_core_order
#print axioms two_of_three_excludes_late
#print axioms no_bridge_vertical_cycle
#print axioms no_old_H_vertical_cycle
#print axioms no_lower_F_vertical_cycle
#print axioms backwards_chain
#print axioms terminal_pair_propagates
#print axioms no_two_endpoint_trap
#print axioms matching_equality
#print axioms forced_matching_count
#print axioms equality_selection_count
#print axioms binary_defect_bound
#print axioms binary_token_budget
#print axioms nonadditive_counterexample
#print axioms no_repeated_token_reserve
end SubQuorum.FrozenEqualityMatchingRigidity
