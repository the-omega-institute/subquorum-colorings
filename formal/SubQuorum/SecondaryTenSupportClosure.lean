import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenSupportClosure

abbrev Point := Int × Int

def endpoint (width near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = width)

def support (width near far : Int) (point : Point) : Prop :=
  (point.1 = 0 ∧ (point.2 = 0 ∨ point.2 = width+1)) ∨
  (point.1 = near+1 ∧ point.2 = 1) ∨
  (point.1 = far+1 ∧ point.2 = width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧
    ((point.1 % 2 = 0 ∧ point.2 = 0) ∨ (point.1 % 2 = 1 ∧ point.2 = 2))) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧
    ((point.1 % 2 = 0 ∧ point.2 = width+1) ∨
      (point.1 % 2 = 1 ∧ point.2 = width-1)))

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def northern (bottom far : Int) (point : Point) : Prop :=
  endpoint 6 4 far (point.1-(bottom-9),point.2-6)

def secondary (bottom width : Int) (point : Point) : Prop :=
  endpoint width 10 4 (point.1-(bottom-11),point.2-5)

def upward (bottom width incident far : Int) (point : Point) : Prop :=
  endpoint width incident far (incident+7-point.2,bottom-4-point.1)

def successor (bottom bar width near far : Int) (point : Point) : Prop :=
  endpoint width near far (bar-point.2,bottom-5-point.1)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def forbidden (bottom : Int) (point : Point) : Prop :=
  point = (bottom-8,11) ∨ point = (bottom-5,7) ∨
  point = (bottom-4,8) ∨ point = (bottom-4,9) ∨
  point = (bottom-8,10) ∨ point = (bottom-8,12)

theorem north_support_and_forcing_neighbors (bottom far : Int) (hfar : 4 ≤ far) :
    support 6 8 4 (0,7) ∧ returning bottom (bottom-4,11) ∧
      northern bottom far (bottom-5,12) := by
  unfold support returning northern endpoint
  dsimp
  omega

theorem north_forced_point_has_neither_prescribed_owner (bottom far : Int) :
    ¬returning bottom (bottom-5,11) ∧ ¬northern bottom far (bottom-5,11) := by
  unfold returning northern endpoint
  dsimp
  omega

theorem every_north_catalogue_blocker_is_owned
    (bottom far : Int) (point : Point) (hpoint : forbidden bottom point) :
    returning bottom point ∨ northern bottom far point := by
  rcases hpoint with rfl | rfl | rfl | rfl | rfl | rfl <;>
    unfold returning northern endpoint <;> dsimp <;> omega

theorem north_terminal_contains_the_three_step_blocker
    (width incident far : Int) (hwidth : 6 ≤ width) (hlength : 4 ≤ incident) :
    endpoint width incident far (incident-3,1) := by
  unfold endpoint
  dsimp
  omega

theorem west_terminal_contains_the_four_step_blocker
    (width incident far : Int) (hwidth : 6 ≤ width) (hlength : 4 ≤ incident) :
    endpoint width incident far (incident-4,1) := by
  unfold endpoint
  dsimp
  omega

theorem north_outer_bar_contains_its_blocker
    (width near far : Int) (hwidth : 6 ≤ width) : endpoint width near far (0,4) := by
  unfold endpoint
  dsimp
  omega

theorem west_outer_bar_contains_its_blocker
    (width near far : Int) (hwidth : 6 ≤ width) : endpoint width near far (0,5) := by
  unfold endpoint
  dsimp
  omega

theorem north_support_must_be_consumed
    (bottom : Int) (occupied endpointAt : Point → Prop)
    (heast : occupied (bottom-5,12))
    (hretain : ¬endpointAt (bottom-5,11) →
      ∀ point, adjacent (bottom-5,11) point → occupied point → point = (bottom-4,11)) :
    endpointAt (bottom-5,11) := by
  by_cases hpoint : endpointAt (bottom-5,11)
  · exact hpoint
  · have hequal := hretain hpoint (bottom-5,12)
      (by unfold adjacent; dsimp; omega) heast
    have hcolumn := congrArg Prod.snd hequal
    dsimp at hcolumn
    omega

theorem width_six_north_has_no_complete_owner_family
    (Owner : Type) (returnOwner northOwner : Owner)
    (belongs : Owner → Point → Prop) (occupied : Point → Prop)
    (bottom far : Int) (hfar : 4 ≤ far)
    (hreturn : ∀ point, belongs returnOwner point ↔ returning bottom point)
    (hnorth : ∀ point, belongs northOwner point ↔ northern bottom far point)
    (hunique : ∀ first second point, belongs first point → belongs second point → first = second)
    (hoccupied : ∀ owner point, belongs owner point → occupied point)
    (hretain : (¬∃ owner, belongs owner (bottom-5,11)) →
      ∀ point, adjacent (bottom-5,11) point → occupied point → point = (bottom-4,11))
    (hcatalogue : ∀ consumer, belongs consumer (bottom-5,11) →
      ¬belongs consumer (bottom-4,11) → ¬belongs consumer (bottom-5,12) →
      ∃ point, belongs consumer point ∧ forbidden bottom point) : False := by
  have hneighbors := north_support_and_forcing_neighbors bottom far hfar
  have heast := hoccupied northOwner (bottom-5,12)
    ((hnorth (bottom-5,12)).mpr hneighbors.2.2)
  obtain ⟨consumer,hconsumer⟩ := north_support_must_be_consumed bottom occupied
    (fun point => ∃ owner, belongs owner point) heast hretain
  have habsent := north_forced_point_has_neither_prescribed_owner bottom far
  have hnotReturn : consumer ≠ returnOwner := by
    intro hequal
    exact habsent.1 ((hreturn (bottom-5,11)).mp (hequal ▸ hconsumer))
  have hnotNorth : consumer ≠ northOwner := by
    intro hequal
    exact habsent.2 ((hnorth (bottom-5,11)).mp (hequal ▸ hconsumer))
  have hnotSouth : ¬belongs consumer (bottom-4,11) := by
    intro hpoint
    exact hnotReturn (hunique consumer returnOwner (bottom-4,11) hpoint
      ((hreturn (bottom-4,11)).mpr hneighbors.2.1))
  have hnotEast : ¬belongs consumer (bottom-5,12) := by
    intro hpoint
    exact hnotNorth (hunique consumer northOwner (bottom-5,12) hpoint
      ((hnorth (bottom-5,12)).mpr hneighbors.2.2))
  obtain ⟨point,hpoint,hforbidden⟩ := hcatalogue consumer hconsumer hnotSouth hnotEast
  rcases every_north_catalogue_blocker_is_owned bottom far point hforbidden with
    hreturnPoint | hnorthPoint
  · exact hnotReturn (hunique consumer returnOwner point hpoint ((hreturn point).mpr hreturnPoint))
  · exact hnotNorth (hunique consumer northOwner point hpoint ((hnorth point).mpr hnorthPoint))

theorem upward_forced_point_and_neighbors
    (bottom width breadth incident far : Int) (hwidth : 6 ≤ width)
    (hbreadth : 6 ≤ breadth) (hlength : width ≤ incident) :
    support width 10 4 (5,width) ∧ secondary bottom width (bottom-7,width+5) ∧
      upward bottom breadth incident far (bottom-5,width+5) ∧
      ¬returning bottom (bottom-6,width+5) ∧
      ¬secondary bottom width (bottom-6,width+5) ∧
      ¬upward bottom breadth incident far (bottom-6,width+5) := by
  unfold support secondary upward returning endpoint
  dsimp
  omega

theorem all_horizontal_rotor_bottom_witnesses_are_upward_owned
    (bottom width breadth incident far offset : Int)
    (hwidth : 6 ≤ width) (hbreadth : 6 ≤ breadth) (hlength : width ≤ incident)
    (hlow : -3 ≤ offset) (hhigh : offset ≤ 2) :
    upward bottom breadth incident far (bottom-5,width+5+offset) := by
  unfold upward endpoint
  dsimp
  omega

theorem bar_window_excludes_zero_gap (width incident bar : Int)
    (hlow : width+7 ≤ bar) (hhigh : bar ≤ incident+5) : width+2 ≤ incident := by
  omega

theorem tight_gap_has_unique_odd_bar (width bar : Int)
    (heven : width % 2 = 0) (hlow : width+7 ≤ bar) (hhigh : bar ≤ width+7) :
    bar = width+7 ∧ bar % 2 = 1 := by
  omega

theorem forced_point_is_on_the_successor_near_leg
    (bottom width bar breadth near far : Int)
    (hlow : width+7 ≤ bar) (hnear : bar-width-5 ≤ near) :
    successor bottom bar breadth near far (bottom-6,width+5) := by
  unfold successor endpoint
  dsimp
  omega

theorem successor_terminal_and_its_consumed_lateral_support
    (bottom bar breadth near far incident otherWidth otherFar : Int)
    (hnear : 4 ≤ near) (heven : near % 2 = 0)
    (hleft : near ≤ bar-7) (hright : bar ≤ incident+5) :
    successor bottom bar breadth near far (bottom-6,bar-near) ∧
      support breadth near far (near,0) ∧
      upward bottom otherWidth incident otherFar (bottom-5,bar-near) := by
  unfold successor support upward endpoint
  dsimp
  omega

theorem tight_gap_long_bar_hits_the_original_far_leg
    (bottom width breadth far span near other : Int)
    (hbreadth : 6 ≤ breadth) (hfar : 4 ≤ far) (hlong : breadth ≤ span) :
    upward bottom breadth (width+2) far (bottom-4-breadth,width+7) ∧
      successor bottom (width+7) span near other (bottom-4-breadth,width+7) := by
  unfold upward successor endpoint
  dsimp
  omega

theorem tight_gap_even_width_bound (breadth span : Int)
    (hevenBreadth : breadth % 2 = 0) (hevenSpan : span % 2 = 0)
    (hshort : ¬breadth ≤ span) : span ≤ breadth-2 := by
  omega

theorem far_leg_reach_forces_a_general_width_collision
    (bottom breadth incident far bar span near other : Int)
    (hbreadth : 6 ≤ breadth) (hreach : incident+7-bar ≤ far)
    (hbar : bar ≤ incident+5) (hlong : breadth ≤ span) :
    upward bottom breadth incident far (bottom-4-breadth,bar) ∧
      successor bottom bar span near other (bottom-4-breadth,bar) := by
  unfold upward successor endpoint
  dsimp
  omega

theorem the_first_even_bar_excludes_successor_width_six
    (bottom width near far : Int) (hwidth : 6 ≤ width) (hfar : 4 ≤ far) :
    secondary bottom width (bottom-11,width+4) ∧
      successor bottom (width+8) 6 near far (bottom-11,width+4) := by
  unfold secondary successor endpoint
  dsimp
  omega

theorem tight_gap_excludes_successor_width_six
    (bottom width near far : Int) (hwidth : 6 ≤ width) (hfar : 4 ≤ far) :
    secondary bottom width (bottom-11,width+5) ∧
      successor bottom (width+7) 6 near far (bottom-11,width+5) := by
  unfold secondary successor endpoint
  dsimp
  omega

theorem odd_bar_charge (halfWidth legs matching inside tiles : Int)
    (hmatching : matching = 2*halfWidth-1+legs) (hinside : inside = legs+4)
    (htiles : tiles = halfWidth+legs+1) : matching+inside-2*tiles = 1 := by
  omega

theorem even_bar_charge (width legs matching inside tiles : Int)
    (hmatching : matching = width-1+legs) (hinside : inside = legs+2)
    (htiles : tiles = width+legs) : matching+inside-2*tiles = 1-width := by
  omega

theorem north_remaining_dimensions (width secondaryWidth : Int)
    (hwidth : 6 ≤ width) (heven : width % 2 = 0) (hexcluded : width ≠ 6)
    (hupper : width ≤ secondaryWidth-2) : 8 ≤ width ∧ 10 ≤ secondaryWidth := by
  omega

end SubQuorum.SecondaryTenSupportClosure
