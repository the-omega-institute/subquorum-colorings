# Freezing forces short-beta pocket guards; cyclic blocks eliminate exactly

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

We prove a local geometric consequence of complete freezing. A horizontal
two-endpoint beta with alpha TP tips immediately beyond both ends must have
two **PP columns in the adjacent band** on its other side. The PP guards
need not be assumed. If a guard were BP, its forced actual mate would
create a two-endpoint closed freezing dependency. This recognizes filled
guarded pockets directly from the current board, without a construction
history or a search template.

Every such beta is one exclusive whole resource incident to its two alpha
owners. Non-tree components of their multigraph can therefore be eliminated
from the full whole-support compensation problem, retaining all exterior
sharing. Maximum payment splits exactly. If the component alphas have no
direct interval support, minimum links split exactly too, at one link per
removed source. This applies to genuine **beta resource cycles**, not to
zero-credit pure PP/M cycles. Universal compensation and 5/6 remain open.

## 1. Short beta between two alpha ends

Use a finite feasible actual matching (T,M) with completely frozen endpoints
P and fixed aligned two-row bands. The full strict freezing certificate may
use vertices anywhere on the board. A retained neighbor of p is selected,
or an endpoint w with rank(mate(w))<rank(p). A freezing event uses two
different nonmate retained neighbors.

Normalize the band orientation so that the beta's two endpoints are

    a=(r,s-1), u=(r,s), v=(r,s+1), b=(r,s+2),

where r is even, uv is the actual matching edge, and the lower band partners
of u,v are blank. Thus {u,v} is an entire original beta, with no internal
PP vertex. Assume a,b are TP tips of original alphas A,B, which may coincide.
The selected partners of a,b are (r+1,s-1),(r+1,s+2). Define

    a*= (r-1,s-1),   h= (r-1,s),   k= (r-1,s+1),  b*= (r-1,s+2),
    a**=(r-2,s-1),  h*= (r-2,s),  k*= (r-2,s+1), b**=(r-2,s+2).

Points outside the board are blank. The proof will in particular force
h,k,h*,k* to lie inside it. Reflections, and isometries carrying the band
convention, give the other orientations.

**Theorem 1 (forced PP guards).** Both {h,h*} and {k,k*} are PP columns.
Moreover h is retained at u and k at v in every strict freezing certificate:

    rank(mate(h))<rank(u),   rank(mate(k))<rank(v).          (1)

**Proof.** An alpha TP tip has its actual mate across the band boundary.
Indeed a horizontal mate would have a blank band partner, by feasibility
at the TP selection, and would terminate that original strand at BP rather
than its required other TP. Hence mate(a)=a* and mate(b)=b*.
The points a**,b** are occupied: a*,b* are either internal PP vertices or
the opposite TP ends of their original alpha paths, never BP ends.

The only possible nonmate occupied neighbors of u are a and h, since
v is its mate and its lower partner is blank. Both must be retained. In
particular h is occupied. It cannot be selected because it sees the two
different endpoints u and a*. Thus h is P. Likewise k is P and retained
at v. This proves (1).

Suppose h* is not P. It cannot be selected either: it would see h in P
and the different occupied point a**. Thus h* is blank. Every possible
actual mate of h is now excluded except k: u already matches v, a*
already matches a, and h* is blank. Therefore mate(h)=k and mate(k)=h.

At h the only nonmate occupied neighbors are a* and u, so u must be
retained. Since mate(u)=v, rank(v)<rank(h). At v the only nonmate occupied
neighbors are b and k, so k must be retained. Since mate(k)=h,
rank(h)<rank(v). This is impossible. Therefore h* is P. Reflection of
the same argument proves k* is P. QED.

The obstruction is the closed pair {h,v}: each member needs another
member of that pair to freeze strictly earlier. Arbitrary exterior ranks
cannot supply extra grid neighbors or resolve this cycle. The theorem
does not assume a bound on freezing depth or uniqueness of M.

## 2. The recognized beta is an exclusive pocket resource

**Corollary 2.** The beta {u,v} has empty whole-body interval support. Its
only declared incoming TP--BP links are a->u and b->v.

**Proof.** Its original body consists only of u,v. Each endpoint's own
band column is P-containing, and its two horizontal neighboring columns
are the other beta column and a fixed alpha TP column. It borders no
endpoint-free gap and has no eligible original interval support. The
nonmate neighbors of u are a,h and its blank lower partner. By Theorem 1,
h is internal PP, so only a can be a TP tip. Similarly only b can enter
v. QED.

Thus it is a filled guarded pocket of the preceding notes. We have not
proved that deleting its actual edge leaves a completely frozen board.
Recognition uses the current configuration; it must not silently be
replaced by an assumed monotone completion history from a frozen empty
pocket. Deleting the edge preserves feasibility, but may destroy freezing.

## 3. The actual short-beta resource multigraph

Construct H on the original alpha owners. Include **every** horizontal
two-endpoint beta with the two neighboring alpha TP tips of Theorem 1;
its distinct original beta identity is an edge between those owners.
Keep loops and parallel edges. Other betas, mixed paths, intervals and
source exits remain exterior. The theorem permits bending alpha paths
and occupied adjacent bands of arbitrary extent elsewhere.

In each connected component C, let n_C be its alpha count and m_C its
short-beta edge count. A component with m_C>=n_C is not a tree; a single
alpha with a loop and two alphas with two parallel beta edges are included.
Every such component has an injective assignment of all its n_C sources
to n_C incident whole beta resources: choose a spanning tree and one extra
edge, root at an endpoint of that extra edge, give it to the root and give
every other vertex its parent edge. A loop can be the extra edge.

Each assigned incidence has its actual one-link witness from Corollary 2.
No two sources spend the same beta, and no source chooses two links.
These are ordinary beta stems; no beta-body interval is spent. This is
the established tree/cycle resource allocation applied to resources whose
required grid guards are now proved from freezing.

## 4. Exact elimination in the full exterior system

Choose any collection of these non-tree components. Let S be their alpha
sources, J all their internal short betas, and write n=|S|, m=|J|.
Delete S and J and their incident links from the whole-support network.
Keep every original interval identity and all other original owners,
supports, actual BP entry capacities and links. Let V_res,c_res be its
maximum payment and minimum links at that value; let V,c be the original
optima. No exterior source-separation assumption is imposed.

**Theorem 3 (closed cyclic-block elimination).** For both ordinary and
full beta-fork compensation,

    V=n+V_res,          c_res<=c<=n+c_res.                  (2)

If W(a) is empty for every a in S, the cost identity strengthens to

    c=n+c_res.                                            (3)

The projection can preserve every paid outside source identity. It need
not preserve all old used resources, literal paths or fork decompositions.

**Proof of payment.** The local assignment of Section 3 pays all n sources
using only their internal betas. A residual packing extends by these n
stems, proving V>=n+V_res.

Conversely, an outside source path cannot enter an alpha owner. It cannot
enter any beta in J either: every incoming link is directly from one of
its two alpha owners in S. Consequently every primitive using a beta in
J has its source in S, and these beta bodies have no interval exits or
fork resource. Remove all paths rooted in S from any full packing. Keep
every outside path. If a removed S arm shared an exterior beta fork with
an outside arm, keep the outside arm as a stem to that same whole beta,
releasing the fork interval. The standard free beta normalization retains
its source and links. The outside packing lies in the residual system.
Thus the original payment is at most n+V_res, proving equality.

Every maximum packing pays all n sources in S: otherwise replacing its
S-rooted part by the n local stems, while retaining outside paths, would
increase value. Dropping the S paths from a minimum-cost maximum gives
a residual maximum at no greater cost, so c_res<=c. The initial extension
has cost n+c_res, proving the upper bound in (2).

**Proof of exact cost under empty support.** Every paid a in S then needs
at least one actual outgoing link. Ordinary paths have distinct source/
mixed owners; fork arms share only their terminal beta body and no links.
Removing all n S-rooted paths therefore removes at least n distinct
positive-cost links. Normalizing any remaining fork arms costs nothing.
The residual maximum costs at most c-n, so c_res<=c-n. Combine with the
upper bound c<=n+c_res to obtain (3). QED.

The empty-support assumption is needed only for (3). A single alpha with
a local beta loop and a direct interval can pay at zero links, whereas
its local beta stem costs one. Its payment still splits exactly as in (2).
We do not turn this failed cost inference into a target counterexample.

For the original scalar ledger, with k all alpha sources, b all betas and
I the available interval set, deleting all m internal betas gives

    |I|+b-k = [|I|+(b-m)-(k-n)] + (m-n),
    k-V = (k-n)-V_res.                                    (4)

The n assigned whole betas pay the n removed sources once. If m>n,
m-n is the count of extra unused internal beta resources; it must not be
counted again through their two BP tips. A pure PP/M cycle has no beta
sink and is not an edge of H, so it supplies none of these units.

## 5. Frozen applications and necessary hypotheses

In the preceding tight-support 16x14 fixture, before filling the shared
pocket there is already a recognized short beta

    {(3,3),(3,4)}, between A:(3,2) and B:(3,5).

Its required PP guards lie in the other band, at rows 4/5, columns 3/4.
After adding {(8,5),(8,6)}, the same A,B owners are joined by a second
recognized short beta. The guards for that edge are at rows 6/7,
columns 5/6. H now has two vertices and two different parallel beta edges.
Both alphas have empty support. Theorem 3 eliminates the entire component
with exactly two payments and two links, leaving no alpha demand there.

This gives a stronger structural interpretation of the preceding cost
obstruction: the tight completed board contains a closed beta resource
cycle. Its apparent tree deficiency arose from retaining only one of
the two recognized edges. Both actual beta identities must be included.

The older frozen guarded-fork fixture gives a one-vertex loop after its
C pocket is filled. C has no direct support then, so it eliminates with
exactly one payment and one link, retaining the full A/D exterior system.
For q separated copies and an arbitrary filled subset S, respectively
2|S| and |S| source payments/links eliminate in the two families. The
copy separation and explicit earlier certificates prove these all-q
statements; finite controls check the implementation.

Complete freezing cannot be weakened to occupied degree at least three.
On a 4x6 board take

    T={(0,1),(0,4),(3,1),(3,4)},
    M={(1,1)--(2,1), (1,4)--(2,4),
       (1,2)--(1,3), (2,2)--(2,3)}.

All eight endpoints have occupied degree three; the two vertical alpha
paths flank both horizontal short betas. Their across-band guards are
BP rather than PP. No endpoint freezes. In particular the closed pairs
{(2,3),(1,2)} and {(2,2),(1,3)} each have at most one possible retained
nonmate neighbor supplied from outside the pair. The checker verifies
these pairs directly. This refutes the weaker degree-only guard rule,
not Theorem 1 or the global grid inequality.

## 6. Verification and scope

`develop/check_forced_pocket_guards_and_cycle_elimination.py` reconstructs
actual strands independently, discovers motifs from the actual short beta
and alpha tips, and checks the forced PP guards and retained-neighbor
rank inequalities. It does not assume guards in the search predicate.
It constructs the non-tree assignment with actual link witnesses, deletes
the sources and whole betas by their original identities, compares both
ordinary/full residual optima, and lifts residual solutions to the original
terminal matching without reused alpha/beta endpoints. The permanent
output includes the explicit nonfrozen counterexample.

The permanent run passes 752 systems, including 268 completely frozen
physical boards and 1,636 recognized short-beta motifs. It makes 1,504
ordinary/full residual value-cost comparisons with actual-link lifts and
290 comparisons against an independent primitive packing optimizer.
There are 720 nonempty eliminations and 84 cardinality-only controls with
direct support allowed. Physical controls include all filled subsets
through four separated copies, further controls through twelve copies,
40 monotone frozen extensions and 16 isometries carrying the band convention.
The degree-three nonfrozen example is an additional negative control.
These checks test recognition and reduction; the general claims follow
from the proofs above, rather than extrapolation from the finite run.

The Lean source `formal/SubQuorum/ForcedPocketGuards.lean` checks three
declarations: selection exclusion by two occupied neighbors, forced use
of both candidates by two distinct witnesses, and the guard-partner
endpoint conclusion from actual neighbor lists, matching symmetry and a
strict freezing certificate. It derives the contradictory rank inequalities;
they are not supplied as assumptions. The first two declarations are
axiom-free. Grid-coordinate/alpha-type adapters and cyclic-block flow
elimination remain written proofs, not complete Lean formalizations.
The source passes Lean 4.33.0 without sorry or native evaluation. No new
independent external review is claimed.

The next residual system should first include **all** recognized short-beta
edges, eliminate non-tree components, and only then compress its remaining
trees. Those trees must obtain further compensation from other beta shapes,
mixed routes or original intervals, with original capacities retained.
Nothing proved here guarantees those remaining exterior cuts are saturated.
Universal compensation and improvement of the 5/6 bound remain open.
