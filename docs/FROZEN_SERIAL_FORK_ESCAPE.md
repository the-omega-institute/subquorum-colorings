# Frozen serial forks force a port or an exterior open owner

25 October 2026. Wenlin Zhang and Haobo Ma. Research branch only.

The [serial revision plateau](COUPLED_LINK_RETRACTION.md) is an abstract
all-live terminal system, not a frozen-grid construction. We now prove a
geometric restriction on every original frozen realization of its skeleton:
the second mixed output must have an original BB port or a link to an open
owner outside the skeleton. An available port repairs that skeleton while
retaining **all** its old source-to-mixed links. A marked port is an explicit
boundary exception. Thus the resource-free, owner-closed serial interface
cannot occur in the interior with its complete original links and resources.

For several owner-disjoint skeletons of the same checkerboard phase, the BP
escapes have different exterior owners. Exterior beta escapes can therefore
be used simultaneously. Forced BB ports still need allocation by ORIGINAL
interval identity; two such ports may share one unit. We give the resulting
joint payment inequality without crediting an exterior mixed gate as a sink.

The geometric rank argument extends the earlier
[alpha beta-fork escape lemma](FROZEN_BETA_FORK_ESCAPE.md) to a mixed strand
whose BP has vertical actual matching. The new application is the exterior-
owner exclusion for a complete serial skeleton and its simultaneous bound.
This is not a new general flow theorem or a proof of arbitrary frozen-grid
compensation. No numerical improvement of the universal 5/6 bound is claimed.

## 1. Original geometry and a mixed beta-fork escape

Use a feasible original (T,M), endpoints P, disjoint aligned two-row bands,
complete finite strict freezing ranks, and original open PP/M strands. The
packet is matching closed, has a blank first column and a blank corner in
its last column as in the vertical-TP theorem. Original intervals I exclude
only the established marked extreme intervals K. No further reservation is
made. An original open strand has opposite checkerboard colors at its ends:
its actual M and PP edges alternate, starting and ending with M, so its
physical path length is odd.

**Lemma 1 (vertical mixed output escape).** Let X be an original mixed
owner. Its BP x is vertically actually matched. Suppose its TP t is next to
a BP b of an original beta Z, and b's other horizontal neighbor u is TP.
Let n be t's horizontal neighbor away from b. Then exactly one of these
physical alternatives occurs:

- n and its within-band partner are B, giving an immediate original BB port;
- n is an original BP of a different owner, and its actual mate is its
  outward horizontal neighbor away from t.

The BB unit may be marked; availability is not automatic. Different such
TP motifs have different BP escape targets. Among motifs whose TP tips
have one common checkerboard color, the BP targets have different original
open owners, not just different BP tips.

**Proof.** A horizontally matched TP necessarily forms a one-M-edge mixed
strand: the selection at its band partner forces the mate's band partner
blank. Hence X's vertical BP mate rules out horizontal mating of t.
Normalize t=(r,c), in the lower row of its band, with b=(r,c-s),
u=(r,c-2s), n=(r,c+s), s in {+1,-1}. Put

    a=(r+1,c), b*=(r+1,c-s), z=(r+1,c+s), h=(r+2,c).

The actual mate of t is a. The beta BP b cannot match either neighboring
TP (either would make it mixed), and its in-band partner is blank, so its
actual mate is b*. Freezing b requires both t and u retained. In particular

    rank(a) < rank(b).                                    (1)

At a, its own mate t is never retained through itself, and retaining b*
would require rank(b)<rank(a), contradicting (1). Therefore its other two
possible neighbors z,h must both be retained. If n were T, it would see
both t and the occupied z, violating feasibility. Thus n is not T.
The selection across from t forces n's band partner blank. If n is B,
we obtain the BB alternative.

If n is P, it is BP. The retained z cannot be T, since it sees both a and
n. Hence z is P and rank(mate(z))<rank(a). Were mate(n)=z, this would give
rank(n)<rank(a). But n, with blank band partner and vertical mate z, needs
t retained in order to freeze, giving rank(a)<rank(n), a contradiction.
The mate of n is therefore its outward horizontal neighbor. In particular
n cannot be X's BP x, whose mate was assumed vertical. The link t->n is a
nonself original link, not a fictitious new resource.

If two different vertical TP tips shared one escape BP n, they would be
its opposite horizontal neighbors. The outward-mate rule for either tip
would match n to the other, contradicting that tip's vertical actual mate.
Thus the targets are distinct. At a common TP phase their BP target colors
are also common; two BPs of one beta have opposite colors, and a mixed
owner has only one BP. Consequently their owners are different. Reflections
handle upper-band rows and both horizontal directions. QED.

This proof uses the original ranks, points and matching throughout. It
performs no deletion and makes no freezing assertion about a reduced board.

## 2. The serial skeleton has an exterior escape

A serial skeleton of length n>=2 consists of distinct original owners
A_1,...,A_n (alpha), X_1,...,X_n (mixed), Z_1,...,Z_n (beta), with active
tips a_i, mixed BP tips x_i, mixed TP tips t_i, and beta BP tips b_i.
Require the following original horizontal TP--BP links to be present:

    C={a_i -> x_i : 1<=i<=n};
    a_i -> x_(i+1),                    1<=i<n;
    a_n -> b_n;
    t_1 -> b_1;
    t_i -> b_(i-1),                    2<=i<=n.             (2)

Other original owners, links and supports are allowed; they must not be
silently discarded. Skeletons in the simultaneous result below have
pairwise disjoint original owners. Their original interval identities need
not be disjoint. The old cancellation choice is exactly C, not physical M.

**Theorem 2 (serial escape).** The output t_2 has an immediate BB port, or
an outgoing original link to a BP of an open owner outside this skeleton.
If its port unit J is available, all n skeleton sources can be paid while
retaining every old link of C, using J and Z_1,...,Z_(n-1) once each.

**Proof of the local hypothesis.** Original alpha TP tips are vertically
matched. In (2), the BP x_2 is between the different alpha TP tips a_1,a_2,
which are already matched vertically; its band partner is blank. Thus x_2
is vertically matched. Lemma 1 applies to X_2 at the beta fork
(t_1,b_1,t_2), giving its port or outward-matched BP escape n_2.

**Why an escape BP cannot be any listed owner.** The terminal rail in (2)
is one horizontal row path, so all a_i have a common checkerboard phase,
all x_i and b_n have the opposite phase, all mixed t_i have the a_i phase,
and every b_i has the opposite phase. The inactive BP of each Z_i has the
a_i phase; n_2, being next to t_2, has the opposite phase. It cannot be any
of those inactive BPs. It is not b_1, the different inward neighbor.

Every x_i is adjacent to the alpha tip a_i. Every b_j with 2<=j<n is
adjacent to t_(j+1), and b_n is adjacent to a_n. Each of these specified
TP neighbors is different from t_2. If any such BP equalled n_2, that TP
would be its other horizontal neighbor and hence its forced actual mate.
This would identify two distinct original owners, a contradiction. There
are no BP tips on the A_i. These cases exhaust every BP in the skeleton,
so n_2 belongs to an exterior beta or mixed owner.

**Repair with J.** Retain all n links C. Use t_1->b_1 and t_i->b_(i-1)
for i=3,...,n, and pay the remaining A_2--X_2 alpha by J. These use different
original mixed owners, BP entrances, whole betas and the one original J.
The paid number is n, with exactly 2n-1 selected actual links including C.
Additional original routes may help too; this is an explicit certificate,
not a uniqueness or minimum-cost claim for the larger original board. QED.

An owner-closed skeleton with no available support at X_2 must therefore
have its forced BB port in K. The previous abstract all-empty-support
serial system is excluded as a complete interior interface. This does NOT
exclude longer revision dependencies with exterior relays, modified terminal
incidences, occupied ports or boundary marks. In particular one boundary
exception might still support a large revision cost; there is no universal
revision bound here.

## 3. Simultaneous compensation: common phase, original units and boundary marks

Consider q owner-disjoint serial skeletons with total N alpha sources.
Assume their a_i tips all have the SAME checkerboard phase. For each one
apply Theorem 2 to t_2, recording its single outward BB port or BP escape.
Classify the escapes as:

    b : exterior beta owners;
    m : exterior mixed owners;
    u : unmarked/available original interval units (one per such skeleton);
    h : marked original interval units.                    (3)

Here b,m,u,h count skeletons, so q=b+m+u+h. Let r be the number of DIFFERENT
original unmarked unit identities among the u ports. Equivalently r is the
matching rank between these u skeletons and their one forced unit each.

**Theorem 3 (joint unchanged-C certificate).** There is a simultaneous
packing, retaining every old C link, that pays at least

    N-q+b+r                                               (4)

of these N sources, with 2N-q+b selected actual links. Consequently their
certified unpaid count obeys

    Delta <= q-b-r <= m+h+floor(u/2),     h<=|K|.            (5)

If m=h=0 and the u units are different (r=u), ALL N sources pay without
revising C. If all escapes are exterior beta owners, the same conclusion
holds. Formula (4) is a lower bound in the full original board; further
supports or exterior routes may increase payment.

**Proof of exterior identities.** Lemma 1 makes all BP targets different
and, by the common phase, all their owners different. The exclusion proof
of Theorem 2 works against the union of ALL skeleton owners: a different
skeleton's active beta BP or mixed BP has a specified different TP neighbor,
while all of its inactive beta BPs have the wrong color. Thus these targets
belong to different owners OUTSIDE the entire skeleton family. In particular
an exterior beta payment does not reuse a baseline beta from another skeleton.
This is where the common-phase assumption is required.

**Proof of simultaneous certificate.** For each skeleton use all C and the
baseline beta links t_1->b_1, t_i->b_(i-1) for i>=3, leaving just its A_2
unpaid. This pays N-q using different owners and betas. For each of the b
beta escapes add its one t_2->escape_BP link, consuming a different exterior
whole beta. Of the u ports choose one skeleton for each different original
unit and pay its remaining A_2 by that unit. No resource is assigned twice;
the interval and beta identities have different types. Do not add any link
or credit for an exterior mixed escape or a marked interval. This pays
N-q+b+r and uses N old C links, N-q baseline beta links and b new links.

An immediate original unit can border at most two original TP tips, so
u<=2r. Each marked extreme interval has at most one interior-side TP tip,
so the h marked targets are different and h<=|K|. Substituting q=b+m+u+h
and u-r<=floor(u/2) proves (5). QED.

Two ports with the same original J give ONE added payment, not two. The
minimal abstract adapter with two serial skeletons sharing J has exactly
one unpaid source even after both ports are opened. Likewise, without the
common phase, two different BP tips may belong to one beta; without an
additional interval that beta supplies only one payment. Both controls are
verified. The m exterior mixed gates remain unresolved routing obligations;
(5) does not turn them into m units of surplus.

An owner-closed, resource-free collection of owner-disjoint skeletons is
therefore charged injectively to K, even without a common-phase assumption:
its only alternatives are marked ports. This bounds the number of such
literal isolated serial obstructions, not their lengths or general defects.

## 4. Explicit nonfrozen necessity control and verification limits

The [28P/7T literal board](../develop/fixtures/nonfrozen_nested_serial_fork.json)
is a feasible 14x18 NONFROZEN configuration. It has different alpha tips
(5,8),(5,10) entering mixed BP (5,9). That same mixed owner ends at TP
(10,9), which shares beta BP (10,10) with TP (10,11). Its outward site
(10,8) is T, so this exact mixed output has neither a BB port nor the forced
outward BP escape. The actual mates are

    mate(10,9)=(9,9),     mate(10,10)=(9,10).

Freezing beta BP (10,10) would require (9,9) earlier. Freezing (9,9) would
require beta BP (10,10) earlier. Both remain unfrozen; only one of the 28
endpoints freezes in the independently recomputed closure. This supplies a
checkable reason the complete-freezing hypothesis cannot be dropped. It is
not a frozen serial realization or a counterexample to the grid target.

The verifier separately checks 72 earlier frozen boards/images: 160 actual
vertical beta-fork motifs all realize the BP escape case, and 12 shared
alpha-alpha mixed heads verify the input geometry. It also checks 400 actual
immediate BB ports for their original identity/multiplicity adapter. No full
nested mixed-head/beta-fork motif, and no forced-BB beta-fork case, was found
in these frozen controls. We do NOT present these separate checks as a frozen
realization of the complete serial skeleton. The general geometry and
arbitrary-n exclusion are proved above, not inferred from this survey.

The simultaneous allocation adapter is tested on 255 abstract decorated
serial systems, with 510 ordinary/full fixed-C comparisons and explicit
selected-terminal certificates. Of these, 243 obey the geometric two-user
interval bound. Twelve higher-multiplicity abstract systems are tested for
exact payment but deliberately excluded from (5). They are not alleged
physical instances. The nonfrozen fixture and an opposite-phase shared-beta
control test the necessary hypotheses.
Certificates constructed separately for opposite checkerboard phases must
not be added without checking their shared beta and interval identities.

Optional bounded SMT discovery, including unsuccessful fixed placements,
is recorded separately. Bounded UNSAT or UNKNOWN is not used to establish
any geometric exclusion. The solver-free verifier requires no Z3.

## 5. Lean scope and next geometric question

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 develop/check_frozen_serial_escape.py \
  --output output/frozen-serial-escape-validation.json
cd formal
lean SubQuorum/FrozenSerialEscape.lean
```

Nine scoped Lean statements check two retained witnesses forcing both local
candidate sites, the two strict-rank contradictions, BP-target injection
from the supplied coordinate hypotheses, the common-phase inactive-tip
exclusion, joint-deficit and distinct-port arithmetic, marked-label counting,
and the explicit certificate's link count. Coordinate forcing of the local
candidate sets, original strand color/owner exclusion and the complete
physical certificate adapter remain written/Python. This is not an end-to-
end formalization of Theorem 2 or 3. Only standard axiom dependencies are
used, with no sorry, native evaluation or added axiom.

The remaining hard case is now explicit: follow the distinct EXTERIOR mixed
escapes while respecting their original capacity-one gates and shared sinks.
They might return into other routing components; injective BP targets alone
do not establish available beta or interval surplus. Boundary-marked escapes
and two-phase interactions also remain. The submitted 11 October version,
public main, PR3 and shared CI are unchanged. No email was sent.
