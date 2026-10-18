# A second Heawood cut transfers the compensation obligation

19 October 2026. Finite simple bipartite graphs and non-induced
two-star formation are used throughout. The [three-pair theorem](CUBIC_TRIPLE_PORT_COMPENSATION.md)
has received independent ACCEPT. This note records a precise obstacle
to extending its attachment rule through a second Heawood cut.

## Two disjoint cuts preserve the Heawood cap, but not saturation

Proposition. Let H be the Fano-plane incidence graph. Delete any two
vertex-disjoint incidence edges, obtaining B. Then beta_2(B)=8.
Unlike the one-cut case, a dissociation eight-set need not saturate
both ports of a prescribed deleted edge.

Here is a proof of the cap for every choice of two disjoint edges.
For a dissociation set D of size t, let p count its selected ports,
i its selected isolates, and e the complement edges. The exact
deficiency identity, with N=14 and total degree deficiency4, gives

    38-5t+2p=i+2e.

Since p<=4, we have t<=9. If t=9, the identity forces p=4,i=1,e=0.
In particular all four cut ports are selected. Let a,b be the numbers
of omitted points and omitted lines; a+b=5.

If a=0, the two selected port lines still have two selected point
neighbors each, impossible. If a=1, there are3selected lines, at least
one of which is not a cut port; it has at least two selected point
neighbors, again impossible. Hence a>=2. Duality gives b>=2, leaving
only (a,b)=(2,3) or (3,2). In the former case four lines are selected,
including at least two non-port lines. Each of these must contain
both omitted points to have at most one selected neighbor. The unique
line through two distinct Fano points excludes this. The other case
is dual. Thus no nine-set exists and t<=8. The one-cut eight-set
remains dissociating after deleting the second edge, proving attainment.

This proof uses the incidence axioms and the deficient-degree count;
enumerating the possible cuts is not a premise.

## An explicit failed local compensation rule

Use the Heawood labeling in `check_cubic_starforming.py`: points0,...,6,
lines7,...,13, with point vector order(1,2,4,5,7,3,6) and line j+7
incident with point indices j,j-1,j-3 modulo7. For the established
forming eight-set {1,2,3,5,7,9,10,11}, the outside edges are

    0--8, 4--12, 6--13.

Delete 0--8 and 4--12. In the resulting B, the set

    D_B={0,2,4,6,8,11,12,13}

is dissociating. Its induced edges are exactly

    2--12, 4--11, 6--13.

The original ports0,8 are both selected isolates. The new ports4,12
are selected and already paired. Thus the original one-cut conclusion
that both original ports are internally saturated is false after
a second cut. The cap8 alone does not imply that conclusion.

For a complete counterexample to the resulting local charging rule,
take the20-vertex six-port core Q from the three-pair theorem, labeled
H=0,...,5, U=6,...,11, X=12,...,17, Y=18,19. Select

    D_Q={0,1,3,4,8,11,12,13,15,16,18,19}.

This twelve-set induces the five edges

    0--1, 3--4, 8--18, 11--19, 15--16,

and the two isolates12,13. Attach B to Q by

    point0--x_1, line8--x_0,

that is,0_B--13_Q and8_B--12_Q. Both attachments join one selected
isolate from each part, so D_B union D_Q remains dissociating and has
20vertices. Since the separate caps are8 and12, this34-vertex module
has exact beta_2=20. The naive19-vertex bound for an eight-vertex
Heawood restriction attached at the original pair is therefore false.

The failed statement is the extension of the one-cut saturated-port
charging rule to a twice-cut Heawood block. The original saturated-port
lemma, the three-pair theorem and the universal cubic inequality remain
valid: their hypotheses do not include this twice-cut attachment.

## Why this is a transferred obligation, not a global counterexample

The module has six degree-two ports. In combined labels, with B shifted
by20, they are

    {14,15,16,17,24,32}.

Ports14,17 are omitted from the displayed twenty-set. Ports15,16,24,32
are selected and already internally paired. In particular the new
Heawood pair now forces any attached external neighbors to be omitted.
This is precisely where the missing original-interface charge moved.

Any cubic completion on these same34vertices would have to match the
six deficient ports with three added edges. Each of four internally
saturated selected ports would need an omitted partner to preserve
this twenty-set, but there are only two omitted ports. Hence at least
one added edge destroys its dissociation property. A completion with
additional vertices has its own capacities to account for. The local
failure therefore does not disprove a global compensation inequality.

## Exact arbitrary interfaces and an architecture limit

There is also a clean obstruction to improving1/24 merely by attaching
more one-cut Heawood blocks to the same six-port cores. Consider a
connected cubic graph built from c copies of Q and b one-cut Heawood
blocks, where each Heawood block attaches both of its ports to one
distinct cut pair in one core, and every remaining edge joins core
ports. The matching between the remaining core ports can be arbitrary,
provided the completed graph is simple and bipartite. It need not respect
the original pairs or form a single cyclic interface. Then, even without
assuming connectedness,

    n=20c+14b, beta_2=12c+7b, SF_2=12c+8b, gap=b.          (1)

For the upper dissociation bound, if a core has a_j attached blocks
and b_j of those restrictions have size8, its distinct attached pairs
include at least b_j wholly omitted pairs. The core contributes at
most12-b_j, and its attached blocks at most7a_j+b_j. Summing over
disjoint core/attached-block modules proves beta<=12c+7b.

For the reverse bound, the fixed minimal forming selection survives
every outside-only interface. Its size is s=12c+8b and its selected
isolate count is z=2b. The general isolate compensation theorem gives
2s<=2beta+z, hence beta>=12c+7b. This proves exact beta without an
assumption about an attaining set fitting a chosen port matching.
The fixed selection gives SF>=s, while cubic compensation gives

    7SF<=3(20c+14b)+2(12c+7b)=7s.

Thus SF=s and (1) follows. The isolate theorem supplies actual exchange
sets in its proof; the lower bound is not a finite-optimization premise.

Now assume connectedness and c>=2.

Contract each Heawood block into its host core and count edges leaving
each resulting module. If a core has a_j attached Heawood blocks, that
cut has size at most6-2a_j. Connectedness forces it positive. Each
module's total number of remaining core stubs is even; its internal
stub edges consume an even number, so its edge cut is also even and
at least two. Thus a_j<=2, and b<=2c. Equation(1) gives

    gap/n=b/(20c+14b)<=1/24,

because this last inequality is exactly b<=2c. The existing cyclic
family attains the bound. This limits the exact gap for every allowed
interface in this architecture.

More precisely, if ell_j matching edges join remaining ports inside
module j, its edge cut has size6-2a_j-2ell_j. Thus a_j+ell_j<=2.
At b=2c every module consequently has exactly two attachments, no
internal port edge and exactly two edges leaving it. The connected
quotient by modules is a cycle. For c=2 its two quotient edges are
parallel but their actual core endpoints are distinct. This classifies
all density-equality interfaces within the stated architecture.

For c=1, three attachments are possible and give
the isolated62-vertex construction with beta33,SF36,gap3; disjoint
copies do not give a connected asymptotic improvement.

Thus improvement beyond this architecture requires a different
interaction: split attachments, multiply cut obstructions, or a
stronger core. The explicit module above shows why multiply cut
obstructions need fresh interface accounting.

## Verification scope

The general two-cut Heawood cap and the architecture limitation have
written proofs above. The checker independently enumerates all168
choices of two disjoint Heawood incidences, verifies their exact cap8,
and checks the explicit34-vertex adjacency, twenty-set, port states,
literal forming/deletion witnesses and vertex-deletion connectivity.
The [control record](../output/heawood-multiport-controls.json) covers
2,752,512subset/cut instances,44completed arbitrary interfaces
(14connected), and4,556literal selected deletion checks including the
explicit obstacle. Both augmented exchange sizes are checked against
12c+7b for every completed interface; they supply independently verified
attainment even when the original alternating-core witness does not fit.
The existing T_r family is already covered by its separate controls.

The [Lean source](../formal/StarForming/HeawoodMultiport.lean) has six
fixed graph certificates: the twenty-set's dissociation and cardinality,
simple subcubic adjacency, bipartition, isolated attachment ports before
joining, and the remaining saturated/omitted port profile. Three further
conditional count theorems verify the deficient-degree equality,
arbitrary-interface parameter deduction and1/24architecture inequality.
The [formal receipt](../output/heawood-multiport-formal-check.json)
records nine local Lean4.33.0audits with standard axioms only. The
general incidence and graph-interface proofs remain written; no finite
enumeration replaces them. The submitted manuscript and upstream are
unchanged. A [separate review receipt](../output/heawood-multiport-oracle-review.json)
records ACCEPT for this extension independently of the accepted triple-port
theorem. The [response](reviews/2026-10-19-heawood-multiport-review-response.txt)
also checks internal matching edges in the cut count and the equality-cycle
classification above. No mathematical repair was requested.
