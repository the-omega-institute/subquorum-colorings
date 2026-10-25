import Lean.Elab.Tactic.Omega

set_option autoImplicit false
set_option maxRecDepth 4096

namespace SubQuorum.TwoSidedSeamRecourse

/-- Edge i connects sources i-1 and i. All sources are paid. Before the
first doubled edge p, two distinct sources cannot use the same edge. -/
theorem first_double_forces_right (k p : Nat) (hp : p<k) (f : Nat → Nat)
    (incident : ∀ a, a<k → f a=a ∨ f a=a+1)
    (positive : ∀ a, a<k → 1≤f a)
    (singleBefore : ∀ a b, a<k → b<k → f a=f b → f a<p → a=b) :
    ∀ a, a<p → f a=a+1 := by
  intro a
  induction a with
  | zero =>
    intro before
    have inc := incident 0 (by omega)
    have pos := positive 0 (by omega)
    omega
  | succ a ih =>
    intro before
    have prev := ih (by omega)
    have inc := incident (a+1) (by omega)
    cases inc with
    | inl same =>
      have collision := singleBefore a (a+1) (by omega) (by omega)
        (prev.trans same.symm) (by omega)
      omega
    | inr yes => exact yes

/-- Every previously paid source strictly between the old omitted boundary
and p must change ORIGINAL edge identity, independent of extra route cost. -/
theorem old_assignments_forced_to_change (k p : Nat) (hp : p<k) (f : Nat → Nat)
    (incident : ∀ a, a<k → f a=a ∨ f a=a+1)
    (positive : ∀ a, a<k → 1≤f a)
    (singleBefore : ∀ a b, a<k → b<k → f a=f b → f a<p → a=b)
    (a : Nat) (before : a<p) : f a≠a := by
  have forced := first_double_forces_right k p hp f incident positive singleBefore a before
  omega

def repairEdge (p a : Nat) : Nat := if a<p then a+1 else a

/-- Side1 is the new upper unit, used only by the source just left of p;
all other sources use original lower units, including source p itself. -/
def repairUnit (p a : Nat) : Nat × Nat :=
  (repairEdge p a, if a+1=p then 1 else 0)

theorem repair_edge_in_range (k p a : Nat) (hp : 1≤p) (pk : p<k) (ha : a<k) :
    1≤repairEdge p a ∧ repairEdge p a<k := by
  unfold repairEdge
  split <;> omega

theorem repair_edge_incident (p a : Nat) :
    repairEdge p a=a ∨ repairEdge p a=a+1 := by
  unfold repairEdge
  split
  · exact Or.inr rfl
  · exact Or.inl rfl

/-- No original unit is assigned twice, including the only edge collision:
sources p-1,p are separated by their original upper/lower unit identities. -/
theorem repair_units_injective (p a b : Nat) (same : repairUnit p a=repairUnit p b) : a=b := by
  have edge := congrArg Prod.fst same
  have side := congrArg Prod.snd same
  change repairEdge p a=repairEdge p b at edge
  change (if a+1=p then 1 else 0 : Nat)=(if b+1=p then 1 else 0) at side
  by_cases ha : a<p <;> by_cases hb : b<p
  · simp only [repairEdge,if_pos ha,if_pos hb] at edge
    omega
  · simp only [repairEdge,if_pos ha,if_neg hb] at edge
    have aa : a+1=p := by omega
    have bb : b+1≠p := by omega
    simp [aa,bb] at side
  · simp only [repairEdge,if_neg ha,if_pos hb] at edge
    have aa : a+1≠p := by omega
    have bb : b+1=p := by omega
    simp [aa,bb] at side
  · simpa only [repairEdge,if_neg ha,if_neg hb] using edge

theorem repair_uses_only_available_sides (p a : Nat) :
    (repairUnit p a).2=0 ∨ ((repairUnit p a).1=p ∧ (repairUnit p a).2=1) := by
  by_cases ha : a+1=p
  · right
    have before : a<p := by omega
    simp [repairUnit,repairEdge,ha,before]
  · left
    simp [repairUnit,ha]

theorem repair_retains_all_old_after_p (p a : Nat) (after : p≤a) :
    repairUnit p a=(a,0) := by
  have notBefore : ¬a<p := by omega
  have notUpper : a+1≠p := by omega
  simp [repairUnit,repairEdge,notBefore,notUpper]

theorem repair_changes_every_prefix_unit (p a : Nat) (before : a<p) :
    repairUnit p a≠(a,0) := by
  intro same
  have edge := congrArg Prod.fst same
  simp only [repairUnit,repairEdge,if_pos before] at edge
  omega

/-- A minimum-link old solution uses only one-link left assignments.
Source zero cannot belong to that old paid set. -/
theorem old_one_link_cannot_pay_zero (f : Nat → Nat)
    (oldAtZero : f 0=0) (validAtZero : 1≤f 0) : False := by omega

theorem cyclic_component_cost (size rightCount : Nat) (bound : rightCount≤size) :
    2*rightCount+(size-rightCount)=size+rightCount := by omega

theorem global_slack_deficit (k components cyclic doubles openings slack deficit : Int)
    (edgeCount : openings=k-components+doubles) (s : slack=2*k+openings)
    (d : deficit=components-cyclic) : slack+deficit=3*k+doubles-cyclic := by omega

theorem single_repair_cost_increment (k p : Int) : (k+p)-(k-1)=p+1 := by omega

/-- Once the forcing/finite-count adapter identifies p-1 changed old
sources, there is no uniform bound as the physical path length varies. -/
theorem unbounded_recourse_parameters (bound : Nat) :
    let k:=bound+3
    let p:=bound+2
    1≤p ∧ p<k ∧ bound<p-1 ∧ bound<(k+p)-(k-1) := by
  dsimp
  omega

abbrev Point := Nat × Nat
abbrev Original := Nat × Nat × Nat
def selected : List Point := [(0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 11), (0, 13), (0, 15), (0, 17), (0, 19), (0, 21), (0, 23), (0, 25), (0, 27), (0, 29), (0, 33), (0, 35), (0, 37), (0, 39), (0, 41), (1, 0), (1, 2), (1, 10), (1, 12), (1, 20), (1, 22), (1, 30), (1, 32), (1, 40), (2, 0), (2, 8), (2, 11), (2, 18), (2, 21), (2, 28), (2, 31), (2, 38), (2, 41), (3, 1), (3, 3), (3, 7), (3, 9), (3, 11), (3, 13), (3, 17), (3, 19), (3, 21), (3, 23), (3, 27), (3, 29), (3, 31), (3, 33), (3, 37), (3, 39), (3, 41), (4, 0), (4, 2), (4, 8), (4, 10), (4, 12), (4, 18), (4, 20), (4, 22), (4, 28), (4, 30), (4, 32), (4, 38), (4, 40), (5, 0), (5, 2), (5, 7), (5, 9), (5, 11), (5, 13), (5, 17), (5, 19), (5, 21), (5, 23), (5, 27), (5, 29), (5, 31), (5, 33), (5, 37), (5, 39), (5, 41), (6, 1), (6, 3), (6, 8), (6, 10), (6, 12), (6, 18), (6, 20), (6, 22), (6, 28), (6, 30), (6, 32), (6, 38), (6, 40), (7, 0), (7, 11), (7, 21), (7, 31), (7, 41), (8, 0), (8, 2), (8, 10), (8, 12), (8, 20), (8, 22), (8, 30), (8, 32), (8, 40), (9, 1), (9, 3), (9, 5), (9, 7), (9, 9), (9, 13), (9, 15), (9, 17), (9, 19), (9, 23), (9, 25), (9, 27), (9, 29), (9, 33), (9, 35), (9, 37), (9, 39), (9, 41)]
def matching : List (Point × Point) := [((1, 5), (2, 5)), ((3, 5), (4, 5)), ((5, 5), (6, 5)), ((7, 5), (8, 5)), ((2, 6), (3, 6)), ((4, 6), (5, 6)), ((6, 6), (7, 6)), ((1, 6), (1, 7)), ((1, 8), (1, 9)), ((8, 6), (8, 7)), ((8, 8), (8, 9)), ((7, 7), (7, 8)), ((1, 3), (1, 4)), ((2, 4), (3, 4)), ((8, 3), (8, 4)), ((7, 4), (6, 4)), ((4, 4), (5, 4)), ((1, 15), (2, 15)), ((3, 15), (4, 15)), ((5, 15), (6, 15)), ((7, 15), (8, 15)), ((2, 16), (3, 16)), ((4, 16), (5, 16)), ((6, 16), (7, 16)), ((1, 16), (1, 17)), ((1, 18), (1, 19)), ((8, 16), (8, 17)), ((8, 18), (8, 19)), ((7, 17), (7, 18)), ((1, 13), (1, 14)), ((2, 14), (3, 14)), ((8, 13), (8, 14)), ((7, 14), (6, 14)), ((4, 14), (5, 14)), ((1, 25), (2, 25)), ((3, 25), (4, 25)), ((5, 25), (6, 25)), ((7, 25), (8, 25)), ((2, 26), (3, 26)), ((4, 26), (5, 26)), ((6, 26), (7, 26)), ((1, 26), (1, 27)), ((1, 28), (1, 29)), ((8, 26), (8, 27)), ((8, 28), (8, 29)), ((7, 27), (7, 28)), ((1, 23), (1, 24)), ((2, 24), (3, 24)), ((8, 23), (8, 24)), ((7, 24), (6, 24)), ((4, 24), (5, 24)), ((1, 35), (2, 35)), ((3, 35), (4, 35)), ((5, 35), (6, 35)), ((7, 35), (8, 35)), ((2, 36), (3, 36)), ((4, 36), (5, 36)), ((6, 36), (7, 36)), ((1, 36), (1, 37)), ((1, 38), (1, 39)), ((8, 36), (8, 37)), ((8, 38), (8, 39)), ((7, 37), (7, 38)), ((1, 33), (1, 34)), ((2, 34), (3, 34)), ((8, 33), (8, 34)), ((7, 34), (6, 34)), ((4, 34), (5, 34))]
def roots : List Nat := [1, 5, 9, 13]
def reachable : List Nat := [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
def ownerLinks : List (Nat × Nat) := [(1, 0), (1, 2), (1, 20), (1, 21), (2, 3), (5, 4), (5, 6), (5, 23), (5, 24), (6, 7), (9, 8), (9, 10), (9, 26), (9, 27), (10, 11), (13, 12), (13, 14), (13, 29), (13, 30), (14, 15), (21, 22), (24, 25), (27, 28), (30, 31)]
def originalUnits : List Original := [(0, 31, 31), (1, 2, 2), (1, 10, 12), (1, 20, 22), (1, 30, 32), (3, 2, 2), (3, 9, 9), (3, 13, 13), (3, 19, 19), (3, 23, 23), (3, 29, 29), (3, 33, 33), (3, 39, 39), (4, 11, 11), (4, 21, 21), (4, 31, 31)]
def newUnits : List Original := [(0, 31, 31), (4, 11, 11), (4, 21, 21), (4, 31, 31)]
def actualSupports : List (Nat × List Original) := [(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, []), (10, []), (11, [(0, 31, 31)]), (12, [(0, 31, 31)]), (13, []), (14, []), (15, []), (16, [(3, 9, 9), (3, 13, 13)]), (17, [(3, 19, 19), (3, 23, 23)]), (18, [(3, 29, 29), (3, 33, 33)]), (19, [(3, 39, 39)]), (20, []), (21, []), (22, [(4, 11, 11)]), (23, [(4, 11, 11)]), (24, []), (25, [(4, 21, 21)]), (26, [(4, 21, 21)]), (27, []), (28, [(4, 31, 31)]), (29, [(4, 31, 31)]), (30, []), (31, [])]

theorem actual_repair_counts : selected.length=130 ∧ matching.length=68 ∧
    roots.length=4 ∧ originalUnits.length=16 ∧ newUnits.length=4 ∧
    134-4=130 ∧ 10*42/2-130-68=12 ∧ (4+3)-(4-1)=4 := by decide

theorem actual_repair_closed_table :
    (roots.all fun o => decide (o ∈ reachable))=true ∧
    (ownerLinks.all fun e => decide (e.1 ∉ reachable ∨ e.2 ∈ reachable))=true ∧
    ((actualSupports.filter fun row => decide (row.1 ∈ reachable)).all fun row =>
      row.2.all fun j => decide (j ∈ newUnits))=true ∧ newUnits.Nodup := by decide

#print axioms first_double_forces_right
#print axioms old_assignments_forced_to_change
#print axioms repair_edge_in_range
#print axioms repair_edge_incident
#print axioms repair_units_injective
#print axioms repair_uses_only_available_sides
#print axioms repair_retains_all_old_after_p
#print axioms repair_changes_every_prefix_unit
#print axioms old_one_link_cannot_pay_zero
#print axioms cyclic_component_cost
#print axioms global_slack_deficit
#print axioms single_repair_cost_increment
#print axioms unbounded_recourse_parameters
#print axioms actual_repair_counts
#print axioms actual_repair_closed_table

end SubQuorum.TwoSidedSeamRecourse
