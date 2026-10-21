# Secondary-ten support closure: an excluded north width and a forced bar window

21 October 2026. Continue the
[four-form first-consumer theorem](SECONDARY_TEN_FIRST_CONSUMER.md), in
the same complete original U/rotor model. Source endpoint ownership and
matching stay fixed. Every unconsumed original support retains its
original anchor as its sole occupied neighbor; consumed supports remain
occupied. U widths are even>=6, both independent legs even>=4. All
original orientations and extra sources are allowed. Tiles are fixed;
b is even. N counts positive owners only.

These results remove two possible boundary cases and identify an actual
positive activation in the tight upward branch. They do not prove global
nonreuse of the new activation or the full allocation/grid objective.

## 1. A width-six north terminal cannot be completed

Prescribe just two original sources

    Q=U(6,8,4), Q(r,c)=(b+2-c,11-r),
    L=U(6,4,v), L(r,c)=(b-9+r,c+6), v>=4.

**North obstruction.** There is no complete U/rotor extension, for any
legal even v. D, A/B/C and any marking assumptions are unnecessary.
Consequently the north-terminal branch at secondary10 requires w>=8;
combined with its existing bound w<=m-2 this requires m>=10.

Proof. Q's original support u=(b-5,11), intrinsic (0,7), has its original
anchor (b-4,11). L owns its east neighbor (b-5,12), intrinsic (4,6),
which exists for every v>=4. Neither prescribed source owns u. Retention
therefore forces a third owner at u, whose own endpoint neighbors can
only be north/west. U straight interiors and degree-three roles are
excluded. A north terminal of incident length>=4 contains the point
u+(-3,0)=(b-8,11), on L's lower bar. A west terminal of incident
length>=4 contains u+(0,-4)=(b-5,7), on L's near stem. A north-bearing
outer bar extends at least five steps north and meets the first blocker;
a west-bearing outer bar extends at least five steps west and meets the
second blocker. These exhaust the U roles, including exchanged leg names.

All four possible rotor tips are also blocked. In relative coordinates
at u, the west-tip forms contain (1,-3) and (1,-2), respectively; both
land on Q at (b-4,8),(b-4,9). The north-tip forms contain (-3,-1) and
(-3,1), respectively; both land on L at (b-8,10),(b-8,12). Every rotor
nontip has three own neighbors and was already excluded. No consumer
exists, contradicting completeness. This proves the obstruction for
arbitrary additional source dimensions, not merely bounded searches.

## 2. Every upward east branch forces a second U in a precise window

Prescribe Q as above and the distinct original sources

    D=U(m,10,4), D(r,c)=(b-11+r,c+5),
    E=U(w,g,v), E(r,c)=(b-4-c,g+7-r),
    m>=6, g>=m, w>=6, v>=4,

with all dimensions even and prescribed endpoint sets disjoint. E is
the actual upward east consumer from the preceding classification.

**Bar-window theorem.** Completeness forces a distinct original U owner

    C=U(omega,h,xi), C(r,c)=(b-5-c,B-r),
    m+7<=B<=g+5,
    4<=h<=B-7, B-m-5<=h, omega>=6, xi>=4.       (1)

Here B is an integer, not assumed even. All three dimensions of C are
legal even integers. Thus g>=m+2. Its isolated charge and the usable
local conclusion are

    B odd:  charge(C)=+1 and its near terminal is activated;
    B even: charge(C)=1-omega.                   (2)

No positive credit is claimed in the even-B case.

Proof. Put p=(b-6,m+5), D's original beyond-far-tip support, intrinsic
(5,m). Its anchor is north, D(4,m)=(b-7,m+5). Its south neighbor
(b-5,m+5) lies in E's entire incident row, whose columns are7,...,g+7.
The point p is absent from Q, D and E. In E it is below neither bar nor
far leg and is strictly left of the bar columns g+6,g+7. Completeness
forces a third owner at p, with own endpoint neighbors only west/east.

The four horizontal rotor-tip forms have relative endpoints at
(1,-3),(1,-2),(1,2),(1,1), respectively. Each is on E's incident row:
their columns lie between m+2 and m+7, within7,...,g+7. Thus no rotor
can own p. A U endpoint with only horizontal own neighbors is a terminal
or a straight leg point; it lies on a horizontal leg, with its bar wholly
to its left or right. This includes a terminal and every straight interior
position; it does not assume p is a terminal.

If the bar is left of p, its leftmost column is at least7: otherwise the
horizontal stem meets D's near stem at (b-6,6). Both bar columns are
at most m+5. An upward bar of width>=6 crosses row b-10 and therefore
D's lower bar. A downward bar crosses E's row b-5. Both are impossible.
So the bar lies to the right. A downward bar again meets E's incident
row, since its columns are at most g+5: the whole horizontal stem must
stop before E's bar at column g+6. Thus the bar points up and its
outer column B is at most g+5.

At a terminal the distance to the outer bar is at least four; at a
straight leg point it is at least two, since the leg/bar junction at
intrinsic row1 has degree three. Therefore B-p.column>=2, equivalently
B>=m+7. This proves the unique chart in (1). In that chart p has
intrinsic coordinates (B-m-5,1), giving h>=B-m-5. Its left terminal
cannot reach column6, so B-h>=7, or h<=B-7. Legal dimensions supply
the remaining restrictions. The nonempty interval for B yields g>=m+2.

The endpoint chart has phase determined by B's parity: its physical row
offset b-5 is odd. Direct source tile counts give charge+1 for odd B
and 1-omega for even B. This is the established complete U phase table,
also reconstructed independently by the controls below. If B is odd,
the near terminal z=(b-6,B-h) is positive. Its original lateral support
(b-5,B-h) is an E endpoint, since7<=B-h<=B-4<=g+1. Hence this original
positive singleton occurrence is activated. No claim that the other
support has a different consumer is needed.

The forcing at p follows from D's original support rule. No assumption
that every newly encountered owner is fresh is used: Q/D/E are excluded
by the absence of p from their endpoint sets before their endpoints are
used as blockers.

## 3. Consequences for the smallest gap cases

More generally, if g+7-B<=v, then

    omega<=w-2.                                  (3a)

Indeed E's far leg contains (b-4-w,B), with intrinsic coordinates
(g+7-B,w). The bar window guarantees g+7-B>=2. If omega>=w, C's outer
bar contains the same point, with intrinsic coordinates (0,w-1), a
contradiction. Evenness yields (3a). Thus v>=g-m is sufficient for
this width bound at EVERY possible bar in the window. In particular it
applies to both gaps2 and4 for every legal v>=4.

If g=m, (1) gives m+7<=B<=m+5, impossible. Thus the entire g=m upward
subclass has NO complete extension, at every width and far leg for which
the prescribed endpoints are disjoint. No reserve is counted for it.

If g=m+2, (1) forces B=m+7, odd, and

    C(r,c)=(b-5-c,m+7-r),
    4<=h<=m, 8<=omega<=w-2.                    (3)

It therefore forces a positive activated owner. To obtain the width
bound, suppose omega>=w. E's far leg contains (b-4-w,m+7), intrinsic
(2,w), since v>=4. C's outer bar also contains this point, intrinsic
(0,w-1), because w>=6 and w-1<=omega. This contradicts endpoint
disjointness. Evenness gives omega<=w-2. Also omega=6 would give
C(2,6)=(b-11,m+5)=D(0,m), another forbidden collision, so omega>=8
and w>=10.
Neither (3) nor the activation asserts existence of a complete instance.

Further original-support closure proves [terminal rigidity](SECONDARY_TEN_TIGHT_TERMINAL_RIGIDITY.md):
in a complete tight-gap instance h=m, so the positive near terminal is
fixed at (b-6,7), with supports owned by D and E. Global target nonreuse
remains a separate obligation.

That obligation is subsequently resolved by the [tight activation transfer](SECONDARY_TEN_TIGHT_ACTIVATION_TRANSFER.md)
for actual labelled residual claims with the full marked-side chain.
The general odd-B bar-window activation, without those additional
actual-chain and tight-gap hypotheses, is not globally credited here.

The first possible even B occurs at g=m+4 and is B=m+8. In this case
omega=6 would put C's far leg at (b-11,m+4), intrinsic (4,6), which
also belongs to D's upper bar. Thus omega>=8. By (3a), w>=10 is necessary
for this first negative successor. This localizes the remaining
width-dependent negative branch rather than bounding it by a finite
search. Its original support closure is the next task.

## 4. Resource scope and verification

The north-width-six and upward-zero-gap exclusions remove impossible
occurrences; they contribute no physical reserve or positive source.
An odd-B C contributes a real local positive activation, but it has not
yet been injected jointly with ALL old targets. Consequently no increment
is inserted into the global ledger. In particular the new result is not
a universal improvement of5/6 or a proof of mu=N+R-G>=0.

The [independent controls](../develop/check_secondary_ten_support_closure.py)
enumerate every bounded endpoint role at the forced sites, including
straight horizontal U interiors in the upward case, and all relevant
rotor tips. They validate the chart, bar window, phase charges and actual
odd-B support consumption, and treat intersecting prescribed sources
separately. Twenty north patterns have no consumer;400 disjoint upward
patterns give106562 bounded U roles,62652 positive activated successors
and43910 negative successors. There are3456 tight-gap controls and72
zero-gap noncompletion controls; all1680 relevant rotor checks exclude
their candidates. Eighty intersecting upward stencils are excluded
explicitly. [Output](../output/secondary-ten-support-closure-controls.json).
Finite enumeration checks the proof and does not supply its unbounded step.

[Scoped Lean](../formal/SubQuorum/SecondaryTenSupportClosure.lean)
checks the blocker/support coordinates, bar-window and tight-gap arithmetic,
and a full arbitrary-owner north obstruction conditional on the explicit
catalogue adapter. Actual U/rotor catalogue adaptation and bar orientation
classification remain written. The same distinction applies to global
injection, which is OPEN.

The final standalone Lean4.33.0 execution4e8873 passes all23 declarations
and their individual axiom audits, with only propext, Classical.choice
and Quot.sound and no warnings, sorry or native extensions. The general
far-leg-reach bound, tight-gap width-six collision and first-even-bar
width-six collision are included.
[Formal scope receipt](../output/secondary-ten-support-closure-formal-check.json).

Independent written audit399fba09 **ACCEPTS** the north obstruction, full
bar-window exhaustion including straight interiors, phase charges,
odd-bar activation and zero/tight-gap consequences. It also supplies the
additional tight-gap omega>=8,w>=10 collision incorporated above. The
original stream97430 exits0 with DONE/no errors; its14066-character
response exactly matches the completed API, observed gpt_6/pro. The
general far-leg-reach corollary and subsequent terminal rigidity receive
a separate **ACCEPT** in follow-up20923ea9, with the original rotor
support identities explicit; see the [rigidity review receipt](../output/secondary-ten-terminal-rigidity-review.json).
These written reviews do not
certify execution, realizability, global nonreuse or novelty.
[Receipt](../output/secondary-ten-support-closure-review.json),
[full response](../output/secondary-ten-support-closure-review-response.md).

Full allocation/grid equality, complete actual marked-chain realizability
and the larger-gap/width branches remain OPEN. Submitted DMGT, primary
star-forming/C4-free results and public main are preserved.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
