"""Run the standalone Std collar audit sequentially on the selected machine."""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    processes = subprocess.check_output(['ps', '-axo', 'pid=,comm=,rss='], text=True)
    active = []
    for line in processes.splitlines():
        process_id, remainder = line.strip().split(None, 1)
        executable, resident = remainder.rsplit(None, 1)
        if Path(executable).name in {'lean', 'lake'}:
            active.append(dict(pid=int(process_id), executable=executable, rss_kib=int(resident)))
    memory = subprocess.check_output(['vm_stat'], text=True)
    print(json.dumps(dict(active_lean_lake=active, memory=memory)), flush=True)
    executable = arguments.lean.resolve()
    version = subprocess.check_output([str(executable), '--version'], text=True).strip()
    assert 'version 4.33.0' in version
    build = root/'build/pressured-collar-formal'
    (build/'SubQuorum').mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, LEAN_PATH=str(build))
    checks = []
    for module in ('SubQuorum/CollarCompensation.lean',
                   'SubQuorum/AttachmentCollarCompensation.lean',
                   'SubQuorum/BlankWitnessCompensation.lean',
                   'SubQuorum/DiagonalWitnessChains.lean',
                   'SubQuorum/MixedPChainCompensation.lean',
                   'SubQuorum/FrozenPromotion.lean',
                   'SubQuorum/OwnedDonorCompensation.lean',
                   'SubQuorum/SingleSquareObstacle.lean',
                   'SubQuorum/LadderReduction.lean', 'SubQuorum/CompatibleBundles.lean',
                   'SubQuorum/BipartitePromotion.lean',
                   'SubQuorum/ComponentReceivers.lean',
                   'SubQuorum/ThinComponents.lean',
                   'SubQuorum/BentReceiverCompensation.lean',
                   'SubQuorum/LongBentTerminalStrips.lean',
                   'SubQuorum/TransverseCombMouths.lean',
                   'SubQuorum/CombEndFlux.lean',
                   'SubQuorum/ParallelCombFlux.lean',
                   'CollarCompensationAudit.lean'):
        command = [str(executable), module]
        if not module.endswith('Audit.lean'):
            command += ['-o', str((build/module).with_suffix('.olean'))]
        started = time.monotonic()
        result = subprocess.run(command, cwd=root/'formal', env=environment,
                                capture_output=True, text=True)
        print(result.stdout, end='', flush=True)
        print(result.stderr, end='', flush=True)
        assert result.returncode == 0, module
        assert not re.search(r'error:|sorryAx|Lean\.ofReduceBool|Lean\.trustCompiler',
                             result.stdout+result.stderr)
        checks.append(dict(module=module, seconds=round(time.monotonic()-started, 3),
                           stdout=result.stdout, stderr=result.stderr, exit_code=result.returncode))
    declarations = re.findall(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)",
                              checks[-1]['stdout'])
    assert len(declarations) == 90
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    assert all({name.strip() for name in axioms.split(',') if name.strip()} <= allowed
               for _, axioms in declarations)
    report = dict(status='ALL_CHECKS_PASSED', lean_version=version,
                  checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  active_lean_lake_before=active, memory_before=memory,
                  peak_child_rss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  peak_child_rss_unit='bytes on macOS; KiB on Linux', checks=checks,
                  audited_declarations=[name for name, _ in declarations],
                  sha256={str(Path('formal')/record['module']): hashlib.sha256(
                      (root/'formal'/record['module']).read_bytes()).hexdigest() for record in checks},
                  scope='Previous 85 scoped declarations plus four exact physical/shifted tile-count formulas for an explicitly labeled horizontal comb of arbitrary positive even endpoint length, and its unconditional finite-sum raw receiver neutrality in both phases. Global source/comb contact geometry, coalesced interval/source-tip counts, normalization adapters and the mixed-contact initial-pair theorem remain written proofs. Earlier geometric scope limitations still apply. No full geometric Lean verification, unmatched exterior compensation or universal source coverage is claimed.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], audited_declarations=len(declarations))), flush=True)


if __name__ == '__main__':
    main()
