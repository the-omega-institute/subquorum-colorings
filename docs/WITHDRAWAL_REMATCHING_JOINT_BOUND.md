# Joint guard withdrawal and arbitrary rematching: a sharp global compensation theorem

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The subsequent [two-guard merger theorem](LOWER_GUARD_MERGER_FRONTIER.md)
also permits arbitrary lower-guard withdrawals without increasing the sharp
frontier, treats the resulting seven-site and cyclic thirteen-site regions,
and proves a local guard-retention implication under complete freezing.

The exact guard-withdrawal frontier survives arbitrary rematching of the old
endpoints. We prove this directly from occupation and the actual matching at
the boundary of one fixed pocket. Restoring the old matching is unnecessary;
the theorem includes completely frozen configurations for which that restoration
is impossible. The resulting signed exterior cut also gives an injective global
allocation of actual original-tile half-unit resources, paying exterior debts
before the net strip deficit and leaving the sharp remaining margin.

## 1. Exact statement

Let k>=2 and let (T0,M0) be the original b=1 family on the 6-by-(6k+4) board,
with P0=V(M0), |T0|=8k+5 and |P0|=8k+2. Its coordinates are fixed in the
[sharp-completion note](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md).
For ANY J subset of {0,...,k-2}, q=|J|, put

    g_i=(3,9+6i),    R=T0 minus {g_i:i in J}.

Suppose T,P are disjoint, R is a subset of T, P0 is a subset of P, every
selected site has at most one occupied neighbour, and M is ANY grid matching
whose endpoint set is exactly P. The old edges need not be retained; their
rematching and the addition of arbitrary new endpoints may occur simultaneously
with the guard withdrawals. Then

    |T|+|M| <= 17k+12+q = area/2-(k-q).                 (1)

For EVERY J equality is attained by the completely frozen construction in the
[joint withdrawal note](SELECTION_WITHDRAWAL_SHARP_STRIPS.md). Thus (1) is the
exact maximum, also after imposing complete freezing. No freezing assumption
is used for the upper bound. The sites allowed to be withdrawn may even be
selected again. The theorem permits only the specified old-T withdrawals and
retains every old endpoint site; other T/P deletions are outside its scope.

## 2. Count occupation across cuts, rather than calling crossing edges new edges

The forced-blank argument depends on retained R and P0, not on the mates of
the old endpoints. Hence all new T and new P still lie in the expanded free
graph classified in the preceding withdrawal note. It has the following
disjoint components, with no free-grid edge between different components:

- one fixed 15-site pocket A;
- q disjoint activated nine-site trees;
- k-1-q untouched two-site gates and k-1-q untouched four-site stars;
- k+1 isolated sites.

These sets exhaust 7k+10+3q sites. Removing g_i, c=9+6i, frees exactly
(3,c),(2,c),(3,c+1), which join the next gate and star. The former neighbour
(4,c) remains forbidden because the retained old selection (4,c-1) already
has an old endpoint neighbour. Consecutive guard withdrawals still produce
disjoint free trees. Every other old anchored T is unchanged, and the old
unanchored row-zero selections have no free neighbour.

Actual matching edges CAN cross from an old core to these free components.
For a free set C therefore define its contribution as

    w(C)=|T intersect C| + |(P minus P0) intersect C|/2.

Write newT=T minus R and newP=P minus P0. Since M matches exactly P,

    |T|+|M| = |R|+|P0|/2 + sum_C w(C)
             = 12k+6-q + sum_C w(C).                  (2)

Every endpoint is counted once in (2), regardless of which side of a cut its
mate occupies. Counting only new internal matching edges would be incorrect.

## 3. Activated trees have occupation capacity six

For one activated guard, c=9+6i, name the nine free sites

    d=(2,c),   g=(3,c),   b=(3,c+1),
    u=(2,c+2), v=(3,c+2), a=(4,c+1),
    s=(5,c+1), l=(5,c),   r=(5,c+2).

Their internal edges are dg,gb,bv,ba,uv,as,sl,sr. The old endpoint-neighbour
counts at g,u,v are respectively 1,2,1, and zero at the other six sites.
Let t_x be the new-T indicator, p_x the new-P indicator, and o_x=t_x+p_x.
These are occupation indicators; there is no assumption about any mate.
In particular t_u=0. The following inequalities follow from feasibility:

    t_g+o_d <= 1,           t_v+o_u <= 1,
    t_b+o_g+o_v <= 2,       t_a+o_b+o_s <= 2,
    t_s+o_l+o_r <= 2,
    t_d,t_l,t_r <= 1,       o_a <= 1.

The first two use the occupied old neighbours of g and v. The next three
are ordinary wedges: a selected centre cannot have two occupied neighbours.
Adding the nine displayed inequalities and t_u=0 gives EXACTLY

    sum_x t_x + sum_x o_x = 2 sum_x t_x + sum_x p_x <= 12.

Every indicator occurs once in this sum. Consequently w(tree)<=6 even when
some tree endpoints are matched into either neighbouring old core. This is
a general linear certificate, not a conclusion inferred from enumeration.

## 4. The fixed pocket has at most one half-unit of certificate slack

The pocket A is the same fixed 15-site set used in the
[endpoint-invasion proof](ENDPOINT_INVASION_SHARP_STRIPS.md):

    (2,3),(2,5); (3,3),(3,4),(3,5);
    (4,0),(4,2),(4,3),(4,4);
    (5,0),(5,1),(5,2),(5,3),(5,4),(5,5).

Its only possible matching-boundary vertices are U=(2,5) and V=(3,5).
The outside neighbours eligible to be endpoints are old P0 sites, since no
other free component touches A. Let e be the number of actual internal
matching edges; let x_U,x_V in {0,1} indicate an actual crossing at U,V.
Then |newP intersect A|=2e+x_U+x_V and t_U=0.

Use the eight weighted wedges of the earlier pocket proof, and add
3t_(2,3)<=3 and 3t_U<=0. Their right sides total 29. Expanding against
actual matching edges now gives

    3*(|newT intersect A|+e+x_V)+2h <= 29,             (3)

where h is the number of the five costly internal edges listed in that
proof. To verify (3), each T has coefficient three, each internal edge has
coefficient three or five, and the endpoint coefficients at U,V are ZERO
and THREE respectively. Thus the two possible crossings contribute 0*x_U
and 3*x_V. This boundary term is what changes under arbitrary rematching.

The integer z=|newT intersect A|+e+x_V satisfies 3z<=29, so z<=9. Hence

    2w(A)=2z+x_U-x_V <= 18+x_U-x_V <= 19.             (4)

We use the safe bound w(A)<=9+1/2. It is certificate slack, not a claim that
a local weight of 9+1/2 is achievable. Independent local controls in fact
find doubled maxima 18,17,17,18 for crossing flags 00,01,10,11; no part of
the proof depends on extrapolating those finite maxima.

## 5. The other components and the single global rounding

An untouched gate has upper site U with two old endpoint neighbours, so U
cannot be selected. Its lower site V has an old endpoint neighbour, giving
t_V+o_U<=1. Together with o_V<=1 this yields 2w(gate)<=2, without a boundary
matching assumption.

An untouched star has NO eligible old endpoint neighbour. Since it has no
free neighbour outside itself, its endpoint set is closed under the ACTUAL
matching. There is at most one internal matching edge. With that edge at
most two sites are selected; with no edge at most three are selected. Thus
w(star)<=3. Likewise an isolated free site has no possible matching partner
and contributes at most one. Closure is used for these components only.

Sum the distinct component bounds:

    2 sum_C w(C) <= 19+12q+8(k-1-q)+2(k+1)
                  = 10k+13+4q.

By (2),

    2*(|T|+|M|) <= 34k+25+2q
                 = 2*(17k+12+q)+1.

The left side is even. ONE global integer rounding proves (1). There is
only one fixed pocket; no half-unit loss is repeated per activated tree.
It would not be valid to round arbitrary fractional contributions separately
and then sum their rounded bounds. The exact all-subset frozen attainer
already established in the preceding note completes the sharpness proof.

## 6. Actual physical compensation for every matching, without reusing credit

Partition the board into its ORIGINAL aligned 2-by-2 tiles Q. Define the
integer half-unit charge

    c(Q)=4-2|T intersect Q|-|P intersect Q|.

All top two-row occupation is unchanged by the hypotheses, so the sum of
charges on that strip is 1-k, regardless of the actual mate map. The sum
over the whole board is exactly twice its surplus. By (1), therefore,

    sum_(Q outside strip) c(Q) >= 3k-1-2q.             (5)

Let Cplus=sum max(c(Q),0) and Cminus=sum max(-c(Q),0), both over exterior
tiles. These are sums over DISTINCT physical tiles, including all negative
exterior receivers. Inequality (5) is equivalently

    Cplus >= Cminus+(k-1)+2(k-q).                     (6)

For each positive tile make c(Q) separate tokens (Q,j), 0<=j<c(Q). First
list a demand for every negative exterior half unit, then k-1 demands for
the net strip deficit. Order these finite lists and assign demand number j
to positive token number j. Inequality (6) proves this assignment exists,
is injective, and leaves at least 2(k-q) unspent half tokens. No allocated
token is also counted as remaining credit. In particular, positive exterior
charge is not all treated as free strip compensation while its own negative
receivers are ignored.

This is a global original-tile compensation lemma for EVERY configuration
in the theorem, with arbitrary actual rematching. It assigns net charge;
it imposes no distance or direction restriction and does not claim an
individual routing rule for every raw D4 demand. Nor does it claim that the
remaining half tokens always occupy k-q distinct whole-unit reserve tiles.
For the explicit sharp attainers the stronger original successor-tile map
from the prior note DOES supply those distinct whole-unit reserves. At
q=k-1 the general theorem retains one whole unit, while the unchanged strip
has arbitrarily negative surplus (1-k)/2.

## 7. Scope, controls, and formal verification

The old [one-guard frozen obstruction](SELECTION_WITHDRAWAL_SHARP_STRIPS.md#6-one-withdrawal-can-also-make-old-edge-normalization-impossible)
retains P0 but has an isolated new endpoint, so its occupation cannot be
normalized to retain M0. It satisfies the hypotheses here and is explicitly
checked. Thus the enlarged theorem genuinely includes the failure case of
the earlier normalization method. That construction is not a counterexample
to (1) or to the half-area target.

The standard-library verifier independently checks all feasible occupation
patterns of the nine-site tree and all partial internal matching/local-T
patterns of the 15-site pocket with each of the four boundary flags. On
actual boards it checks the free graph and all boundary possibilities,
random alternating-path rematchings, explicit simultaneous withdrawals and
noncanonical core matchings, the fully frozen normalization obstructions,
and the sharp frozen attainers with their successor payments. It constructs
the global token assignment from actual original-tile charges in every
board model and checks exterior debts, injection and remaining credit.
Guard subsets are exhausted through k=6; representative boards reach k=128.
These computations check the general proof, and do not replace it.

The recorded run passes 3,941 independent tree occupations and 147,297 pocket
models; 815 board models include 391 that do not retain the old edges, 112
sharp frozen attainers, and 15 frozen normalization obstructions. The 815
global physical allocations pay 1,098 exterior-negative half tokens and
6,019 net strip half demands, leaving 19,518 distinct unspent half tokens.
The 112 sharp attainers also pass the stronger original successor-payment
map, with 583 reserve conversions and 1,222 unspent whole-unit original tiles.

Lean 4.33.0 checks 18 declarations covering anchored-pair/wedge arithmetic,
the occupation-only tree identity and capacity, boundary-aware pocket
arithmetic, gate/star bounds, arbitrary-k/q aggregation and the SINGLE global
rounding, sharp slack and margin, the signed exterior cut, token capacity,
injective token allocation and unspent half-token margin. No sorry,
native_decide or new axioms are used. The all-k coordinate classification,
matching adapter for the pocket certificate, global geometric partition,
charge adapter and the inherited frozen attaining construction remain
general written proofs with executable checks, not an end-to-end formal
grid theorem.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_withdrawal_rematching_joint_bound.py --output output/withdrawal-rematching-joint-bound-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_withdrawal_rematching_joint_bound_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/withdrawal-rematching-joint-bound-formal-validation.json

Next is a geometric cut beyond this retained-P0 strip family: other old-T/P
withdrawals, multiple interacting exceptional pockets and direction-constrained
individual payments. The universal improvement of the 5/6 bound remains open.
The submitted 11 October manuscript, public main/PR3, shared CI, C4 work and
correspondence are preserved. This stage performs no Mail operations.
