# Actual incoming U10 sources preserve a joint activation remainder

20 October 2026. In the full finite original U/rotor model, an actual incoming
source of the form below prevents its positive terminal from being any B
output, including cap outputs. This holds at every legal positive width,
without the AA restriction. Together with the grouped C/D and cap exclusions,
it preserves a set of actual activations in the SAME all-route remainder.
The unrestricted allocation and rectangular-grid equality remain OPEN.

## Hypotheses and actual occurrence keys

Retain all complete-source, fixed-partition, endpoint-uniqueness, unchanged-
matching, mandatory-support and selected-degree hypotheses of
[the enhanced D budget](BACKFILL_D_INTERIOR_TWO_CORNER_COMPENSATION.md).
All U widths are even and at least6; their independent heights are even and
at least4. Recurring original owners and arbitrary other sources remain allowed.

Normalize a positive source to O=U(w,L,b), with its right terminal z=(b,w).
Require an ACTUAL original incoming U10 source

    V(s,t)=(k+2-s,t+w-2), from U(v,k,f), k>=b.       (1)

This is an additional geometric hypothesis, not inferred from a numerical
saturation census. No width-six or L>b condition is required here. Coordinate
changes transport the original physical partition. Source reflections may
exchange the independent original left/right height labels.

Put p=(b+1,w-1), q=(b+1,w-2). Their inverse V coordinates are
(k-b+1,1) and (k-b+1,0). Thus V owns p and lacks q, including k=b.
The positive beyond-tip support s=(b+1,w) has the two persistent endpoint
neighbors z,p. If s remained selected its occupied degree would exceed one.
Mandatory retention therefore forces s into P. The existing activation A
counts an original terminal1P2T occurrence when at least ONE of its two
intratile supports is consumed. Thus s already proves an actual activation;
no assertion about its other support is needed. At a full cap or C/D/B
output both supports are consumed, as in the preceding proofs.

## All B outputs are excluded by the two complete sources alone

Suppose a B event outputs at z. The original B coordinates have terminal
x=(1,-a-1), positive-source map (s,t)->(t,-s-1), and companion map
(s,t)->(t-1,s-h-1). The terminal's outward west direction and north side
support fix the transport to O as

    Phi(r,c)=(-c-1,w+1-r).

Hence a=b and the actual U11 companion becomes

    F(s,t)=(h-s,w+2-t), from U(u,h,g), h>=b+2.      (2)

The boundary h=b+2 is the B cap case; h>=b+4 is interior. Both are covered.
F owns the complete column w+1 through rows0,...,h, and its bar owns
(h,w-1). V's bar owns (k+1,w+1), and its near stem owns column w-1
through rows2,...,k+2.

- If k+1<=h, the point (k+1,w+1) belongs to both V's bar and F's stem/bar.
- If k+1>h, the point (h,w-1) belongs to F's bar and V's stem.

These are exhaustive, including equality. F and V are different original
owners: their fixed original phases are11 and10. Thus recurring owners
cannot evade the endpoint contradiction. No second-corner classification,
rotor exclusion or assumption about the other positive activation is needed.

## Separation from the other positive claims

A positive cap filler at z has exactly two normalized U11 cap-owner maps:

    (s,t)->(b+2-s,w+2-t),
    (s,t)->(b+2-t,w+2-s).

Both own p and q: their inverse coordinates are respectively (1,3),(1,4),
or (3,1),(4,1). Since V lacks q, either cap owner differs from V, then
collides at p. Thus z cannot belong to Fpos.

For a C/D positive second corner, use the same EXACT grouped stencil as the
[C two-corner](BACKFILL_TWO_CORNER_COMPENSATION.md) and
[D enhancement](BACKFILL_D_INTERIOR_TWO_CORNER_COMPENSATION.md) proofs.
The two compatible terminal support frames send either F's two adjacent
stem endpoints or H's two adjacent bar endpoints to p and q. The SAME
original owner contains both. Its q distinguishes it from V and its p
contradicts endpoint uniqueness. This does not depend on w=6. Consequently
z belongs to neither Cplus nor Dplus.

## One preserved activation family and the simultaneous bound

Let Wterm be the set of original (positive owner, terminal index) occurrences
having an actual incoming source (1), and put omega=|Wterm|. Count each terminal
once even if more than one event refers to it. All are actually activated and
are disjoint from the established jointly disjoint families

    Fpos, Cplus, Binterior, Dplus.

Therefore, with Binterior denoting the EVENT count formerly written b,

    rhoA=A-Fpos-Cplus-Binterior-Dplus >= omega.       (3)

The old inequality rhoA>=Eterm also remains. Without an additional disjointness
proof, retain rhoA>=max(omega,Eterm); do not add omega+Eterm.

Substitute (3) in the SAME enhanced all-route identity, once:

    2R=Kback+KC+d-2(K01+K10)+e+Q+rhoA+Z0+H+Lnew.

The resulting bound is

    2R>=Kback+KC+d-2(K01+K10)+e+Q+Z0+H+omega.       (4)

All counters and occurrence families must cover the SAME chosen source
collection. This improves that lower bound by a retained omega, with no new
reserve. It does not remove the signed negative-source count. When the already
established AA incoming theorem applies to both actual short-tip activations,
omega=A=2 and (3) excludes all four positive claim families. This recovers
the AA negative-only census by a shorter no-B proof, rather than excluding all
AA components. Outside AA it remains conditional on ACTUAL incoming sources.

## Verification scope

[IncomingTerminalReserve.lean](../formal/SubQuorum/IncomingTerminalReserve.lean)
checks the arbitrary-width incoming present/missing pair, complete B companion
crossing and disjointness contradiction, both cap orientations, and conditional
joint-budget deductions. Actual phase/role normalization, mandatory-support
activation and global occurrence-family separation remain written adapters.
The original Oracle research proposed the general B crossing; the present
proof and its activation definition are checked against the original model.
Finite physical controls are for coordinates, not a general-proof substitute.
