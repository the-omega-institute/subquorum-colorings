import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenNarrowCapExclusion

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def residual (origin width breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 8 far (point.1-origin+6,width+12-point.2)

def cavity (origin width : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+4-point.1,point.2-width-7)

def cap (origin width breadth height : Int) (point : Point) : Prop :=
  endpoint breadth height (height-8) (point.1-origin-1+height,width+15-point.2)

def leftCap (origin width breadth height far : Int) (point : Point) : Prop :=
  endpoint breadth height far (point.1-origin-1+height,width+15-point.2)

def leftCapRegion (width oldBreadth breadth height far : Int) : Prop :=
  (breadth ≤ oldBreadth+2 ∧ 12 ≤ height ∧ far ≤ height-8) ∨
  (oldBreadth = width+8 ∧ breadth = width+12 ∧ 10 ≤ height ∧ far ≤ height+8) ∨
  (width+14 ≤ breadth ∧ 10 ≤ height)

def rightU (origin width breadth height far : Int) (point : Point) : Prop :=
  endpoint breadth height far (point.1-origin-2+height,point.2-width-11)

def leftU (origin width breadth height far : Int) (point : Point) : Prop :=
  endpoint breadth height far (point.1-origin-2+height,width+13-point.2)

def fixed (origin width : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,origin+11-point.1) ∨
  endpoint (width+4) 10 4 (point.1-origin+2,point.2-5) ∨
  endpoint width 4 6 (point.1-origin,point.2-6) ∨
  endpoint 8 6 4 (origin+6-point.1,point.2-width-6) ∨
  cavity origin width point ∨
  endpoint 6 4 4 (point.2-width-1,point.1-origin-1)

def firstReturn (origin width : Int) (point : Point) : Prop :=
  endpoint (width+6) 6 4 (point.1-origin+4,width+11-point.2)

def northRotor (handed : Bool) (origin width : Int) (point : Point) : Prop :=
  (point.1-origin-2,point.2-width-12) ∈
    if handed then
      [(-3,1),(-2,-1),(-2,0),(-2,1),(-1,0),(-1,1),(-1,2),(0,0)]
    else
      [(-3,-1),(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(0,0)]

theorem gap_absent (origin width breadth far capBreadth height : Int)
    (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) (hheight : 12 ≤ height) :
    ¬(fixed origin width (origin+2,width+12) ∨
      firstReturn origin width (origin+2,width+12) ∨
      residual origin width breadth far (origin+2,width+12) ∨
      cap origin width capBreadth height (origin+2,width+12)) := by
  unfold fixed firstReturn residual cap cavity endpoint
  dsimp
  omega

theorem gap_three_neighbors (origin width breadth far : Int) :
    residual origin width breadth far (origin+2,width+11) ∧
      cavity origin width (origin+2,width+13) ∧
      cavity origin width (origin+3,width+12) := by
  unfold residual cavity endpoint
  dsimp
  omega

theorem right_bar_hits_cap (origin width capBreadth height breadth depth far : Int)
    (hcap : 6 ≤ capBreadth)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) (hbelow : depth < height) :
    rightU origin width breadth depth far (origin+3-depth,width+14) ∧
      cap origin width capBreadth height (origin+3-depth,width+14) := by
  unfold rightU cap endpoint
  dsimp
  omega

theorem long_near_leg_hits_cap (origin width capBreadth height breadth depth far : Int)
    (hcap : 6 ≤ capBreadth) (hheight : 12 ≤ height)
    (hbreadth : 6 ≤ breadth) (hdepth : height ≤ depth) :
    rightU origin width breadth depth far (origin+2-height,width+12) ∧
      leftU origin width breadth depth far (origin+2-height,width+12) ∧
      cap origin width capBreadth height (origin+2-height,width+12) := by
  unfold rightU leftU cap endpoint
  dsimp
  omega

theorem short_left_bar_hits_residual (origin width oldBreadth oldFar breadth depth far : Int)
    (holdBreadth : 6 ≤ oldBreadth) (hbreadth : 6 ≤ breadth)
    (hdepthMin : 4 ≤ depth) (hdepthMax : depth ≤ 8) :
    leftU origin width breadth depth far (origin+3-depth,width+11) ∧
      residual origin width oldBreadth oldFar (origin+3-depth,width+11) := by
  unfold leftU residual endpoint
  dsimp
  omega

theorem intermediate_left_bar_hits_cap
    (origin width capBreadth height breadth depth far : Int)
    (hcapMin : 6 ≤ capBreadth) (hcapMax : capBreadth ≤ 8)
    (hbreadth : 6 ≤ breadth) (hdepthMin : 10 ≤ depth) (hbelow : depth < height) :
    leftU origin width breadth depth far (origin+3-depth,width+15-capBreadth) ∧
      cap origin width capBreadth height (origin+3-depth,width+15-capBreadth) := by
  unfold leftU cap endpoint
  dsimp
  omega

theorem every_right_consumer_collides
    (origin width capBreadth height breadth depth far : Int)
    (hcap : 6 ≤ capBreadth) (hheight : 12 ≤ height)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) :
    ∃ point : Point, rightU origin width breadth depth far point ∧
      cap origin width capBreadth height point := by
  by_cases hbelow : depth < height
  · exact ⟨_,right_bar_hits_cap origin width capBreadth height breadth depth far
      hcap hbreadth hdepth hbelow⟩
  · have hlong : height ≤ depth := by omega
    have hhit := long_near_leg_hits_cap origin width capBreadth height breadth depth far
      hcap hheight hbreadth hlong
    exact ⟨_,hhit.1,hhit.2.2⟩

theorem every_left_consumer_collides
    (origin width oldBreadth oldFar capBreadth height breadth depth far : Int)
    (holdBreadth : 6 ≤ oldBreadth) (hcapMin : 6 ≤ capBreadth) (hcapMax : capBreadth ≤ 8)
    (hheight : 12 ≤ height) (hbreadth : 6 ≤ breadth)
    (hdepth : 4 ≤ depth) (heven : depth % 2 = 0) :
    ∃ point : Point, leftU origin width breadth depth far point ∧
      (residual origin width oldBreadth oldFar point ∨
        cap origin width capBreadth height point) := by
  by_cases hshort : depth ≤ 8
  · have hhit := short_left_bar_hits_residual origin width oldBreadth oldFar breadth depth far
      holdBreadth hbreadth hdepth hshort
    exact ⟨_,hhit.1,Or.inl hhit.2⟩
  · by_cases hbelow : depth < height
    · have hten : 10 ≤ depth := by omega
      have hhit := intermediate_left_bar_hits_cap origin width capBreadth height breadth depth far
        hcapMin hcapMax hbreadth hten hbelow
      exact ⟨_,hhit.1,Or.inr hhit.2⟩
    · have hlong : height ≤ depth := by omega
      have hhit := long_near_leg_hits_cap origin width capBreadth height breadth depth far
        hcapMin hheight hbreadth hlong
      exact ⟨_,hhit.2.1,Or.inr hhit.2.2⟩

theorem north_rotor_hits_cavity (handed : Bool) (origin width : Int) :
    northRotor handed origin width (origin,width+13) ∧
      cavity origin width (origin,width+13) := by
  constructor
  · cases handed <;> simp only [northRotor, Bool.false_eq_true, ite_false, ite_true,
      List.mem_cons, Prod.mk.injEq] <;> omega
  · unfold cavity endpoint
    dsimp
    omega

theorem left_bar_spanning_cap_far_column
    (origin width capBreadth height breadth depth far : Int)
    (hcap : 6 ≤ capBreadth) (hspan : capBreadth-2 ≤ breadth)
    (hdepth : 10 ≤ depth) (hbelow : depth < height) :
    leftU origin width breadth depth far (origin+3-depth,width+15-capBreadth) ∧
      cap origin width capBreadth height (origin+3-depth,width+15-capBreadth) := by
  unfold leftU cap endpoint
  dsimp
  omega

theorem left_far_leg_reaching_residual
    (origin width oldBreadth oldFar breadth depth far : Int)
    (hbreadth : 6 ≤ breadth) (hinside : breadth-1 ≤ oldBreadth)
    (hdepth : 10 ≤ depth) (hfar : depth-8 ≤ far) :
    leftU origin width breadth depth far (origin-6,width+13-breadth) ∧
      residual origin width oldBreadth oldFar (origin-6,width+13-breadth) := by
  unfold leftU residual endpoint
  dsimp
  omega

theorem tight_left_avoids_all_retained_endpoints
    (origin width oldBreadth oldFar capBreadth height breadth depth far : Int)
    (point : Point) (hwidth : 12 ≤ width)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hcapMin : 6 ≤ capBreadth) (hcapMax : capBreadth ≤ width+10)
    (hbreadthMin : 6 ≤ breadth) (hbreadthMax : breadth ≤ capBreadth-4)
    (hdepthMin : 14 ≤ depth) (hdepthMax : depth ≤ height-2)
    (hfarMax : far ≤ depth-10) :
    ¬(leftU origin width breadth depth far point ∧
      (fixed origin width point ∨ firstReturn origin width point ∨
        residual origin width oldBreadth oldFar point ∨
        cap origin width capBreadth height point)) := by
  unfold leftU fixed firstReturn residual cap cavity endpoint
  dsimp
  omega

theorem tight_left_disjointness_necessary
    (origin width oldBreadth oldFar capBreadth height breadth depth far : Int)
    (hwidth : 12 ≤ width) (hold : width+8 ≤ oldBreadth)
    (hcapMin : 6 ≤ capBreadth) (hcapMax : capBreadth ≤ width+10)
    (hheight : 12 ≤ height) (hbreadth : 6 ≤ breadth)
    (hdepth : 4 ≤ depth) (hfar : 4 ≤ far)
    (hcapEven : capBreadth % 2 = 0) (hheightEven : height % 2 = 0)
    (hbreadthEven : breadth % 2 = 0) (hdepthEven : depth % 2 = 0)
    (hfarEven : far % 2 = 0)
    (hdisjoint : ∀ point : Point,
      ¬(leftU origin width breadth depth far point ∧
        (residual origin width oldBreadth oldFar point ∨
          cap origin width capBreadth height point))) :
    breadth ≤ capBreadth-4 ∧ 14 ≤ depth ∧ depth ≤ height-2 ∧ far ≤ depth-10 := by
  have hbelow : depth < height := by
    apply Classical.byContradiction
    intro hnot
    have hlong : height ≤ depth := by omega
    have hhit := long_near_leg_hits_cap origin width capBreadth height breadth depth far
      hcapMin hheight hbreadth hlong
    exact hdisjoint _ ⟨hhit.2.1,Or.inr hhit.2.2⟩
  have hten : 10 ≤ depth := by
    apply Classical.byContradiction
    intro hnot
    have hshort : depth ≤ 8 := by omega
    have holdMin : 6 ≤ oldBreadth := by omega
    have hhit := short_left_bar_hits_residual origin width oldBreadth oldFar breadth depth far
      holdMin hbreadth hdepth hshort
    exact hdisjoint _ ⟨hhit.1,Or.inl hhit.2⟩
  have hspan : breadth ≤ capBreadth-4 := by
    apply Classical.byContradiction
    intro hnot
    have hwide : capBreadth-2 ≤ breadth := by omega
    have hhit := left_bar_spanning_cap_far_column origin width capBreadth height breadth depth far
      hcapMin hwide hten hbelow
    exact hdisjoint _ ⟨hhit.1,Or.inr hhit.2⟩
  have hshortFar : far ≤ depth-10 := by
    apply Classical.byContradiction
    intro hnot
    have hreach : depth-8 ≤ far := by omega
    have hinside : breadth-1 ≤ oldBreadth := by omega
    have hhit := left_far_leg_reaching_residual origin width oldBreadth oldFar breadth depth far
      hbreadth hinside hten hreach
    exact hdisjoint _ ⟨hhit.1,Or.inl hhit.2⟩
  omega

theorem all_left_cap_avoids_retained_endpoints
    (origin width oldBreadth oldFar breadth height far : Int) (point : Point)
    (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hregion : leftCapRegion width oldBreadth breadth height far) :
    ¬(leftCap origin width breadth height far point ∧
      (fixed origin width point ∨ firstReturn origin width point ∨
        residual origin width oldBreadth oldFar point)) := by
  unfold leftCapRegion at hregion
  unfold leftCap fixed firstReturn residual cavity endpoint
  dsimp
  omega

theorem all_left_cap_disjointness_necessary
    (origin width oldBreadth oldFar breadth height far : Int)
    (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth)
    (hheight : 4 ≤ height) (hfar : 4 ≤ far)
    (hwidthEven : width % 2 = 0) (hbreadthEven : breadth % 2 = 0)
    (hheightEven : height % 2 = 0)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hdisjoint : ∀ point : Point,
      ¬(leftCap origin width breadth height far point ∧
        (fixed origin width point ∨ residual origin width oldBreadth oldFar point))) :
    leftCapRegion width oldBreadth breadth height far := by
  have hten : 10 ≤ height := by
    apply Classical.byContradiction
    intro hnot
    have hhit : leftCap origin width breadth height far (origin+2-height,width+11) ∧
        residual origin width oldBreadth oldFar (origin+2-height,width+11) := by
      unfold leftCap residual endpoint
      dsimp
      omega
    exact hdisjoint _ ⟨hhit.1,Or.inr hhit.2⟩
  by_cases hband : breadth ≤ oldBreadth+2
  · have hbound : far ≤ height-8 := by
      apply Classical.byContradiction
      intro hnot
      have hhit : leftCap origin width breadth height far (origin-6,width+15-breadth) ∧
          residual origin width oldBreadth oldFar (origin-6,width+15-breadth) := by
        unfold leftCap residual endpoint
        dsimp
        omega
      exact hdisjoint _ ⟨hhit.1,Or.inr hhit.2⟩
    exact Or.inl ⟨hband,by omega,hbound⟩
  · by_cases htip : oldBreadth = width+8 ∧ breadth = width+12
    · have hbound : far ≤ height+8 := by
        apply Classical.byContradiction
        intro hnot
        have hhit : leftCap origin width breadth height far (origin+10,3) ∧
            fixed origin width (origin+10,3) := by
          constructor
          · unfold leftCap endpoint
            dsimp
            omega
          · unfold fixed
            apply Or.inl
            unfold endpoint
            dsimp
            omega
        exact hdisjoint _ ⟨hhit.1,Or.inl hhit.2⟩
      exact Or.inr (Or.inl ⟨htip.1,htip.2,hten,hbound⟩)
    · exact Or.inr (Or.inr ⟨by omega,hten⟩)

theorem all_left_cap_blocks_right_consumer
    (origin width capBreadth height capFar breadth depth far : Int)
    (hcap : 6 ≤ capBreadth) (hheight : 10 ≤ height)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) :
    ∃ point : Point, rightU origin width breadth depth far point ∧
      leftCap origin width capBreadth height capFar point := by
  by_cases hbelow : depth < height
  · refine ⟨(origin+3-depth,width+14),?_⟩
    unfold rightU leftCap endpoint
    dsimp
    omega
  · refine ⟨(origin+2-height,width+12),?_⟩
    unfold rightU leftCap endpoint
    dsimp
    omega

theorem all_zero_cap_left_consumer_sufficient
    (origin width oldBreadth oldFar capBreadth height capFar breadth depth far : Int)
    (point : Point) (hwidth : 12 ≤ width)
    (hold : oldBreadth = width+8 ∨ oldBreadth = width+10)
    (hcapMin : 6 ≤ capBreadth)
    (hbreadthMin : 6 ≤ breadth) (hbreadthMax : breadth ≤ capBreadth-4)
    (hdepthMin : 14 ≤ depth) (hdepthMax : depth ≤ height-2)
    (hfarMax : far ≤ depth-10) :
    ¬(leftU origin width breadth depth far point ∧
      (fixed origin width point ∨ firstReturn origin width point ∨
        residual origin width oldBreadth oldFar point ∨
        leftCap origin width capBreadth height capFar point)) := by
  unfold leftU fixed firstReturn residual leftCap cavity endpoint
  dsimp
  omega

theorem all_zero_cap_left_consumer_necessary
    (origin width oldBreadth oldFar capBreadth height capFar breadth depth far : Int)
    (hwidth : 12 ≤ width) (hold : width+8 ≤ oldBreadth)
    (hcapMin : 6 ≤ capBreadth) (hcapMax : capBreadth ≤ width+12)
    (hheight : 10 ≤ height) (hcapFar : height-8 ≤ capFar)
    (hbreadth : 6 ≤ breadth) (hdepth : 4 ≤ depth) (hfar : 4 ≤ far)
    (hcapEven : capBreadth % 2 = 0) (hheightEven : height % 2 = 0)
    (hbreadthEven : breadth % 2 = 0) (hdepthEven : depth % 2 = 0)
    (hfarEven : far % 2 = 0)
    (hdisjoint : ∀ point : Point,
      ¬(leftU origin width breadth depth far point ∧
        (residual origin width oldBreadth oldFar point ∨
          leftCap origin width capBreadth height capFar point))) :
    breadth ≤ capBreadth-4 ∧ 14 ≤ depth ∧ depth ≤ height-2 ∧ far ≤ depth-10 := by
  have hbelow : depth < height := by
    apply Classical.byContradiction
    intro hnot
    have hhit : leftU origin width breadth depth far (origin+2-height,width+12) ∧
        leftCap origin width capBreadth height capFar (origin+2-height,width+12) := by
      unfold leftU leftCap endpoint
      dsimp
      omega
    exact hdisjoint _ ⟨hhit.1,Or.inr hhit.2⟩
  have hten : 10 ≤ depth := by
    apply Classical.byContradiction
    intro hnot
    have hshort : depth ≤ 8 := by omega
    have holdMin : 6 ≤ oldBreadth := by omega
    have hhit := short_left_bar_hits_residual origin width oldBreadth oldFar breadth depth far
      holdMin hbreadth hdepth hshort
    exact hdisjoint _ ⟨hhit.1,Or.inl hhit.2⟩
  have hspan : breadth ≤ capBreadth-4 := by
    apply Classical.byContradiction
    intro hnot
    have hhit : leftU origin width breadth depth far (origin+3-depth,width+15-capBreadth) ∧
        leftCap origin width capBreadth height capFar (origin+3-depth,width+15-capBreadth) := by
      unfold leftU leftCap endpoint
      dsimp
      omega
    exact hdisjoint _ ⟨hhit.1,Or.inr hhit.2⟩
  have hshortFar : far ≤ depth-10 := by
    apply Classical.byContradiction
    intro hnot
    have hreach : depth-8 ≤ far := by omega
    have hinside : breadth-1 ≤ oldBreadth := by omega
    have hhit := left_far_leg_reaching_residual origin width oldBreadth oldFar breadth depth far
      hbreadth hinside hten hreach
    exact hdisjoint _ ⟨hhit.1,Or.inl hhit.2⟩
  omega

end SubQuorum.SecondaryTenNarrowCapExclusion
