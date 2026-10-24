# Two distinct slots pay every unactivated nonexceptional double

20 October 2026. In the complete U/rotor model, every nonexceptional
double-marked positive with neither terminal activated has two actual
defect slots, with no reuse between sources or between witness types.
The first one-reserve failure is reduced to two positives each with
exactly one activated terminal and no nonfull defect tile. This proves
joint allocation for an arbitrary number of nonexceptional sources when
at most one double has exactly one activation. The unrestricted mixed
allocation and rectangular-grid triple equality remain open.

## 1. Model and quantitative statement

Keep complete sources, original endpoint ownership, the original unions
P and M, mandatory retention of every original support outside P, and
final selected occupied degree at most one. All negative dimensions and
rotor phases are arbitrary. The actual canonical marks, terminal activation
occurrences and exact defect identity are the established definitions.
Nonexceptional positive dimensions are width6 at arbitrary permitted
independent even heights, or width8/10 with both heights in{4,6}.

Partition the nonexceptional DOUBLE-MARKED positives by how many of their
two original terminal singleton occurrences are activated. Let z,s,t
count zero, one and two activations, respectively. Let e count ACTUAL
double-marked exceptional positives, and let n0 count all unmarked
positives. Other one-mark positives can occur in arbitrary number.

Keep the exact geometric identity

    D=2R=A+U0+Z0+H,
    H=L1+2L2bar+2L2mutual+L3.

**Compensation theorem.** The actual nonfull-tile defect pool has two
distinct slots for each of the z sources, while all positive activation
occurrences retain their separate A contribution. In particular

    H>=2z,
    D>=A+U0+Z0+2z>=2(z+s+t)-s.                    (1)

No A occurrence is spent a second time, and no half-area of a separate
bounding rectangle is added. Since n2=z+s+t+e, the original source ledger
and integer parity imply the following bound. Here R=S+C-Kirregular is
an integer by that ledger, not merely by D=2R.

    sigma >= n0+R-n2 >= n0-e-floor(s/2).           (2)

Thus joint allocation follows if e+floor(s/2)<=n0. In particular, if all
positive dimensions are nonexceptional and s<=1, it holds at EVERY reserve
value, for arbitrarily many zero-activation or two-activation doubles.
More generally s<=2n0+1 suffices when e=0. This is a sufficient class of
complete-source fusions, not a decomposition of arbitrary grid objects.

## 2. Every blank-gate marked tile is exactly an irregular pair

Normalize a marked positive canonical tile as

    u=(2,2), zeta=(2,3), x=(3,2), y=(3,3),
    positive anchor p=(3,1), positive guard q=(1,3).

Suppose u is finally blank. The established assignment gives at least
one endpoint in{x,zeta}. We now apply its source-role argument to EVERY
endpoint in that set, rather than to just one selected witness.

For either endpoint v, its original owner differs from the positive
owner. Since u is finally blank, it was blank in that original source.
The continuation opposite its other intratile neighbor would be p or q,
an endpoint of the positive source and therefore not its own endpoint.
Thus v is in its owner's X set. The complete rotor barrier and all-phase
X catalogue force phase11 U ownership, in an A or F role. In both cases
the original endpoint profile in this tile is EXACTLY{v,y}: an upper
corner2P0T or terminal2P1T. These are complete-source role facts, not just
the abstract local profile catalogue.

Both x and zeta cannot be endpoints. If their owners differ, their two
original pairs share y, contradicting original endpoint disjointness.
If their owners agree, either role's exact two-point original profile
would exclude the other endpoint. Hence exactly one of x,zeta is an
endpoint, its original owner also owns y, and there are only two final
endpoints in the tile.

The2P1T possibility is also impossible. Its original support is the other
corner in{x,zeta}. If retained, that corner has occupied neighbors y and
p or q. Final selected feasibility therefore forces it into P, contrary
to the preceding exclusion. Mandatory support retention is essential here.
The profile is consequently2P0T, and the nonfull tile is one L2bar defect.
Distinct canonical tiles give a distinct such tile for EVERY blank mark.

Thus blank marks have TWO units each in the exact defect identity. In
particular an L3 blank-gate tile allowed by a merely local profile table
has no complete-source realization under these assumptions. This refutes
that proposed complete-source extension, not the local table or the grid
target. The same argument excludes complete2P1T blank-gate realizations.

## 3. Short unactivated occupied gates have only phase11 tip owners

Consider a positive of width8/10 and heights4/6, with an unactivated left
terminal and an occupied marked left gate(2,2). Its selected original
support(a+1,1) forces f=(a+1,2) finally blank, hence absent from EVERY
original source's endpoints AND supports.

The established gate catalogue excludes phase10 without activation.
It permits a phase01 upper corner, or a phase11 tip with predecessor
down/bar right (longitudinal) or predecessor right/bar down (transverse).
Both phase01 corner orientations can now be excluded using the short leg:

- If the near leg runs down from the gate, its height h>=4 gives original
  endpoints in column2 from row2 through h+2, followed by its original
  beyond-tip support at(h+3,2). For a in{4,6}, f lies in this segment or
  is that support. Both violate its final blankness.
- If the bar runs down, its width v>=6 gives original endpoints in column2
  from row2 through v+1>=7, again containing f.

Therefore only the two phase11 tip forms remain. The argument is local
to the corresponding side and uses original supports as well as endpoints.

## 4. Two occupied unactivated gates force one exact common owner

Consider a nonexceptional double with zero activations and both gates
occupied. Width6 is excluded by its shorter/equal-side activation theorem.
Thus it has width w in{8,10} and heights a,b in{4,6}, with the tip forms
of Section3 on both sides.

Two distinct transverse owners overlap at(2,5), by their length-five
footprints. For a left longitudinal owner, the unactivated-tip clearance
is4<=h<=a-2, so a=6,h=4. Its original bar contains

    {5,6} x {2,...,v+1}, v>=6.                     (3)

Suppose the right owner is transverse, with incident height k>=4 and
width v'>=6. Its near stem lies in row2 from column w-k-1 through w-1.
Disjointness from the positive endpoint(2,1) gives k<=w-4. Its bar lies
in columns w-k-1,w-k and rows2 through v'+1. Since

    4<=w-k<=6,

the point(5,w-k) lies in both this bar and(3). These cannot be distinct
original owners. Reflection gives the other mixed case.

If both owners are longitudinal, both incident heights are4, and the
right bar contains{5,6}x{w-v',...,w-1}. The point(5,5) belongs to both
bars since w in{8,10} and v,v'>=6. Again distinct owners are impossible.
The common-owner classification excludes a mixed A/F form and gives
exactly an inverted U(w-2,4,4), with both positive heights equal to6.
It has the two distinct outside bar-corner tiles

    Q_left={6,7}x{2,3},
    Q_right={6,7}x{w-2,w-1}.                       (4)

Each has an original2P0T pair, and a corner forbidden by its retained
positive tip support. It is therefore a nonfull L2bar or L3 tile.

The short-leg injection's original corner reconstruction makes each
such forced tile exclusive to this one positive among forced witnesses.
Its eight-orientation lemma excludes sharing with ANY blank-gate canonical
tile. The two tiles in(4) are distinct for w>=8. Thus we obtain two
different actual slots, not two roundings of one defect subtotal.

## 5. A common physical pool and the count

Let B count all blank-gate marked sides, including sides of other positive
sources. Let Cocc count the z sources with both gates occupied. Section2
gives B distinct L2bar tiles, each with its two actual slots. Section4
gives two distinct forced tiles for each of the Cocc sources. All2Cocc tiles
are distinct across their original positive owners and avoid every one
of those B tiles, by the preceding geometric non-reuse lemmas. Reserve
one slot in each forced tile; its actual weight is at least one. Hence

    H>=2B+2Cocc.                                     (5)

Every one of the remaining z-Cocc sources has at least one blank marked
side, and different such sources choose different canonical tiles. Thus
z-Cocc<=B, so(5) proves H>=2z. This pays each zero-activation double once
with two units. It does not allocate the same L2bar's second slot to an
unrelated source or spend regular full-tile credit again.

Distinct source-labelled positive terminals give A>=s+2t. Substituting
this and H>=2z in the exact identity proves(1). Since2R is even,
2R>=2(z+s+t)-s implies R>=z+s+t-floor(s/2). The source census and ledger
give(2), proving the compensation theorem.

Whenever the criterion in Section1 holds, |T|+|M|<=mn/2 improves the
existing5/6 matching-coefficient bound by |M|/6 on this complete-source
class. General one-activation doubles, exceptional positive dimensions
and arbitrary-grid coverage remain open.

## 6. The only first-reserve candidate is two single activations

Assume all positive dimensions nonexceptional. Restrict a failing source
allocation to an actual endpoint component using the earlier complete-
source restriction lemma. If its reserve is1, its failure needs
z+s+t>=n0+2, while(1) gives2>=2z+s+2t. These integer inequalities force

    n0=0, z=0, s=2, t=0,
    A=2, H=U0=Z0=0.                               (6)

Thus only the A+A alternative from the original seventeen patterns remains.
Both double-marked positives have exactly one activated terminal. Every
original irregular pair and original phase11 U triple must be full, and
there are no blank-gate marked sides anywhere in the component. A negative
source allocation margin would still not refute actual ambient sigma.

The former A+L3 and L3+L3 cases are excluded by the universal two-slot
proof, not finite enumeration. Existence or impossibility of the remaining
connected A+A complete fusion is unresolved. There can still be arbitrarily
many one-mark sources, negative dimensions and full zero-defect tiles.

## 7. Verification scope

The companion checker reconstructs actual marks, source activation counts,
all blank tiles and both forced tiles in complete physical images. It
allocates labelled unit slots from the actual nonfull defect pool before
checking(5), so witness collisions fail before aggregate inequalities.
Separate all-parameter written role arguments above are exercised by
finite blank-role and two-gate controls; incomplete role pairs are never
reported as complete feasible fusions. These controls cannot decide the
remaining A+A case.

The Lean companion checks source-role ownership implications, universal
corner/short-leg and crossbar inequalities, finite physical-slot injection
cardinality, the shared weighted count and parity, the sufficient all-
reserve class and the exact A+A remaining census. Complete source-role
normalization and physical source/ledger adapters remain written. Local
execution and independent proof-review status are recorded separately.

Local execution PASS with Lean4.33.0: all16 declarations compile and
their individual axiom audits use only the standard propext,
Classical.choice and Quot.sound axioms, or no axioms. No sorryAx or
native_decide is used. The complete geometry-to-role and ledger adapters
are still written, as specified above; this is not end-to-end Lean
verification of an arbitrary grid. See the formal-check JSON receipt.

Physical controls PASS on664 complete images, with128 zero-activation
double occurrences,256 distinct assigned slots, and24 images containing
several such doubles. All4008 tested distinct two-gate role pairs collide;
147 blank-pair role controls exercise the local masks. The complete-image
fixtures contain ZERO blank-mark and ZERO single-activation-double images;
these branches are supported by the universal written arguments, not by
an unexercised test. The remaining A+A census is arithmetic, not a
physical realization or an impossibility proof.

Independent taskd0553d32 completed ACCEPT at04:06:57UTC, observed
gpt_6/pro,18634 characters, for the written blank-gate rigidity,
occupied-gate classification, two-witness non-reuse, all-reserve criterion
and only-A+A reduction under the supplied source/ledger/component
dependencies. Its original stream68434 ended with DONE and exit0 and
matches the task API response exactly. It did not execute code or Lean;
complete physical adapters remain written. The suggested count rename
Cocc distinguishes occupied-gate doubles from ledger credit C. See
output/unactivated-double-compensation-review.json.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
