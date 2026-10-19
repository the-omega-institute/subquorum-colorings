# Long bent sources: saturated inward bands and disjoint terminal-strip payment

19 October 2026. General written arguments, separate from the submitted
manuscript. Finite controls are auxiliary. The final theorem has an explicit
endpoint-free terminal-strip hypothesis; universal source coverage is open.

## 1. A fully frozen family at every width and depth

Use the feasible-pair and original physical-tile ledger conventions of
`COMPONENT_RECEIVERS_AND_SQUARE_FREE_BOUND.md`. Thus T vertices have at most
one occupied neighbor, P is the endpoint set of the actual matching M, and
a promotion retains T, selects one endpoint of each chosen edge and deletes
its mate. A complete endpoint component is a component of the induced P graph.

Fix even w>=8 and h>=1. Put L=2h+1 and r=2h+2. Define

    H=({0,1} x {0,...,w-1}) union ({2,...,r} x {0,w-1}).

The two arms have equal odd length L. Write p_j^c=(j+1,c), where
c is 0 or w-1 and 1<=j<=L. The actual matching consists of

- (0,j)--(0,j+1) for even j=0,2,...,w-2;
- (1,j)--(1,j+1) for odd j=1,3,...,w-3;
- (1,c)--p_1^c on both arms;
- p_(2i)^c--p_(2i+1)^c for 1<=i<=h on both arms.

Require these selected supports:

- (0,-1),(0,w);
- (j+1,-1),(j+1,w) when j is odd;
- (j+1,1),(j+1,w-2) when j is even;
- (r+1,0),(r+1,w-1).

There are 4h+6 such supports, mutually nonadjacent; each sees exactly its
intended endpoint. Every endpoint has occupied degree three in the baseline,
and completeness holds when every unlisted site is blank.

**Freezing lemma.** Every endpoint of this prescribed source is immune to
every feasible simultaneous promotion bundle, including bundles on exterior
components. This remains true in every feasible completion retaining H,
its actual matching and the displayed supports.

Proof. If z is not promoted, its actual mate m(z) remains occupied: that
mate disappears only when the edge is used with z promoted. On either arm,
p_L has two selected neighbors, its outer and axial supports, and cannot be
promoted. Descending through odd j, p_j sees its outer selected support and
the retained mate m(p_(j+2))=p_(j+1). Thus p_1 is frozen on both arms.

Freeze the chamber using the zigzag of the unit-tail proof: start at
z_0=p_1^0, and set z_j=(0,j-1) for odd j and (1,j-1) for even j,
1<=j<=w. The first chamber vertex sees (0,-1) and m(z_0).
Each later z_(j+2) sees the distinct retained neighbors m(z_j),m(z_(j+1)).
Reflection in the chamber's vertical midpoint preserves the matching and
supports and supplies the other checkerboard-color wave. Finally p_2^c
sees its inside support and the retained mate of p_1^c, namely (1,c).
Ascending through even j, p_j^c sees its inside support and
m(p_(j-1)^c)=p_(j-2)^c. These three finite inductions freeze all H.
They apply to any fixed simultaneous bundle, so exterior promotions cannot
evade the argument. QED.

Place the chamber origin at even row and odd column relative to the fixed
2-by-2 tiling. Equivalently, in these coordinates tiles have even first row
and odd first column. The complete receiver R_H has

    |P|=2w+4h+2, |M|=w+2h+1,
    |R_H|=w/2+2h+3, T_R=2h+6,
    rho(R_H)=T_R+|H|/2-2|R_H|=1.                    (1)

The chamber has w/2+1 tiles; each arm contributes h+1 tiles. Each nonterminal
arm tile contains two P and one outer support. Its other exterior corner is
forced blank by that support. Each last arm tile contains one P, one outer
support and one axial support. The chamber end tiles each have two P and
one lateral support, with their last corners forced blank. All labels in
the receiver are therefore fixed in arbitrary feasible complete-component
exteriors. Actual matching transfers stay within this receiver, so (1)
includes the original saturated corrections.

## 2. Arbitrarily many completely saturated inward bands

For s=0,...,h-1, take the inward band

    B_s={2+2s,3+2s} x {1,...,w-2}.

It consists of N=(w-2)/2 aligned physical tiles. Write a=2+2s,b=a+1.
Add selected sites, preserving existing supports, in the following pattern:

    tile 1, columns 1,2:       (a,2),(b,1);
    tile 2, columns 3,4:       (b,3),(b,4);
    tile i>=3, columns 2i-1,2i: (a,2i-1),(b,2i).

All other unlisted sites are blank. The two lower boundary sites are the
prescribed inside supports. Every tile of every B_s has exactly two T and
no P, hence original charge zero.

To check feasibility for all h and w, each interior column has exactly one
T in the two-row pattern. Repetition of the pattern in successive bands
creates no vertical T adjacency: a lower-row selected column has its next
upper-row site blank. Upper-row selected sites have no horizontal T neighbor.
The only horizontal T adjacency is the lower-row pair in columns 3,4.
Each of those two sites has exactly that one selected neighbor and no P
neighbor. The lower boundary T sites see their arm P and no T neighbor.
An upper-row selected site can see a chamber P only in the first band,
where it has no selected neighbor. No added T touches any other P or forced
support. Thus every selected vertex has at most one occupied neighbor.
The freezing lemma still applies, and the full configuration is terminal.

The selected cardinality is hw+6, so the objective is

    |T|+|M|=(h+1)w+2h+7.

Translation by (2,3) embeds the configuration in an even rectangle of size
(2h+8)-by-(w+8). Its deficit from half the area is 3w+6h+25>0.

**Obstruction theorem.** For every prescribed finite depth k>=1, there is
a complete fully frozen positive receiver with its first k entire inward
bands saturated. In particular, enlarging that receiver by these bands
leaves charge exactly +1.

Choose h>=k in the preceding construction. This is an arbitrary-width,
arbitrary-depth construction and proof, not extrapolation from enumeration.
It refutes extending the unit-tail canonical donor unchanged, and refutes
every rule that always pays the receiver using a fixed number of complete
inward bands. The unit-tail proof used T(3,0); that vertex is now P, so its
sparsity hypothesis is absent. This does not refute the earlier theorem,
the global coefficient-one target, other exterior donors, or every bounded
radius method. In particular the next section finds a remote payment.

## 3. An endpoint-free terminal strip has two units of deficit

The terminal strip, immediately inside and below the two tips, is

    F_H={r,r+1} x {1,...,w-2}.                         (2)

It is a union of N aligned tiles, disjoint from R_H. Impose the additional
hypothesis P intersection F_H is empty. This hypothesis is not inferred from
feasibility or terminality. It holds in the obstruction construction above.
The required axial supports ensure row r+1 exists in the physical rectangle;
all strip columns lie between the two arms, so no extra padding is needed.

**Terminal-strip lemma.** In any feasible exterior with this endpoint-free
strip, its original charge is at most -2.

Proof. The entire first and last columns of F_H are blank. For the upper
left site (r,1), the support (r-1,1) is already adjacent to the endpoint
(r-1,0), so it forbids any additional occupied neighbor. For the lower left
site (r+1,1), the axial support (r+1,0) is already adjacent to (r,0).
Reflection gives the right boundary column. These conclusions use only
feasibility and the prescribed supports, not the endpoint-free hypothesis.

The remaining width w-4 is even. Partition columns 2,...,w-3 into pairs
(2,3),(4,5),...,(w-4,w-3). These are shifted unit squares, used only to
count selected vertices. Any unit square has at most two selected vertices:
three corners would include a selected corner with two selected neighbors.
There are (w-4)/2 squares, hence |T intersection F_H|<=w-4.
The physical strip has (w-2)/2 tiles and no endpoints, so its original
charge, on the original tiling, is

    rho(F_H)=|T intersection F_H|-(w-2)<=-2.           (3)

No ledger or matching transfer is changed by the shifted counting squares.
This is a selected-set bound on the same vertices, followed by the original
physical ledger. QED.

The bound is sharp in the sparse forced-support baseline: select both sites
in each odd interior column 3,5,...,w-3, and no other site in F_H. Each selected
pair is vertical and separated from the next by a blank column. The preceding
row contains only the boundary inside supports, so no new selected site sees
an occupied vertex outside its vertical pair. This feasible completion has
w-4 selected vertices in the strip. No simultaneous sharpness with the
saturated-band filling of Section 2 is asserted.

## 4. Terminal strips of distinct sources are disjoint

Assume distinct complete prescribed long sources, each in a positive
tile-preserving orientation and with its own endpoint-free terminal strip.
Surrounding neighborhoods need not be disjoint.

**Disjoint-strip lemma.** The physical tile sets F_H are pairwise disjoint,
even for perpendicular source orientations.

Proof for parallel strips. If they overlap, they occupy the same aligned
two-row band. Each strip is an interval of tile columns; its source has a
tip P in the immediately preceding and immediately following tile. Two
overlapping unequal intervals have a boundary tile of one lying inside the
other. That source tip contradicts the other's endpoint-free strip. If the
intervals are equal, the corresponding tips occupy the same inward-facing
column in each boundary tile. They are either the same vertex, or occupy
the two adjacent rows. Either case connects the two purported complete P
components. Rotation proves the parallel vertical case.

For perpendicular strips, normalize the first source as in Section 1.
Any vertical strip meeting F_H has both columns strictly between 0 and w-1.
Let u and v be the rows of the second source's upper and lower tips. Since
its strip consists of the rows strictly between those tips, meeting the
aligned band {r,r+1} gives u<=r-1 and v>=r+2. Its two tips have the same
column c in {1,...,w-2}.

If u<=0, the vertical endpoint-free strip contains a chamber endpoint of
H in row 1, a contradiction. If u=1, the upper tip itself belongs to H.
Thus 2<=u<=r-1. The upper tip lies in

    I={2,...,r-1} x {1,...,w-2},

whereas the lower tip lies outside I. But no P path in a different complete
component can exit I: its upper, left and right outside neighbors are P
of H, and its bottom outside row r in these columns lies in the no-P strip
F_H. A path exiting through an H vertex would join the components; exiting
through a no-P vertex is impossible. The connected second source cannot
contain both tips. This contradiction proves the perpendicular case. QED.

This proof allocates each entire physical strip once. There is no fractional
payment, hidden overlap multiplicity or shared boundary-tile contribution.

## 5. A new mixed-direction coefficient-one theorem with strict deficit

Let (T_0,M_0) be a feasible pair in an even-by-even rectangular grid.
Suppose every complete initial endpoint component is thin, has at most one
P-square, or is one of B prescribed long sources of Section 1 in a positive
tile-preserving position, with its actual matching and all its selected
supports. Require that each prescribed source's F_H initially has no P.
Then

    |T_0|+|M_0| <= mn/2-B.                            (4)

Proof. Apply objective-preserving feasible bundles until terminal. The long
sources are frozen in arbitrary exteriors, so survive with their actual
matching, supports and complete components. Other endpoint components can
only shrink; the thin/one-square alternatives pass to their final components.
No operation adds P, so every prescribed terminal strip stays endpoint-free.
Each nonprescribed final receiver has charge <=0 by the existing all-phase
thin/one-square theorem. Every prescribed receiver has charge +1 by (1).

By terminal tile ownership, all receivers are disjoint. By Section 4, the
prescribed strips are mutually disjoint; because they have no P, they also
lie outside every receiver. Put F=union_H F_H and let Z be all no-P tiles.
The exact original ledger is

    mn/2-|T_0|-|M_0|
      = sum_nonprescribed(-rho(R_H))
        + sum_prescribed(-1-rho(F_H))
        + sum_(Q in Z minus F)(2-t_Q).

Each prescribed summand is at least 1 by (3), and all remaining summands
are nonnegative. This proves (4) without spending any physical tile twice.
Relative to the universal 5/6 matching coefficient, the covered class gains
the full |M_0|/6 term and the additional B units. This remains a covered-class
theorem: the endpoint-free mouth condition and prescribed geometry matter.

## 6. Remaining boundary and verification scope

The saturated-depth obstruction and the terminal-strip theorem are compatible:
the former saturates intermediate bands, while the latter uses a strip beyond
all of them. Its distance from the chamber grows with h. The obstruction
therefore shows why the payment may need to follow the whole component.

If another component has endpoints in F_H, the strip no longer has charge
t-2, and its vertices may belong to another receiver. Those contacts are the
remaining cross-component transport problem. We do not assume their charges
are nonpositive, assign their budget twice, or infer a universal theorem.

The endpoint-free hypothesis is not automatic even when every component is
fully frozen. For w=10,h=2,r=6, start with the sparse forced-support baseline.
Add the four-endpoint vertical comb (r-1,3),...,(r+2,3), with consecutive
matching pairs and supports

    (r-2,3),(r+3,3),(r-1,4),(r,2),(r+1,4),(r+2,2).

The top and bottom comb endpoints each have two selected supports; alternating
retained-mate waves freeze the other two. Every added support sees exactly
its one comb endpoint and no other occupied vertex. The two components are
complete and distinct. The comb crosses F_H in two endpoints; its whole
receiver has charge zero, while the original long source still has charge
+1. Translation (2,3) gives a concrete 12-by-18 fixture of objective 37,
recorded by the verifier. It refutes deriving the no-P mouth condition from
global freezing, not (4) or the universal target.

`develop/check_saturated_bent_bands.py` reproduces family feasibility, full
freezing, exact receiver counts and all saturated bands. Further terminal-strip
and overlap controls are supplied separately. General proofs above do not use
any finite census as a premise. New independent review is recorded separately.

Completed controls: 78 saturated-band cases and 72 symmetry images; 68 sharp
terminal-strip cases; exact selected-set dynamic programming at 17 even strip
widths; all overlap-producing aligned translations for 72 source descriptions
against one fixed source, giving 240 parallel and 504 perpendicular placements.
Every overlapping placement either puts P in a claimed no-P strip or joins the
two endpoint components. A four-source fixture checks mixed orientations,
distinct strip resources and a total four-unit compensated deficit. The occupied
mouth fixture above independently checks the essential missing hypothesis.

The sequential local Lean 4.33.0 audit passes 78 declarations, including five
new statements in `formal/SubQuorum/LongBentTerminalStrips.lean`: physical square
selected capacity and forced blank boundary; conditional shifted-strip count
and paid-strip summation; integer interval-overlap alternatives. Full source
freezing, cardinality/partition adapters, perpendicular separation and the
initial-pair theorem remain written. The receipt is
`output/long-bent-strip-formal-check.json`; no full geometric formalization is
claimed. Earlier proofs retain their explicitly stated scope.
