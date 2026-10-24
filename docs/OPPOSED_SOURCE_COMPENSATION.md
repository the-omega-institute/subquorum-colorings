# Two opposed sources share one receiver without reusing its budget

8 October 2026. This resolves a multi-source case excluded by the earlier
tile-disjoint one-source accounting. The geometric starting point was suggested
in the completed NyxID oracle follow-up955516e3. We independently prove the
result, formalize its band/counting consequences, and extend the suggested
closed-rail configuration to allow source-to-band matching edges. The general
grid inequality and arbitrary bent-source compensation remain open.

## 1. A four-spare-blank lemma

Let S be two aligned physical rows with L>=2 columns. Every vertex in its
upper row has an occupied neighbor immediately above S, and every vertex in
its lower row has an occupied neighbor immediately below S. Assume the two
vertices in each endpoint column are blank. Feasibility means every selected
vertex has at most one occupied neighbor. Write t,b for the selected and blank
counts in S.

**Lemma 1.** Under these hypotheses,

    b-t >= 4.

**Proof.** A selected vertex already has an occupied neighbor outside S, so
its vertical partner inside S is blank. Map every selected vertex to that
partner. This is injective: each vertex has a unique vertical partner, and a
column cannot contain two selected vertices. The four endpoint blanks are
outside the image, since their columns contain no selected vertex. Thus there
are at least t+4 blanks. This proves the result at every length, including
L=2. No matching or horizontal neighbor hypothesis is needed for this final
injection once the vertical implication has been derived. QED.

If mu matching edges are wholly in S and j have exactly one endpoint there,

    2L=t+b+2mu+j,
    b-t >= 4+(j mod2).                                    (1)

The second assertion follows because b-t and j have the same parity.
For aligned tile rows L=2w. A saturated tile in S has no matching endpoint:
two selected corners must be diagonal, since adjacent selected corners would
each have their external occupied neighbor and the other selected corner;
each remaining corner must then be blank. Therefore the existing regional
ledger applies without a saturated endpoint correction inside S:

    rho(S)=-(b-t)/2+sigma/2 <= -2+(sigma-(j mod2))/2,        (2)

where sigma counts all matching edges from S to saturated tiles outside S.
For completeness, with h within-tile matching edges in deficient S tiles,
the residual internal/crossing edge counts are mu-h and j-sigma, and
R(S)=2w-t-h-sigma. Substitution into
rho=C_inside+C_crossing/2-R gives (2). Every inter-region residual edge is
split equally between its two regions.

Thus two disjoint source regions U+,U- with rho(U+)<=1 and rho(U-)<=1 are
paid by this single band whenever sigma<=j mod2. This includes sigma=0 and
also sigma=1 with an even number of residual exports. These three regions
must be tile-disjoint. The band is inserted once with its stronger two-unit
estimate; two copies of a one-unit estimate would not justify the result.

## 2. Exact opposed fronts, allowing interacting matchings

Take w>=3, N=2w. The charged core is physical rows2,...,7, with upper source
U+ in rows2,3, receiver S in rows4,5, and lower source U- in rows6,7.
Use zero-based coordinates. The following source-frame hypotheses suffice:

- The upper source's selected vertices are (3,0),(3,N-1); its blank vertices
  are (2,0),(2,N-1). Its corners (2,1),(2,N-2) are matched upward to saturated
  tiles. For 1<=a<=w-2, prescribe matching edges (2,2a)--(2,2a+1).
- Every remaining vertex (3,c),1<=c<=N-2, is a matching endpoint. Its partner
  is otherwise unrestricted subject to overall feasibility and the frame.
- The lower source is the reflection row r -> 9-r of the upper source:
  selected endpoints are (6,0),(6,N-1), blank endpoints (7,0),(7,N-1),
  attachments leave downward, and its interior row7 matching edges are fixed.
  Its row6 matching endpoints have unrestricted partners.
- The receiver is arbitrary subject to feasibility. Saturated cap tiles
  supporting the four prescribed attachments are outside the core.

**Theorem 2.** Every feasible completion of this frame satisfies

    rho(U+)=rho(U-)=1,  sigma(S)=0,
    rho(S)<=-2-(j mod2)/2,
    rho(U+ union S union U-)<=0.                          (3)

**Proof.** Each source endpoint tile has t=1,h=0,s=1,r=0 and one residual
incidence, so its charge is1/2. Every interior source tile has four matching
endpoints, t=0,h>=1 and no saturated attachment. With r=2-h and d=4-2h,
its charge is0. Here full occupancy excludes saturated attachments because
an attachment to a saturated tile requires a blank companion on the adjacent
side. Thus each source charge is1 even if its front matches into S.

Every S vertex has an occupied external neighbor in its respective source
front. The four endpoint vertices of S face selected source endpoints which
already have an occupied lateral neighbor; they are consequently blank.
Lemma1 applies. A matching edge leaving S cannot leave horizontally through
these blanks. Its only vertical neighbors are source vertices in deficient
tiles, so sigma(S)=0. Equation(2) proves (3).

The entire core is residual-closed. Its only physical matching exits are
the four prescribed saturated cap attachments, which are not residual edges.
Side exit vertices are selected or blank, and the source backs are blank
or already paired internally or to the caps. Crossings between S and a source
remain inside the core. Consequently every maximum auxiliary decomposition
of the core satisfies

    n_LL(core) <= n_SS(core)+c(core).                    (4)

This is the exact residual-closed strand/charge identity, applied after (3).
It does not require switching one donor strand onto a debt strand. QED.

If front matching edges enter S, the individual source rows need not be
residual-closed and need not each decompose into one LL strand. Their local
charges still equal1. Only the closed core is used in (4). This distinction
prevents a silent source-port omission.

## 3. Sharp physical families and interacting variants

In the 10-by-N rectangle, put selected vertices at

    (3,0),(3,N-1),(6,0),(6,N-1),
    (0,1),(1,0),(0,N-2),(1,N-1),
    (8,0),(9,1),(8,N-1),(9,N-2).

For r in{3,4,5,6}, use edges (r,2a+1)--(r,2a+2),0<=a<=w-2.
For r in{2,7}, use edges (r,2a)--(r,2a+1),1<=a<=w-2.
Add attachments (2,1)--(1,1),(2,N-2)--(1,N-2),
(7,1)--(8,1),(7,N-2)--(8,N-2). All unspecified vertices are blank.

For every w>=3 these matching edges are disjoint. Each selected vertex has
exactly one occupied neighbor, so the configuration is feasible. S has t=0,
b=4 and j=sigma=0. Hence rho(S)=-2 and the core charge is0. In the receiver,
the two endpoint tiles have r=2,d=2 and one reserve each; interior tiles have
r=2,d=4. All maximum pairings give core counts n_LL=2,n_SS=0,c=2.
Each source's two leaf terminals have opposite checkerboard colors, so the
earlier monochromatic-demand criterion does not pay either isolated source.
The full rectangle has |T|=12,|M|=6w-4 and q=-4(w-2); it is not a target
counterexample. It witnesses equality of the core estimate.

Independently choose any subsets A+,A- of{0,...,w-2}. For each a in A+,
flip the two horizontal edges at rows3,4 and columns2a+1,2a+2 into the two
vertical edges. For a in A-, do the same at rows5,6. All plaquettes are
vertex-disjoint, even if indices in A+ and A- agree. Occupancy, matching size,
feasibility and every tile charge remain unchanged: each removed horizontal
edge crosses a tile boundary, and its replacement vertical edge crosses the
source/receiver boundary; every affected tile retains the same residual
degree and internal-edge count. Now

    j(S)=2(|A+|+|A-|), sigma(S)=0, rho(S)=-2,
    rho(core)=0.

The band contains arbitrarily many capacity-two tiles and has arbitrarily
many genuine inter-region edges. The two original positive source components
may now interact through S. Equation(3) remains sharp; the half-incidences of
each crossing are counted once at each end. Separate closed-source strand
arguments would no longer be valid, but aggregate accounting still is.

## 4. Disjoint packing and exact limits

In an even rectangle take any collection of pairwise tile-disjoint opposed
cores as above, allowing aligned translations, rotations and reflections.
Require disjoint supporting cap tiles as well. Let W be all remaining
deficient tiles. The cores are residual-closed, so W is also residual-closed.
If every residual component of W has monochromatic active zero-capacity
leaves, the earlier one-color theorem gives rho(W)<=0. Therefore

    q=sum rho(core_i)+rho(W)<=0, hence |T|+|M|<=mn/2.

The coefficient-one sufficient class now includes interacting pairs of
mixed-color sources sharing one occupied receiver. Each receiver belongs to
one packed core. No Hall inequality, donor allocation, or switch reachability
is assumed. This does not settle staggered/overlapping fronts, arbitrary bent
sources, or a universal improvement of5/6.

## 5. Formal verification and provenance

`formal/SubQuorum/OpposedBandCompensation.lean` checks actual T/P/B columns,
derives nonnegative column surplus from the vertical selected-to-blank rule,
and proves the four-spare-blank theorem for arbitrary middle lists. It then
proves boundary-parity, charge, and two-source consequences. The matching
vertex identity, regional charge identity and source charge bounds are explicit
interfaces. The source-frame-to-label implication and residual-grid geometry
still have written proofs; they are not asserted as full-grid Lean adapters.
No finite width list replaces the all-length proof.

Independent controls pass152 sharp cores at widths3..40 with unflipped,
upper-only, both-front and all-front flips;1216 symmetry images; and all165
feasible closed-front receiver completions at width3, including8 with a
saturated receiver tile. Two choices of maximum local pairing give330
additional strand checks for these completions. The family controls also
check two maximum-pairing choices for every sharp core. These controls test
the proof and interfaces; the arbitrary-size conclusion uses the preceding
general argument and Lean induction, not these finite ranges.

The local Lean4.33.0 run passes all three compensation modules and audits12
declarations, including the four new opposed-band/source declarations. Every
axiom set is contained in{propext,Classical.choice,Quot.sound}; no sorry,
admit, native_decide, compiler-trust axiom or new axiom is used. The receipt
`output/opposed-grid-formal-verification.json` binds the actual compiler output,
source hashes and pinned dependency revisions. Reproduce with the locally
selected executable and read-only matching package cache:

    python3 scripts/check_grid_formal.py --lean /path/to/lean4.33.0 \
      --package-cache /path/to/pinned/packages \
      --output output/opposed-grid-formal-verification.json

The oracle suggested the unflipped closed-rail frame and four-blank injection.
The response is archived privately with its task metadata; the actual returned
model label is5.6Pro, distinct from the queued label GPT-6Pro. We independently
checked the counting and geometry, added the parity correction, and removed
the requirement that source-front partners stay in their source rows. Local
Lean, coordinate controls and maximum-pairing checks provide the evidence.
The protected manuscript and correspondence are unchanged.
