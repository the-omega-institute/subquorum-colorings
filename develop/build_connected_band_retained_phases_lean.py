"""Independent small kernel check of the corrected whole-board periodic pattern."""
from pathlib import Path
from check_connected_band_fractional_matching import PERIOD_T, PERIOD_X, ROOT

def site(v):return f'({v[0]},{v[1]})'
lines=['import Lean.Elab.Tactic.Omega','set_option autoImplicit false',
'namespace SubQuorum.ConnectedBandRetainedPhases','abbrev Site := Nat × Nat',
'def retained : List Site := [(0,1),(0,3),(0,5),(1,2),(1,4)]',
'def oldP : List Site := [(1,0),(1,1),(1,5),(2,0),(2,1),(3,0),(3,1),(3,2)]',
'def free : List Site := [(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]',
'def tFree : Site → Nat']
lines += [f'  | {site(v)} => {q}' for v,q in sorted(PERIOD_T.items())]+['  | _ => 0','def x : Site → Site → Nat']
for (v,u),q in sorted(PERIOD_X.items()):
 lines += [f'  | {site(v)}, {site(u)} => {q}',f'  | {site(u)}, {site(v)} => {q}']
lines += ['  | _, _ => 0', '''def ns (v : Site) : List Site :=
  (if v.1>0 then [(v.1-1,v.2)] else []) ++
  (if v.1<5 then [(v.1+1,v.2)] else []) ++
  [(v.1,(v.2+5)%6),(v.1,(v.2+1)%6)]
def board : List Site := (List.range 6).flatMap (fun r => (List.range 6).map (fun c => (r,c)))
def sum (f : Site → Nat) (s : List Site) : Nat := (s.map f).sum
def t (v : Site) : Nat := if retained.contains v then 80 else tFree v
def p (v : Site) : Nat := sum (x v) (ns v)
def o (v : Site) : Nat := t v+p v

theorem periodic_occupation_and_matching :
    board.all (fun v => decide (t v≤o v ∧ o v≤80) &&
      (ns v).all (fun a => (ns v).all (fun w => decide
        (a=w ∨ t v+o a+o w≤160))) &&
      decide (((ns v).length-1)*t v+sum o (ns v)≤80*(ns v).length))=true ∧
    oldP.all (fun v => decide (p v=80))=true := by decide

theorem corrected_retained_domain :
    retained.all (fun v => (ns v).all (fun u => !(retained.contains u) && !(free.contains u)))=true ∧
    retained.all (fun v => decide (((ns v).filter oldP.contains).length≤1))=true ∧
    retained.length=5 ∧ retained.contains (0,3)=true ∧ retained.contains (0,0)=false := by decide

#print axioms periodic_occupation_and_matching
#print axioms corrected_retained_domain
end SubQuorum.ConnectedBandRetainedPhases
''']
(ROOT/'formal/SubQuorum/ConnectedBandRetainedPhases.lean').write_text('\n'.join(lines).rstrip()+'\n')
p=ROOT/'develop/check_connected_band_fractional_matching_formal.py'
s=p.read_text().replace('ConnectedBandFractionalMatching','ConnectedBandRetainedPhases').replace('assert len(audits)==9','assert len(audits)==2')
a=s.index("        scope='");b=s.index('        sorry=False',a)
s=s[:a]+'''        scope='Two axiom-free kernel computations verify the corrected retained phases (row0 residues1,3,5; row1 residues2,4), the entire periodic whole-board occupation/wedge/full-degree system and old endpoint matching saturation. Explicitly excludes incorrect row0 residue0.',
        not_formalized=['All-length finite old-family to periodic coordinate adapter remains a written proof and exact Python check. No integer/frozen or end-to-end grid theorem.'],
'''+s[b:]
s=s.replace('PASS:9 simultaneous fractional matching Lean audits','PASS:2 corrected periodic whole-board Lean audits')
(ROOT/'develop/check_connected_band_retained_phases_formal.py').write_text(s)
