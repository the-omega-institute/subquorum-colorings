import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.GapEightSuccessorReturn

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  endpoint width height far (height+2-point.2,point.1-1)

def returnEndpoint (width near far crossWidth height incident : Int)
    (point : Point) : Prop :=
  endpoint width near far (height+near-incident-point.2,crossWidth+2-point.1)

theorem forced_third_source_and_cross_share_an_endpoint
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hincident : 4 ≤ incident) (hnear : incident+2 ≤ returnNear) :
    crossEndpoint width height far (width+1,height+1) ∧
      returnEndpoint returnWidth returnNear returnFar width height incident
        (width+1,height+1) := by
  unfold crossEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem equal_endpoint_sets_force_the_return_length_identity
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hfar : 4 ≤ far) (hincident : 4 ≤ incident)
    (hnear : incident+2 ≤ returnNear)
    (hsame : ∀ point, crossEndpoint width height far point ↔
      returnEndpoint returnWidth returnNear returnFar width height incident point) :
    returnNear = incident+2 ∧ far = incident+2 := by
  have htop := (hsame (width+1,height+returnNear-incident)).mpr
  have hbottom := (hsame (width+1,height-incident)).mpr
  have hcrossbottom := (hsame (width+1,height+2-far)).mp
  unfold crossEndpoint returnEndpoint endpoint at htop hbottom hcrossbottom
  dsimp at htop hbottom hcrossbottom
  omega

theorem unequal_return_lengths_exclude_equal_endpoint_sets
    (width height far returnWidth returnNear returnFar incident : Int)
    (hwidth : 10 ≤ width) (hreturn : 6 ≤ returnWidth)
    (hfar : 4 ≤ far) (hincident : 4 ≤ incident)
    (hnear : incident+2 ≤ returnNear) (hunmatched : far ≠ incident+2) :
    ¬(∀ point, crossEndpoint width height far point ↔
      returnEndpoint returnWidth returnNear returnFar width height incident point) := by
  intro hsame
  exact hunmatched (equal_endpoint_sets_force_the_return_length_identity
    width height far returnWidth returnNear returnFar incident
    hwidth hreturn hfar hincident hnear hsame).2

theorem a_short_cross_far_leg_cannot_match_the_positive_successor
    (far incident other : Int) (hfar : far ≤ other+4)
    (hgrowth : other+4 ≤ incident) : far ≠ incident+2 := by
  omega

end SubQuorum.GapEightSuccessorReturn
