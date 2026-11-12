# Unbudgeted primary exchange cost is NP-complete

13 November 2026. This note settles the primary fixed-list optimization left
open by the earlier operation-budget and minimum-operation reductions. A
polynomial physical construction has minimum unit auxiliary matching cost
exactly equal to the source graph's vertex-cover number. Every partial batch
admits a whole-group rounding with no greater cost, and every batch yields
a source cover of size at most its cost. The result retains two-connected
bipartite physical graphs of minimum degree2 and maximum degree3, minimum
square-owner omissions and auxiliary components P2/P4.

The source problem is classical Vertex Cover. The construction and proofs
below are self-contained relative to its NP-completeness. No claim of a
literature-priority audit is made.

## 1. Domain and primary decision problem

Use disjoint physical layers I,X,C of sizes b,2b,2b. Helpers I are adjacent
to their respective pairs of witnesses in X, with no other helper edges.
Each witness has a distinct owner in C. Identify witnesses and owners by
indices V. Let P be the helper perfect matching on V, Q a matching of
witness-witness edges, and B the transported owner graph. Witness physical
colours agree on P and differ on Q/B; helpers and owners have the opposite
colour from their adjacent witnesses. The resulting graph is bipartite.
The ambient auxiliary graph A=P union Q has only paths and even cycles.

An omission U is permitted when B[V minus U] has maximum degree at most1.
Fix distinct candidates x_i in U to y_i outside U, one individually permitted
replacement per distinct owner component. All subsets and prefixes then stay
permitted, since the owner changes belong to disjoint components. Additions
may be adjacent to surviving old points. Define the unit matching cost

    C(S)=nu(A[U_S]),
    U_S=(U minus {x_i:i in S}) union {y_i:i in S}.

The decision asks whether some S has C(S)<=B0. **There is no operation-count
budget, no minimum-operation tie-break, and no final-isolation condition.**
The cost bound B0 is the primary decision threshold.

For any final tight auxiliary cover K, all b helpers, the owners outside
U_S, and the witnesses in U_S minus K form a physical dissociation set of
size3b-C(S). Its induced degrees are at most1: selected witnesses are
independent in P union Q and have no selected own owner, while selected
owners satisfy permittedness. This certificate interprets the cost; the
problem optimizes only the fixed list, not all permitted omission states.

## 2. Exact charged-group construction

**Theorem1.** Let H be any finite simple graph on h>=1 vertices, with m
edges. Put D=Delta(H)+2 and q=hD. A polynomial construction gives:

- b=2(q+h) helpers and a physical graph of order10(q+h), bipartite, minimum
  degree2 and maximum degree3;
- square owner components, a minimum-cardinality permitted initial omission,
  and q permitted replacements on distinct owners; all subsets are allowed;
- ambient auxiliary graph consisting only of P2/P4 components, and no edge
  between two addition endpoints;
- for every S, a polynomially computable set Z of touched source groups and
  a rounded whole-group batch S+ satisfying

      C(S+) = |Z|+|E(H-Z)| <= C(S);

- a source vertex cover computable from S of size at most C(S), and a batch
  of cost |T| for every source vertex cover T.

Consequently

    min over all S C(S) = tau(H).

If H is connected and bridgeless, the physical graph is two-connected. The
one-vertex edgeless source also satisfies that conclusion. Initially C=m;
selecting all q operations gives C=h, so a greatest batch need not be optimal.

### Labels, colours and owner squares

For each v in H, form a cyclic group L_v of D labels, one incidence label
(v,e) per incident edge, followed by enough dummy labels. Every group has
at least two consecutive dummy labels. Globally index the q labels by i.
Write succ(i),prev(i) for cyclic successor/predecessor in its group.
Introduce witnesses x_i,y_i,z_i,w_i. Initially all x and z lie in U;
candidate i replaces x_i by y_i. Put

    P contains y_i--x_succ(i),
    Q contains x_(u,e)--x_(v,e) for each e=uv in H.

Assign the two x-incidences of each edge opposite physical colours, and give
dummy x's colour0. Give y_i the colour of x_succ(i). This makes these
P-edges monochromatic and Q a bichromatic matching.

Complete colours and P within each group. If x_i,y_i have the same colour c,
give both z_i,w_i colour1-c. At labels where x_i,y_i differ, assign z_i,w_i
opposite colours, choosing z-colour0 at half these labels and1 at the rest.
The number of changes around a cyclic binary word is even. Thus every
four-point block has two of each colour. Within each group the number of
z-points of each colour equals the number of w-points of that colour; pair
same-colour z's and w's to complete P. Order the four owner indices of each
block as an alternating square. All P,Q,B physical-colour requirements hold.

For group v, let rep_v be the penultimate dummy label, followed by its final
dummy label. Both x_rep and y_rep have colour0; z_rep,w_rep have colour1.
The index x_succ(rep) has no old Q-edge.

### The charging and zero-cost connections

For each source vertex v add four witnesses u_v,v_v,p_v,t_v with physical
colours1,1,0,0, P-pairs(u_v,v_v),(p_v,t_v), and owner square(u_v,p_v,v_v,t_v).
Initially add u_v,p_v to U. Add two Q-edges

    y_rep--u_v,       w_rep--t_v.

The old endpoints had no Q-edges, so Q remains a bichromatic matching.
There are now4(q+h) witnesses,2(q+h) helpers and4(q+h) owners. Every owner
square has two omissions, which is minimum: any three retained vertices of
a square contain a degree2 point, whereas any two retained vertices are
permitted. All old candidates retain this property in their own distinct
squares, and the new squares have no candidates.

The first new Q-edge joins two P2s into

    x_succ(rep) -- y_rep -- u_v -- v_v.

Since u_v is fixed present and v_v fixed absent, its exact induced matching
cost is the representative bit s_rep, independent of s_succ(rep). The second
new Q-edge gives

    z_j -- w_rep -- t_v -- p_v,

where z_j is the P-partner of w_rep. Both middle points stay absent and both
ends stay present, so its cost is0. All remaining padding pairs have z
present and w absent. The old edge-incidence components are P4s, all other
old x/y components P2s. Thus the whole ambient auxiliary graph is P2/P4.
No new Q or P edge joins two candidate additions y_i.

### Exact cost ledger and rounding

Write s_i=1 iff i is selected. The original x_i point is present iff s_i=0,
while its P-neighbour y_prev(i) is present iff s_prev(i)=1. Put

    r_i=(1-s_i)s_prev(i).

On an old Q component with incidence labels i,j, the P4 is

    y_prev(i) -- x_i -- x_j -- y_prev(j).

Its exact induced matching cost is

    r_i+r_j+1_{s_i=s_j=s_prev(i)=s_prev(j)=0}.                 (1)

If both r's are1, the two P-edges give two disjoint matching edges. If
exactly one is1, its P-edge gives cost1 and the middle edge cannot add a
disjoint second edge. If neither is1, only a middle edge with both x's
present can contribute, giving the last indicator. This proves1 in every
case. An old non-Q P2 contributes r_i. Each charged component replaces
precisely r_succ(rep) by s_rep, and its successor is a dummy, so no original
Q component is changed. Summing disjoint auxiliary components gives

    C(S)=sum_v G_v(S)+sum_{e=uv} epsilon_e(S),               (2)
    G_v=s_rep_v+sum_{i in L_v, i!=succ(rep_v)} r_i,
    epsilon_e=1_{both incidence labels and predecessors have bit0}.

This ledger is global. When a Q component uses two P-edges, they are distinct;
its middle-edge indicator is charged only when both P contributions vanish.
The charging and zero-cost components are separate. Nothing is paid twice.

Let Z={v:S intersects L_v}. Then G_v>=1 for every v in Z. If s_rep=1 it is
immediate. Otherwise a nonempty proper cyclic selection has a selected-to-
unselected boundary. That boundary cannot be the removed term, whose tail
rep has bit0, so a remaining r_i is1. A full group has G_v=1, an empty group
G_v=0. Every edge of H-Z has epsilon_e=1. Therefore

    C(S)>=|Z|+|E(H-Z)|.                                    (3)

Round every touched group to fully selected. Formula2 now gives exactly
|Z|+|E(H-Z)|, proving the claimed no-increase rounding. This rounding can
increase the operation count, which is why no operation budget is imposed.

Add one endpoint of every uncovered edge of H-Z to Z. The resulting source
cover has size at most |Z|+|E(H-Z)|<=C(S), constructed in polynomial time.
Conversely, select all labels of a source cover T. Formula2 gives cost|T|.
Taking a minimum source cover proves min C=tau(H). An optimal touched set Z
need not itself cover H; the endpoint completion is part of the decoding.

### Physical connectivity

Within one source group, choose a path between the distinct x/y owner ports
in each owner square. Together with the helper-subdivided y_i--x_succ(i)
links these paths form a cycle; D>=2, and D=2 uses two different joining paths.
The other port-to-port path in each square is an ear. Thus this backbone
contains every owner and every x/y witness and their helpers, and is
two-connected. Each remaining z_i--w_j helper path is an ear between distinct
owner vertices already in that backbone, so its group module remains
two-connected and includes all old vertices of that group.

The only edges between old group modules are the Q-edges representing H.
Deleting one physical vertex preserves each module and destroys at most one
intergroup Q-edge, since Q is a matching. Connectedness and bridgelessness of
H keep this quotient connected. For a single source vertex the group module
alone is two-connected.

Each new ten-vertex module is an owner square with two helper-path ears, so
it is two-connected. Its two joining Q-edges have distinct endpoints on both
sides: old y_rep,w_rep and new u_v,t_v. A single vertex deletion preserves
both interiors and at least one join. Adding these modules therefore preserves
two-connectivity. Helpers and non-Q witnesses have degree2, Q witnesses and
owners degree3; the prescribed colours prove bipartiteness. QED.

## 3. Connected and bridgeless source normalization

**Lemma2.** For any finite simple graph F on h0>=0 vertices, a polynomial
construction gives a simple connected bridgeless J and an explicit integer
R such that

    tau(J)=tau(F)+R.

It also lifts every F cover T to a J cover of size|T|+R, and projects every
J cover C to an F cover of size at most|C|-R, without solving either problem.

**Proof.** Add an apex adjacent to all h0 original vertices and h0+2 new
leaves, forming F+. A cover omitting the apex contains all original vertices
and leaves, of size2h0+2. The apex plus all original vertices gives sizeh0+1,
so a minimum cover contains the apex and tau(F+)=tau(F)+1.

Let m+=|E(F+)|. Replace every edge uv by two internally disjoint length3
paths u-a-b-v and u-c-d-v. The resulting J is simple and connected, and each
edge lies on its gadget's six-cycle, so J is bridgeless. Fix a subset Z of
the original F+ vertices. Each path requires one internal vertex if at least
one endpoint is in Z, and two if neither is. Hence the minimum cover size
with that fixed Z is

    2m+ + |Z| + 2|E(F+-Z)|.                               (4)

Adding an endpoint of an uncovered F+ edge costs1 and removes a penalty of
at least2. Minimizing4 therefore gives tau(J)=2m+ +tau(F)+1. Set R=2m+ +1.

For an explicit lift, take T plus the apex. Every F+ edge is covered. On
each length3 path choose its internal vertex adjacent to an unselected
endpoint if one exists, and either internal vertex when both ends are
selected. This adds exactly2m+ vertices and proves the lifting formula.

For projection, let C be any J cover and Z its subset on the F+ vertices.
For each F+ edge initially uncovered by Z, C contains all four internal
vertices of its two paths; otherwise it contains at least two. Thus
|C|>=|Z|+2m+ +2u, where u is the number of initially uncovered edges. Add one
endpoint for each remaining uncovered edge to obtain a cover Z' of F+ with
|Z'|<=|Z|+u<=|C|-2m+. If the apex is absent, this cover contains all original
vertices and leaves; replace it by apex plus all original vertices, which
cannot increase its size. Remove the apex and discard leaves. The remaining
F cover has size at most|C|-(2m+ +1)=|C|-R. QED.

## 4. Primary NP-completeness and parameter boundary

**Theorem3.** Deciding whether some batch has C(S)<=B0 is NP-complete in the
fixed-list domain of Theorem1, even with a two-connected bipartite physical
graph of minimum degree2 and maximum degree3, minimum square omissions,
P2/P4 auxiliary components, and no edge between two additions.

**Proof.** From Vertex Cover instance(F,t), construct J,R by Lemma2 and
apply Theorem1 to J. Its unbudgeted optimum is tau(J)=tau(F)+R. Set primary
cost threshold B0=t+R. This is a polynomial reduction; no operation-count
constraint is encoded or used. It also decodes any batch into an F cover
of size at most C(S)-R by the two constructive cover maps.

Membership in NP is direct. A candidate batch determines U_S in polynomial
time, permittedness is checked from owner degrees, and an auxiliary cover
of size at mostB0 certifies nu(A[U_S])<=B0. Bipartiteness also permits exact
cost computation in polynomial time. The stated structural restrictions
are polynomially checkable. QED.

This closes the primary fixed-list complexity question left by the preceding
[operation-budget reduction](MIXED_ISOLATED_REPAIR_AND_OPERATION_HARDNESS.md).
The earlier isolation-feasible primary maximum-saving result remains valid:
the present domain allows the new representative addition to meet a fixed
present neighbour. Forcing final isolation would exclude the charging route.

The [cycle-rank algorithm](COMPONENT_CYCLE_RANK_FRONTIER.md) also remains
consistent. For this construction, if H has c_H connected components, the
candidate component multigraph has cycle rank m+c_H. Before the original
Q-edges merge incidence auxiliary vertices, its nontrivial part is one
label cycle per source vertex. The m Q-edges merge distinct incidence pairs;
its core has q-m vertices and c_H connected components. The q padding
components are isolated candidate vertices. New charging connections only
extend old components with new, noncandidate endpoints. Thus the total
candidate vertex count is2q-m, its connected-component countq+c_H, and its
cycle rank is q-(2q-m)+(q+c_H)=m+c_H. This grows in the hardness family.

## 5. Reproduction and scope

Implementation: [primary_exchange_hardness.py](../develop/primary_exchange_hardness.py).
Run the complete assertion-enabled checker:

```sh
python3 -B scripts/check_primary_exchange_hardness.py
```

Its independent augmenting-path matching routine checks every tested cost
and rounded cost. It enumerates every source graph through4 vertices, every
batch when q<=12 and120 seeded batches per larger small-source model, plus
all whole-group batches. It verifies actual auxiliary matching/cover pairs,
physical dissociation sets, owner permission, colours, component types,
cycle ranks and source-cover decoding. Literal vertex deletion calibrates
iterative articulation checks, which support larger physical normalization
instances. Source-cover enumeration and independent cover branching test
the normalization; every lifted and projected cover is checked directly.
All-size conclusions depend on the proofs above, not extrapolation.
The [report](../output/primary-exchange-hardness-check.json) holds aggregate
counts, a digest and a triangle-source coordinate/certificate example,
not every batch row. The [audit receipt](../output/primary-exchange-hardness-review.json)
records frozen identity and actual independent original-checker execution.

The result is a computational boundary for a fixed replacement list and its
unit matching cost. It does not prove hardness of optimizing all helper
omission states, unrestricted SF/beta graph parameters, weighted TH routing
or rectangular grids. The physical certificate is a valid all-helper set,
not a claim of unrestricted beta-optimality. Universal8b/3, remaining sharp
degree/regularity parameters, optimal composition constants, compatible
physical multi-Hall routing, the unit5/6 improvement and arbitrary-width grid
triple equality remain open in the full ACTIVE goal. October's submitted
manuscript is preserved; no Lean execution, email or submission is involved.
