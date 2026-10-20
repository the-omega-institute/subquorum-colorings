# Every finite rotor-only fusion has reserve, in every phase

20 October 2026. We prove that complete rotor supports exclude the
unpaid exceptional contacts left by the general half-slot theorem.
The negative contact components must be rectangles in rotated tile
coordinates. An exact Euler count then leaves two units per component.
No prescribed contact graph, pair-feasibility or freezing is required.

## 1. Model and theorem

Use the complete fixed-source fusion model of
ALL_PHASE_JOINT_COMPENSATION_SLOTS.md, restricted to rotor sources.
The reference endpoint and selected sets are

    E={(1,2),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,3)},
    T={(0,2),(1,1),(2,5),(1,4),(5,3),(4,4),(3,0),(4,1)}.

The original four matching edges join each outer endpoint to its adjacent
central endpoint, as in develop/rotor_networks.py. All lattice isometries,
integer translations, effective phases and both chiralities are allowed.
Original endpoint sets are pairwise disjoint. Final P and M are exactly
the original unions. Write

    T=(union_i T_i minus P) union Topt,

where optional Topt is outside every original receiver and has no endpoint
neighbor. Require this complete final retained-support union to be feasible.
The admitted ledger below applies to this final T, including Topt. All
sources and the ambient even-by-even rectangle are finite.

A rotor has charge-2 or zero. Each negative rotor has a unique aligned
full central tile. Form a graph on the negative rotors, joining two when
their central tile indices differ by(+/-1,+/-1). Let cminus count its
connected components, with cminus=0 if it has no vertices. With the
established original-owner notation, S=2Rminus, G=N=0 and

    C=sum_Q [2J_Q-Kregular(Q)] >=0.

We prove

    S+C-Kirregular = 2cminus+Cother >= 2cminus,
    Cother=sum_{Q not a negative-component face} c_Q >=0,
    sigma=mn/2-|T|-|M| >= 2cminus.                    (1)

If every source is negative, equality holds in the first line. The
actual ambient slack in the second line can be much larger.
This proves coefficient one, improving5/6 by |M|/6 in this class,
without restricting the zero-rotor phases or the number of negative
rotors. It does not settle arbitrary mixed U/rotor fusions or the
rectangular-grid triple equality.

Every event retains its ORIGINAL endpoint tail. It records that tail's
unique original intratile blank becoming a foreign original endpoint.
An irregular event has original1P1T profile; Kregular(Q) uses the original
endpoint-bearing regular profiles in Q. Extra source selections consumed
inside Q do not create another endpoint owner or another regular event.

## 2. Complete sixteen-role ownership, with no translation cutoff

Write Rplus(a,b) for E,T translated by(a,b), and Rminus(a,b) for
(r,c)->(r+a,-c+b). The reference rotor is invariant under

    quarter(r,c)=(c,5-r),

including its endpoints, selections and matching. Thus every affine
rotor image is one of these two translation families. If target z is
an endpoint of a specified chirality and original endpoint role e in E,
its translation is uniquely

    (a,b)=(z_r-e_r,z_c-e_c) for Rplus,
    (a,b)=(z_r-e_r,z_c+e_c) for Rminus.

There are exactly sixteen possibilities. Remove any candidate sharing
an endpoint with an already present source. The following tables are
therefore exhaustive over all integer translations, not bounded tests.

Normalize a negative source to Rplus(0,0). Its endpoint p=(1,2) has
unique original blank delta(p)=(1,3). Endpoint-disjoint owners of delta(p)
are precisely

    Rplus(-2,2), Rplus(-3,0), Rminus(-3,6).           (2)

The first is a negative rotor with diagonally adjacent central tile.
We next exclude the other two in any finite complete feasible fusion.

## 3. Two impossible contact types force unending extension

Any old selection with two persistent endpoint neighbors must be an
original foreign endpoint in final P. Otherwise it remains selected,
in contradiction to feasibility. Additional sources can remove candidate
owners through endpoint collisions, but cannot create a seventeenth role
or permit a multiply anchored old selection to remain selected.

**Type A.** Suppose Rplus(0,0) and Rplus(-3,0) occur. The following
sixteen-role calculations give all possible original owners.

| Already present sources | Forced old selection | Persistent endpoint neighbors | All possible owners |
|---|---|---|---|
|Rplus(0,0), Rplus(-3,0) |(1,1)|(0,1),(1,2)|Rplus(-1,-3) or Rminus(-2,2)|
|previous pair and Rminus(-2,2) |(2,1)|(1,1),(2,2),(3,1)|none|
|original pair and Rplus(-1,-3) |(0,0)|(0,-1),(0,1),(1,0)|Rplus(-4,-3)|

The reflected option is impossible. Consequently the fusion contains
Rplus(-1,-3) and Rplus(-4,-3), a copy of the original ordered pair
translated by(-1,-3). These deductions depend only on endpoint/support
incidence and therefore apply to every translated copy, even if its
effective phase differs. Among all copies in a finite fusion, choose
one whose first-source column translation is least. Its forced copy
has column translation smaller by three, a contradiction.

**Type B.** Suppose Rplus(0,0) and Rminus(-3,6) occur.

| Already present sources | Forced old selection | Persistent endpoint neighbors | All possible owners |
|---|---|---|---|
|Rplus(0,0), Rminus(-3,6) |(1,4)|(0,4),(1,3),(2,4)|Rminus(-1,8)|
|previous pair and Rminus(-1,8) |(3,4)|(2,4),(3,3),(3,5)|Rplus(2,2)|

The forced new pair Rplus(2,2),Rminus(-1,8) is the original ordered
pair translated by(2,2). Among all copies in the finite fusion choose
one with greatest first-source row translation. The forced copy increases
it by two, again a contradiction. Neither argument discards a support.

Only the first owner in (2) survives. Quarter turns preserve the aligned
tiling, and the reflection(r,c)->(r,5-c) also preserves it. They normalize
any negative rotor port and either chirality to the case just proved.
Hence every actual irregular event is owned at its other end by a
negative rotor of the SAME chirality with diagonally adjacent central
tile. In particular a negative1P1T/zero3P0T full contact cannot occur:
it would give exactly such an event with a zero-rotor owner. Thus BR=0
for every rotor-only fusion. Sections4-5 prove reserve directly from the
three stated established inputs, without using the half-slot theorem.

## 4. Complete supports force rectangular negative components

The local port geometry is explicit. Relative to a physical port tile Q,
the direction of a negative rotor's central tile determines its endpoint
corner in Q:

| Central tile lies from Q | plus chirality | minus chirality |
|---|---|---|
|North|NE|NW|
|East|SE|NE|
|South|SW|SE|
|West|NW|SW|

A plus port's intratile original selection is the next clockwise corner;
a minus port uses the preceding corner. The other adjacent corner is
its unique original blank.

Central tiles cannot be cardinally adjacent: a port would overlap the
other source's central full tile. Diagonally adjacent centers cannot
have opposite chiralities: in one of the two shared port tiles their
endpoints coincide. Therefore every negative contact component is
monochiral.

Suppose two same-chirality negative centers lie on opposite sides of Q.
Their ports occupy opposite corners of Q. Both other corners are original
supports and each sees the two persistent endpoints, so each must become
a foreign original endpoint. Each forced corner is an irregular blank
of one of the known negative rotors. The event-owner theorem in Section3
therefore forces a same-chirality negative rotor at each of the other
two central-tile positions around Q.

Fix one component and a reference center(row0,column0) in it. Set

    u=((row-row0)+(column-column0))/2,
    v=((row-row0)-(column-column0))/2.

Both are integers because diagonal center steps preserve checkerboard
parity. Diagonal adjacency becomes ordinary nearest-neighbor adjacency.
The preceding forcing says that occupied opposite corners of an elementary
square in(u,v) force its other two corners. The forced centers belong
to the same component, since they are adjacent to the given ones.

Here is a complete rectangle argument. Start with one occupied vertex,
a1x1 rectangle. If the connected component has a vertex outside the
current occupied rectangle, a path to it has a first vertex outside;
that vertex is adjacent to the rectangle along one side. Adjoin it.
For each successive position along that side, the new vertex and the
old vertex diagonally across the next elementary square force the next
new vertex. Propagating in both directions fills the entire new row or
column along that side. Thus the rectangle expands by one complete row
or column, remains occupied and stays in the same component. Since the
component is finite, expansion terminates. Connectedness then excludes
any vertex outside the final rectangle. The component is exactly a
Cartesian rectangle, including a single row, column or vertex.

Let its dimensions be a_h x b_h. Summing over components, define

    V=sum_h a_h b_h,
    Ecount=sum_h[(a_h-1)b_h+a_h(b_h-1)],
    Fcount=sum_h(a_h-1)(b_h-1).

Counting vertices, edges and unit faces in each rectangle gives

    V-Ecount+Fcount=cminus.                          (3)

## 5. Exact event count and distinct unspent credit

Each diagonally adjacent negative pair has two common port tiles.
The port table shows exactly one irregular event in each tile, for a
total of two. This follows from its original unique blank becoming the
other rotor's original endpoint, whether or not further sources occur.
Conversely every irregular event belongs to precisely this pair by
Section3. Different pairs give different events because each event
retains its original tail and unique foreign endpoint owner. Therefore

    Kirregular=2Ecount.                              (4)

Every unit face of one rotated rectangle corresponds to a physical
tile with four ports from four different negative rotors. It is a NEW
mixed full tile. All four original local profiles are1P1T, so it has
four irregular events and NO regular event. Its full two units remain
in C. Distinct faces give distinct tiles, including across components:
the four central tiles around a face determine its physical tile
uniquely, and their diagonal adjacencies put them in one component.
All other tiles have nonnegative residual c_Q by the established
regular-tile theorem. Thus

    C=2Fcount+Cother, Cother>=0,
    C>=2Fcount.                                     (5)

No regular payment or another face uses these same two units. Since
S=2V, (3)-(5) yield

    S+C-Kirregular >=2V+2Fcount-2Ecount=2cminus.

Keeping Cother gives the exact identity

    S+C-Kirregular=2V+2Fcount+Cother-2Ecount
                 =2cminus+Cother.

The established ledger gives the second part of (1). If all sources
are negative, every new mixed full tile must consist of four ports;
an original central full tile cannot contain any foreign endpoint.
Such a four-port tile is one of the counted faces. Also Kregular=0,
so C=2Fcount and equality holds in the reserve identity.

## 6. Sharp all-parameter family with full original supports

For arbitrary integers a,b>=1 use the standard negative rotors translated by

    h(i,j)=(2i+2j,2i-2j), 0<=i<a, 0<=j<b.

All original matching edges are retained. The entire retained support
set is described as follows, with coordinates translated by h(i,j).

| Original support pair | Retained exactly when | Original anchor |
|---|---|---|
|(0,2),(1,1)|i=0|(1,2)|
|(1,4),(2,5)|j=0|(2,4)|
|(4,4),(5,3)|i=a-1|(4,3)|
|(3,0),(4,1)|j=b-1|(3,1)|

These formulas have an exact finite-role proof for all integer indices.
This explicit family uses Topt=empty; its cardinality and ambient-slack
formulas below include exactly the retained original supports.
A displacement(row,column) equals h(delta_i,delta_j) precisely when
row+column and row-column are divisible by4; its indices are then
((row+column)/4,(row-column)/4). Differences E-E and T-T give no
nonzero integer index displacement. Thus endpoints of different sources
are disjoint and original support points are distinct. For each support,
apply this inverse to its differences with all eight endpoint roles.
The unique possible consuming source has relative indices(-1,0),
(0,-1),(1,0),(0,1), respectively for the four rows of the table.

For the first support pair, apply the same inverse to differences between
any nonanchor neighbor and all original occupied roles E union T.
Every possible additional occupied neighbor comes from relative source
indices with delta_i=-1. All such sources are absent when i=0.
The other three rows respectively require delta_j=-1, delta_i=1 and
delta_j=1. They are absent on their stated boundaries. Thus every retained
selection has exactly its original anchor as its unique occupied neighbor.
All consumed supports are original endpoints of the identified neighboring
source. This proves complete feasibility for arbitrary a,b, not just a
collection of small rectangles.

The exact counts are

    |P|=8ab, |M|=4ab, |T|=4(a+b),
    S=2ab, Kirregular=4ab-2a-2b,
    J=(a-1)(b-1), Kregular=0, C=2(a-1)(b-1),
    S+C-Kirregular=2.                               (6)

For a=b=3, actual irregular demand24 exceeds source reserve18 by six;
four distinct mixed full tiles supply eight unused units, leaving two.
Translating columns by2(b-1) embeds the complete family in an even square
of side2(a+b+1). In that particular square the actual ambient slack is
2(a*a+b*b+1), distinct from reserve2.

## 7. Verification, review and scope

The exact sixteen-role classifications, all-index displacement tests
and complete physical controls are implemented in
develop/check_rotor_only_reserve.py. All59 complete physical controls pass,
including25 rectangle sizes,32 isometry/phase images, separated negative
components with zero rotors and a genuine negative/zero support contact.
The finite fixture sizes do not prove the universal theorem; Sections2-6
give its ownership, finiteness, rectangle and arbitrary-parameter proofs.
The underlying ledger and tilewise regular payment are established inputs.
Nineteen Lean declarations and individual axiom audits pass locally with
Lean4.33.0, one job and44% free memory at the current audit preflight. They check the
six complete16-role tables and forced-support obligations, original degrees,
quarter invariance, port geometry, diagonal event counts, exact support-role
displacements and conditional Euler/reserve/slack arithmetic. No
sorryAx/native_decide is used. The arbitrary-source normalization, finite
descent, general rectangle argument and event/face bijections remain written.
This is not a full Lean proof of arbitrary rotor fusions. See
output/rotor-only-reserve-formal-check.json and
output/rotor-only-reserve-controls.json for execution evidence.

The candidate argument originated in exploratory taskf629ba4e. This note
reconstructs and checks its missing ownership, support and rectangle steps.
It is outside the earlier separated, general-defect and half-slot review
scopes; no previous ACCEPT is claimed to cover it. Independent review
d8ed1445-df3a-4a57-af3c-c685f6d3eef3 inconv_8ea87be5d39c5eaa completed
ACCEPT at00:43:51.859UTC, observed gpt_6/pro. Original stream35800 exits0,
ends DONE and matches all17864 terminal response characters exactly.
Its standalone event-definition, unused half-slot dependency and optional
selection clarifications are implemented above. Execution checks remain
separate; normalization/descent/rectangle/event-face geometry are written.
The unrestricted U/rotor joint
allocation and general rectangular-grid problem remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
