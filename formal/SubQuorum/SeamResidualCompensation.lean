import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.SeamResidualCompensation

def bottomFirst (first i : Nat) : Prop :=
    first=9+24*i ∨ first=11+24*i ∨ first=12+24*i ∨ first=13+24*i

theorem adjacent_tp_columns_excluded {V : Type} (T O : V → Prop)
    (adj : V → V → Prop)
    (unique : ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y)
    (t v w : V) (ht : T t) (hv : O v) (hw : O w)
    (htv : adj t v) (htw : adj t w) (different : v≠w) : False := by
  exact different (unique t ht v hv htv w hw htw)

theorem seam_bp_column_injection (i j kind kind' side side' : Nat)
    (hk : kind<2) (hk' : kind'<2) (hs : side<2) (hs' : side'<2)
    (same : 22+24*i+kind+2*side=22+24*j+kind'+2*side') :
    i=j ∧ kind=kind' ∧ side=side' := by omega

theorem degree_three_excludes_guarded_mate (degree : Nat)
    (minimum : 3≤degree) (twoGuards : degree≤2) : False := by omega

theorem periodic_window_injection (a b first i j : Nat)
    (width : b<a+24)
    (hi : a+24*i≤first ∧ first≤b+24*i)
    (hj : a+24*j≤first ∧ first≤b+24*j) : i=j := by omega

theorem bottom_private_copy_injection (first i j : Nat)
    (hi : bottomFirst first i) (hj : bottomFirst first j) : i=j := by
  have wi : 9+24*i≤first ∧ first≤13+24*i := by
    rcases hi with h | h | h | h <;> omega
  have wj : 9+24*j≤first ∧ first≤13+24*j := by
    rcases hj with h | h | h | h <;> omega
  omega

theorem same_color_holes_no_unpaid {V : Type} (color : V → Nat)
    (hole : V → Prop) (oddHole : ∀ v, hole v → color v=1)
    (x y : V) (opposite : color x≠color y) : ¬ (hole x ∧ hole y) := by
  intro h
  exact opposite ((oddHole x h.1).trans (oddHole y h.2).symm)

theorem certificate_ledger (n h p g q z zBP b bBP : Nat)
    (hh : h≤5*n) (hq : q≤g) (hz : zBP≤z) (hb : bBP≤b) :
    23*n+p+g+z+b =
      (18*n+h+p+q+zBP+bBP)+(5*n-h+g-q+(z-zBP)+(b-bBP)) := by omega

theorem full_payment_ledger (a b aFinal bFinal : Nat)
    (balance : a+bFinal=b+aFinal) (monotone : bFinal≤b) :
    b-bFinal+aFinal=a := by omega

theorem saturated_guard_blank {V : Type} (T O : V → Prop)
    (adj : V → V → Prop)
    (unique : ∀ t, T t → ∀ x, O x → adj t x → ∀ y, O y → adj t y → x=y)
    (t old blank : V) (ht : T t) (ho : O old)
    (hto : adj t old) (htb : adj t blank) (different : old≠blank) : ¬ O blank := by
  intro hb
  exact different (unique t ht old ho hto blank hb htb)

abbrev Point := Nat × Nat
def adjacent (v w : Point) : Prop :=
  (v.1=w.1 ∧ (v.2+1=w.2 ∨ w.2+1=v.2)) ∨
  (v.2=w.2 ∧ (v.1+1=w.1 ∨ w.1+1=v.1))
instance (v w : Point) : Decidable (adjacent v w) :=
  inferInstanceAs (Decidable ((_ ∧ (_ ∨ _)) ∨ (_ ∧ (_ ∨ _))))
/-- Literal blanks, selected guards, and their retained occupied neighbors.
Membership in the actual base is separately checked by the Python adapter. -/
def guardTriples : List (Point × Point × Point) := [
 ((25,1),(25,2),(24,2)),((26,2),(25,2),(24,2)),
 ((25,12),(25,11),(24,11)),((26,11),(25,11),(24,11)),
 ((25,16),(25,17),(24,17)),((26,17),(25,17),(24,17)),
 ((25,22),(25,21),(24,21)),((26,21),(25,21),(24,21)),
 ((24,23),(24,22),(24,21)),((25,25),(25,26),(24,26)),
 ((24,24),(24,25),(24,26)),((26,26),(25,26),(24,26))]
theorem actual_guard_triple_geometry : ∀ e∈guardTriples,
    adjacent e.2.1 e.2.2 ∧ adjacent e.2.1 e.1 ∧ e.2.2≠e.1 := by decide

#print axioms adjacent_tp_columns_excluded
#print axioms seam_bp_column_injection
#print axioms degree_three_excludes_guarded_mate
#print axioms periodic_window_injection
#print axioms bottom_private_copy_injection
#print axioms same_color_holes_no_unpaid
#print axioms certificate_ledger
#print axioms full_payment_ledger
#print axioms saturated_guard_blank
#print axioms actual_guard_triple_geometry
end SubQuorum.SeamResidualCompensation
