# A two-path alternative to direct exterior completion

The coupled exposure theorem computes the exact one-TH-centre,
direct-exterior optimum U_1. Its upper bound need not equal the generic
HH-source lower bound Lambda. We give a second lower bound which can
certify U_1 even when Lambda<U_1. It keeps physical actual-edge capacities
and includes the case of zero actual weights.

## 1. Hypotheses and the alternative

Use precisely assumptions 1--5 of
`EXPOSABLE_PORTS_AND_BRANCHED_SOURCE_OBSTRUCTION.md`. In particular, M is
an actual matching covering P on a finite even rectangle; T consists
of feasible white Q vertices, Q=V minus P; there are r separated cores
P_i and black Q centres h_i; the white holes W number r-1; the HH-source
graph saturates W; and the direct exterior graph has black-saturating
matching and white surplus one. Weights on actual M are nonnegative.
Lambda and U_1 retain their definitions in that theorem. Additionally:

    No centre h_i has a grid neighbour in T.                 (H6)

Thus every TH path ending at a centre contains an actual edge. Call a
terminal path *nontrivial* if it contains at least one actual M edge.
Every other TH path is one direct grid edge. P-only alternating cycles
and doubled M edges do not contribute to the TH expense f(N).

Let C={h_1,...,h_r}. Define F_2^C as the minimum sum of actual expenses
of TWO vertex-disjoint nontrivial alternating TH paths, with different
sources in T and different endpoints in black Q, at least one endpoint
in C. These paths need not extend to a full auxiliary matching N.
The minimum of the empty set is +infinity. Define F_2 without the
centre-endpoint condition; thus F_2<=F_2^C.

Here P=V(M), and a full auxiliary matching N is a perfect matching
of the whole vertex set V. The mathematical statements allow finite
nonnegative real weights. The supplied exact-arithmetic Python API
accepts nonnegative integer weights.

**Two-path dichotomy.** Every full auxiliary grid matching N has either:

1. exactly one TH centre, every other centre HH, and all remaining
   terminal paths direct TH (the previous terminal normal form); or
2. two vertex-disjoint nontrivial TH paths, at least one ending in C.

Proof. Every terminal path in M union N has form N,M,...,M,N. It has odd
grid length, so its two Q endpoints have opposite checkerboard colours.
Since all selected vertices are white, every black centre is either a
TH endpoint with source in T or an HH endpoint with source in W.
There are r centres but only r-1 distinct white holes. Hence at least
one centre is TH. Its path is nontrivial by (H6).

If at least two centres are TH, take their two paths. Otherwise there
is exactly one TH centre, and the other r-1 centre paths use ALL the
white holes, each once. Every other terminal path is consequently TH.
If each is direct, alternative 1 holds. If any is nontrivial, take it
together with the unique TH-centre path. Distinct components have
disjoint vertices and actual edges, giving alternative 2. P-only
components affect neither alternative. QED.

## 2. Lower bound and exactness certificate

**Theorem.** Under assumptions 1--5 and (H6), the true optimum f* obeys

    B_2 := max{Lambda, min{U_1,F_2^C}} <= f*.              (1)

If U_1 is finite, f*<=U_1, with the complete matching constructed by
the coupled exposure theorem. In particular,

    U_1 <= F_2^C  implies  f*=U_1.                        (2)

The existing condition Lambda=U_1 remains sufficient as well. Unlike
the earlier necessity criterion for attaining Lambda, (1)--(2) do NOT
require strictly positive weights or positive rho_i.

Proof. A full N in the first alternative costs at least U_1, by the
exactness of that specified terminal normal form. A full N in the
second alternative costs at least F_2^C: the two paths are feasible
for its definition, their actual edges have different owners, and
discarding the remaining TH expenses cannot increase cost. Thus every
N costs at least min{U_1,F_2^C}. Independently the HH-source theorem
gives f(N)>=Lambda. Taking the minimum over full N proves (1).
The existing construction supplies the upper bound and (2). Zero-cost
additional paths and P-only cycles do not alter this argument. QED.

If w_(1),w_(2) are the two least weights of DISTINCT actual edges,
then F_2^C>=F_2>=w_(1)+w_(2); use +infinity if fewer than two edges
exist. Indeed each of the two paths uses an actual edge, and their
actual sets are disjoint. This gives a weaker certificate which needs
no flow. Using the same actual edge twice in this comparison is invalid.

## 3. Computing the two-path relaxation

Orient each actual M edge black-to-white, with capacity one and its
actual weight. Orient every non-M grid edge white-to-black, capacity
one and cost zero. Add a supersource with capacity-one arcs into T.
Remove every direct T-to-black-Q arc. For F_2, join each black Q
terminal directly to the supersink with capacity one.

For F_2^C, join centres directly to the supersink, each with capacity
one. Join each other black Q vertex to a common exterior collector,
again with capacity one, and give the collector-to-supersink arc
capacity ONE. A flow of value two must therefore end at least one
path in C. This permits both paths to end at centres.

**Flow representation lemma.** Integral flows of value two, after
discarding circulations, represent precisely the two paths in the
definition of F_2 or F_2^C. The minimum flow cost equals that quantity.

Proof. A black P vertex has just one outgoing arc, its capacity-one
actual edge. A white P vertex has just one incoming arc, the same
actual edge. Both vertices of every actual pair therefore have a
single shared physical bottleneck. A white Q vertex has no incoming
grid arc, and a black Q vertex has no outgoing grid arc. Only T can
start a flow path. Source and terminal capacities make endpoints
distinct. Thus integral flow paths cannot share any physical vertex.
Deleting direct T-to-Q arcs forces each path through an actual edge.
The collector enforces the stated endpoint condition. Conversely any
feasible pair of paths gives a flow of value two of the same cost.
Circulations cost nonnegatively, so discarding them never increases
cost. At a minimum any remaining circulation has cost zero. QED.

Two standard successive shortest augmentations compute the answer.
Bellman--Ford permits negative reverse residual costs; integer costs
are exact and no finite sentinel stands for infinity. If value two
cannot be reached, the residual reachable set gives a cut of capacity
at most one. If it is reached, nonnegative reduced costs on every
residual arc certify minimum cost at fixed value. The code returns
both the physical path pair and the corresponding residual certificate.
There are O(v) arcs on a grid, including the terminal and quota arcs.
Two augmentations and the residual-potential check take O(v^2)
arithmetic time and O(v) stored words. Integer bit costs are additional.
These are standard flow algorithms; the contribution here is the
terminal dichotomy and its coupling to the prior normal-form bound.

## 4. Consequences on the fixed branched obstruction

In the existing unit-weight 18-by-18 example, Lambda=1 and U_1=2.
Every nontrivial TH path costs at least one and their actual edges
are distinct. Hence F_2^C>=2, so (2) proves f*=2. The returned
relaxation witness has cost two, showing F_2^C=2 exactly.

For the canonical matching with e_* of weight one and all other
actual edges of weight integer K>=2, U_1=K. Distinct-edge capacity
gives F_2^C>=K+1. One central cheap relay and a disjoint one-edge
arm relay attain K+1 in the relaxation. Therefore F_2^C=K+1 and
the theorem proves f*=K for every K>=2. This reproves that entire
weighted family using a general certificate rather than a separate
case-specific argument about a purported completion below K.

This is an improvement to the TH expense bound in the stated model.
It does not by itself improve the universal 5/6 colouring bound, and
does not assert that the relaxed pair always extends to a full N.

## 5. A genuine cross-component compensation: f*=2 while U_1=K

The relaxation also identifies a failure of global normal-form
optimality. Keep the SAME 18-by-18 board, five cores, centres, selected
set T, white holes, and tight Hall chamber from the branched example.
Change the internal rematching to the fixed explicit M in
`develop/fixtures/two-th-compensation.json`. This file also supplies
two complete auxiliary matchings. Its edge lists are constant
coordinate witnesses, not calls to an enumerator or a random search.

Give the two distinct actual edges

    e_A={(2,2),(3,2)},     e_B={(6,9),(6,10)}

weight one. Give EVERY other actual edge weight integer K>=3.
The fixed full matching N in that file has exactly two nontrivial
TH paths (listed from selected white source to black Q endpoint):

    A: (1,2),(2,2),(3,2),(4,2),
    B: (6,11),(6,10),(6,9),(5,9).

Path A ends at the northwest centre. Path B ends at the exterior black
vertex (5,9) of the tight Hall chamber. Their actual expenses are one
each. The four HH paths are, with either endpoint orientation allowed:

    (2,12),(2,11),(2,10),(3,10),(4,10),(5,10),
    (6,5),(6,6),(6,7),(6,8),(7,8),(8,8),
    (10,11),(10,12),(11,12),(11,13),(11,14),(12,14),
    (11,6),(12,6),(13,6),(14,6),(14,5),(14,4).

All six paths are vertex-disjoint. Each white hole occurs once, and
each centre occurs once. All other terminal paths in the supplied N
are direct; its remaining P-only components use doubled unused M.
Checking this SINGLE coordinate edge list covers all 324 vertices
and gives f(N)=2 for EVERY K. In particular no expensive HH edge is
being charged or reused as a TH resource.

**Proposition.** For this fixed M and all integer K>=3,

    Lambda=1,          F_2^C=f*=2,          U_1=K.          (3)

Proof. The centres have no T neighbours. Each nontrivial TH path
costs at least one, so F_2^C>=2. Paths A,B attain two in that
relaxation. Every centre except the northwest one needs an actual
edge of weight K: e_A is in a different separated core, and the
white endpoint (6,9) of e_B is not adjacent to any centre. A path
using only e_B therefore cannot reach a centre. Only the northwest
centre can use a cheap-only relay, and its ONLY such selected source
is (1,2), via A. Each core's displayed single-K relay proves its
other finite costs are attainable; the source incidence graph still
has every core as an eligible root. Thus Lambda=1.

Recall the tight chamber B_D,F with N_T(B_D)=F and |B_D|=|F|=20.
The vertex (1,2) belongs to F, so it cannot be exposed by a direct
exterior matching. Consequently a TH-centre path in the specified
normal form cannot use a cheap-only relay: it must spend at least K.
The file's `normal_form_N` is a complete matching with precisely one
nontrivial TH path

    (8,5),(8,6),(8,7),(8,8),

whose actual edge has weight K; all other terminal paths are in
the specified normal form. Hence U_1=K. Formula (1) now gives
f*>=min{K,2}=2. The first supplied full N attains two, proving (3).
All weight comparisons in this argument hold for arbitrary K>=3;
there is no extrapolation from a finite range of K. QED.

The compensation is visible at the chamber boundary. Path A removes
one white vertex of F for a centre relay. Path B matches one black
vertex of B_D from an exterior selected source, leaving 19 black
chamber vertices and 19 available chamber whites. The actual edge
sets of A and B, the four HH paths, and the doubled M edges are
pairwise disjoint. The exhibited complete N verifies the remaining
exterior simultaneously. Thus the second relay supplies a different
resource, rather than spending the same Hall surplus twice.

This gives an unbounded gap U_1/f*=K/2 using strictly positive weights
on a fixed footprint. It refutes the rule that one paid centre and
direct remaining TH paths always suffice for a global optimum.
It does not refute (1), the old normal-form theorem, or the 5/6 target.
With weight zero on e_A,e_B and weight one on every other edge, the
same proof and the same two matchings give f*=0 and U_1=1.

## 6. Validation scope

`develop/check_two_th_path_bound.py` compares the flow with independent
enumeration of simple physical path pairs on small grids, including
infeasible pairs, centre quotas, zero weights and 401-digit integers.
It also checks all full 4-by-4 auxiliary matchings on a separate
one-core fixture, rescoring with the older decomposition routine.

On the same 48 changed-M controls used by the prior exposure theorem,
the combined lower bound increases the count of certified global
normal-form optima from 39 to 44; variants 2,22,26,34,42 are newly
certified. Variants 14,23,31,45 are still undetermined by the bounds
alone. The explicit family in Section 5 uses the M discovered at
variant 31 with simpler symbolic weights and fixed certificates;
its all-K proof does not claim to solve the original random weights
of that control. Finite tests validate implementation and fixed
witnesses; Sections 1--3 and 5 supply the mathematical arguments.

The subsequent note `CANONICAL_HALL_BARRIER_AND_PAIR_COMPLETION.md`
strengthens B_2 using the canonical exterior Hall barrier. It certifies
the normal-form optima in original variants 14,23,45, and supplies a
zero-fee full completion for original variant31. Thus all 48 original
controls are subsequently certified, while the scope of B_2 and its
review below remains unchanged.

Independent Oracle review of source `87e7b802de4e42b7beb25cb2c0ae89cef9ccd356`
returned **ACCEPT** with no required mathematical changes. The reviewer
ran the checker and reproduced the report structurally and byte for
byte, and independently reconstructed the fixed coordinate witnesses
without importing the project decomposition. The review covers the
dichotomy, physical flow, combined bound, and all-K/zero-weight family;
it used the supplied git archive, not a GitHub fetch. The two explicit
conventions above are the reviewer's optional clarifications. See
`output/two-th-path-review.json` for provenance and limitations.
