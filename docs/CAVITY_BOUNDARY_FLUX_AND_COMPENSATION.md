# Exact cavity boundary flux with escaping complete combs

19 October 2026. This extends `CLOSED_SOURCE_CAVITY_COMPENSATION.md` by
removing containment of contact combs. It identifies exactly the additional
term when combs escape a source cavity, and gives a common original-resource
inequality for cavity networks. It does not establish an unconditional bound
on that term or a universal grid theorem.

## 1. Hypotheses and physical end membership

Use the original whole-receiver ledger

    Delta=-B+D_all+E,        E>=0,                    (1)

at the fixed single-terminal representative. Fix a positive root source and
its complete inner cavity C, as in the closed-cavity note. Every endpoint
meeting C belongs either to a prescribed complete straight comb, whose full
endpoint component may extend outside C, or to one of n fully enclosed
positive long sources parallel to the root. No partial foreign source or
other endpoint shape is allowed inside C. The root has no endpoints in C.
Matching and supports are the actual prescribed ones, with the usual
outside receiver/normalization coverage. Different roots may have different
tile-preserving orientations; each cavity is analyzed in its root's frame.

For each complete comb K with physical singleton end tiles S_K (sparse)
and U_K (saturated), define

    phi_C(K)=1[U_K in C]-1[S_K in C],
    Phi_C=sum_K phi_C(K).                            (2)

Combs without singleton end tiles contribute zero. Membership concerns an
original physical tile, and is never membership of an auxiliary shifted
square or a selected side support alone. Each summand is -1,0 or 1.

## 2. The exact leaky-cavity identity

Let D_C,D'_C denote the original and horizontally shifted no-endpoint
deficits, with the root's extreme columns trimmed in the second partition.
Then

    D_C=2+2n+Phi_C+D'_C.                             (3)

Proof. The root's boundary contains exactly 2h selections and no endpoints,
and the partition sizes differ by h+1, independently of comb containment.
The raw partition identity in the closed-cavity note therefore still gives

    D_C-D'_C=2+sum_K(E_C(K)-E'_C(K)).                 (4)

Every enclosed parallel positive source contributes two, by the shifted
source count already proved there. For a comb parallel to the cavity's
row bands, a path meeting C cannot escape its extreme endpoint-free columns;
its fixed row is in C. Thus the whole horizontal comb is inside C and its
raw weights are zero in both partitions. Both physical singleton ends, if
present, are in C, so its phi_C is zero.

A perpendicular comb may leave through a transverse boundary. In any
physical row band meeting its path in two endpoints, the endpoint square
has (p,t)=(2,1) in both column phases and raw excess zero. A singleton row
band is an actual physical end band of that complete comb: C is a union of
whole physical row pairs, so cutting C does not invent a singleton end.
Its physical tile has (1,1) at a sparse end or (1,2) at a saturated end.
The horizontally shifted square flips those two types, because the selected
side support and the forced-blank side exchange receiver membership; the
axial support remains in the row pair. The raw difference is respectively
-1 or +1. These labels follow from the retained complete-comb supports
and feasibility in the arbitrary exterior, as in the accepted comb tables.

Summing the actual physical end memberships gives exactly phi_C(K).
All endpoint squares have unique component owners. Thus the final sum in
(4) is 2n+Phi_C, proving (3). The partial E terms are auxiliary raw counting
weights only. No partial endpoint receiver is assigned a corrected donor
charge or exported matching credit. QED.

Complete-component closure makes both ends of each comb belong together,
so Phi_C=0 and (3) recovers the stronger closed-cavity identity. In general,
it is the aggregate signed membership in the entire cavity that matters;
the original mouth's end flux may differ.

## 3. One unified physical-resource inequality

Take any finite collection of such cavities C_j. Let k_j=1+n_j, K=sum_j k_j,
and Phi=sum_j Phi_(C_j). Suppose every original positive-deficit no-endpoint
tile belongs to at most c cavities, with an integer c>=1. Nonnegative shifted
deficits and original physical incidence give

    2K+Phi <= sum_j D_(C_j) <= c D_all,
    c Delta >= 2K+Phi-cB+cE.                         (5)

The allocation is literal: a physical tile of deficit d is counted with
its actual cavity multiplicity, at most c. Endpoint charge is still included
only once through (1), and shifted deficits are only nonnegative slack.

In particular:

- Disjoint cavities accounting for every source have K>=B. They prove
  coefficient one whenever Phi>=-B, and Phi>=0 gives Delta>=B.
- Cavities of multiplicity at most two accounting for every source satisfy
  2Delta>=Phi. Therefore Phi>=-1 suffices by integrality.
- More generally coefficient one follows whenever
  2K+Phi-cB>=-(c-1), since c Delta is an integral multiple of c.

These are sufficient conditions; no universal lower bound on Phi is asserted.
The deficit-zero exemption requires uniform zero over a claimed completion
class, just as in the closed-cavity incidence theorem.

The flux admits a network interpretation without spending any additional
resource. For each complete comb, let nu_S,nu_U count selected cavities
containing its sparse and saturated physical singleton tiles. Then

    Phi=sum_K(nu_U(K)-nu_S(K)).                      (6)

Hence nu_U>=nu_S for every comb suffices for Phi>=0, while only the aggregate
condition is needed. Equal membership cancels even when the two ends lie in
different cavities. This gives a precise cross-component routing criterion:
internal end contacts cancel, and only unmatched signed end multiplicity
remains. It does not require assigning two separate copies of a physical
donor to the two participating source cavities.

With nonnegative cavity weights lambda_j one can instead impose pointwise
sum_(j:Q in C_j)lambda_j<=1 and use the lower bound
sum_j lambda_j(2k_j+Phi_j). No numerical optimization can certify a pointwise
incidence condition that the geometry does not satisfy.

## 4. Initial data and actual limits

For an initial-pair theorem require every initial endpoint in every cavity
to belong to one of the prescribed frozen complete combs or fully enclosed
parallel sources. Comb containment is no longer needed. Their endpoints and
supports persist under normalization; other components never add endpoints
to a cavity, and promotions only change their own existing endpoint sites.
Thus cavity labels and physical end memberships remain fixed. The stated
outside coverage is still required for E>=0. Alternatively impose all data
at the fixed terminal representative.

The existing zero-mouth remote family has two sparse ends inside C and
their saturated ends outside, so Phi_C=-2. Equation (3) becomes D_C=D'_C;
it supplies no positive structural lower bound by itself. In contrast,
the new occupied-rung family has mouth flux -2 but cavity flux zero because
its entire three combs are inside C. It obeys D_C=2+D'_C. This precisely
distinguishes a missing closure/flux hypothesis from a failure of the target
bound. The remote family is not claimed to have actual D_C=0.

The theorem still excludes partial foreign sources, perpendicular enclosed
sources and arbitrary bent components. Finding sufficiently many cavities
with the required source coverage, controlled signed end membership and
adequate unique physical capacity is the remaining geometric existence
problem. Equation (5) is a counting theorem under its hypotheses, not a
solution of that existence problem.

## 5. Verification scope

`develop/check_cavity_boundary_flux.py` checks 69 physical configurations:
48 open-comb instances with Phi_C=-2, 16 endpoint-free sharp cavities with
D_C=2,D'_C=0, four nested source examples, and one zero-mouth occupied-rung
example with mouth flux -2 but cavity flux zero. It recomputes per-component
raw phase differences, physical end membership and both physical ledgers.
The 48 closed-cavity controls are rerun after adapting the checker.

Scoped Lean statements prove the doubled conditional partition identity and
the disjoint/twofold aggregate consequences. Full geometric phase tables,
membership preservation and cavity existence remain written or open as
specified above. This extension is distinct from the independent review
of the earlier closed-cavity note; acceptance of that note is not acceptance
of this later extension.
