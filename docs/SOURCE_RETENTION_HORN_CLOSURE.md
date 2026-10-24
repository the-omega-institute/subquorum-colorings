# Exact source-retention closure and a least legal marked-source hull

20 October 2026. In ANY fixed finite complete feasible U/rotor fusion, the
feasible complete-source subfamilies are exactly the closed sets of a finite
system of implications

    retain i AND retain k  ==>  retain j.                 (1)

Every nontrivial rule involves THREE distinct original owners. In particular,
feasible source subfamilies are closed under arbitrary intersections, and any
prescribed seed has a UNIQUE least complete feasible extension. This provides
a legal way to retain occupied boundary owners without paying for individual
restored supports. It applies to all dimensions, phases, contacts and recurring
owners of the full model. It does not prove reserve monotonicity or the full
allocation inequality.

The crucial point is that an original support stays OCCUPIED whenever its
producer is retained, whether it is finally selected or consumed into a retained
endpoint. Adjacent restored supports do not provide an either/or repair:
consuming just one leaves the other selected beside both that occupied point
and its own anchor. The correct source dependencies are Horn implications,
not disjunctive choices between two consumers.

## 1. Exact hypotheses and the occupied-set identity

Fix the original complete source family F. Endpoints P_i are pairwise disjoint;
supports T_i do not belong to P_i. Each x in T_i has a unique original endpoint
anchor a_i(x), adjacent to x, and no other original occupied neighbor. The full
mandatory fusion is feasible. These are existing complete U/rotor properties;
no phase, width, height, port, freezing, contact-degree or source-count restriction
is added. The argument actually applies to any finite anchored source family
with these properties, not only U/rotor constructors.

For a retained owner set I write

    P_I = union_(i in I) P_i,
    T_I = (union_(i in I) T_i) minus P_I,
    O_i = P_i union T_i,
    O_I = P_I union T_I = union_(i in I) O_i.           (2)

The last identity is exact, even when I is infeasible. In particular retained
support production guarantees occupancy; it does not guarantee selection.
Optional extra selections are omitted, as in the source-only ledger: they lie
outside original receivers and have no endpoint neighbor. All original supports
and unchanged matching edges are retained in each subfamily.

## 2. Constructing all necessary three-owner rules

Take original owners i,k and vertices x,y such that

    x in T_i, y in O_k, x adjacent y, y != a_i(x).     (3)

In the full fusion x has the two DISTINCT occupied neighbors a_i(x),y. Hence
full feasibility forces x to be an endpoint. Endpoint uniqueness gives one
original consumer j with x in P_j. Introduce rule(1). If j=k the rule is a
tautology and may be dropped. The case j=i is impossible since T_i and P_i
are disjoint. The case k=i is impossible by intrinsic single-source feasibility.
Thus every remaining rule has three distinct owners.

The neighbor y may be an endpoint OR an original support of k. Its eventual
selected/consumed status is irrelevant to its occupation under retention of k.
This includes conflicts between two restored supports, and avoids the incorrect
assumption that retaining one of their consumers resolves the other selection.

Keep one rule for each unordered antecedent pair{i,k} and consumer j. All
geometric occurrences yielding the same rule impose the same owner obligation;
they are not separate payments. For s original sources there are at most
binom(s,2)*(s-2) distinct nontrivial rules, however long their occupied bands.
Each retained rule has an exact witness(x,y,i,k,j) in the original geometry.

## 3. Feasibility is equivalent to closure under these rules

Suppose the complete subfamily I is feasible. For a rule whose antecedents
i,k belong to I, both a_i(x) and y remain occupied by(2). If j were absent,
endpoint uniqueness would make x a selected mandatory support. Its two occupied
neighbors violate feasibility. Therefore j belongs to I.

Conversely suppose I satisfies every rule. Take any x in T_I and a retained
producer i. Its anchor a_i(x) remains an endpoint. If x had a second occupied
neighbor y, equation(2) supplies a retained k with y in O_k. The construction
in Section2 supplies consumer j and the rule{i,k}->j. Closure retains j,
which makes x an endpoint, contradicting x in T_I. Thus every selected point
has exactly its one original anchor as occupied neighbor. This proves complete
feasibility, including exclusion of selected-selected conflicts.

This is an equivalence about the actual original sources and actual mandatory
support set. No local profile relaxation, pair-feasibility assumption, allowed
support omission or finite geometric census appears in the general proof.

## 4. Arbitrary intersections and the canonical least extension

If every I_alpha is feasible, it is closed under(1). Whenever both antecedents
belong to their intersection, every I_alpha contains the consequent. The
intersection is therefore closed and feasible. The empty intersection is F,
which is feasible by hypothesis. This proves arbitrary intersection closure.

For any seed S, define Cl(S) as the intersection of all feasible subfamilies
containing S. Such subfamilies exist because F is one. Then Cl(S) is feasible,
contains S, and is contained in every feasible completion of S. Consequently
it is unique, monotone in S, and idempotent: Cl(Cl(S))=Cl(S).

It can be constructed without searching among subsets. Starting with S, retain
every consequent whose two antecedents are already retained, and repeat. Every
addition is forced in ANY feasible completion, by induction on the iteration.
At termination the set is closed, hence feasible. Since the source family is
finite, there are at most s-|S| strictly increasing rounds. The result is Cl(S),
independent of the order in which enabled rules were processed.

Each newly retained j has endpoint x adjacent to the already retained anchor
a_i(x). Hence, when each P_i is connected, adding forced sources preserves
endpoint connectedness of a connected seed. It never requires a disconnected
remote owner merely as a formal consequence without a physical endpoint contact.

## 5. A legal hull preserving all actual positive marks

Seed ALL original positive owners. For each of their actual marked canonical
sides, choose one fourth-neighbor witness w at a protector endpoint v and also
seed its original owner. Such w is an endpoint: if w were retained support of
a different source, it would have both v and its own distinct endpoint anchor
as occupied neighbors. Optional selections have no endpoint neighbor.

Take the least feasible hull of this seed. It has exactly the original positive
owners, since every positive owner was seeded and no source outside F is created.
Each chosen pair v,w remains an endpoint contact, preserving that actual mark.
Conversely its occupied set is a subset of the full occupied set by(2), so an
unmarked side cannot become marked. Thus N,G,n0,n1,n2 are all preserved, for any
choice of one actual witness per marked side. A different choice may give a
different hull; uniqueness refers to a FIXED seed, not to all witness choices.

This is a complete legal restriction theorem with preserved demand. It replaces
an arbitrary unsafe spatial cut by an actual feasible complete-source fusion.
It does NOT imply that the restricted reserve is at most the original reserve.
Without that additional signed inequality, proving allocation on this hull alone
would not prove allocation on F.

## 6. What the previous occupied-band obstruction becomes

For the concrete four-source obstruction of
[the previous note](SOURCE_CUT_BOUNDARY_PAYMENT_OBSTRUCTION.md), the complete
nontrivial rule set, with owners numbered1 through4, is

    {1,2}->3,  {1,3}->2,  {1,3}->4,  {1,4}->3,
    {2,3}->1,  {2,4}->1,  {2,4}->3,  {3,4}->1.

Every two-owner seed therefore forces all four original sources. The legal
subfamilies are exactly the empty set, the four singletons and the full family.
In particular retaining3,4 cannot legally avoid1,2, regardless of whether its
pointwise omission cost could be paid. The closure directly retains the actual
boundary consumers, without claiming an extra reserve unit for any rule.

Nine finite controls at lengths4,10,40 and widths8,10,14 give these SAME eight
rules while the number of geometric conflict occurrences increases. This is
finite verification of band compression, not a claim that those controls prove
the whole two-parameter assertion. The general bound in Section2 already shows
that a fixed number of original owners always has a bounded rule system.

## 7. Remaining signed-resource obligation

R is not monotone under legal retention in general. In the four-source example,
the sole phase10 source V4 has R=5, whereas the full four-source fusion has R=3.
Both are feasible; closing a larger seed can reduce reserve. Thus no monotonicity
of the closure SET can be used as monotonicity of the reserve COUNT.

Even preservation of positive demand does not supply a global monotonicity
theorem. Place the established seven-source marked-gate chamber far away. It
has N=1,G=2,R=6. Union it first with V4 alone and then with all four obstruction
sources. The two nested feasible fusions have the SAME N=1,G=2 and respectively
R=11,R=9, by exact endpoint-component additivity. These are two-component
examples, not a refutation of a stronger endpoint-connected statement or of the
target: their allocation margins are10 and8, both positive.

The full task remains 2(n2-n0)<=A+U0+Z0+H for arbitrary complete fusions. The
new legal hull handles retained boundary occupancy exactly. A successful proof
must additionally control the signed reserve change under closed extensions,
using actual common occurrences once; neither the number of rules nor the
number of newly retained sources is itself available reserve.

## 8. Verification scope

[SourceRetentionClosure.lean](../formal/SubQuorum/SourceRetentionClosure.lean)
formalizes the source predicates, exact occupied-set identity, two-neighbor
consumption, feasibility iff Horn closure, arbitrary intersection feasibility,
least feasible hull and its order properties. These are source-level graph
theorems, not conditional arithmetic substitutes for the main equivalence.
Constructor anchors/endpoint disjointness/full feasibility are explicit inputs.
Finite forward-iteration termination, connectedness and canonical-mark adapters
in Sections4--5 remain written proofs.

Run `python3 develop/check_source_retention_closure.py`. It compares direct
mandatory-support feasibility with the exact rule system on831 subfamilies of
existing complete fixtures. For fixtures through seven owners, all subsets are
checked and426 hulls are independently compared with intersections of ALL
feasible supersets. Larger fixtures use deterministic samples. The actual
positive-mark hull is checked for each fixture. No finite enumeration replaces
the general proof in Sections1--5, and no full allocation claim follows.

All11 source-level Lean4.33 declarations compile and pass the individual axiom
audit. Only propext, Classical.choice and Quot.sound appear as applicable;
six order/closure statements are axioms-free. See the
[formal receipt](../output/source-retention-closure-formal-check.json) and
[physical controls](../output/source-retention-closure-controls.json).
Independent written-proof review67bbc41f completed with ACCEPT. Its original
stream completed successfully and all21279 response characters match the task
response. This acceptance covers the written retention theorem, not independent
coordinate reconstruction of the examples. The physical three-owner reduction,
finite compression, constructor/mark adapters and finite iteration are written
proofs beyond the abstract Lean module. See the
[review](../output/source-retention-closure-review-response.md).
The separate full-target research573e88ad also completed and independently
recovered the Horn correction. Its connected source-cut proposal is independently
checked in the subsequent connected-obstruction note; it is not a proof of full
allocation or of a signed reserve bound.
