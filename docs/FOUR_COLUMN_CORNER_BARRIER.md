# A four-column rotor barrier forces the long-H return length

21 October 2026. This is a new addendum AFTER the initial long-H review
packet. That earlier packet does not cover this argument. The full mixed
allocation and rectangular-grid triple equality remain OPEN.

## 1. Four-column barrier lemma

Work in the finite complete original U/rotor model with disjoint original
endpoints and every unconsumed original support retained and having its
unique original anchor as its sole occupied neighbor. Use a lattice rectangle

    D=[l,u] x [c,c+5].

Its strict interior has FOUR columns c+1,...,c+4. Suppose a collection of
fixed original owners occupies every boundary vertex except possibly the
bottom-right corner (u,c+5), and those fixed owners have no endpoint on the
STRICT-INTERIOR segment of the first interior column:

    F intersect ({l+1,...,u-1} x {c+1}) = empty,

where F is their endpoint union. The top and bottom boundary points on that
coordinate column are permitted and required. The fixed owners may have
endpoints elsewhere in the interior.

**Barrier lemma.** No OTHER original source has an endpoint strictly
inside D, in any complete extension retaining those boundary owners.

**Proof.** Any lattice-edge path from a strict interior point to a noninterior
point must first visit a boundary vertex other than the possibly missing
corner. A corner has no strict-interior lattice neighbor. Therefore a foreign
connected endpoint source entering D is confined entirely to the strict
interior, even when the bottom-right corner is unoccupied or foreign-owned.

A U cannot fit: every permitted orientation spans at least five columns.
A rotor spans exactly four columns, so a confined rotor must use all four
interior columns. It has a UNIQUE endpoint on column c+1, a leftmost tip x.
In coordinates with x=(0,0), its endpoint set has exactly two possible forms:

    R-={(-2,1),(-1,1),(-1,2),(-1,3),
         (0,0),(0,1),(0,2),(1,2)},
    R+={(-1,2),(0,0),(0,1),(0,2),
         (1,1),(1,2),(1,3),(2,1)}.

R- has an original support at x+(1,0); R+ has an original support at
x+(-1,0). In either case that support y is STRICTLY inside D: both rotor
forms have endpoints at row x.row-1 and x.row+1, so either adjacent support
row stays between the horizontal boundaries.

At y, its original anchor x is occupied, and the left neighbor on boundary
column c is a fixed endpoint. Those neighbors are distinct. Support retention
forces y to be an endpoint. By the no-fixed-owner condition on column c+1,
its consumer is another foreign owner. That owner is confined by the same
path argument, cannot be a U, and is therefore a rotor with its own leftmost
tip exactly at y.

But two such rotors with vertically adjacent leftmost tips ALWAYS share
an endpoint. Both R- and R+ contain (-1,2),(0,2),(1,2). Consequently the
point x+(0,2) belongs to the rotor at x and to either rotor form at y,
whether y is above or below. The consumer cannot be the first rotor,
since y is its original support rather than its endpoint. This violates
disjoint original endpoint ownership. Hence there is no foreign rotor,
and no foreign endpoint at all. QED.

This is a local two-rotor collision proof. It uses neither an infinite
descent nor a finite search. The side-occupancy and no-fixed-owner conditions
are essential stated hypotheses; four-column width alone would not exclude
a rotor. The conclusion permits fixed owners' interior endpoints outside
column c+1.

## 2. Consequence: the return length is forced in a wider long-H subclass

Suppose a complete family contains endpoint-disjoint original owners

    B=U(6,b,e), map(b+3-r,c+1),
    H=U(6,b-2,k), map(r+3,c+2),
    b>=6, e>=4, k>=b-2,

with all usual evenness assumptions. Then necessarily

    e=b-2.                                         (1)

In particular the hypothesis e>=b-2 in the initial
[long-H channel theorem](LONG_HORIZONTAL_CORNER_CHANNEL.md) need not be
separately imposed in this width-six H subclass. Its permanent first lower
pair and nonreusing payment follow automatically.

**Proof.** If e>=b, B's far leg contains (3,7), also on H's upper bar.
Endpoint disjointness and evenness therefore give e<=b-2.

Use D=[4,b+2] x [3,8]. H supplies its top boundary, left boundary down
to b+1, and right boundary down to b+1 because k>=b-2. B supplies its
bottom boundary from column3 through7. Thus every boundary point except
possibly (b+2,8) is a fixed endpoint. Neither fixed owner has an endpoint
on the first interior column4. B may have interior endpoints on column7;
the barrier lemma explicitly permits this. Hence no foreign endpoint can
lie in the strict interior.

If e<=b-4, put m=b+2-e. Then 6<=m<=b-2, so x=(m,7) is strictly inside D.
It is B's original beyond-tip support at original coordinates(e+1,6).
Its own anchor is B's far terminal(m+1,7), and H's far leg provides the
second permanent endpoint neighbor(m,8). The latter exists because
k+3>=b+1>m. Thus x must be consumed. Neither B nor H has an endpoint at x,
so its consumer would be foreign, contradicting the barrier lemma.
The only remaining even length is e=b-2, proving (1).

For e<=b-4 the TWO prescribed owners have no complete U/rotor extension,
regardless of the number and dimensions of extra sources. For e=b-2,
the previously constructed eleven-source families realize every even b>=6.
Thus the forced-length conclusion is compatible with actual unbounded
complete families, and does not mistakenly exclude all long H.

## 3. Counting effect and scope

Every actual marked H claim with W=d=6, a=b-2 and k>=b-2 is now resolved
without an extra far-leg hypothesis: its complete geometry forces the
returning e=b-2, so it injects into the SAME permanent lower-pair union p
as the earlier long-H theorem. No new receipt pool or numerical term is
created by the exclusion proof itself. Wrong return lengths are impossible
configurations, not extra unmarked-owner bonuses or extra reserve.

The new [maximal-return rigidity corollary](MAXIMAL_H_RETURN_RIGIDITY.md)
uses the reflected barrier to force H's near leg when B's far leg is
maximal, without first assuming those lengths match. That corollary has
a separate verification and review scope. H with wider returning sources,
other unmatched near or shorter far legs, Vcorner, occupied corridors,
vertical exits and universal residual
coverage remain open. Neither this barrier nor the preceding channel lemma
establishes unrestricted allocation or the grid triple equality.

The checker reconstructs both rotor endpoint/support forms, all eight
adjacent-tip collisions, rectangle barriers and mandatory wrong-return
support stencils at independent lengths. These finite checks supplement
the explicit all-dimensional proof above. Source-to-rotor classification
and physical counting adapters remain written where noted by the separate
Lean receipt. The separate written review191f56c9 ACCEPTS both the barrier
and forced-return conclusion under the stated source/support model. Its
strict-interior column clarification is incorporated above. The review does
not certify checker/Lean execution or establish unrestricted allocation.

All twelve declarations in FourColumnCornerBarrier.lean pass local
Lean4.33.0 source and individual axiom audits, session71687 exit0. The
preflight measured62% free memory and no lean/lake executable by comm
basename. Only ordinary propext/Classical.choice/Quot.sound occur; the
rotor spine declaration is axioms-free. No sorry/native reduction is used.
The support-forcing and complete constructor adapters remain written.
Controls pass two rotor forms, eight adjacent-tip collisions,108 confined
placements,114 disjoint H/B patterns and96 wrong-return stencils.

Submitted manuscripts and correspondence are unchanged.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
