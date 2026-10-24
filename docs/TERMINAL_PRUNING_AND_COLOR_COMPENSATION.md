# Terminal-free pruning, leaves of one color, and export mismatch

7 October 2026. An external review of [terminal strands](TERMINAL_STRAND_ACCOUNTING.md)
confirmed the local table, exact shortage identity and neutrality consequences.
It prompted the boundary clarification and extensions proved below. The
proofs and controls here independently check those suggestions; a review
response is not used as a proof certificate.

## 1. Prune cycles while preserving all open strands and reserves

Fix any deficient tile region D and a maximum adjacent auxiliary pairing
in every tile. Cancel every cycle component of its physical strand graph,
using the preceding alternating-circuit theorem. These components have
disjoint physical endpoint vertices, so their replacements can be simultaneous.
Open strands and all matching edges crossing the region boundary stay fixed.

If z_Q auxiliary pairs are removed in tile Q, its residual data become

    r'_Q=r_Q-z_Q, d'_Q=d_Q-2z_Q, H'_Q=H_Q.

No S endpoint belongs to a canceled cycle. Hence u'_Q=u_Q and c'_Q=c_Q.
The uncanceled auxiliary pairs remain maximum for the remaining residual
endpoint set: the local table only permits r=2,d=4 becoming r=1,d=2 adjacent
or r=0,d=0; r=2,d=3 becoming r=1,d=1; r=2,d=2 adjacent becoming r=1,d=0;
and r=1,d=2 becoming r=0,d=0. These exhaust changed tiles. A tile reaching
capacity zero has degree zero and cannot acquire a positive leaf.

Thus T, all occupied vertices, objective, each tile charge, saturated mates,
every boundary matching edge, all six open-strand counts, p,a,u,H and c
are preserved. Every remaining residual matching edge lies on an open
L/S/P strand in this inherited decomposition. Another choice of auxiliary
pairs may exhibit further cycles; auxiliary irreducibility is not asserted.

**Theorem 1 (terminal-free pruning).** If p=a=u=0, every residual edge
meeting D is removable. After the simultaneous replacement,

    d'_Q=0, r'_Q=c_Q, rho(D)=-c.

**Proof.** Without terminals every physical strand component is a cycle.
Every residual endpoint is paired, so z_Q=d_Q/2 and
r'_Q=r_Q-d_Q/2=H_Q/2=c_Q. QED.

Tilewise neutrality is unnecessary. Closed neutral-region pruning is the
special case c=0. Negative terminal-free circuits are converted into isolated
reserves while preserving their entire negative budget. This removes closed
capacity-two circuitry from the residual graph without inventing compensation.

For example, choose no T on a 4-by-4 grid and match

    (1,1)--(1,2), (1,3)--(2,3),
    (2,2)--(2,1), (2,0)--(1,0).

The four tiles form a cycle; each has capacity two, adjacent residual
endpoints, u_Q=0 and c_Q=1. Its charge is -4. Replacing the cycle by its
four internal pairs leaves each tile with r'=1,d'=0, retaining all four
reserve units and every occupied vertex. This is a physical feasible control,
not a claim that an irreducible diagonal cycle can be pruned.

## 2. Leaves or ports of one color have an injective compensator

Let the fixed regional incidence graph contain the deficient tiles of D,
the residual matching edges meeting D, and one degree-one terminal for each
outside end of a boundary residual edge. Distinct outside ends remain
distinct: do not join them through tiles outside D. An isolated tile with no
residual endpoint is harmless and contributes only its reserve. Write X for
the L and P terminals together, using the physical checkerboard coloring.

**Theorem 2 (one-color terminal compensation).** Suppose that, in each
connected regional incidence component, every X terminal has the same
physical checkerboard color. Different components may choose different
colors; components without X terminals satisfy the condition vacuously.
Then every X terminal lies on an XS strand and has a distinct S compensator.
In particular,

    n_LL=n_LP=n_PP=0, epsilon(D)=-n_SS-c<=0.

**Proof.** An open strand cannot leave its incidence component, and every
strand has opposite-color ends. An XX strand would contradict the assumed
one-color condition. Thus the other end of each X strand is S. Physical
strand components are endpoint-disjoint, so different X terminals receive
different S endpoints. Each S uses one distinct unused-slot token. Apply
the exact shortage identity. QED.

Take D to be all deficient tiles in the rectangle, so p=0. If each residual
component's active zero-capacity leaves have one color, Theorem 2 gives

    |T|+|M| <= |V|/2.

This is an arbitrary-size sufficient class for coefficient one, including
bends, capacity-two branching, repeated tile visits, cycles, occupied
neighboring bands and saturated attachments. No strip theorem or assumed
Hall condition is used. Components with leaves of both colors remain outside
this criterion, even when their total charge is nonpositive. The theorem
does not prove the unrestricted grid conjecture or improve the universal
5/6 bound.

For exterior receivers, apply the regional theorem componentwise with
X=L union P. Combine its single-use allocation with the complete previous
source-patch hypotheses and the retained tau/remainder terms. That source
application still uses the earlier local geometric lemma; do not transfer
its hypotheses to arbitrary source regions.

## 3. Account for export mismatch before substituting strands

Let A_i be pairwise tile-disjoint source patches for which the previously
proved local inequality rho(A_i)<=beta_i/2+tau_i holds. Partition all
remaining deficient tiles into pairwise disjoint regions D_j and W_0.
Write p_j for every actual residual edge leaving D_j, including edges into
another D, an A patch, or W_0; degrees and ports use the same conventions.
No assumption equates beta exports with these ports. Then exactly

    q <= sum_i tau_i + sum_j epsilon(D_j) + rho(W_0)
         +(sum_i beta_i-sum_j p_j)/2.                   (1)

**Proof.** Sum the local patch bounds and charges of the tile partition.
For each D_j substitute rho(D_j)=epsilon(D_j)-p_j/2. QED.

Under the full earlier exterior-component incidence hypotheses,
sum beta_i=sum p_j and the mismatch term vanishes. Tile-disjointness alone
does not guarantee this. An inter-patch residual edge counted at both lower
exports contributes two to sum beta and none to exterior ports, giving its
one-unit correction. An unmarked residual crossing, or an edge between two
chosen receiver regions, also alters the difference and must stay in (1).
The original source-patch assumptions are now stated explicitly in the
terminal-strand note so its simpler formula has an auditable domain.

The mismatch is a signed algebraic correction, not an additional donor.
Reserves or strands from overlapping regions cannot be added as independent
resources. Single-use ownership is certified only within one fixed disjoint
accounting partition and its chosen physical strand decomposition.

## 4. Existing distant-donor obstruction and validation scope

The review rederived the existing nested neutral-band equality family at
width k=2d and depth d. It has one LL strand in tile row zero, one SS strand
in tile row d, no reserves and q=0. The two components are distance d apart,
and all local pairing choices are forced. Thus no fixed-radius direct charge
rule can pay the LL from initial nearby negative budgets. This is already
proved in [compensation transport](COMPENSATION_TRANSPORT.md); the rederivation
is a check and sharper strand description, not a new priority claim.

The response supplied |T|=2+2d(d+1), |M|=2(d+1)(d+2)-2 on a
(2d+2)-by-(4d+4) grid. Their sum is |V|/2. The coordinate constructor and
strand controls are checked for depths 1..40 against the existing family.
The all-depth conclusion uses the prior written proof, not the finite range.

Run `python3 develop/check_terminal_pruning_and_colors.py --output output/terminal-pruning-color-controls.json`.
The checker verifies inherited open strands after cycle pruning, independent
color-based injections for regional incidence components, the negative
terminal-free four-tile fixture, and the distant-donor formulas. Remaining
mixed-color geometry, directed relay reachability/packing and saturated or
inter-patch compensation are open. The manuscript is preserved; no new
Lean formalization or arbitrary-width strip theorem is claimed.
