import SubQuorum.FullPoolSingletonObstruction
import SubQuorum.ForcedMatesAdjacentMaxima

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

namespace SubQuorum.CrossingMatchingPorts
open SubQuorum.BTColumnCorridorObstruction (Frozen Point adjacent)
open SubQuorum.FullPoolSingletonObstruction (Reach reach_stays_closed)

/-- Count the missing actual-mate incidences as ports, retaining every P
vertex. The BB/TT resource adapter supplies q=bb-tt. -/
theorem local_port_ledger
    (area selected endpoints internal ports bb tt bt pp pt pb q a b x ct bc cc : Int)
    (areaCount : area=bb+tt+bt+pp+pt+pb)
    (selectedCount : selected=2*tt+bt+pt)
    (endpointCount : endpoints=2*pp+pt+pb)
    (cutCount : endpoints=2*internal+ports)
    (tTips : pt=2*a+x+ct) (bTips : pb=2*b+x+bc)
    (portCount : ports=ct+bc+2*cc) (resourceCount : q=bb-tt) :
    area-selected-internal=q+b-a+bc+cc := by omega

/-- Restoring the port matching has no extra resource credit: its exact
correction is the new beta-minus-alpha count. -/
theorem interface_correction (ct bc cc e a b x : Int)
    (tTips : ct=2*a+x) (bTips : bc=2*b+x)
    (ports : 2*e=ct+bc+2*cc) :
    bc+cc-e=b-a ∧ e=cc+a+b+x := by omega

theorem interface_alpha_bound (e cc a b x : Int)
    (count : e=cc+a+b+x) (hcc : 0≤cc) (hb : 0≤b) (hx : 0≤x) : a≤e := by omega

/-- A port-only cycle spends one CC incidence pair for every restored edge. -/
theorem port_cycle_zero (bc cc e a b x : Int)
    (count : e=cc+a+b+x) (noA : a=0) (noB : b=0) (noX : x=0)
    (noBHalf : bc=0) : bc+cc-e=0 := by omega

/-- The local-to-global body map is exact for a component with no port:
restoration cannot change any of its reachable vertices. -/
theorem closed_body_exact {V : Type} (edgeLocal edgeGlobal : V → V → Prop)
    (body : V → Prop) (root : V) (inside : body root)
    (stable : ∀ u v, body u → edgeGlobal u v → body v)
    (included : ∀ u v, edgeLocal u v → edgeGlobal u v)
    (spans : ∀ v, body v → Reach edgeLocal root v) :
    ∀ v, Reach edgeGlobal root v ↔ body v := by
  have lift (v : V) (path : Reach edgeLocal root v) : Reach edgeGlobal root v := by
    induction path with
    | root => exact Reach.root
    | step _ edge ih => exact Reach.step ih (included _ _ edge)
  intro v
  constructor
  · exact reach_stays_closed edgeGlobal body stable inside
  · intro bv
    exact lift v (spans v bv)

def combinedPayment {A B R : Type} (oldPay : A → R) (newPay : B → R) : Sum A B → R
  | .inl a => oldPay a
  | .inr b => newPay b

/-- One unused-reserve matching extends the old allocation only when both
internal injectivity and cross-disjointness are checked. -/
theorem reserve_extension_injective {A B R : Type} (oldPay : A → R) (newPay : B → R)
    (oldInj : ∀ a b, oldPay a=oldPay b → a=b)
    (newInj : ∀ a b, newPay a=newPay b → a=b)
    (unused : ∀ a b, oldPay a ≠ newPay b) :
    ∀ a b, combinedPayment oldPay newPay a=combinedPayment oldPay newPay b → a=b := by
  intro a b same
  cases a with
  | inl a =>
    cases b with
    | inl b => exact congrArg Sum.inl (oldInj a b same)
    | inr b => exact False.elim (unused a b same)
  | inr a =>
    cases b with
    | inl b => exact False.elim (unused b a same.symm)
    | inr b => exact congrArg Sum.inr (newInj a b same)

theorem retained_pack_deficit (ag al ai vg vl dg dl : Int)
    (alphaCount : ag=al+ai) (value : vl≤vg)
    (globalDeficit : dg=ag-vg) (localDeficit : dl=al-vl) : dg≤dl+ai := by omega

theorem unused_reserve_deficit (ag al ai vg vl nu dg dl : Int)
    (alphaCount : ag=al+ai) (value : vl+nu≤vg)
    (globalDeficit : dg=ag-vg) (localDeficit : dl=al-vl) : dg≤dl+ai-nu := by omega

theorem full_compensation (ag al ai vg vl nu : Int)
    (alphaCount : ag=al+ai) (localFull : vl=al) (allReserved : nu=ai)
    (constructed : vl+nu≤vg) (sourceBound : vg≤ag) : vg=ag := by omega

theorem sharp_cut_ledger (q : Nat) :
    (0 : Int)+3*(q:Int)-(q:Int)=2*(q:Int) := by omega

/-- Reuse the actual 34-endpoint freezing proof on the unchanged board. -/
theorem actual_all_endpoints_frozen :
    ∀ v ∈ ForcedMatesAdjacentMaxima.endpoints,
      Frozen (fun x => x ∈ ForcedMatesAdjacentMaxima.endpoints)
        (fun x => x ∈ ForcedMatesAdjacentMaxima.selected)
        ForcedMatesAdjacentMaxima.mate ForcedMatesAdjacentMaxima.nonmateAdjacent v :=
  ForcedMatesAdjacentMaxima.all_endpoints_frozen

def crossed : List (Point × Point) :=
  ForcedMatesAdjacentMaxima.matching.filter fun e =>
    decide ((e.1.1<2 ∧ 2≤e.2.1) ∨ (e.2.1<2 ∧ 2≤e.1.1))

theorem actual_cut_and_counts :
    crossed=[((1,5),(2,5))] ∧
    (ForcedMatesAdjacentMaxima.matching.filter fun e => decide (e.1.1<2 ∧ e.2.1<2)).length=3 ∧
    (ForcedMatesAdjacentMaxima.matching.filter fun e => decide (2≤e.1.1 ∧ 2≤e.2.1)).length=13 ∧
    ForcedMatesAdjacentMaxima.selected.length=41 ∧
    41+17+2=10*12/2 := by decide

/-- Top rectangle pairs columns; lower rectangle pairs rows. -/
def auxiliary (v : Point) : Point :=
  if v.1<2 then (v.1,if v.2%2=0 then v.2+1 else v.2-1)
  else (if v.1%2=0 then v.1+1 else v.1-1,v.2)

def alphaBody : List Point :=
  [(1,3),(1,4),(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5)]

/-- The cut actually lies in this closed, connected alternating TT path;
its top ordinary end moves from (1,5) to (1,3) under the mixed direction. -/
theorem actual_interface_alpha_path :
    alphaBody.Nodup ∧
    (∀ v ∈ alphaBody, v ∈ ForcedMatesAdjacentMaxima.endpoints) ∧
    (∀ v ∈ alphaBody,
      ForcedMatesAdjacentMaxima.mate v ∈ alphaBody ∧
      (auxiliary v ∈ ForcedMatesAdjacentMaxima.endpoints → auxiliary v ∈ alphaBody)) ∧
    (∀ e ∈ alphaBody.zip alphaBody.tail,
      ForcedMatesAdjacentMaxima.mate e.1=e.2 ∨ auxiliary e.1=e.2) ∧
    (alphaBody.filter fun v => decide (auxiliary v ∉ ForcedMatesAdjacentMaxima.endpoints))=[(1,3),(8,5)] ∧
    auxiliary (1,3) ∈ ForcedMatesAdjacentMaxima.selected ∧
    auxiliary (8,5) ∈ ForcedMatesAdjacentMaxima.selected := by decide

def ownerLinks : List (Nat × Nat) := [(0,2),(0,3),(1,1),(2,2),(3,3),(3,4),(4,4)]
def closedOwners : List Nat := [0,2,3,4]
def alphas : List Nat := [0]
def betas : List Nat := []
def raw : List (Nat × Nat × Nat) := [(6,2,2),(8,2,2),(8,9,9)]
def supports : List (Nat × List (Nat × Nat × Nat)) :=
  [(0,[]),(1,[(8,9,9)]),(2,[]),(3,[]),(4,[])]
def support (o : Nat) : List (Nat × Nat × Nat) :=
  ((supports.find? fun x => x.1==o).map Prod.snd).getD []
def ownerEdge (u v : Nat) : Prop := (u,v) ∈ ownerLinks
instance (u v : Nat) : Decidable (ownerEdge u v) := inferInstanceAs (Decidable (_ ∈ _))

theorem actual_zero_exit_certificate :
    (∀ a ∈ alphas, a ∈ closedOwners) ∧
    (∀ e ∈ ownerLinks, e.1 ∈ closedOwners → e.2 ∈ closedOwners) ∧
    (∀ o ∈ closedOwners, support o=[] ∧ o ∉ betas) ∧
    alphas.length=1 ∧ raw.length=3 := by decide

theorem actual_arbitrary_route_no_payment {a b : Nat} (start : a ∈ alphas)
    (route : Reach ownerEdge a b) : support b=[] ∧ b ∉ betas := by
  have inside := reach_stays_closed ownerEdge (fun o => o ∈ closedOwners)
    (fun u v hu edge => actual_zero_exit_certificate.2.1 (u,v) edge hu)
    (actual_zero_exit_certificate.1 a start) route
  exact actual_zero_exit_certificate.2.2.1 b inside

#print axioms local_port_ledger
#print axioms interface_correction
#print axioms interface_alpha_bound
#print axioms port_cycle_zero
#print axioms closed_body_exact
#print axioms reserve_extension_injective
#print axioms retained_pack_deficit
#print axioms unused_reserve_deficit
#print axioms full_compensation
#print axioms sharp_cut_ledger
#print axioms actual_all_endpoints_frozen
#print axioms actual_cut_and_counts
#print axioms actual_interface_alpha_path
#print axioms actual_zero_exit_certificate
#print axioms actual_arbitrary_route_no_payment

end SubQuorum.CrossingMatchingPorts
