import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenNorthGapFourPackage

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

def secondary (bottom width far : Int) (point : Point) : Prop :=
  endpoint (width+4) 10 far (point.1-(bottom-11),point.2-5)

def northern (bottom width far : Int) (point : Point) : Prop :=
  endpoint width 4 far (point.1-(bottom-9),point.2-6)

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def outward (bottom width breadth near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (bottom-9+near-point.1,point.2-(width+6))

def inward (bottom width breadth near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (bottom-9+near-point.1,width+8-point.2)

def secondRight (bottom width breadth near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (bottom-9+near-point.1,point.2-(width+7))

def secondLeft (bottom width breadth near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (bottom-9+near-point.1,width+9-point.2)

theorem first_site_absent (bottom width far other : Int) (hwidth : 8 ≤ width) :
    ¬returning bottom (bottom-9,width+7) ∧
      ¬secondary bottom width far (bottom-9,width+7) ∧
      ¬northern bottom width other (bottom-9,width+7) := by
  unfold returning secondary northern endpoint
  dsimp
  omega

theorem first_support_and_blockers (bottom width far other : Int)
    (hwidth : 8 ≤ width) (hfar : 4 ≤ far) :
    support width 4 other (0,width+1) ∧
      northern bottom width other (bottom-9,width+6) ∧
      secondary bottom width far (bottom-10,width+7) ∧
      secondary bottom width far (bottom-9,width+9) := by
  unfold support northern secondary endpoint
  dsimp
  omega

theorem first_rotor_blockers (bottom width far other : Int)
    (hwidth : 8 ≤ width) (hother : 4 ≤ other) :
    northern bottom width other (bottom-7,width+6) ∧
      northern bottom width other (bottom-8,width+6) ∧
      secondary bottom width far (bottom-11,width+8) ∧
      secondary bottom width far (bottom-10,width+9) := by
  unfold northern secondary endpoint
  dsimp
  omega

theorem outward_terminal_supports (bottom width breadth near far : Int)
    (hnear : 4 ≤ near) (heven : near % 2 = 0) :
    outward bottom width breadth near far (bottom-9,width+7) ∧
      support breadth near far (near+1,1) ∧
      support breadth near far (near,0) ∧
      (bottom-9+near-(near+1),width+6+1) = (bottom-10,width+7) ∧
      (bottom-9+near-near,width+6+0) = (bottom-9,width+6) := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · unfold outward endpoint
    dsimp
    omega
  · unfold support
    dsimp
    omega
  · unfold support
    dsimp
    omega
  · apply Prod.ext <;> dsimp <;> omega
  · apply Prod.ext <;> dsimp <;> omega

theorem inward_terminal_and_next_support (bottom width breadth near far : Int)
    (hnear : 4 ≤ near) (heven : near % 2 = 0) :
    inward bottom width breadth near far (bottom-9,width+7) ∧
      support breadth near far (near,0) ∧
      (bottom-9+near-near,width+8-0) = (bottom-9,width+8) := by
  refine ⟨?_, ?_, ?_⟩
  · unfold inward endpoint
    dsimp
    omega
  · unfold support
    dsimp
    omega
  · apply Prod.ext <;> dsimp <;> omega

theorem outward_short_collision (bottom width breadth near far : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (hshort : near ≤ far-2) :
    secondary bottom width far (bottom-10+near,width+9) ∧
      outward bottom width breadth near far (bottom-10+near,width+9) := by
  unfold secondary outward endpoint
  dsimp
  omega

theorem inward_short_collision (bottom width breadth near far other : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (hshort : near ≤ other) :
    northern bottom width other (bottom-10+near,width+6) ∧
      inward bottom width breadth near far (bottom-10+near,width+6) := by
  unfold northern inward endpoint
  dsimp
  omega

theorem even_outward_bound (near far : Int) (hnear : near % 2 = 0)
    (hfar : far % 2 = 0) (hcollision : ¬near ≤ far-2) : far ≤ near := by
  omega

theorem even_inward_bound (near other : Int) (hnear : near % 2 = 0)
    (hother : other % 2 = 0) (hcollision : ¬near ≤ other) : other+2 ≤ near := by
  omega

theorem second_site_absent (bottom width breadth near far other : Int)
    (hwidth : 8 ≤ width) (hbreadth : 6 ≤ breadth) :
    ¬returning bottom (bottom-9,width+8) ∧
      ¬secondary bottom width far (bottom-9,width+8) ∧
      ¬northern bottom width other (bottom-9,width+8) ∧
      ¬inward bottom width breadth near far (bottom-9,width+8) := by
  unfold returning secondary northern inward endpoint
  dsimp
  omega

theorem second_blockers (bottom width breadth near far other : Int)
    (hwidth : 8 ≤ width) (hnear : 6 ≤ near) (hfar : 4 ≤ far) :
    secondary bottom width far (bottom-10,width+8) ∧
      secondary bottom width far (bottom-9,width+9) ∧
      inward bottom width breadth near other (bottom-9,width+7) ∧
      inward bottom width breadth near other (bottom-8,width+7) ∧
      inward bottom width breadth near other (bottom-7,width+7) := by
  unfold secondary inward endpoint
  dsimp
  omega

theorem second_right_short_collision (bottom width breadth near far : Int)
    (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) (hshort : near ≤ far-2) :
    secondary bottom width far (bottom-10+near,width+9) ∧
      secondRight bottom width breadth near far (bottom-10+near,width+9) := by
  unfold secondary secondRight endpoint
  dsimp
  omega

theorem second_left_short_collision (bottom width breadth near far nextBreadth nextNear nextFar : Int)
    (hbreadth : 6 ≤ breadth) (hnextBreadth : 6 ≤ nextBreadth) (hnextNear : 4 ≤ nextNear)
    (hshort : nextNear ≤ near) :
    inward bottom width breadth near far (bottom-10+nextNear,width+7) ∧
      secondLeft bottom width nextBreadth nextNear nextFar (bottom-10+nextNear,width+7) := by
  unfold inward secondLeft endpoint
  dsimp
  omega

theorem different_bar_tile_rows (base near far : Int) (hnear : far ≤ near)
    (hbase : base % 2 = 1) (hnearEven : near % 2 = 0) (hfarEven : far % 2 = 0)
    : (base+far-2)/2 < (base+near-1)/2 := by
  omega

theorem outward_increment (overlap deltaMass deltaFull deltaEvents : Int)
    (hmass : deltaMass = 0) (hfull : deltaFull = 1+overlap)
    (hevents : deltaEvents = 1+2*overlap) :
    deltaMass+2*deltaFull-deltaEvents = 1 := by
  omega

theorem neutral_package (halfWidth overlap deltaN deltaMass deltaFull deltaEvents : Int)
    (hN : deltaN = 1) (hmass : deltaMass = 2*halfWidth-1)
    (hfull : deltaFull = halfWidth+3+overlap)
    (hevents : deltaEvents = 4*halfWidth+6+2*overlap) :
    deltaN+deltaMass+2*deltaFull-deltaEvents = 0 := by
  omega

theorem external_partition (delta internal extraFull externalEvents : Int)
    (hpartition : delta = internal+2*extraFull-externalEvents)
    (hinternal : internal = 0) : delta = 2*extraFull-externalEvents := by
  omega

theorem negative_external_witness : (2 : Int)*2-7 = -3 := by
  omega

theorem cavity_site_absent (bottom width breadth near far other : Int)
    (hwidth : 8 ≤ width) (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) :
    ¬returning bottom (bottom-8,width+8) ∧
      ¬secondary bottom width far (bottom-8,width+8) ∧
      ¬northern bottom width other (bottom-8,width+8) ∧
      ¬outward bottom width breadth near far (bottom-8,width+8) := by
  unfold returning secondary northern outward endpoint
  dsimp
  omega

theorem cavity_original_supports (width breadth near far other : Int)
    (hfar : 4 ≤ far) (hnear : 4 ≤ near) (heven : near % 2 = 0) :
    support (width+4) 10 far (3,width+3) ∧
      support breadth near other (near-1,2) := by
  unfold support
  dsimp
  omega

theorem cavity_blockers (bottom width breadth near far other : Int)
    (hwidth : 8 ≤ width) (hbreadth : 6 ≤ breadth) (hnear : 4 ≤ near) :
    secondary bottom width far (bottom-10,width+7) ∧
      secondary bottom width far (bottom-10,width+9) ∧
      outward bottom width breadth near other (bottom-6,width+7) ∧
      outward bottom width breadth near other (bottom-7,width+7) := by
  unfold secondary outward endpoint
  dsimp
  omega

theorem cavity_window_strict (base bar near far : Int)
    (hlower : base+far ≤ bar) (hupper : bar ≤ base+near-2) : far+2 ≤ near := by
  omega

theorem cavity_tight_parameters (base bar near far nextNear : Int)
    (hbase : base % 2 = 1) (hfar : far % 2 = 0)
    (hnextEven : nextNear % 2 = 0) (htight : near = far+2)
    (hlower : base+far ≤ bar) (hupper : bar ≤ base+near-2)
    (hstemLower : bar-base-1 ≤ nextNear) (hstemUpper : nextNear ≤ bar-base) :
    bar = base+far ∧ nextNear = far ∧ bar % 2 = 1 := by
  omega

theorem cavity_terminal_phases (base bar near : Int)
    (hbase : base % 2 = 1) (heven : near % 2 = 0)
    (hlower : bar-base-1 ≤ near) (hupper : near ≤ bar-base) :
    (bar % 2 = 1 → bar-near = base) ∧
      (bar % 2 = 0 → bar-near = base+1) := by
  omega

theorem cavity_tight_width_collision (bottom width breadth far other nextBreadth nextFar : Int)
    (hbreadth : 6 ≤ breadth) (hother : 4 ≤ other) (hlarge : breadth ≤ nextBreadth) :
    outward bottom width breadth (far+2) other (bottom-9+far,width+6+breadth) ∧
      secondRight bottom width nextBreadth far nextFar (bottom-9+far,width+6+breadth) := by
  unfold outward secondRight endpoint
  dsimp
  omega

theorem cavity_tight_width_bound (breadth nextBreadth : Int)
    (hnext : 6 ≤ nextBreadth) (heven : breadth % 2 = 0)
    (hnextEven : nextBreadth % 2 = 0) (hcollision : ¬breadth ≤ nextBreadth) :
    nextBreadth ≤ breadth-2 ∧ 8 ≤ breadth := by
  omega

end SubQuorum.SecondaryTenNorthGapFourPackage
