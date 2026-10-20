# Critical owner profiles, capacity two and actual shared stop compensation

20 October 2026. The complete critical geometry excludes positive U and
negative rotor receiving owners. Every critical event has at least two
original owner endpoints in its physical tile. These original profiles
are globally disjoint even when critical receiving tiles coincide, giving
capacity at most two events per tile and a stronger outside-owner count.
Nonfull phase10 terminal and zero-rotor exits can also be charged directly
to the existing H and Z0 occurrences. This is a partial compensation lemma
for the unrestricted model, not the full coefficient-one allocation or
rectangular-grid equality, which remain OPEN.

## 1. Complete-source setting and an active bar wall

Use ALL the complete finite original U/rotor, legal even dimensions,
original endpoint ownership, unchanged matching, mandatory support and
degree-one hypotheses of
[the critical continuation theorem](PHASE11_CRITICAL_CONTINUATION_AND_ALL_OWNER_COUNT.md).
Use its globally injective critical points and
[separation from ALL first/LONG receivers](ALL_CRITICAL_REGULAR_RECEIVER_SEPARATION.md).
No contact-graph, freshness, dimension bound, AA or closedness assumption
is imposed. Source phases always use the transported physical partition.

Normalize a critical root t to0 with frame(N,E) and tile Q={0,1}^2.
Its active phase01 U is O, its first phase11 owner is F, and its own
original owner is G. The inherited critical construction gives a width W
and opposite F leg height h, both even, with h+4<=W. In canonical O
coordinates t=(2,h+3). Consequently

    k=W-h-3 is odd and at least1;
    (-1,c) belongs to O for every0<=c<=k;
    (0,k),(1,k),(2,k) belong to O.                  (1)

The last three points use O's opposite height at least4. These are
original endpoints, including the minimum k=1. They are foreign to G.
The original F endpoint(0,-1) is also foreign. In particular G avoids
the north and west neighbors of t. Other original owners can recur.

## 2. Complete original profile classification

For a U owner, split the canonical endpoint predicate into its bar and
two stems and split the eight signed coordinate permutations. Avoiding
the north and west neighbors leaves precisely:

- an upper outer bar corner, with the canonical row flip false and the
  column flip pointing into the bar; or
- a terminal, with canonical row flip true, pointing south or east.

This is an arbitrary-dimension inequality proof. Pulling the actual Q
origin gives(anchor.row-int(flipRow),anchor.column-int(flipColumn)).
The bar case therefore has phase01 and an exact original4P0T profile.
The terminal case has row phase1 and an exact original2P1T profile.
Thus a positive phase00 U cannot own ANY critical point. Terminal
column phase0/1 distinguishes the following possibilities:

| Original owner | Root role and original endpoints in Q | Original support in Q |
|---|---|---|
| U01 | outer corner, all four points | none |
| U10 | terminal south, (0,0),(1,0) | (0,1) |
| U11 | terminal south, (0,0),(1,0) | (1,1) |
| U11 | terminal east, (0,0),(0,1) | (1,1) |
| zero rotor, pair type | tip south, (0,0),(1,0) | (0,1) |
| zero rotor, triple type | tip south, (0,0),(1,0),(1,1) | none |

The phase10 eastward terminal that the two-neighbor test alone allows
is impossible by(1). Its other leg lies north. Let g>=4 be its incident
height. If g>=k its eastward stem owns(0,k), colliding with O's wall.
If g<k its vertical bar owns(-1,g), colliding with O's bar. This covers
both terminal columns and independent opposite heights.

For a rotor, every central endpoint has three own neighbors, so t must
be a tip. Quarter-turn invariance reduces all arbitrary placements to
two chiralities times eight anchored roles. The north/west exclusions
leave exactly four roles: two original2P1T and two original3P0T profiles.
All four have original charge zero, not minus two.

The horizontal pair role owns(-1,1), so is excluded by O. For k=1,
each remaining role meets one of(0,1),(1,1),(2,1), so no rotor fits.
For k>=3, O also owns(-1,2), excluding the horizontal triple role.
Exactly the two south-pointing rotor roles in the table remain. This
exhaustive fixed-role calculation is a proof of the rotor classification;
it does not bound translations or source dimensions.

## 3. Profiles inject even if receiving tiles do not

For each critical event e let G(e) be its actual original owner, Q(e)
its actual receiving tile, and

    V(e)=P_G(e) intersect Q(e).

The map e -> (G(e),Q(e)) is injective. A U01 root is one of two upper
outer corners, separated by width-1>=5. A U10/U11 root is one of two
terminal tips, likewise separated by width-1>=5 in one canonical
coordinate. For a fixed owner these classes cannot mix because its
effective phase is fixed. Rotor roots are tips, and any two distinct
rotor tips have a coordinate difference greater than1. Thus two critical
roots of the same owner cannot share a physical tile. Global critical
point injection then identifies the event.

The sets V(e) are pairwise disjoint. Different owners have disjoint
original endpoints. The same owner at different events has different
physical tiles. No injection of receiving owners or receiving tiles is
being assumed.

Every V(e) has size2,3 or4. Hence at most TWO critical events can share
a tile. If two do share it, they have different original owners, each
with an exact original2P1T profile, and together fill the tile. A triple
or original full-bar critical receiver admits no second critical event.
This upper bound is not claimed sharp for complete feasible critical
configurations; no complete sharing example is supplied here.

Let K2,K3,K4 count the three profile sizes, and K=K2+K3+K4. Then

    |union_e V(e)|=2K2+3K3+4K4=2K+K3+2K4.          (2)

This resolves critical-to-critical ENDPOINT reuse for this profile count.
Whether the physical receiver map itself is injective remains open and
is unnecessary for(2). All V(e) avoid every first/LONG receiving tile.

Choose original closed phase01 owners C and split critical events into
Kc owned by C and Ke not owned by C. Every C-owned return has size4.
Among the Ke external events let Ke3,Ke4 count sizes3,4. Write Ve,Vc
for the corresponding profile unions, and retain X,J=J01+J11 from the
ordinary receiver theorem. Exact disjointness gives

    |Ve|=2Ke+Ke3+2Ke4, Ve intersect P_C=empty;
    |X union Ve|+J=2(C01+L11)+2Ke+Ke3+2Ke4;
    |X union Ve union Vc|+J=
      2(C01+L11)+2Ke+Ke3+2Ke4+4Kc.                (3)

The external requirement gains Ke+Ke3+2Ke4 compared with counting only
one root per external event. In a qualifying SAME AA endpoint component,
direct H packing gives J=0 and C01>=4ell, hence

    |X union Ve|>=8ell+2L11+2Ke+Ke3+2Ke4 outside P_C. (4)

Each profile lies in that same full endpoint component: it is connected
inside its tile to its critical root. The root adjoins its producing
sources. Equation(4) is a necessary endpoint requirement, not a reserve
payment or an unrestricted density theorem.

## 4. Two genuine stop classes and one compensation ledger

Call a critical pair event eligible if its original owner is U10 or a
pair-type zero rotor. By the classification its unique original support
is w=(0,1). Its original owner supplies the anchor(0,0), and O supplies
the distinct anchor(-1,1). Mandatory retention therefore forces w into
the final original endpoint set P. There are at least three final
endpoints in Q. Let Jcrit count eligible events whose Q is nonfull.
Such Q has exactly3 endpoints of multiple original owners; its fourth
corner has two persistent endpoint neighbors and cannot be selected.
It contributes one actual L3 occurrence to H.

These nonfull Q are injective. Distinct pair owners would fill Q. For
the same owner, Section3 gives at most one critical event in Q.
They avoid ALL first/LONG stops by the accepted physical separation.
They also avoid the old passive-corner D and C0 stops: C0 has a positive
U pair, so a different owner; D has a phase10 irregular2P0T pair, while
the new U10 profile is regular2P1T. Different owners fill a coincident
tile; the same owner cannot have two different exact original profiles
in one fixed tile. Rotor versus U likewise distinguishes the owner.
Thus the actual simultaneous packing is

    D+C0+J01+J11+Jcrit <= H,
    B+J01+J11+Jcrit <= 2A+H.                     (5)

Now consider a critical triple-type zero rotor. In the normalized table
its paired regular singleton is at(1,2); its original supports are(0,2)
and(1,3). The original support(0,2) has the rotor anchor(1,2) and the
foreign O anchor(-1,2). As shown in Section2, a rotor requires k>=3,
so both anchors exist. Retention forces(0,2) into P. Consequently its
paired regular singleton is activated even if the critical triple tile
itself is not full.

Let Tcrit count critical rotor-triple events with nonfull Q. By the
definition in the exact reserve identity, each is an actual Z0
occurrence. Different such events have different original owner/triple
tiles by Section3; the original rotor triple/singleton pairing is
bijective. Hence

    Tcrit <= Z0.                                                (6)

Substitute(5)--(6) ONCE into the SAME exact identity
2R=A+U0+Z0+H, to obtain the compensation lemma

    B+J01+J11+Jcrit+Tcrit+U0 <= 2R+A.            (7)

The H and Z0 terms have been replaced by their jointly chosen actual
subfamilies, not counted a second time. This proves compensation for
these critical nonfull exits in arbitrary complete finite mixed fusions.
It does not say every critical event is a nonfull stop.

In a same-component AA census with H=Z0=0, Jcrit=Tcrit=0. Thus eligible
pair and rotor-triple critical receivers must be full. A need not vanish.
For counts outside that census use(5)--(7), without assuming saturation.

## 5. A complete four-source neutral terminal exit

There is an actual complete critical exit into U11, outside the previous
full U01 bar family. In a20 by30 grid take these four canonical U sources:

| Owner | (width,left,right) | Actual image of(r,c) |
|---|---|---|
| O | (26,12,4) | (r,c+1) |
| F | (10,4,4) | (c+1,r+3) |
| B | (6,4,4) | (c+11,7-r) |
| G | (6,4,4) | (c+1,12-r) |

Their original phases are01,11,01,11. O and B have the actual active/passive
neutral terminal contact(12,2),(12,3). Its first forced point is(11,3)
in F. Since O's incident height12 equals F's width10 plus2, this is the
critical branch and its second point is t=(2,8), the original G terminal.
Its actual receiving tile has

    P intersect Q={(2,8),(2,9)}, T intersect Q={(3,9)}.          (8)

The diagonal original G support(3,9) is retained, with sole occupied
neighbor(2,9). Thus this critical receiver is neutral2P1T, not full and
not an H or Z0 stop. This refutes extending the eligible-stop rule to
EVERY critical U terminal, or assuming every critical receiving tile has
at least three final endpoints. It does not refute(5)--(7), whose eligible
pair owners explicitly exclude U11, or the target allocation inequality.

For a direct finite certificate, the labelled original endpoints are:

| Owner | Rows | Columns |
|---|---|---|
| O | 0,1 | [2,27] |
| O | 2 through12 | 2 |
| O | 2 through4 | 27 |
| F | 2,11 | [3,7] |
| F | 3 through10 | 3,4 |
| B | 12,17 | [3,7] |
| B | 13 through16 | 6,7 |
| G | 2,7 | [8,12] |
| G | 3 through6 | 11,12 |

These sets are disjoint. Use the original canonical matching and support
formulas in CRITICAL_CLOSED_OWNER_COUNTEREXAMPLE.md under the four maps.
The mandatory retained support set has exactly the following28 points;
the right column lists its sole occupied neighbor in P union T:

| Support | Sole occupied neighbor |
|---|---|
| (0,1) | (0,2) |
| (0,28) | (0,27) |
| (2,1) | (2,2) |
| (2,28) | (2,27) |
| (3,6) | (2,6) |
| (3,9) | (2,9) |
| (3,26) | (3,27) |
| (4,1) | (4,2) |
| (4,28) | (4,27) |
| (5,27) | (4,27) |
| (6,1) | (6,2) |
| (6,9) | (7,9) |
| (7,7) | (7,8) |
| (8,1) | (8,2) |
| (8,8) | (7,8) |
| (8,10) | (7,10) |
| (8,12) | (7,12) |
| (10,1) | (10,2) |
| (10,6) | (11,6) |
| (11,8) | (11,7) |
| (12,1) | (12,2) |
| (13,2) | (12,2) |
| (13,4) | (12,4) |
| (16,4) | (17,4) |
| (17,2) | (17,3) |
| (18,3) | (17,3) |
| (18,5) | (17,5) |
| (18,7) | (17,7) |

Every omitted original support is an endpoint in the labelled table;
the verifier also reconstructs the new G matching/supports from the
independent canonical formulas. There are64 original matching edges and
128 endpoints. The objective is64+28=92, against half-area300, giving
positive slack208. The exact reserve census has A=Z0=0,U0=4,H=16,R=10.
No AA or near-extremal claim is made. Eight physical partition-preserving
images retain the critical terminal branch. This new finite certificate
does not replace the general proofs in Sections1--4.

## 6. What remains for the full allocation

The physical profile mass in(2)--(4) is original source mass, not fresh R.
Full2+2 critical receivers may have zero residual square credit, and a
filled zero-rotor triple cancels its activated singleton in the existing
identity. U11 terminals can have an unconsumed diagonal support. Original
full U01 bar returns remain possible. These full or neutral branches must
still be tied to the cap, singleton and marked-side reservation ledger to
prove unrestricted coefficient one. No better unrestricted5/6 bound or
grid triple equality is claimed by this note.

The Lean companion checks arbitrary-dimension U roles, exclusion of
positive owners, exact terminal endpoint/support profiles, the phase10
wall collision, same-owner terminal separation, complete rotor role
tables, profile-capacity and joint count/reserve arithmetic. Actual source
ownership, transport of coordinates, pairing to Z0 and the physical stop
separation are the written adapters above. Validation and independent
review are recorded separately; no execution or acceptance is inferred.

## 7. Validation and independent audit boundaries

All17 declarations in
[CriticalOwnerProfiles.lean](../formal/SubQuorum/CriticalOwnerProfiles.lean)
compile with Lean4.33.0 on the user-selected local Mac. The scoped audit
finds no sorry, native_decide or additional axioms; six fixed-role statements
are axioms-free. The remaining statements use only propext, Quot.sound
and Classical.choice. See the
[formal receipt](../output/critical-owner-profiles-formal-check.json)
for the exact execution and adapter scope.

The [checker](../develop/check_critical_owner_profiles.py) passes14,400
anchored U images, the16 exact rotor roots and216 complete feasible
physical images. Those complete images contain96 critical events
(88 original full profiles and8 U11 pairs) and104 ordinary receivers.
There are no complete shared-critical-tile, eligible H-stop, rotor Z0-stop
or AA witnesses in this batch. The general claims about these branches
are proved in Sections1--4, not inferred from zero-coverage samples.
The four-source certificate has its exact matching/support census and
all retained-support anchors in the
[control record](../output/critical-owner-profiles.json).

Independent Oracle audit61a86e8f-57df-4407-9672-2a236de66dca completed
ACCEPT at11:12:31 UTC on20 October2026, observed gpt_6/pro. Its original
stream ended0 with DONE and exactly matches the terminal response.
The [receipt](../output/critical-owner-profiles-review.json) and
[complete response](../output/critical-owner-profiles-review-response.txt)
cover Sections1--4 and the initial15-declaration source snapshot. The
review does not certify execution or cover the later Section5 certificate
and two additional rotor statements. These have a distinct live audit,
c2e80e20-cd66-4f49-84f8-c5413e10a5b9; its verdict must be recorded separately.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
