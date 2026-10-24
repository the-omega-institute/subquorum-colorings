"""Mixed neutral-word identities and conditional external-region quota controls."""

from collections import Counter
import itertools
import json

from check_incoming_and_cycle_regions import region_controls


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def word_controls():
    counts = Counter()
    by_length = {}
    for length in (2, 4, 6, 8):
        accepted = 0
        for phases in itertools.product((False, True), repeat=length):
            for exits in itertools.product((False, True), repeat=length):
                signs = [1 if index % 2 == 0 else -1 for index in range(length)]
                total = -sum(sign*(2*int(phase)+(1 if active else -1))
                             for sign, phase, active in zip(signs, phases, exits))
                if total != 4:
                    continue
                inward = outward = positive01 = negative01 = negative10 = 0
                passive01 = double10 = 0
                for index in range(length):
                    following = (index+1) % length
                    contact = -signs[index]*(1 if exits[index] else -1)
                    if phases[index] and phases[following]:
                        inward += int(contact == 1)
                        outward += int(contact == -1)
                    double10 += int(not phases[index] and not phases[following])
                    passive_owner = index if not exits[index] else following
                    other_owner = following if not exits[index] else index
                    if not phases[passive_owner]:
                        if phases[other_owner]:
                            positive01 += int(signs[passive_owner] == 1)
                            negative01 += int(signs[passive_owner] == -1)
                            passive01 += 1
                        else:
                            negative10 += int(signs[passive_owner] == -1)
                phase01, phase10 = sum(phases), length-sum(phases)
                assert 2*inward+phase10+2*positive01 == phase01+4+2*negative01+2*negative10
                assert phase01+4 <= phase10+2*passive01+2*inward
                assert inward+outward+phase10 == phase01+double10
                counts['words_with_10_to_10_contacts'] += int(double10 > 0)
                counts['words_requiring_passive01_correction'] += int(phase01+4 > phase10+2*inward)
                counts['mixed_words'] += int(0 < phase01 < length)
                accepted += 1
        by_length[str(length)] = accepted
    assert by_length == {'2': 1, '4': 28, '6': 495, '8': 8008}
    assert counts['words_requiring_passive01_correction'] > 0
    return dict(positive_turn_words_by_length=by_length, counts=counts,
                scope='Consistent cyclic type/activity words with signed turn4. '
                      'Not claims of embedded curves or complete feasible source fusions.')


def budget_controls():
    counts = Counter()
    for phase01, phase10, passive01, internal, external in itertools.product(
            range(9), range(5), range(5), range(9), range(5)):
        if internal > 2*phase10:
            continue
        for inward in range(internal+4*external+1):
            if phase01+4 > phase10+2*passive01+2*inward:
                continue
            deficit = max(0, phase01+4-phase10-2*passive01-2*internal)
            assert (deficit+7)//8 <= external
            assert phase01+4 <= 5*phase10+2*passive01+8*external
            counts['conditional_regional_and_global_budgets'] += 1
            for activation, boundary in itertools.product(range(3), range(3)):
                if passive01 > 2*activation+boundary:
                    continue
                assert phase01+4 <= 5*phase10+4*activation+2*boundary+8*external
                for unfilled, rotor in itertools.product(range(2), repeat=2):
                    doubled_reserve = activation+unfilled+rotor+boundary
                    if doubled_reserve % 2:
                        continue
                    reserve = doubled_reserve//2
                    assert phase01+4+4*unfilled+4*rotor+2*boundary <= (
                        5*phase10+8*external+8*reserve)
                    counts['conditional_shared_reserve_substitutions'] += 1
    return dict(counts)


def main():
    print(json.dumps(dict(status='PASS', words=word_controls(), budgets=budget_controls(),
                          region_adapter_controls=region_controls(),
                          complete_critical_U10_realizations=0,
                          complete_mixed_U_port_cycle_realizations_added=0,
                          scope='General mixed-cycle geometry and original occurrence packing '
                                'are written proofs. Finite words/arithmetic/rectangle controls '
                                'do not establish realizability, full allocation or grid equality.'), indent=2))


if __name__ == '__main__':
    main()
