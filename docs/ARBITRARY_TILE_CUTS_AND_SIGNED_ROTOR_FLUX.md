# Arbitrary tile cuts, physical terminal credits and signed rotor flux

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Purpose and hypotheses

The localized exterior theorem in `LOCALIZED_COMPLETE_EXTERIOR_BUDGET.md`
requires each added original to stay wholly inside one region when interpreting
the regional quantity as a source-addition marginal. Its general cut bound also
requires old negative rotor singletons to keep their positive mates inside the
cut. Here we give an exact accounting formula for ARBITRARY physical tile cuts,
including cuts through bent U originals and rotors. The formula records signed
boundary transfers explicitly; it does not assert nonnegative addition marginals.

Use the same finite immutable full-even-U/standard-rotor model, endpoint-disjoint
originals, charge normalization and potential Phi. Let O be any old inventory
and K=O union Y a complete inventory. Retain every original support outside the
final endpoint set with occupied degree exactly one. The old inventory may be
incomplete. Its beta weights retain ORIGINAL SUPPORT INCIDENCE MULTIPLICITY.
No contact graph, source-count, orientation, dimension or cut-shape restriction
is imposed. All source records and their original matching remain fixed.

Use the established exact identity, with beta extended by zero to empty tiles:

    Phi(H)=2P(H)+sum_tau beta_tau(H),
    beta_tau(H)=3n_tau/2-2e_tau-r_tau+2 I[n_tau=4].       (1)

Here P counts positive-charge ORIGINAL sources, and r is an incidence count
until H is complete. The complete tile table and injective negative-rotor to
positive-triple pairing are proved in the preceding note. We use those written
geometric facts; the new result is the finite accounting across arbitrary cuts.

## Physical credits from added positive U terminals

Every positive U original J has exactly two original terminal singleton tiles.
Each contains its terminal endpoint and two original intratile supports. These
two terminal occurrences remain distinguished by (J,terminal), even if later
activated or sharing a final tile with other endpoints. For every tile tau let

    t_tau = number of these terminal occurrences belonging to Y in tau.

Thus sum_tau t_tau=2P(Y). This is a physical allocation of half a unit to each
original terminal, not a new copy of the source's reserve.

Choose once, for each positive source in Y, an endpoint tile a(J) as its anchor.
Any fixed choice is allowed. For a tile set Q put p_Q=#{J in Y:q_J=1,a(J) in Q}
and B_Q=sum_Q beta_tau(O). Define the LOCAL ACCOUNTING INCREMENT

    L_Q=p_Q+sum_(tau in Q)[beta_tau(K)-beta_tau(O)+t_tau/2].  (2)

If a disjoint collection of cuts partitions all endpoint tiles of K, then

    sum_Q L_Q=Phi(K)-Phi(O).                             (3)

Indeed the anchor counts sum to P(Y), and the physical terminal credits sum to
P(Y), recovering exactly the 2P(Y) source term in (1). No source weight is copied
across regions. Individual L_Q may be half-integral.

When every added source has its entire endpoint footprint inside or outside Q,
and its anchor follows that footprint, t_Q=2p_Q and the tile identity/locality
give L_Q=Phi(O union Y_Q)-Phi(O). Otherwise L_Q is a regional accounting term,
NOT a marginal obtained by adding a subset of sources. This distinction is
essential when cuts pass through a source.

## The exact boundary formula

Let U_old be the tiles which are negative U singleton tiles in the COMPLETE K
and whose endpoint belongs to an OLD positive U original. Let R be the actual
negative rotor singleton tiles of K, and m:R->tiles their established injective
positive-triple mate map. The range m(R) is disjoint from U_old and R.

For Q let u_Q=|U_old intersect Q|. Define the directed rotor transfers

    out_Q=#{tau in R:tau in Q,m(tau) outside Q},
    in_Q =#{tau in R:tau outside Q,m(tau) in Q}.          (4)

The direction is from the negative singleton to its positive mate. Thus an
outgoing arc leaves a debit inside Q; an incoming arc brings a positive credit.

For each physical tile define

    z_tau=2 beta_tau(K)+t_tau
            +I[tau in U_old]+I[tau in R]-I[tau in m(R)]. (5)

**Nonnegative residual.** Every z_tau>=0. This follows exhaustively from the
complete tile table and the ownership rules:

- A negative NEW U tile has exactly one endpoint, that source's terminal. It
  has precisely one new terminal occurrence, so 2beta+t=-1+1=0.
- A negative OLD U tile has no new endpoint or new terminal occurrence; its
  old-U indicator cancels its -1.
- A negative rotor tile likewise has no new U terminal occurrence, and its
  rotor indicator cancels its -1.
- A rotor mate has beta=+1/2; mate injectivity subtracts exactly one unit from
  its doubled weight. Its remaining terminal credits, if any, are nonnegative.
- Every other tile has beta>=0 and receives only nonnegative terminal credits.

In particular the negative tile sets and mate range cannot use one physical
tile twice. Put Z_Q=sum_Q z_tau. Substitution into (2) gives the EXACT FORMULA

    2L_Q=2p_Q-2B_Q-u_Q+in_Q-out_Q+Z_Q,   Z_Q>=0.         (6)

To see the boundary sign, the rotor contribution is
|m(R) intersect Q|-|R intersect Q|. Every internal pair cancels, leaving
in_Q-out_Q. This identity allows both old and new rotor pairs to cross Q.

Let b_Q count old positive-U terminal tiles in Q which have exactly one OLD
endpoint and the two own intratile supports. These are the eligible old
terminal tiles of the preceding cut theorem. Every tile counted by u_Q belongs
to b_Q: endpoints only increase, and its two retained supports remain original
supports of that old terminal. Thus u_Q<=b_Q and

    2L_Q>=2p_Q-2B_Q-b_Q+in_Q-out_Q.                     (7)

This is the arbitrary-cut compensation inequality. No added-source containment
or old-rotor-mate containment assumption is needed. Boundary terms cannot be
dropped unless independently controlled.

## Conservation and the previous cut theorem

For any disjoint partition of physical endpoint tiles, every rotor arc is
either internal or crosses between exactly two parts. A crossing arc contributes
one outgoing unit in its source part and one incoming unit in its target part.
Consequently

    sum_Q in_Q=sum_Q out_Q.                             (8)

Each anchor contributes to exactly one p_Q; each terminal occurrence contributes
to exactly one t_tau; each old negative U tile contributes to exactly one u_Q;
and every physical residual z_tau is used once. Summing (6) is therefore a
conservation identity, not repeated access to a global reserve. It recovers

    2[Phi(K)-Phi(O)]=2P(Y)-2sum_tau beta_tau(O)
                       -|U_old|+sum_tau z_tau.          (9)

This global expression is a reformulation of the existing reserve argument,
not a stronger universal grid theorem. The added flexibility is that individual
cuts can now pass through added originals, and exported rotor debt stays visible.

Under the preceding theorem's stronger hypotheses, L_Q is the source-addition
marginal. New rotors then stay wholly inside or outside Q. The old-rotor mate
condition excludes outgoing negative old rotor arcs. Thus out_Q=0, while any
incoming arc is nonnegative. Dropping in_Q in (7) recovers exactly

    2[Phi(O union Y_Q)-Phi(O)]>=2P_Q-b_Q-2B_Q.

For the retained nested A/B core there are no old rotors, old terminal tiles
are already activated, and the sealed chamber/exterior cuts contain every new
source wholly. Both rotor fluxes and b_Q vanish. The old baselines -3 and -2
therefore recover Delta_i>=3+P_i and Delta_out>=2+P_out, respectively.

## Diagnostic examples and a rounding obstruction

First take O=K to be the complete zero-charge rotor used in the preceding note,
with its upper negative singleton in Q=[0,1]x[0,1] and its mate outside. There
are no additions: L_Q=p_Q=u_Q=Z_Q=0, B_Q=-1/2, out_Q=1, in_Q=0. Formula (6)
reads 0=1-1. The mate tile has B=+1/2 and one incoming unit, again giving zero.
The earlier false 0>=1 rule has been repaired by exactly the missing boundary
debit, with no hypothesis pretending that the mate is inside Q.

Second take O empty and K one positive U(6,4,4) in canonical phase. Choose an
anchor in its bar and Q containing only one terminal tile. Then p_Q=0,
beta_Q(K)=-1/2,t_Q=1, so L_Q=0. The source crosses the cut, but its terminal
debit is locally paid. The whole source still has Phi=1; its remaining base
unit is assigned once at its anchor. This demonstrates why L_Q should not be
described as a subset-addition marginal on an arbitrary cut.

There is also a complete obstruction to rounding regional credits separately.
Take O empty and K a single complete zero-charge rotor in a two-L phase. Its
four endpoint tiles have local accounting increments -1/2,-1/2,+1/2,+1/2.
Their exact sum is Phi(K)=0, whereas the sum of their individual ceilings is2.
The two rotor arcs connect the negative and positive halves. Consequently one
must conserve the signed half-unit terms before using integrality. Individual
L_Q are not integer source marginals when a source crosses the cut; rounding
each one upward would invent two units of reserve in this complete example.
This refutes that rounding rule, not the conservation formula or grid target.

## Relation to the open research problem

The formula supplies a uniform ledger for cuts through mixed-direction sources,
including bands which split a bent U or a rotor. It isolates exactly which
cross-region debit must be compensated, instead of requiring those cuts to be
closed under entire source footprints. A new geometric bound would still be
needed to eliminate the boundary debit on an individual band, or to pay all
marked-side demand in an arbitrary grid representative. The sharp exterior
minimum between2 and5, general source decomposition, unrestricted five-sixths
improvement and rectangular-grid triple equality remain open. The submitted
11October manuscript is unchanged.

## Validation and review scope

The checker `develop/check_arbitrary_tile_flux_cuts.py` passed736 complete
inventories and2104 old-inventory choices. It checked122572 cuts, including
94032 split-added-source occurrences,600 crossing-rotor arc occurrences,
58220 footprint-closed marginal identities and8028 half-integral local
increments. Partitions include row bands, column bands, checkerboards and
single physical tiles. Complete controls include original source images,
mixed-source fixtures, nested chambers, unequal walls and short-wall crossings.
Each partition checks the direct immutable potential and exact global sum;
these are finite controls of the written proof, not an arbitrary-size search
certificate for any open grid inequality.

The local Lean file `formal/SubQuorum/BoundaryFluxCuts.lean` passed13 theorems
and29 individual declaration audits on the user-selected local Mac using
Lean4.33.0, with no warnings, errors, sorry or native evaluation. It proves
the nonnegative role residual, signed-arc boundary identity, complementary-cut
flux conservation, finite regional sum and conditional compensated bounds.
Its axioms are at most propext and Quot.sound. Geometric source classification,
the source-to-tile adapters, rotor injection and correspondence of regions to
the physical records remain written/dependencies; this is not end-to-end Lean.

The earlier localized theorem has independent ACCEPTd8adad0c. That acceptance
does not include this later arbitrary-cut extension. Same-conversation audit
96e3f47c-6327-4f7b-a21d-7826061da91a is running on the conservation proof
and separate later width6 marked-slack corollary. The elementary separate-
rounding diagnostic was added after that audit input and is checked directly
and by kernel reduction. No ACCEPT is yet claimed for
these two extensions. Separately, research task8b95f828-f11e-4975-b7c3-6c958fa7b60c
is investigating whether the universal exterior bound can be sharpened to5;
it is a distinct research question, not a second review of this note.
