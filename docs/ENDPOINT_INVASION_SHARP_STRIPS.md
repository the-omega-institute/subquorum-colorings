# Sharp compensation survives arbitrary retained endpoint additions

26 October 2026. Wenlin Zhang and Haobo Ma. Research continuation.

The preceding [sharp completion theorem](FROZEN_STRIP_SHARP_COMPLETION_AND_RESERVES.md)
fixed every endpoint. We now allow arbitrary additional actual matching edges,
including edges that occupy its previously unused physical reserves. The sharp
whole-board inequality survives. A second result localizes every completely
frozen new edge to a fixed 15-vertex region, independent of strip length. An
explicit frozen extension consumes one old reserve and replaces it in a different
original tile. These are results for this specified family; the general geometric
compensation problem and universal improvement of 5/6 remain open.

## 1. The retained-extension theorem

Let k>=1 and let (T0,M0) be exactly the b=1 configuration on the 6-by-(6k+4)
board defined in Section 1 of the preceding note. Thus |T0|=8k+5,
|M0|=4k+1. An extension (T,M) is required to satisfy:

1. T0 is a subset of T, and M0 is a subset of the actual matching M.
2. M is a grid matching, P=V(M), and T and P are disjoint.
3. Every t in T has at most one grid neighbour in T union P.

There is no bound on how many additional edges may be attempted and no freezing
assumption in the counting theorem. Then

    |T|+|M| <= 17k+12 = area/2-k.

This is sharp, including among completely frozen extensions with a genuinely
new actual matching edge. The top strip remains exactly unchanged, so its
surplus is still (1-k)/2. For k>=2 it remains a negative occupied strip even
at the true maximum over ALL such retained endpoint additions.

Keeping T0 and M0 is essential to the present proof. In particular the theorem
does not permit withdrawing old selections, deleting old edges, or rematching
their endpoints. Unlike the earlier fixed-P bound, it does not allow arbitrary
reselection of T0.

## 2. The exact graph available for new occupancy

Call an old selection anchored if it has an old P0 neighbour. Every other
neighbour of that anchored selection must remain blank, even if we try to add
an endpoint instead of a selection. Delete old occupied sites and all these
forced blanks; call the remaining set F. Every new selection and every new
endpoint lies in F. A new matching edge has both ends in F, since every old
endpoint is already matched by its retained old edge.

For completeness the exact row description of F is below. Every i in a set
expression ranges from 0 to k-1:

| Row | Free columns |
| --- | --- |
| 0,1 | none |
| 2 | {3} union {5+6i} |
| 3 | {3,4} union {5+6i} |
| 4 | {0,2,3} union {4+6i} |
| 5 | {0,1,2} union {3+6i,4+6i,5+6i,7+6i} union {6k+3} |

This table follows directly by taking the old occupied sites listed in the
preceding note and deleting the other neighbours of each anchored old T.
The only unanchored old selections are the row-0 bridge sites (0,3+6i);
none has a neighbour in F. Thus there is no additional omitted old-selection
constraint coupling the free components. The table also proves that no new
occupancy is possible in the top two-row strip.

The induced grid graph on F has the following components, with no edges between
different components:

* A fixed pocket A of 15 vertices:

      (2,3),(2,5);
      (3,3),(3,4),(3,5);
      (4,0),(4,2),(4,3),(4,4);
      (5,0),(5,1),(5,2),(5,3),(5,4),(5,5).

* For i=1,...,k-1, a gate pair (2,5+6i)--(3,5+6i).
* For i=1,...,k-1, a three-leaf star with centre (5,4+6i) and leaves
  (4,4+6i),(5,3+6i),(5,5+6i).
* k+1 isolated sites: (5,7+6i) for i=0,...,k-1 and (5,6k+3).

The coordinate table proves both exhaustion and separation: the horizontal
gaps between the repeated groups exceed one, and their only possible vertical
adjacencies are the displayed gate or star edges. In total |F|=7k+10.
This is a classification for every k, not a conclusion drawn from testing a
finite list of board lengths.

Write q(H)=number of new T in H + number of new matching edges in H.
Each new edge belongs to exactly one component. Gate upper sites have two
old P neighbours, so cannot be selected. With no gate edge only the lower
site can be selected; with the gate edge neither site is selected. Hence
q(gate)<=1. A star has at most one matching edge; with that edge only two
other leaves remain available for selection. With no edge at most three sites
can be selected, since selecting all four violates feasibility at the centre.
Thus q(star)<=3. An isolated site contributes at most one.

It remains to prove q(A)<=9. The next section supplies a short universal
inequality, including its exact incidence accounting.

## 3. A weighted certificate for the 15-vertex pocket

For v in A let t_v indicate a NEW selection, let m_e indicate a NEW actual
matching edge in A, and set

    o_v = t_v + sum_(e incident with v) m_e.

Matching and disjointness make o_v precisely its new occupancy indicator.
For distinct neighbours a,b of v in A, feasibility implies the wedge inequality

    t_v + o_a + o_b <= 2.                       (W)

Indeed if t_v=0 the two indicators sum to at most two, and if t_v=1 at most
one of its neighbours can be occupied. Also t_(2,3)<=1 and t_(2,5)=0; the
latter site sees the two old endpoints (1,5),(2,6).

Use (W) at these triples with the stated positive integer weights:

| Weight | Centre v | Neighbour a | Neighbour b |
| --- | --- | --- | --- |
| 2 | (3,4) | (3,3) | (3,5) |
| 1 | (3,4) | (3,5) | (4,4) |
| 2 | (4,2) | (4,3) | (5,2) |
| 1 | (4,3) | (3,3) | (4,4) |
| 3 | (5,0) | (4,0) | (5,1) |
| 1 | (5,2) | (4,2) | (5,3) |
| 1 | (5,4) | (4,4) | (5,5) |
| 2 | (5,4) | (5,3) | (5,5) |

Add these eight weighted inequalities to 3t_(2,3)<=3 and 3t_(2,5)<=0.
The right side is 2*13+3=29. Expanding the left side gives EXACTLY

    3 sum_(v in A) t_v + 3 sum_(e in E(A)) m_e + 2 sum_(e in H) m_e,

where H consists of the five edges

    (3,3)--(4,3), (4,3)--(4,4), (4,3)--(5,3),
    (5,1)--(5,2), (5,2)--(5,3).

One can verify the identity simply by checking the 15 site coefficients and
17 edge coefficients: every site has coefficient 3; each edge has coefficient
3, or 5 precisely in H. Consequently

    3q(A)+2|M_new intersect H| <= 29,
    q(A) <= 9,                                  (integer rounding)

for every feasible local choice, however its matching or selected sites are
chosen. The certificate is a linear inequality proof, not exhaustive search.
Although wedge neighbourhoods overlap, their coefficients are all explicitly
accounted for. We never interpret two overlapping inequalities as two separate
physical donors. Each actual matching edge is counted once in q(A), and every
extra incidence has a nonnegative coefficient.

Summing the disjoint components now gives

    |T\T0|+|M\M0| <= 9+(k-1)+3(k-1)+(k+1) = 5k+6.

Adding |T0|+|M0|=12k+6 proves the claimed 17k+12 bound.

## 4. Every completely frozen new edge stays in the first pocket

Here freezing is the actual inductive two-witness process used in the existing
validators: a witness is a retained T, or a P neighbour whose mate is already
frozen. In any finite complete freezing process give each endpoint its layer
as strict rank. A witness of v cannot be v's own mate: that mate is not T,
and to be an endpoint witness it would require v itself to have smaller rank
than v. Thus every frozen endpoint needs two distinct occupied neighbours
OTHER THAN its mate.

In each repeated gate i>=1, the lower site (3,5+6i), if matched upwards, has
only its mate and the single old endpoint (3,6+6i) as occupied neighbours.
The other two neighbours are forced blank by the table in Section 2. Hence
the lower endpoint can never freeze. A new star edge has a matched leaf with
only its mate as an occupied neighbour: none of the star sites has an old
occupied neighbour, and F has no additional adjacent component. That leaf can
never freeze either. Isolated sites cannot be matched.

Therefore every new edge of a COMPLETELY frozen retained extension lies in A,
and in particular there are at most floor(15/2)=7 new matching edges, regardless
of k. This bound is only a uniform localization bound; we do not claim it is
the exact maximum number of completely frozen pocket edges. Notice the first
gate (2,5)--(3,5) belongs to A and DOES have the extra possible support (3,4).
It is not excluded by the repeated-gate argument.

## 5. A sharp frozen invasion and physical reserve replacement

Take the periodic attaining T* from the preceding note, retaining M0. For every
k>=1 make this fixed patch:

    remove from T*: (3,3),(3,5),(4,0),(4,4),(5,3);
    add to T*:     (3,4),(4,3),(5,1),(5,4);
    add to M0:     (2,5)--(3,5).

Call the result (Tdag,Mdag). No removed selection is in T0, and the new edge
uses two old blank sites. In the affected region the selected-selected pairs
are now

    (4,3)--(4,2), (5,0)--(5,1), (5,4)--(5,5).

Their other neighbours are blank. The new selection (3,4) sees only its new
endpoint neighbour (3,5); the retained selection (2,3) is now isolated. Every
unchanged selection sees no additional occupied neighbour: the neighbours of
the new endpoints outside A are old P or forced blanks, and the boundary of
the changed patch has no other new occupied sites. This checks feasibility
for every k; the unchanged periodic suffix was already checked in the preceding
proof. The patch retains T0 and M0, so all old strict freezing witnesses remain
valid. After the old endpoints have frozen, (2,5) has the endpoint witnesses
(1,5),(2,6), whose mates are old frozen endpoints. The other new endpoint
(3,5) has T witness (3,4) and P witness (3,6), whose mate is old and frozen.
Both new endpoints therefore freeze, without circular use of the new edge.

The patch loses one selected site and adds one matching edge. Hence

    |Tdag|=13k+10, |Mdag|=4k+2, |Pdag|=8k+4,
    |Tdag|+|Mdag|=17k+12.

There is a genuinely new completely frozen edge at the true retained-extension
maximum. It occupies the first reserve tile Q_(1,2), where
Q_(a,b)={2a,2a+1} x {2b,2b+1}. The doubled physical surplus is

    c(Q)=4-2|Tdag intersect Q|-|Pdag intersect Q|.

Its exact exterior ledger is:

* The consumed reserve Q_(1,2) now has two new endpoints and T(3,4), so c=0.
* The DIFFERENT endpoint-free tile Q_(1,1) contains only T(2,3), so c=2.
  It replaces the consumed full unit.
* The remaining old reserves Q_(1,2+3i), i=1,...,k-1, still have c=2.
* The k distinct rebate tiles Q_(1,4+3i), i=0,...,k-1, still have c=1.
* Q_(1,0) still has c=-1. Every other exterior tile has c=0.

The internal C=1 still pays the boundary half-unit demand; the k original
half-unit rebates still pay the k D4 demands. After these payments, the
distinct full-unit tiles Q_(1,1) and Q_(1,2+3i), i>=1, remain unused. Their
number is k. In particular we do not keep counting the consumed Q_(1,2).
The exact sum is (1-k)+(k-1)+2k=2k in doubled units.

This is a physical replacement lemma for the displayed all-k invasion. The
general scalar theorem in Section 1 covers every retained extension; we do
not assert that every such extension has this same tile-by-tile payment map.

## 6. Verification and remaining scope

The standard-library validator checks exact free components, the integer
coefficient certificate, arbitrary sampled retained extensions, the fully
frozen attaining patch, actual strip budgets, and every physical tile charge.
It tests k=1,...,16,32,64,128, 96 random endpoint/selection completions and
24 isometries. The k=2 fixture has 36T/10M/20P, all endpoints inductively
frozen, strip surplus -1/2 and whole surplus 2.

Lean 4.33.0 verifies ten declarations: the universal feasible-wedge implication,
the strict-witness exclusion of the own mate, the mate-plus-one obstruction,
the pocket's edge geometry, exact weighted incidence identity, universal
pocket bound 9, gate/star capacity lemmas, and all-k count aggregation and
whole-surplus arithmetic. No finite set of pocket selections is enumerated
in the proof. The all-k grid classification, actual-configuration-to-incidence
adapter, frozen attaining pattern and physical tile relocation remain written
proofs with executable checks, not an end-to-end formal grid theorem.

    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_endpoint_invasion_sharp_strips.py --output output/endpoint-invasion-sharp-strips-validation.json
    PYTHONDONTWRITEBYTECODE=1 python3 develop/check_endpoint_invasion_sharp_strips_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/endpoint-invasion-sharp-strips-formal-validation.json

The next geometric issue is retaining enough of this decomposition when old
edges or selections may be withdrawn, or when another occupied band changes
the forced-blank graph. The present theorem settles arbitrary NEW endpoints
for the sharp negative-strip family under retained T0/M0. It leaves arbitrary
mixed-direction footprints, general shared-resource cuts and the universal
5/6 question open. The submitted 11 October manuscript and correspondence
are unchanged.
