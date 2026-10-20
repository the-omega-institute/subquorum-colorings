# An arbitrary-width positive cap needs a long incoming U tip

20 October 2026. We replace a list of small cap obstructions by a
necessary condition for an unbounded cap family. The new argument
excludes short incoming U tips using an inward original support, rather
than the upward support used for the width-eight obstruction.

## 1. Family and admission theorem

Keep the complete fixed-source model and reference U/rotor constructors
of WIDTH_EIGHT_U_CAP_NONCOMPLETION.md. Let W>=6 and A>=4 be arbitrary
even integers. Consider the partial seed

    Rplus(0,0), Rplus(-3,0), Rplus(-1,-3),
    U(W,A,4)+(-4,-W).                                (1)

The cap has independent left height A and right height4. Subsequent
complete U sources have arbitrary even widths>=6, independent even
heights>=4 and arbitrary translations/isometries/phases. Any number
of rotors and permitted optional selections are allowed. Original
endpoint ownership, matching and mandatory supports are preserved.

**Admission theorem.** If (1) has a complete feasible extension, then
W>=12. The original owner of p=(-1,-1) must be a U whose endpoint at p
is a terminal tip with its own stem running physically left. If h is
that terminal's reference height, then

    8 <= h <= W-4.                                  (2)

The incoming U's bar extends physically downward. Its width and its
other leg height remain unbounded. Thus widths6,8,10 admit no complete
extension for ANY permitted A. For W>=12, (2) is necessary only; we do
not assert that any of its values gives a feasible completion.

All conclusions transport under a common lattice isometry of (1).
This classifies a residual family and gives no new unrestricted grid
bound or full mixed-source compensation theorem.

## 2. A fixed mask contained in every cap with W>=8

For W>=8, (1) contains the same43 known endpoints: the24 original
endpoints of the three rotors, together with

    {-4,-3} x {-7,-6,...,0},
    {(-2,0),(-1,0),(0,0)}.                           (3)

Call this set B. It is a partial endpoint mask, not a separate complete
source collection. It is contained in every cap regardless of A:
the first16 sites are within its two bar rows and the last3 within
its right stem. The corresponding integer-coordinate inclusions hold
for all W>=8,A>=4, not just a sample of dimensions.

The support p=(-1,-1) of Rplus(-1,-3) is absent from B and the entire
seed endpoint set. Its endpoint neighbors (-1,0),(0,-1) persist. Hence
p must have a foreign original endpoint owner in any feasible completion.

The three-blocker terminal lemma applies to every U owner: right, down
and two-up from p are known endpoints of B. Its own stem therefore
points left, its reference role is (a,1) or (b,w), and every back-ray
point at distances1 through h is its original endpoint. In particular
it contributes the five sites

    L={(-1,-1),(-1,-2),(-1,-3),(-1,-4),(-1,-5)}.       (4)

## 3. Rotor ownership is excluded for this entire mask

The exact sixteen-role rotor table against B has the sole candidate
Rplus(-3,-5). Its original support q=(-2,-1) is forced to be an endpoint
by the persistent neighbors (-3,-1),(-2,0),(-1,-1). It is not an endpoint
of that rotor or the seed cap/rotors, so its owner is foreign to them.

The four-site U barrier at up, right, two-left and four-down from q is
contained in B together with this rotor. The exact sixteen-role rotor
table at q is empty. Thus q has no permitted owner, contradicting
complete retention. This argument uses only B and original rotor
supports, so it works for every W>=8 and every permitted A.

Consequently p's owner must be a U. This is a static owner statement
inside a hypothetical final extension, without any insertion order.

## 4. Every short incoming terminal creates an impossible inner support

Assume its height h<=6. Since h is even and at least4, h is4 or6.
Its bar has adjacent physical columns p_c-h and p_c-h+1. The bar
cannot extend upward: its outer column would hit (-3,-5) for h=4
or (-3,-7) for h=6. Both are in B. Hence it extends downward.

Move one step left from the terminal. That point is in reference
row h-1, an odd nonterminal stem row. Its inward side, which now
points downward, is an ORIGINAL support of the same source. Thus

    r=(0,-2) belongs to its original support set.

The same incoming source has the bar endpoint

    (0,-h), namely (0,-4) or (0,-6).                  (5)

The support r is not an endpoint of its own source, by disjointness
of the complete original support and endpoint sets. Nor is it a seed
endpoint. Its two persistent endpoint neighbors (-1,-2),(0,-1) force
r to become a foreign endpoint. This does not assume that unspecified
endpoints of its supporting source omit r; the full support formula
establishes that fact directly.

No rotor can own r: its exact sixteen-role table is already empty
against B union L. For a U owner, the sites right, up and two-down
from r are foreign endpoints:

    (0,-1),(-1,-2),(2,-2).

Apply the reflected left-ray lemma. That candidate U would contain
every endpoint at distances1 through4 left of r. But one of them is
the foreign endpoint in (5): its distance is h-2, namely2 or4. This
contradicts endpoint disjointness. Therefore r has no owner.

This proves h>=8 for every extension containing B and the required
rotor support at p. The arbitrary source width and the other leg
height never enter the short-tip exclusion. Optional selections
cannot delete either mandatory support or its endpoint neighbors.

The flexible four-site stencil makes the last step explicit: for
each integer d with1<=d<=4, every U endpoint has an own endpoint
at right, down, two-up or d-left. It follows directly from the
three-blocker left-ray lemma, with no finite dimension enumeration.

## 5. The actual cap supplies the upper bound and bar direction

The cap's left stem contains the endpoint

    ell=(-1,1-W)=p+(0,-(W-2)),

because its reference row is3 and A>=4. If h>=W-2, the incoming
U's left back-ray would hit ell. Endpoint disjointness therefore
gives h<W-2. Since h and W are even, h<=W-4. Together with h>=8
this proves W>=12 and (2).

More generally, its bar cannot extend upward for ANY allowed h in
(2): the outer bar column at -1-h would hit the cap's lower bar row
at (-3,-1-h). That column lies between1-W and0 by h<=W-4, and the
incoming width is at least6. Hence the incoming bar points downward.

For W=6, the original four-site blocker at p excludes every U owner.
The unique possible rotor owner produces the same closed two-site
cavity as POSITIVE_U_CAP_NONCOMPLETION_OBSTRUCTION.md. That proof
uses the cap's bar/right stem and only reference rows2,3,4 of its
left stem, plus original rotor supports. All these endpoint sites
persist for arbitrary A>=4; q and both cavity sites remain outside
the extended left stem. Thus the same contradiction covers W=6
with arbitrary left height. No support of a truncated U is assumed.

## 6. Evidence, formal scope and remaining work

develop/check_short_tip_cap_barrier.py independently checks the fixed43
mask, the three complete rotor tables, mandatory neighbors, representative
short-tip support/bar controls and cap-mask inclusions for independent
dimensions. The finite cap10 UNSAT is discovery evidence only. Sections2-5
give the arbitrary-parameter proof and do not use a finite search bound.

formal/SubQuorum/ShortTipCapObstruction.lean imports the unchanged
universal coordinate lemmas from WidthEightUCapObstruction. It adds the
distance-parametrized stencil, universal short-tip support/bar consequence,
exact fixed-mask geometry and conditional bound arithmetic, together with
all-parameter cap bar/stem inclusions. All17 current declarations and their
individual axiom audits pass locally with Lean4.33.0 and one job. The
unchanged imported dependency was freshly compiled. Preflight memory was
40% free for that dependency and42% for the passing current-source audit;
comm-basename checks found no active real lean/lake process. No
sorryAx/native_decide. See output/short-tip-cap-barrier-formal-check.json
for scope and reproduction commands. Full source
isometry/support adapters, the physical wall argument and theorem assembly
remain written. We do not claim the whole admission theorem is in Lean.

This theorem is later than the width-eight ACCEPT and is reviewed
separately. It excludes all short incoming terminals in this cap family;
it does not exclude long terminals satisfying (2), other cap orientations
or positions, or feasible mixed sources generally. The remaining joint
allocation is still2G+BU+BR<=2N+2B11+Lambda, with every original slot and
physical tile credit used once. No improvement of that unrestricted bound
is inferred from an impossible partial configuration.

No email, draft or submitted-manuscript action is part of this result.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
