"""Discovery-only checks of an unproved cubic bipartite stability inequality."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compiler', default='g++')
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    build = root / 'build/cubic-stability'
    build.mkdir(parents=True, exist_ok=True)
    executable = build / 'explorer'
    subprocess.run([arguments.compiler, '-O3', '-std=c++20',
                    str(root / 'scripts/explore_subcubic_starforming.cpp'), '-o', str(executable)],
                   check=True)
    parameters = [(half, first, second) for half in range(3, 11)
                  for first, second in combinations(range(1, half), 2)]
    parameters += [(11, first, second) for first, second in
                   [(1, 2), (1, 3), (1, 4), (1, 5), (2, 5), (3, 7)]]
    results = []
    for half, first, second in parameters:
        result = json.loads(subprocess.check_output(
            [str(executable), '--circulant', str(half), str(first), str(second)], text=True))
        result.update(half=half, first_shift=first, second_shift=second,
                      defect=6 * half - 5 * result['SF'])
        result['candidate_slack'] = 6 * half + 2 * result['beta'] - 7 * result['SF']
        results.append(result)
    receipt = dict(candidate='7 SF_2 <= 3n + 2 beta_2 for cubic bipartite graphs',
                   candidate_status='UNPROVED', checked_instances=len(results),
                   counterexample_found=any(result['candidate_slack'] < 0 for result in results),
                   strict_gap_instances=sum(result['SF'] > result['beta'] for result in results),
                   smallest_slack=min(result['candidate_slack'] for result in results),
                   scope='Exact subset evaluation of120circulant parameter choices through20vertices and6choices on22vertices. Parameters can give isomorphic or disconnected graphs; these are instances, not distinct isomorphism classes. Stars use the local predicate, and minimality uses the single-deletion equivalence proved separately. This is discovery evidence only, not a proof of the candidate inequality.',
                   instances=results)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: value for key, value in receipt.items() if key != 'instances'}))


if __name__ == '__main__':
    main()
