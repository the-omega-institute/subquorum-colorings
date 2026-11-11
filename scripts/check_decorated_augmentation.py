"""Supplement the unchanged decoration checker with its missing augmentation branch.

These two prescribed minimal sets were supplied and independently checked in
review. Literal three-vertex stars check their formation and every deletion;
the original upper_map is the implementation under test.
"""
import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'decoration_under_test', ROOT / 'scripts/check_decorated_interface.py')
impl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(impl)


def literal_failures(graph, selected):
    outside = set(graph) - selected
    formed = set()
    for a, b in itertools.combinations(selected, 2):
        ab = b in graph[a]
        for x in outside - formed:
            if ab + (x in graph[a]) + (x in graph[b]) >= 2:
                formed.add(x)
    return outside - formed


def main():
    report = {'status': 'PASS', 'cases': [], 'single_deletions': 0,
              'original_checker_changed': False, 'new_Lean': False}
    for leaves in (1, 2):
        h = {0: set(range(1, leaves + 1))}
        h.update({i: {0} for i in range(1, leaves + 1)})
        graph = impl.decorate(h)
        selected = set()
        # Centre: both six-sets; its interface and every Z are omitted.
        for block in (0, 10):
            selected.update(block + i for i in (0, 1, 2, 3, 8, 9))
        for leaf in range(1, leaves + 1):
            offset = 21 * leaf
            # First block V + {z1,u}; second block A + W + {p}; selected y.
            selected.update(offset + i for i in
                            (2, 3, 6, 9, 10, 11, 14, 15, 18, 20))
        assert len(selected) == 12 + 10 * leaves
        assert not literal_failures(graph, selected)
        witnesses = {}
        for vertex in sorted(selected):
            failed = literal_failures(graph, selected - {vertex})
            assert failed, (leaves, vertex)
            witnesses[vertex] = min(failed)
            report['single_deletions'] += 1
        losses = {v: 12 - len(selected & set(range(21*v, 21*v+21)))
                  for v in h}
        p = {v for v in h if losses[v] > 0}
        # Each leaf is selected and internally active, and has no P neighbour.
        assert p == set(range(1, leaves + 1))
        for v in p:
            assert 21*v+20 in selected and 21*v+6 in selected
            assert h[v] and not h[v] & p and losses[v] == 2
        choices = {v: min(h[v]) for v in p}
        assert set(choices.values()) == {0}
        q = p | set(choices.values())
        assert not literal_failures(h, q)
        assert impl.upper_map(h, graph, selected) == 2 * leaves
        report['cases'].append({
            'interface': f'K1,{leaves}', 'decorated_order': len(graph),
            'selected_size': len(selected), 'augmentation_indices': sorted(p),
            'added_choices': choices, 'distinct_additions': 1,
            'repeated_choice': leaves > 1, 'upper_Q_size': len(q),
            'total_module_loss': sum(losses.values()),
            'deletion_failure_witnesses': witnesses})
    path = ROOT / 'output/decorated-augmentation-check.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'cases': len(report['cases']),
                      'single_deletions': report['single_deletions'],
                      'repeated_choice_cases': sum(c['repeated_choice']
                                                   for c in report['cases'])}))


if __name__ == '__main__':
    main()
