import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.PinwheelTwoTrackSwitches

def bit (b : Bool) : Nat := if b then 1 else 0
def cut (a b : Bool) : Nat := bit (a && !b)

def doubleFaces (nw ne sw se : Bool) : Nat :=
  bit (!nw && !ne) + bit (!sw && !se) + bit (nw && sw) + bit (ne && se)

/-- True means horizontally outward actual M at that corner. -/
theorem pinwheel_classification (nw ne sw se : Bool) :
    doubleFaces nw ne sw se = 0 →
      (nw = false ∧ ne = true ∧ sw = true ∧ se = false) ∨
      (nw = true ∧ ne = false ∧ sw = false ∧ se = true) := by
  cases nw <;> cases ne <;> cases sw <;> cases se <;> decide

/-- Unit input/output capacities imply a partial permutation; it extends. -/
theorem two_track_extension (a00 a01 a10 a11 : Bool) :
    (bit a00 + bit a01 ≤ 1 ∧ bit a10 + bit a11 ≤ 1 ∧
     bit a00 + bit a10 ≤ 1 ∧ bit a01 + bit a11 ≤ 1) →
    (a01 = false ∧ a10 = false) ∨ (a00 = false ∧ a11 = false) := by
  cases a00 <;> cases a01 <;> cases a10 <;> cases a11 <;> decide

def oldCut (entry0 entry1 stub0 stub1 tail0 tail1 : Bool) : Nat :=
  cut entry0 stub0 + cut entry1 stub1 + cut stub0 tail0 + cut stub1 tail1

def relaxedCut (entry0 entry1 stub0 stub1 tail0 tail1 : Bool) : Nat :=
  oldCut entry0 entry1 stub0 stub1 tail0 tail1 + cut stub0 tail1 + cut stub1 tail0

/-- If both new arcs cross, move both stubs far. Otherwise add at most one.
External resource arcs only leave stubs, so that move cannot add their cost. -/
theorem local_cut_repair (e0 e1 s0 s1 t0 t1 : Bool) :
    if (s0 && !t1 && s1 && !t0) then
      cut e0 false + cut e1 false ≤ oldCut e0 e1 s0 s1 t0 t1
    else
      relaxedCut e0 e1 s0 s1 t0 t1 ≤ oldCut e0 e1 s0 s1 t0 t1 + 1 := by
  cases e0 <;> cases e1 <;> cases s0 <;> cases s1 <;> cases t0 <;> cases t1 <;> decide

theorem sum_cut_repairs (ps : List (Nat × Nat))
    (h : ∀ p ∈ ps, p.2 ≤ p.1 + 1) :
    (ps.map Prod.snd).sum ≤ (ps.map Prod.fst).sum + ps.length := by
  induction ps with
  | nil => simp
  | cons p ps ih =>
    have hp := h p (by simp)
    have ht := ih (by intro q hq; exact h q (by simp [hq]))
    simp only [List.map_cons, List.sum_cons, List.length_cons]
    omega

theorem sharp_gain (old best q : Nat) (h : old ≤ best) (cap : best ≤ old + q) :
    best - old ≤ q := by omega

theorem separated_copy_counts (q : Nat) :
    26*q + 33*q = 59*q ∧ 2*(33*q) = 66*q := by omega

#print axioms pinwheel_classification
#print axioms two_track_extension
#print axioms local_cut_repair
#print axioms sum_cut_repairs
#print axioms sharp_gain
#print axioms separated_copy_counts

end SubQuorum.PinwheelTwoTrackSwitches
