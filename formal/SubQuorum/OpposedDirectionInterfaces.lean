import SubQuorum.FullPoolSingletonObstruction

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

namespace SubQuorum.OpposedDirectionInterfaces
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)
open SubQuorum.FullPoolSingletonObstruction (Reach reach_stays_closed)

/-- Every-length routes remain unpayable when a closed owner set contains
neither an interval exit nor a beta exit. The geometry supplies the closure. -/
theorem closed_route_no_exit {O : Type} (edge : O → O → Prop)
    (closed payable : O → Prop)
    (stable : ∀ u v, closed u → edge u v → closed v)
    (noExit : ∀ u, closed u → ¬ payable u)
    {a b : O} (start : closed a) (route : Reach edge a b) : ¬ payable b := by
  exact noExit b (reach_stays_closed edge closed stable start route)

def taggedPayment {I A R : Type} (pay : I → A → R) (x : I × A) : I × R :=
  (x.1,pay x.1 x.2)

theorem region_payments_injective {I A R : Type} (pay : I → A → R)
    (localInjective : ∀ i a b, pay i a=pay i b → a=b) :
    ∀ x y, taggedPayment pay x=taggedPayment pay y → x=y := by
  intro ⟨i,a⟩ ⟨j,b⟩ same
  have regions : i=j := congrArg Prod.fst same
  subst j
  have values : pay i a=pay i b := congrArg Prod.snd same
  have ab := localInjective i a b values
  subst b
  rfl

theorem partition_ledger (regions : List (Int × Int × Int)) :
    (regions.map (fun p => p.1-p.2.1-p.2.2)).sum =
      (regions.map (fun p => p.1)).sum -
      (regions.map (fun p => p.2.1)).sum -
      (regions.map (fun p => p.2.2)).sum := by
  induction regions with
  | nil => rfl
  | cons p ps ih =>
    simp only [List.map_cons,List.sum_cons]
    rw [ih]
    omega

theorem square_area (q : Nat) :
    (10*q+2)*(10*q+2)=100*(q*q)+40*q+4 := by
  simp only [Nat.add_mul,Nat.mul_add,Nat.mul_assoc]
  rw [Nat.mul_left_comm q 10 q]
  omega

theorem opposed_ledger (q : Nat) :
    (70*(q*q)+26*q+3)+(30*(q*q)+10*q)+(4*q+1)=(10*q+2)*(10*q+2) := by
  rw [square_area]
  omega

def selected : List Point := [(0,1), (0,3), (0,5), (0,7), (0,9), (0,11), (0,12), (0,14), (0,15), (0,17), (0,19), (0,21), (0,23), (1,0), (1,2), (1,10), (1,13), (1,16), (1,18), (1,20), (1,22), (2,0), (2,8), (2,12), (2,15), (2,17), (2,19), (2,23), (3,1), (3,3), (3,7), (3,9), (3,11), (3,14), (3,16), (3,18), (3,20), (4,0), (4,2), (4,8), (4,10), (4,12), (4,15), (4,17), (4,19), (4,23), (5,1), (5,3), (5,7), (5,9), (5,11), (6,0), (6,2), (6,8), (6,10), (6,12), (6,23), (7,0), (7,2), (7,7), (7,9), (7,11), (8,1), (8,3), (8,8), (8,10), (8,12), (8,15), (8,17), (8,20), (8,23), (9,0), (9,11), (9,13), (9,16), (9,18), (9,19), (9,22), (10,0), (10,2), (10,10), (10,12), (10,15), (10,17), (10,20), (10,23), (11,1), (11,3), (11,5), (11,7), (11,9), (11,11), (11,13), (11,14), (11,16), (11,18), (11,19), (11,21), (11,22)]
def matching : List (Point × Point) := [((1,5),(2,5)), ((3,5),(4,5)), ((5,5),(6,5)), ((7,5),(8,5)), ((9,5),(10,5)), ((2,6),(3,6)), ((4,6),(5,6)), ((6,6),(7,6)), ((8,6),(9,6)), ((1,6),(1,7)), ((1,8),(1,9)), ((10,6),(10,7)), ((10,8),(10,9)), ((9,7),(9,8)), ((1,3),(1,4)), ((2,4),(3,4)), ((10,3),(10,4)), ((9,4),(8,4)), ((4,4),(5,4)), ((6,4),(7,4)), ((6,13),(6,14)), ((6,15),(6,16)), ((6,17),(6,18)), ((6,19),(6,20)), ((6,21),(6,22)), ((5,14),(5,15)), ((5,16),(5,17)), ((5,18),(5,19)), ((5,20),(5,21)), ((5,13),(4,13)), ((3,13),(2,13)), ((5,22),(4,22)), ((3,22),(2,22)), ((4,21),(3,21)), ((8,13),(7,13)), ((7,14),(7,15)), ((8,22),(7,22)), ((7,21),(7,20)), ((7,16),(7,17)), ((7,18),(7,19))]
def endpoints : List Point := matching.flatMap fun e => [e.1,e.2]
def mate (v : Point) : Point := BTColumnCorridorObstruction.lookupMate v matching
def nonmateAdjacent (v w : Point) : Prop := adjacent v w ∧ w ≠ mate v
instance (v w : Point) : Decidable (nonmateAdjacent v w) := inferInstanceAs (Decidable (_ ∧ _))
def witnesses : List BTColumnCorridorObstruction.Witness := [
  ⟨(1,3), 0, (0,3), (1,2)⟩,
  ⟨(1,4), 32, (1,5), (2,4)⟩,
  ⟨(1,5), 2, (0,5), (1,4)⟩,
  ⟨(1,6), 25, (1,5), (2,6)⟩,
  ⟨(1,7), 6, (0,7), (1,8)⟩,
  ⟨(1,8), 26, (1,7), (2,8)⟩,
  ⟨(1,9), 3, (0,9), (1,10)⟩,
  ⟨(2,4), 30, (1,4), (2,5)⟩,
  ⟨(2,5), 24, (2,6), (3,5)⟩,
  ⟨(2,6), 10, (1,6), (2,5)⟩,
  ⟨(2,13), 43, (1,13), (2,12)⟩,
  ⟨(2,22), 45, (1,22), (2,23)⟩,
  ⟨(3,4), 31, (3,3), (3,5)⟩,
  ⟨(3,5), 11, (2,5), (3,6)⟩,
  ⟨(3,6), 23, (3,5), (3,7)⟩,
  ⟨(3,13), 66, (3,14), (4,13)⟩,
  ⟨(3,21), 48, (3,20), (3,22)⟩,
  ⟨(3,22), 69, (3,21), (4,22)⟩,
  ⟨(4,4), 34, (3,4), (4,5)⟩,
  ⟨(4,5), 22, (4,6), (5,5)⟩,
  ⟨(4,6), 12, (3,6), (4,5)⟩,
  ⟨(4,13), 46, (3,13), (4,12)⟩,
  ⟨(4,21), 68, (4,22), (5,21)⟩,
  ⟨(4,22), 47, (3,22), (4,23)⟩,
  ⟨(5,4), 37, (5,3), (5,5)⟩,
  ⟨(5,5), 13, (4,5), (5,6)⟩,
  ⟨(5,6), 21, (5,5), (5,7)⟩,
  ⟨(5,13), 65, (5,14), (6,13)⟩,
  ⟨(5,14), 50, (5,13), (6,14)⟩,
  ⟨(5,15), 63, (4,15), (5,16)⟩,
  ⟨(5,16), 52, (5,15), (6,16)⟩,
  ⟨(5,17), 61, (4,17), (5,18)⟩,
  ⟨(5,18), 54, (5,17), (6,18)⟩,
  ⟨(5,19), 59, (4,19), (5,20)⟩,
  ⟨(5,20), 56, (5,19), (6,20)⟩,
  ⟨(5,21), 49, (4,21), (5,22)⟩,
  ⟨(5,22), 67, (5,21), (6,22)⟩,
  ⟨(6,4), 35, (5,4), (6,5)⟩,
  ⟨(6,5), 20, (6,6), (7,5)⟩,
  ⟨(6,6), 14, (5,6), (6,5)⟩,
  ⟨(6,13), 42, (6,12), (7,13)⟩,
  ⟨(6,14), 64, (5,14), (6,15)⟩,
  ⟨(6,15), 51, (5,15), (6,14)⟩,
  ⟨(6,16), 62, (5,16), (6,17)⟩,
  ⟨(6,17), 53, (5,17), (6,16)⟩,
  ⟨(6,18), 60, (5,18), (6,19)⟩,
  ⟨(6,19), 55, (5,19), (6,18)⟩,
  ⟨(6,20), 58, (5,20), (6,21)⟩,
  ⟨(6,21), 57, (5,21), (6,20)⟩,
  ⟨(6,22), 44, (6,23), (7,22)⟩,
  ⟨(7,4), 36, (7,5), (8,4)⟩,
  ⟨(7,5), 15, (6,5), (7,6)⟩,
  ⟨(7,6), 19, (7,5), (7,7)⟩,
  ⟨(7,13), 72, (6,13), (7,14)⟩,
  ⟨(7,14), 70, (6,14), (7,13)⟩,
  ⟨(7,15), 71, (6,15), (8,15)⟩,
  ⟨(7,16), 74, (6,16), (7,15)⟩,
  ⟨(7,17), 77, (6,17), (7,18)⟩,
  ⟨(7,18), 75, (6,18), (7,17)⟩,
  ⟨(7,19), 76, (6,19), (7,20)⟩,
  ⟨(7,20), 78, (6,20), (7,19)⟩,
  ⟨(7,21), 73, (6,21), (7,22)⟩,
  ⟨(7,22), 79, (6,22), (7,21)⟩,
  ⟨(8,4), 38, (7,4), (8,3)⟩,
  ⟨(8,5), 18, (8,6), (9,5)⟩,
  ⟨(8,6), 16, (7,6), (8,5)⟩,
  ⟨(8,13), 40, (8,12), (9,13)⟩,
  ⟨(8,22), 41, (8,23), (9,22)⟩,
  ⟨(9,4), 33, (9,5), (10,4)⟩,
  ⟨(9,5), 17, (8,5), (9,6)⟩,
  ⟨(9,6), 9, (9,5), (9,7)⟩,
  ⟨(9,7), 28, (9,6), (10,7)⟩,
  ⟨(9,8), 8, (8,8), (10,8)⟩,
  ⟨(10,3), 1, (10,2), (11,3)⟩,
  ⟨(10,4), 39, (9,4), (10,5)⟩,
  ⟨(10,5), 4, (10,4), (11,5)⟩,
  ⟨(10,6), 27, (9,6), (10,5)⟩,
  ⟨(10,7), 7, (10,8), (11,7)⟩,
  ⟨(10,8), 29, (9,8), (10,7)⟩,
  ⟨(10,9), 5, (10,10), (11,9)⟩]
def record (v : Point) : BTColumnCorridorObstruction.Witness :=
  (witnesses.find? fun w => w.point == v).getD default
def rank (v : Point) : Nat := (record v).rank
def validAt (v : Point) : Prop :=
  let a := (record v).left
  let b := (record v).right
  a ≠ b ∧ nonmateAdjacent v a ∧ nonmateAdjacent v b ∧
    (a ∈ selected ∨ (a ∈ endpoints ∧ rank (mate a) < rank v)) ∧
    (b ∈ selected ∨ (b ∈ endpoints ∧ rank (mate b) < rank v))
instance (v : Point) : Decidable (validAt v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ (_ ∨ (_ ∧ _)) ∧ (_ ∨ (_ ∧ _))))

theorem geometry_valid :
    selected.Nodup ∧ endpoints.Nodup ∧
    (∀ e ∈ matching, adjacent e.1 e.2) ∧
    (∀ v ∈ endpoints, v ∉ selected) ∧
    (∀ v ∈ selected ++ endpoints, v.1<12 ∧ v.2<24) ∧
    (∀ v ∈ selected,
      ((selected ++ endpoints).filter fun w => decide (adjacent v w)).length ≤ 1) := by decide

theorem mate_closed : ∀ v ∈ endpoints, mate v ∈ endpoints := by decide
theorem certificate_valid : ∀ v ∈ endpoints, validAt v := by decide

theorem all_endpoints_frozen : ∀ v ∈ endpoints,
    Frozen (fun x => x ∈ endpoints) (fun x => x ∈ selected) mate nonmateAdjacent v := by
  apply BTColumnCorridorObstruction.strict_rank_complete (fun x => x ∈ endpoints)
    (fun x => x ∈ selected) mate nonmateAdjacent rank mate_closed
  intro v pv
  exact ⟨(record v).left,(record v).right,certificate_valid v pv⟩

def hLinks : List (Nat × Nat) := [(0,0), (1,0), (1,2), (1,10), (1,11), (2,2), (2,3), (3,3), (5,5), (5,6), (6,6), (6,7), (7,4), (7,7), (9,9), (10,10), (11,11), (11,12), (12,12)]
def hAlphas : List Nat := [1, 8]
def hBetas : List Nat := [4]
def hFailed : List Nat := [1]
def hClosed : List Nat := [0, 1, 2, 3, 10, 11, 12]
def hRaw : List (Nat × Nat × Nat) := [(1,2,2), (1,10,10), (4,2,2), (4,9,9), (4,14,14), (4,21,21)]
def hSupports : List (Nat × List (Nat × Nat × Nat)) := [(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, [(4,9,9), (4,14,14), (4,21,21)]), (9, [(4,9,9)]), (10, []), (11, []), (12, [])]
def hSupport (o : Nat) : List (Nat × Nat × Nat) :=
  ((hSupports.find? fun e => e.1 == o).map Prod.snd).getD []
def hEdge (u v : Nat) : Prop := (u,v) ∈ hLinks
instance (u v : Nat) : Decidable (hEdge u v) := inferInstanceAs (Decidable (_ ∈ _))

theorem h_closure_certificate :
    (∀ a ∈ hFailed, a ∈ hClosed) ∧
    (∀ e ∈ hLinks, e.1 ∈ hClosed → e.2 ∈ hClosed) ∧
    (∀ o ∈ hClosed, o ∉ hBetas ∧ hSupport o=[]) := by decide

theorem h_arbitrary_route_exclusion {a b : Nat} (start : a ∈ hFailed)
    (route : Reach hEdge a b) : b ∉ hBetas ∧ hSupport b=[] := by
  have inside : b ∈ hClosed :=
    reach_stays_closed hEdge (fun o => o ∈ hClosed)
      (fun u v hu edge => h_closure_certificate.2.1 (u,v) edge hu)
      (h_closure_certificate.1 a start) route
  exact h_closure_certificate.2.2 b inside

theorem h_direct_payment_witness :
    hAlphas.length=2 ∧ hFailed.length=1 ∧
    8 ∈ hAlphas ∧ (4,14,14) ∈ hSupport 8 ∧ (4,14,14) ∈ hRaw := by decide

def vLinks : List (Nat × Nat) := [(1,1), (1,2), (2,2), (2,3), (3,3), (3,4), (5,5), (6,5), (6,6), (7,6), (7,8), (7,11), (7,12), (8,8), (9,9), (10,10), (11,10), (11,11), (12,12)]
def vAlphas : List Nat := [0, 7]
def vBetas : List Nat := [4]
def vFailed : List Nat := [7]
def vClosed : List Nat := [5, 6, 7, 8, 10, 11, 12]
def vRaw : List (Nat × Nat × Nat) := [(1,2,2), (1,9,9), (5,2,2), (7,9,9), (10,2,2), (10,9,9)]
def vSupports : List (Nat × List (Nat × Nat × Nat)) := [(0, [(1,2,2), (1,9,9)]), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [(10,2,2)]), (10, []), (11, []), (12, [])]
def vSupport (o : Nat) : List (Nat × Nat × Nat) :=
  ((vSupports.find? fun e => e.1 == o).map Prod.snd).getD []
def vEdge (u v : Nat) : Prop := (u,v) ∈ vLinks
instance (u v : Nat) : Decidable (vEdge u v) := inferInstanceAs (Decidable (_ ∈ _))

theorem v_closure_certificate :
    (∀ a ∈ vFailed, a ∈ vClosed) ∧
    (∀ e ∈ vLinks, e.1 ∈ vClosed → e.2 ∈ vClosed) ∧
    (∀ o ∈ vClosed, o ∉ vBetas ∧ vSupport o=[]) := by decide

theorem v_arbitrary_route_exclusion {a b : Nat} (start : a ∈ vFailed)
    (route : Reach vEdge a b) : b ∉ vBetas ∧ vSupport b=[] := by
  have inside : b ∈ vClosed :=
    reach_stays_closed vEdge (fun o => o ∈ vClosed)
      (fun u v hu edge => v_closure_certificate.2.1 (u,v) edge hu)
      (v_closure_certificate.1 a start) route
  exact v_closure_certificate.2.2 b inside

theorem v_direct_payment_witness :
    vAlphas.length=2 ∧ vFailed.length=1 ∧
    0 ∈ vAlphas ∧ (1,2,2) ∈ vSupport 0 ∧ (1,2,2) ∈ vRaw := by decide

theorem piecewise_physical_payments :
    (2,2) ∉ selected ++ endpoints ∧ (2,3) ∉ selected ++ endpoints ∧
    (8,14) ∉ selected ++ endpoints ∧ (9,14) ∉ selected ++ endpoints ∧
    ([(2,2),(2,3),(8,14),(9,14)] : List Point).Nodup := by decide

theorem actual_counts_and_slack :
    selected.length=99 ∧ matching.length=40 ∧ endpoints.length=80 ∧
    99+40+5=12*24/2 := by decide

#print axioms closed_route_no_exit
#print axioms region_payments_injective
#print axioms partition_ledger
#print axioms square_area
#print axioms opposed_ledger
#print axioms geometry_valid
#print axioms mate_closed
#print axioms certificate_valid
#print axioms all_endpoints_frozen
#print axioms h_closure_certificate
#print axioms h_arbitrary_route_exclusion
#print axioms h_direct_payment_witness
#print axioms v_closure_certificate
#print axioms v_arbitrary_route_exclusion
#print axioms v_direct_payment_witness
#print axioms piecewise_physical_payments
#print axioms actual_counts_and_slack

end SubQuorum.OpposedDirectionInterfaces
