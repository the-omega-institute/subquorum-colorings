"""Scoped local Lean run with comm-basename and memory preflight."""
from pathlib import Path
import json
import re
import subprocess
from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]
NAMES = ['physical_to_canonical', 'canonical_to_physical', 'canonical_accepts',
         'accepts_canonical', 'accepts_iff_physical']


def main():
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/StripColourLift.lean'], cwd=ROOT/'formal',
                         text=True, capture_output=True)
    assert run.returncode == 0 and not run.stderr, run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx', run.stdout), run.stdout
    found = re.findall(r"'SubQuorum.StripColourLift\.(\w+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", run.stdout)
    assert [name for name, _ in found] == NAMES
    audits = [dict(theorem='SubQuorum.StripColourLift.'+name,
                   axioms=[a.strip() for a in axs.split(',') if a.strip()]) for name, axs in found]
    assert all(set(x['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'} for x in audits)
    result = dict(status='PASS', execution_location='local', preflight=check,
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  theorems=audits, stdout=run.stdout, stderr=run.stderr,
                  scope='Arbitrary alphabet and word length: physical rung/vertical grammar normalizes to mono/mixed-pair grammar, equivalent to greedy recognizer.',
                  not_formalized='Geometric extraction of ladder grammar, weighted three-colour model, forest/feedback algorithm, all-width physical families and complexity remain written proofs.')
    (ROOT/'output/strip-colour-formal.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(audits))))


if __name__ == '__main__':
    main()
