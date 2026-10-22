# Two residual components can reach the same donor

23 October 2026. Written general construction and independent finite controls.
This note is subsequent to the one-sided allocation review request; that
request does not cover this new construction.

The statement "each deficient demand component can expose a usable interval"
does not imply that all components can be paid simultaneously. We realize the
failure in a feasible, completely frozen, uniquely matched grid, using legal
mixed-path continuation only at unpaid alpha demands. The two separate
continuation certificates reach the SAME interval resource. After both links,
the maximum allocation grows by one, not two. The target inequality remains
strictly true throughout.

## Construction for every even W>=8

Use relay_family(W,4,1,1) with its existing even column translation by2. Its
occupied columns lie between2 and10, and its endpoints between3 and9. Make
a second copy translated horizontally by10. The closest occupied sites of
the two copies are two columns apart; there are no new occupied-neighbour
edges. Therefore selections stay feasible, old complete freezing certificates
replay independently, and the endpoint graphs have disjoint unique matchings.

Use the single compact packet rows4..W+5, columns0..21. It is a union of
original physical tiles, includes all selected sites and all original
receivers, and has BB first and last columns. Count the union once:

    dimensions (W+2) by22,
    |T|=34, |M|=2W+16,
    S=9W-28, B=W+2, S-B=8W-30>0.                           (1)

This is one physical packet. The old padded crop rectangles overlap and are
not separate budgets that may be added under the union's new occupied set.

Let C initially contain only the link (5,5)--(5,6), in the left copy. It
moves that alpha's upper free terminal to(5,7). Its other terminal is(W+4,5).
The right alpha's free terminals are(5,15),(W+4,15). Each of these four tips
has BP columns on both sides, hence no direct or selected-cap access. There
are two alpha demands, zero beta credit and no incident interval resource:
two isolated deficient demand components.

There are two possible further links, with disjoint endpoints:

    left extension:  (5,7)--(5,8);
    right extension: (5,15)--(5,14).

Both are unit horizontal opposite-kind original-terminal adjacencies. The left
link joins the unpaid alpha to the mixed gate with TP(5,9), BP(5,8). The
right link joins the other unpaid alpha to the mixed gate with TP(5,13),
BP(5,14). Thus each step transfers an unpaid alpha demand, leaving all other
strands unchanged and producing no beta credit.

## The same physical resource is reached

After the left extension, TP(5,9) uses the selected cap(5,10) and reaches BB
column11 in the band rows4,5. After the right extension, TP(5,13) uses the
selected cap(5,12) and reaches that VERY SAME BB column11 in the same band.
Both caps have their selection in the TP endpoint's physical row.

The BB11 interval is a singleton: its neighbouring columns10 and12 are BT.
It is unmarked because the packet boundaries are columns0 and21. Every other
free alpha tip remains blocked by BP columns. Consequently:

| Continuations added | Resources incident to demands | Maximum paid | Unpaid |
| --- | --- | --- | --- |
| neither | none |0|2|
| left only | BB11, owned by left demand |1|1|
| right only | BB11, owned by right demand |1|1|
| both | ONE BB11, owned by both demands |1|1|

With both extensions, the resource graph is exactly two demand vertices joined
by one edge resource. The two formerly separate deficient components merge
into one deficient tree; they do not both disappear. The complete two-demand
set with its one-resource neighbourhood is the Hall witness. The general
two-owner allocation theorem proves the maximum is exactly one.

Thus two individually valid donor certificates are insufficient without
distinct resource identities. No terminal, cap or mixed owner has been reused;
the failure is reuse of the common interval's UNIT CREDIT. It persists even
when continuation is restricted to unpaid demands, so that restriction alone
does not establish a full allocation theorem. At W=8 the physical packet is
10 by22, S=44, B=10, margin34; this is a rule counterexample, not a target
inequality counterexample.

## Verification and remaining question

The permanent checker verifies all even W=8..40, independently checks complete
freezing and unique matching, retains physical receiver closure, and computes
all four continuation states using the full candidate-incidence relation and
an independent maximum-matching algorithm. It checks equality of the physical
interval owner in both individual certificates and in their simultaneous
realization. The coordinate argument above proves the unrestricted statement.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_shared_donor_collision_after_mixed_relays.py --output output/shared-donor-collision-after-mixed-relays-validation.json

The next sufficient condition must control the joint neighbourhood of deficient
components, or supply a concrete augmenting allocation that retains distinct
resource identities. Individual reachability does not supply that condition.
No general grid equality, universal5/6 improvement, or manuscript revision is
claimed here. This construction has not received a separate external review.
