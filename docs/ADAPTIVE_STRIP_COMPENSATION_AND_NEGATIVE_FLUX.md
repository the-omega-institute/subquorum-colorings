# Exclusive strip certificates compensate negative comb flux

19 October 2026. This note continues the prescribed-source grid problem,
separately from the submitted manuscript. It proves a compensation criterion
that does not require nonnegative total comb flux. Its optimization is a
classical bipartite cut problem; the contribution here is the geometric
adapter, an explicit negative-flux family and the resource accounting.

## 1. Hypotheses and the exact per-strip input

Retain all hypotheses in Section 1 of
`DIRECTIONAL_AVERAGING_SOURCE_COMPENSATION.md`: an even physical rectangle,
a feasible initial pair (T_0,M_0), the prescribed complete positive long
sources with their actual matching and selected supports, the stated outside
thin/one-square/complete-comb coverage, and only prescribed source or complete
contact-comb endpoints in source mouths. Normalize preserving those frozen
data and the objective. No arbitrary positive bent-source coverage is assumed.

Coalesce parallel mouths as before. For strip i, let b_i be its number of
member source mouths, f_i=U_i-S_i its signed complete-comb end incidence,
a_i its perpendicular-source phase gain, d'_i its shifted no-P deficit,
and D_i its original physical no-P deficit. Then

    D_i=2b_i+f_i+a_i+d'_i,       a_i,d'_i>=0.          (1)

Indeed the accepted strip identity is D_i=2+L_i+f_i+a_i+d'_i. The coalescing
argument gives L_i=2b_i-2 individually. Any parallel tip in the strip has
its owner's mouth in this same merged interval, since its adjacent mouth
would otherwise make two intervals adjacent and hence merged. At least two
member tips are outside, at the two extreme ends, so L_i<=2b_i-2. The
accepted global conservation sum L_i=2B-2C=sum(2b_i-2) forces every one
of these inequalities to be an equality. Perpendicular tips are counted
by a_i, not by L_i. Also sum_i b_i=B.

Define the conservative, integral strip weight

    q_i=max(0,2b_i+f_i).                              (2)

Equation (1) and physical nonnegativity give D_i>=q_i in every feasible
completion covered by the hypotheses. These weights deliberately do not
spend the phase gains, shifted deficits or exterior remainder.

Form the graph H whose vertices are coalesced strips, with an edge precisely
when two strips share a physical tile. Same-direction strips are disjoint,
so H is bipartite, with horizontal and vertical sides. Endpoint-containing
and zero-deficit intersections may be retained as edges: this conservative
choice depends only on the prescribed mouth geometry. Removing an edge is
valid only after verifying that its shared tiles contribute no actual donor.
For a uniform completion-class certificate, that exclusion must hold in
every allowed completion, not just in an observed baseline.

## 2. General exclusive-strip compensation lemma

Let I be any independent set of H and put q(I)=sum_(i in I) q_i. Write

    Delta=mn/2-|T_0|-|M_0|=-B+D_G+R,       R>=0,     (3)

for the established whole-receiver ledger, where G is the union of mouths
and D_G its original no-P deficit. Then

    Delta>=q(I)-B+R.                                 (4)

In particular q(I)>=B proves |T_0|+|M_0|<=mn/2. This conclusion permits
negative F=sum_i f_i, arbitrary prescribed source directions and arbitrary
crossings. It is a sufficient condition, not an equivalence with the grid
bound.

Proof. Strips in I have disjoint physical tile sets. Each claimed no-P tile
therefore has one owner and is used at most once, with its actual deficit
2-t_Q. Consequently

    D_G>=sum_(i in I) D_i>=sum_(i in I) q_i.

Substitution into (3) proves (4). No source endpoint, comb end, corrected
matching export or shifted square becomes a second donor. R is retained
once in (3). QED.

Maximize q(I) over independent sets and call the result W. The strongest
certificate in this conservative strip-selection family is W>=B. It can
be computed exactly by a cut, as follows; the proof does not depend on
enumerating possible grid configurations.

## 3. Exact optimization and what its failure means

Construct a network with source s and sink t. Give s->i capacity q_i for
horizontal vertices, j->t capacity q_j for vertical vertices, and i->j
capacity 1+sum q for every edge of H. A minimum cut never cuts an i->j
arc, since a cut of capacity at most sum q exists. Its horizontal vertices
on the sink side together with its vertical vertices on the source side
therefore form a vertex cover C. Conversely every cover defines such a
cut of cost q(C). Thus the minimum cut is the minimum-weight vertex cover,
and taking complements gives

    W=sum_i q_i-mincut.                              (5)

The standard integral max-flow/min-cut theorem supplies the cut and an
independent-set witness. The checker separately verifies their weights,
the cover property and exclusive physical ownership. It also saves a
feasible edge-flow witness and checks its capacities and vertex totals;
its value equals the cut weight. The latter equality certifies optimality,
whereas an independent-set witness alone certifies only the lower bound.

There is an exact limitation statement for these scalar data. Relax physical
resources to permit one unbounded shared resource on every graph edge and
one private resource at each vertex, requiring total incident resource at
least q_i. The minimum total resource in this relaxed model is exactly W.

Proof. Every independent set gives a lower bound q(I) by exclusive incidence,
so the relaxed cost is at least W. Let f_ij be an integral maximum flow in
the network above. Assign f_ij units to its shared edge resource and assign
q_i minus the incident flow to vertex i's private resource. The latter is
nonnegative by the capacity at i. Each vertex receives exactly q_i. If the
flow value is v, shared resources cost v and private resources cost
sum q-2v. Total cost is sum q-v=W by (5). QED.

Hence W<B is an obstruction to proving the desired payment using only these
scalar strip demands and this relaxed incidence data. It is not a graph
counterexample: the relaxation discards finite tile capacities, the existence
of private donor sites, feasibility, phase gains, shifted deficits and R.
The max-flow theorem is classical; no novelty is claimed for (5).

A simple useful subcertificate avoids even a cut. In each connected component
of H, select its entire heavier direction. If q_H(C),q_V(C) are the two
directional weight sums, then

    W>=sum_C max(q_H(C),q_V(C)).                      (6)

Different components have disjoint strip tile sets, so these choices compose.
They can beat both uniform half allocation and choosing one global direction.
More generally an independent set may mix directions within one component;
the cut certificate already includes that possibility.

## 4. An explicit negative-flux crossing star for every p>=2

Use the fully frozen source from `LONG_BENT_BANDS_AND_TERMINAL_STRIP_COMPENSATION.md`.
For p>=2 take p downward sources H_i, i=0,...,p-1, with

    width w_i=8p+20-8i, depth h_i=4p+2,
    chamber origin (2+4i,3+4i).

Their left/right arm columns are x_i=3+4i and y_i=8p+22-4i;
their tip rows are t_i=8p+8+4i. Add a perpendicular source K by transposing
the standard origin-(2,3) source of width 8p+6 and depth 2, and translating
by (4p+2,4p+4). Its chamber is

    rows 4p+5,...,12p+10, columns 4p+6,4p+7,

and its rightward mouth is

    rows 4p+6,...,12p+9, columns 4p+12,4p+13.

Finally put one vertical four-endpoint comb at column c=4p+2 and rows
t-3,...,t, where t=8p+8. Match consecutive endpoints. Its selected supports
are (t-4,c),(t+1,c), and

    (row,c+1) for odd row=t-3,t-1,
    (row,c-1) for even row=t-2,t.

Use all prescribed source supports, select nothing else, and embed in the
even rectangle (12p+18)-by-(8p+30). These are exactly the coordinates in
`negative_star(p)` in `develop/check_adaptive_strip_compensation.py`.

**General feasibility and completeness proof.** Endpoint sets of distinct
H_i have Manhattan distance at least three. The distance-three pairs occur
only between the lower chamber row R_i+1 of H_i and the upper chamber row
R_i+4 of H_(i+1), where R_i=2+4i; arm-to-arm and arm-to-chamber separations
are at least four. Three steps prevent a prescribed support from seeing a
foreign endpoint, but do not alone exclude support-to-support adjacency.
Here is the missing interface check. In origin-(R,x) coordinates a source's
supports are precisely

    (R,x-1),(R,x+w);
    (R+2j,x-1),(R+2j,x+w) for j=1,...,h+1;
    (R+2j+1,x+1),(R+2j+1,x+w-2) for j=1,...,h;
    (R+2h+3,x),(R+2h+3,x+w-1).

In particular there is no support above row R. If supports assigned to
two distance-three chamber endpoints were adjacent, they would have to
occupy rows R_i+2 and R_i+3 in a common column. But H_(i+1) has no support
at R_i+3, since its origin row is R_i+4. Such adjacency is impossible.
All other endpoint separations are at least four and hence give support
distance at least two. This proves compatibility for the original coordinates;
it does not use the incorrect distance-four assertion in the first review
input. Source K and all its supports lie strictly inside the H_i arms
and below all H_i chambers, with endpoint separation at least four. For
example its top chamber endpoint row is 4p+5, while all H_i chamber rows
are at most 4p-1; its chamber column is at least six beyond the innermost
left arm and well before the innermost right arm. Its upper/lower arms
and their supports obey the same separation.

Only the new comb and H_(p-1) require a closer check. The innermost left
arm is at column c-3. On odd rows its inside support is at c-2, while
the comb side support is at c+1. On even rows the source's outer support
is at c-4 and the comb's side support is at c-1. Across successive rows
the nearest side supports are diagonal, at distance two. Each axial comb
support is at column c and is at least distance two from these source
supports. Thus none acquires a second occupied neighbor. The other H_i
are farther away. Comb endpoints are at least four from K's chamber;
the comb's right side supports remain at least three columns from it.
Each prescribed support therefore has exactly its own endpoint neighbor
and no other occupied neighbor. The separate source and comb feasibility
checks cover the remaining internal adjacencies. No endpoint components
are joined. All coordinates lie in the displayed rectangle.

The retained-support freezing proofs apply independently to all components,
so every endpoint is universally frozen. The components have whole receiver
charges +1 for each source and zero for the comb.

**Mouth graph and flux.** The p horizontal mouths have different physical
row bands and K's vertical mouth meets each once, so H is the star K_(p,1).
The common tile for H_i and K has rows t_i,t_i+1 and columns 4p+12,4p+13.
All are strictly inside the vertical mouth. They contain neither endpoints
nor selected supports in the displayed baseline, hence have deficit two.
There are X=p crossings and exact crossing loss K_loss=2p.

The comb's saturated singleton is in rows t-4,t-3 and columns c,c+1,
outside every mouth. Its sparse singleton is in rows t,t+1 and columns
c,c+1, in H_0's mouth only. Its other physical tile has two endpoints.
The axial supports and the preceding alternating side support force the
remaining sparse-tile corners blank, so feasible completions preserving
the prescribed data do not change these end types. Thus

    B=p+1,  F=-1,  O=1,  J=0,
    q(H_0)=1,  q(H_i)=2 (i>=1),  q(K)=2.

The entire horizontal side is independent and has weight 2p-1. The star
has no independent set mixing its center with a leaf, so

    W=max(2p-1,2)=2p-1>=p+1=B.                       (7)

The compensation lemma proves the coefficient-one bound for every feasible
completion in the stated class retaining these source/comb data. This is
a genuinely negative-flux application. In the explicit baseline the earlier
crossing criterion fails: K_loss+O=2p+1>B+J=p+1. Extra slack may give other
ways to certify a particular completion; the comparison here concerns the
stated structural criteria, not every possible use of the exact ledger.

Here and in Section 5, a completion retains the listed sources and combs as
complete endpoint components, with their matching and selected supports, and
has no additional endpoint component meeting the mouth union G. Additional
feasible selections and allowed nonpositive components outside G are permitted.
This fixes the end incidences used by the displayed weights. The more general
lemma in Section 2 allows other mouth combs, but recomputes their actual f_i.
For the old-criterion comparison, O counts complete combs whose sparse end
belongs to G and saturated end does not; J counts the reverse membership.
Both use union membership, rather than strip multiplicity.

## 5. Arbitrarily negative flux and why componentwise choices matter

For any k>=1, take k copies of the p=2 construction, transpose every second
copy, translate each by (2,2+50j), j=0,...,k-1, and embed in the rectangle
50-by-50k. The untransposed copy has size 42-by-46 and the transposed copy
46-by-42, so both fit inside their 50-by-50 blocks with a two-vertex margin.
Different blocks have no selected or endpoint adjacency. This proves
feasibility, completeness and freezing for every k, using the preceding
general construction, rather than inferring them from finitely many cases.

The strip graph is k disjoint K_(2,1) stars, with

    B=3k, F=-k, W=3k, X=2k, O=k, J=0.

Select the two leaves in each star, irrespective of its spatial direction.
The resulting strip claims are globally disjoint and supply at least 3k
actual original donor units. Thus every covered feasible completion has
Delta>=R>=0, even though the total negative flux is unbounded with k.
The deficit is supplied by whole selected strips; the negative comb ends
and positive matching exports are not spent as extra physical resources.

For even k the horizontal and vertical structural weight totals are both
5k/2. Uniform half allocation of the structural demands also gives only
5k/2, below the source charge 3k. A single global direction therefore misses
the certificate; independent component choices give exactly 3k. In the
baseline K_loss+O=5k>3k, so the older exact crossing-loss criterion also fails.
For odd k>=3 the better single direction gives (5k+1)/2<3k as well.

This is a closed family of compensation lemmas for arbitrarily negative
weighted flux, not a proof that every negative-flux configuration is paid.
It also does not refute any exact identity: the positive phase/shifted/single
or exterior terms in those identities remain available.

## 6. Validation, formal scope and the remaining gap

Run the independent controls with

    python3 develop/check_adaptive_strip_compensation.py --output output/adaptive-strip-compensation-controls.json

The checker verifies the initial physical ledger, feasibility, complete
freezing, per-strip tip counts, flux, cut/independent witnesses, and actual
exclusive ownership. Small strip graphs are also checked against all their
independent sets. The explicit construction and the general proofs above
establish the all-p/all-k conclusions; finite controls only test them.

The physical receipt passes 70 configurations and 32 symmetry images,
including 47 compensated negative-flux cases and six expected uncertified
end-locality cases. It checks p=2,...,10,16,24 and k=1,2,3,4,6,8,12, as
well as dense source-only crossings. A further 1,024 abstract bipartite
graph/weight controls compare the cut algorithm to exhaustive independent
sets; a connected four-vertex path verifies that the optimum can select
both directions inside a component. That abstract path is not asserted
to be a new geometric construction.

The Lean module `formal/SubQuorum/AdaptiveStripCompensation.lean` separates
the exclusive physical resource sum, the conditional objective implication
and the unbounded star arithmetic. The local sequential Lean 4.33.0 audit
passes 100 scoped declarations, adding these three to the prior 97.
As in the prior work, the full geometric
adapter, coalescing, graph construction, maximum-flow theorem and explicit
grid family remain written proofs. No full geometric Lean theorem is claimed.

The first independent review fcb4aa67-e6d9-4f74-af8d-c0c33fcd2160 completed
REVISE at 11:57:14 UTC. It accepts the compensation lemma, weighted cut
and relaxed optimum, but correctly rejects the first input's distance-four
argument. The explicit support-interface repair above, completion quantifier,
O/J definitions and exact flow witness address its requested revisions.
Follow-up c91ffe7a-1550-4fe1-94b7-087d8bc51f8b completed ACCEPT at
12:10:24 UTC. It checks the explicit support-interface repair, original
all-p/all-k coordinates, uniform completion class, actual resource ownership
and exact flow witness. The response is archived in
`output/adaptive-strip-repair-review-response.json`.
The initial stream 81531 ended with a TLS observation error, but the same
task's completed response was retrieved and archived without restarting it.

The broader research task f8af741f completed at 11:58:11 UTC; its proposal
is developed separately in `REMOTE_COMB_RUNG_COMPENSATION.md`. The later
`CAPACITY_AWARE_STRIP_COMPENSATION.md` also improves this note's conservative
exclusive certificate. Both extensions have a separate live review and are
not covered by the first exclusive-note assessment.

The existing all-radius frozen-end locality construction has one mouth with
two sparse ends, b=1 and f=-2, so q=0 and W=0<B=1. This identifies a real
limit of the new scalar strip certificate. It requires additional distant
or source-level geometry, phase/shifted information or exterior payment.
Arbitrary positive bent components, the universal grid coefficient-one bound
and the proposed grid triple equality remain open. Submitted manuscripts
are preserved.
