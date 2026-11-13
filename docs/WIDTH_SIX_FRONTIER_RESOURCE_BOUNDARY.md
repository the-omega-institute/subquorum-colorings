# Width six: an exact small rectangle and the transfer boundary

13 November 2026. The five-row transfer proof does not extend by simply
changing the height bound to six. The old implementation materialises one
local kernel entry for every subset of a five-column window. At height six
this is (2^{30}) entries, about four GiB before the transfer table is
allocated. We replaced that materialisation by an on-demand optimized kernel
and an independent literal checker. This removes the artificial kernel
allocation, but the exact frontier itself still grows too quickly for the
existing state representation.

## Exact (6\times4) control

The standalone checker
[`check_grid_6x4_exact.cpp`](../scripts/check_grid_6x4_exact.cpp) evaluates
the definition directly on every subset of the (6\times4) board. It checks
formation for every omitted vertex, then checks every single deletion of every
forming set, so its `SF2` value is an exact finite result. It also checks the
dissociation condition directly. The run gives

\[
  \#\{S:S\text{ forms}\}=3{,}641{,}635,
  \qquad
  \#\{S:S\text{ is minimal and forms}\}=24{,}380,
\]
and

\[
  \boxed{SF_2(P_6\square P_4)=12=\beta_2(P_6\square P_4).}
\]

The complete search has (2^{24}=16{,}777{,}216) subsets. It used 18.2 MB
of resident memory and took 1.59 seconds on the local machine. The fixed
report is [`grid-6x4-exact-check.json`](../output/grid-6x4-exact-check.json).

The optimized frontier independently reaches `SF=12` at length four. Thus
the first width-six frontier value agrees with the literal whole-board
enumeration. This is a control for the transfer implementation; it is not a
proof for all widths or all lengths.

## On-demand transfer and independent cross-check

[`grid_star_compact_transfer_dynamic.cpp`](../scripts/grid_star_compact_transfer_dynamic.cpp)
computes the same local optimized rule as the five-row generator, but only
when a window is reached by an exact transition. The checker
[`check_grid_star_compact_dynamic.cpp`](../scripts/check_grid_star_compact_dynamic.cpp)
does not import that rule: it reconstructs local witnesses from the literal
three-vertex star definition and rebuilds every prefix independently.

As a regression, the dynamic generator and checker were run at height three
through length fifteen. They agreed at every prefix, including the complete
translated endpoint vector:

```text
height=3 length=15 SF=25 reachable=14726 mismatches=0
PASS height=3 start=12 period=3
reference height=3 length=15 states=14726 SF=25
status=PASS, complete_prefixes_rebuilt=15, endpoint_states=14726
```

The checker also compared 4,680 small-board subset acceptances, including 192
minimal sets. The height-three endpoint vector has period three and increment
five, as in the established strip theorem. These checks validate the new
on-demand plumbing against an already proved width.

## Resource boundary at height six

With the original 12,000,000-state guard, the dynamic frontier produced

```text
height=6 length=1 SF=4 reachable=64
height=6 length=2 SF=6 reachable=4096
height=6 length=3 SF=10 reachable=136832
height=6 length=4 SF=12 reachable=7506432
```

It then exceeded the state guard while constructing the next frontier. The
peak resident memory was 746,340,352 bytes. Raising the guard to 50,000,000
does not produce a certificate: the fixed packed table reaches its 2^25-slot
allocation limit after the same (n=4) layer, with a 745,275,392-byte peak
and a 6.73-second run. These are measured limits of this exact transfer
implementation, not mathematical counterexamples and not evidence that a
width-six theorem is false.

The next algorithmic step would need a genuinely smaller state quotient or a
profile argument that proves eventual translation without storing the whole
frontier. Merely increasing the local-kernel memory or the state cap does not
provide that proof. The general width-six equality and the arbitrary
width-six unit-weight improvement therefore remain open after this run.

## Reproduction

From the repository root:

```sh
clang++ -std=c++20 -O3 scripts/check_grid_6x4_exact.cpp -o /tmp/check-grid-6x4
/tmp/check-grid-6x4 output/grid-6x4-exact-check.json

clang++ -std=c++20 -O3 scripts/grid_star_compact_transfer_dynamic.cpp \\
  -o /tmp/grid-star-dynamic
clang++ -std=c++20 -O3 scripts/check_grid_star_compact_dynamic.cpp \\
  -o /tmp/check-grid-dynamic
/tmp/grid-star-dynamic 3 15 output/grid-height-three-dynamic-20261113
/tmp/check-grid-dynamic 3 12 3 5 output/grid-height-three-dynamic-20261113
```

The finite (6\times4) enumeration and the height-three cross-check are
verification evidence. The only general conclusion in this note is the
resource diagnosis for the tested transfer representation.
