import SubQuorum.WidthSixBottomOwner

set_option autoImplicit false

namespace SubQuorum.NeutralPhaseTenDescent

open WidthSixBottomOwner

def phaseTenAtForcedPoint (flipRow flipColumn : Bool) (anchor : Point) : Prop :=
  anchor.1%2 = (if flipRow then 1 else 0) ∧
  anchor.2%2 = (if flipColumn then 0 else 1)

set_option maxHeartbeats 2000000 in
theorem phase_ten_forced_owner_is_north_terminal
    (width left right : Int) (anchor : Point)
    (transpose flipRow flipColumn : Bool)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ left) (hright : 4 ≤ right)
    (hevenWidth : width%2 = 0) (hevenLeft : left%2 = 0) (hevenRight : right%2 = 0)
    (hroot : endpoint width left right anchor)
    (hwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (0,-1)))
    (hsouth : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,0)))
    (hnorthwest : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (-1,-1)))
    (hsoutheast : ¬ endpoint width left right
      (pull transpose flipRow flipColumn anchor (1,1)))
    (hphase : phaseTenAtForcedPoint flipRow flipColumn anchor) :
    transpose = false ∧ flipRow = false ∧
      ((flipColumn = false ∧ anchor = (left,1)) ∨
       (flipColumn = true ∧ anchor = (right,width))) := by
  rcases anchor with ⟨row,column⟩
  rcases hroot with hbar | hnear | hfar
  all_goals
    cases transpose <;> cases flipRow <;> cases flipColumn <;>
      simp [endpoint, pull, phaseTenAtForcedPoint, Prod.mk.injEq] at hwest hsouth hnorthwest hsoutheast hphase ⊢ <;> omega

theorem phase_ten_terminal_owns_next_corner (width incident far : Int)
    (hwidth : 6 ≤ width) (hincident : 4 ≤ incident) :
    endpoint width incident far (incident-1,1) := by
  simp [endpoint]
  omega

theorem incident_height_strictly_decreases (active incoming : Int)
    (hactive : 4 ≤ active) (_hincoming : 4 ≤ incoming)
    (hevenActive : active%2 = 0) (hevenIncoming : incoming%2 = 0)
    (hdisjoint : ¬ (-incoming ≤ 2-active ∧ 2-active ≤ 0)) :
    incoming+4 ≤ active := by omega

theorem shortest_legs_exclude_phase_ten (active incoming : Int)
    (hactive : active = 4 ∨ active = 6) (hincoming : 4 ≤ incoming)
    (hdescent : incoming+4 ≤ active) : False := by omega

theorem minimal_height_descent_is_sharp (incoming : Int) :
    incoming+4-incoming = 4 := by omega

theorem iterated_descent_bound (height : Nat → Int) (length : Nat)
    (hstep : ∀ index, index+1 < length →
      height (index+1)+4 ≤ height index) :
    ∀ index, index < length →
      height index+4*(index : Int) ≤ height 0 := by
  intro index hindex
  induction index with
  | zero => simp
  | succ index ih =>
    have hprior : index < length := by omega
    have hbefore := ih hprior
    have hnext := hstep index (by omega)
    omega

end SubQuorum.NeutralPhaseTenDescent
