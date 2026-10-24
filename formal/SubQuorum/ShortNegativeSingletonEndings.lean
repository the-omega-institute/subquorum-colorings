import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.ShortNegativeSingletonEndings

abbrev Point := Int × Int

def uEndpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def terminalEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.1,point.2-1)

def crossEndpoint (width height far : Int) (point : Point) : Prop :=
  uEndpoint width height far (height+2-point.2,point.1-1)

def eastEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.2,point.1-2)

def southEndpoint (width near far : Int) (point : Point) : Prop :=
  uEndpoint width near far (near+3-point.1,point.2-2)

def inside (width : Int) (point : Point) : Prop :=
  2 < point.1 ∧ point.1 < 6 ∧ 2 < point.2 ∧ point.2 < width+1

def boundary (width : Int) (point : Point) : Prop :=
  2 ≤ point.1 ∧ point.1 ≤ 6 ∧ 2 ≤ point.2 ∧ point.2 ≤ width+1 ∧
    (point.1 = 2 ∨ point.1 = 6 ∨ point.2 = 2 ∨ point.2 = width+1)

theorem a_length_four_singleton_requires_height_at_least_width_plus_two
    (width far crossWidth height crossFar halfWidth halfHeight : Int)
    (_hwidth : 6 ≤ width) (hheight : 4 ≤ height) (hcross : 6 ≤ crossWidth)
    (hweven : width = 2*halfWidth) (hheven : height = 2*halfHeight)
    (hdisjoint : ∀ point, terminalEndpoint width 4 far point →
      ¬crossEndpoint crossWidth height crossFar point) :
    width+2 ≤ height := by
  by_cases hbound : width+2 ≤ height
  · exact hbound
  have hterminal : terminalEndpoint width 4 far (6,height+1) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  have hbar : crossEndpoint crossWidth height crossFar (6,height+1) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (6,height+1) hterminal hbar)

theorem the_length_four_rectangle_has_an_original_endpoint_boundary
    (width far crossWidth height crossFar : Int) (point : Point)
    (_hwidth : 6 ≤ width) (hfar : 4 ≤ far) (hheight : width+2 ≤ height)
    (hboundary : boundary width point) :
    terminalEndpoint width 4 far point ∨ crossEndpoint crossWidth height crossFar point := by
  unfold boundary at hboundary
  unfold terminalEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem the_length_four_rectangle_has_no_endpoints_of_either_boundary_owner
    (width far crossWidth height crossFar : Int) (point : Point)
    (_hwidth : 6 ≤ width) (hcross : 6 ≤ crossWidth) (hheight : width+2 ≤ height)
    (hinside : inside width point) :
    ¬terminalEndpoint width 4 far point ∧ ¬crossEndpoint crossWidth height crossFar point := by
  unfold inside at hinside
  unfold terminalEndpoint crossEndpoint uEndpoint
  dsimp
  omega

theorem the_forced_support_is_strictly_inside_the_length_four_rectangle
    (width : Int) (hwidth : 6 ≤ width) : inside width (3,3) := by
  unfold inside
  dsimp
  omega

theorem the_east_companion_leg_is_at_least_the_singleton_width
    (width far companionWidth incident other halfWidth halfIncident : Int)
    (_hwidth : 6 ≤ width) (hcompanion : 6 ≤ companionWidth) (hincident : 4 ≤ incident)
    (hweven : width = 2*halfWidth) (hieven : incident = 2*halfIncident)
    (hdisjoint : ∀ point, eastEndpoint companionWidth incident other point →
      ¬terminalEndpoint width 6 far point) : width ≤ incident := by
  by_cases hbound : width ≤ incident
  · exact hbound
  have heast : eastEndpoint companionWidth incident other (8,incident+2) := by
    unfold eastEndpoint uEndpoint
    dsimp
    omega
  have hbar : terminalEndpoint width 6 far (8,incident+2) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (8,incident+2) heast hbar)

theorem the_east_branch_requires_producer_width_at_least_fourteen
    (producerWidth height incident singletonWidth : Int)
    (hsingleton : 6 ≤ singletonWidth) (hincident : singletonWidth ≤ incident)
    (hgap : incident+4 ≤ height) (hproducer : height ≤ producerWidth-4) :
    14 ≤ producerWidth := by
  omega

theorem the_south_companion_has_incident_leg_four
    (width far companionWidth incident other halfIncident : Int)
    (hwidth : 6 ≤ width) (hcompanion : 6 ≤ companionWidth) (hincident : 4 ≤ incident)
    (hieven : incident = 2*halfIncident)
    (hdisjoint : ∀ point, southEndpoint companionWidth incident other point →
      ¬terminalEndpoint width 6 far point) : incident = 4 := by
  by_cases hequal : incident = 4
  · exact hequal
  have hsouth : southEndpoint companionWidth incident other (8,3) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hbar : terminalEndpoint width 6 far (8,3) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (8,3) hsouth hbar)

theorem the_south_companion_far_leg_is_also_four
    (companionWidth other crossWidth height crossFar halfOther : Int)
    (hcompanion : 6 ≤ companionWidth) (hother : 4 ≤ other)
    (hoeven : other = 2*halfOther) (hgap : companionWidth ≤ height-2)
    (hdisjoint : ∀ point, southEndpoint companionWidth 4 other point →
      ¬crossEndpoint crossWidth height crossFar point) : other = 4 := by
  by_cases hequal : other = 4
  · exact hequal
  have hsouth : southEndpoint companionWidth 4 other (2,companionWidth+2) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hcross : crossEndpoint crossWidth height crossFar (2,companionWidth+2) := by
    unfold crossEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (2,companionWidth+2) hsouth hcross)

theorem no_original_producer_endpoint_has_column_zero
    (width near far row : Int) (hwidth : 6 ≤ width) : ¬uEndpoint width near far (row,0) := by
  unfold uEndpoint
  dsimp
  omega

theorem the_south_companion_is_narrower_than_the_singleton
    (width far companionWidth other halfWidth halfCompanion : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ far)
    (hweven : width = 2*halfWidth) (hceven : companionWidth = 2*halfCompanion)
    (hdisjoint : ∀ point, southEndpoint companionWidth 4 other point →
      ¬terminalEndpoint width 6 far point) : companionWidth ≤ width-2 := by
  by_cases hbound : companionWidth ≤ width-2
  · exact hbound
  have hsouth : southEndpoint companionWidth 4 other (6,width+1) := by
    unfold southEndpoint uEndpoint
    dsimp
    omega
  have hterminal : terminalEndpoint width 6 far (6,width+1) := by
    unfold terminalEndpoint uEndpoint
    dsimp
    omega
  exact False.elim (hdisjoint (6,width+1) hsouth hterminal)

theorem resolving_short_singletons_strengthens_the_residual_floor
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred ≤ activation) (hpairs : resolved ≤ lower)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve) :
    unmarked+upper+(lower+prior-residual+1)/2 ≤ positive+reserve-marked := by
  omega

theorem the_reduced_residual_threshold_implies_allocation
    (positive marked transferred caps resolved residual activation prior upper lower
      reserve unmarked : Int)
    (hmarks : marked ≤ 2*(positive-unmarked))
    (hpartition : marked = transferred+caps+resolved+residual)
    (hinjection : transferred ≤ activation) (hpairs : resolved ≤ lower)
    (hfloor : activation+prior+caps+2*upper+2*lower ≤ 2*reserve)
    (hcoverage : residual ≤ 2*unmarked+2*upper+lower+prior+1) :
    0 ≤ positive+reserve-marked := by
  omega

end SubQuorum.ShortNegativeSingletonEndings
