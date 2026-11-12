# Choosing the initial matching and combining both removal sides

Initial matching choice can be eliminated by one constrained bipartite
matching test for a prescribed batch and initial minimum cover. The same
criterion works when the batch removes points both inside and outside that
cover. Every destroyed initial matching edge is charged once, even if both
endpoints are removed. This unifies the two earlier one-sided certificates.

A two-connected 30m-vertex unit-cost family separates the unified rule from
both one-sided rules at every scale. A second family shows that even choosing
all initial minimum covers and maximum matchings does not make the unified
inherited-cover rule complete for the actual fixed-list problem.

## Tight initial pair and edge ownership

Let A be a finite simple graph, U a subset of its vertex set, and G=A[U].
Supply a vertex cover C and matching M0 of G with |C|=|M0|=nu0. Put I=U-C.
The supplied pair certifies optimality by weak duality, even if G is not
bipartite. Every maximum matching M has exactly one cover endpoint per edge
and saturates C; I is independent. Edges inside C are allowed.

Let X be any subset of U and Y any subset outside U with |X|=|Y|. Write
U'=(U-X) union Y. For a maximum initial matching M define

$$
 D_M(X)=\{c\in C:\text{the M-edge at c meets X}\},\qquad
 M'=\{e\in M:e\cap X=\varnothing\},\qquad C'=C\setminus D_M(X).
$$

The points in C intersect X automatically belong to D_M(X), so C' is a
subset of U'. If C' covers A[U'], then

$$
 \boxed{\nu(A[U'])=|M'|=|C'|=\nu_0-|D_M(X)|}.             \tag{1}
$$

Indeed the destroyed matching edges correspond bijectively to their cover
endpoints in D_M(X); the surviving matching and cover give equal lower and
upper bounds. An edge with two removed endpoints still occurs only once.
Unmatched removals consume no edge credit. This certificate subsumes the
inside-cover final-isolation rule and the outside-cover credit rule for a
fixed initial pair, while allowing further final edges whenever C' covers them.
It is a direct use of matching weak duality, not a new duality theorem.

## Forced retirement and a polynomial matching-choice test

For c in C, let N_I(c) be its neighbours in I in the initial graph G. Set

$$
 D=(C\cap X)\ \cup\
   \{c\in C\setminus X:N_I(c)\subseteq X\},\qquad K=C\setminus D.       \tag{2}
$$

Construct a bipartite graph H_X with sides C,I, using all initial cross
edges except those from K to X intersect I. Edges inside C do not belong to
H_X. The initial tight certificate implies that every cover vertex has an
initial neighbour in I.

**Theorem 1 (all initial matchings, fixed C and batch).** Some maximum initial
matching M makes the inherited cover C-D_M(X) cover A[U'] if and only if:

1. K covers A[U']; and
2. H_X admits a matching saturating C.

Whenever such a matching exists, every feasible initial matching retires
exactly D, and the final cost is exactly |K|. Thus the retirement set and
credit are determined by C,X, not by the choice among feasible matchings.
A successful test returns an initial matching, final matching, cover and
one-time edge charges. Failure returns either an uncovered final edge or a
Hall set S in C with |N_HX(S)|<|S|.

**Proof.** Suppose an initial matching M gives a valid inherited cover.
Every c in C intersect X is retired. If c survives but its M-mate is removed,
then c is retired while remaining in U'. Any initial neighbour in I-X also
survives and never belongs to the inherited cover. Such a neighbour would
leave their edge uncovered. Therefore every retired surviving c has all its
I-neighbours in X.

Conversely, if a surviving c has every I-neighbour in X, its mate in any
maximum matching lies in X, so it must retire. Together these observations
prove D_M(X)=D. The inherited cover must consequently be K. Each c in K
survives and is not retired, so its matching edge cannot meet X; M uses only
allowed edges of H_X and saturates C. This proves necessity.

For sufficiency, take a C-saturating matching M in H_X. It has |C|=nu0 edges
of the initial graph, so is a maximum initial matching. Every c in D is
removed itself or has all I-neighbours removed, hence its M-edge meets X.
Every c in K survives and is matched outside X by H_X's edge restriction.
Thus D_M(X)=D. Delete the |D| destroyed edges. The surviving matching and
assumed cover K have the same size |K| and certify (1). ∎

A standard augmenting-path algorithm solves the cross matching problem in
polynomial time. In a failed search from an unmatched left vertex, let S be
the reachable left set and T the reachable right set. Exhausting the search
gives N_HX(S)=T and |T|<|S|. The implementation returns these actual point
sets. The Hall certificate belongs to the constrained initial graph H_X;
it is not asserted to be a Hall deficiency of the physical final graph.

**Outside-cover specialization.** If X is a subset of I, condition 2 is
equivalent to saturating K into I-X. Necessity follows by retaining only
M's edges at K. Conversely take any initial tight matching M0. Its edges at
D match D into X. Unite those edges with a matching saturating K into I-X;
the endpoints are disjoint and the union saturates C. This proves the
preliminary smaller matching-choice criterion.

With removals in C allowed, the matching at a removed cover point can use
points of I-X. The full H_X test handles this competition, rather than
independently allocating those points to several parts of the certificate.

## An initial matching can block a useful zero-credit prerequisite

For a concrete generic example, use the initial path 0-1-2-3-4 and disjoint
edge 6-7, with U={0,1,2,3,4,6,7}, C={1,3,6}. Add ambient edge 0-9 and
candidate operations 0→8, 7→9. Point 8 is isolated.

The initial matching {01,23,67} makes removal 0 retire 1 while point 2
survives, so that candidate is blocked. The other candidate depends on it,
and the fixed-pair rule earns no credit. Theorem 1 instead chooses matching
{12,34,67}. Removal 0 now has zero credit but enables 7→9; that removal
retires 6. Final cover {1,3} and matching {12,34} certify cost two instead
of three. This is a source-level example, not a claim about a new graph-gap
extremizer. Both removed endpoints of one edge are tested separately by the
four-vertex control U={0,1}, M={01}, X={0,1}, Y={2,3}: credit is one.

## Exact search over all initial pairs for specified physical candidates

Use the established helper/witness/owner model. There are b helpers, 2b
witness/owner indices, auxiliary graph A=P union Q and owner graph B. P is a
perfect matching, Q a partial matching, so A has maximum degree two and only
alternating even cycles. Physical colours need not be an A-bipartition.
An omission U is permitted if B[V-U] has maximum degree at most one.

Specify at most one individually permitted replacement per connected owner
component. Every candidate subset and every sequential prefix is therefore
owner-permitted; the theorem certifies matching cost only at its endpoint.
It does not establish a nonincreasing execution schedule for arbitrary batches.

Enumerate all minimum covers C of A[U], using the complete path/even-cycle
catalogue. For each cover enumerate all candidate subsets and apply Theorem 1.
In the outside-only mode, omit subsets whose removal meets C. In mixed mode,
removals can lie anywhere in U. Choose the largest |D|, then the fewest
operations. If there are L initial minimum covers and q candidates, this
requires at most L times 2^q polynomial work; L itself can be exponential.
No initial maximum matchings need to be enumerated. Every certified batch
for every initial pair is considered, since Theorem 1 is necessary and
sufficient for its fixed cover and subset. This proves exact optimization
within the corresponding inherited-cover rule, including the operation-count
tie-break. It does not optimize arbitrary final covers.

The final cover K, surviving matching and permitted omission construct an
actual dissociation set: select all b helpers, witnesses indexed by U'-K,
and owners indexed by V-U'. Its size is 3b-|K|. Matching independence
prevents two selected witnesses at one helper or a selected witness Q-edge;
owner permittedness and disjoint witness/owner indices handle the rest.
The algorithm runs no matching optimization on the final graph. The checker
may solve such problems independently to validate its certificates.

## A uniform separation between one-sided and mixed batches

For every integer m≥1, take 12m indices v_(j,t)=12j+t, b=6m, with
A=C_(12m) in its consecutive cyclic order. P consists of consecutive even-odd
pairs, Q of the complementary odd-even edges. Give index v physical colour
floor(v/2) modulo 2. In each block the owner squares, in cyclic order, are

$$
 (v_0,v_2,v_1,v_{11}),\qquad
 (v_4,v_6,v_9,v_3),\qquad
 (v_8,v_{10},v_5,v_7).                                  \tag{3}
$$

These partition the block and alternate physical colours. Set

$$
 U\cap V_j=\{v_1,v_2,v_3,v_6,v_7,v_8\},\qquad
 C\cap V_j=\{v_2,v_7\}.
$$

The initial graph consists of 2m three-vertex paths, so the cost is 2m
and C is its unique minimum cover. There are exactly two initial omissions
in each square, the minimum needed. Specify, in the three distinct squares,

$$ v_1\mapsto v_0,\qquad v_3\mapsto v_4,\qquad v_7\mapsto v_{10}.       \tag{4} $$

**Theorem 2.** On these candidates, the best outside-cover inherited batch
has cost m even after all initial matchings are allowed. The earlier
inside-cover, final-isolating exact-deletion rule also has best cost m.
The mixed inherited rule attains zero, and the exact all-helper value is
beta_I=18m.

**Proof.** An outside-cover batch cannot use the third operation, because
v_7 belongs to the unique minimum cover. Its path v_6-v_7-v_8 remains and
costs one per block. Choosing the first two operations together retires v_2
and removes the first path's cost; the additions v_0,v_4 are isolated in
the endpoint. This attains cost m.

An inside-cover batch cannot use the first two operations. The first path
then remains and costs one per block. Choosing every third operation deletes
v_7 and adds isolated v_10, attaining m. The uniqueness of C excludes another
initial cover that could evade either restriction.

Choosing all three operations leaves exactly the even indices. All cover
points are retired, final matching and cover are empty, and the physical
omission is permitted. For example use initial matching v_1-v_2 and
v_6-v_7 in every block: its two edges are destroyed once each; removal v_3
contributes no additional matching-edge charge. Hence the all-helper value
is 3b=18m, also its universal upper bound. ∎

For a subset containing labels a_j,b_j,c_j of the three operations in block j,
its actual endpoint cost is

$$
 \sum_j\bigl(1-\mathbf1_{\{a_j,b_j\}\subseteq S}\bigr)
 +\sum_j\bigl(1-\mathbf1_{c_j\in S}\bigr).               \tag{5}
$$

With neither of a_j,b_j selected, the first part is a three-vertex path.
With just one selected, it is an edge plus isolate, still of cost one;
with both it is independent. The second path disappears exactly when c_j
is used. No selected edge joins these blocks or parts: their unused adjacent
indices separate them. This proves (5). Applying two one-sided rules in
successive stages can also reach zero; Theorem 2 compares single batches
from the specified initial omission, and does not assert iterative failure.

## A uniform Hall obstruction that survives mixed removal and pair choice

Use the same auxiliary cycle, colours and b=6m, but owner squares

$$
 (v_1,v_7,v_0,v_2),\qquad
 (v_5,v_{11},v_8,v_3),\qquad
 (v_4,v_6,v_9,v_{10}).                                   \tag{6}
$$

Let U in each block be {v_1,v_2,v_3,v_4,v_5,v_9}; its graph is a five-vertex
path plus an isolate. The cost is 2m and the unique minimum cover consists
of v_2,v_4 in every block. Candidates are v_1→v_7 and v_5→v_11, in the
first two squares of (6). Every square again has two initial omissions.

**Theorem 3.** Even after every initial minimum cover and maximum matching is
allowed, the best mixed inherited-cover certificate has cost 2m. The actual
minimum over these candidate subsets is exactly m. The additive gap m is
unbounded on this two-connected unit-cost family.

**Proof.** All candidate removals are outside the unique C, and the surviving
point v_3 remains adjacent to both v_2,v_4. Hence D is empty for every subset.
Any applicable inherited certificate therefore has unchanged cost 2m; the
empty subset proves attainability within the rule. More specifically, when
both endpoint removals occur in a block, K contains {v_2,v_4} but their only
available neighbour in H_X is v_3. This is an explicit 2-versus-1 Hall
certificate ruling out every initial matching, not just a particular choice.

The actual endpoint cost in a block is two until both operations are selected:
its five-vertex path becomes a four-vertex path after a single endpoint swap,
and a three-vertex path after both. The additions and v_9 remain isolated,
and no selected edge connects blocks. Thus

$$ \nu(A[U_S])=2m-\#\{j:\text{both block-j operations are selected}\}. $$

The minimum is m. At the full batch, a final cover is {v_3:all blocks}, with
matching {v_2-v_3:all blocks}. These supply a complete physical certificate
of size 17m. No equality beta_I=17m over arbitrary omissions is asserted. ∎

Both families have physical order 5b=30m, minimum degree two and maximum
degree three. Their helper/witness core is a cycle with every P-edge subdivided;
each owner square has four distinct attachments to it. Deleting a core point
leaves a connected path and at least three attachments per square; deleting
an owner leaves its square as a connected three-owner path attached to the
intact core. This proves two-connectivity at every m. The explicit colours
prove bipartiteness, including the cycle wraparound.

The original cost 2m already meets the all-helper 8b/3 target, since
3b-2m=16m=8b/3. These families separate certificate methods and do not refute
that target or establish a better universal numerical bound.

## The fourteen stored gaps and verification scope

The preceding fixed-pair milestone preserved fourteen seeded physical cases
where its answer exceeded the actual specified-list minimum by one. Their
full coordinates and candidates are now a fixture. Allowing every initial
cover and matching while retaining outside-only removals closes twelve of
these gaps. Two remain: (auxiliary order12,trial12) and (order64,trial0).
Allowing mixed removals closes all fourteen, with explicit initial/final
matching and cover witnesses in the report. These are statements about the
stored benchmark, not a completeness theorem for arbitrary physical inputs;
Theorem 3 already gives uniform failures of the broader rule.

The checker evaluates every candidate subset to obtain the exact endpoint
minimum independently. For cover-choice searches it safely prunes any subset
whose endpoint cost cannot improve the already certified old bound. Each
stored gap is exactly one, so it suffices to search every improving subset
and minimum cover until an actual-cost witness is found, or exhaust them to
prove no certificate improvement. Source/report counts distinguish the checks
actually performed from a hypothetical full L times 2^q execution.

Run the original assertion-enabled checker:

```sh
python3 -B scripts/check_matching_choice_exchange.py
```

The report checks 10,960 generic batch models with literal enumeration of all
maximum matchings: every simple ambient graph through four vertices and its
tight covers, both removal modes, plus 120 larger seeded models and explicit
controls. It checks 689 small cross graphs and returned Hall witnesses;
7,487 successful matching reconstructions and 7,797 feasible initial-pair
certificates are independently scored. It also compares ninety physical
all-pair optimizer calls, including minimum-operation tie-breaks, with 2,354
literal pair/batch tests, and constructs 122 physical dissociation certificates.

Each new family is checked at sixteen scales through m=128. The common-neighbour
family has all 340 subsets through m=4 checked; the mixed family has all 584
subsets through m=3 checked. There are 348 explicit connectivity deletion
checks in the common-neighbour family; arbitrary-scale connectivity for both
families relies on the proof above. The stored fourteen cases add 1,912
endpoint-subset scores and 21,595 constrained matching-choice tests. All-scale
claims rely on the arguments, not on these finite checks.

The independent exact-source audit and its actual execution scope are recorded
in [the review receipt](../output/matching-choice-exchange-review.json).
No Lean or priority review is claimed. Universal8b/3, sharp graph-gap constants,
compatible general multi-Hall routing, a universal unit5/6 improvement and
arbitrary-width rectangular-grid triple equality remain in the full ACTIVE goal.
