"""Local arithmetic-only Lean checks, with memory/process preflight."""
import json
from pathlib import Path
import re
import subprocess

from check_unprotected_white_pair_formal import preflight

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['terminal_balance', 'batch_residuals', 'full_hall_weighted',
         'retention_normalized', 'terminal_penalty', 'band_counts', 'penalty_one']


def main():
    check = preflight()
    run = subprocess.run(['lean', 'SubQuorum/MixedTerminalCompensation.lean'],
                         cwd=ROOT/'formal', text=True, capture_output=True)
    assert run.returncode == 0 and not run.stderr, run.stdout+run.stderr
    assert not re.search(r'warning:|error:|sorryAx', run.stdout), run.stdout
    found = re.findall(
        r"'SubQuorum.MixedTerminalCompensation\.(\w+)' "
        r"(?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", run.stdout)
    assert [name for name, _ in found] == NAMES
    theorems = [dict(theorem='SubQuorum.MixedTerminalCompensation.'+name,
                     axioms=[a.strip() for a in axioms.split(',') if a.strip()])
                for name, axioms in found]
    assert all(set(x['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for x in theorems)
    result = dict(status='PASS', execution_location='local',
                  command='cd formal && lean SubQuorum/MixedTerminalCompensation.lean',
                  toolchain=(ROOT/'formal/lean-toolchain').read_text().strip(),
                  preflight=check, theorems=theorems, stdout=run.stdout, stderr=run.stderr,
                  scope='Terminal counts, simultaneous-batch residuals, conditional half-area and exact scaled 5/6 margin, normalized retention arithmetic, terminal penalty and arbitrary band counts, with explicit geometric/optimization hypotheses.',
                  not_formalized='Matching decomposition, square-arm gluing, component-disjoint switches, Hall theorem, optimization existence and all-length coordinate/feasibility proof remain written. Not end-to-end grid Lean.')
    (ROOT/'output/mixed-terminal-compensation-formal.json').write_text(
        json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', theorems=len(theorems))))


if __name__ == '__main__':
    main()
