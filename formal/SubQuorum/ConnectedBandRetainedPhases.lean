import Lean.Elab.Tactic.Omega
set_option autoImplicit false
namespace SubQuorum.ConnectedBandRetainedPhases
abbrev Site := Nat × Nat
def retained : List Site := [(0,1),(0,3),(0,5),(1,2),(1,4)]
def oldP : List Site := [(1,0),(1,1),(1,5),(2,0),(2,1),(3,0),(3,1),(3,2)]
def free : List Site := [(2,3),(2,5),(3,3),(3,4),(3,5),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]
def tFree : Site → Nat
  | (2,3) => 80
  | (3,4) => 44
  | (4,0) => 36
  | (4,1) => 26
  | (4,2) => 36
  | (4,3) => 40
  | (4,4) => 36
  | (4,5) => 36
  | (5,0) => 35
  | (5,1) => 54
  | (5,2) => 39
  | (5,3) => 54
  | (5,4) => 44
  | (5,5) => 54
  | _ => 0
def x : Site → Site → Nat
  | (1,0), (1,1) => 56
  | (1,1), (1,0) => 56
  | (1,0), (1,5) => 24
  | (1,5), (1,0) => 24
  | (1,1), (2,1) => 24
  | (2,1), (1,1) => 24
  | (1,5), (2,5) => 56
  | (2,5), (1,5) => 56
  | (2,0), (3,0) => 80
  | (3,0), (2,0) => 80
  | (2,1), (3,1) => 56
  | (3,1), (2,1) => 56
  | (2,5), (3,5) => 24
  | (3,5), (2,5) => 24
  | (3,1), (3,2) => 15
  | (3,2), (3,1) => 15
  | (3,1), (4,1) => 9
  | (4,1), (3,1) => 9
  | (3,2), (3,3) => 52
  | (3,3), (3,2) => 52
  | (3,2), (4,2) => 13
  | (4,2), (3,2) => 13
  | (3,3), (4,3) => 4
  | (4,3), (3,3) => 4
  | (3,4), (3,5) => 36
  | (3,5), (3,4) => 36
  | (4,0), (4,1) => 9
  | (4,1), (4,0) => 9
  | (4,0), (5,0) => 9
  | (5,0), (4,0) => 9
  | (4,2), (5,2) => 5
  | (5,2), (4,2) => 5
  | (4,5), (5,5) => 8
  | (5,5), (4,5) => 8
  | _, _ => 0
def ns (v : Site) : List Site :=
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
