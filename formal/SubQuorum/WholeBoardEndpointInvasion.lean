import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 16384
set_option maxHeartbeats 0

namespace SubQuorum.WholeBoardEndpointInvasion

/-- A two-demand selector and a one-demand selector fit in the same triple. -/
theorem triple_budget (C f u v w : Nat) (_hC : C≤1) (hf : f≤1)
    (hc : 2*C≤u+v+w) (hfv : f≤v) : C+f≤u+v+w := by
  omega

/-- The four-hole helper used in the explicit pocket case proof. -/
theorem four_hole_budget (C f E w y z q : Nat)
    (hC : C≤1) (_hf : f≤1) (hE : E≤1)
    (hc : 3*C≤w+y+z+q) (hff : 2*f≤z+q)
    (he : E≤w+q) : C+f+E≤w+y+z+q := by
  omega

/-- Injective mates for the two occupied white sites use distinct available
    black sites. The coordinate injection is a written geometric premise. -/
theorem two_site_actual_mate_capacity (D occupied r s : Nat)
    (hocc : occupied+r+s=2) (hcap : D+occupied≤4) : D≤2+r+s := by
  omega

/-- The local nine-hole compensation lemma. All variables are binary; blanks
    mean genuinely empty sites. Hall is the actual two-site matching capacity.
    No freezing assumption or local colour balance is used. -/
theorem pocket_budget (a b C d e f g h u v w x y z q r s : Nat)
    (_ha : a≤1) (hb : b≤1) (hC : C≤1) (_hd : d≤1)
    (he : e≤1) (hf : f≤1) (_hg : g≤1) (hh : h≤1)
    (_hu : u≤1) (hv : v≤1) (hw : w≤1) (hx : x≤1)
    (hy : y≤1) (hz : z≤1) (hq : q≤1) (hr : r≤1) (hs : s≤1)
    (hau : a≤u) (hbv : b≤v) (hbw : b≤w) (hbx : b≤x)
    (hcz : 3*C≤w+y+z+q) (hdv : 2*d≤v+x+r)
    (hew : 3*e≤w+x+q+s) (hfz : f≤z) (hfq : f≤q)
    (hgx : 2*g≤x+r+s) (hhq : h≤q+s)
    (hall : d+e+g+h≤2+r+s) :
    a+b+C+d+e+f+g+h≤u+v+w+x+y+z+q+r+s := by
  have htr0 := triple_budget C f w z y hC hf (by omega) hfz
  have htr : C+f≤w+y+z := by omega
  have htr' : C+f≤y+z+q :=
    triple_budget C f y z q hC hf (by omega) hfz
  have hff : 2*f≤z+q := by omega
  have rs : (r=0 ∨ r=1) ∧ (s=0 ∨ s=1) := by omega
  rcases rs with ⟨hr0 | hr1, hs0 | hs1⟩
  · -- r=s=0: split on the single remaining bottom neighbour q.
    have hqcases : q=0 ∨ q=1 := by omega
    rcases hqcases with hq0 | hq1
    · omega
    · have hxcases : x=0 ∨ x=1 := by omega
      rcases hxcases with hx0 | hx1
      · omega
      · omega
  · -- r=0,s=1: v=0 uses the four-hole helper; v=1 uses the triple.
    have hewq : e≤w+q := by omega
    have hfour := four_hole_budget C f e w y z q hC hf he hcz hff hewq
    have hvcases : v=0 ∨ v=1 := by omega
    rcases hvcases with hv0 | hv1
    · omega
    · omega
  · -- r=1,s=0: e=1 invokes Hall, and e=0 uses its local degree bounds.
    have hecases : e=0 ∨ e=1 := by omega
    rcases hecases with he0 | he1
    · omega
    · omega
  · -- r=s=1: b+d<=v+x and the four-hole helper suffice.
    have hewq : e≤w+q := by omega
    have hfour := four_hole_budget C f e w y z q hC hf he hcz hff hewq
    omega

/-- The disjoint physical pocket/tail partition supplies the two equalities
    and inequalities below. This makes the exact nonreuse budget explicit. -/
theorem whole_board_count (Tb Tp Tt Hw Hp Hl Ho : Nat)
    (hT : Tb=Tp+Tt) (hH : Hw=Hp+Hl+Ho)
    (hp : Tp≤Hp) (hl : Tt≤Hl) :
    Tb≤Hw ∧ Hw-Tb=(Hp-Tp)+(Hl-Tt)+Ho := by
  omega

/-- Bipartite colour balance and the preceding empty-site budget imply the
    sharp half-area objective bound. The adapter supplies the cardinalities. -/
theorem objective_half_area (J Tb Ow Hw white : Nat)
    (hJ : J=Tb+Ow) (hW : white=Ow+Hw) (hbudget : Tb≤Hw) : J≤white := by
  omega

end SubQuorum.WholeBoardEndpointInvasion
#print axioms SubQuorum.WholeBoardEndpointInvasion.triple_budget
#print axioms SubQuorum.WholeBoardEndpointInvasion.four_hole_budget
#print axioms SubQuorum.WholeBoardEndpointInvasion.two_site_actual_mate_capacity
#print axioms SubQuorum.WholeBoardEndpointInvasion.pocket_budget
#print axioms SubQuorum.WholeBoardEndpointInvasion.whole_board_count
#print axioms SubQuorum.WholeBoardEndpointInvasion.objective_half_area
