# Boundary parity pays a single saturated export

8 October 2026. This strengthens the geometric occupied-band estimate in
[cross-component compensation](CROSS_COMPONENT_COMPENSATION.md). It also gives
the first Lean-checked grid-band compensation result in this research branch.
The unrestricted grid conjecture is still open.

## 1. The sharp surplus for every band length

Consider two rows of length w>=1, labeled T (selected), P (matching endpoint)
or B (blank). Assume each upper-row T has only B neighbors within the band,
each lower-row T has at most one occupied neighbor within the band, the upper
endpoints are not T, and the lower endpoints are B. At w=1 the two endpoint
conditions refer to the same column.

**Theorem 1 (parity-corrected blank surplus).** If t,b count T,B, then

    b-t >= 2 if w is even, and b-t >= 1 if w is odd.       (1)

Both constants are sharp for all positive lengths of their respective parity.

**Elementary proof.** No column has two T vertices. Associate each T whose
vertical neighbor is B to that B. All other T vertices are lower-row T with
an upper P. Their column indices form a nonconsecutive subset X of the
interior columns. Each neighbor of an X column has lower B and contains no
T: an upper T there would neighbor the upper P in X. The endpoint columns
also contain no T and supply a lower B.

If X is nonempty, split it into d maximal chains at successive distance two.
Their neighbor sets are disjoint and contain |X|+d columns. This supplies at
least |X|+1 extra B for any w. For even w, d>=2 supplies |X|+2; if d=1, the
neighbors have one parity and cannot contain both endpoints, so adjoining
the missing endpoint again supplies |X|+2. If X is empty, the endpoints
supply two different B for w>=2 and one B for w=1. These B are in columns
with no T and were not associated to the first group. This proves (1).

For odd w=2k+1, put P throughout the upper row and put lower T at odd
zero-based columns 1,3,...,2k-1, with B elsewhere. Then b-t=1. For even
w=2k, use lower T at 1,3,...,2k-3 instead; then b-t=2. All hypotheses hold.
These labelings have physical matching realizations: pair upper P consecutively;
for odd w, match the last upper P to an additional outside column. QED.

If a matching has mu internal edges and j edges leaving the band, then

    2w=t+b+2mu+j, so b-t has the parity of j.              (2)

Combining (1) with this equality gives the stronger, sharp bound

    b-t >= 2+(j mod 2),                  w even,           (3)
    b-t >= 1+((j+1) mod 2),              w odd.            (4)

In particular, an even-length band with an odd number of crossing matching
edges has surplus at least three. Matching edges to saturated tiles are part
of j. Omitting them would give the wrong parity.

## 2. Stronger compensation with the same geometric hypotheses

Use exactly the filled-source frame of Theorem 2 in the predecessor note.
Its upper tile region U has rho(U)=1. Its lower inner band S has even vertex
width, no matching endpoint in a saturated tile inside S, and the exact ledger

    rho(S)=-(b(S)-t(S))/2+sigma/2,

where sigma counts every matching edge from S to a saturated tile outside S.
Let p count edges from S to deficient tiles outside S. Thus j=p+sigma counts
all crossing matching edges, including any into U. Define eta=j mod 2.

**Theorem 2 (parity-enhanced source compensation).** Without assuming that
S is blank or closed under matching,

    rho(S) <= -1+(sigma-eta)/2,
    rho(U union S) <= (sigma-eta)/2.                     (5)

**Proof.** The same source frame enforces all label hypotheses of Theorem 1.
Substitute (3) in the exact ledger. U,S are tile-disjoint, so charges add.
Residual crossing edges are already split between their two deficient ends;
an edge into U is not an additional resource. QED.

This strictly extends the prior sufficient condition sigma=0. If sigma=1
and p is even, then j is odd and (5) pays the entire source despite its
one outward saturated attachment. More generally sigma<=eta suffices.
The new condition uses actual local edge counts and parity; it does not
assume a negative donor charge or a Hall allocation.

For pairwise tile-disjoint source patches A_i=U_i union S_i, let W be the
remaining deficient tiles. Then the exact partition gives

    q <= (sum_i sigma_i-sum_i eta_i)/2+rho(W).            (6)

Consequently, if each patch either has sigma_i=0, or has sigma_i=1 and an
even number of residual band exports, and rho(W)<=0, then

    |T|+|M| <= mn/2.

This replaces 5/6 by 1 on an unbounded geometric class allowing occupied
bands, capacity-two passages, and one saturated export per source patch.
The remainder condition and fixed source-frame hypotheses remain explicit.
This is not a universal coefficient improvement or an arbitrary bent-source
theorem. Disjointness supplies unique budget ownership; overlapping patches
cannot be added. Every eta is a correction to its own band's estimate,
not an independently reusable donor token.

## 3. Actual sharp one-export patches of arbitrary width

For k>=3 take the existing nested neutral-band equality construction
`nested_corridor(k,2)` on a 6-by-(2k+4) rectangle. Keep all selected vertices
and remove just the matching edge (3,3)--(4,3). Feasibility persists because
selected vertices only lose occupied neighbors. The objective decreases by one.

Let U be the upper tile row and S the inner k tiles of the next tile row,
physical rows2,3 and columns2,...,2k+1. The original S is neutral, with its
only crossing edges the two saturated attachments. It has t=0,b=2,sigma=j=2.
Removing the left attachment gives

    t=0,b=3,sigma=j=1,p=0,eta=1,
    rho(S)=-1,rho(U)=1,rho(U union S)=0.                 (7)

Thus the new one-export condition is physically realizable at every width
k>=3, and the new bound is sharp. The old bound rho(S)<=-1+sigma/2 would
only supply -1/2, insufficient by itself to pay this source. The remaining
deficient tiles have total charge -1; the full configuration has q=-1.
No target-grid counterexample is involved.

There is also a capacity-two version with arbitrarily many residual band ports.
For any l with 0<=l<=k, in each of the first l inner tile columns replace
the two horizontal matching edges in rows1,2 by the two vertical edges across
their interface. These disjoint plaquette flips preserve occupancy, feasibility,
matching size, all selected vertices and every tile charge. They introduce l
full capacity-two source passages and 2l actual residual edges from S into U.
Hence sigma=1,p=2l,j=2l+1 while (7) remains true, and both inequalities in (5)
are still sharp. This proves an unbounded family with occupied adjacent bands,
capacity-two junctions and residual crossings; the extra ports are counted
inside j and split by the regional ledger, never spent twice.

## 4. What Lean checks

`formal/SubQuorum/BandCompensation.lean` encodes the actual three labels in
each of nine column types. Its local compatibility predicate asserts exactly
the two T-neighbor conditions above, with blank sentinel columns at both ends.
Endpoint conditions are stated separately. A 162-state parity potential is
checked by ordinary `decide` in the Lean kernel, then telescoped by induction
over an arbitrary list of columns. This proves (1) for all lengths, not a
finite list of widths. Counting B and T is derived from those labels inside
Lean; it is not assumed as an opaque surplus inequality.

The matching-band theorem takes the actual vertex partition count as its
explicit matching interface and proves (3). The charge theorem takes the
stated regional charge identity and proves (5). The one-export theorem proves
nonpositive patch charge from sigma<=eta. The construction of an arbitrary
full-grid tiling, the geometric source-frame implication, and its regional
charge identity still have written proofs rather than Lean adapters.
The final general grid conjecture is not asserted as a formal theorem.

`formal/SubQuorum/EndpointCompensation.lean` separately models physical and
auxiliary matching as color-reversing involutions, the latter fixing terminals,
both preserving component ownership. It derives terminal color balance from
these matchings, then constructs injective allocations from one-color demands
to opposite-color supplies within each component. The injection uses finite
cardinality, not an assumed Hall condition or assumed terminal balance.
It combines those allocations into one map on all demand endpoints, proves
that this map preserves component ownership and reverses endpoint color, and
proves global injectivity. Thus the no-reuse conclusion is itself a Lean
theorem, including different components and different color fibers.
Its matching/ownership interface is explicit; conversion of every feasible
grid to this network is not yet formalized.

All these theorems are audited without `sorry`, `admit`, `native_decide`, or
new axioms. The potential discovery script only finds a candidate certificate;
the checked Lean proof is independent of Python's execution or truthfulness.
No shared CI workflow or protected manuscript is changed.

Independent controls check all 534 reachable local potential transitions,
all 26 terminal states, both starting states, and the exact Lean certificate
table. Eighty physical bands attain every stated width/crossing-parity bound
at widths1..40. At widths3..40, the base, one-flip and all-flip versions give
114 one-export source patches and 912 symmetry images satisfying the exact
charge equalities above. Source
hashes are archived in `output/band-parity-compensation-controls.json`.
The separate formal receipt `output/grid-formal-verification.json` records
the pinned compiler/dependencies, actual compiler output and theorem axioms.
