# Three cut pairs pay independently: cubic gaps of order one twenty-fourth

19 October 2026. Finite simple graphs, non-induced two-stars and
inclusion-minimal forming selections are used throughout. The local
proof below strengthens the [four-port padding lemma](CUBIC_EQUALITY_PADDING_RINGS.md)
for its smallest core. It gives a better connected asymptotic gap
construction than the preceding coefficient1/28. This is a comparison
with this project's proved constructions, not a literature-priority claim.

## Statement

For every r>=1 there is a two-connected cubic bipartite graph T_r with

    n=48r,
    beta_2(T_r)=26r,
    SF_2(T_r)=28r,
    SF_2(T_r)-beta_2(T_r)=2r=n/24,
    7SF_2(T_r)=3n+2beta_2(T_r).                            (1)

The selected isolates number4r. Thus the isolate bound is attained,
and the general cubic compensation inequality is attained too. The
connected asymptotic coefficient is now bounded below by1/24and above
by1/14; determining the optimum remains open.

The entire improvement rests on one local statement: a six-port core
loses at least one dissociation vertex for **each** wholly omitted cut
pair. Two neighboring obstructions cannot share the same loss.

## The fixed six-port core

Use C_1 from the periodic-core construction, with indices modulo six:

    H={h_0,...,h_5}, U={u_0,...,u_5}, X={x_0,...,x_5},
    Y={y_0,y_1}.

H and X induce six-cycles, and the other edges are h_i--u_i--x_i and
u_i--y_(i mod2). Delete all three edges

    e0=x_0--x_1, e2=x_2--x_3, e4=x_4--x_5.

Call this20-vertex core Q. Its remaining X edges are x_1--x_2,
x_3--x_4,x_5--x_0. These three edges form a matching. The six X
vertices have degree two, and every other vertex has degree three.

For a dissociation set D put t=|D|, p=|D intersect X|, i_D equal to
its number of isolated vertices, and e_T the number of edges inside
the complement in Q. The exact deficiency identity is

    54-5t+2p=i_D+2e_T.                                    (2)

Let m be the number of pairs e0,e2,e4 whose endpoints are both
omitted from D.

Lemma. Every dissociation set D in Q satisfies

    |D|+m<=12.                                            (3)

We prove it by the four possible values of m, with one short
classification by the two Y vertices in the only tight case.

## No omitted pair: at most twelve

In every case p<=6, so (2) gives5t<=66 and t<=13. If t=13, (2)
forces p=6. Both ends of every remaining X matching edge then belong
to D, so every u_i must be omitted: otherwise its x_i neighbor has
two selected neighbors. A dissociation set on the H six-cycle has
at most four vertices, and there are only two Y vertices. Hence
t<=6+4+2=12, a contradiction. Thus t<=12 without any omission
assumption. The six-cycle cap follows by summing its six three-consecutive
vertex constraints, each of which contains at most two selected vertices.

## One specified omitted pair: at most eleven

Rotate indices by two to assume x_0,x_1 are omitted. Among the other
two cut pairs, suppose at most one has both endpoints in D. Restore
the cut edge at the remaining pair: since at most one endpoint is
selected, this does not alter the induced graph on D. The resulting
graph is C_1 with two cut edges, including e0. The four-port strict-loss
lemma gives t<=11. That lemma applies to any two of e0,e2,e4: rotation
by two maps each unordered pair to {e0,e2}.

It remains to consider both x_2,x_3 and x_4,x_5 selected. By the
unconditional cap it suffices to rule out t=12. The selected edge
x_3--x_4 forces u_3,u_4 to be omitted. Thus at most four U vertices
are selected. Let a=|D intersect H|, u=|D intersect U| and
q=|D intersect Y|. We have a<=4 and

    a+u+q=8, since exactly four X vertices are selected.    (4)

- If q=0, (4) forces a=u=4. The selected U vertices must be
  u_0,u_1,u_2,u_5. Since u_2 and u_5 already meet selected x_2,x_5,
  h_2,h_5 are omitted. Thus the four selected H vertices would have
  to be h_0,h_1,h_3,h_4. But h_0 then meets both selected h_1 and u_0,
  contradicting dissociation.
- If q=1, reflect indices by i->1-i if needed to assume y_0 is
  selected. This reflection preserves Q and the omitted pair e0,
  while interchanging the two Y vertices. The even U vertices u_2,u_4
  cannot be selected because their x_i and y_0 neighbors are both
  selected. Thus at most u_0,u_1,u_5 are available, and (4) forces
  u=3,a=4. Now u_0 meets y_0 and u_5 meets x_5, so h_0,h_5 are
  omitted. The other four H vertices induce a four-vertex path, which
  cannot be wholly contained in a dissociation set. This contradicts a=4.
- If q=2, every U vertex whose X partner is selected is omitted,
  so only u_0,u_1 are available. Equation (4) forces u=2,a=4.
  Both h_0,h_1 must then be omitted because u_0,u_1 already meet their
  Y partners. The other four H vertices again induce a path, a contradiction.

Thus t<=11 whenever any cut pair is wholly omitted. The reflection
and rotations used here preserve the three removed pairs, the remaining
X matching, both cycles' index order up to reversal, and U's parity hubs.

## Two specified omitted pairs: at most ten

Rotate so x_0,x_1,x_2,x_3 are omitted. Then p<=2. Suppose t=11;
larger values have already been excluded. The complement contains the
remaining edge x_1--x_2, so e_T>=1. Equation (2) becomes

    -1+2p=i_D+2e_T,

forcing p=2,e_T=1,i_D=1. Thus both x_4,x_5 are selected, and there
can be no complement edge other than x_1--x_2.

The edges x_j--u_j for j=0,1,2,3 force all u_0,u_1,u_2,u_3 to be
selected. Both Y vertices must therefore be omitted, since each has
two of these selected neighbors. Then the absence of any further
complement edge forces u_4,u_5 to be selected as well. Each already
meets selected x_4,x_5, so h_4,h_5 are omitted. To reach t=11 would
require three H vertices among h_0,h_1,h_2,h_3. But all their U
neighbors are selected, so these H vertices must form an independent
set in a four-vertex path, of size at most two. This is a contradiction.

Hence t<=10. Any two of the three cut pairs have the same relation
under the stated rotations.

An equivalent shorter end to this case is that omitted h_4,h_5 create
the second complement edge h_4--h_5, directly contradicting e_T=1.

## All three pairs omitted: at most nine

Here p=0 and the complement contains all three remaining X matching
edges, so e_T>=3. If t>=10, equation (2) gives

    i_D+2e_T=54-5t<=4,

contrary to i_D+2e_T>=6. Thus t<=9. The four cases prove (3) for every
dissociation set, without an exhaustive-subset premise.

## Two obstructions per core and a cyclic interface

For each i=0,...,r-1 take one Q_i and two disjoint broken Heawood
blocks B_(i,0),B_(i,1), each obtained by deleting point0--line8.
For j=0,1 add

    point0_(i,j)--x_(2j+1,i),
    line8_(i,j)--x_(2j,i).

Join the remaining ports by x_(4,i)--x_(5,i+1), cyclically in i.
For r=1 this restores e4. All vertices now have degree three, and
the graph is simple and bipartite.

Let D be a dissociation set in the full graph. In one module let b
be the number, zero, one or two, of its Heawood restrictions having
size eight. The saturated-port lemma forces the corresponding core
pair to be wholly omitted for each such block. Its core therefore
has at least b omitted pairs, and (3) gives at most12-b vertices.
The two Heawood blocks contribute at most14+b. The entire module
contributes at most26, independent of its interface ports. Summing
over disjoint modules proves beta_2(T_r)<=26r, with every dense block's
gain charged once to its own distinct cut pair.

For r=1, first delete the restored e4 when restricting to the auxiliary
core Q. A dissociation set remains dissociating after deleting an edge,
so the same bound applies without consuming another interface condition.

For attainment, choose all seven points in each Heawood block, and
U union H_odd union X_even in each Q. The latter has twelve vertices
and induces a matching. Every interface edge has an omitted endpoint,
so the union is dissociating with26rvertices.

The minimal forming selection consists of the established eight-set
in every Heawood block and H union U in each core, giving28rvertices.
All modified edges have both endpoints outside this fixed selection,
so its literal covering and single-deletion witnesses survive. The
cubic compensation theorem then gives

    7SF_2(T_r)<=3(48r)+2(26r)=7(28r),

proving exact SF_2. This establishes all numerical claims in (1).

Each module before removing e4 is formed by two successive edge swaps
between the two-connected C_1 and two-connected Heawood graphs, so
it is two-connected by the established edge-swap lemma. Deleting e4
in each module and joining the modules cyclically preserves two-connectivity
by the same vertex-deletion proof used for the four-port rings. At
r=1 the edge is restored; at r=2 both cross edges join distinct
vertices. Thus every T_r is two-connected.

## Verification scope

The local omission inequality and the all-r graph construction have
general written proofs above. Fixed-core enumeration is discovery
and verification only. The stated comparison1/24versus1/28 concerns
the previously proved family, without asserting historical priority.
The manuscript under journal review and upstream remain unchanged.

The [local Lean source](../formal/StarForming/CubicTriplePorts.lean)
has eight audited conditional count theorems. They check the six-port
deficiency consequences, the hard one-pair case from binary high/leaf/Y
variables and necessary local inequalities, the two-pair equality,
the all-pairs cap, additive omission accounting, the two-obstruction
module cap, and ring parameter/SF arithmetic. The
[formal receipt](../output/cubic-triple-port-formal-check.json) records
local Lean4.33.0, standard axioms only and sequential compilation after
memory and real-process preflight. The graph-to-count implications,
restoration symmetries, two-pair structural forcing and all-r graph
construction/connectivity are written proofs, rather than a complete
graph formalization.

The [independent controls](../output/cubic-triple-port-controls.json)
check all1,048,576subsets of the fixed core, including87,639dissociation
sets, exact deficiency identities and all64prescribed port patterns.
The independently computed maxima for exactly0,1,2,3omitted pairs
are12,11,10,9. Ten ring instances, r=1,...,10, pass literal formation,
all1,540selected deletion checks, the displayed dissociation witnesses,
both augmented exchange sizes26r, equality accounting and all2,640
vertex-deletion connectivity checks. Full48-vertex adjacency and
attainment/deletion selections for r=1 are included. Larger beta/SF
labels cite the written composition proof, not independent optimization.

Run `python3 scripts/check_cubic_triple_ports.py --output output/cubic-triple-port-controls.json`.
The [independent review request](reviews/2026-10-19-triple-port-compensation-review-question.md)
includes this proof and its complete four-port dependency. Its
[receipt](../output/cubic-triple-port-oracle-review.json) records ACCEPT
for the full new omission lemma and exact all-r graph theorem. The
[response](reviews/2026-10-19-triple-port-compensation-review-response.txt)
rechecks the four-port dependency, restoration and symmetry arguments,
all tight cases, separate module charges, attainment and connectivity.
Its optional shorter m=2 contradiction and explicit r=1 restriction
clarification are incorporated above. The established Heawood saturation
and cubic compensation theorems are specified inputs to that review.
