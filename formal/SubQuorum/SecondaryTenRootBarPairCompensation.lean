import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootBarPairCompensation

abbrev Point := Int × Int

def blocked (top rootBar : Int) (point : Point) : Prop :=
  (point.2 = -1 ∧ top ≤ point.1 ∧ point.1 ≤ 22) ∨
  (point.2 = 1 ∧ rootBar ≤ point.1 ∧ point.1 ≤ 30) ∨ point = (23,0)

def avoids (top rootBar : Int) (fresh : Point → Prop) : Prop :=
  ∀ point, blocked top rootBar point → ¬fresh point

theorem support_neighbours_blocked (top rootBar : Int)
    (htop : top ≤ 17) (hroot : rootBar ≤ 22) :
    blocked top rootBar (22,-1) ∧ blocked top rootBar (22,1) ∧
      blocked top rootBar (23,0) := by
  constructor
  · exact Or.inl ⟨rfl,by omega,by omega⟩
  · constructor
    · exact Or.inr (Or.inl ⟨rfl,by omega,by omega⟩)
    · exact Or.inr (Or.inr rfl)

theorem matching_forces_north (top rootBar : Int) (fresh : Point → Prop)
    (htop : top ≤ 17) (hroot : rootBar ≤ 22)
    (havoid : avoids top rootBar fresh)
    (hmatched : ∃ other : Point,
      (other = (21,0) ∨ other = (23,0) ∨ other = (22,-1) ∨ other = (22,1)) ∧
      fresh other) : fresh (21,0) := by
  rcases support_neighbours_blocked top rootBar htop hroot with ⟨hwest,heast,hsouth⟩
  rcases hmatched with ⟨other,hnorth | hsouthEq | hwestEq | heastEq,hother⟩
  · exact hnorth ▸ hother
  · exact False.elim (havoid (23,0) hsouth (hsouthEq ▸ hother))
  · exact False.elim (havoid (22,-1) hwest (hwestEq ▸ hother))
  · exact False.elim (havoid (22,1) heast (heastEq ▸ hother))

theorem north_rotor_excluded (top rootBar : Int) (fresh : Point → Prop)
    (htop : top ≤ 17) (hfork : fresh (20,-1))
    (havoid : avoids top rootBar fresh) : False := by
  exact havoid (20,-1) (by simp [blocked]; omega) hfork

theorem terminal_bar_bound (bar depth : Int) (htip : bar+depth = 22)
    (hdepth : 4 ≤ depth) (heven : depth % 2 = 0) :
    bar ≤ 18 ∧ bar % 2 = 0 := by omega

theorem east_bar_frontier (top rootBar bar : Int) (fresh : Point → Prop)
    (hbar : bar ≤ 18) (heven : bar % 2 = 0) (hrootEven : rootBar % 2 = 0)
    (hinner : fresh (bar+1,1)) (havoid : avoids top rootBar fresh) :
    bar ≤ rootBar-2 := by
  by_cases hbefore : bar+1 < rootBar
  · omega
  · have hblocked : blocked top rootBar (bar+1,1) := by simp [blocked]; omega
    exact False.elim (havoid (bar+1,1) hblocked hinner)

theorem west_bar_frontier (top rootBar bar : Int) (fresh : Point → Prop)
    (hbar : bar ≤ 18) (heven : bar % 2 = 0) (htop : top % 2 = 1)
    (hinner : fresh (bar+1,-1)) (havoid : avoids top rootBar fresh) :
    bar ≤ top-3 := by
  by_cases hbefore : bar+1 < top
  · omega
  · have hblocked : blocked top rootBar (bar+1,-1) := by simp [blocked]; omega
    exact False.elim (havoid (bar+1,-1) hblocked hinner)

theorem east_near_receipt (halfBand : Int) :
    1+2*(halfBand+1)-(2*halfBand+2) = 1 := by omega

theorem west_near_receipt (halfBand : Int) :
    1+2*(halfBand+1)-(2*halfBand+1) = 2 := by omega

theorem far_band_receipt (halfBand : Int) :
    2*halfBand-(2*halfBand+1) = -1 := by omega

theorem east_exact_marginal (nearBand farBand eta cap triple : Int) :
    1+2*(nearBand+1+farBand+triple)-
      (2*nearBand+2+2*farBand+eta+cap) = 1-eta-cap+2*triple := by omega

theorem joint_pair_nonnegative (delta eta cap triple : Int)
    (hdelta : delta = 0 ∨ delta = 1) (heta : eta = 0 ∨ eta = 1)
    (hcap : cap = 0 ∨ cap = 1) (htriple : triple = cap*delta) :
    0 ≤ (1-delta)+(1-eta-cap+2*triple) := by
  rcases hdelta with hdelta | hdelta <;>
    rcases hcap with hcap | hcap <;>
    simp_all <;> omega

theorem west_joint_pair_bound (delta : Int) (hdelta : delta = 0 ∨ delta = 1) :
    2 ≤ (1-delta)+2 := by omega

theorem separate_marginal_lower_bound (eta cap triple : Int)
    (heta : eta = 0 ∨ eta = 1) (hcap : cap = 0 ∨ cap = 1)
    (htriple : 0 ≤ triple) : -1 ≤ 1-eta-cap+2*triple := by omega

theorem sharp_receipt : (1 : Int)+2*5-12 = -1 ∧ 1+(-1) = 0 := by omega

theorem maximal_return_absolute_bound (width halfWidth joint : Int)
    (hwidth : width = 2*halfWidth) (hjoint : 0 ≤ joint) :
    halfWidth+34 ≤ width+36-(halfWidth+2)+joint := by omega

end SubQuorum.SecondaryTenRootBarPairCompensation
