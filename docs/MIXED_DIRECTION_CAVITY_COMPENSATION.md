# Complete perpendicular sources have at least two units of phase gain

19 October 2026. This note removes the parallel-orientation restriction on
fully enclosed positive sources in the closed-cavity and boundary-flux
theorems. The new step uses adjacency along the entire chamber flanks;
the older nonnegative phase estimate for individual row bands loses this
information. No claim is made about arbitrary partially entering sources.

## 1. Setting and a whole perpendicular source

Retain the feasible single-terminal pair, original physical tiling and
prescribed long-source matching/support conventions of the previous notes.
Take a horizontal root cavity C: its physical squares start at even rows
and even columns in actual coordinates. Its extreme columns have no
endpoints. Trim those columns and shift the column partition by one vertex.

Suppose a complete prescribed positive long source K lies in C, with its
whole chamber perpendicular to the root's chamber. Normalize K to open
rightward. Its chamber occupies rows u,...,v and columns c,c+1, where
u is odd, v is even, w=v-u+1 is even and at least eight, and c is even.
Its two horizontal arms lie in rows u,v and open to the right. Physical
tile-preserving reflections cover the other directions. Let E_K,E'_K be
the raw excess sums t+p/2-2 over endpoint-containing squares belonging to
K in the physical and shifted cavity partitions. Complete containment
and the endpoint-free extreme columns place both whole receivers in C.

Write ell for the number of selected sites on the outer chamber flank

    L={(row,c-1):u<=row<=v},

and q for the number selected on the arm-side interior flank

    I={(row,c+2):u+1<=row<=v-1}.

These count actual selections, including optional ones in a feasible exterior;
they are not extra donor resources.

## 2. Exact phase formula and its sharp lower bound

**Whole perpendicular-source lemma.** Under these hypotheses,

    E_K=1,
    E'_K=1-w+ell+q,
    Gamma_K=E_K-E'_K=w-ell-q>=2.                     (1)

Proof of the exact formula. The original raw sum is +1 by the complete
positive-source receiver count. In each of the (w-2)/2 physical row bands
strictly between the chamber end rows, the shifted partition has two
endpoint squares. Each contains two endpoints and zero or one flank
selection, so its raw excess is -1 plus that selected count. Summed over
both flanks and all these bands, this is

    -(w-2)+ell_interior+q.

The upper end-row band contains the entire odd-length horizontal endpoint
path from the chamber through its tip. Its shifted full tiles are (p,t)=(2,1).
The single chamber-side cap has (p,t)=(1,1+a_u), where a_u indicates the
optional outer flank selection in row u. Thus the end-row raw sum is
-1/2+a_u. The lower end gives -1/2+a_v. These are the established local
source tables; summing them gives E'_K=1-w+ell+q.

To bound ell, each selected site of L already sees its chamber endpoint.
Two consecutive selected sites on L would each have a second occupied
neighbor, violating feasibility. Pair its w consecutive sites into w/2
adjacent pairs; each pair has at most one selection. Hence ell<=w/2.

The first and last sites of I cannot be selected. For (u+1,c+2), both
(u+1,c+1) in the chamber and (u,c+2) on the upper arm are endpoints.
The analogous two endpoint neighbors exclude (v-1,c+2). The remaining
w-4 sites of I likewise have no consecutive selections, because each
already sees its chamber endpoint. Pairing them gives q<=(w-4)/2.
Consequently ell+q<=w-2, proving Gamma_K>=2. QED.

This is stronger than separately summing nonnegative row-band gains.
For example, selecting an optional cap can exclude a flank selection in
the neighboring band. The complete even-length flank and the two arm-side
exclusions retain precisely the two units that the bandwise estimate loses.

The bound is sharp. Select every second site of L beginning in row u,
and every second site of I beginning in row u+2, stopping in row v-3.
Then ell=w/2, q=(w-4)/2 and Gamma_K=2. These sites are pairwise nonadjacent,
see exactly their own chamber endpoints, and are diagonal to the nearest
prescribed lateral/arm supports. With sufficient exterior clearance they
form a feasible retaining completion. Section 5 gives such clearances and
an explicit grid witness. Thus the constant is not justified only by a
finite optimization.

## 3. Arbitrary-direction enclosed-source cavity theorem

Use a root cavity with n fully enclosed prescribed positive sources in any
tile-preserving orientations. Every other endpoint in C belongs to a
prescribed complete straight comb, which may escape C. No partial foreign
source or other component shape is allowed. Let Phi_C be saturated-minus-
sparse physical singleton end membership of complete combs in C, as in
`CAVITY_BOUNDARY_FLUX_AND_COMPENSATION.md`.

For each perpendicular enclosed source define

    a_K=Gamma_K-2=w_K-2-ell_K-q_K>=0,
    A_C=sum_(perpendicular enclosed K)a_K.

Parallel enclosed sources have exact phase difference two, by the earlier
complete-source table. The root boundary and comb arguments are unchanged,
so the exact original-resource identity is

    D_C=2+2n+Phi_C+A_C+D'_C.                         (2)

Every term is counted in the same physical and shifted partitions. The
new A_C is slack in that identity, not an additional physical supply.
With complete-comb closure Phi_C=0, hence

    D_C>=2(n+1)                                     (3)

for arbitrary enclosed source directions. If one such cavity, or disjoint
such cavities, account for all B positive sources in the retained original
whole-receiver ledger, then

    |T|+|M|<=mn/2-B.                                (4)

This strict margin removes the entire matching loss from the universal
5/6 inequality on the stated class. It is not a universal coefficient
improvement and does not cover arbitrary positive bent receivers.

## 4. Cross-cavity capacity and signed flux

For a finite family of cavities put k_j=1+n_j, K=sum_j k_j,
Phi=sum_j Phi_j and A=sum_j A_j. If every positive physical no-endpoint
donor belongs to at most c cavities, c>=1, then

    2K+Phi+A <=sum_j D_Cj <=c D_all,
    cDelta >=2K+Phi+A-cB+cE,       E>=0.             (5)

This is the earlier original-donor incidence proof with the nonnegative
whole-source slack retained. Nothing is counted beyond c copies before
dividing by that incidence bound. Shifted squares and partial receiver
weights are not independently allocated. Actual source coverage K>=B and
Phi+A>=-B suffice for disjoint cavities. With multiplicity at most two,
Phi+A>=-1 suffices by integrality. The previous criteria using Phi alone
remain sufficient, now without an enclosed-source direction restriction.

Comb membership cancellation across cavities still depends only on the
two original physical singleton ends. It is unaffected by enclosed-source
orientation. Cavity existence, source coverage and the actual pointwise
incidence condition are still hypotheses, not inferred from (5).

For an initial-pair statement retain all initially prescribed frozen sources
and complete comb data on every cavity endpoint. Their labels and the flank
selections persist under the same normalization argument as before. Other
components cannot add endpoints or promote an exterior vertex into C.
The outside nonpositive-receiver coverage remains necessary for E>=0.

## 5. Explicit nonempty mixed families

An occupied-rung example works for every even root width W>=32 and root
depth H>=7. Place the root at chamber origin (2,3), with tip row y=2H+4.
Use vertical complete combs at columns 9 and 22 with endpoints rows 7,...,y,
outer supports at odd rows (columns 8 and 23), inner supports at even rows
(columns 10 and 21), and both axial supports. Their upper ends are saturated,
lower ends sparse. Use the explicit zero-mouth selection pattern of the
previous closed-cavity example, unchanged.

Replace that example's horizontal blocking comb by a rightward positive
source of width eight and depth one, chamber rows 7,...,14 and columns
14,15; its tips are (7,18),(14,18). It lies wholly in the root cavity and
occupies the negative comb pair's saturated band {6,7} x {10,...,21}.
The old parallel-only cavity hypothesis fails. Equation (2) applies.

For the sharp version add outer flank selections in column 13, rows
7,9,11,13, and inner flank selections in column 16, rows 9,11. Its phase
gain is exactly two. The original root mouth is still saturated on every
no-endpoint tile and total mouth flux is -2. The inner source's own mouth
has its usual separate physical ledger. No claim is made that every older
global certificate fails in this two-source example.

The closest inner-source chamber point is four rows below the root chamber;
its chamber/arm columns 14,...,18 are at least four endpoint steps from
the two comb paths. Its right axial supports at column 19 are separated
from the right comb's inner supports at column 21 by two columns. The new
outer flank selections see chamber endpoints only. The first inner flank
selection (9,16) is diagonal to the upper arm's inside support (8,17);
the other inner selection has greater clearance. All other nearest support
contacts are diagonal or farther. Since y>=18, the mouth pattern is at
least three rows below the inner source's lowest support. The root and
both combs retain their previous uniform feasibility argument. Therefore
all endpoints are complete, retain their actual matching/supports and are
frozen in every feasible retaining completion.

For arbitrarily many independently oriented enclosed sources, pack finite
source templates in successive disjoint 32-by-32 islands inside one tall
root. Widths 8,10,12 and depths one,two fit with all supports in an 18-by-18
even box. Any transpose or reflection in that box preserves the physical
tiling and bounds. Translating island i by (8+32i,8) leaves support margins
from the root chamber/arms and between islands. A root of width48 and depth
16a+12 contains a such islands for every a>=1. This supplies a general
mixed-direction family; optional sharp flank selections fit in the same
islands. The original donor incidence is still measured globally.

## 6. Verification and remaining scope

`develop/check_mixed_cavity_sources.py` checks the exact per-source raw
weights, both flank bounds, the full mixed-cavity identity, actual complete
components/freezing, the original receiver ledger and sharp examples. It
also checks arbitrary independent reflected/transposed island choices,
greedily filled completions and all eight global symmetries of the sharp
occupied-rung example. The finite checks test the written general proof.

`formal/SubQuorum/MixedCavitySources.lean` supplies scoped proofs of local
flank exclusion, a finite adjacent-pair budget, the sharp arithmetic phase
bound and the conditional mixed-cavity identity/consequence. Complete
source geometry, the grid adapters and the coordinate families remain
written proofs. No general cavity existence or full grid theorem is formalized.

The result resolves the fully contained perpendicular-source obstruction
left by the earlier cavity notes. Partial foreign sources, uncontrolled
signed comb exits, insufficient unique donor capacity, arbitrary positive
bent components and the unrestricted grid/triple equality remain open.

The subsequent `OPEN_SOURCE_CAVITY_COMPENSATION.md` removes the partial
contact restriction for prescribed long sources by aggregating their
nonnegative row-band phases. It also proves that two-unit credit for
each merely touching source is false with unbounded overclaim. General
positive bent components and sufficient global capacity remain open.
