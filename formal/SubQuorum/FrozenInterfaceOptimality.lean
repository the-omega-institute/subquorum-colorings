import SubQuorum.OpposedDirectionInterfaces

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

namespace SubQuorum.FrozenInterfaceOptimality
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)

/-- Any inductive freezing derivation has two distinct occupied nonmate
neighbours at its last step. This only asserts a necessary condition. -/
theorem frozen_two_occupied {V : Type} {P T : V → Prop} {mate : V → V}
    {adj : V → V → Prop} {v : V} (f : Frozen P T mate adj v) :
    ∃ a b, a ≠ b ∧ adj v a ∧ adj v b ∧ (T a ∨ P a) ∧ (T b ∨ P b) := by
  cases f with
  | ss _ ne va vb ta tb => exact ⟨_,_,ne,va,vb,Or.inl ta,Or.inl tb⟩
  | sp _ ne va vb ta pb _ => exact ⟨_,_,ne,va,vb,Or.inl ta,Or.inr pb⟩
  | ps _ ne va vb pa _ tb => exact ⟨_,_,ne,va,vb,Or.inr pa,Or.inl tb⟩
  | pp _ ne va vb pa _ pb _ => exact ⟨_,_,ne,va,vb,Or.inr pa,Or.inr pb⟩

/-- Zero or one possible occupied witness cannot freeze an endpoint,
regardless of the ranks assigned to the other endpoints. -/
theorem single_possible_witness_not_frozen {V : Type} {P T : V → Prop}
    {mate : V → V} {adj : V → V → Prop} {v w : V}
    (only : ∀ u, adj v u → (T u ∨ P u) → u=w) :
    ¬ Frozen P T mate adj v := by
  intro f
  obtain ⟨a,b,ne,va,vb,oa,ob⟩ := frozen_two_occupied f
  exact ne ((only a va oa).trans (only b vb ob).symm)

/-- An integer packing cut for the physical four-tile interface. All
conditions are necessary consequences of the stated endpoint stencil,
feasibility and freezing of two specific endpoints. -/
theorem local_packing_cut
    (a b c d e f g h i j k u : Int)
    (ha : 0≤a ∧ a≤1) (_hb : 0≤b ∧ b≤1) (_hc : 0≤c ∧ c≤1)
    (_hd : 0≤d ∧ d≤1) (_he : 0≤e ∧ e≤1) (hf : 0≤f ∧ f≤1)
    (_hg : 0≤g ∧ g≤1) (_hh : 0≤h ∧ h≤1) (_hi : 0≤i ∧ i≤1)
    (_hj : 0≤j ∧ j≤1) (_hk : 0≤k ∧ k≤1) (_hu : 0≤u ∧ u≤1)
    (tile1 : b+c+d+e≤2) (tile2 : f+g+h+i≤2) (tile3 : j+k≤1)
    (ad : a+d≤1) (bc : b+c≤1) (ce : c+e≤1)
    (freezeLeft : 1≤c+u) (uf : u+f≤1) (hei : h+e+i≤2)
    (jg : j+g≤1) (freezeRight : k=0) :
    a+b+c+d+e+f+g+h+i+j+k≤5 := by omega

def localWitness : List Point :=
  [(0,9),(1,10),(2,8),(2,11),(3,7),(3,9),(3,10),(4,12)]

/-- A physical five-point strip attainer, with both required selections
for the left witness and the forced selection for the right witness. -/
theorem actual_sharp_local_witness :
    localWitness.Nodup ∧
    (∀ v ∈ localWitness, v ∉ OpposedDirectionInterfaces.endpoints) ∧
    (∀ v ∈ localWitness,
      ((localWitness ++ OpposedDirectionInterfaces.endpoints).filter
        fun w => decide (adjacent v w)).length≤1) ∧
    (localWitness.filter fun v => decide (v.1=2 ∨ v.1=3)).length=5 ∧
    (∀ v ∈ ([(0,9),(1,10),(4,12)] : List Point), v ∈ localWitness) := by decide

/-- Replacing the four old tiles by their loss bound charges the strip
once, with all other disjoint cover members retained in the remainder. -/
theorem cover_loss (total strip rest t : Int)
    (partition : total=strip+rest) (localBound : strip≤5)
    (otherBound : rest≤2*t-6) : total≤2*t-1 := by omega

theorem unrestricted_count (q : Nat) (positive : 1≤q) :
    (70*(q*q)+26*q+3)+8*q=(70*(q*q)+26*q+4)+(8*q-1) := by
  omega

theorem removed_count (q : Nat) (positive : 1≤q) :
    5*q+2*q+(q-1)=8*q-1 := by omega

theorem frozen_count_gap (q : Nat) :
    (70*(q*q)+26*q+4)-(70*(q*q)+26*q+3)=1 := by omega

/-- Every grid q1 endpoint fact used to extract the two necessary freezing
conditions is checked directly against the existing actual matching. -/
theorem actual_endpoint_stencil :
    OpposedDirectionInterfaces.mate (1,9)=(1,8) ∧
    OpposedDirectionInterfaces.mate (4,13)=(5,13) ∧
    (1,9) ∈ OpposedDirectionInterfaces.endpoints ∧
    (4,13) ∈ OpposedDirectionInterfaces.endpoints ∧
    (3,13) ∈ OpposedDirectionInterfaces.endpoints ∧
    (5,14) ∈ OpposedDirectionInterfaces.endpoints ∧
    (∀ v ∈ ([(0,9),(1,10),(2,9),(4,12),(4,14)] : List Point),
      v ∉ OpposedDirectionInterfaces.endpoints) := by decide

def unrestrictedSelected : List Point := [(0, 1), (0, 2), (0, 4), (0, 6), (0, 8), (0, 10), (0, 12), (0, 14), (0, 15), (0, 17), (0, 19), (0, 21), (0, 23), (1, 0), (1, 11), (1, 13), (1, 16), (1, 18), (1, 20), (1, 22), (2, 0), (2, 2), (2, 8), (2, 10), (2, 12), (2, 15), (2, 17), (2, 19), (2, 23), (3, 1), (3, 3), (3, 7), (3, 9), (3, 11), (3, 14), (3, 16), (3, 18), (3, 20), (4, 0), (4, 2), (4, 8), (4, 10), (4, 12), (4, 15), (4, 17), (4, 19), (4, 23), (5, 1), (5, 3), (5, 7), (5, 9), (5, 11), (6, 0), (6, 2), (6, 8), (6, 10), (6, 12), (6, 23), (7, 0), (7, 2), (7, 7), (7, 9), (7, 11), (8, 1), (8, 3), (8, 8), (8, 10), (8, 12), (8, 15), (8, 17), (8, 20), (8, 23), (9, 0), (9, 11), (9, 13), (9, 16), (9, 18), (9, 19), (9, 22), (10, 0), (10, 2), (10, 10), (10, 12), (10, 15), (10, 17), (10, 20), (10, 23), (11, 1), (11, 3), (11, 5), (11, 7), (11, 9), (11, 11), (11, 13), (11, 14), (11, 16), (11, 18), (11, 19), (11, 21), (11, 22)]

/-- The unrestricted q1 maximum really has 100 feasible selections on the
same actual endpoint set; the submitted frozen witness has only 99. -/
theorem actual_unrestricted_geometry :
    unrestrictedSelected.Nodup ∧ unrestrictedSelected.length=100 ∧
    (∀ v ∈ unrestrictedSelected, v ∉ OpposedDirectionInterfaces.endpoints) ∧
    (∀ v ∈ unrestrictedSelected, v.1<12 ∧ v.2<24) ∧
    (∀ v ∈ unrestrictedSelected,
      ((unrestrictedSelected ++ OpposedDirectionInterfaces.endpoints).filter
        fun w => decide (adjacent v w)).length≤1) := by decide

theorem p_nonmate_enumeration (u : Point)
    (neighbour : OpposedDirectionInterfaces.nonmateAdjacent (1,9) u) :
    u=(0,9) ∨ u=(1,10) ∨ u=(2,9) := by
  have mateP := actual_endpoint_stencil.1
  rcases u with ⟨r,c⟩
  rcases neighbour with ⟨adj,ne⟩
  rw [mateP] at ne
  simp [adjacent,Prod.mk.injEq] at adj ne ⊢
  omega

theorem unrestricted_p_witnesses_empty :
    ∀ v ∈ ([(0,9),(1,10),(2,9)] : List Point),
      v ∉ unrestrictedSelected ∧ v ∉ OpposedDirectionInterfaces.endpoints := by decide

theorem actual_unrestricted_p_not_frozen :
    ¬ Frozen (fun v => v ∈ OpposedDirectionInterfaces.endpoints)
      (fun v => v ∈ unrestrictedSelected) OpposedDirectionInterfaces.mate
      OpposedDirectionInterfaces.nonmateAdjacent (1,9) := by
  intro f
  obtain ⟨a,b,ne,va,vb,oa,ob⟩ := frozen_two_occupied f
  have absent : a ∉ unrestrictedSelected ∧ a ∉ OpposedDirectionInterfaces.endpoints := by
    rcases p_nonmate_enumeration a va with same | same | same
    · subst a
      exact unrestricted_p_witnesses_empty (0,9) (by decide)
    · subst a
      exact unrestricted_p_witnesses_empty (1,10) (by decide)
    · subst a
      exact unrestricted_p_witnesses_empty (2,9) (by decide)
  exact oa.elim absent.1 absent.2

#print axioms frozen_two_occupied
#print axioms single_possible_witness_not_frozen
#print axioms local_packing_cut
#print axioms actual_sharp_local_witness
#print axioms cover_loss
#print axioms unrestricted_count
#print axioms removed_count
#print axioms frozen_count_gap
#print axioms actual_endpoint_stencil

#print axioms actual_unrestricted_geometry
#print axioms p_nonmate_enumeration
#print axioms unrestricted_p_witnesses_empty
#print axioms actual_unrestricted_p_not_frozen

end SubQuorum.FrozenInterfaceOptimality
