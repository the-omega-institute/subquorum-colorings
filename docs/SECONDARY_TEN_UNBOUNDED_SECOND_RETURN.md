# A positive forced-site owner can create an unbounded second return debit

22 October 2026. This extends the
[first return-debit family](SECONDARY_TEN_SHARP_RETURN_DEBIT.md).
The new conclusion is uniform in two independent, unbounded parameters.
Consuming the next forced support can create a debit proportional to
the width of an earlier occupied band, even when the new owner has
positive charge. Thus two forced-owner steps, endpoint
disjointness and positive-owner counting alone cannot establish a
nonnegative selected-union compensation rule.

The construction is a partial family of complete original U records.
It does not assert a complete feasible extension and does not refute
the global inequality or the selected-pair theorem. Its enlarged
family still has a forced support requiring another owner.

## Two independent even parameters

Let h>=12 and g>=4 be even. Construct H3 with two blocks,

    a_0=31, s_0=0, w_0=h, w_1=12,
    z_0=z_1=g+24, root breadth6.

Then a_1=g+49,s_1=-24. Add

    R=U(32,10,g+2), chart(g+38+r,2-c),
    T=U(6,4,g), chart(g+41+r,-23-c),
    W=U(2g+20,4,40), chart(2g+42-c,r-34).

R and T have selected-pair gain4. W consumes their common forced
support x=(2g+41,-30), has marginal-3 and leaves z=(22,7) forced.
The first-return proof remains valid for any h: only the first six
columns of the P_0 bar participate, and every earlier base endpoint
remains to the right of R. In particular

    Phi(H3+R+T+W)-Phi(H3)=1.

Now add the positive original

    V=U(6,4,h+8), chart(r,c)=(16+c,h+15-r).          (1)

It consumes z as its far terminal and is endpoint-disjoint from ALL
the previous records. Its exact marginal and combined gain are

    DeltaPhi(V | H3+R+T+W) = -h/2-2,
    Phi(H3+R+T+W+V)-Phi(H3) = -h/2-1.             (2)

Both formulas hold for every permitted h,g. The second quantity tends
to minus infinity with h, even with g fixed or with both earlier far
legs arbitrarily long.

## Endpoint geometry and source charge

V's two-column bar occupies columns h+14,h+15 and rows17,...,22.
Its near leg is row17, columns h+11,...,h+15. Its far leg is row22,
columns7,...,h+15. All H3 endpoints are at rows at least23. The
earliest old endpoints are the P_0 bar at row23, columns1,...,h+12.
R and T start below row22. W's bar is left of column-32, its short
leg lies at row2g+41, and its far leg is row22, ending at column6.
This proves endpoint disjointness and z in V without a size cutoff.

Direct immutable-source counts for V are

    matching=h/2+11,
    endpointTiles=h/2+10,
    originalSupportsInside=h/2+10,
    charge(V)=1.

The bar has four endpoint tiles, the near leg adds two and the far
leg adds (h+8)/2. Both bar-end supports and both axial terminal supports
lie inside. The near leg contributes two lateral supports at intrinsic
even rows2,4; the far leg contributes (h+8)/2 at intrinsic even rows.
Thus the inside count is4+2+(h+8)/2=h/2+10. V therefore adds
one positive-owner count and no negative mass. This is precisely why
positive-owner count by itself cannot pay the following event debit.

## Exact new full tiles and directed events

Physical tiles are specified by even top-left coordinates. Every NEW
mixed full tile is in the band at rows22,23. Their top-left corners are

    (22,c), c=6,8,...,h+10.                         (3)

There are h/2+3. At c=6 the upper-left belongs to W, upper-right to V,
and both lower cells to P_0. All other tiles have V above and P_0 below.
The c=6 tile was not full before V and is counted once. V's remaining
bar tiles are single-owner tiles, which are not mixed full tiles.

The complete NEW directed-event list is

    P_0:(23,c) -> V:(22,c), c=7,...,h+12;
    V:(22,c) -> P_0:(23,c), c=8,10,...,h+12.        (4)

The first row contributes h+6 events and the second h/2+3, for
3h/2+9 altogether. The downward directions from odd V columns are
excluded by V's immutable original lateral supports. The two horizontal
W/V directions between (22,6) and z are excluded by their respective
axial supports. The P_0 upward event at column6 already existed before
V; it is not counted a second time. There are no other foreign endpoints
in V's physical endpoint tiles. Consequently (3) and (4) give

    1+2(h/2+3)-(3h/2+9) = -h/2-2,

proving (2) for all parameters. No old mass, old positive-owner count
or earlier full-tile credit has been reused.

## The next forced support and the precise obstruction

The point q=(23,h+13) is an original lateral support of V and an
original bar-end support of P_0. It is absent from the enlarged
endpoint union. Its occupied endpoint neighbours are exactly

    V:(22,h+13), P_0:(23,h+12).

Its other two neighbours are absent. Thus every complete extension
containing this partial family must consume q with another fresh
original. That next original cannot be a rotor. Indeed its internal
endpoint neighbours at q must lie south or east. A rotor endpoint
having this restriction is a terminal. Substitution in the eight
rotor symmetries gives four distinct relative endpoint patterns:

| Pattern | Own neighbour at q | A mandatory extra relative endpoint |
|---|---|---|
| South terminal, first chirality | (1,0) | (2,1) |
| South terminal, second chirality | (1,0) | (2,1) |
| East terminal, first chirality | (0,1) | (-1,1) |
| East terminal, second chirality | (0,1) | (2,1) |

But q+(2,1)=(25,h+14) is an endpoint of the retained root K, and
q+(-1,1)=(22,h+14) is an endpoint of V. Every possible rotor
therefore collides with a retained endpoint. This is an exhaustive
fixed-shape substitution, uniform in h,g, not a bounded search over
unclassified U dimensions. Under the full U/rotor model, q must be
consumed by another U. Complete extendibility remains open.

The counterexample is to a rule on partial selected unions: neither
two successive forced-site receptions nor requiring the second owner
to have positive charge guarantees nonnegative new compensation.
Any proof valid for actual complete families must either exclude
these returns by complete-closure constraints or account jointly for
the next q-consumer and the old band without reusing an earlier
reserve. The target global inequality has not failed.

The exact-set verifier checks every new full tile and owner-labelled
event, both source-count increments, the variable-width first return,
the next forced support, all four rotor exclusions and invariance
under even translations. The
scoped Lean module proves the conditional receipt arithmetic and
unboundedness. Neither replaces the written source-chart proof.
This later result is outside the both-far main-theorem review input.
