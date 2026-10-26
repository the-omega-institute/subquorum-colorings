"""Export exact witness data; Lean independently evaluates the stated predicates."""
from pathlib import Path
from check_connected_band_fractional_matching import *


def site(v): return f'({v[0]},{v[1]})'
def sites(vs): return '['+','.join(site(v) for v in sorted(vs))+']'
def fun(name,data):
    return '\n'.join([f'def {name} : Site → Nat']+[f'  | {site(v)} => {q}' for v,q in sorted(data.items())]+['  | _ => 0'])
def xfun(name,data):
    pats=[]
    for (v,u),q in sorted(data.items()):
        pats.extend([f'  | {site(v)}, {site(u)} => {q}',f'  | {site(u)}, {site(v)} => {q}'])
    return '\n'.join([f'def {name} : Site → Site → Nat',*pats,'  | _, _ => 0'])

old,R,P0,U,C,es=domain(8)
_,_,HP,HU,_,_=domain(2)
Pphase={reduced(v) for v in P0 if 20<=v[1]<=40}
lines=['import Lean.Elab.Tactic.Omega','set_option autoImplicit false','set_option maxRecDepth 16384','set_option maxHeartbeats 0',
'namespace SubQuorum.ConnectedBandFractionalMatching','abbrev Site := Nat × Nat',
fun('baseT',BASE_T),xfun('baseX',BASE_X),fun('periodT',PERIOD_T),xfun('periodX',PERIOD_X),
f'def oldP : List Site := {sites(P0)}',f'def retained : List Site := {sites(R)}',
f'def free : List Site := {sites(U)}',f'def component : List Site := {sites(C)}',
f'def phaseP : List Site := {sites(Pphase)}',
f'def phaseFree : List Site := {sites({reduced(v) for v in C})}',
'def sum (f : Site → Nat) (s : List Site) : Nat := (s.map f).sum',
'def phase (v : Site) : Site := (v.1,v.2%6)',
'''def ns (v : Site) : List Site :=
  (if v.1>0 then [(v.1-1,v.2)] else []) ++
  (if v.1<5 then [(v.1+1,v.2)] else []) ++
  (if v.2>0 then [(v.1,v.2-1)] else []) ++
  (if v.2<57 then [(v.1,v.2+1)] else [])
def pns (v : Site) : List Site :=
  (if v.1>0 then [(v.1-1,v.2)] else []) ++
  (if v.1<5 then [(v.1+1,v.2)] else []) ++
  [(v.1,(v.2+5)%6),(v.1,(v.2+1)%6)]
def inc (v : Site) : Nat := sum (baseX v) (ns v)
def pinc (v : Site) : Nat := sum (periodX v) (pns v)
def occ (v : Site) : Nat := baseT v+inc v
def pocc (v : Site) : Nat := periodT v+pinc v
def checkLocal (t o : Site → Nat) (v : Site) (adj : List Site) (b : Nat) : Bool :=
  decide (t v ≤ o v ∧ o v ≤ 80 ∧ (b<2 ∨ t v=0)) &&
  adj.all (fun u => decide (b=0 ∨ t v+o u≤80)) &&
  adj.all (fun a => adj.all (fun w => decide (a=w ∨ t v+o a+o w≤160))) &&
  decide ((adj.length+b-1)*t v+sum o adj≤80*adj.length)
def board : List Site := (List.range 6).flatMap (fun r => (List.range 58).map (fun c => (r,c)))
def allT (v : Site) : Nat := if retained.contains v then 80 else baseT v
def allO (v : Site) : Nat := allT v+inc v

theorem finite_matching_capacities :
    oldP.all (fun v => decide (inc v=80))=true ∧
    free.all (fun v => decide (baseT v+inc v≤80))=true ∧
    board.all (fun v => (ns v).all (fun u => decide
      (baseX v u≤80 ∧ baseX v u=baseX u v)))=true := by decide

theorem finite_local_constraints :
    free.all (fun v => checkLocal baseT occ v ((ns v).filter free.contains)
      (((ns v).filter oldP.contains).length))=true ∧
    component.all (fun v => decide (v.1≠5 ∨
      sum (fun u => baseT u+occ u) (v::((ns v).filter free.contains))≤480))=true := by decide

theorem finite_global_occupation :
    board.all (fun v => decide (allT v≤allO v ∧ allO v≤80) &&
      (ns v).all (fun a => (ns v).all (fun w => decide
        (a=w ∨ allT v+allO a+allO w≤160))) &&
      decide (((ns v).length-1)*allT v+sum allO (ns v)≤80*(ns v).length))=true := by decide
''']
# Window lists are literal coordinates in the finite board, independently checked by Lean.
ws=[]
for _,pat,b in WINDOWS:
    for i in range(8):
        S={(r,c+9+6*i) for r,c in pat}
        if S<=C:ws.append((S,b))
lines.append('def windows : List (List Site × Nat) := ['+','.join(f'({sites(s)},{b})' for s,b in ws)+']')
lines.append('def phaseWindows : List (List Site × Nat) := ['+','.join(f'({sites({reduced((r,c+9)) for r,c in pat})},{b})' for _,pat,b in WINDOWS)+']')
lines.extend(['''theorem finite_windows :
    windows.all (fun w => decide (sum (fun v => baseT v+occ v) w.1≤80*w.2))=true := by decide

theorem periodic_matching_and_local :
    phaseP.all (fun v => decide (pinc v=80))=true ∧
    phaseFree.all (fun v => checkLocal periodT pocc v ((pns v).filter phaseFree.contains)
      (((pns v).filter phaseP.contains).length))=true ∧
    phaseFree.all (fun v => decide (v.1≠5 ∨
      sum (fun u => periodT u+pocc u) (v::((pns v).filter phaseFree.contains))≤480))=true ∧
    phaseWindows.all (fun w => decide (sum (fun v => periodT v+pocc v) w.1≤80*w.2))=true := by decide

theorem seed_periodic_collar :
    free.all (fun v => decide (v.2<20 ∨ v.2>40 ∨ baseT v=periodT (phase v)))=true ∧
    board.all (fun v => (ns v).all (fun u => decide
      (v.2<20 ∨ v.2>40 ∨ u.2<20 ∨ u.2>40 ∨ baseX v u=periodX (phase v) (phase u))))=true := by decide

def edgeTotal : Nat := (board.map (fun v => sum (baseX v) (ns v))).sum/2
def periodBoard : List Site := (List.range 6).flatMap (fun r => (List.range 6).map (fun c => (r,c)))
def phaseEdgeTotal : Nat := (periodBoard.map (fun v => sum (periodX v) (pns v))).sum/2

theorem base_and_period_counts :
    sum (fun v => 2*baseT v+inc v) component=12069 ∧
    80*retained.length+sum baseT free+edgeTotal=13346 ∧
    sum (fun v => 2*periodT v+pinc v) phaseFree=1548 ∧
    sum periodT phaseFree=614 ∧ phaseEdgeTotal=480 := by decide

theorem all_m_gap (m whole target : Int) (hm : m≥18)
    (hw : whole=1494*m+1394) (ht : target=80*(18*m+29)) :
    whole-target=54*m-926 ∧ whole>target := by omega
''',f'def hallPossible : List Site := {sites(HP|HU)}',
'def hallA : List Site := [(1,18),(2,17),(2,19),(3,18),(3,20)]',
'def hallN : List Site := [(1,17),(1,19),(2,18),(3,17),(3,19)]',
'''def adjacent (v u : Site) : Bool :=
  decide ((v.1=u.1 ∧ (v.2+1=u.2 ∨ u.2+1=v.2)) ∨
          (v.2=u.2 ∧ (v.1+1=u.1 ∨ u.1+1=v.1)))
def hallDemand (v : Site) : Nat := if v=(3,17) then 61 else 92

theorem old92_terminal_hall_deficit :
    hallPossible.all (fun u => decide ((hallA.any (fun v => adjacent v u)) = hallN.contains u))=true ∧
    sum hallDemand hallA=460 ∧ sum hallDemand hallN=429 ∧ (460:Nat)>429 := by decide
'''])
names=['finite_matching_capacities','finite_local_constraints','finite_global_occupation','finite_windows','periodic_matching_and_local','seed_periodic_collar','base_and_period_counts','all_m_gap','old92_terminal_hall_deficit']
lines.extend('#print axioms '+n for n in names)
lines.append('end SubQuorum.ConnectedBandFractionalMatching')
(ROOT/'formal/SubQuorum/ConnectedBandFractionalMatching.lean').write_text('\n\n'.join(lines)+'\n')
