# Paying internal attachments with distinct forced blanks

19 October 2026. This supplies a geometric payment mechanism for nonzero
internal saturated-attachment debt in the attachment-corrected collar theorem.
It also gives an exact obstruction to assigning a blank separately for every
apparently available witness. All-size proofs precede finite controls.

## 1. Reserve selected and cap blanks before paying attachments

Fix a feasible pair and a tile region R with L distinct marked BB-cap tiles
satisfying the earlier two perpendicular pressure conditions. Write D,k,sigma
as in `ATTACHMENT_CORRECTED_COLLAR_COMPENSATION.md`, so

    2rho(R)=-D+k+sigma,       D>=2L.

Reserve one internal blank neighbor of the T in every deficient tile with
t=1. Such a neighbor exists by feasibility. In a marked tile with t=1,
reserve the other noncap corner: the pressure condition forces it blank.
Reserve the two cap blanks in every marked tile as well. These reservations
are disjoint. Let F be all remaining blanks in deficient tiles of R. Then

    |F|=D-2L.                                             (1)

Any such choice of the noncap T reservations is permitted. A reservation
policy is part of a certificate, and is fixed before assigning debt witnesses.
Saturated-tile blanks are excluded from F.

Let A be the saturated tiles whose unique matching endpoint is matched to
a deficient tile inside R. Each internal attachment has one distinct such
tile, and every such tile has just one endpoint. Hence |A|=k.

## 2. Geometric witness multiplicity

Every S in A has diagonal selected corners and one P corner. Each selected
corner already has that P as an occupied internal neighbor. Every actual
external neighbor of either selected corner is therefore blank. Each of
the four faces of S contains exactly one selected corner, giving up to four
distinct external forced blanks, subject to the ambient boundary.

Join S to each of these blanks that belongs to F. This defines the witness
bipartite graph between A and F. **Every F vertex has at most two owners.**
Indeed it lies at a corner of its own deficient tile. Two of its four grid
neighbors are inside that tile, and only the other two can be selected
corners in saturated tiles. Those two external neighbors lie in different
tiles. Multiple orientation descriptions never create another edge.

**Two-witness compensation theorem.** If every S in A has at least two
neighbors in F, then there is an injection assigning one adjacent free blank
to every internal attachment. Consequently D>=2L+k and

    2rho(R)<=-2L+sigma.                                  (2)

Proof. For any subset X of A there are at least 2|X| witness incidences,
while every neighboring blank receives at most two, so |N(X)|>=|X|.
For completeness, take a maximum matching in the finite witness graph.
If an attachment is unmatched, follow alternating paths from it. Write X
for reachable left vertices. All their neighboring blanks must be matched,
else an augmenting path increases the matching. Their matched left partners
belong to X excluding its initially unmatched root. Thus |N(X)|<=|X|-1,
contradicting the incidence count. The matching covers A. Every assigned
blank is a distinct member of F, proving (2) using (1) and the exact ledger.
This derives the required allocation condition from grid geometry; no Hall
inequality is assumed as an extra premise. QED.

For disjoint source regions of total charge at most L, sigma=0 now pays
them even with arbitrarily many internal attachments. If the boundary
parity is retained, D>=2L+k improves (2) to

    2rho(R)<=-2L+sigma-((j+eta) mod2),                    (3)

because D has parity j+Q and Q=k+eta. The proof does not allocate one budget
per residual passage through a capacity-two tile.

## 3. Exact component criterion, including one-witness attachments

The two-witness condition is sufficient and can be weakened completely.
Replace every blank of witness degree two by an edge between its two owners;
keep parallel edges when two distinct blanks have the same owner pair.
Call the resulting multigraph H on A the shared-blank graph. A degree-one
blank is a private blank at its unique owner. Degree-zero free blanks remain
unused by this witness incidence.

Let v=k, e be the shared edges, p the private blanks, u the unused free
blanks, c the connected components of H including isolated vertices, and
mu=e-v+c its total cycle rank. For v=0 set c=mu=0. Exactly

    |F|=e+p+u,
    k-|F|=c-mu-p-u,
    2rho(R)=-2L+sigma+c-mu-p-u.                          (4)

These identities retain the signed balances of all components and every
unused free blank. Parallel edges each consume one actual blank and count
in mu. They must not be collapsed into a simple edge.

**Allocation theorem.** A component of H admits distinct adjacent blanks
for all its attachment vertices if and only if it has a cycle or a private
blank. A tree with no private blank leaves exactly one attachment unmatched.

Proof. If a private blank exists, choose a spanning tree rooted at its owner.
Assign that blank to the root and each other vertex the blank of its parent
edge. If there is a cycle, including a two-edge parallel cycle, assign its
distinct edge blanks cyclically to its vertices, and extend along a forest
rooted on the cycle. All choices are distinct and incident to their owners.
A component without a cycle or private blank is a tree: it has v-1 blanks
for v attachments, so all cannot be covered; orienting a spanning tree away
from one uncovered root covers exactly the other v-1 vertices. QED.

Thus the exact unmatched count under this incidence is the number of tree
components with no private blank. The simple sufficient class 'each component
has a cycle or private blank' establishes D>=2L+k, even if some attachments
have only one available witness. More generally, disjoint sources of total
charge at most L satisfy

    2rho(R union sources)<=sigma+c-mu-p-u.               (5)

The checkable condition mu+p+u>=c+sigma proves aggregate compensation,
including cancellation between component balances. Each blank has one
identity in this sum; a private blank or a cycle is never separately reused
as another resource. No assertion of a new geometric route between distinct
components is needed for the additive charge inequality.

## 4. Sharp staircases: one shared witness per edge is short by half a unit

For any integer a>=2 use a (2a+4)-by-(2a+6) rectangle. Let saturated tiles
S_i=(1+i,a-i), 0<=i<a, and deficient tiles W_i=(2+i,a-i), 0<=i<a-1,
where these are tile coordinates. R consists of these 2a-1 tiles, an induced
staircase tile path. In every S_i select the TR and BL corners and make BR
a matching endpoint; TL is blank. In every W_i only TL is blank, with its
other three corners matching endpoints. Prescribe matching edges:

- S_0.BR--W_0.TR;
- S_i.BR--W_(i-1).BL for 1<=i<a;
- W_i.TR--W_i.BR for 1<=i<a-1;
- W_0.BR--its immediate right external neighbor.

All unspecified vertices are blank. The endpoints are disjoint. Each T has
its tile's P neighbor and all its external neighbors blank. This proves
feasibility for every a, without enumeration.

Every S has exactly one internal attachment. W_0 has t=0,p=3,s=2,h=0,
so (r,d)=(0,1) and charge1/2. Every other W has t=0,p=3,s=1,h=1,
so (r,d)=(0,0) and charge0. Hence k=a,D=a-1,sigma=eta=0,j=1 and rho=1/2.
The a-1 free blanks W_i.TL are each shared by exactly S_i and S_(i+1).
Thus H is a path: c=1,mu=p=u=0. Every debt has at least one free witness,
yet distinct allocation is short by one blank. This refutes the one-witness
rule, with a connected physical receiver of arbitrary size and many bends.

Two local repairs pay all a internal debts, with L=0:

1. Add tile V=(0,a) with labels PP/PB. Match V.TL--V.BL and V.TR to its
   immediate right external neighbor. Its BR blank is private to S_0.
   Thus p=1,mu=0 and rho(R union V)=0.
2. Add tile V=(1,a-1), also PP/PB. Match V.TL--V.BL and V.TR to its
   immediate upper external neighbor. Its BR blank is shared by S_0,S_1.
   It creates a second distinct edge between these two owners, giving
   mu=1,p=0 and rho(R union V)=0.

The added endpoints do not touch any T or an existing matching endpoint.
Each repair adds one free blank and a tile of charge -1/2. These formulas
prove both repairs at every a. Collapsing the parallel edges in the second
repair would lose the exact resource that pays the tree deficit.

The base full-grid objective is 4a-1 and each repaired objective is 4a+1,
all below mn/2=2a^2+10a+12. The examples distinguish regional rule failures
from a counterexample to the grid target. They involve positive internal
attachment debt; global matching or residual connectedness is not asserted.

## 5. Verification, attribution and limits

The geometric argument and constructive graph allocation are written proofs.
The new Lean module checks the degree-two corner fact and conditional count,
source and parity consequences. It does not formalize the whole witness
construction or the spanning-tree/cycle allocation. Finite controls construct
the actual witness graph, compute a maximum assignment independently and
verify the regional ledger, both repairs and single-use ownership under all
eight rectangle symmetries. Enumeration is auxiliary.

On 19 October 2026 the controls passed 69 staircase regions (sizes 2
through 24, each with no repair, private repair and cycle repair), 552
symmetry images and 45 inherited regions. The combined Lean audit passed
15 declarations, including the five new scoped statements, with only
propext and Quot.sound in their axiom dependencies.

Reproduce from the repository root:

    python3 develop/check_blank_witness_compensation.py --output output/blank-witness-controls.json
    python3 scripts/check_collar_formal.py --lean /path/to/lean-4.33.0/bin/lean --output output/blank-witness-formal-check.json

The second command compiles sequentially and records active lean/lake
processes and available-memory evidence before execution. Full existing
CI at the preceding attachment-corrected revision 7a5eeca passed; that
run does not certify these newly added files.

The component accounting resembles the earlier exterior-component ledger,
but its vertices here are saturated attachment owners and its edges are
actual shared blank vertices. Its new payment certificate follows from
the two-external-neighbor property of a tile corner. No external priority
claim is made. The preceding attachment-collar ACCEPT does not review this
new witness theorem. The universal 5/6 bound, arbitrary overlapping cores,
and proving the certificate for every grid configuration remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
