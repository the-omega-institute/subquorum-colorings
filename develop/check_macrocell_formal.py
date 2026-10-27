"""Local Lean run, measuring memory and real Lean/Lake processes first."""
from pathlib import Path
import json
import re
import subprocess
from check_unprotected_white_pair_formal import preflight

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['top_left_neighbours', 'top_right_neighbours', 'side_neighbours',
         'forced_top_ports', 'forced_selected_end']


def main():
    checks = preflight()
    r = subprocess.run(['lean', 'SubQuorum/MacrocellPorts.lean'], cwd=ROOT/'formal',
                       text=True, capture_output=True)
    assert r.returncode == 0 and not r.stderr, r.stdout+r.stderr
    assert not re.search(r'warning:|error:|sorryAx', r.stdout), r.stdout
    found = re.findall(r"'SubQuorum.MacrocellPorts\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", r.stdout)
    assert [n for n, _ in found] == NAMES
    audits = [dict(theorem='SubQuorum.MacrocellPorts.'+n,
                   axioms=[a.strip() for a in axs.split(',') if a.strip()]) for n, axs in found]
    assert all(set(a['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'} for a in audits)
    out = dict(status='PASS', execution_location='local', preflight=checks,
               toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
               command='cd formal && lean SubQuorum/MacrocellPorts.lean',
               theorems=audits, stdout=r.stdout, stderr=r.stderr,
               scope='Local 4-by-2 grid neighbour constraints and forced top-port/selected-end laws from arbitrary legal involutive mate maps.',
               not_formalized='Global flow/min-cut, all-width concatenation and stacked coordinate embedding, and exact batch-depth bounds are written proofs.')
    (ROOT/'output/macrocell-formal.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(audits))))


if __name__ == '__main__':
    main()
