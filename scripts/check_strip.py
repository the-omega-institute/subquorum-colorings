"""Regenerate one strip's readouts and both full certificate vectors."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    m = int(sys.argv[1])
    assert 1 <= m <= 11
    saved = ROOT/f'develop/results/omega-w{m}'
    rows = list(csv.DictReader(saved.with_suffix('.csv').open()))
    meta = json.loads(saved.with_suffix('.json').read_text())
    with tempfile.TemporaryDirectory(prefix=f'grid-w{m}-') as tmp:
        prefix = Path(tmp)/'omega'
        run = subprocess.run([str(ROOT/'build/grid_omega'), str(m), str(len(rows)), str(prefix)],
                             check=True, capture_output=True, text=True)
        actual = list(csv.DictReader(run.stdout.splitlines()))
        assert actual == rows, f'finite readouts differ at width {m}'
        assert json.loads(prefix.with_suffix('.json').read_text()) == meta
        for suffix in ('-start.tsv','-end.tsv'):
            assert Path(str(prefix)+suffix).read_bytes() == Path(str(saved)+suffix).read_bytes()
        independent = subprocess.run([str(ROOT/'build/check_omega'), str(m), str(meta['start']),
                                      str(meta['period']), str(meta['doubled_increment']), str(prefix)],
                                     check=True, capture_output=True, text=True)
    report = dict(status='passed', width=m, finite_lengths=len(rows), certificate=meta,
                  from_initial_state=True, independent_check=independent.stdout.strip(),
                  source_hashes={name: hashlib.sha256((ROOT/'develop'/name).read_bytes()).hexdigest()
                                 for name in ('grid_omega.cpp','check_omega.cpp')})
    out = ROOT/'build'
    (out/f'check-width-{m}.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
