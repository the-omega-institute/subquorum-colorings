import SubQuorum.GuardedSteppedArms

set_option autoImplicit false

namespace SubQuorum.SteppedPatchIsolation

open OwnedDonorCompensation

theorem port_degree_at_most_two (state : Int → Int → Label)
    (hleft : state (-1) 2 = .blank) (hright : state (-1) 4 = .blank) :
    degree state (-1) 3 ≤ 2 := by
  cases hnorth : state (-2) 3 <;> cases hsouth : state 0 3 <;>
    simp_all [degree, occupied]

theorem matched_boundary_exclusion {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (endpoint core : Vertex → Prop)
    (mate : Vertex → Vertex) (vertex : Vertex)
    (houtside : ¬core vertex)
    (hinvolution : ∀ point, mate (mate point) = point)
    (hclosed : ∀ point, core point → core (mate point))
    (hendpointMate : ∀ point, endpoint point → endpoint (mate point))
    (hadjacentMate : ∀ point, endpoint point → adjacent point (mate point))
    (havailable : ∀ neighbor, adjacent vertex neighbor → endpoint neighbor → core neighbor) :
    ¬endpoint vertex := by
  intro hvertex
  have hmate := havailable (mate vertex) (hadjacentMate vertex hvertex)
    (hendpointMate vertex hvertex)
  have hreturn := hclosed (mate vertex) hmate
  exact houtside (by simpa [hinvolution vertex] using hreturn)

inductive EndpointReach {Vertex : Type} (adjacent : Vertex → Vertex → Prop)
    (endpoint : Vertex → Prop) (root : Vertex) : Vertex → Prop where
  | root : EndpointReach adjacent endpoint root root
  | step {first second : Vertex} : EndpointReach adjacent endpoint root first →
      adjacent first second → endpoint second → EndpointReach adjacent endpoint root second

theorem reachable_stays_in_core {Vertex : Type}
    (adjacent : Vertex → Vertex → Prop) (endpoint core : Vertex → Prop)
    (root vertex : Vertex) (hroot : core root)
    (hboundary : ∀ first second, core first → adjacent first second → endpoint second → core second)
    (hpath : EndpointReach adjacent endpoint root vertex) : core vertex := by
  induction hpath with
  | root => exact hroot
  | step hprevious hadjacent hendpoint inductionHypothesis =>
      exact hboundary _ _ inductionHypothesis hadjacent hendpoint

theorem promoted_port_feasible (state : Int → Int → Label)
    (hremoved : state (-2) 3 = .blank)
    (hleft : state (-1) 2 = .blank) (hright : state (-1) 4 = .blank)
    (hanchor : state 0 3 = .endpoint) : feasibleAt state (-1) 3 := by
  simp [feasibleAt, degree, occupied, hremoved, hleft, hright, hanchor]

end SubQuorum.SteppedPatchIsolation
