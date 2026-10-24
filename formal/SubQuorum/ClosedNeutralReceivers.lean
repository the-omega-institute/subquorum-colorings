import Std

set_option autoImplicit false

namespace SubQuorum.ClosedNeutralReceivers

abbrev Corner := Fin 4

def adjacentPairs : List (Corner × Corner) :=
  [(0,1),(0,2),(1,3),(2,3)]

theorem opposite_pair_exhaustion :
    adjacentPairs.filter (fun pair =>
      decide (pair.1 ≠ 0 ∧ pair.1 ≠ 2 ∧ pair.2 ≠ 0 ∧ pair.2 ≠ 2)) =
      [(1,3)] := by decide

theorem remaining_pair_contains_forced_corner (pair : Corner × Corner)
    (hpair : pair ∈ adjacentPairs)
    (hfirst : pair.1 ≠ 0 ∧ pair.1 ≠ 2)
    (hsecond : pair.2 ≠ 0 ∧ pair.2 ≠ 2) :
    pair = (1,3) := by
  simp only [adjacentPairs, List.mem_cons, List.not_mem_nil, or_false] at hpair
  rcases hpair with rfl | rfl | rfl | rfl
  all_goals simp_all

theorem closed_pair_owner_is_active (owner : Corner → Nat)
    (closed : Nat → Prop) (active other : Nat) (pair : Corner × Corner)
    (hpair : pair ∈ adjacentPairs)
    (hzero : owner 0 = active) (htwo : owner 2 = active)
    (hforced : ¬ closed (owner 3)) (hclosed : closed other)
    (hfirst : owner pair.1 = other) (hsecond : owner pair.2 = other) :
    other = active := by
  simp only [adjacentPairs, List.mem_cons, List.not_mem_nil, or_false] at hpair
  rcases hpair with rfl | rfl | rfl | rfl
  · exact hfirst.symm.trans hzero
  · exact hfirst.symm.trans hzero
  · exact False.elim (hforced (hsecond.symm ▸ hclosed))
  · exact hfirst.symm.trans htwo

theorem receiver_map_injective_of_owner_separation {Contact Tile Owner : Type}
    (receiver : Contact → Tile) (active : Contact → Owner)
    (hdifferent : ∀ first second, receiver first = receiver second →
      active first ≠ active second → False)
    (hsame : ∀ first second, receiver first = receiver second →
      active first = active second → first = second) :
    ∀ first second, receiver first = receiver second → first = second := by
  intro first second hequal
  classical
  by_cases howner : active first = active second
  · exact hsame first second hequal howner
  · exact False.elim (hdifferent first second hequal howner)

theorem outside_endpoint_count (contacts stops full outside : Nat)
    (hpartition : contacts = stops+full)
    (hcount : outside = stops+2*full) :
    outside+stops = 2*contacts := by omega

theorem outside_endpoint_lower_bound (contacts stops outside boundary : Nat)
    (hcount : outside+stops = 2*contacts) (hstops : stops ≤ boundary) :
    2*contacts ≤ outside+boundary := by omega

theorem shared_outside_corner_budget
    (contacts stops outside counted activation boundary : Nat)
    (hcount : outside+stops = 2*contacts)
    (hshared : counted+stops ≤ 2*activation+boundary) :
    2*contacts+counted ≤ outside+2*activation+boundary := by omega

theorem phase_edge_incidence
    (phase01 phase10 edges01 edges10 mixed : Nat)
    (hfirst : 2*phase01 = 2*edges01+mixed)
    (hsecond : 2*phase10 = 2*edges10+mixed) :
    (edges01 : Int)-edges10 = (phase01 : Int)-phase10 := by omega

theorem AA_edges_from_no_phase10_edges
    (phase01 phase10 edges01 edges10 mixed : Nat)
    (hfirst : 2*phase01 = 2*edges01+mixed)
    (hsecond : 2*phase10 = 2*edges10+mixed) (hnone : edges10 = 0) :
    edges01+phase10 = phase01 := by omega

theorem AA_stops_vanish (stops boundary : Nat)
    (hstops : stops ≤ boundary) (hboundary : boundary = 0) :
    stops = 0 := by omega

theorem AA_eight_outside_endpoints
    (components phase01 phase10 contacts outside stops : Nat)
    (hphase : contacts+phase10 = phase01)
    (hturn : 4*components+phase10 ≤ phase01)
    (hcount : outside+stops = 2*contacts) (hstops : stops = 0) :
    8*components ≤ outside := by omega

end SubQuorum.ClosedNeutralReceivers
