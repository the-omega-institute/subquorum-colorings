import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.ConnectedBandMateCoverageBarrier
abbrev Site := Nat × Nat
def phaseSites : List Site :=
  [(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
   (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]
def t92 : Site → Nat
  | (2,3) => 92
  | (2,5) => 0
  | (3,3) => 0
  | (3,4) => 56
  | (3,5) => 0
  | (4,0) => 36
  | (4,1) => 38
  | (4,2) => 36
  | (4,3) => 47
  | (4,4) => 36
  | (4,5) => 53
  | (5,0) => 55
  | (5,1) => 54
  | (5,2) => 49
  | (5,3) => 54
  | (5,4) => 56
  | (5,5) => 54
  | _ => 0
def o92 : Site → Nat
  | (2,3) => 92
  | (2,5) => 92
  | (3,3) => 67
  | (3,4) => 92
  | (3,5) => 61
  | (4,0) => 54
  | (4,1) => 56
  | (4,2) => 54
  | (4,3) => 56
  | (4,4) => 36
  | (4,5) => 56
  | (5,0) => 56
  | (5,1) => 54
  | (5,2) => 56
  | (5,3) => 70
  | (5,4) => 56
  | (5,5) => 58
  | _ => 0
def oldCount : Site → Nat
  | (2,5) => 2 | (3,3) => 1 | (3,5) => 1 | (4,0) => 1 | (4,1) => 1 | (4,2) => 1
  | _ => 0
def ns (v : Site) : List Site :=
  [(v.1-1,v.2),(v.1+1,v.2),(v.1,(v.2+5)%6),(v.1,(v.2+1)%6)].filter
    (fun u => phaseSites.contains u)
def charge92 (v : Site) : Nat := t92 v+o92 v
def total (f : Site → Nat) (vs : List Site) : Nat := (vs.map f).sum
def checkWith (t o : Site → Nat) (b : Nat) (v : Site) (adj : List Site) : Bool :=
  decide (t v ≤ o v ∧ o v ≤ 92 ∧ (b<2 ∨ t v=0)) &&
  adj.all (fun u => decide (b=0 ∨ t v+o u ≤ 92)) &&
  adj.all (fun a => adj.all (fun bb => decide (a=bb ∨ t v+o a+o bb ≤ 184))) &&
  decide ((adj.length+b-1)*t v+total o adj ≤ 92*adj.length) &&
  decide (v.1 ≠ 5 ∨ total (fun u => t u+o u) (v::adj) ≤ 552) &&
  decide (o v-t v ≤ 92*b+total (fun u => o u-t u) adj)
def windowSites : List (List Site × Nat) :=
  [ ([(2,3),(2,5),(3,3),(3,4),(3,5),(4,2),(4,3),(4,4),
       (5,1),(5,2),(5,3),(5,4),(5,5)],16),
    ([(4,2),(4,4),(5,1),(5,2),(5,3),(5,4),(5,5)],10),
    ([(2,3),(2,5),(3,3),(3,4),(3,5),(4,4),(4,5),(4,0),
       (5,3),(5,4),(5,5),(5,0),(5,1)],16),
    ([(2,5),(3,5),(4,4),(4,5),(4,0),(5,3),(5,4),(5,5),(5,0),(5,1)],12) ]


theorem bulk_and_windows :
    phaseSites.all (fun v => checkWith t92 o92 (oldCount v) v (ns v))=true ∧
    windowSites.all (fun w => decide (total charge92 w.1 ≤ 92*w.2))=true := by decide

def phase (v : Site) : Site := (v.1,v.2%6)
def tb (v : Site) : Nat := t92 (phase v)
def ob (v : Site) : Nat := if v=(5,17) then tb v else o92 (phase v)
def boundaryData : List (Site × List Site) :=
  [ ((3,17),[(2,17),(3,16)]), ((4,8),[(4,9),(5,8)]),
    ((4,16),[(3,16),(4,15),(5,16)]), ((5,7),[(5,8)]),
    ((5,16),[(4,16),(5,15),(5,17)]), ((5,17),[(5,16)]) ]

theorem patched_boundary_constraints :
    boundaryData.all (fun w => checkWith tb ob (oldCount (phase w.1)) w.1 w.2)=true := by decide

theorem period_omission_and_patch : total charge92 phaseSites=1782 ∧
    total charge92 [(4,0),(4,1),(4,5),(5,0)]=404 ∧ o92 (5,5)-t92 (5,5)=4 := by decide

theorem all_m_positive_gap (m value target : Int) (hm : m ≥ 2)
    (hv : value=1782*m-408) (ht : target=92*(18*m-2)) :
    value-target=126*m-224 ∧ value>target := by omega

#print axioms bulk_and_windows
#print axioms patched_boundary_constraints
#print axioms period_omission_and_patch
#print axioms all_m_positive_gap
end SubQuorum.ConnectedBandMateCoverageBarrier
