import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.FiveEndpointCap

abbrev Point := Int × Int

def neighbors (point : Point) : List Point :=
  [(point.1-1,point.2),(point.1+1,point.2),
   (point.1,point.2-1),(point.1,point.2+1)]

def uEndpoint (width leftHeight rightHeight : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ width) ∨
  (2 ≤ point.1 ∧ point.1 ≤ leftHeight ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ rightHeight ∧ point.2 = width)

theorem a_u_single_neighbor_is_a_terminal
    (width leftHeight rightHeight : Int) (point next : Point)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hpoint : uEndpoint width leftHeight rightHeight point)
    (hsingle : ∀ other, other ∈ neighbors point →
      uEndpoint width leftHeight rightHeight other → other = next) :
    point = (leftHeight,1) ∨ point = (rightHeight,width) := by
  rcases point with ⟨row, column⟩
  dsimp only [uEndpoint] at hpoint
  rcases hpoint with ⟨hbar, hcolumn, hlast⟩ | ⟨hrow, hheight, hcolumn⟩ |
    ⟨hrow, hheight, hcolumn⟩
  · have hvertical : uEndpoint width leftHeight rightHeight (1-row,column) := by
      unfold uEndpoint
      dsimp
      omega
    have hverticalAdjacent : (1-row,column) ∈ neighbors (row,column) := by
      rcases hbar with hzero | hone
      · subst row
        simp [neighbors]
      · subst row
        simp [neighbors]
    by_cases hfirst : column = 1
    · have hhorizontal : uEndpoint width leftHeight rightHeight (row,column+1) := by
        unfold uEndpoint
        dsimp
        omega
      have hequal := (hsingle (1-row,column) hverticalAdjacent hvertical).trans
        (hsingle (row,column+1) (by simp [neighbors]) hhorizontal).symm
      have hcoordinates := congrArg Prod.fst hequal
      dsimp at hcoordinates
      omega
    · have hhorizontal : uEndpoint width leftHeight rightHeight (row,column-1) := by
        unfold uEndpoint
        dsimp
        omega
      have hequal := (hsingle (1-row,column) hverticalAdjacent hvertical).trans
        (hsingle (row,column-1) (by simp [neighbors]) hhorizontal).symm
      have hcoordinates := congrArg Prod.fst hequal
      dsimp at hcoordinates
      omega
  · by_cases hterminal : row = leftHeight
    · exact Or.inl (Prod.ext hterminal hcolumn)
    have hupper : uEndpoint width leftHeight rightHeight (row-1,column) := by
      unfold uEndpoint
      dsimp
      omega
    have hlower : uEndpoint width leftHeight rightHeight (row+1,column) := by
      unfold uEndpoint
      dsimp
      omega
    have hequal := (hsingle (row-1,column) (by simp [neighbors]) hupper).trans
      (hsingle (row+1,column) (by simp [neighbors]) hlower).symm
    have hcoordinates := congrArg Prod.fst hequal
    dsimp at hcoordinates
    omega
  · by_cases hterminal : row = rightHeight
    · exact Or.inr (Prod.ext hterminal hcolumn)
    have hupper : uEndpoint width leftHeight rightHeight (row-1,column) := by
      unfold uEndpoint
      dsimp
      omega
    have hlower : uEndpoint width leftHeight rightHeight (row+1,column) := by
      unfold uEndpoint
      dsimp
      omega
    have hequal := (hsingle (row-1,column) (by simp [neighbors]) hupper).trans
      (hsingle (row+1,column) (by simp [neighbors]) hlower).symm
    have hcoordinates := congrArg Prod.fst hequal
    dsimp at hcoordinates
    omega

theorem a_u_single_neighbor_continues_four_steps
    (width leftHeight rightHeight : Int) (point next : Point)
    (hwidth : 6 ≤ width) (hleft : 4 ≤ leftHeight) (hright : 4 ≤ rightHeight)
    (hpoint : uEndpoint width leftHeight rightHeight point)
    (hsingle : ∀ other, other ∈ neighbors point →
      uEndpoint width leftHeight rightHeight other → other = next) :
    uEndpoint width leftHeight rightHeight
      (point.1+4*(next.1-point.1),point.2+4*(next.2-point.2)) := by
  have hterminal := a_u_single_neighbor_is_a_terminal width leftHeight rightHeight
    point next hwidth hleft hright hpoint hsingle
  rcases hterminal with hterminal | hterminal
  · subst point
    have hprevious : uEndpoint width leftHeight rightHeight (leftHeight-1,1) := by
      unfold uEndpoint
      dsimp
      omega
    have hequal := hsingle (leftHeight-1,1) (by simp [neighbors]) hprevious
    subst next
    unfold uEndpoint
    dsimp
    omega
  · subst point
    have hprevious : uEndpoint width leftHeight rightHeight (rightHeight-1,width) := by
      unfold uEndpoint
      dsimp
      omega
    have hequal := hsingle (rightHeight-1,width) (by simp [neighbors]) hprevious
    subst next
    unfold uEndpoint
    dsimp
    omega

def blockingStencil : List Point := [(1,2),(2,1),(3,2),(2,6),(1,4)]

def fourPointStencil : List Point := [(1,2),(2,1),(3,2),(1,4)]

def rotorEndpoints : List Point :=
  [(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)]

def rotorAtRole (reflected : Bool) (role : Point) : List Point :=
  rotorEndpoints.map fun point =>
    (2+point.1-role.1,
     2+(if reflected then -point.2 else point.2)-
       (if reflected then -role.2 else role.2))

theorem all_sixteen_rotor_owner_roles_hit_the_cap :
    ([false,true].all fun reflected => rotorEndpoints.all fun role =>
      (rotorAtRole reflected role).any fun point => blockingStencil.contains point) = true := by
  decide

theorem all_sixteen_rotor_owner_roles_hit_the_four_point_cap :
    ([false,true].all fun reflected => rotorEndpoints.all fun role =>
      (rotorAtRole reflected role).any fun point => fourPointStencil.contains point) = true := by
  decide

def rotorSupports : List Point :=
  [(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)]

def producerRing : List Point := [(1,1),(1,2),(1,3),(1,4),(2,1),(3,1),(4,1)]

def rotorPointsAtGate (reflected : Bool) (role : Point) (points : List Point) : List Point :=
  points.map fun point =>
    (3+point.1-role.1,
     2+(if reflected then -point.2 else point.2)-
       (if reflected then -role.2 else role.2))

theorem every_rotor_gate_role_collides_or_has_the_forced_support :
    ([false,true].all fun reflected => rotorEndpoints.all fun role =>
      ((rotorPointsAtGate reflected role rotorEndpoints).any fun point => producerRing.contains point) ||
      (rotorPointsAtGate reflected role rotorSupports).contains (2,2)) = true := by
  decide

theorem the_transverse_even_height_is_at_most_width_minus_four
    (width height halfWidth halfHeight : Int)
    (hwidth : width = 2*halfWidth) (hheight : height = 2*halfHeight)
    (hshort : height < width-2) : height ≤ width-4 := by
  omega

theorem the_transverse_cap_requires_width_at_least_eight
    (width height halfWidth halfHeight : Int)
    (hwidth : width = 2*halfWidth) (hheight : height = 2*halfHeight)
    (hminimum : 4 ≤ height) (hshort : height < width-2) : 8 ≤ width := by
  have hbound := the_transverse_even_height_is_at_most_width_minus_four
    width height halfWidth halfHeight hwidth hheight hshort
  omega

theorem five_endpoint_cap_blocks_an_original_owner
    (belongs : Point → Prop) (hpoint : belongs (2,2))
    (havoid : ∀ point, point ∈ blockingStencil → ¬belongs point)
    (hrole : belongs (2,2) →
      (∀ other, other ∈ neighbors (2,2) → belongs other → other = (2,3)) →
      belongs (2,6) ∨ belongs (1,4)) : False := by
  have hsingle : ∀ other, other ∈ neighbors (2,2) → belongs other → other = (2,3) := by
    intro other hneighbor hbelongs
    simp [neighbors] at hneighbor
    rcases hneighbor with hupper | hlower | hfirst | hsecond
    · subst other
      exact False.elim (havoid (1,2) (by simp [blockingStencil]) hbelongs)
    · subst other
      exact False.elim (havoid (3,2) (by simp [blockingStencil]) hbelongs)
    · subst other
      exact False.elim (havoid (2,1) (by simp [blockingStencil]) hbelongs)
    · exact hsecond
  rcases hrole hpoint hsingle with hfar | hrotor
  · exact havoid (2,6) (by simp [blockingStencil]) hfar
  · exact havoid (1,4) (by simp [blockingStencil]) hrotor

theorem a_regular_singleton_gate_consumer_is_activated
    (occupied endpoint : Point → Prop)
    (hproducer : occupied (2,1))
    (hselected : ¬endpoint (2,2) → ∀ other, other ∈ neighbors (2,2) →
      occupied other → other = (3,2)) : endpoint (2,2) := by
  apply Classical.byContradiction
  intro hnot
  have hequal := hselected hnot (2,1) (by simp [neighbors]) hproducer
  cases hequal

end SubQuorum.FiveEndpointCap
