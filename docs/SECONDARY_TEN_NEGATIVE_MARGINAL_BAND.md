# A positive next consumer with unbounded negative marginal

21 October 2026. This is a general obstruction to a local compensation rule
on prescribed partial original-source inventories. It is not a counterexample
to the complete-family inequality or to rectangular-grid equality.

## Hypotheses and statement

Use the original U/rotor source model, retained original supports, fixed even
tile phase, and functional Phi=N+S+2F-Ev from
[the persistent-pair note](SECONDARY_TEN_PERSISTENT_PAIR_COMPENSATION.md).
Here N counts positive ORIGINAL owners, S is negative original-charge mass,
F counts mixed endpoint-full tiles excluding original-own full tiles, and Ev
counts directed foreign intratile endpoint contacts excluding targets in the
source owner's ORIGINAL support set. No original support is deleted upon
consumption.

Let b be even, a=b-9, and w>=12 even. Let A consist of the six fixed sources
Q,D,L,C,E,W, followed by T0 and the residual source

    V=U(k,8,z),  (r,c) -> (a-6+r,w+12-c),

where either k=w+8 and z is even with 4<=z<=14, or k=w+10 and z>=16 is even.
The established inventory gives Phi(A)=w+8 and Phi(Q,D,W)=w+9.
For ANY even ell>=12 add

    K=U(6,ell,ell-8),  (r,c) -> (a+1-ell+r,w+15-c).

The preceding note proves q(K)=1 and DeltaPhi(K|A)=0. K consumes the two
persistent supports e=(a,w+14), t=(a+1,w+14), but its far lateral support

    rho=(a-7,w+8)

is missing and forced: K has the endpoint east of rho, and V has the endpoint
south of rho. Now define

    H=U(6,4,w+4),  (r,c) -> (a-13+c,4+r).

**Theorem.** H is endpoint-disjoint from A+K and consumes rho. It is a
positive original owner, q(H)=1, but its exact insertion counts are

    DeltaN=1,  DeltaS=0,
    DeltaF=w/2+3,  DeltaEv=3w/2+7,
    DeltaPhi(H|A+K)=-w/2.

Consequently Phi(A+K+H)=w/2+8>0 and its difference from Phi(Q,D,W) is
-w/2-1. Thus there is no width-independent lower bound on the marginal of
such a candidate consumer in these partial inventories, even if the candidate
is positive and consumes a forced original support of the preceding consumer.

## General geometric proof

H has vertical bar columns 4,5 and rows a-12 through a-7, upper horizontal
stem row a-12 and columns 6 through 8, and lower horizontal stem row a-7
and columns 6 through w+8. Its far terminal is exactly rho.

V has bar rows a-6,a-5. Its bar begins at column 4 in the first residual
family and column 2 in the second; it ends at w+11 in both. Its far stem
is therefore in column 4 or 2, entirely below the H bar and stems. T0's bar
and all six fixed sources are also below H. All K endpoints have columns
at least w+9; H endpoints have columns at most w+8. These inequalities prove
endpoint disjointness for every allowed z,ell,w and translation, without a
dimension bound.

The elementary original-source count in this phase is

    |M_H|=w/2+9,
    number of endpoint tiles=w/2+8,
    original supports inside those tiles=w/2+8.

Indeed, the six-row vertical bar occupies four tile rows in its single tile
column: its first and last rows each occupy half a tile row. The short upper
stem contributes two new tiles and the long lower stem contributes w/2+2
new tiles. The two bar-corner supports and two terminal axial supports all
lie in endpoint tiles. Two of the three short-stem lateral supports and
the w/2+2 even-indexed long-stem lateral supports also lie in endpoint
tiles; the odd-indexed lateral supports lie outside them. Thus there are
4+2+(w/2+2)=w/2+8 counted supports. Substitution in
q=|M|+|A in tiles|-2|tiles| gives q(H)=1, DeltaN=1 and DeltaS=0.

Only the following endpoint tiles are shared with the old inventory.
Coordinates in this table are LOWER CORNERS in the fixed tile phase.

| Lower corner | Number | Newly full | New directed events |
|---|---:|---:|---:|
| (a-7,c), c=4,6,...,w+6 | w/2+2 | 1 each | 3 each |
| (a-7,w+8) | 1 | 1 | 1 |

To verify exhaustiveness, H's upper tiles end at row a-11 or a-9 and
columns at most 8. The old V endpoint tiles start at lower-corner row a-7;
the other old owners start lower still, except K whose tile columns start
at w+8. Hence only H's lower-stem tiles can meet old endpoint tiles.

In every central tile (a-7,c), V occupies both bottom corners and H both
top corners. Both V-to-H vertical events survive: neither top corner is a
V original support. Of the two H-to-V vertical events, precisely the even
column target is an original lateral support of H and is excluded. Thus
one H-to-V and two V-to-H events survive. Horizontal edges belong to their
respective individual sources and create no foreign event.

In the terminal tile, V again occupies both bottom corners, K the top-right
corner, and H fills the top-left corner rho. The H/K horizontal directions
are both excluded by their owners' original supports. The H-to-V vertical
direction is excluded by H's original far lateral support. The single
V-to-H direction survives. The old V-to-K event remains counted once and
is not an increment. Each tile becomes mixed full; none is original-own
full. This proves the table as an exact set partition, not just a lower bound.

Summing once over that partition gives

    DeltaPhi=1+2(w/2+3)-(3w/2+7)=-w/2.

The formula holds uniformly in both residual families and all ell>=12.
Choosing arbitrarily large even w proves the claimed absence of a constant
lower bound on this partial-inventory marginal.

## Completeness and what fails

The support (a+9,6), shared by Q and D, is still missing as an endpoint.
Its north and south neighbors remain D and Q endpoints. Neither K nor H
consumes it. The displayed family is therefore NOT complete. The marginal-count
theorem alone does not decide complete extendibility. The subsequent
[narrow-cap noncompletion lemma](SECONDARY_TEN_NARROW_CAP_NONCOMPLETION.md)
now proves that A+K already has NO complete feasible U/rotor extension,
before H is inserted. The negative-marginal family is thus excluded from
the complete model. In particular, its
absolute Phi is positive, and the negative difference from a baseline is
not the target inequality.

The failed rule is that every successive forced-support consumer supplies a
nonnegative (or uniformly bounded-below) independent reserve receipt in any
prescribed partial inventory. Here a positive owner's unit is overwhelmed by
the exact signed contribution of an occupied adjacent band. A complete-model
proof can now discard this specific branch by the cited noncompletion lemma.
Other branches still require complete-family exclusions or joint accounting
of further owners and their boundary contributions. Counting
rho, or either previously consumed persistent support, as another credit
would miss these directed contacts.

## Verification scope

Run `python3 develop/check_secondary_ten_negative_marginal_band.py`.
The checker independently reconstructs original endpoints, supports and
matchings, tests exact shared-tile and directed-event SETS, and checks the
persisting missing support. Translated, long-leg and large-width cases are
finite corroboration of the general proof above. This note has no new Lean
verification or independent Oracle verdict. The earlier ACCEPT covers the
return classification and full mandatory-support inventories only.
