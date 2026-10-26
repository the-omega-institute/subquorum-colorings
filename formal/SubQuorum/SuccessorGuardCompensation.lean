import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.SuccessorGuardCompensation

def sum13 (f : Nat → Nat) : Nat :=
  f 0+f 1+f 2+f 3+f 4+f 5+f 6+f 7+f 8+f 9+f 10+f 11+f 12

/-- d,u,g,b,v,a,x,f,l,s,r,z,R. -/
def gfLHS (t o : Nat → Nat) : Nat :=
  3*(t 2+o 0)+3*(t 4+o 1)+2*(t 7+o 6)+(t 7+o 11)+
  (t 3+o 2+o 4)+2*(t 3+o 2+o 5)+2*(t 5+o 3+o 6)+
  (t 5+o 3+o 9)+2*(t 6+o 4+o 10)+(t 9+o 5+o 8)+
  2*(t 9+o 8+o 10)+2*(t 10+o 9+o 11)+3*(t 11+o 7+o 12)+
  3*(t 0+t 8+t 12)+3*t 1

theorem gf_identity (t o : Nat → Nat) :
    gfLHS t o+t 6+t 10=3*(sum13 t+sum13 o)+o 6+o 10 := by
  simp only [gfLHS,sum13]
  omega

theorem gf_bound (t o : Nat → Nat)
    (a0 : t 2+o 0 ≤ 1) (a1 : t 4+o 1 ≤ 1)
    (a2 : t 7+o 6 ≤ 1) (a3 : t 7+o 11 ≤ 1)
    (w0 : t 3+o 2+o 4 ≤ 2) (w1 : t 3+o 2+o 5 ≤ 2)
    (w2 : t 5+o 3+o 6 ≤ 2) (w3 : t 5+o 3+o 9 ≤ 2)
    (w4 : t 6+o 4+o 10 ≤ 2) (w5 : t 9+o 5+o 8 ≤ 2)
    (w6 : t 9+o 8+o 10 ≤ 2) (w7 : t 10+o 9+o 11 ≤ 2)
    (w8 : t 11+o 7+o 12 ≤ 2)
    (td : t 0 ≤ 1) (tl : t 8 ≤ 1) (tR : t 12 ≤ 1) (tu : t 1=0)
    (sx : t 6 ≤ o 6) (sr : t 10 ≤ o 10) :
    sum13 t+sum13 o ≤ 16 := by
  have identity := gf_identity t o
  have bound : gfLHS t o ≤ 50 := by unfold gfLHS; omega
  omega

def sum10 (f : Nat → Nat) : Nat :=
  f 0+f 1+f 2+f 3+f 4+f 5+f 6+f 7+f 8+f 9

/-- u,v,a,x,f,l,s,r,z,R. -/
def fLHS (t o : Nat → Nat) : Nat :=
  t 0+o 1+(t 1+o 0)+(t 3+o 2+o 7)+(t 4+o 8)+t 5+
  (t 6+o 2+o 5)+(t 7+o 3+o 6)+(t 8+o 4+o 9)+t 9

theorem f_identity (t o : Nat → Nat) :
    fLHS t o+t 2=sum10 t+sum10 o+o 2 := by
  simp only [fLHS,sum10]
  omega

theorem f_occupation_bound (t o : Nat → Nat)
    (tu : t 0=0) (ov : o 1 ≤ 1) (av : t 1+o 0 ≤ 1)
    (wx : t 3+o 2+o 7 ≤ 2) (af : t 4+o 8 ≤ 1)
    (tl : t 5 ≤ 1) (ws : t 6+o 2+o 5 ≤ 2)
    (wr : t 7+o 3+o 6 ≤ 2) (wz : t 8+o 4+o 9 ≤ 2)
    (tR : t 9 ≤ 1) (sa : t 2 ≤ o 2) : sum10 t+sum10 o ≤ 13 := by
  have identity := f_identity t o
  have bound : fLHS t o ≤ 13 := by unfold fLHS; omega
  omega

theorem f_equality_data (t o : Nat → Nat)
    (tu : t 0=0) (ov : o 1 ≤ 1) (av : t 1+o 0 ≤ 1)
    (wx : t 3+o 2+o 7 ≤ 2) (af : t 4+o 8 ≤ 1)
    (tl : t 5 ≤ 1) (ws : t 6+o 2+o 5 ≤ 2)
    (wr : t 7+o 3+o 6 ≤ 2) (wz : t 8+o 4+o 9 ≤ 2)
    (tR : t 9 ≤ 1) (subset : ∀ i, t i ≤ o i) (bounded : ∀ i, o i ≤ 1)
    (ws' : t 6+o 5+o 7 ≤ 2) (wa : t 2+o 3+o 6 ≤ 2)
    (af' : t 4+o 3 ≤ 1) (wr' : t 7+o 3+o 8 ≤ 2)
    (eq : sum10 t+sum10 o=13) :
    t 2=1 ∧ t 5=1 ∧ t 7=1 ∧ o 6=1 := by
  have identity := f_identity t o
  unfold fLHS at identity
  have s2 := subset 2
  have tight : t 5=1 ∧ t 9=1 ∧ t 2=o 2 ∧ t 3+o 2+o 7=2 ∧
      t 4+o 8=1 ∧ t 6+o 2+o 5=2 ∧ t 7+o 3+o 6=2 := by omega
  obtain ⟨el,eR,sa,ex,ef,es,er⟩ := tight
  have s5 := subset 5; have b5 := bounded 5
  have ol : o 5=1 := by omega
  have zero : t 6=0 := by
    by_cases pos : t 6=0
    · exact pos
    · have b2 := bounded 2
      have b3 := bounded 3; have s3 := subset 3
      omega
  have ea : t 2=1 := by omega
  have osum : o 3+o 6 ≤ 1 := by omega
  have br := bounded 7; have sr := subset 7
  have tr : t 7=1 := by omega
  have centre : o 6=1 := by
    have bs := bounded 6
    by_cases occupied : o 6=1
    · exact occupied
    · omega
  exact ⟨ea,el,tr,centre⟩

theorem f_matching_bound (t o p : Nat → Nat)
    (tu : t 0=0) (ov : o 1 ≤ 1) (av : t 1+o 0 ≤ 1)
    (wx : t 3+o 2+o 7 ≤ 2) (af : t 4+o 8 ≤ 1)
    (tl : t 5 ≤ 1) (ws : t 6+o 2+o 5 ≤ 2)
    (wr : t 7+o 3+o 6 ≤ 2) (wz : t 8+o 4+o 9 ≤ 2)
    (tR : t 9 ≤ 1) (subset : ∀ i, t i ≤ o i) (bounded : ∀ i, o i ≤ 1)
    (ws' : t 6+o 5+o 7 ≤ 2) (wa : t 2+o 3+o 6 ≤ 2)
    (af' : t 4+o 3 ≤ 1) (wr' : t 7+o 3+o 8 ≤ 2)
    (occupation : ∀ i, o i=t i+p i)
    (mateCoverage : p 6 ≤ p 2+p 5+p 7) : sum10 t+sum10 o ≤ 12 := by
  have upper := f_occupation_bound t o tu ov av wx af tl ws wr wz tR (subset 2)
  by_cases bound : sum10 t+sum10 o ≤ 12
  · exact bound
  · have eq : sum10 t+sum10 o=13 := by omega
    obtain ⟨ea,el,er,es⟩ := f_equality_data t o tu ov av wx af tl ws wr wz tR
      subset bounded ws' wa af' wr' eq
    have oa := occupation 2; have ol := occupation 5
    have or' := occupation 7; have os := occupation 6
    have ba := bounded 2; have bl := bounded 5; have br := bounded 7
    omega

theorem successor_isolate_injective (i j : Nat) (eq : 9+6*i+4=9+6*j+4) : i=j := by
  omega

theorem successor_component_sum (k n0 ng nf nb g f extra : Nat)
    (partition : n0+ng+nf+nb+1=k) (gcount : g=ng+nb) (fcount : f=nf+nb)
    (capacity : extra ≤ 19+10*n0+14*ng+12*nf+16*nb+4) :
    extra ≤ 10*k+13+4*g+2*f := by omega

theorem successor_permissions_cancel (k g f extra total : Nat)
    (capacity : extra ≤ 10*k+13+4*g+2*f)
    (retained : 2*total+2*g+2*f=24*k+12+extra) : total ≤ 17*k+12+g := by omega

theorem successor_margin (k g total : Nat) (valid : g ≤ k)
    (bound : total ≤ 17*k+12+g) : total+(k-g) ≤ 18*k+12 := by omega

abbrev Site := Nat × Nat
def phaseSites : List Site :=
  [(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
   (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]
def t36 : Site → Nat
  | (2,3) => 36 | (3,4) => 24
  | (4,0) => 12 | (4,1) => 18 | (4,2) => 12 | (4,3) => 23 | (4,4) => 12 | (4,5) => 21
  | (5,0) => 24 | (5,1) => 18 | (5,2) => 24 | (5,3) => 18 | (5,4) => 24 | (5,5) => 18
  | _ => 0
def o36 : Site → Nat
  | (2,3) => 36 | (2,5) => 36 | (3,3) => 21 | (3,4) => 36 | (3,5) => 27
  | (4,0) => 18 | (4,1) => 24 | (4,2) => 18 | (4,3) => 24 | (4,4) => 12 | (4,5) => 24
  | (5,0) => 24 | (5,1) => 18 | (5,2) => 24 | (5,3) => 24 | (5,4) => 24 | (5,5) => 24
  | _ => 0
def oldCount : Site → Nat
  | (2,5) => 2 | (3,3) => 1 | (3,5) => 1 | (4,0) => 1 | (4,1) => 1 | (4,2) => 1
  | _ => 0
def ns (v : Site) : List Site :=
  [(v.1-1,v.2),(v.1+1,v.2),(v.1,(v.2+5)%6),(v.1,(v.2+1)%6)].filter
    (fun u => phaseSites.contains u)
def charge36 (v : Site) : Nat := t36 v+o36 v
def total (f : Site → Nat) (vs : List Site) : Nat := (vs.map f).sum
def vertexCheck (v : Site) (adj : List Site) : Bool :=
  decide (t36 v ≤ o36 v ∧ o36 v ≤ 36 ∧ (oldCount v < 2 ∨ t36 v=0)) &&
  adj.all (fun u => decide (oldCount v=0 ∨ t36 v+o36 u ≤ 36)) &&
  adj.all (fun a => adj.all (fun b => decide (a=b ∨ t36 v+o36 a+o36 b ≤ 72))) &&
  decide ((adj.length+oldCount v-1)*t36 v+total o36 adj ≤ 36*adj.length) &&
  decide (v.1 ≠ 5 ∨ total charge36 (v::adj) ≤ 216)

theorem periodic_local_constraints : phaseSites.all (fun v => vertexCheck v (ns v))=true := by
  decide

/-- Four module-window cuts, with columns reduced modulo six. -/
def windowSites : List (List Site × Nat) :=
  [ ([(2,3),(2,5),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),
       (5,1),(5,2),(5,3),(5,4),(5,5)],16),
    ([(4,2),(4,4),(5,1),(5,2),(5,3),(5,4),(5,5)],10),
    ([(2,3),(2,5),(3,3),(3,4),(3,5),(4,4),(4,5),(4,0),
       (5,3),(5,4),(5,5),(5,0),(5,1)],16),
    ([(2,5),(3,5),(4,4),(4,5),(4,0),(5,3),(5,4),(5,5),(5,0),(5,1)],12) ]

theorem periodic_window_constraints :
    windowSites.all (fun w => decide (total charge36 w.1 ≤ 36*w.2))=true := by decide

theorem periodic_charge_and_omission :
    total charge36 phaseSites=698 ∧ total charge36 [(4,0),(4,1),(4,5),(5,0)]=165 := by decide

def boundaryData : List (Site × List Site) :=
  [ ((3,5),[(2,5),(3,4)]), ((4,2),[(4,3),(5,2)]),
    ((4,4),[(3,4),(4,3),(5,4)]), ((5,1),[(5,2)]), ((5,5),[(5,4)]) ]

theorem periodic_boundary_constraints :
    boundaryData.all (fun w => vertexCheck w.1 w.2)=true := by decide

/-- Scale all fractional charges by36. The chain target has a positive gap. -/
theorem connected_fractional_gap (m value target : Int) (hm : m ≥ 2)
    (hv : value=698*m-165) (ht : target=36*(18*m-2)) :
    value-target=50*m-93 ∧ value>target := by omega

theorem sharp_f_patch_count (k f selected edges : Nat)
    (hs : selected+f=13*k+11) (he : edges=4*k+1+f) : selected+edges=17*k+12 := by omega

/-- Explicit actual6x22 matching; permissions may be restored. -/
def exampleT : List Site := [(0,1),(0,3),(0,5),(0,7),(0,9),(0,11),(0,13),(0,15),(0,17),(0,19),(0,21),(1,2),(1,4),(1,8),(1,10),(1,14),(1,16),(1,20),(2,0),(2,9),(2,15),(3,1),(3,10),(3,16),(3,21),(4,6),(4,8),(4,11),(4,15),(4,18),(4,20),(5,7),(5,9),(5,10),(5,12),(5,14),(5,16),(5,17)]
def exampleM : List (Site × Site) := [((1,1),(2,1)),((1,5),(2,5)),((1,6),(1,7)),((1,11),(2,11)),((1,12),(1,13)),((1,17),(1,18)),((1,19),(2,19)),((2,6),(3,6)),((2,7),(3,7)),((2,12),(2,13)),((2,17),(3,17)),((2,18),(3,18)),((3,8),(3,9)),((3,12),(4,12)),((3,13),(4,13)),((3,14),(4,14)),((3,19),(3,20))]
def exampleP : List Site := exampleM.flatMap (fun e => [e.1,e.2])
def exampleR : List Site := [(0,1),(0,3),(0,5),(0,7),(0,9),(0,11),(0,13),(0,15),(0,17),(0,19),(0,21),(1,2),(1,4),(1,8),(1,10),(1,14),(1,16),(1,20),(2,0),(3,1),(3,21),(4,6),(4,18),(4,20)]
def exampleP0 : List Site := [(1,1),(1,5),(1,6),(1,7),(1,11),(1,12),(1,13),(1,17),(1,18),(1,19),(2,1),(2,6),(2,7),(2,12),(2,13),(2,18),(2,19),(3,6),(3,7),(3,8),(3,12),(3,13),(3,14),(3,18),(3,19),(3,20)]
def exampleC : List Site := [(2,9),(2,11),(2,15),(2,17),(3,9),(3,10),(3,11),(3,15),(3,16),(3,17),(4,8),(4,9),(4,10),(4,11),(4,12),(4,13),(4,14),(4,15),(4,16),(5,7),(5,8),(5,9),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(5,17)]
def gridAdjacent (a b : Site) : Bool :=
  decide ((a.1-b.1)+(b.1-a.1)+(a.2-b.2)+(b.2-a.2)=1)
def insideExample (v : Site) : Bool := decide (v.1<6 ∧ v.2<22)

theorem integer_counterexample_feasible :
    exampleT.all insideExample=true ∧ exampleP.all insideExample=true ∧
    exampleP.eraseDups.length=exampleP.length ∧
    exampleT.all (fun v => !exampleP.contains v)=true ∧
    exampleM.all (fun e => gridAdjacent e.1 e.2)=true ∧
    exampleT.all (fun v => decide (((exampleT++exampleP).filter (gridAdjacent v)).length ≤ 1))=true := by
  decide

theorem integer_counterexample_retains_baseline :
    exampleR.all (fun v => exampleT.contains v)=true ∧
    exampleP0.all (fun v => exampleP.contains v)=true := by decide

theorem integer_counterexample_charge :
    2*(exampleT.filter (fun v => exampleC.contains v)).length+
      (exampleP.filter (fun v => exampleC.contains v)).length=35 ∧
    exampleT.length+exampleM.length=55 ∧ (35 : Nat)>34 := by decide

#print axioms gf_identity
#print axioms gf_bound
#print axioms f_identity
#print axioms f_occupation_bound
#print axioms f_equality_data
#print axioms f_matching_bound
#print axioms successor_isolate_injective
#print axioms successor_component_sum
#print axioms successor_permissions_cancel
#print axioms successor_margin
#print axioms periodic_local_constraints
#print axioms periodic_window_constraints
#print axioms periodic_charge_and_omission
#print axioms periodic_boundary_constraints
#print axioms connected_fractional_gap
#print axioms sharp_f_patch_count

#print axioms integer_counterexample_feasible
#print axioms integer_counterexample_retains_baseline
#print axioms integer_counterexample_charge

end SubQuorum.SuccessorGuardCompensation
