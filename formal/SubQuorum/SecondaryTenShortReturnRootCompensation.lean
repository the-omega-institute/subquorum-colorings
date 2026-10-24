import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenShortReturnRootCompensation

abbrev Point := Int × Int

def blocked (point : Point) : Prop :=
  (point.2 = -1 ∧ 23 ≤ point.1 ∧ point.1 ≤ 33) ∨
  (point.2 = 1 ∧ 25 ≤ point.1 ∧ point.1 ≤ 31) ∨ point = (31,0)

def avoids (fresh : Point → Prop) : Prop :=
  ∀ point, blocked point → ¬fresh point

theorem early_support_rotor_excluded (fresh : Point → Prop) (row : Int)
    (hrow : 26 ≤ row ∧ row ≤ 30) (hfork : fresh (row+2,-1))
    (havoid : avoids fresh) : False := by
  exact havoid (row+2,-1) (by simp [blocked]; omega) hfork

theorem early_support_long_stem_excluded (fresh : Point → Prop) (row depth : Int)
    (hrow : 26 ≤ row ∧ row ≤ 30) (hreach : 31 ≤ row+depth)
    (hstem : ∀ step, 0 ≤ step → step ≤ depth → fresh (row+step,0))
    (havoid : avoids fresh) : False := by
  have hcollision : fresh (31,0) := by
    have hpoint := hstem (31-row) (by omega) (by omega)
    have hrow31 : row+(31-row) = 31 := by omega
    simpa only [hrow31] using hpoint
  exact havoid (31,0) (by simp [blocked]) hcollision

theorem early_support_short_stem_excluded (fresh : Point → Prop) (east : Bool)
    (hcompanion : fresh (30,if east then 1 else -1))
    (havoid : avoids fresh) : False := by
  cases east with
  | false => exact havoid (30,-1) (by simp [blocked]) hcompanion
  | true => exact havoid (30,1) (by simp [blocked]) hcompanion

theorem every_early_support_U_excluded (fresh : Point → Prop) (row depth : Int)
    (hrow : 26 ≤ row ∧ row ≤ 30) (hdepth : 4 ≤ depth)
    (heven : depth % 2 = 0)
    (hstem : ∀ step, 0 ≤ step → step ≤ depth → fresh (row+step,0))
    (hbar : ∃ east : Bool, fresh (row+depth,if east then 1 else -1))
    (havoid : avoids fresh) : False := by
  by_cases hreach : 31 ≤ row+depth
  · exact early_support_long_stem_excluded fresh row depth hrow hreach hstem havoid
  · have hrow26 : row = 26 := by omega
    have hdepth4 : depth = 4 := by omega
    rcases hbar with ⟨east,hcompanion⟩
    apply early_support_short_stem_excluded fresh east _ havoid
    simpa [hrow26,hdepth4] using hcompanion

theorem root_tip_is_thirty (tip : Int) (hinterval : 25 ≤ tip ∧ tip ≤ 30)
    (hclosure : tip < 30 → ∃ fresh : Point → Prop, avoids fresh ∧
      ((∃ depth : Int, 4 ≤ depth ∧ depth % 2 = 0 ∧
        (∀ step, 0 ≤ step → step ≤ depth → fresh (tip+1+step,0)) ∧
        (∃ east : Bool, fresh (tip+1+depth,if east then 1 else -1))) ∨
        fresh (tip+1+2,-1))) : tip = 30 := by
  by_cases hearly : tip < 30
  · rcases hclosure hearly with ⟨fresh,havoid,hroles⟩
    rcases hroles with ⟨depth,hdepth,heven,hstem,hbar⟩ | hfork
    · exact False.elim (every_early_support_U_excluded fresh (tip+1) depth
        (by omega) hdepth heven hstem hbar havoid)
    · exact False.elim (early_support_rotor_excluded fresh (tip+1) (by omega) hfork havoid)
  · omega

theorem root_bar_parity (bar depth : Int) (htip : bar+depth = 30)
    (heven : depth % 2 = 0) : bar % 2 = 0 := by omega

theorem root_bar_bound (bar : Int) (hbar : bar ≤ 24) (heven : bar % 2 = 0)
    (hinner : bar ≠ 24) : bar ≤ 22 := by omega

theorem west_bar_bound (bar : Int) (hbar : bar ≤ 22) (heven : bar % 2 = 0)
    (hinner : bar ≠ 22) : bar ≤ 20 := by omega

theorem crossing_bar_frontier (bar top : Int)
    (hbar : bar % 2 = 0) (htop : top % 2 = 1) :
    bar+1 < top ↔ bar ≤ top-3 := by omega

theorem root_source_receipt (deduction : Int) :
    1+2*4-(8+deduction) = 1-deduction := by omega

theorem root_marginal_nonnegative (deduction : Int)
    (hdelta : deduction = 0 ∨ deduction = 1) :
    0 ≤ 1+2*4-(8+deduction) := by omega

theorem selected_group_receipt (halfDepth deduction : Int) :
    1+(2-halfDepth)+(1-deduction) = 4-halfDepth-deduction := by omega

theorem selected_absolute_budget (width halfDepth deduction : Int)
    (hdepth : 2*halfDepth ≤ width+4) (hdelta : 0 ≤ deduction ∧ deduction ≤ 1) :
    width/2+34 ≤ (width+33)+(4-halfDepth-deduction) := by omega

end SubQuorum.SecondaryTenShortReturnRootCompensation
