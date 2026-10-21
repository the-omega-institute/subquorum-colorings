# A positive north package forces a second owner in a strict bar window

21 October 2026. This is a subsequent support-closure result, beyond the
initial independent review input for the [neutral gap-four package](SECONDARY_TEN_NORTH_GAP_FOUR_PACKAGE.md).
It removes the nominal h=t boundary from COMPLETE outward instances and
describes the next actual consumer. The endpoint-disjoint partial package
and its exact algebraic identity remain valid at that boundary.

## General theorem

Retain precisely the complete original-source hypotheses of that note,
with a=b-9, Q,D,L, and the actual positive outward consumer

    D=U(w+4,10,t), D(r,c)=(a-2+r,c+5),
    L=U(w,4,v), L(r,c)=(a+r,c+6),
    C=U(K,h,f), C(r,c)=(a+h-r,w+6+c), h>=t.

The shared ORIGINAL support s=(a+1,w+8) is absent from Q/D/L/C.
Its original anchors are D(3,w+4)=(a+1,w+9) to the east and
C(h-1,1)=(a+1,w+7) to the west. It cannot remain retained. Thus a
distinct actual U owner E consumes s, with

    E=U(J,g,z), E(r,c)=(B-r,w+7+c),
    a+t<=B<=a+h-2,
    B-a-1<=g<=B-a.                           (1)

All J,g,z are legal even original dimensions. In particular

    h>=t+2.                                 (2)

There is no complete extension in the nominal h=t case, irrespective
of additional source dimensions or the other legal parameters. In (1),
B is an integer, not assumed odd. The existing U phase table gives

    B odd: g=B-a, near terminal (a,w+8), charge -1;
    B even: g=B-a-1, near terminal s, charge 1-J.

Thus the next forced consumer is negative in BOTH phases. It supplies
no new positive owner or activation credit.

If h=t+2, the bar window and parity force

    B=a+t, g=t, J<=K-2, K>=8.               (3)

Its original terminal supports are (a-1,w+8) in D and (a,w+7) in C.
In particular a breadth-six outward C cannot have the tight incident
length h=t+2 in a complete instance. These are necessary forms, not a
claim of complete realizability or a global compensation increment.

## Proof for arbitrary original dimensions

The shared-support and anchor identities follow directly from D's
odd intrinsic far-stem support (3,w+3) and C's odd intrinsic near-stem
support (h-1,2). Their two anchors are distinct endpoints. Point s is
strictly between D's stems, right of L, outside C's own stem/bar, and
right of every Q endpoint. Completeness forces a consumer whose own
endpoint neighbors can only be north/south.

The complete U catalogue leaves vertical terminals and vertical straight
leg interiors; perpendicular corners and degree-three roles cannot fit.
All four vertical rotor tips are blocked. Each north tip contains a
relative endpoint (-2,1) or (-2,-1), on D's lower bar at row a-1.
South A contains (2,-1) and south B (1,-1), on C's original near
stem or its bar junction. These endpoints exist even at h=4.

For a U the whole incident leg and both bar rows lie strictly below
D's lower bar at row a-1 and above C's first bar row a+h-1, at the
column of s. A bar above s is impossible: an admissible leg point is
at least two steps from its outer bar, leaving no room between s and
the D row. A bar below s cannot point left, because C's near stem at
column w+7 occupies every row from a through a+h. Therefore its bar
is below and to the right, giving the unique frame E in (1).

The two bar rows B-1,B cross D's far-stem column w+9. D occupies that
column through row a+t-2, so B>=a+t. The incident stem at w+8 cannot
reach C's bar row a+h-1, hence B<=a+h-2. Its terminal row B-g is at
least a, since it cannot meet D's lower bar; and the owned point s has
intrinsic coordinates (B-a-1,1), hence g>=B-a-1. This proves (1),(2).
Evenness of g leaves exactly the two terminal/charge cases stated above.

At h=t+2 the interval for B is a singleton, B=a+t, which is odd because
a is odd and t even. Thus g=t. Suppose J>=K. C's endpoint C(2,K)
is (a+t,w+6+K), since its independent far leg f>=4. E's bar contains
that point with intrinsic coordinates (0,K-1), because J>=K>=6.
This contradicts original endpoint disjointness. Evenness gives J<=K-2
and legal J>=6 gives K>=8. Its stated original support owners follow
by evaluating E(g+1,1) and E(g,0).

## Scope and verification

The direct checker includes bounded role exhaustion at s, every relevant
rotor, the interval and phase formulas, the empty h=t case and tight
width exclusion. Scoped Lean checks the shared original support sites,
blockers, parity/window implications and tight width collision. Catalogue
adaptation, the general geometric window proof and phase count remain
written. Finite enumeration is not their unbounded proof. See the
[checker](../develop/check_secondary_ten_north_gap_four_package.py),
[cavity controls](../output/secondary-ten-north-gap-four-package-controls.json),
[Lean source](../formal/SubQuorum/SecondaryTenNorthGapFourPackage.lean)
and [formal scope receipt](../output/secondary-ten-north-gap-four-package-formal-check.json).

The five-source obstruction in the preceding note uses h=t=4; this
theorem explicitly shows why it is not complete. It still correctly
refutes the ENDPOINT-ONLY external-sign rule, which assumed no completeness.
No complete-model rule or target inequality is refuted. The next task
is to account for E and its further actual support closure jointly with
external source mass and events, without spending the neutral package
as surplus or counting E as a positive owner.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
