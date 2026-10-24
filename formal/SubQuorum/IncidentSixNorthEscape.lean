import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.IncidentSixNorthEscape

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

def cornerEndpoint (bottom near far : Int) (point : Point) : Prop :=
  endpoint (bottom-2) near far (point.2-3,point.1-2)

def returnEndpoint (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def escapeEndpoint (bottom width other : Int) (point : Point) : Prop :=
  endpoint width 6 other (point.1-(bottom-7),point.2-4)

def fixedEndpoint (bottom near far width other : Int) (point : Point) : Prop :=
  cornerEndpoint bottom near far point ∨ returnEndpoint bottom point ∨
    escapeEndpoint bottom width other point

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def axialU (outer width incident other : Int) (above right : Bool) (point : Point) : Prop :=
  endpoint width incident other
    ((if above then point.1-outer else outer-point.1),
     (if right then point.2-5 else 7-point.2))

def axialRotor (bottom : Int) (north left : Bool) (point : Point) : Prop :=
  let row := if north then point.1-(bottom-4) else (bottom-4)-point.1
  let column := if left then point.2-6 else 6-point.2
  (row = -3 ∧ column = -1) ∨
  (row = -2 ∧ -1 ≤ column ∧ column ≤ 1) ∨
  (row = -1 ∧ -2 ≤ column ∧ column ≤ 0) ∨
  (row = 0 ∧ column = 0)

theorem both_original_supports_and_distinct_anchors (bottom width other : Int)
    (hwidth : 6 ≤ width) :
    support width 6 other (3,2) ∧ support 6 8 4 (5,6) ∧
      escapeEndpoint bottom width other (bottom-4,5) ∧
      returnEndpoint bottom (bottom-4,7) := by
  unfold support escapeEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem none_of_the_three_owners_owns_the_forced_point
    (bottom near far width other : Int) (hbottom : 8 ≤ bottom)
    (hwidth : 6 ≤ width) (_hfar : far = 4 ∨ far = 6) :
    ¬fixedEndpoint bottom near far width other (bottom-4,6) := by
  unfold fixedEndpoint cornerEndpoint returnEndpoint escapeEndpoint endpoint
  dsimp
  omega

theorem the_shared_support_is_forced
    (bottom : Int) (occupiedEndpoint : Point → Prop)
    (heast : occupiedEndpoint (bottom-4,7))
    (hretained : ¬occupiedEndpoint (bottom-4,6) →
      ∀ next, adjacent (bottom-4,6) next → occupiedEndpoint next →
        next = (bottom-4,5)) : occupiedEndpoint (bottom-4,6) := by
  by_cases hpoint : occupiedEndpoint (bottom-4,6)
  · exact hpoint
  · have hequal := hretained hpoint (bottom-4,7) (by simp [adjacent]) heast
    have hcolumn := congrArg Prod.snd hequal
    dsimp at hcolumn
    omega

theorem a_bar_above_hits_the_escape_lower_bar
    (bottom width incident other outer : Int) (right : Bool)
    (hwidth : 6 ≤ width) (habove : outer ≤ bottom-6)
    (hincident : bottom-4-outer ≤ incident) :
    axialU outer width incident other true right (bottom-6,6) := by
  cases right <;> unfold axialU endpoint <;> dsimp <;> omega

theorem the_upper_blocker_is_escape_owned (bottom width other : Int)
    (hwidth : 6 ≤ width) : escapeEndpoint bottom width other (bottom-6,6) := by
  unfold escapeEndpoint endpoint
  dsimp
  omega

theorem a_distant_bar_below_hits_the_corner
    (bottom width incident other outer : Int) (right : Bool)
    (hwidth : 6 ≤ width) (houter : bottom ≤ outer)
    (hincident : outer-(bottom-4) ≤ incident) :
    axialU outer width incident other false right (bottom,6) := by
  cases right <;> unfold axialU endpoint <;> dsimp <;> omega

theorem the_lower_blocker_is_corner_owned (bottom near far : Int)
    (_hbottom : 8 ≤ bottom) (hfar : 4 ≤ far) :
    cornerEndpoint bottom near far (bottom,6) := by
  unfold cornerEndpoint endpoint
  dsimp
  omega

theorem a_close_left_bar_hits_the_escape_leg
    (bottom width incident other outer : Int)
    (hwidth : 6 ≤ width) (hlower : bottom-2 ≤ outer) (hupper : outer < bottom) :
    axialU outer width incident other false false (outer,5) ∧
      ∀ escapeWidth escapeOther, escapeEndpoint bottom escapeWidth escapeOther (outer,5) := by
  constructor
  · unfold axialU endpoint
    dsimp
    omega
  · intro escapeWidth escapeOther
    unfold escapeEndpoint endpoint
    dsimp
    omega

theorem a_close_right_bar_hits_the_return_bar
    (bottom width incident other outer : Int)
    (hwidth : 6 ≤ width) (hlower : bottom-2 ≤ outer) (hupper : outer < bottom) :
    axialU outer width incident other false true (outer,10) ∧
      returnEndpoint bottom (outer,10) := by
  unfold axialU returnEndpoint endpoint
  dsimp
  omega

theorem every_axial_U_consumer_collides
    (bottom near far escapeWidth escapeOther width incident other outer : Int)
    (above right : Bool) (hbottom : 8 ≤ bottom) (hfar : 4 ≤ far)
    (hwidth : 6 ≤ width) (hescape : 6 ≤ escapeWidth)
    (hleg : 2 ≤ (if above then bottom-4-outer else outer-(bottom-4)))
    (hincident : (if above then bottom-4-outer else outer-(bottom-4)) ≤ incident) :
    ∃ point, axialU outer width incident other above right point ∧
      fixedEndpoint bottom near far escapeWidth escapeOther point := by
  cases above with
  | true =>
    refine ⟨(bottom-6,6), ?_, Or.inr (Or.inr ?_)⟩
    · exact a_bar_above_hits_the_escape_lower_bar bottom width incident other outer right
        hwidth (by dsimp at hleg; omega) hincident
    · exact the_upper_blocker_is_escape_owned bottom escapeWidth escapeOther hescape
  | false =>
    by_cases hdistant : bottom ≤ outer
    · exact ⟨(bottom,6),
        a_distant_bar_below_hits_the_corner bottom width incident other outer right
          hwidth hdistant hincident,
        Or.inl (the_lower_blocker_is_corner_owned bottom near far hbottom hfar)⟩
    · have hclose : bottom-2 ≤ outer := by dsimp at hleg; omega
      cases right with
      | false =>
        have hhit := a_close_left_bar_hits_the_escape_leg bottom width incident other outer
          hwidth hclose (by omega)
        exact ⟨(outer,5), hhit.1, Or.inr (Or.inr (hhit.2 escapeWidth escapeOther))⟩
      | true =>
        have hhit := a_close_right_bar_hits_the_return_bar bottom width incident other outer
          hwidth hclose (by omega)
        exact ⟨(outer,10), hhit.1, Or.inr (Or.inl hhit.2)⟩

theorem all_four_axial_rotors_collide
    (bottom near far width other : Int) (north left : Bool) (hwidth : 6 ≤ width) :
    ∃ point, axialRotor bottom north left point ∧
      fixedEndpoint bottom near far width other point := by
  cases north with
  | true =>
    refine ⟨(bottom-6,5), ?_, Or.inr (Or.inr ?_)⟩
    · cases left <;> unfold axialRotor <;> dsimp <;> omega
    · unfold escapeEndpoint endpoint
      dsimp
      omega
  | false =>
    refine ⟨(bottom-2,5), ?_, Or.inr (Or.inr ?_)⟩
    · cases left <;> unfold axialRotor <;> dsimp <;> omega
    · unfold escapeEndpoint endpoint
      dsimp
      omega

def freshAxialConsumer (bottom near far width other : Int) : Prop :=
  (∃ consumerWidth incident consumerOther outer above right,
    6 ≤ consumerWidth ∧
    2 ≤ (if above then bottom-4-outer else outer-(bottom-4)) ∧
    (if above then bottom-4-outer else outer-(bottom-4)) ≤ incident ∧
    ∀ point, axialU outer consumerWidth incident consumerOther above right point →
      ¬fixedEndpoint bottom near far width other point) ∨
  (∃ north left, ∀ point, axialRotor bottom north left point →
    ¬fixedEndpoint bottom near far width other point)

theorem no_fresh_axial_consumer (bottom near far width other : Int)
    (hbottom : 8 ≤ bottom) (hfar : 4 ≤ far) (hwidth : 6 ≤ width) :
    ¬freshAxialConsumer bottom near far width other := by
  intro hconsumer
  rcases hconsumer with hU | hrotor
  · obtain ⟨consumerWidth, incident, consumerOther, outer, above, right,
      hconsumerWidth, hleg, hincident, havoid⟩ := hU
    obtain ⟨point, hown, hfixed⟩ := every_axial_U_consumer_collides
      bottom near far width other consumerWidth incident consumerOther outer above right
      hbottom hfar hconsumerWidth hwidth hleg hincident
    exact havoid point hown hfixed
  · obtain ⟨north, left, havoid⟩ := hrotor
    obtain ⟨point, hown, hfixed⟩ := all_four_axial_rotors_collide
      bottom near far width other north left hwidth
    exact havoid point hown hfixed

theorem no_extension_under_the_original_owner_catalogue
    (bottom near far width other : Int) (occupiedEndpoint : Point → Prop)
    (hbottom : 8 ≤ bottom) (hfar : 4 ≤ far) (hwidth : 6 ≤ width)
    (heast : occupiedEndpoint (bottom-4,7))
    (hretained : ¬occupiedEndpoint (bottom-4,6) →
      ∀ next, adjacent (bottom-4,6) next → occupiedEndpoint next → next = (bottom-4,5))
    (hcatalogue : occupiedEndpoint (bottom-4,6) →
      freshAxialConsumer bottom near far width other) : False := by
  exact no_fresh_axial_consumer bottom near far width other hbottom hfar hwidth
    (hcatalogue (the_shared_support_is_forced bottom occupiedEndpoint heast hretained))

theorem remaining_even_escape_requires_fourteen (bottom incident : Int)
    (hminimum : 6 ≤ incident) (hupper : incident ≤ bottom-6)
    (heven : incident % 2 = 0) (hexcluded : incident ≠ 6) :
    8 ≤ incident ∧ 14 ≤ bottom := by omega

theorem no_remaining_escape_at_twelve (incident : Int)
    (hminimum : 6 ≤ incident) (hupper : incident ≤ 12-6)
    (hexcluded : incident ≠ 6) : False := by omega

def pairEndpoint (bottom near : Int) (point : Point) : Prop :=
  cornerEndpoint bottom near 6 point ∨ returnEndpoint bottom point

def cornerSelected (bottom near : Int) (point : Point) : Prop :=
  (point.1 = 2 ∧ 3 ≤ point.2 ∧ point.2 ≤ near+3 ∧ point.2 % 2 = 1) ∨
  (point.1 = 3 ∧ point.2 = near+4) ∨
  (point.1 = 4 ∧ 6 ≤ point.2 ∧ point.2 ≤ near+2 ∧ point.2 % 2 = 0) ∨
  (point.1 = bottom-1 ∧ (point.2 = 6 ∨ point.2 = 8))

def returnSelected (bottom : Int) (point : Point) : Prop :=
  (point.1 = bottom+2 ∧ (point.2 = 3 ∨ point.2 = 5 ∨ point.2 = 7 ∨
    point.2 = 9 ∨ point.2 = 11)) ∨
  (point.1 = bottom-5 ∧ (point.2 = 7 ∨ point.2 = 9 ∨ point.2 = 11)) ∨
  point = (bottom+1,2) ∨ point = (bottom-4,6) ∨ point = (bottom-3,8)

def pairSelected (bottom near : Int) (point : Point) : Prop :=
  cornerSelected bottom near point ∨ returnSelected bottom point

def pairOccupied (bottom near : Int) (point : Point) : Prop :=
  pairEndpoint bottom near point ∨ pairSelected bottom near point

theorem pair_endpoints_are_disjoint (bottom near : Int) (point : Point)
    (hbottom : 10 ≤ bottom) :
    ¬(cornerEndpoint bottom near 6 point ∧ returnEndpoint bottom point) := by
  unfold cornerEndpoint returnEndpoint endpoint
  dsimp
  omega

theorem corner_selected_are_exactly_unconsumed_original_supports
    (bottom near : Int) (point : Point) (hbottom : 10 ≤ bottom)
    (hnear : 4 ≤ near) (heven : near % 2 = 0) :
    cornerSelected bottom near point ↔
      (support (bottom-2) near 6 (point.2-3,point.1-2) ∧
        ¬pairEndpoint bottom near point) := by
  unfold cornerSelected pairEndpoint cornerEndpoint returnEndpoint support endpoint
  dsimp
  constructor
  · intro hselected
    rcases hselected with htop | htip | hinner | hfar
    all_goals constructor <;> omega
  · intro hselected
    rcases hselected with ⟨hsource,hnot⟩
    rcases hsource with hbar | hnearTip | hfarTip | hnearLeg | hfarLeg <;> omega

theorem return_selected_are_exactly_unconsumed_original_supports
    (bottom near : Int) (point : Point) (hbottom : 10 ≤ bottom) :
    returnSelected bottom point ↔
      (support 6 8 4 (11-point.2,bottom+2-point.1) ∧
        ¬pairEndpoint bottom near point) := by
  unfold returnSelected pairEndpoint cornerEndpoint returnEndpoint support endpoint
  simp only [Prod.ext_iff]
  dsimp
  constructor
  · intro hselected
    rcases hselected with hbottomrow | hreturntop | hreturntip | hreturninner | hreturnlast
    all_goals constructor <;> omega
  · intro hselected
    rcases hselected with ⟨hsource,hnot⟩
    rcases hsource with hbar | hnearTip | hfarTip | hnearLeg | hfarLeg <;> omega

theorem pair_selected_are_exactly_unconsumed_original_supports
    (bottom near : Int) (point : Point) (hbottom : 10 ≤ bottom)
    (hnear : 4 ≤ near) (heven : near % 2 = 0) :
    pairSelected bottom near point ↔
      ((support (bottom-2) near 6 (point.2-3,point.1-2) ∨
        support 6 8 4 (11-point.2,bottom+2-point.1)) ∧
        ¬pairEndpoint bottom near point) := by
  have hcorner := corner_selected_are_exactly_unconsumed_original_supports
    bottom near point hbottom hnear heven
  have hreturn := return_selected_are_exactly_unconsumed_original_supports
    bottom near point hbottom
  constructor
  · intro hselected
    rcases hselected with hselected | hselected
    · exact ⟨Or.inl (hcorner.mp hselected).1, (hcorner.mp hselected).2⟩
    · exact ⟨Or.inr (hreturn.mp hselected).1, (hreturn.mp hselected).2⟩
  · intro hselected
    rcases hselected with ⟨hsource,hnot⟩
    rcases hsource with hsource | hsource
    · exact Or.inl (hcorner.mpr ⟨hsource,hnot⟩)
    · exact Or.inr (hreturn.mpr ⟨hsource,hnot⟩)

theorem pair_selected_have_unique_occupied_neighbors
    (bottom near : Int) (point : Point) (hbottom : 10 ≤ bottom)
    (hnear : 4 ≤ near) (heven : near % 2 = 0)
    (hselected : pairSelected bottom near point) :
    ∃ anchor, pairEndpoint bottom near anchor ∧ adjacent point anchor ∧
      ∀ next, adjacent point next → pairOccupied bottom near next → next = anchor := by
  unfold pairSelected cornerSelected returnSelected at hselected
  rcases hselected with (htop | htip | hinner | hfar) |
    (hbottomrow | hreturntop | hreturntip | hreturninner | hreturnlast)
  · refine ⟨(3,point.2), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · refine ⟨(3,near+3), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · refine ⟨(3,point.2), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · refine ⟨(bottom,point.2), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · refine ⟨(bottom+1,point.2), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · refine ⟨(bottom-4,point.2), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · subst point
    refine ⟨(bottom+1,3), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · subst point
    refine ⟨(bottom-4,7), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega
  · subst point
    refine ⟨(bottom-4,8), ?_, ?_, ?_⟩
    · unfold pairEndpoint cornerEndpoint returnEndpoint endpoint
      dsimp
      omega
    · unfold adjacent
      dsimp
      omega
    · intro next hnext hoccupied
      unfold adjacent at hnext
      unfold pairOccupied pairEndpoint cornerEndpoint returnEndpoint endpoint pairSelected cornerSelected returnSelected at hoccupied
      simp only [Prod.ext_iff] at hoccupied
      try dsimp at *
      apply Prod.ext <;> dsimp <;> omega

end SubQuorum.IncidentSixNorthEscape
