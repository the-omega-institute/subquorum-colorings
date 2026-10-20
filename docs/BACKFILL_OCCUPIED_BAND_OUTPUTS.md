# Occupied-band outputs for both positive-corner and phase10-terminal routes

20 October 2026. The complete companion bar routes the remaining B and D
backfill branches into actual original cap or singleton occurrences. In B
the positive terminal is necessarily activated, even though the starting
point is only a positive outer corner. Interior output tiles inject and
avoid every old ordinary receiver, critical receiver and backfill tile.
This supplies simultaneous new terms for the existing single-pool ledger.
The unrestricted coefficient-one allocation and grid triple equality remain
OPEN; the signed source census is retained throughout.

## 1. Complete-source hypotheses and the occupied band

Use ALL complete finite U/rotor, original endpoint uniqueness, unchanged
matching, mandatory support, degree-one and transported-partition hypotheses
of [the four-route theorem](BACKFILL_CORNER_ROUTING_AND_SHALLOW_BARRIER.md).
Keep its normalization and original U11 companion F:

    F(r,c)=(c-1,r-h-1), F is U(v,h,f),
    Qb={0,1}x{-2,-1}, q=(1,-1).

All widths are even and at least6; all independent heights are even and
at least4. This formula names the incident companion leg; it does not
equate its two heights. Consider B or D at q, naming H's incident height a:

    B: H(r,c)=(c,-r-1),       H is positive U(w,a,b);
    D: H(r,c)=(c,r-a-1),      H is phase10 U(w,a,b).

These are exactly the allowed top-arm forms of the four-route table, after
renaming the two original legs if necessary. Both have the complete run

    (1,c) in P_H for -a-1<=c<=-1.

The point(1,-h) is in F's original bar. If a+1>=h it is also on that H
run. Endpoint uniqueness therefore gives the NEW B bound, and repeats the
established D bound:

    a<=h-2.                                                     (1)

Define the output point, adjacent corner and their physical tile by

    x=(1,-a-1), y=(1,-a-2),
    Tx={0,1}x{-a-2,-a-1}.                                      (2)

The physical coordinates in(2) are aligned because a is even. This is a
transported tile of the original partition, never a reset partition.
In B, x is H's actual positive terminal singleton, with original supports
(0,-a-1) and y. In D, x is H's actual phase10 outer-corner singleton,
with sole original intratile support(0,-a-1). Its other three corners
are not H endpoints in either case. F owns(0,-a-1), so the north support
is consumed. In particular every B event activates this particular leg.

## 2. Exactly two original companion profiles

Evenness and(1) leave two alternatives.

**Cap output: a=h-2.** F's EXACT original profile in Tx is

    {(0,-a-2),(0,-a-1),y}, an original U11 triple.

Thus x fills that actual cap. In B this is an existing positive cap-filler
activation Fpos; in D it is an existing negative cap filler Fneg. Neither
is a new copy of that cap or of its singleton filler. The actual cap
determines the leg of F and hence its terminal f=(0,-1), which determines
the critical root f+(0,1). Global critical-point injection then determines
the original event. These cap-output occurrences inject.

**Interior output: a<=h-4.** F's EXACT original profile in Tx is the
regular2P1T pair

    {(0,-a-2),(0,-a-1)}, with original support y.                (3)

In canonical F coordinates these endpoints are(h-a-1,1),(h-a,1), with
h-a>=4. They are strictly interior stem points, not either original F
terminal and not a bar pair. The support y has two persistent endpoint
anchors(0,-a-2) and x, with different original owners F and H. Mandatory
retention forces y into final P. Consequently Tx is full and y has a
third original owner, different from F and H. No assertion about its U
or rotor type is needed here.

For B, both original supports of the positive terminal x are consumed.
For D, x belongs to the EXISTING negative U singleton pool Pneg and to
E1reg, since F supplies the exact regular pair(3).

Let b count B interior outputs and d count D interior outputs. Let
KBcap,KDcap count the two cap-output classes. Then

    KB=KBcap+b, KD=KDcap+d,
    KBcap<=Fpos, KDcap<=Fneg.                                  (4)

These inequalities record actual subfamilies, not independent payments.

## 3. Global injection and separation of interior output tiles

Every interior Tx has F's exact two-point U11 stem profile and H's exact
singleton, with H phase00 or10. If another event has the same output tile
but a different U11 companion F', its original pair must occupy the two
corners outside F's pair. One of those corners is x, owned by H. Since
H's phase differs from F', endpoint uniqueness makes this impossible.
Therefore coincident output tiles have the same original companion F.

The exact interior stem pair identifies which original leg of F it lies
on: opposite legs are separated by v-1>=5. That leg has one original
terminal. As above, this terminal determines the critical root, and global
critical-point injection identifies the event. Hence ALL interior output
tiles, with B and D considered together and recurring owners allowed, are
globally distinct. Their x occurrences are distinct as well.

They avoid every ordinary first/LONG receiver. Such a receiver contains
an exact original phase01 regular pair. Its owner differs from F and H,
so that pair cannot fit into Tx's single remaining corner.

They avoid every critical receiver. The established critical profile
theorem makes a critical root's original profile have at least two
endpoints in its receiver. In Tx only F has more than one endpoint. F is
U11, so a critical root belonging to it would have to be one of its
original terminals. The exact pair(3) contains neither terminal.

They avoid ALL original backfill tiles. Such a tile contains a U11
companion's exact pair INCLUDING one of its original terminals. A different
companion pair cannot fit outside F's pair because x has owner H of phase00
or10. The same companion F has no terminal in the interior pair(3).

These arguments compare actual original profiles in the same fixed tile;
they hold across different components and do not assume fresh owners.
In particular the d new negative singleton occurrences avoid E1old and
both q/r corner sets of [the two-corner lemma](BACKFILL_TWO_CORNER_COMPENSATION.md).

## 4. One negative singleton pool and one activation pool

Use KC,Cminus,Cplus,E0,E1old,Fneg,Fpos,U0,A,Z0,H,R and the ORIGINAL U
source counts K01,K10,K11 from the two-corner lemma. H here is the defect
count, not the source named H in Sections1--3.

The new d occurrences are pair-reserved negative U singletons. Their exact
regular pair separates them from E0's irregular pair, and the existing
pair-versus-triple argument separates them from negative cap fillers.
Section3 separates them from E1old and the KC+Cminus backfill singletons.
Defining L as the complement of precisely this enlarged disjoint union
in the ONE original Pneg pool gives

    Fneg+|E0|+|E1old|+KC+Cminus+d+L=2K01+2K10, L>=0.           (5)

The b positive occurrences are distinct actual activations. They are
disjoint from every Fpos activation by the exact pair/triple argument,
including the same-owner case. They are disjoint from Eterm terminal
claims, whose tile contains an exact irregular2P0T pair. They are disjoint
from Cplus because all Cplus tiles are backfill tiles, excluded in Section3.
Together with the established three-family separation this proves

    Eterm+Fpos+Cplus+b<=A.                                    (6)

Since KBcap<=Fpos and KB=KBcap+b, the same bound also gives

    Eterm+Cplus+KB<=A; in particular KB<=A.                   (6a)

This is an activation bound on ALL B events, not just a corner count
KB<=2N. The cap-output branch is included by its existing Fpos occurrence.

Different terminals of one recurring positive source count separately.
No additional copy of a positive leg, cap filler or H/Z0 resource appears.

Use the SAME cap identity Fneg+Fpos+U0=2K11 and Cminus+Cplus=KC. Put
Delta=K11-K01-K10 and e=|E0|+|E1old|. Substitution ONCE into the exact
reserve identity gives

    2R=2Delta+e+2KC+d+b
         +(A-Fpos-Cplus-b)+Z0+H+L.                            (7)

Both displayed remainders are nonnegative. In particular

    2K11+e+2KC+d+b<=2K01+2K10+A+U0,
    2R>=2Delta+e+2KC+d+b+Z0+H.                               (8)

The old E1reg count already includes the d occurrences; they must not be
added to the full E1reg count a second time. Cap-output classes in(4)
remain within the cap partition, rather than becoming extra summands.

Retain B=D+C0+C1+Eterm for the OLD passive-corner partition, with
C1<=A, J=J01+J11+Jcrit, D+C0+J<=H, and Tcrit<=Z0. Equation(6) and the
ONE reserve identity give the strengthened shared-stop bound

    B+J+Tcrit+Fpos+Cplus+b+U0<=2R+A.                          (9)

Substituting(5) and the cap partition gives its single-pool form

    B+J+Tcrit+2Delta+e+2KC+d+b+L<=2R+A.                      (10)

Since KBcap+b=KB and KBcap<=Fpos, (9) also yields

    B+J+Tcrit+KB+Cplus+U0<=2R+A.                             (11)

Thus every B event enters the shared bound, including cap outputs, while
the exact source-census form retains b+d interior-output contributions.
The signed Delta and the A on the right still require global control.
No unconditional R>=KC+(b+d)/2 or global marked-side allocation follows.

## 5. Verification scope and remaining full allocation

The local Lean companion checks normalized complete-source endpoint and
support profiles, B's incident bound, and the conditional joint ledger
arithmetic. Global phase/partition transport, event/output injection and
separation, actual activation families and pool assembly are the written
proof above. Execution and independent review are recorded separately.

All14 declarations compile with Lean4.33.0 on the user-selected local Mac;
their axiom audit passes with only propext, Classical.choice and Quot.sound.
No sorry/native_decide/additional axioms. Final source19509 exit0 at44%
free memory; axiom audit chunk84b7d9 exit0 at43%. Actual ps comm basenames
lean/lake and memory were measured before every invocation, with sequential
builds. See the [source](../formal/SubQuorum/BackfillBandOutputs.lean) and
[formal scope/receipt](../output/backfill-band-outputs-formal-check.json).

Finite controls reconstruct both band forms from independent-height source
constructors, check both cap/interior profiles, and test exact algebra.
Complete two-source B cap bands can be feasible without any critical event;
those are distinguished from full critical U10 realizations. The latter
still have ZERO control coverage. No finite search proves the general
classification, injection or compensation theorem.

The [controls](../output/backfill-band-outputs-controls.json) pass1728source
pairs:930overlap and798endpoint-disjoint profiles, including142B/120D cap
and272B/264D interior profiles. They include92complete feasible two-source
B cap bands, no complete D cap band in this sample, and11664joint ledger
instances,9936with negative source census. They do not turn the zero
critical-event/interior-realization coverage into an existence theorem.

Independent initial B/D audit8b3b2d3b ended with a terminal browser
infrastructure failure cdp_disconnected@typing, not a mathematical verdict.
Its stream89333 exited0/DONE but contains an error, so that transport status
does not establish acceptance. See the [failure receipt](../output/backfill-band-outputs-review.json).
Only after confirming that terminal failure, a NEW combined proof audit
was submitted on original stream96627 in a new conversation. Its packet
includes this complete theorem/final14-statement source and the later
[A-cap nonreuse/four-route extension](BACKFILL_FOUR_ROUTE_SINGLE_POOL_BUDGET.md).
The distinct prior shared-stop audit7ea29eb0 completed ACCEPT; it does not
cover either new theorem. The combined audit29f4d714 completed ACCEPT at
13:18:39UTC on20October, with20394response characters and observedgpt6/pro.
Original96627 exited0; the DONE stream and archived terminal response match
exactly. It checks this complete written theorem and the A-cap/all-route
extension, with no must-fix issue. It does not certify Lean execution or
finite controls, complete critical U10 realizability, full allocation or
grid equality. See the [review receipt](../output/backfill-four-route-budget-review.json)
and [full response](../output/backfill-four-route-budget-review-response.txt).

This routes B and D into the same original occurrence ledger used by A's
caps and C's two corners. It does not prove that those resources suffice
for all marked sides. Remaining full and neutral continuation branches,
recurring source ownership, and the signed source/mark census remain part
of the unrestricted coefficient-one and rectangular-grid equality problem.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
