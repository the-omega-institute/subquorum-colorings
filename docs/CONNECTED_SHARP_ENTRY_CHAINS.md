# Connected sharp entry chains with arbitrarily many flexible blocks

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. Result and consequence for compensation

The bound 2f<=j from FLEXIBLE_BLOCK_ENTRY_REDUCTION.md remains sharp even
when arbitrarily many flexible matching blocks lie in ONE connected endpoint
component. Here f counts flexible allowed-edge blocks and j counts endpoints
of occupied degree four. For every positive integer k we construct a feasible
exchange-terminal pair with

    |P|=16k, |T|=8k+2, |M|=8k, f=k, j=2k,

exactly 2^k perfect matchings, and no occupied-degree-four endpoint in any
forced block. Each of the k flexible blocks is a square. Thus neither endpoint
connectivity nor having many flexible blocks forces an additional degree-four
event in the intervening forced network. Compensation cannot budget such an
event merely from these structural conditions.

This strengthens the separated-copy family in SHARP_TWO_ENTRY_BLOCKS.md.
It does not assert positive receiver charge, a minimum-size construction,
or a new global grid inequality. It excludes a candidate source of extra
compensation, not the target half-area bound.

## 2. Construction and complete interaction geometry

Use exactly the core P_0,T_0 and six forced pairs of SHARP_TWO_ENTRY_BLOCKS.md.
For self-containment, P_0 consists of

    (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
    (2,2),(2,3),(2,4),(2,5),(3,2),(3,3),(3,5),(4,1),(4,2),(4,3),

and

    T_0={(0,1),(0,3),(0,6),(1,0),(1,7),
         (3,6),(4,0),(4,5),(5,1),(5,3)}.

For 0<=i<k let v_i=(-3i,6i). Translate both sets by v_i, take the union
of endpoint sets, and retain exactly the old selections outside that union:

    P=union_i(P_0+v_i), T=(union_i(T_0+v_i)) minus P.

The matching is any independent choice of the two core square matchings,
together with every translated forced pair. To place the construction on an
even rectangular board, translate everything down by
s=2ceil(3(k-1)/2) and use (s+6) rows and 6k+2 columns.

There is no interaction between copies whose indices differ by at least two:
their occupied column intervals [6i,6i+7] have a gap of at least four columns.
For adjacent copies translate back to i=0. The complete occupied intersections
are

    T_0 intersect P_1={(1,7)}, P_0 intersect T_1={(1,6)},
    P_0 intersect P_1=T_0 intersect T_1=empty.

The only endpoint edge between copies is (1,6)--(1,7). Its endpoints are
the right endpoint r=(1,6) of copy0 and the left endpoint l=(4,1) of copy1.
The only old selections consumed are the right support (1,7) of copy0 and
the left support (4,0) of copy1, translated to the displayed coordinates.

For an exhaustive check of possible new adjacencies, the ordered pairs
(old occupied site, next-copy occupied site), excluding coincident sites,
are precisely

    (0,6)--(1,6), (1,5)--(1,6), (1,6)--(1,7),
    (1,7)--(2,7), (1,7)--(1,6), (1,7)--(1,8).

This follows by checking only columns6,7 of the first occupied footprint
and columns6,7 of the next: these are the sole overlapping columns, with
adjacency also reaching the neighboring columns5,8. The displayed lists
give all row possibilities. In this ordered list either the next-copy site
was already occupied in the first copy, or the first site is its consumed
selection (1,7). Reversing copy roles gives the same conclusion. Therefore
no native endpoint or retained selection acquires a new occupied neighbor.
Every endpoint keeps its original occupied degree, and every retained
selection keeps its single occupied neighbor. This proves feasibility.

There are16k distinct endpoints and10k distinct old selections. Exactly
two selections are consumed at each of the k-1 interfaces, at distinct
sites, so |T|=10k-2(k-1)=8k+2. Each core has exactly two degree-four
endpoints, a=(1,3) and c=(2,3). All other endpoints retain degree three.

## 3. Classify every perfect matching without enumeration

Every inter-copy endpoint edge is a bridge. Removing the interface after
copy i separates16(i+1) endpoints from16(k-i-1) endpoints. A matching can
cross an even vertex cut only an even number of times, whereas this cut
has exactly one available crossing edge. Consequently NO perfect matching
uses any interface bridge.

Every perfect matching restricts independently to each core. In a core,
successively deleting the leaf pairs

    (1,1)--(1,2), (1,6)--(1,5), (3,5)--(2,5),
    (4,1)--(4,2), (4,3)--(3,3), (3,2)--(2,2)

leaves exactly the square a=(1,3),b=(1,4),c=(2,3),d=(2,4). It has just
the matchings ab,cd and ac,bd. Thus the whole endpoint graph has exactly
2^k perfect matchings, six forced blocks and one flexible square per copy.
The bridge chain connects the internally connected core graphs, so there
is one endpoint component. In particular f=k,j=2k, and all12k forced-block
endpoints have occupied degree three.

## 4. Uniform two-stage freezing for every matching choice

For a fixed matching m, an endpoint can be frozen when it has two distinct
neighbors which are retained selections or mates of earlier frozen endpoints.
Both witnesses then persist in every feasible promotion bundle: a selection
is never deleted, and deleting m(z) requires promoting the already excluded
endpoint z. A first-promoted induction therefore excludes mixed bundles too.

Here is a complete eight-step PREFIX in each core. It uses neither port
selection (1,7),(4,0). Rows are read from top to bottom. H denotes ab,cd;
V denotes ac,bd. The first, second, third, seventh and eighth rows agree.

| Step | H endpoint; witnesses | V endpoint; witnesses |
|---|---|---|
| 1 | (1,1); (0,1),(1,0) | same |
| 2 | (3,5); (3,6),(4,5) | same |
| 3 | (1,3); (0,3),(1,2) | same |
| 4 | (1,5); (1,4),(2,5) | (2,2); (1,2),(2,3) |
| 5 | (2,4); (1,4),(2,5) | (2,4); (2,3),(2,5) |
| 6 | (2,2); (1,2),(2,3) | (1,5); (1,4),(2,5) |
| 7 | (3,3); (2,3),(3,2) | same |
| 8 | (4,2); (3,2),(4,3) | same |

Each nonselected witness is the mate of an endpoint in an earlier row.
Thus all copies can execute their chosen prefix simultaneously, regardless
of their neighbors' square choices. Crucially, the mates (1,5) of r=(1,6)
and (4,2) of l=(4,1) are both frozen by the end of this stage.

Every original port selection is now persistent. If not consumed, it is
still a selection. If consumed, it is precisely a neighboring copy's l or r,
whose matching mate has just been frozen. This conclusion assigns no donor
capacity; it is only a statement that these occupied sites cannot be deleted.

Finish each copy by the following eight rows, using all its original support
sites as persistent witnesses. Again each non-support witness is the mate
of an earlier frozen endpoint, in this stage or the prefix.

| Step | H endpoint; witnesses | V endpoint; witnesses |
|---|---|---|
| 9 | (1,6); (0,6),(1,7) | same |
| 10 | (4,1); (4,0),(5,1) | same |
| 11 | (4,3); (4,2),(5,3) | same |
| 12 | (3,2); (3,3),(4,2) | same |
| 13 | (2,3); (2,2),(3,3) | same |
| 14 | (1,4); (1,5),(2,4) | (1,2); (1,3),(2,2) |
| 15 | (1,2); (1,3),(2,2) | (1,4); (1,3),(1,5) |
| 16 | (2,5); (1,5),(2,4) | same |

These tables freeze all16k endpoints under ANY of the2^k matching choices.
They use at most sixteen synchronous freezing rounds, independent of k:
each row can run in every copy at once; a consumed support used after row8
has its foreign mate frozen by row8. This proves exchange terminality for
every k without enumerating the matching choices or promotion bundles.

## 5. Scope and validation

On the displayed even board the exact objective is16k+2 and the half-area
margin is

    (s+6)(3k+1)-(16k+2)=s(3k+1)+2k+4>0.

Thus this family does not contradict the grid bound. No positive-demand
sharpness is claimed. It shows that an extra degree-four forced endpoint
cannot be charged even after imposing endpoint connectivity and allowing
arbitrarily many flexible blocks. A physical payment proof for the interface
ledger must obtain its resources elsewhere and retain shared-tile corrections.

The verifier passes314models,72224physical certificate rows,254independently
enumerated matchings,128phase/symmetry images and960image matching checks.
It covers all square assignments through k=7 and twelve mixed patterns at
each of k=8,16,32,64,128. These finite checks supplement the arbitrary-k proof.

ConnectedSharpEntryChains.lean passes9theorems/9individual axiom audits:
both finite core tables, their coverage and partner involution, prefix port
mates and occupied degrees, generic rank-certificate induction excluding
promotion bundles, and count/board arithmetic. The all-k physical geometry
and matching-classification adapters remain written proofs. The separate
bounded-height source adds8arithmetic theorems, with its own stated scope.

The complete written diagonal-chain proof receives independent ACCEPT from
Oracle taskf67a299f-c9b0-46c2-acfa-5eae17f43345,actualgpt_6/pro,completed
22October09:04UTC. The review checks both tables and all-k geometry/matching
arguments, without executing code or Lean. It does not cover the subsequently
developed bounded-height variant. Exact scopes and provenance are in
output/connected-sharp-entry-review-accepted.json and
output/connected-sharp-chains-formal-check.json.
The submitted manuscript, public main and shared CI remain unchanged.

See BOUNDED_HEIGHT_SHARP_ENTRY_CHAINS.md for the further height10construction
and the exact3k+3synchronous freezing-depth theorem.
