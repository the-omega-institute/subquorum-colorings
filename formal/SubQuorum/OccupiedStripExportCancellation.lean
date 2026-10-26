import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.OccupiedStripExportCancellation

/-- Actual mate uniqueness and one endpoint per BP column make refund targets
injective, including across different strips and strip directions. -/
theorem distinct_BP_targets {X V C : Type} (source : X → V)
    (endpoint : C → V) (target : X → C) (mate : V → V)
    (source_injective : ∀ x y, source x = source y → x = y)
    (involution : ∀ v, mate (mate v) = v)
    (actual : ∀ x, mate (source x) = endpoint (target x)) :
    ∀ x y, target x = target y → x = y := by
  intro x y equal
  apply source_injective x y
  have matched : mate (source x) = mate (source y) := by
    rw [actual x, actual y, equal]
  have original := congrArg mate matched
  simpa only [involution] using original

/-- Each side site already has its central P neighbor. If it is selected,
its adjacent side site must therefore be blank. 0=B, 1=T, 2=P. -/
def sideCompatible (a c : Fin 3) : Prop :=
  (a.val = 1 → c.val = 0) ∧ (c.val = 1 → a.val = 0)

instance (a c : Fin 3) : Decidable (sideCompatible a c) :=
  inferInstanceAs (Decidable ((a.val = 1 → c.val = 0) ∧ (c.val = 1 → a.val = 0)))

/-- A transverse TP-to-BP actual matching edge between parallel bands,
with both P endpoints of occupied degree >=3, forces a P-square on at least
one side. Its opposite axial neighbors are respectively T and blank;
the degree conditions give the four hypotheses below. -/
theorem parallel_export_forces_square (a b c d : Fin 3)
    (left : sideCompatible a c) (right : sideCompatible b d)
    (top_degree : a.val ≠ 0 ∨ b.val ≠ 0)
    (bottom_left : c.val ≠ 0) (bottom_right : d.val ≠ 0) :
    (a.val = 2 ∧ c.val = 2) ∨ (b.val = 2 ∧ d.val = 2) := by
  have checked : ∀ a b c d : Fin 3,
      sideCompatible a c → sideCompatible b d →
      (a.val ≠ 0 ∨ b.val ≠ 0) → c.val ≠ 0 → d.val ≠ 0 →
      ((a.val = 2 ∧ c.val = 2) ∨ (b.val = 2 ∧ d.val = 2)) := by decide
  exact checked a b c d left right top_degree bottom_left bottom_right

/-- Global column counts cancel all TP-BP matches, including cross-strip
ones. A TP-TP edge contributes two TP endpoints but only one unit debit. -/
theorem exact_joint_flux
    (surplusTwice forest BP TP good unused tp_tp tp_pp exterior : Int)
    (columns : surplusTwice = 2 * forest + BP - TP)
    (tp_ledger : TP = good + 2 * tp_tp + tp_pp + exterior)
    (bp_ledger : BP = good + unused) :
    surplusTwice = 2 * forest + unused - 2 * tp_tp - tp_pp - exterior := by
  omega

/-- Boundary forest surplus gives the corrected budget for arbitrary
mixed-direction disjoint regions. Refunds are already inside this budget. -/
theorem corrected_union_bound
    (surplusTwice forest boundary unused tp_tp tp_pp exterior : Int)
    (identity : surplusTwice = 2 * forest + unused - 2 * tp_tp - tp_pp - exterior)
    (forest_bound : boundary ≤ forest) (unused_nonnegative : 0 ≤ unused) :
    2 * boundary - 2 * tp_tp - tp_pp - exterior ≤ surplusTwice := by
  omega

/-- Matching closure of each strip is unnecessary: it suffices that all
TP endpoints have BP mates somewhere in the union. -/
theorem safe_union_debit_free
    (surplusTwice forest boundary unused : Int)
    (identity : surplusTwice = 2 * forest + unused)
    (forest_bound : boundary ≤ forest) (unused_nonnegative : 0 ≤ unused) :
    2 * boundary ≤ surplusTwice := by
  omega

/-- The outside RAW tile-block ledger uses each original tile once.
No assumption about an individual strip containing whole receivers is used. -/
theorem original_grid_compensation
    (marginTwice regionalTwice forest unused tp_tp tp_pp exterior
      outsideDeficit outsidePositiveTwice outsideNegativeTwice : Int)
    (regional : regionalTwice = 2 * forest + unused - 2 * tp_tp - tp_pp - exterior)
    (partition : marginTwice = regionalTwice + 2 * outsideDeficit -
      outsidePositiveTwice + outsideNegativeTwice)
    (covered : outsidePositiveTwice + 2 * tp_tp + tp_pp + exterior ≤ 2 * forest + unused)
    (deficit_nonnegative : 0 ≤ outsideDeficit)
    (negative_nonnegative : 0 ≤ outsideNegativeTwice) :
    0 ≤ marginTwice := by
  omega

end SubQuorum.OccupiedStripExportCancellation

#print axioms SubQuorum.OccupiedStripExportCancellation.distinct_BP_targets
#print axioms SubQuorum.OccupiedStripExportCancellation.parallel_export_forces_square
#print axioms SubQuorum.OccupiedStripExportCancellation.exact_joint_flux
#print axioms SubQuorum.OccupiedStripExportCancellation.corrected_union_bound
#print axioms SubQuorum.OccupiedStripExportCancellation.safe_union_debit_free
#print axioms SubQuorum.OccupiedStripExportCancellation.original_grid_compensation
