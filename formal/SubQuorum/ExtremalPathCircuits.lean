import SubQuorum.EndpointComponentResourceGluing

set_option autoImplicit false

namespace SubQuorum.ExtremalPathCircuits

/-- The upper seam-tile cell already faces a fixed endpoint. Selecting its
lower neighbor as well supplies two DISTINCT occupied neighbors. -/
theorem seam_selected_pair_forbidden {V : Type} (selected occupied : V → Prop)
    (adjacent : V → V → Prop) (upper lower fixed : V)
    (selectedOccupied : ∀ v, selected v → occupied v)
    (fixedOccupied : occupied fixed) (fixedNeighbor : adjacent upper fixed)
    (lowerNeighbor : adjacent upper lower) (different : fixed≠lower)
    (feasible : selected upper → ∀ u v, adjacent upper u → adjacent upper v →
      occupied u → occupied v → u=v) : ¬(selected upper ∧ selected lower) := by
  intro both
  exact different (feasible both.1 fixed lower fixedNeighbor lowerNeighbor
    fixedOccupied (selectedOccupied lower both.2))

def bit (b : Bool) : Nat := if b then 1 else 0

theorem open_seam_tile_cap (a b c d : Bool) (emptyC : c=false) (emptyD : d=false)
    (forbidden : ¬(a=true ∧ b=true)) : bit a+bit b+bit c+bit d≤1 := by
  subst c
  subst d
  cases a <;> cases b <;> simp_all [bit]

/-- Geometry supplies one disjoint cover, replacing 2k patches and then
charging each open seam once. No minimum from separate covers is added. -/
theorem exact_opening_budget (selected initialCap modules opened : Int)
    (oneCover : selected≤initialCap-2*modules-opened) :
    selected+opened≤initialCap-2*modules := by omega

theorem deformation_slack_deficit (k m s d raw : Int)
    (slack : s=2*k+m) (deficit : d=k-m) (ledger : raw=s+k) :
    s+d=3*k ∧ raw=3*k+m := by omega

/-- Edges are numbered 1,...,k-1, joining source vertices i-1 and i. -/
def payEdge (omitted vertex : Nat) : Nat :=
  if vertex<omitted then vertex+1 else vertex

theorem basis_edge_in_range (k r a : Nat) (hr : r<k) (ha : a<k) (different : a≠r) :
    1≤payEdge r a ∧ payEdge r a<k := by
  unfold payEdge
  split <;> omega

theorem basis_edge_incident (r a : Nat) : payEdge r a=a ∨ payEdge r a=a+1 := by
  unfold payEdge
  split
  · exact Or.inr rfl
  · exact Or.inl rfl

/-- A single omitted source yields distinct original resources for ALL
remaining sources, for arbitrary length rather than an enumerated bound. -/
theorem basis_edge_injective (r a b : Nat) (ha : a≠r) (hb : b≠r)
    (same : payEdge r a=payEdge r b) : a=b := by
  unfold payEdge at same
  split at same <;> split at same <;> omega

/-- In a full maximum paid basis, force allocations from the left boundary
until the omitted vertex. The source at zero cannot use nonexistent edge0. -/
theorem allocation_forced_left (k r : Nat) (f : Nat → Nat) (hr : r<k)
    (incident : ∀ a, a<k → a≠r → f a=a ∨ f a=a+1)
    (valid : ∀ a, a<k → a≠r → 1≤f a ∧ f a<k)
    (injective : ∀ a b, a<k → b<k → a≠r → b≠r → f a=f b → a=b) :
    ∀ a, a<r → f a=a+1 := by
  intro a
  induction a with
  | zero =>
    intro before
    have inc := incident 0 (by omega) (by omega)
    have pos := (valid 0 (by omega) (by omega)).1
    omega
  | succ a ih =>
    intro before
    have previous := ih (by omega)
    have inc := incident (a+1) (by omega) (by omega)
    cases inc with
    | inl same =>
      have collision := injective a (a+1) (by omega) (by omega) (by omega) (by omega)
        (previous.trans same.symm)
      omega
    | inr yes => exact yes

/-- Reverse induction from the right boundary. The last source cannot use
nonexistent edge k; every next left choice would collide with its neighbor. -/
theorem allocation_forced_right_distance (k r : Nat) (f : Nat → Nat)
    (incident : ∀ a, a<k → a≠r → f a=a ∨ f a=a+1)
    (valid : ∀ a, a<k → a≠r → 1≤f a ∧ f a<k)
    (injective : ∀ a b, a<k → b<k → a≠r → b≠r → f a=f b → a=b) :
    ∀ distance a, a+distance+1=k → r<a → f a=a := by
  intro distance
  induction distance with
  | zero =>
    intro a count after
    have inc := incident a (by omega) (by omega)
    have bound := (valid a (by omega) (by omega)).2
    omega
  | succ distance ih =>
    intro a count after
    have next := ih (a+1) (by omega) (by omega)
    have inc := incident a (by omega) (by omega)
    cases inc with
    | inl yes => exact yes
    | inr same =>
      have collision := injective a (a+1) (by omega) (by omega) (by omega) (by omega)
        (same.trans next.symm)
      omega

theorem allocation_forced_right (k r : Nat) (f : Nat → Nat)
    (incident : ∀ a, a<k → a≠r → f a=a ∨ f a=a+1)
    (valid : ∀ a, a<k → a≠r → 1≤f a ∧ f a<k)
    (injective : ∀ a b, a<k → b<k → a≠r → b≠r → f a=f b → a=b)
    (a : Nat) (ha : a<k) (after : r<a) : f a=a :=
  allocation_forced_right_distance k r f incident valid injective (k-1-a) a (by omega) after

theorem maximum_basis_allocation_unique (k r : Nat) (f : Nat → Nat) (hr : r<k)
    (incident : ∀ a, a<k → a≠r → f a=a ∨ f a=a+1)
    (valid : ∀ a, a<k → a≠r → 1≤f a ∧ f a<k)
    (injective : ∀ a b, a<k → b<k → a≠r → b≠r → f a=f b → a=b) :
    ∀ a, a<k → a≠r → f a=payEdge r a := by
  intro a ha different
  unfold payEdge
  split
  · exact allocation_forced_left k r f hr incident valid injective a (by omega)
  · exact allocation_forced_right k r f incident valid injective a ha (by omega)

theorem maximum_basis_exact_link_count (k r : Nat) (hr : r<k) :
    2*r+(k-1-r)=k-1+r := by omega

/-- Reuse the earlier arbitrary-length path injection. The new geometric
adapter makes it apply to the FULL original pool, not only a restricted one. -/
theorem proper_withdrawal_injection (k r : Nat) (deleted : Nat → Prop)
    (hr : r+1<k) (kept : ¬deleted r) :
    (∀ v, v<k → EndpointComponentResourceGluing.Lost k deleted v →
      EndpointComponentResourceGluing.parentEdge r v+1<k ∧
      deleted (EndpointComponentResourceGluing.parentEdge r v)) ∧
    (∀ a b, EndpointComponentResourceGluing.Lost k deleted b →
      EndpointComponentResourceGluing.parentEdge r a=
        EndpointComponentResourceGluing.parentEdge r b → a=b) :=
  EndpointComponentResourceGluing.lost_vertices_inject_into_deleted_edges k r deleted hr kept

/-- Once all k-1 path units are withdrawn, one extra inaccessible original
already removes the positive excess. This is why Qpath alone is unique. -/
theorem all_path_withdrawn_unique_positive (k extra : Nat) :
    (k:Int)-((k:Int)-1+(extra:Int))>0 ↔ extra=0 := by omega

theorem one_below_maximum_mixed (w : Int) :
    (8*w+8)-1=8*w+7 ∧ (11*w+22)-(8*w+7)-(3*w+10)=5 := by omega

abbrev Point := Nat × Nat
abbrev Original := Nat × Nat × Nat
def selected : List Point := [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 11), (0, 13), (0, 15), (0, 17), (0, 19), (0, 21), (0, 23), (0, 25), (0, 27), (0, 29), (0, 31), (1, 0), (1, 2), (1, 10), (1, 12), (1, 20), (1, 22), (1, 30), (2, 0), (2, 8), (2, 11), (2, 18), (2, 21), (2, 28), (2, 31), (3, 1), (3, 3), (3, 7), (3, 9), (3, 11), (3, 13), (3, 17), (3, 19), (3, 21), (3, 23), (3, 27), (3, 29), (3, 31), (4, 0), (4, 2), (4, 8), (4, 10), (4, 12), (4, 18), (4, 20), (4, 22), (4, 28), (4, 30), (5, 0), (5, 2), (5, 7), (5, 9), (5, 11), (5, 13), (5, 17), (5, 19), (5, 21), (5, 23), (5, 27), (5, 29), (5, 31), (6, 1), (6, 3), (6, 8), (6, 10), (6, 12), (6, 18), (6, 20), (6, 22), (6, 28), (6, 30), (7, 0), (7, 11), (7, 21), (7, 31), (8, 0), (8, 2), (8, 10), (8, 12), (8, 20), (8, 22), (8, 30), (9, 1), (9, 3), (9, 5), (9, 7), (9, 9), (9, 13), (9, 15), (9, 17), (9, 19), (9, 23), (9, 25), (9, 27), (9, 29), (9, 31)]
def matching : List (Point × Point) := [((1, 5), (2, 5)), ((3, 5), (4, 5)), ((5, 5), (6, 5)), ((7, 5), (8, 5)), ((2, 6), (3, 6)), ((4, 6), (5, 6)), ((6, 6), (7, 6)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((8, 6), (8, 7)), ((8, 8), (8, 9)), ((7, 7), (7, 8)), ((1, 3), (1, 4)), ((2, 4), (3, 4)), ((8, 3), (8, 4)), ((7, 4), (6, 4)), ((4, 4), (5, 4)), ((1, 15), (2, 15)), ((3, 15), (4, 15)), ((5, 15), (6, 15)), ((7, 15), (8, 15)), ((2, 16), (3, 16)), ((4, 16), (5, 16)), ((6, 16), (7, 16)), ((1, 16), (1, 17)), ((1, 18), (1, 19)), ((8, 16), (8, 17)), ((8, 18), (8, 19)), ((7, 17), (7, 18)), ((1, 13), (1, 14)), ((2, 14), (3, 14)), ((8, 13), (8, 14)), ((7, 14), (6, 14)), ((4, 14), (5, 14)), ((1, 25), (2, 25)), ((3, 25), (4, 25)), ((5, 25), (6, 25)), ((7, 25), (8, 25)), ((2, 26), (3, 26)), ((4, 26), (5, 26)), ((6, 26), (7, 26)), ((1, 26), (1, 27)), ((1, 28), (1, 29)), ((8, 26), (8, 27)), ((8, 28), (8, 29)), ((7, 27), (7, 28)), ((1, 23), (1, 24)), ((2, 24), (3, 24)), ((8, 23), (8, 24)), ((7, 24), (6, 24)), ((4, 24), (5, 24))]
def actualPairs : List (Point × Point) := [((1, 3), (1, 4)), ((1, 5), (8, 5)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((1, 13), (1, 14)), ((1, 15), (8, 15)), ((1, 16), (1, 17)), ((1, 18), (1, 19)), ((1, 23), (1, 24)), ((1, 25), (8, 25)), ((1, 26), (1, 27)), ((1, 28), (1, 29)), ((7, 7), (7, 8)), ((7, 17), (7, 18)), ((7, 27), (7, 28)), ((8, 3), (8, 4)), ((8, 6), (8, 7)), ((8, 8), (8, 9)), ((8, 13), (8, 14)), ((8, 16), (8, 17)), ((8, 18), (8, 19)), ((8, 23), (8, 24)), ((8, 26), (8, 27)), ((8, 28), (8, 29))]
def ownerLinks : List (Nat × Nat) := [(1, 0), (1, 2), (1, 15), (1, 16), (2, 3), (5, 4), (5, 6), (5, 18), (5, 19), (6, 7), (9, 8), (9, 10), (9, 21), (9, 22), (10, 11), (16, 17), (19, 20), (22, 23)]
def roots : List Nat := [1, 5, 9]
def reachable : List Nat := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17, 18, 19, 20, 21, 22, 23]
def originalUnits : List Original := [(1, 2, 2), (1, 10, 12), (1, 20, 22), (3, 2, 2), (3, 9, 9), (3, 13, 13), (3, 19, 19), (3, 23, 23), (3, 29, 29), (4, 11, 11), (4, 21, 21)]
def openedUnits : List Original := [(4, 11, 11), (4, 21, 21)]
def actualSupports : List (Nat × List Original) := [(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, []), (12, [(3, 9, 9), (3, 13, 13)]), (13, [(3, 19, 19), (3, 23, 23)]), (14, [(3, 29, 29)]), (15, []), (16, []), (17, [(4, 11, 11)]), (18, [(4, 11, 11)]), (19, []), (20, [(4, 21, 21)]), (21, [(4, 21, 21)]), (22, []), (23, [])]

theorem actual_full_pool_counts : selected.length=101 ∧ matching.length=51 ∧
    roots.length=3 ∧ reachable.length=21 ∧ originalUnits.length=11 ∧
    openedUnits.length=2 ∧ 103-2=101 ∧ 10*32/2-101-51=8 := by decide

/-- Boolean finite certificates checked against the actual compiler, with
all extra original units retained. Their general geometry is written. -/
theorem actual_full_pool_closed_table :
    (roots.all fun o => decide (o ∈ reachable))=true ∧
    (ownerLinks.all fun e => decide (e.1 ∉ reachable ∨ e.2 ∈ reachable))=true ∧
    ((actualSupports.filter fun row => decide (row.1 ∈ reachable)).all fun row =>
      row.2.all fun j => decide (j ∈ openedUnits))=true ∧
    openedUnits.Nodup := by decide

#print axioms seam_selected_pair_forbidden
#print axioms open_seam_tile_cap
#print axioms exact_opening_budget
#print axioms deformation_slack_deficit
#print axioms basis_edge_in_range
#print axioms basis_edge_incident
#print axioms basis_edge_injective
#print axioms allocation_forced_left
#print axioms allocation_forced_right_distance
#print axioms allocation_forced_right
#print axioms maximum_basis_allocation_unique
#print axioms maximum_basis_exact_link_count
#print axioms proper_withdrawal_injection
#print axioms all_path_withdrawn_unique_positive
#print axioms one_below_maximum_mixed
#print axioms actual_full_pool_counts
#print axioms actual_full_pool_closed_table

end SubQuorum.ExtremalPathCircuits
