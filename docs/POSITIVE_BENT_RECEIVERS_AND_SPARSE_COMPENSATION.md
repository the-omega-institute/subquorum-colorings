# Positive bent receivers and a sparse-tile compensation lemma

19 October 2026. This gives an explicit all-width obstacle to extending
the thin-component proof by declaring every terminal component receiver
nonpositive. It also proves a local compensation inequality in arbitrary
feasible exteriors. It does not refute the grid coefficient-one target.
Submitted manuscripts are unchanged.

## 1. An all-width fully frozen bent component

For even w>=4, let

    H=({0,1} x {0,...,w-1}) union {(2,0),(2,w-1)}.

The two pendant endpoints bend downward from the lower corners. The component
has height three and width w and contains w-1 all-P squares. Take the matching

- (0,j)--(0,j+1) for even j=0,2,...,w-2;
- (1,j)--(1,j+1) for odd j=1,3,...,w-3;
- (1,0)--(2,0) and (1,w-1)--(2,w-1).

The six selected supports are

    T={(0,-1),(0,w),(2,-1),(2,w),(3,0),(3,w-1)}.

Every support has exactly its intended P neighbor and no selected neighbor;
w>=4 ensures the two lower axial supports are not adjacent. Every endpoint
has occupied degree three. All remaining sites are blank in the baseline.
The counts are |H|=2w+2, |M|=w+1, |T|=6 and objective w+7.

Let m be the actual matching involution and define the even-color wave

    z_0=(2,0),
    z_j=(0,j-1) for odd j, (1,j-1) for even j, 1<=j<=w.

The tail z_0 freezes using (2,-1),(3,0). Vertex z_1=(0,0) freezes using
(0,-1) and retained m(z_0)=(1,0). For every 0<=j<=w-2, z_(j+2) has the
two distinct neighbors m(z_j),m(z_(j+1)). At j=0 these are (1,0),(0,1);
thereafter one incidence is horizontal and the other vertical along the
displayed staggered matching. Induction freezes the whole wave. Reflection
(r,c) -> (r,w-1-c) preserves the matching and six supports and exchanges colors
because w is even. It gives the disjoint odd-color wave. The two waves
exhaust H, so no nonempty mixed promotion bundle can use any edge of H.
The certificate persists in arbitrary feasible exterior completions preserving
H, its matching and the six supports.

## 2. A complete component can have strictly positive receiver charge

Translate the core origin to even row and odd column in the fixed 2-by-2
tiling. The endpoint receiver R_H consists of w/2-1 full-P central tiles,
two upper end tiles with one T and two P, and two lower tail tiles with
two T and one P. These receiver labels are forced in arbitrary feasible
exteriors: the sole extra corner of a lower tail tile neighbors its selected
supports, and the missing upper-end corner neighbors a selected support.

Therefore

    |R_H|=w/2+3, T_R=6, P_R=2w+2,
    rho(R_H)=6+(w+1)-2(w/2+3)=1.                         (1)

Equation (1) is the original closed-receiver charge, including saturated
corrections. Each lower tail tile is saturated, with raw excess 1/2 but
original charge zero. Its matching mate lies in the upper end tile, whose
raw charge is zero and original saturated-transfer correction is 1/2.
Thus the two upper end tiles contribute the positive unit. Dropping the
corrections would incorrectly erase the obstruction.

This refutes the general rule that every complete bundle-terminal component
has nonpositive receiver charge. The component is outside the proved
thin-or-one-square class: it has height three, width at least four and
at least three P-squares. The baseline embeds after translation (2,3) in
an 8-by-(w+8) grid. Its objective w+7 is well below half that area. The
global coefficient-one inequality is not refuted.

## 3. A canonical sparse tile pays the positive unit locally

In these normalized coordinates the physical tile

    D={(2,1),(2,2),(3,1),(3,2)}

is aligned with the fixed tiling and disjoint from R_H. This definition also
works at w=4. Let the complete H, actual matching and displayed supports be
retained in any feasible exterior completion.

**Sparse compensation lemma.** The original tile charge satisfies

    rho(D)<=-1, hence rho(R_H)+rho(D)<=0.                 (2)

Proof. The site (2,1) touches the two endpoints (2,0),(1,1), so cannot be
selected; it cannot be P without joining H. Thus it is blank. The selected
support (3,0), already adjacent to (2,0), forces (3,1) blank. The site (2,2)
cannot be P because it neighbors (1,2) in the complete H. If it is selected,
it already sees (1,2), so (3,2) must be blank. If it is blank, only (3,2)
can be occupied. Hence D contains at most one occupied vertex.

In the original ledger, write t,p for its selected and endpoint counts and
s for its endpoints whose matching mates are in saturated tiles. We have
t+p<=1 and 0<=s<=p. The tile is deficient, so

    rho(D)=t+p/2-2+s/2 <= t+p-2 <= -1.

This retains all matching-transfer corrections and holds even when D contains
an endpoint from another component. Together with (1), it proves (2). QED.

For w=4 all four D vertices are forced blank: the two right-side arguments
also apply, so rho(D)=-2. For every even w>=6, the general bound -1 is sharp:
add only the selected vertex (3,2) to the blank baseline. It has no occupied
neighbor, is not adjacent to any of the six supports, and gives t=1,p=s=0
in D. The receiver is unchanged. Thus local compensation can be exactly tight.

## 4. Terminality makes the donor a no-P tile

The donor tile D need not be a no-P tile in an arbitrary feasible completion.
For example, for w>=6 add matching edge (3,2)--(4,2) to the baseline. It is
disjoint and not adjacent to H; the pair remains feasible. Then D belongs to
another endpoint component and has t=0,p=1,s=0, original charge -3/2.
This example is not terminal in its added component. It establishes why a
local arbitrary-exterior argument cannot assume D lies in the no-P complement
before normalization. The following stronger conclusion holds at a global
single-terminal representative.

**Terminal no-P lemma.** If every endpoint in the entire configuration is
single-terminal, D contains no endpoint, so its original charge is t_D-2
with t_D<=1.

Proof. Section 3 shows that the only possible endpoint in D is (3,2).
If it were P, then (2,2), already forbidden to be P by completeness of H,
could not be T either: it would touch both (1,2) and (3,2). Thus (2,2) is
blank. Its other neighbor (3,1) is already blank, so (3,2) has at most two
occupied neighbors. This contradicts single terminality. QED.

Consequently canonical donors at the final representative are disjoint
from every endpoint-component receiver, not just their own source receiver.

## 5. Distinct bent sources cannot claim the same donor

Each prescribed bent source chooses one normalized left donor, with arbitrary
tile-preserving symmetries and translations. If its two possible descriptions
give different left/right donors, choose either one once. No component makes
two claims. The following local argument works for every even w>=4.

Put a purported shared donor at {(0,0),(0,1),(1,0),(1,1)} and orient the first
source as above. Its forced endpoint footprint contains

    E=({-2,-1} x {-1,0,1,2}) union {(0,-1)},

and its forced supports contain (-2,-2),(0,-2),(1,-1). These are the first
four chamber columns, its near tail and three near supports. They occur at
all widths. A second source claiming that same physical tile has one of the
eight orientations of this footprint. Let

    F(r,c)=(c,1-r), J(r,c)=(r,1-c).

Every relative orientation is F^j J^e for e in {0,1}, j in {0,1,2,3}.
The six cases j=0,1,3 have a shared endpoint in the two footprints:

| e | j=0 | j=1 | j=3 |
| --- | --- | --- | --- |
| 0 | (-2,-1) | (-1,1) | (-1,-1) |
| 1 | (-2,-1) | (-1,2) | (-1,-1) |

Such endpoints would belong to both complete components, so the sources
cannot be distinct. For e=0,j=2, the second source requires T at (0,2),
which touches distinct endpoints (-1,2) of the first source and (1,2) of
the second. For e=1,j=2, the first source's T at (1,-1) touches its endpoint
(0,-1) and the second source's endpoint (2,-1). Both violate feasibility.
These eight explicit constant-coordinate witnesses exhaust the relative
orientations of a fixed tile. They do not depend on a width search.

**Donor injectivity lemma.** Canonical donors of distinct prescribed bent
components are distinct, for arbitrary widths and all tile-preserving
orientations. At a global single-terminal representative they belong to
the no-P complement and each contributes at least one deficit unit.

## 6. A compensation theorem without repeated resources

**Mixed-class compensation theorem.** On an even-by-even rectangular grid,
suppose every initial complete endpoint component is either thin, has at
most one P-square, or is a prescribed bent component of Sections 1--2 with
its actual staggered matching and six forced T supports. The prescribed
bent components can have arbitrary even widths and tile-preserving symmetries
of the positive alignment. Then

    |T|+|M|<=mn/2.

If B_4 of those prescribed bent components have width four, the stronger
bound |T|+|M|<=mn/2-B_4 holds.

Proof. The freezing certificates make every prescribed bent edge immune to
all feasible global bundles, even before the other components are terminal.
The six selected supports stay selected. Normalize the remaining configuration
by the complete bipartite bundle procedure. Endpoints only disappear, so each
other final component is thin or has at most one P-square. Its receiver is
nonpositive by THIN_COMPONENT_CLASSIFICATION_AND_BOUND.md. Each prescribed
bent receiver has original charge exactly one and remains complete.

Let B be the set of prescribed bent sources, let D_B be their chosen canonical
donors, and let Z be all no-P tiles of this final pair. Terminal no-P and donor
injectivity show that D_B is a set of |B| distinct members of Z, all disjoint
from every receiver. Summing the exact original ledger and pairing each
positive unit with its one donor gives

    mn/2-|T|-|M|
      = sum_(H not in B) (-rho(R_H))
        + sum_(D in D_B) (1-t_D)
        + sum_(Q in Z minus D_B) (2-t_Q).                 (3)

Every term is nonnegative. Each physical tile is present once and every
saturated transfer closes in its actual component receiver. No donor is
also spent as part of another receiver or twice in the donor sum. For width
four the two opposite-side forcing arguments make its donor entirely blank,
so its term 1-t_D is one. Distinctness retains all B_4 units. Objective
preservation proves both conclusions for the initial pair. QED.

This removes the original five-sixths matching loss on a class with genuinely
positive complete receivers and genuine three-row mixed-direction components.
It extends the thin-or-one-square theorem by an explicit all-width bent family.
Arbitrary bent shapes, other possible positive receivers, and complete source
coverage for the universal grid bound remain open.

## 7. Verification and review scope

The exact 3-by-4 discovery census gives 4,563 single-terminal local
configurations outside the thin-or-one-square class, of which 111 are fully
frozen, with 444 alignment checks. Its maximum observed complete-receiver
charge is one, attained by the w=4 member above. This finite maximum is not
claimed for larger components. The all-width construction, freezing waves,
positive charge and local compensation are proved independently above.

```sh
python3 develop/check_bent_component_discovery.py --columns 4 --output output/bent-component-discovery-3x4.json
python3 develop/check_bent_cap_compensation.py --output output/bent-cap-compensation-controls.json
```

Controls check 31 even widths, 91 baseline/exterior variants and all eight
constant donor-orientation witnesses. A mixed fixture places eight rotated
positive bent sources alongside the earlier thin/one-square fixture, performs
normalization, and checks their distinct no-P donors and exact equation (3).
The nonterminal extra-P example normalizes to a no-P donor as predicted.

The bent-family theorem is outside the Oracle review of the thin-component
note. The first bent review input covers Sections 1--3 and the original
arbitrary-exterior warning. The later terminal no-P, donor-injectivity and
mixed-class theorem in Sections 4--6 require their own subsequent review;
they are not silently covered by an earlier verdict. Formal scope and exact
review receipts are recorded separately. No universal grid theorem, external
priority or full Lean formalization is claimed here.

The final local combined Lean audit passes 73 declarations, with eight new
scoped statements across the thin and bent developments. The physical sparse
tile and terminal exclusion of its possible external endpoint are kernel checked.
The footprint check covers the six intersection cases; the two half-turn
infeasibilities and full component-to-coordinate adapters retain written proofs.
The local payment review is task 9a6895af-214a-4439-b79a-9c1e03f9a909,
conversation conv_65f1d5aa3e20f514, original stream 38980. The separate full
injective-payment review is task 4a9d8625-be7a-4eb0-a47b-c6ccde5112ea,
conversation conv_b6e03602f9701743, original stream 62345. Both pending handles
are preserved without inferring acceptance. These reviews do not execute Lean
or code and do not establish priority.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
