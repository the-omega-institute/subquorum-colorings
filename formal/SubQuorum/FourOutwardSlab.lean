import SubQuorum.FrozenPromotion
import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace SubQuorum.FourOutwardSlab
abbrev Vertex := Nat × Nat
def selected : List Vertex := [(0,1),(0,6),(1,0),(1,7),(2,1),(2,6),(3,0),(3,7),(4,1),(4,6),(5,0),(5,2),(5,5),(5,7)]
def endpoints : List Vertex := [(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,2),(2,3),(2,4),(2,5),(3,2),(3,3),(3,4),(3,5),(4,2),(4,5)]
def matching : List (Vertex × Vertex) := [((0,2),(0,3)),((0,4),(0,5)),((1,3),(1,4)),((2,3),(2,4)),((1,2),(2,2)),((1,5),(2,5)),((3,3),(3,4)),((3,2),(4,2)),((3,5),(4,5))]
def mate (v : Vertex) : Vertex :=
  if v = (0,2) then (0,3) else
  if v = (0,3) then (0,2) else
  if v = (0,4) then (0,5) else
  if v = (0,5) then (0,4) else
  if v = (1,2) then (2,2) else
  if v = (1,3) then (1,4) else
  if v = (1,4) then (1,3) else
  if v = (1,5) then (2,5) else
  if v = (2,2) then (1,2) else
  if v = (2,3) then (2,4) else
  if v = (2,4) then (2,3) else
  if v = (2,5) then (1,5) else
  if v = (3,2) then (4,2) else
  if v = (3,3) then (3,4) else
  if v = (3,4) then (3,3) else
  if v = (3,5) then (4,5) else
  if v = (4,2) then (3,2) else
  if v = (4,5) then (3,5) else v

def vertices : List Vertex :=
  (List.range 6).flatMap fun r => (List.range 8).map fun c => (r,c)
def tiles : List Vertex :=
  (List.range 3).flatMap fun r => (List.range 4).map fun c => (r,c)
def tile (v : Vertex) : Vertex := (v.1/2,v.2/2)
def adjacent (a b : Vertex) : Prop :=
  (a.1=b.1 ∧ (a.2+1=b.2 ∨ b.2+1=a.2)) ∨
  (a.2=b.2 ∧ (a.1+1=b.1 ∨ b.1+1=a.1))
instance (a b : Vertex) : Decidable (adjacent a b) :=
  inferInstanceAs (Decidable ((_ ∧ _) ∨ (_ ∧ _)))
def degree (v : Vertex) : Nat :=
  (vertices.filter fun w => decide (adjacent v w) &&
    (selected.contains w || endpoints.contains w)).length
def tIn (q : Vertex) : Nat := (selected.filter fun v => tile v == q).length
def pIn (q : Vertex) : Nat := (endpoints.filter fun v => tile v == q).length
/-- There are no saturated endpoint tiles, so this is twice corrected charge. -/
def charge2 (q : Vertex) : Int := 2*(tIn q : Int)+(pIn q : Int)-4

theorem valid_matching : endpoints.Nodup ∧ selected.Nodup ∧
    (matching.flatMap fun e => [e.1,e.2]).Perm endpoints ∧
    (∀ e ∈ matching, adjacent e.1 e.2 ∧ mate e.1=e.2 ∧ mate e.2=e.1) ∧
    (∀ v ∈ endpoints, v ∈ vertices ∧ v ∉ selected) ∧
    (∀ v ∈ selected, v ∈ vertices) := by decide

theorem feasible_selected : ∀ v ∈ selected, degree v ≤ 1 := by decide
theorem endpoint_terminal : ∀ v ∈ endpoints, 3 ≤ degree v := by decide

theorem complete_tile_profiles : ∀ q ∈ tiles,
    ((q.2=0 ∨ q.2=3) ∧ tIn q=2 ∧ pIn q=0) ∨
    ((q.2=1 ∨ q.2=2) ∧ q.1<2 ∧ tIn q=0 ∧ pIn q=4) ∨
    ((q.2=1 ∨ q.2=2) ∧ q.1=2 ∧ tIn q=1 ∧ pIn q=1) := by decide

theorem no_saturated_endpoint_tile : ∀ v ∈ endpoints, tIn (tile v) < 2 := by decide

theorem two_four_outward_tiles : ∀ q ∈ [(1,1),(1,2)],
    tIn q=0 ∧ pIn q=4 ∧
    (∀ v ∈ endpoints, tile v=q → tile (mate v) ≠ q) := by decide

theorem complete_charge_table : ∀ q ∈ tiles,
    charge2 q = if q=(2,1) ∨ q=(2,2) then -1 else 0 := by decide

theorem exact_negative_capacity :
    (tiles.map fun q => max 0 (-charge2 q)).sum = 2 ∧
    (tiles.map charge2).sum = -2 := by decide

theorem exact_counts : selected.length=14 ∧ endpoints.length=18 ∧
    matching.length=9 ∧ selected.length+matching.length+1=6*8/2 := by decide

theorem all_frozen : ∀ v ∈ endpoints,
    FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate v := by
  have f0 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (4,2) :=
    .two_selected (4,2) (4,1) (5,2) (by decide) (by decide) (by decide) (by decide) (by decide)
  have f1 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (4,5) :=
    .two_selected (4,5) (4,6) (5,5) (by decide) (by decide) (by decide) (by decide) (by decide)
  have f2 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (2,2) :=
    .selected_frozen (2,2) (2,1) (3,2) (by decide) (by decide) (by decide) (by decide) (by simpa [mate] using f0)
  have f3 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (2,5) :=
    .selected_frozen (2,5) (2,6) (3,5) (by decide) (by decide) (by decide) (by decide) (by simpa [mate] using f1)
  have f4 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (0,2) :=
    .selected_frozen (0,2) (0,1) (1,2) (by decide) (by decide) (by decide) (by decide) (by simpa [mate] using f2)
  have f5 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (0,5) :=
    .selected_frozen (0,5) (0,6) (1,5) (by decide) (by decide) (by decide) (by decide) (by simpa [mate] using f3)
  have f6 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (1,3) :=
    .two_frozen (1,3) (0,3) (1,2) (by decide) (by decide) (by decide) (by simpa [mate] using f4) (by simpa [mate] using f2)
  have f7 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (1,4) :=
    .two_frozen (1,4) (0,4) (1,5) (by decide) (by decide) (by decide) (by simpa [mate] using f5) (by simpa [mate] using f3)
  have f8 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (0,3) :=
    .two_frozen (0,3) (0,4) (1,3) (by decide) (by decide) (by decide) (by simpa [mate] using f5) (by simpa [mate] using f7)
  have f9 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (0,4) :=
    .two_frozen (0,4) (0,3) (1,4) (by decide) (by decide) (by decide) (by simpa [mate] using f4) (by simpa [mate] using f6)
  have f10 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (1,2) :=
    .two_frozen (1,2) (0,2) (1,3) (by decide) (by decide) (by decide) (by simpa [mate] using f8) (by simpa [mate] using f7)
  have f11 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (1,5) :=
    .two_frozen (1,5) (0,5) (1,4) (by decide) (by decide) (by decide) (by simpa [mate] using f9) (by simpa [mate] using f6)
  have f12 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (2,3) :=
    .two_frozen (2,3) (1,3) (2,2) (by decide) (by decide) (by decide) (by simpa [mate] using f7) (by simpa [mate] using f10)
  have f13 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (2,4) :=
    .two_frozen (2,4) (1,4) (2,5) (by decide) (by decide) (by decide) (by simpa [mate] using f6) (by simpa [mate] using f11)
  have f14 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (3,3) :=
    .two_frozen (3,3) (2,3) (3,2) (by decide) (by decide) (by decide) (by simpa [mate] using f13) (by simpa [mate] using f0)
  have f15 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (3,4) :=
    .two_frozen (3,4) (2,4) (3,5) (by decide) (by decide) (by decide) (by simpa [mate] using f12) (by simpa [mate] using f1)
  have f16 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (3,2) :=
    .two_frozen (3,2) (2,2) (3,3) (by decide) (by decide) (by decide) (by simpa [mate] using f10) (by simpa [mate] using f15)
  have f17 : FrozenPromotion.Frozen adjacent (fun v => v ∈ selected) mate (3,5) :=
    .two_frozen (3,5) (2,5) (3,4) (by decide) (by decide) (by decide) (by simpa [mate] using f11) (by simpa [mate] using f14)
  intro v hv
  simp only [endpoints, List.mem_cons, List.not_mem_nil, or_false] at hv
  rcases hv with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact f4
  · exact f8
  · exact f9
  · exact f5
  · exact f10
  · exact f6
  · exact f7
  · exact f11
  · exact f2
  · exact f12
  · exact f13
  · exact f3
  · exact f16
  · exact f14
  · exact f15
  · exact f17
  · exact f0
  · exact f1

/-- Physical bundle exclusion: mate retention is required only on endpoints. -/
theorem no_feasible_promotion (promoted retained : Vertex → Prop)
    (keepT : ∀ v, v ∈ selected → retained v)
    (keepMate : ∀ v, v ∈ endpoints → ¬promoted (mate v) → retained v)
    (feasible : ∀ v a b, promoted v → adjacent v a → adjacent v b →
      retained a → retained b → a=b) :
    ∀ v ∈ endpoints, ¬promoted v := by
  have f0 : ¬promoted (4,2) := by
    intro hp
    exact (by decide : (4,1) ≠ (5,2)) (feasible (4,2) (4,1) (5,2) hp (by decide) (by decide)
      (keepT (4,1) (by decide)) (keepT (5,2) (by decide)))
  have f1 : ¬promoted (4,5) := by
    intro hp
    exact (by decide : (4,6) ≠ (5,5)) (feasible (4,5) (4,6) (5,5) hp (by decide) (by decide)
      (keepT (4,6) (by decide)) (keepT (5,5) (by decide)))
  have f2 : ¬promoted (2,2) := by
    intro hp
    exact (by decide : (2,1) ≠ (3,2)) (feasible (2,2) (2,1) (3,2) hp (by decide) (by decide)
      (keepT (2,1) (by decide)) (keepMate (3,2) (by decide) (by simpa [mate] using f0)))
  have f3 : ¬promoted (2,5) := by
    intro hp
    exact (by decide : (2,6) ≠ (3,5)) (feasible (2,5) (2,6) (3,5) hp (by decide) (by decide)
      (keepT (2,6) (by decide)) (keepMate (3,5) (by decide) (by simpa [mate] using f1)))
  have f4 : ¬promoted (0,2) := by
    intro hp
    exact (by decide : (0,1) ≠ (1,2)) (feasible (0,2) (0,1) (1,2) hp (by decide) (by decide)
      (keepT (0,1) (by decide)) (keepMate (1,2) (by decide) (by simpa [mate] using f2)))
  have f5 : ¬promoted (0,5) := by
    intro hp
    exact (by decide : (0,6) ≠ (1,5)) (feasible (0,5) (0,6) (1,5) hp (by decide) (by decide)
      (keepT (0,6) (by decide)) (keepMate (1,5) (by decide) (by simpa [mate] using f3)))
  have f6 : ¬promoted (1,3) := by
    intro hp
    exact (by decide : (0,3) ≠ (1,2)) (feasible (1,3) (0,3) (1,2) hp (by decide) (by decide)
      (keepMate (0,3) (by decide) (by simpa [mate] using f4)) (keepMate (1,2) (by decide) (by simpa [mate] using f2)))
  have f7 : ¬promoted (1,4) := by
    intro hp
    exact (by decide : (0,4) ≠ (1,5)) (feasible (1,4) (0,4) (1,5) hp (by decide) (by decide)
      (keepMate (0,4) (by decide) (by simpa [mate] using f5)) (keepMate (1,5) (by decide) (by simpa [mate] using f3)))
  have f8 : ¬promoted (0,3) := by
    intro hp
    exact (by decide : (0,4) ≠ (1,3)) (feasible (0,3) (0,4) (1,3) hp (by decide) (by decide)
      (keepMate (0,4) (by decide) (by simpa [mate] using f5)) (keepMate (1,3) (by decide) (by simpa [mate] using f7)))
  have f9 : ¬promoted (0,4) := by
    intro hp
    exact (by decide : (0,3) ≠ (1,4)) (feasible (0,4) (0,3) (1,4) hp (by decide) (by decide)
      (keepMate (0,3) (by decide) (by simpa [mate] using f4)) (keepMate (1,4) (by decide) (by simpa [mate] using f6)))
  have f10 : ¬promoted (1,2) := by
    intro hp
    exact (by decide : (0,2) ≠ (1,3)) (feasible (1,2) (0,2) (1,3) hp (by decide) (by decide)
      (keepMate (0,2) (by decide) (by simpa [mate] using f8)) (keepMate (1,3) (by decide) (by simpa [mate] using f7)))
  have f11 : ¬promoted (1,5) := by
    intro hp
    exact (by decide : (0,5) ≠ (1,4)) (feasible (1,5) (0,5) (1,4) hp (by decide) (by decide)
      (keepMate (0,5) (by decide) (by simpa [mate] using f9)) (keepMate (1,4) (by decide) (by simpa [mate] using f6)))
  have f12 : ¬promoted (2,3) := by
    intro hp
    exact (by decide : (1,3) ≠ (2,2)) (feasible (2,3) (1,3) (2,2) hp (by decide) (by decide)
      (keepMate (1,3) (by decide) (by simpa [mate] using f7)) (keepMate (2,2) (by decide) (by simpa [mate] using f10)))
  have f13 : ¬promoted (2,4) := by
    intro hp
    exact (by decide : (1,4) ≠ (2,5)) (feasible (2,4) (1,4) (2,5) hp (by decide) (by decide)
      (keepMate (1,4) (by decide) (by simpa [mate] using f6)) (keepMate (2,5) (by decide) (by simpa [mate] using f11)))
  have f14 : ¬promoted (3,3) := by
    intro hp
    exact (by decide : (2,3) ≠ (3,2)) (feasible (3,3) (2,3) (3,2) hp (by decide) (by decide)
      (keepMate (2,3) (by decide) (by simpa [mate] using f13)) (keepMate (3,2) (by decide) (by simpa [mate] using f0)))
  have f15 : ¬promoted (3,4) := by
    intro hp
    exact (by decide : (2,4) ≠ (3,5)) (feasible (3,4) (2,4) (3,5) hp (by decide) (by decide)
      (keepMate (2,4) (by decide) (by simpa [mate] using f12)) (keepMate (3,5) (by decide) (by simpa [mate] using f1)))
  have f16 : ¬promoted (3,2) := by
    intro hp
    exact (by decide : (2,2) ≠ (3,3)) (feasible (3,2) (2,2) (3,3) hp (by decide) (by decide)
      (keepMate (2,2) (by decide) (by simpa [mate] using f10)) (keepMate (3,3) (by decide) (by simpa [mate] using f15)))
  have f17 : ¬promoted (3,5) := by
    intro hp
    exact (by decide : (2,5) ≠ (3,4)) (feasible (3,5) (2,5) (3,4) hp (by decide) (by decide)
      (keepMate (2,5) (by decide) (by simpa [mate] using f11)) (keepMate (3,4) (by decide) (by simpa [mate] using f14)))
  intro v hv
  simp only [endpoints, List.mem_cons, List.not_mem_nil, or_false] at hv
  rcases hv with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact f4
  · exact f8
  · exact f9
  · exact f5
  · exact f10
  · exact f6
  · exact f7
  · exact f11
  · exact f2
  · exact f12
  · exact f13
  · exact f3
  · exact f16
  · exact f14
  · exact f15
  · exact f17
  · exact f0
  · exact f1

theorem general_count_consequences (h : Nat) (positive : 1≤h) :
    (4*h+10)+(4*h+5)+1=4*(2*h+4) ∧ 2≤2*h ∧ 1<2*(2*h) := by omega

theorem arbitrarily_many_centers (n : Nat) : ∃ h : Nat, 1≤h ∧ n≤2*h := by
  exact ⟨n+1, by omega, by omega⟩

end SubQuorum.FourOutwardSlab
#print axioms SubQuorum.FourOutwardSlab.valid_matching
#print axioms SubQuorum.FourOutwardSlab.feasible_selected
#print axioms SubQuorum.FourOutwardSlab.endpoint_terminal
#print axioms SubQuorum.FourOutwardSlab.complete_tile_profiles
#print axioms SubQuorum.FourOutwardSlab.no_saturated_endpoint_tile
#print axioms SubQuorum.FourOutwardSlab.two_four_outward_tiles
#print axioms SubQuorum.FourOutwardSlab.complete_charge_table
#print axioms SubQuorum.FourOutwardSlab.exact_negative_capacity
#print axioms SubQuorum.FourOutwardSlab.exact_counts
#print axioms SubQuorum.FourOutwardSlab.all_frozen
#print axioms SubQuorum.FourOutwardSlab.no_feasible_promotion
#print axioms SubQuorum.FourOutwardSlab.general_count_consequences
#print axioms SubQuorum.FourOutwardSlab.arbitrarily_many_centers
