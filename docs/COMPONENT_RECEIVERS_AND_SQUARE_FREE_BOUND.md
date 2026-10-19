# Whole-component receivers and the coefficient-one square-free class

19 October 2026. Research note, separate from the submitted manuscript.
The statements below are general written proofs; finite controls and scoped
Lean statements are auxiliary. No universal grid triple equality is claimed.

## 1. Configuration, tiling and the original charge

Let (T,M) be feasible on an even-by-even rectangular grid with mn vertices.
Put P=V(M), A=T union P. Every vertex of T has at most one neighbor in A.
Use the fixed disjoint 2-by-2 tiling. A configuration is single-terminal
when every P has at least three neighbors in A. Extend labels outside the
physical rectangle by blank. Endpoint components are components of the
graph induced by P, not of the residual tile graph.

For a tile let t,p,b count T,P,B; h counts internal matching edges.
It is saturated when t=2 and deficient otherwise. For a deficient tile,
s counts its endpoints matched to saturated tiles, d counts matching
incidences to other deficient tiles, and r=2-t-h-s. The original charge is

    rho(Q)=d/2-r=t+p/2-2+s/2   on deficient tiles,
    rho(Q)=0                   on saturated tiles.

Charges on regions always sum these original physical tile charges.
Saturated tiles have at most one P, no internal matching edge and no
matching edge to another saturated tile, by GRID_ABSORPTION_PROOF.md,
Lemma A.1. Thus each saturated P transfers its raw half-unit to its
deficient mate tile, giving the exact global identity

    rho(grid)=|T|+|M|-mn/2.                                  (1)

## 2. A terminal tile has only one endpoint-component owner

**Tile-ownership lemma.** In a feasible single-terminal configuration,
the P vertices in any unit square, aligned or not, induce a connected
graph whenever that set is nonempty. Consequently a tile cannot contain
endpoints from two distinct endpoint components.

Proof. A subset of the four-cycle is disconnected only when it consists
of the two opposite corners. Suppose two opposite corners are P and no
other corner is P. Each remaining corner has two P neighbors, so neither
can be T. Both are blank. Either P corner then has two blank neighbors
inside the square and at most two occupied neighbors outside it. This
contradicts occupied degree at least three. Every other nonempty subset
of a four-cycle is connected. QED.

For each endpoint component H, define R_H as exactly the aligned tiles
containing at least one endpoint of H. The R_H are pairwise disjoint.
Their complement Z consists of tiles with no P. This is a partition of
physical tiles; a selected vertex in a shared contact tile with no P
does not make that tile belong to either receiver.

**Closed-receiver ledger.** For every H in a single-terminal configuration,

    rho(R_H)=|T intersection V(R_H)|+|H|/2-2|R_H|.           (2)

Proof. Every P in R_H belongs to H by tile ownership. Every actual matching
edge incident to H stays in H, so all mates of its endpoints lie in R_H.
The saturated-to-deficient matching edges therefore have both tile ends
in R_H. The sum of s over deficient receiver tiles is precisely the number
of saturated receiver tiles containing P. The raw excess of those saturated
tiles is one half each. Adding the deficient corrections s/2 exactly restores
the sum of raw excesses over all receiver tiles, proving (2). There is no
uncounted saturated export, incoming attachment or crossing matching edge.

In particular, (1) decomposes exactly as

    |T|+|M|-mn/2 = sum_H rho(R_H) - sum_(Q in Z)(2-t_Q).    (3)

The final sum is nonnegative because every tile has t<=2. This decomposition
is valid for arbitrary terminal component shapes, even when some receivers
have positive charge. It does not assert each arbitrary receiver is nonpositive.

## 3. Every straight-comb receiver has charge zero in all alignments

Suppose H is a straight horizontal path of 2r endpoints, r>=1, in a
single-terminal configuration. The straight-comb argument of
SQUARE_FREE_ENDPOINTS_AND_OWNED_DONORS.md applies to this component alone:
its matching is the unique consecutive pairing; every inner endpoint has
one perpendicular T, the end vertices also have axial T, and perpendicular
supports alternate sides. The argument needs only that H is a straight
complete component; other components can contain squares.

All labels in R_H are forced by these supports and component completeness.
To see this, a perpendicular site next to H cannot be P outside H. Exactly
one of the two perpendicular sites at each endpoint is T. An unselected
site on either side along the segment is adjacent to a selected support
at the preceding or following column, since the segment has even positive
length and the supports alternate. That support already has its endpoint
neighbor, so this other site is blank. At a partial end tile the site
perpendicular to the axial T is blank for the same feasibility reason.

Let b be the column of the first endpoint, and take either choice of which
neighboring row is paired with H by the fixed tiling.

If b is even, R_H has r tiles. Each has two P and one T. Hence

    |R_H|=r,      T_R=r,      P_R=2r.

If b is odd, R_H has r+1 tiles. Its r-1 middle tiles each have two P and
one T. The two end tiles have respectively (t,p,b)=(2,1,1) and (1,1,2):
the two endpoint perpendicular supports are on opposite sides. Thus

    |R_H|=r+1,    T_R=r+2,    P_R=2r.

In both cases (2) gives rho(R_H)=0. Rotation gives the same statement for
vertical combs. These counts hold in arbitrary feasible exteriors retaining
the complete component, not just an isolated drawing with every other site blank.

The misaligned case illustrates why the saturated correction matters.
One end tile is saturated and has original charge zero, although its raw
physical excess is +1/2. The half-unit moves to the deficient tile containing
its endpoint's actual mate. That tile need not be the opposite end tile.
Only the whole receiver is assigned zero; its individual deficient tiles
need not all be nonpositive. No end contribution is reused.

## 4. A complete coefficient-one theorem

**Square-free endpoint theorem.** If the graph induced by the matching
endpoints contains no all-P unit square, then

    |T|+|M| <= mn/2.                                       (4)

No single-terminality, matching-direction, component-disjoint-collar or
tile-alignment assumption is imposed on the initial pair.

Proof. If an endpoint has at most two occupied neighbors, promote it and
remove its matching mate. The promoted endpoint then has at most one occupied
neighbor. The occupied set shrinks, so every original T remains feasible;
the objective |T|+|M| is unchanged. Each move deletes one matching edge,
so at most the original |M| such moves are possible. No P is added, hence
no P-square can be created. At termination all endpoints have occupied
degree at least three. By the local turn/branch lemmas and straight-comb
theorem, every remaining endpoint component is a straight even comb.
Its receiver has charge zero by Section 3. Tile ownership makes all these
receivers disjoint, independently of horizontal or vertical orientation.
Every other tile has no P and charge t-2<=0. Equation (3) now proves (4)
for the terminal pair, and objective preservation proves it for the initial
pair. QED.

For any such terminal representative the exact deficit is

    mn/2-|T|-|M| = sum_(Q in Z)(2-t_Q).                     (5)

Equality holds precisely when every no-P tile is saturated; this includes
the case Z is empty. Different possible normalization sequences need not
produce the same components, but (5) holds for each resulting terminal
representative. In particular, (4) covers every endpoint forest, while the
geometric no-P-square hypothesis can allow endpoint cycles initially.

Relative to the established universal |T|+(5/6)|M|<=mn/2, this removes the
entire |M|/6 loss on the stated square-free class. It is a conditional
improvement in coefficient, not a new universal bound.

## 5. Pure rectangular components and mixed capped receivers

The pure-component reduction in PURE_TWO_ROW_COMPONENT_REDUCTION.md removes
all squares from a complete full 2-by-w endpoint component using its actual
matching and arbitrary feasible exterior, leaving at most one matching edge.
It preserves the objective and adds no P. Distinct such component reductions
compose, and may be rotated. Consequently (4) also holds if each initial
endpoint component is either square-free or a full two-row/two-column rectangle.
The complete-rectangle hypothesis cannot be replaced by arbitrary two-row
support; the capped obstruction is an explicit counterexample to that step.

There is also a useful strict version permitting that obstruction. Suppose
each initial endpoint component is one of:

- a square-free component;
- a full two-row/two-column rectangle;
- one of L prescribed capped components of FROZEN_TWO_ROW_CAPPED_LADDERS.md,
  with its matching and six supports, in any of the stated tile-preserving
  positions and symmetries.

Then

    |T|+|M| <= mn/2-L.                                     (6)

First reduce the pure rectangles, then perform singles on every remaining
component that admits them. None of these operations changes any prescribed
capped component or its six supports: its endpoints are universally frozen,
other components never add endpoints, and the original T is preserved.
Every other final component is a square-free straight comb. The complete
terminal endpoint receivers are disjoint by Section 2. Each comb contributes
zero and each capped receiver contributes exactly -1 by its proved original
ledger. Every no-P tile contributes t-2. Thus in fact

    mn/2-|T|-|M| = L + sum_(Q in Z)(2-t_Q).                 (7)

This is a whole-component counting theorem with no source-assignment
hypothesis. It covers different component orientations and the given capped
receivers together. It does not allocate the same capped -1 once per square,
nor does it cover all arbitrary square-bearing or branched components.
Those general receivers and their positive-source coverage remain open.

## 6. Verification and review scope

The physical controls check all 6,561 local label/exterior-occupancy models,
including 625 satisfying local feasibility and terminality. All 220 nonempty
endpoint models induce a connected subgraph in the tile. They also check
64 comb lengths in all four alignment phases, 256 cases and 2,048 symmetry
images, including the exact saturated-to-deficient transfer count and forced
blank labels. Complete enumeration covers 24,296 feasible configurations on
2-by-2, 2-by-4, 2-by-6 and 3-by-4 source grids; the last shape is embedded
with a blank fourth row for its even-rectangle ledger. Of these, 17,925 have
no P-square and are checked through objective-preserving single normalization.
A separate 18-by-22 fixture combines horizontal combs, vertical combs, a
pure rectangle requiring a bundle and one frozen capped component; it checks
the exact strict-deficit identity, all ownership and transfer counts.

The local sequential Lean 4.33.0 audit passes 65 declarations. Four new
statements in formal/SubQuorum/ComponentReceivers.lean prove the physical
integer-coordinate diagonal bridge, endpoint-owner equality under ownership
of adjacent endpoints, and the two conditional comb count identities.
No sorry or nonstandard reduction axiom is used. The complete component
partition, saturated-transfer cardinality, all-length comb geometry and
normalization-to-bound argument retain the general written proofs above.
The receipt is output/component-receiver-formal-check.json. The task-owned
build was removed after preserving the source-matching receipt and confirming
no real lean or lake executable remained active.

```sh
python3 develop/check_component_receivers.py --output output/component-receiver-controls.json
```

An independent written-proof review has been submitted through the Oracle
broker. It includes the earlier turn/branch/comb and pure-rectangle proofs;
no verdict is inferred while the original stream remains live.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
