# Nonpositive pressure bands can have arbitrarily many exits

30 September 2026. Continuation of [boundary-aware compensation](CROSS_COMPONENT_COMPENSATION.md)
and [neutral transport](COMPENSATION_TRANSPORT.md), on the isolated research
branch. The current joint manuscript is not changed.

We strengthen the local band estimate: under a full row of matched endpoints,
every tile in the band has nonpositive residual charge, with no assumptions
on its internal matching or lower-row labels. We also construct neutral bands
with arbitrarily many downward saturated attachments. Thus a general neutral
band cannot automatically be treated as the two-exit relay of the preceding
transport lemma. The family has explicit, disjoint terminal donors and satisfies
the target inequality; it refutes the two-exit inference, not coefficient one.

## 1. Precise entrance and attachment restrictions

Use the fixed aligned 2x2 tiling of a feasible even-by-even rectangle. A vertex
is T, P or B according as it is selected, is a matching endpoint, or is blank.
For a deficient tile Q, write t_Q, h_Q and s_Q for its selected vertices,
internal matching edges and matching attachments to saturated tiles. Put

    r_Q = 2-t_Q-h_Q-s_Q,
    rho(Q) = deg_Gamma(Q)/2-r_Q.

Saturated tiles have two T vertices and are assigned rho=0. The global identity
is q=|T|+|M|-mn/2=sum_Q rho(Q).

Let S be a horizontal band of w>=1 aligned tiles, with two vertex rows. Assume:

1. Every vertex immediately above the upper row of S is **P**.
2. Its left cap is `T P / B T` and its right cap is `P T / T B`.
   Each cap's P is matched upward, away from S.
3. The entire surrounding configuration is feasible.

These are satisfied by the filled source corridor and by the entrances created
in the preceding neutral-transfer lemma. The P assumption is stronger than
merely saying that the row above is occupied. All rotations and reflections
of the statement are permitted.

Every saturated tile inside S has no P. An upper T has an occupied neighbor
above, so both its within-tile neighbors must be B, leaving room only for an
opposite T. If neither T is upper, both lower corners are T and both upper
corners must be B. These cases exhaust the saturated tiles.

No matching attachment from S to a saturated tile can go upward: both lower
corners of every tile directly above S are P, whereas a saturated tile can
contain at most one P. None goes sideways: the only P in either flanking cap
is already matched upward. None goes to a saturated tile inside S, by the
previous paragraph. Consequently **all saturated attachments from S go
downward**.

A downward attachment at a lower P corner forces its lower within-tile
companion to be B. Indeed, the receiving saturated tile has diagonal T corners,
one P at the receiving upper corner, and one B. Its other upper corner is T,
already adjacent to that P; the vertex immediately above this T must be B.
In particular there is at most one such attachment per tile.

## 2. Tilewise nonpositivity and the sharp aggregate bound

**Theorem 1 (pressure-band nonpositivity).** Under the hypotheses in Section 1,
every tile Q of S satisfies rho(Q)<=0. If sigma is the total number of
saturated attachments from S and Delta=(|B intersect S|-|T intersect S|)/2,
then

    rho(S) = -Delta+sigma/2 <= min(0, -1+sigma/2).          (1)

Equivalently, Delta>=max(1,sigma/2). In particular a neutral band must have
sigma>=2 and Delta=sigma/2. The theorem permits arbitrary residual matching
edges across its boundary and capacity-two tiles.

**Proof.** Let p_Q be the number of P corners. For a deficient tile,

    deg_Gamma(Q) = p_Q-2h_Q-s_Q,
    2rho(Q) = 2t_Q+p_Q+s_Q-4.                            (2)

All matching incidences are included: internal edges use two P corners,
saturated attachments use one, and the remaining P corners are residual
incidences. There are three cases.

- If t_Q=0, every saturated attachment has its distinct forced B companion.
  Hence p_Q+s_Q<=4, and (2) is nonpositive.
- If t_Q=1 and T is upper, its two within-tile neighbors are B because of
  the P above it. Thus p_Q<=1 and s_Q<=p_Q, again giving (2)<=0.
- If t_Q=1 and T is lower, p_Q<=2: three P corners would give T two occupied
  neighbors within Q. There is no downward saturated attachment in Q,
  since it would require both lower corners to be P,B, excluding the lower T.
  Thus s_Q=0 and (2)<=0.

Saturated tiles have charge zero by definition. This proves the tilewise claim.
The boundary-aware band identity and blank-surplus lemma apply to this stronger
entrance and give rho(S)=-Delta+sigma/2 with Delta>=1. Combining the two bounds
proves (1). QED.

The local argument depends on labels and saturated attachment incidence, not
on h_Q or the pairing of residual ports. In particular repeated routed visits
and matching flips cannot create an extra resource in a neutral tile.

**Corollary 2 (closed-band compensation).** For the associated filled source
U, rho(U)=1, so

    rho(U union S) <= min(1,sigma/2).

When sigma=0, this is coefficient one for the pair of regions. For pairwise
disjoint such pairs with sigma=0 and a remainder of nonpositive charge, summing
proves |T|+|M|<=mn/2, improving 5/6 to 1 on that covered class. For sigma>=2,
tilewise nonpositivity alone still leaves the source's full unit unpaid.
The new bound does not improve the universal 5/6 constant.

There is a useful limited termination fact: a sequence following only the
saturated exits of bands satisfying Section 1 in the same downward orientation
cannot contain a directed cycle. Each exit increases the tile-row index.
This does not say that an exit supplies another band entrance, or assign any
terminal donor. Rotating at a bend leaves this row-monotonic argument.

## 3. A neutral band with arbitrarily many outgoing pairs

For an integer b>=1 put k=4b-1 and N=2k+4=8b+2. Use a 6xN rectangle,
with vertex rows 0,...,5 and tile columns 0,...,k+1.

Start with the filled corridor of the earlier note:

    T_frame = {(0,0),(0,N-1),(2,0),(3,1),(2,N-1),(3,N-2)};
    source edges = {((0,2j+1),(0,2j+2)): 0<=j<=k}
                   union {((1,2j),(1,2j+1)): 1<=j<=k}
                   union {((1,1),(2,1)),((1,N-2),(2,N-2))}.

In S, the inner tiles of tile row 1, match the two upper vertices internally
in every tile. For each a=0,...,b-1 set

    L=4a+1,  C=4a+2,  R=4a+3.

Add matching edges

    ((3,2L+1),(4,2L+1)),  ((3,2R),(4,2R)),
    ((3,2C),(3,2C+1)),    ((4,2C),(4,2C+1)),

and selected vertices

    (4,2L), (5,2L+1), (4,2R+1), (5,2R).

For a=0,...,b-2 also set J=4a+4, match ((3,2J),(3,2J+1)), and select
(5,2J),(5,2J+1). Finally select (4,0),(5,1),(4,N-1),(5,N-2).
All unspecified vertices are B.

The b=2 tile layout is

```text
source:       L F F F F F F F L
neutral band: A E D E D E D E A
bottom:       O A C A Z A C A O
```

Here the two L's are residual leaves. F has h=1,r=1,degree=2.
E is `PP/Bs` or `PP/sB` with a downward attachment s, h=s=1,r=degree=0.
D is full P with two internal edges, also r=degree=0. A is a saturated
attached cap. Each C is `PP/BB`, with one internal edge and rho=-1.
Z is `BB/TT`, saturated; O is a saturated exterior diagonal pair.
The letters describe tiles, not extra vertices or edges.

**Proposition 3 (unbounded exit count).** The construction is feasible for
every b>=1 and has exactly:

- one source component with k+1 edges, capacity k and excess +1;
- k isolated neutral band tiles with r=degree=0;
- b isolated bottom donor tiles with r=1,degree=0 and excess -1.

All other tiles are saturated. Thus

    sigma(S)=2b,  Delta(S)=b,  rho(Q)=0 for every Q in S,
    |T|=6b+8,  |M|=17b-1,  H=24b+6,  q=1-b.             (3)

Each pair of consecutive caps at L,R supplies a width-one child band C with
sigma=0 and rho=-1. The b child bands are pairwise disjoint.

**Proof.** Source feasibility is as in the filled corridor. New upper-band
edges use only its previously blank vertices. At the lower row of S, the
endpoint tiles reserve B,s or s,B, and all other tiles match their two P
vertices internally. These vertices and the b bottom C edges are disjoint,
and the receiving P vertices lie only in the bottom caps.

In each bottom cap the diagonal T vertices have their single P neighbor.
The top T sees a B above, the companion of the prescribed outgoing attachment.
Its horizontal external neighbor is B: it faces an exterior O or a separator Z,
both blank at that upper corner. The lower T faces a B of C. There is no row
below. A separator Z has two adjacent lower T vertices; each sees only the
other T, since its upper neighbor and its external horizontal neighbor are B.
The two exterior O tiles have diagonal T vertices; their outside-facing upper
T sees a B above, and their lower T sees a B in the adjacent cap. All other
neighbors of these T vertices are B or outside the rectangle. The source and
row-1 cap T vertices see no new occupied neighbor: each new vertex immediately
below their lower T is B. This verifies every T constraint and feasibility.

The source residual graph is unchanged. In S there are 2b end tiles with
h=s=1 and 2b-1 full tiles with h=2; each has capacity and degree zero. In the
bottom row the C tiles have h=1,capacity=1,degree=0; everything else is
saturated. This gives the entire component list and proves the charge claims.
There are 2b blanks and no T in S, hence Delta=b. Counting selected vertices
gives 6+4b+2(b-1)+4=6b+8. The matching has 8b+1 source edges, 4b-1 upper-band
edges, 2b-1 lower-band internal edges, 2b outgoing attachments and b bottom
edges, totaling 17b-1. The counts prove (3).

Below the intermediate full tile C of each triple L,C,R, the caps have exactly
the entrance orientations of Section 1, the pressure row is PP, and the child
band is PP/BB. It therefore supplies one unit. Their distinct tile columns
make the b donors disjoint. QED.

Already b=2, on 6x18, has a neutral band with four outgoing attachments,
|T|=20, |M|=33, H=54 and q=-1. Its two bottom donors each pay one unit;
there is only one positive source. This explicitly refutes the inference
“rho(S)=0 forces sigma=2 and one narrower successor band.” Taking b arbitrarily
large refutes any bound on the number of exits independent of band width.

The example does not exhibit two sources overusing one donor. It instead
shows why counting one new unit of inherited demand for every outgoing pair
would overstate the original demand: b outgoing pairs coexist with a single
incoming unit. A global branching or merging rule must specify the allocation
of that unit and unique ownership of each donor; (1) does not supply that rule.

## 4. Sharpness, matching flips, and verification

The earlier sharp occupied band has sigma=0,Delta=1,rho=-1. The b=1 member
above has sigma=2,Delta=1,rho=0. For sigma=1, take the depth-two, width-three
nested corridor from the transport note, and delete the top-right T at (4,7)
from its right receiving cap. Deleting T preserves feasibility. The band
labels stay unchanged, while its right downward matching edge now meets a
deficient tile. Hence Delta=1,sigma=1,rho=-1/2. These three coordinate examples
attain (1) for sigma=0,1,2. The family in Section 3 attains the zero upper
bound for every positive even sigma.

In the family, the square matching flips from the preceding note preserve
every tile's charge and produce capacity-two passages. Flip only squares
straddling two deficient tiles and leave the saturated attachments fixed.
In each affected tile h decreases by one, r increases by one and residual
degree increases by two. The original component list can change, while
Theorem 1, all per-tile charges, sigma and the objective remain unchanged.

Run:

```sh
python3 develop/check_pressure_bands.py --output develop/results/pressure-band-branching-2026-09-30.json
```

The checker enumerates all 81 tile labelings with necessary upper-pressure
constraints and all downward attachment choices. This is a relaxed local
control, not a classification of globally realizable matchings. It separately
checks the explicit families for b=1,...,32, first/all square-flip variants,
and all eight rectangle symmetries: 768 family images. The three sharpness
examples add 24 images, for 792 in total. Coordinate feasibility, component
reconstruction, prescribed routing and the existing five-sixths assertions
are checked independently of the written case proof. Coordinates and source
hashes are archived. The all-size proofs are the arguments above, not finite
enumeration; no new Lean theorem is claimed.

## 5. Manuscript proposal and remaining boundary

After joint review, Theorem 1 can follow the boundary-aware compensation lemma
after Proposition B.13. Proposition 3 can accompany the discussion of why
arbitrary occupied bands need more than a single-chain transport proof.
These are proposed additions only; the arXiv source remains at its existing
revision.

Next, seek a rule that selects and weights outgoing entrances, controls bends,
and gives each terminal tile a single total budget even when chains merge.
The row-monotonic observation does not settle cycles after turns, and the
disjoint donors of the displayed family do not settle shared terminals.
General bent paths and the unrestricted coefficient-one bound remain open.
