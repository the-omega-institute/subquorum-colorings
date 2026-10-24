import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenFirstConsumer

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 10 far (point.1-(bottom-11),point.2-5)

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def north (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 4 far (point.1-(bottom-9),point.2-6)

def corner (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 4 far (bottom-5-point.1,point.2-6)

def eastDown (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+7-point.2,point.1-(bottom-6))

def eastUp (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+7-point.2,bottom-4-point.1)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

theorem forcing_neighbors (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-5,6) ∧ returning bottom (bottom-4,7) ∧
      ¬secondary bottom width far (bottom-5,7) ∧ ¬returning bottom (bottom-5,7) := by
  unfold secondary returning endpoint
  dsimp
  omega

theorem fixed_rotor_blockers (bottom width far : Int) :
    secondary bottom width far (bottom-7,6) ∧ returning bottom (bottom-4,9) ∧
      returning bottom (bottom-4,10) := by
  unfold secondary returning endpoint
  dsimp
  omega

theorem north_stem_bound (length : Int) (hlength : 4 ≤ length)
    (heven : length % 2 = 0) (hblock : ¬(5 ≤ length)) : length = 4 := by
  omega

theorem north_bar_collision (bottom width far breadth other : Int)
    (hwidth : 6 ≤ width) (hfar : 4 ≤ far) (hlong : width ≤ breadth) :
    secondary bottom width far (bottom-9,width+5) ∧
      north bottom breadth other (bottom-9,width+5) := by
  unfold secondary north endpoint
  dsimp
  omega

theorem corner_long_far_collision (bottom width far breadth other : Int)
    (hbreadth : 6 ≤ breadth) (hother : 6 ≤ other) (hshort : breadth ≤ width-2) :
    secondary bottom width far (bottom-10,breadth+6) ∧
      corner bottom breadth other (bottom-10,breadth+6) := by
  unfold secondary corner endpoint
  dsimp
  omega

theorem corner_long_secondary_far_collision (bottom width far breadth other : Int)
    (hwidth : 6 ≤ width) (hfar : 6 ≤ far) (hlong : width ≤ breadth) :
    secondary bottom width far (bottom-5,width+5) ∧
      corner bottom breadth other (bottom-5,width+5) := by
  unfold secondary corner endpoint
  dsimp
  omega

theorem incompatible_corner_bounds (width breadth other : Int)
    (hother : 4 ≤ other) (heven : other % 2 = 0)
    (hshort : breadth ≤ width-2) (hlarge : 6 ≤ other → width ≤ breadth) :
    other = 4 := by
  by_cases hlong : 6 ≤ other
  · have hwidth := hlarge hlong
    omega
  · omega

theorem corner_support_images (bottom width far : Int) (hwidth : 6 ≤ width) :
    secondary bottom width far (bottom-10,7) ∧
      secondary bottom width far (bottom-9,6) ∧
      (bottom-5-5,1+6) = (bottom-10,7) ∧
      (bottom-5-4,0+6) = (bottom-9,6) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · unfold secondary endpoint
    dsimp
    omega
  · unfold secondary endpoint
    dsimp
    omega
  · apply Prod.ext <;> dsimp <;> omega
  · apply Prod.ext <;> dsimp <;> omega

theorem corner_intrinsic_terminal_and_supports (bottom width far : Int) :
    corner bottom width far (bottom-9,7) ∧
      support width 4 far (5,1) ∧ support width 4 far (4,0) := by
  unfold corner endpoint support
  dsimp
  omega

theorem upward_far_must_be_four (width incident far : Int)
    (hfar : 4 ≤ far) (heven : far % 2 = 0) (hlong : width ≤ incident)
    (hbarrier : 6 ≤ far → incident ≤ width-4) : far = 4 := by
  by_cases hlarge : 6 ≤ far
  · have hshort := hbarrier hlarge
    omega
  · omega

theorem east_down_length_four_collision (bottom width far : Int)
    (hwidth : 6 ≤ width) :
    returning bottom (bottom-4,11) ∧ eastDown bottom width 4 far (bottom-4,11) := by
  unfold returning eastDown endpoint
  dsimp
  omega

theorem east_incident_collision (bottom width far breadth incident other : Int)
    (hwidth : 6 ≤ width) (hfar : 6 ≤ far) (hbreadth : 6 ≤ breadth)
    (hlong : width-2 ≤ incident) :
    secondary bottom width far (bottom-5,width+5) ∧
      eastDown bottom breadth incident other (bottom-5,width+5) ∧
      eastUp bottom breadth incident other (bottom-5,width+5) := by
  unfold secondary eastDown eastUp endpoint
  dsimp
  omega

theorem east_up_bar_collision (bottom width far breadth incident other : Int)
    (hbreadth : 6 ≤ breadth) (hincident : 4 ≤ incident)
    (hshort : incident ≤ width-2) :
    secondary bottom width far (bottom-10,incident+7) ∧
      eastUp bottom breadth incident other (bottom-10,incident+7) := by
  unfold secondary eastUp endpoint
  dsimp
  omega

theorem north_charge (width legs matching inside tiles : Int)
    (hmatching : matching = width-1+legs) (hinside : inside = legs+2)
    (htiles : tiles = width+legs) : matching+inside-2*tiles = 1-width := by
  omega

theorem positive_charge (halfWidth legs matching inside tiles : Int)
    (hmatching : matching = 2*halfWidth-1+legs) (hinside : inside = legs+4)
    (htiles : tiles = halfWidth+legs+1) : matching+inside-2*tiles = 1 := by
  omega

theorem east_up_charge (halfWidth legs matching inside tiles : Int)
    (hmatching : matching = 2*halfWidth-1+legs) (hinside : inside = legs)
    (htiles : tiles = halfWidth+legs) : matching+inside-2*tiles = -1 := by
  omega

end SubQuorum.SecondaryTenFirstConsumer
