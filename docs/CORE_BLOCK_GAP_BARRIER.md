# Two dissociation witnesses bound shared-port core/block constructions

19 October 2026. The earlier [architecture bound](CLOSED_HIGH_CYCLE_COMPENSATION.md)
assumed distinct core attachment vertices. The following theorem removes
that assumption and also allows arbitrary bipartite high cycles and hub
regrouping. It rules out two apparent ways of improving the3/62coefficient:
reusing a core X vertex, or changing only the selected high cycles.
It is independent of the separately accepted general Heawood block-ledger proof.

## Construction class and theorem

Let r>=1 and b>=0 be integers. Start with the following disjoint classes.

- H contains3r vertices in each bipartition class and induces any simple
  bipartite two-regular graph. Its components may have different even lengths.
- Each h has its own vertices u_h,x_h and the path h--u_h--x_h.
  The vertex x_h has the color of h; u_h has the opposite color.
- Y contains r vertices of each color. Partition the U vertices of each
  color into triples and join each triple to its own opposite-color Y vertex.
- There are b disjoint copies of a Heawood graph with the edge between
  ports0,8 removed. Its seven point vertices and seven line vertices give
  its bipartition. Port0 is a point and port8 is a line.

Attach each block port by one edge to a core X vertex of the opposite
color. Different ports may use the same X vertex, including ports from
different blocks. Complete the remaining degrees using arbitrary X--X
edges. Require the resulting graph to be simple, cubic and bipartite;
there are no other edges. In particular an X vertex has capacity for two
block attachments, and necessarily b<=6r. No connectivity is assumed.
The core contains20r vertices and the full graph has n=20r+14b.

**Theorem.** Every graph G in this class satisfies, with beta=beta_2(G),
star=SF_2(G) and g=star-beta,

    beta >= max(12r+7b, 9r+8b),                            (1)
    62beta >= 33n,                                        (2)
    g <= min(b, floor((15r+2b)/7)),
    62g <= 3n.                                           (3)

Equality62g=3n forces

    b=3r, n=62r, beta=33r, star=36r.                       (4)

The bound is attained for every r by the two-connected Z_r family.
Thus3/62is optimal in this entire enlarged class. This is an architecture
theorem, not a universal bound for all cubic bipartite graphs.

## First dissociation witness

Fix either global color, called even, and write H_odd for the opposite
color in H. Select

    D_1 = U union H_odd union X_even
          union all even-color vertices in every Heawood block.

In the core, each u_h has exactly one selected neighbor: h when h is
odd, and x_h when h is even. Each selected H or X vertex has its U
partner as its only selected neighbor. No high-cycle edge has both
endpoints selected, and Y is omitted. Thus the selected core induces a
matching of6r edges and has12r vertices.

Each block contributes its seven vertices of one color, an independent
set. An attachment at an even X reaches an omitted odd block port;
an attachment at an odd X has its core endpoint omitted. Every X--X
edge also has an odd X endpoint omitted. These arguments apply to each
edge independently, even when two attachments meet the same X vertex.
Therefore D_1 is dissociating, with |D_1|=12r+7b.

## Second dissociation witness

In each broken Heawood block use the explicit dissociation eight-set

    B_8={0,1,2,3,7,8,12,13}.

In the project's fixed labeling its selected edges are

    0--7, 1--8, 2--12, 3--13.

This follows directly from the cyclic Fano incidence rule: point i is
incident to lines i,i+1,i+3 modulo7, with lines numbered7 through13,
and the edge0--8 has been removed. Each displayed vertex has exactly
one neighbor inside B_8. Both ports are selected. This certificate
needs neither an optimum computation nor the saturation lemma.

Select

    D_2 = U union H_odd union all copies of B_8.

The core contributes9r vertices. Its odd H vertices pair with their U
partners; U vertices with even H owners are isolated. All X and Y
vertices are omitted. Consequently every block attachment has an
omitted X endpoint, irrespective of how many attachments meet it.
The blocks have no direct edges to one another. Hence D_2 is
dissociating and has9r+8b vertices. This proves(1).

The two witnesses are alternatives in the same graph. They are not
combined as vertex sets, nor are their block capacities counted twice.

## Density and gap inequalities

Multiply beta>=12r+7b by17 and beta>=9r+8b by14, then add:

    31beta >= 17(12r+7b)+14(9r+8b)
            =330r+231b
            =(33/2)(20r+14b)=(33/2)n.

This proves(2). These positive weights average two independent lower
bounds for one maximum; they do not assert simultaneous attainment.

The established [general cubic compensation inequality](SHARP_CUBIC_BIPARTITE_GAP.md)
states7star<=3n+2beta. Subtracting7beta gives7g<=3n-5beta.
Apply the first witness and then the second to obtain respectively

    7g <= 3(20r+14b)-5(12r+7b)=7b,
    7g <= 3(20r+14b)-5(9r+8b)=15r+2b.

Apply(2) to the same inequality to obtain

    7g <= 3n-5(33n/62)=21n/62,

which proves(3). No attachment injectivity or local block ledger was used.

If62g=3n, compensation forces beta<=33n/62, so equality holds in(2).
Both lower bounds in its positive weighted sum must then be equal to
beta. Their equality gives12r+7b=9r+8b, hence b=3r. Substitution
gives every identity in(4). Each Z_r satisfies the hypotheses and
attains these identities, proving optimality in the enlarged class.

## A quantitative cost for the wrong block/core ratio

The two bounds also give a strict deficit away from b=3r:

    if b<=3r:  3n-62g >= 20(3r-b),
    if b>=3r:  7(3n-62g) >= 170(b-3r).                    (5)

For the first inequality use g<=b and n=20r+14b. For the second use
7g<=15r+2b and expand21n-62(15r+2b)=170(b-3r).
Increasing the number of blocks beyond3r cannot improve the coefficient:
the additional size-eight dissociation selections offset that attempt.

For completeness, H union U together with the fixed port-omitting
minimal forming eight-set in each block is a minimal forming set of
size12r+8b in every graph in the class. At each x_h, deleting h leaves
only the isolated selected u_h, and deleting u_h leaves no selected
neighbor. These witnesses prove core minimality directly for every
allowed high cycle and Y partition. Block minimality is established
in the [Heawood proof](CUBIC_STAR_FORMING_GAPS.md). All interface edges
have both endpoints outside this fixed forming selection, so the
all-subselection rewiring argument preserves its minimality. This
attaining witness is not needed for the upper-bound argument, and no
exact SF or beta value is asserted for arbitrary gluings.

For a self-contained local certificate, use the existing checker selection
{1,2,3,5,7,9,10,11}. Its selected six-cycle is
1--9--2--10--3--11--1, and5,7 are isolated. Outside selected neighborhoods
are0:{7,10},4:{7,11},6:{7,9},8:{1,5},12:{2,5},13:{3,5}.
Deleting a cycle vertex leaves one displayed outside witness with only
an isolated selected neighbor. Deleting5 or7 leaves that vertex itself
without a selected neighbor. This proves formation and all eight deletion
failures without a new optimization premise. Both ports0,8 are omitted.

Let L1=12r+7b,L2=9r+8b, e=beta-max(L1,L2)>=0,
c=3n+2beta-7star>=0, and Delta=3n-62g. Exact expansion gives

    if b<=3r:  7Delta=140(3r-b)+310e+62c,
    if b>=3r:  7Delta=170(b-3r)+310e+62c.

The imbalance, extra dissociation capacity and compensation slack are
distinct nonnegative terms. The lower forming witness and compensation
also give the numerical equivalence

    62g=3n  iff  b=3r and beta=33r.

This does not classify which gluings have beta=33r. These supplementary
identities have written algebraic proofs; the eleven-declaration formal
audit retains its original scope.

## Verification and scope

The four new declarations in [ClosedHighCycle.lean](../formal/StarForming/ClosedHighCycle.lean)
verify the conditional density count, gap bound, necessary equality
balance and piecewise deficit. Together with the earlier seven counts,
the [local Lean audit](../output/closed-high-cycle-formal-check.json)
passes eleven declarations with standard logical axioms only. Graph-to-count
extraction and both graph witnesses have the general written proof above.

The [independent controls](../output/core-block-gap-barrier-controls.json)
check285actual graphs,570dissociation witnesses and37,260literal
selected deletions;228instances have a reused core attachment vertex.
They cover one to five cores, every block count0 through6r, fixed
six-cycles, one high cycle and arbitrary high two-factors, with regrouped
hub triples. They do not optimize beta or SF. Their finite conclusions
are not premises of the theorem.

The earlier Z_r Oracle ACCEPT predates this enlarged theorem and does
not constitute its review. Its own [independent review](../output/core-block-gap-barrier-oracle-review.json)
now completed ACCEPT, covering both witnesses, repeated attachments,
arbitrary high cycles, all counting steps and equality necessities.
The exact response is archived; its supplementary identities and a
self-contained local certificate are included above.
The general cubic bipartite ceiling remains1/14;
this theorem identifies a larger class that cannot approach it. To
improve3/62one must change a hypothesis affecting the two witnesses,
such as the blocks or the core's H/U/X/Y incidence pattern. Arbitrary
high-cycle rewiring and shared X attachments alone do not suffice.
The rectangular-grid equality and psi_sq<=SF bridge remain open.

Reproduce the controls and conditional formal audit with:

```sh
python3 scripts/check_core_block_gap_barrier.py --output output/core-block-gap-barrier-controls.json
python3 scripts/check_cover_pullback_formal.py --lean /path/to/lean4.33.0/bin/lean --audit closed-high-cycle --output output/closed-high-cycle-formal-check.json
```

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
