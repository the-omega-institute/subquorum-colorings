# Guarded two-column pockets and monotone fork replacement

25 October 2026. Haobo Ma and Wenlin Zhang. Research branch only.

The existing frozen beta-fork board cannot be turned into an indispensable
fork obstruction merely by adding selections and matching edges around its
C gap. We prove a local dichotomy for arbitrary feasible monotone extensions:
the two-column pocket either stays BB/BB, or its top vertices become one
forced horizontal beta. In the first case C retains private interval credit;
in the second case the new beta is accessible only from C. Either resource
replaces a fork rooted at C without disturbing any outside certificate.
The C arm may contain an arbitrarily long legal mixed path.

The empty case strictly reduces link cost. The filled case need only tie
that cost, but reduces the number of forks. Thus a maximum-payment,
minimum-link packing can always be chosen without such a fork. This is
stronger than a finite failed construction search, but is not exclusion of
every tied optimal fork or a proof for every grid. It yields a precise
sufficient class on which ordinary whole-owner-support flow is exact.

## 1. A local pattern with fixed old mates

Use the established horizontal band convention, with an even row r>=2.
Consider the two pocket columns s,s+1, strictly inside a band. Initially:

* u=(r,s), v=(r,s+1), d=(r+1,s), e=(r+1,s+1) are blank;
* x=(r,s-1), y=(r,s+2) are the two TP tips of one original alpha C;
* t=(r+1,s-1), z=(r+1,s+2) are selected, so x and y respectively
  are already occupied neighbors of t and z;
* a=(r-1,s), b=(r-1,s+1) are old matching endpoints, and their vertical
  band partners (r-2,s), (r-2,s+1) are also old endpoints. Thus a,b
  lie in fixed PP columns and cannot be free terminals;
* the old actual matching, all selected vertices, and the original C path
  are retained. In particular x,y,a,b already have fixed old mates.

The local pattern is visible in the base fixture at r=12,s=3:

    row 10:          P  P       [partners of the two endpoints below]
    row 11:          P  P       [a,b, internal PP]
    row 12:       C  .  .  C    [x,u,v,y]
    row 13:       T  .  .  T    [t,d,e,z]

The diagram shows only the listed columns; it does not specify all matching
edges. The base fixture's actual old mates supply those edges.

An extension may add arbitrarily many selected vertices and actual matching
edges elsewhere. It may not remove old selections, change an old mate, or
violate feasibility: every selected vertex has at most one occupied neighbor.
All new actual edges are between nearest neighbors and form a matching.
No freezing assumption on the extension is needed for the local theorem.

The C tips remain TP under such an extension because their selected vertical
partners are fixed. All old PP vertices on C remain PP, with unchanged old
mates. Thus C remains the same original alpha. We use the fixed original
interval convention of the current board, with only the standard outer
boundary marks. The pocket's internal singleton intervals, when present,
are unmarked. Deliberately reserving these units is outside this theorem.

## 2. Dichotomy for every feasible monotone extension

**Lemma 1.** Exactly one of the following holds:

(a) All four pocket vertices remain blank.

(b) u and v are endpoints of the actual edge uv, d and e remain blank,
and uv is an original two-endpoint beta E with BP tips u,v.

**Proof.** The old selected guard t already has occupied neighbor x, hence
d cannot be occupied by a selection or matching endpoint. Similarly e
cannot be occupied because of z and y. This uses only retained old
neighbors; further additions cannot undo the exclusion.

The vertex u has two distinct old occupied neighbors x and a, so u cannot
be selected. Likewise v cannot be selected, because it sees b and y.
Thus each top pocket vertex is blank or a matching endpoint.

If u is an endpoint, its actual mate must be one of x,a,v,d. The endpoints
x and a already have unchanged old mates and cannot be reused. The vertex
d cannot be occupied. The mate is therefore v. By matching symmetry v's
mate is u. Starting with v gives the same conclusion. Hence a single
occupied top vertex is impossible, and the only possibilities are (a),(b).

In (b), each within-band partner d,e is blank. Consequently u,v are BP
free tips, joined by their actual edge and no PP continuation; they form
one whole beta E. ∎

**Lemma 2 (exclusive replacement resource).** In case (a), C alone supports
each of the two available original pocket intervals. In case (b), every
legal link entering E has its TP endpoint in C. Consequently any ordinary
or fork certificate using E also uses C, and E cannot occur in another
certificate compatible with a fork rooted at C.

**Proof.** In (a), the consecutive BB columns s,s+1 are singleton intervals
of the original BB/TT forest. Their endpoint-free gap has precisely the
fixed C columns s-1,s+2 as boundaries. No other original open owner borders
this gap; both singleton units therefore have C as sole owner. They are
internal and unmarked.

In (b), u's neighbors are x,a,v,d. Of these, only x is a TP terminal:
a is permanently internal PP, v is the other BP, and d is blank. Likewise
only y can be a TP neighbor of v. The two links are x->u and y->v, both
from C. The beta E is a sink, not an ordinary transit owner. Any primitive
using it must end an arm with one of these links, and thus contain C.
A beta fork into E would require two different alpha roots; both entries
here come from the same original alpha C, so no such fork exists.
Owner-disjointness now prevents any outside certificate from using E while
a chosen fork already uses C. This proves availability rather than assuming
an unreserved extra beta. ∎

## 3. Replacement in an arbitrary compatible packing

**Theorem 3 (guarded-pocket fork replacement).** Let P be any compatible
whole-support primitive packing in a feasible monotone extension of the
pattern above. Suppose P contains a fork f with C as one of its two alpha
roots and beta B. Let l>=1 be the number of links on its C-to-B arm; the
other arm may also contain arbitrary mixed owners. Then a compatible
packing P' has the same payment, agrees with P on every other certificate,
and has one fewer fork. Its cost satisfies

    links(P') <= links(P)-l       in the empty-pocket case,
    links(P') <= links(P)-l+1     in the filled-pocket case.       (1)

**Proof.** Keep f's other complete arm as a beta stem into B. It pays its
original alpha source with the same one whole beta as before. Discard f's
C arm, releasing its mixed owners, and release f's old interval assignment
J_f. All other certificates remain unchanged.

In the empty case pay C by a zero-link interval stem using either private
pocket unit. Neither could equal J_f: a fork interval has a witness in its
beta body B, while this unit has only C as an original owner. Neither is
used outside f either, since every certificate using it would contain C.
Thus this is a different, unused original unit, allocated exactly once.
Both original fork sources remain paid; deleting l links proves (1).

In the filled case pay C by the one-link stem x->u into E (or y->v).
By Lemma 2 E is different from B and absent from every outside certificate.
It was also absent from f's mixed arms, since a beta cannot be an internal
mixed owner. The replacement therefore consumes the different whole units
B and E exactly once each. It no longer spends J_f. Again both original
sources remain paid, and replacing l links by one gives (1).

The two replacement stems are owner-disjoint: one lies on the old other
arm and B, and the other uses C plus, in the filled case, E. All outside
owners and assignments are retained. In particular J_f is released before
any new resource is used; no old used interval is counted as fresh slack. ∎

The filled case may save no link when l=1. It does not imply that every
maximum-payment/minimum-link packing omits f. Rather, among tied packings,
minimize the number of forks as a third criterion. Theorem 3 contradicts
such minimality if a fork has a guarded C root. This criterion changes no
payment or link optimum; it chooses a representative attaining both.

For several owner-disjoint guarded roots, the replacements can be performed
simultaneously. Private interval units cannot belong to two different C
owners. If two filled pockets supplied the same beta, that beta would have
two distinct incoming source owners, contradicting Lemma 2. Thus even these
new whole-beta resources are different; their two BP tips are never counted
as two resources.

## 4. A sufficient class for full-network ordinary exactness

**Corollary 4.** Suppose every feasible beta fork in a given finite system
has at least one alpha root with a guarded pocket as above. Then ordinary
whole-owner-support flow has the same maximum payment and the same minimum
link cost at that payment as the full stem/fork system.

**Proof.** Choose a full packing maximizing payment, then minimizing links,
then minimizing fork count. A fork has a guarded root by hypothesis, so
Theorem 3 either strictly reduces links or retains links and reduces forks.
Both contradict the chosen optimum. The packing is ordinary. Since ordinary
packings are a subclass of full packings, equality of both optima follows. ∎

This is a sufficient geometric condition on all feasible forks, not just
the forks selected by a particular initial algorithm. It allows arbitrary
bent mixed arms and outside interactions. A board with a new unguarded fork
need not satisfy it. The theorem does not assume every alpha has a pocket,
and does not prove every actual grid satisfies the condition.

## 5. Base fixture, arbitrary stacks and arbitrary inserted subsets

For the 16-by-14 base board, all feasible forks use A and C to enter B.
The existing E beta has only the D entry, and the new pocket beta, if
inserted, has only C entries. Separated vertical copies create no cross-copy
links. Consequently arbitrary q copies and any subset S of pocket insertions
satisfy Corollary 4. Their exact unrestricted optima are

    full value = ordinary value = 3q,
    full minimum links = ordinary minimum links = q+|S|.         (2)

A pays its old private interval with no link; D enters its old neighboring
beta with one link; C either uses a pocket interval for zero links or the
inserted private beta with one. These resources differ in every copy.
There are exactly 3q alpha sources, proving the value upper bound.
Every D has empty initial support, and each inserted C has empty initial
support. Each needs a link at its own TP source; a TP--BP link has only one
TP endpoint, so these q+|S| links are different even in a fork packing.
This proves the cost lower bound and (2), for every q and S without enumeration.

For an arbitrary monotone extension of the base fixture, Theorem 3 still
removes forks rooted at C whenever present. Additional forks elsewhere may
be unguarded. We do not infer (2) or unrestricted ordinary exactness for
all those extensions.

## 6. Verification, formal scope and continuation

The solver-free checker passes 224 fully frozen physical controls with 308
pockets: 141 private-interval replacements and 167 exclusive-beta replacements.
It replays 202 unchanged outside certificates and saves exactly 141 links.
Two hundred greedily constructed extensions include 1600 accepted selection
or matching additions. They keep standard blank boundary columns and the
old designated beta tips plus one body interval, so its fork remains feasible.
Twenty-four stack controls use q=1..8 and empty/full/alternating insertion
subsets, checking (2) and that all feasible forks have a guarded C root.
All 81 local B/T/P labelings independently leave exactly BBBB or PPBB.
An additional 144 abstract mixed-arm controls use C-arm lengths 1..12 and
other-arm lengths 1..6, checking both resources and independent ordinary
flow. Six filled cases exhibit a fork tied in value and cost with its
ordinary replacement; they are abstract, not claimed physical tie examples.
These controls distinguish nonincreasing replacement from strict exclusion.
All finite controls support the written all-extension arguments above.

Four scoped local Lean 4.33.0 declarations verify the four-neighbor forced
mate, empty-or-paired endpoint dichotomy, the owner-disjoint exclusive-beta
argument and injectivity of private beta resources for distinct roots.
Three declarations are axiom-free; the fourth uses only propext,
Classical.choice and Quot.sound. There are no warnings, sorry, admit,
native_decide or new axioms. Coordinate/support adapters, the full route
replacement, lexicographic reasoning and all-q statement (2) remain written
proofs, not claimed complete Lean formalizations. No new external review
is claimed.

Reproduce:

    python3 develop/check_guarded_pocket_fork_replacement.py --output output/guarded-pocket-fork-replacement-validation.json
    python3 develop/check_guarded_pocket_fork_replacement_formal.py --lean /path/to/lean-4.33.0 --output output/guarded-pocket-fork-replacement-formal-validation.json

Together with the [joint allocation and terminal-fork theorem](FORK_ALLOCATION_EXCHANGE_AND_CLOSED_TREES.md),
this excludes a whole monotone construction route for a necessary C-rooted
fork. A surviving geometric obstruction must change the retained old mates
or guard pattern, or use a fork with no such guarded root; it must then
survive both all ordinary interval exchanges and alternative private-beta
exits. Arbitrary capacity-two tiles and occupied neighboring bands remain
outside this sufficient class. The general mixed compensation inequality
and universal 5/6 improvement remain open. The submitted manuscript is kept
separate from these research notes.
