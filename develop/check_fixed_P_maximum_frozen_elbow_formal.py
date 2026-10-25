"""Generate and kernel-check the concrete feasible, completely frozen board.

The186 upper bound and resource/flow adapter remain written/executable.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

from check_fixed_P_maximum_frozen_elbow import fixture

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def source():
    cur,bits,layers,units=fixture();R,C,T,M=cur;assert (R,C)==(16,28)
    index=lambda v:v[0]*C+v[1]
    P={v for edge in M for v in edge};mate=list(range(R*C));rank=[0]*(R*C)
    wx=[0]*(R*C);wy=[0]*(R*C);old=set()
    for e in M:
        a,b=map(index,e);mate[a]=b;mate[b]=a
    for i,layer in enumerate(layers):
        for v in layer:rank[index(v)]=i
    for layer in layers:
        kept=T|{v for v in P if mate[index(v)] in {index(p) for p in old}}
        for v in layer:
            r,c=v
            ws=sorted({(r-1,c),(r+1,c),(r,c-1),(r,c+1)}&kept)
            assert len(ws)>=2;wx[index(v)],wy[index(v)]=map(index,ws[:2])
        old|=set(layer)
    def array(name,values):
        rows=[', '.join(map(str,values[i:i+16])) for i in range(0,len(values),16)]
        return 'def '+name+' : Array Nat := #[\n  '+',\n  '.join(rows)+'\n]\n\n'
    s='''import SubQuorum.FrozenCertificateReplay

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace SubQuorum.FixedPMaximumFrozenElbow

abbrev Vertex := Fin 448

def at (n : Nat) : Vertex := ⟨n % 448, Nat.mod_lt _ (by decide)⟩

'''
    s+='def selectedIndices : List Nat := ['+', '.join(map(str,sorted(map(index,T))))+']\n\n'
    s+='def endpointIndices : List Nat := ['+', '.join(map(str,sorted(map(index,P))))+']\n\n'
    s+=array('mateIndices',mate)+array('rankIndices',rank)+array('witnessX',wx)+array('witnessY',wy)
    s+='def actualEdges : List (Vertex × Vertex) := ['+', '.join('(at '+str(index(a))+', at '+str(index(b))+')' for a,b in M)+']\n\n'
    s+='''def T (v : Vertex) : Prop := v.val ∈ selectedIndices

def P (v : Vertex) : Prop := v.val ∈ endpointIndices

instance (v : Vertex) : Decidable (T v) := inferInstanceAs (Decidable (v.val ∈ selectedIndices))
instance (v : Vertex) : Decidable (P v) := inferInstanceAs (Decidable (v.val ∈ endpointIndices))

def mate (v : Vertex) : Vertex := at (mateIndices[v.val]!)
def rank (v : Vertex) : Nat := rankIndices[v.val]!
def x (v : Vertex) : Vertex := at (witnessX[v.val]!)
def y (v : Vertex) : Vertex := at (witnessY[v.val]!)

/-- Four physical nearest neighbors, with no wrap across the board boundary. -/
def neighbors (v : Vertex) : List Vertex :=
  (if v.val % 28 > 0 then [at (v.val + 447)] else []) ++
  (if v.val % 28 < 27 then [at (v.val + 1)] else []) ++
  (if v.val ≥ 28 then [at (v.val + 420)] else []) ++
  (if v.val < 420 then [at (v.val + 28)] else [])

def E (v w : Vertex) : Prop := w ∈ neighbors v
instance (v w : Vertex) : Decidable (E v w) := inferInstanceAs (Decidable (w ∈ neighbors v))

def occupiedDegree (v : Vertex) : Nat :=
  ((neighbors v).filter fun w => decide (T w ∨ P w)).length

/-- Exact stored counts, with no duplicate selected or endpoint index. -/
theorem inventory :
    selectedIndices.length = 186 ∧ selectedIndices.Nodup ∧
    endpointIndices.length = 70 ∧ endpointIndices.Nodup ∧
    actualEdges.length = 35 := by decide

/-- Concrete physical feasibility of the selected vertices. -/
theorem selected_feasible : ∀ v : Vertex, T v → ¬ P v ∧ occupiedDegree v ≤ 1 := by
  decide

/-- The stored actual edges are physical, have the stored mates, and
cover each endpoint exactly once. The mate map is an involution. -/
theorem actual_matching :
    (actualEdges.all fun e => decide (E e.1 e.2 ∧ mate e.1 = e.2 ∧ mate e.2 = e.1)) = true ∧
    (actualEdges.flatMap fun e => [e.1.val,e.2.val]).Nodup ∧
    (∀ v : Vertex, P v ↔ v.val ∈ (actualEdges.flatMap fun e => [e.1.val,e.2.val])) ∧
    (∀ v : Vertex, mate (mate v) = v) := by decide

/-- Every one of the70 concrete endpoints has two distinct physical kept
neighbors, with a strictly earlier actual-mate rank for nonselected witnesses. -/
theorem strict_witness_checks : ∀ p : Vertex, P p →
    x p ≠ y p ∧ E p (x p) ∧ E p (y p) ∧
    FrozenCertificateReplay.Kept T P P mate rank p (x p) ∧
    FrozenCertificateReplay.Kept T P P mate rank p (y p) := by
  unfold FrozenCertificateReplay.Kept
  decide

theorem certificate : FrozenCertificateReplay.Certificate E T P P mate rank := by
  intro p hp
  exact ⟨x p,y p,strict_witness_checks p hp⟩

/-- Every predicate closed under the physical two-kept-neighbor freezing
rule contains all70 matching endpoints. This uses general rank soundness. -/
theorem completely_frozen (F : Vertex → Prop)
    (closed : ∀ p, P p → (∃ a b, a ≠ b ∧ E p a ∧ E p b ∧
      (T a ∨ F (mate a)) ∧ (T b ∨ F (mate b))) → F p) :
    ∀ p, P p → F p := by
  exact FrozenCertificateReplay.certificate_sound E T P P F mate rank certificate closed

end SubQuorum.FixedPMaximumFrozenElbow

#print axioms SubQuorum.FixedPMaximumFrozenElbow.inventory
#print axioms SubQuorum.FixedPMaximumFrozenElbow.selected_feasible
#print axioms SubQuorum.FixedPMaximumFrozenElbow.actual_matching
#print axioms SubQuorum.FixedPMaximumFrozenElbow.strict_witness_checks
#print axioms SubQuorum.FixedPMaximumFrozenElbow.certificate
#print axioms SubQuorum.FixedPMaximumFrozenElbow.completely_frozen
'''
    return re.sub(r"\bat\b", "vertex", s)


def main():
    p=argparse.ArgumentParser();p.add_argument('--lean',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--generate',action='store_true');args=p.parse_args();root=Path(__file__).resolve().parents[1]
    path=root/'formal/SubQuorum/FixedPMaximumFrozenElbow.lean'
    if args.generate:path.write_text(source())
    assert path.read_text()==source()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',path.read_text())
    def processes():
        lines=subprocess.check_output(['ps','-axo','pid=,comm='],text=True).splitlines()
        return [s.strip() for s in lines if len(s.split(None,1))==2 and os.path.basename(s.split(None,1)[1]) in ('lean','lake')]
    memory=subprocess.check_output(['memory_pressure'],text=True)
    preflight=dict(active_processes_by_comm_basename=processes(),memory_free_percentage=re.search(r'System-wide memory free percentage: (\d+%)',memory).group(1),physical_memory_bytes=int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True)),execution='User chose local; one concrete module plus its small existing rank-soundness dependency, sequential; no shared CI changes.')
    print(json.dumps(preflight),flush=True);lean=str(args.lean.resolve());version=subprocess.check_output([lean,'--version'],text=True).strip()
    assert 'version 4.33.0' in version
    with tempfile.TemporaryDirectory(prefix='fixed-P-frozen-lean-') as tmp:
        tmpdir=Path(tmp);(tmpdir/'SubQuorum').mkdir();env=os.environ.copy();env['LEAN_PATH']=str(tmpdir)
        dep=root/'formal/SubQuorum/FrozenCertificateReplay.lean'
        result=subprocess.run([lean,'-o',str(tmpdir/'SubQuorum/FrozenCertificateReplay.olean'),str(dep)],cwd=root/'formal',env=env,text=True,capture_output=True)
        assert result.returncode==0,result.stdout+result.stderr
        result=subprocess.run([lean,str(path)],cwd=root/'formal',env=env,text=True,capture_output=True)
    output=result.stdout+result.stderr;print(output,end='',flush=True);assert result.returncode==0
    assert not re.search(r'warning:|error:|sorryAx|Lean.ofReduceBool|Lean.trustCompiler',output)
    audits=[s for s in output.splitlines() if 'depends on axioms' in s or 'does not depend' in s]
    assert len(audits)==6
    for body in re.findall(r'depends on axioms: \[([^\]]*)\]',output):
        assert {a.strip() for a in body.split(',') if a.strip()} <= {'propext','Quot.sound'}
    args.output.write_text(json.dumps(dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=version,preflight=preflight,active_processes_after_by_comm_basename=processes(),declaration_audits=audits,scope='Concrete186selected/70endpoint/35matchingedge inventory and uniqueness, all selected physical neighbor degrees, actual matching validity and involution, all70strict-rank witnesses, and complete freezing via general soundness. Kernel decide, no native evaluation.',not_formalized=['Geometric186upper bound, canonical mixed bands, original forests/whole-support and physical links, exact packing optima, and E/F resource replacements. These have written proofs and independent executable checks.'],allowed_standard_axioms=['propext','Quot.sound'],sorry=False,native_decide=False,new_axioms=False),indent=2)+'\n')
    print('PASS: 6 concrete board and complete-freezing audits')

if __name__=='__main__':main()
