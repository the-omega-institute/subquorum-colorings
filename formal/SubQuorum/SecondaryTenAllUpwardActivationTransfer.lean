import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenAllUpwardActivationTransfer

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

def secondary (bottom width : Int) (point : Point) : Prop :=
  endpoint width 10 4 (point.1-bottom+11,point.2-5)

def returning (bottom : Int) (point : Point) : Prop :=
  endpoint 6 8 4 (11-point.2,bottom+2-point.1)

def upward (bottom breadth incident far : Int) (point : Point) : Prop :=
  endpoint breadth incident far (incident+7-point.2,bottom-4-point.1)

def successor (bottom breadth bar near far : Int) (point : Point) : Prop :=
  endpoint breadth near far (bar-point.2,bottom-5-point.1)

def adjacent (point next : Point) : Prop :=
  (next.1 = point.1-1 ∧ next.2 = point.2) ∨
  (next.1 = point.1+1 ∧ next.2 = point.2) ∨
  (next.1 = point.1 ∧ next.2 = point.2-1) ∨
  (next.1 = point.1 ∧ next.2 = point.2+1)

def rotorA (bottom terminal : Int) (point : Point) : Prop :=
  (point.1 = bottom-9 ∧ point.2 = terminal-2) ∨
  (point.1 = bottom-8 ∧ terminal-2 ≤ point.2 ∧ point.2 ≤ terminal) ∨
  (point.1 = bottom-7 ∧ terminal-3 ≤ point.2 ∧ point.2 ≤ terminal-1) ∨
  (point.1 = bottom-6 ∧ point.2 = terminal-1)

def rotorB (bottom terminal : Int) (point : Point) : Prop :=
  (point.1 = bottom-9 ∧ point.2 = terminal) ∨
  (point.1 = bottom-8 ∧ terminal-2 ≤ point.2 ∧ point.2 ≤ terminal) ∨
  (point.1 = bottom-7 ∧ terminal-1 ≤ point.2 ∧ point.2 ≤ terminal+1) ∨
  (point.1 = bottom-6 ∧ point.2 = terminal-1)

theorem every_window_terminal_lies_between_the_two_wall_columns
    (width bar near : Int) (hlength : near ≤ bar-7) (hposition : bar-width-5 ≤ near) :
    7 ≤ bar-near ∧ bar-near ≤ width+5 := by omega

theorem rigidity_makes_the_bar_odd_and_bounds_the_incident_length
    (width incident bar near : Int) (hlower : width+7 ≤ bar) (hupper : bar ≤ incident+5)
    (heven : near % 2 = 0) (hrigid : bar-near = 7) :
    bar = near+7 ∧ bar % 2 = 1 ∧ width ≤ near ∧ near ≤ incident-2 := by omega

theorem a_nontight_rigid_successor_has_a_genuinely_larger_incident_length
    (width near : Int) (hevenWidth : width % 2 = 0) (hevenNear : near % 2 = 0)
    (hlower : width ≤ near) (hdifferent : near ≠ width) :
    width+2 ≤ near := by omega

theorem the_enlarged_top_interval_has_both_D_walls_and_the_north_bar
    (bottom width column : Int) (hwidth : 6 ≤ width)
    (hlower : 7 ≤ column) (hupper : column ≤ width+4) :
    secondary bottom width (bottom-9,6) ∧
      secondary bottom width (bottom-9,width+5) ∧
      secondary bottom width (bottom-10,column) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_top_U_bar_blockers_exist_for_every_upward_gap
    (bottom width breadth incident far column : Int)
    (_hwidth : 6 ≤ width) (hincident : width ≤ incident)
    (hlower : 7 ≤ column) (hupper : column ≤ width+4) :
    secondary bottom width (bottom-10,column) ∧
      upward bottom breadth incident far (bottom-5,column) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem three_top_rotor_blockers_extend_to_the_new_right_boundary
    (bottom width column : Int) (hlower : 7 ≤ column) (hupper : column ≤ width+4) :
    secondary bottom width (bottom-11,column+1) ∧
      secondary bottom width (bottom-11,column-1) ∧
      ((column = 7 ∧ secondary bottom width (bottom-9,column-1)) ∨
        (8 ≤ column ∧ secondary bottom width (bottom-10,column-2))) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_fourth_top_rotor_has_a_bar_or_right_wall_blocker
    (bottom width column : Int) (hlower : 7 ≤ column) (hupper : column ≤ width+4) :
    (column ≤ width+3 ∧ secondary bottom width (bottom-10,column+2)) ∨
      (column = width+4 ∧ secondary bottom width (bottom-9,column+1)) := by
  unfold secondary endpoint
  dsimp
  omega

theorem the_first_forced_point_is_not_a_prescribed_endpoint
    (bottom width breadth incident far nextBreadth bar near nextFar terminal : Int)
    (_hwidth : 6 ≤ width) (hbreadth : 6 ≤ breadth) (hnextBreadth : 6 ≤ nextBreadth)
    (hincident : width ≤ incident) (hbar : width+7 ≤ bar)
    (_hnear : 4 ≤ near) (hterminal : bar-near = terminal)
    (hlower : 8 ≤ terminal) (hupper : terminal ≤ width+5) :
    ¬returning bottom (bottom-6,terminal-1) ∧
      ¬secondary bottom width (bottom-6,terminal-1) ∧
      ¬upward bottom breadth incident far (bottom-6,terminal-1) ∧
      ¬successor bottom nextBreadth bar near nextFar (bottom-6,terminal-1) := by
  unfold returning secondary upward successor endpoint
  dsimp
  omega

theorem the_first_point_has_its_original_anchor_and_an_extra_south_neighbor
    (bottom width breadth incident far nextBreadth bar near nextFar terminal : Int)
    (hincident : width ≤ incident) (hnear : 4 ≤ near) (hterminal : bar-near = terminal)
    (hlower : 8 ≤ terminal) (hupper : terminal ≤ width+5) :
    support nextBreadth near nextFar (near+1,1) ∧
      successor bottom nextBreadth bar near nextFar (bottom-6,terminal) ∧
      upward bottom breadth incident far (bottom-5,terminal-1) ∧
      secondary bottom width (bottom-10,terminal-1) := by
  unfold support successor upward secondary endpoint
  dsimp
  omega

theorem west_A_is_blocked_even_at_terminal_eight
    (bottom width breadth incident far terminal : Int)
    (hincident : width ≤ incident) (hlower : 8 ≤ terminal) (hupper : terminal ≤ width+5) :
    (terminal = 8 ∧ secondary bottom width (bottom-5,terminal-2)) ∨
      (9 ≤ terminal ∧ upward bottom breadth incident far (bottom-5,terminal-2)) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem west_B_needs_no_H_blocker_at_terminal_eight
    (bottom width breadth incident far terminal : Int)
    (_hwidth : 6 ≤ width) (hincident : width ≤ incident)
    (hlower : 8 ≤ terminal) (hupper : terminal ≤ width+5) :
    (terminal = 8 ∧ secondary bottom width (bottom-8,terminal-2)) ∨
      (terminal = 9 ∧ secondary bottom width (bottom-5,terminal-3)) ∨
      (10 ≤ terminal ∧ upward bottom breadth incident far (bottom-5,terminal-3)) := by
  unfold secondary upward endpoint
  dsimp
  omega

theorem north_A_at_the_right_boundary_hits_D
    (bottom width : Int) (_hwidth : 6 ≤ width) :
    rotorA bottom (width+5) (bottom-8,width+5) ∧
      secondary bottom width (bottom-8,width+5) := by
  unfold rotorA secondary endpoint
  dsimp
  omega

theorem north_B_at_the_left_boundary_hits_D
    (bottom width : Int) (hwidth : 6 ≤ width) :
    rotorB bottom 8 (bottom-8,6) ∧ secondary bottom width (bottom-8,6) := by
  unfold rotorB secondary endpoint
  dsimp
  omega

theorem the_two_north_rotor_top_supports_are_not_own_endpoints
    (bottom terminal : Int) :
    ¬rotorA bottom terminal (bottom-9,terminal) ∧
      ¬rotorB bottom terminal (bottom-9,terminal-2) := by
  unfold rotorA rotorB
  dsimp
  omega

theorem the_two_north_rotor_original_anchors_are_owned
    (bottom terminal : Int) :
    rotorA bottom terminal (bottom-8,terminal) ∧
      rotorB bottom terminal (bottom-8,terminal-2) := by
  unfold rotorA rotorB
  dsimp
  omega

theorem surviving_rotors_force_sites_in_the_enlarged_forbidden_interval
    (width terminal : Int) (hlower : 8 ≤ terminal) (hupper : terminal ≤ width+5) :
    (terminal ≤ width+4 → 7 ≤ terminal ∧ terminal ≤ width+4) ∧
      (9 ≤ terminal → 7 ≤ terminal-2 ∧ terminal-2 ≤ width+4) := by omega

theorem original_support_retention_forces_a_second_top_consumer
    (bottom column : Int) (occupied endpointAt : Point → Prop)
    (hnorth : occupied (bottom-10,column))
    (hretain : ¬endpointAt (bottom-9,column) →
      ∀ point, adjacent (bottom-9,column) point → occupied point → point = (bottom-8,column)) :
    endpointAt (bottom-9,column) := by
  by_cases hpoint : endpointAt (bottom-9,column)
  · exact hpoint
  · have hequal := hretain hpoint (bottom-10,column)
      (by unfold adjacent; dsimp; omega) hnorth
    have hrow := congrArg Prod.fst hequal
    dsimp at hrow
    omega

theorem the_full_two_stage_catalogue_adapter_implies_terminal_rigidity
    (bottom width bar near : Int) (endpointAt : Point → Prop)
    (hwindow : 7 ≤ bar-near ∧ bar-near ≤ width+5)
    (hfirst : 8 ≤ bar-near → endpointAt (bottom-6,bar-near-1))
    (hcatalogue : 8 ≤ bar-near → endpointAt (bottom-6,bar-near-1) →
      ((bar-near ≤ width+4 ∧ endpointAt (bottom-9,bar-near)) ∨
        (9 ≤ bar-near ∧ endpointAt (bottom-9,bar-near-2))))
    (htop : ∀ column, 7 ≤ column → column ≤ width+4 → ¬endpointAt (bottom-9,column)) :
    bar-near = 7 := by
  by_cases hequal : bar-near = 7
  · exact hequal
  exfalso
  have hlower : 8 ≤ bar-near := by omega
  rcases hcatalogue hlower (hfirst hlower) with hleft | hright
  · exact htop (bar-near) (by omega) hleft.1 hleft.2
  · exact htop (bar-near-2) (by omega) (by omega) hright.2

theorem every_rigid_terminal_has_the_same_two_consumed_original_supports
    (bottom width breadth incident far nextBreadth bar near nextFar : Int)
    (hwidth : 6 ≤ width) (hincident : width ≤ incident)
    (hnear : 4 ≤ near) (heven : near % 2 = 0) (hrigid : bar-near = 7) :
    successor bottom nextBreadth bar near nextFar (bottom-6,7) ∧
      support nextBreadth near nextFar (near+1,1) ∧
      support nextBreadth near nextFar (near,0) ∧
      secondary bottom width (bottom-6,6) ∧ upward bottom breadth incident far (bottom-5,7) := by
  unfold successor support secondary upward endpoint
  dsimp
  omega

def oldS (near row column : Int) : Point := (near+3-row,3-column)
def oldP (row column : Int) : Point := (column+2,row+2)
def oldE (near row column : Int) : Point := (column+2,near+3-row)
def oldCompanionS (near row column : Int) : Point := (near+3-row,column+2)
def frameS (bottom : Int) (point : Point) : Point := (bottom-8+point.2,point.1+4)
def frameP (bottom near : Int) (point : Point) : Point := (bottom-3-point.1,near+9-point.2)
def frameE (bottom : Int) (point : Point) : Point := (bottom-3-point.1,point.2+4)
def frameCompanionS (bottom : Int) (point : Point) : Point := (bottom-3-point.2,point.1+4)

theorem all_old_recipient_frames_compose_for_arbitrary_new_incident_length
    (bottom near row column : Int) :
    frameS bottom (oldS near row column) = (bottom-5-column,near+7-row) ∧
      frameP bottom near (oldP row column) = (bottom-5-column,near+7-row) ∧
      frameE bottom (oldE near row column) = (bottom-5-column,near+7-row) ∧
      frameCompanionS bottom (oldCompanionS near row column) = (bottom-5-column,near+7-row) := by
  unfold frameS oldS frameP oldP frameE oldE frameCompanionS oldCompanionS
  simp only [Prod.ext_iff]
  omega

theorem the_old_P_width_bound_supplies_both_mandatory_bar_endpoints
    (width near oldNear oldFar : Int) (hnear : 4 ≤ near) (hwidth : near+4 ≤ width) :
    endpoint width oldNear oldFar (0,near+3) ∧
      endpoint width oldNear oldFar (1,near+2) := by
  unfold endpoint
  dsimp
  omega

theorem both_old_P_images_are_fixed_D_and_Q_endpoints
    (bottom width near : Int) :
    frameP bottom near (0,near+3) = (bottom-3,6) ∧
      frameP bottom near (1,near+2) = (bottom-4,7) ∧
      secondary bottom width (bottom-3,6) ∧ returning bottom (bottom-4,7) := by
  unfold frameP secondary returning endpoint
  simp only [Prod.ext_iff]
  dsimp
  omega

theorem equal_recovered_D_and_E_incident_lengths_cannot_have_different_gap_classes
    (width incident oldWidth oldIncident : Int)
    (hwidth : width = oldWidth) (hincident : incident = oldIncident)
    (hold : oldIncident = oldWidth+2) (hnew : width+4 ≤ incident) : False := by omega

def ceilHalf (value : Int) : Int := (value+1)/2

theorem the_same_inventory_all_upward_single_activation_bound
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve) :
    unmarked+upper+pairs+ceilHalf (m8-resolved-residual+extra+added) ≤
      positiveCount+reserve-total := by
  unfold ceilHalf
  omega

theorem every_two_larger_gap_claims_gain_one (baseline added : Int) :
    ceilHalf (baseline+added+2)-ceilHalf (baseline+added) = 1 := by
  unfold ceilHalf
  omega

theorem the_all_upward_coefficient_one_sufficient_threshold
    (positiveCount reserve total unmarked upper pairs m8 resolved residual oldClaims added extra caps : Int)
    (hgate : total ≤ 2*(positiveCount-unmarked))
    (hcount : total = oldClaims+caps+resolved+residual)
    (hreserve : oldClaims+added+extra+m8+caps+2*pairs+2*upper ≤ 2*reserve)
    (hthreshold : resolved+residual ≤ 2*unmarked+2*upper+2*pairs+m8+extra+added+1) :
    0 ≤ positiveCount+reserve-total := by omega

end SubQuorum.SecondaryTenAllUpwardActivationTransfer
