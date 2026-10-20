# Exact geometric event reserve and zero-reserve saturation

20 October 2026. In the complete fixed-source model of
ACTIVATED_SINGLETON_FLOW_CANCELLATION.md, the event reserve is exactly a
nonnegative sum of seven geometric counts. This refines the universal
reserve inequality to an identity and identifies the precise saturation
required by any single-positive-source failure of the joint allocation.
It does not establish that a saturated bad-gate fusion exists or is impossible.

## 1. Model, definitions and theorem

Retain every established constructor assumption: finitely many complete U
and rotor sources; disjoint original endpoint sets; final P and M equal
their original unions; every original support outside P remains in T;
every final selected vertex has at most one occupied neighbor. All allowed
dimensions, independent heights, phases and square-lattice isometries remain
permitted. Original source ownership is never changed by fusion. Work on
the aligned two-by-two tiles meeting original endpoints. Original support
in a tile means support in that tile, even if a foreign endpoint consumes it.

Use the established original profile catalogue: regular 1P2T, 2P1T,
3P0T, 4P0T; irregular 1P1T and 2P0T. Each endpoint profile is connected.
The negative sign does not make a 2P1T or 3P0T profile irregular. Every
irregular profile belongs to a negative source. A positive U has two
regular terminal singleton occurrences. Triple-bearing zero rotors have
two regular singleton occurrences, bijectively paired to their two triples;
the other zero-rotor type has neither. No other source contributes a
regular singleton. These catalogue facts and the rotor support bridge
are proved in the preceding notes and are inputs here.

Let R=S+C-K be event reserve, not rotor count; N is the number of positive
sources and G the number of marked positive sides. Keep the exact half-slot
identity and the source ledger:

    2R = 2B11-BU-BR+Lambda,
    sigma >= N+R-G,                                  (1)
    Lambda = sum_Q [i_Q+b_Q-2(k_Q-c_Q)].

Here i_Q counts endpoints in original irregular profiles, k_Q counts their
events, c_Q is actual full-tile credit after regular events have been paid,
and b_Q is one precisely for a full 3+1 tile with an irregular singleton.
BU and BR count those full 3+1 contacts according to U/zero-rotor triple
ownership. Define seven nonnegative GEOMETRIC counts:

- A: activated original positive regular singleton occurrences. Activation
  means at least one of its two original intratile supports belongs to P.
- U0: original phase11 U triples whose tile is not full in final P.
- Z0: activated original zero-rotor singleton occurrences whose uniquely
  paired original triple tile is not full in final P.
- L1: nonfull tiles with exactly one endpoint and original profile 1P1T.
- L2bar: nonfull tiles with exactly two endpoints, both in one 2P0T profile.
- L2mutual: nonfull tiles with two 1P1T endpoint owners, each having the
  other endpoint as its original support. Equivalently, both irregular
  events are inactive. This excludes the adjacent two-singleton case with
  one event.
- L3: nonfull tiles with exactly three endpoints and more than one
  original endpoint owner.

Write H=L1+2L2bar+2L2mutual+L3. Then the exact reserve theorem is

    2R = A+U0+Z0+H.                                  (2)

Each source occurrence is counted once, and each nonfull tile has exactly
one of the four listed defect classes or contributes zero. U0 and Z0 are
different occurrence classes even when their geometric tiles coincide;
the derivation below proves their simultaneous contributions rather than
assuming that different labels alone create extra capacity.

## 2. The exact local defect table

In a tile let d count activated regular singleton occurrences and let f
indicate a full 3+1 tile whose singleton is regular. Put

    h_Q = Lambda_Q+f_Q-d_Q.

We prove the following table by exhausting endpoint partitions of a square.
The four nonfull defect indicators are denoted l1, l2bar, l2mutual, l3.

    h_Q = l1+2l2bar+2l2mutual+l3.                    (3)

The proof uses the finite set of possible profiles, so it applies to every
source size and every number of sources. A bounded experiment is not needed
for any case below. In a nonfull tile c_Q=b_Q=f_Q=0: there is no new full
tile, and regular events cannot create negative residual credit.

**Zero or one endpoint.** An empty tile contributes zero. A sole regular
singleton is unactivated and contributes zero. A sole irregular singleton
has i=1,k=d=0, so contributes one, exactly l1.

**Two endpoints, one owner.** An original 2P0T pair has i=2,k=d=0,
and contributes two. A 2P1T pair contributes zero. Endpoints of a single
profile cannot be diagonal because profiles are connected.

**Two endpoints, two owners.** They cannot be diagonal: every original
singleton has an adjacent support, which could not be consumed by the
other endpoint and would have two endpoint neighbors. For adjacent
endpoints p,q, let r,s be their respective other neighbors in the tile;
r and s are adjacent. Retaining both r and s is impossible, since each
would have both an endpoint neighbor and a selected neighbor.

If one singleton is regular, the other must be irregular with its support
at the regular endpoint. Otherwise both r,s are retained. Exactly the
regular singleton is activated, while i=1,k=0. Thus Lambda=d=1 and h=0.
Two regular singletons are impossible for the same retained-support reason.
For two irregular singletons, at least one consumes the other endpoint
as support. If both do, k=0,i=2 and h=2; this is exactly l2mutual.
If exactly one does, the other fires its one event, so k=1,i=2 and h=0.
No other two-owner case exists.

**Three endpoints, one owner.** The original triple has no support or
event; it contributes zero.

**Three endpoints, a pair and a singleton.** Denote the pair by p,q,
the singleton by r adjacent to q, and the missing corner by s. The corner
s neighbors two endpoints and therefore cannot retain any original
support. If the pair is 2P0T, its event q toward r fires. The singleton
must be irregular with support q: a regular singleton would retain s.
Hence i=3,k=1,d=0 and h=1. If the pair is 2P1T, its support must be r,
since support s cannot be retained. The singleton is again irregular
with support q, and no irregular event fires. Thus i=1,k=d=0 and h=1.

**Three singleton owners.** The endpoints form an L. Each leaf's support
must be the elbow, since the missing corner cannot retain support. Both
leaves are irregular. If the elbow is regular, it is activated and
i=2,k=0,d=1, giving h=1. If the elbow is irregular, its support is one
leaf and its event toward the other leaf fires: i=3,k=1,d=0, again h=1.
Thus every mixed nonfull triple contributes exactly l3=1.

**Four endpoints.** The original-owner partitions are 4, 3+1, 2+2,
2+1+1 and 1+1+1+1. The sole-owner case has all counts zero. For 3+1
with regular singleton, Lambda=0,d=f=1. For 3+1 with irregular singleton,
i=b=k=1,c=d=f=0, hence Lambda=0. For 2+2 each 2P0T pair has two
irregular events and contributes two irregular endpoints; each 2P1T pair
has one regular event. If t is the number of irregular pairs, then
i=2t,k=2t,c=t, and Lambda=d=f=0. For 2+1+1 let t indicate an irregular
pair and j count irregular singletons. The regular pair, if present,
has one regular event. Thus i=2t+j,k=2t+j,c=1+t and
Lambda=2-j=d; f=0. For four singletons with j irregular owners,
i=k=j,c=2, and Lambda=4-j=d. In every full case h=0.
This proves (3), including cases where multiple original sources merge.

## 3. Summation and cancellation

Let DR count activated zero-rotor singletons. All regular singleton
occurrences are positive terminals or zero-rotor singletons, so

    D = A+DR.

The full 3+1 regular-singleton contacts split as F=FU+FR by U/rotor
triple ownership. Each phase11 U has exactly two triples, so directly
counting unfilled triples gives

    U0 = 2B11-BU-FU.                                (4)

The zero-rotor support bridge forces the paired singleton to activate
whenever its triple is filled, irrespective of the missing corner's
foreign regular/irregular ownership. Since the triple/singleton pairing
is bijective, direct counting gives

    Z0 = DR-BR-FR.                                  (5)

Sum (3) over physical tiles:

    H = Lambda+FU+FR-A-DR.                          (6)

Substitute (4)--(6):

    A+U0+Z0+H
      = A+(2B11-BU-FU)+(DR-BR-FR)
        +(Lambda+FU+FR-A-DR)
      = 2B11-BU-BR+Lambda
      = 2R.

No choice of routing or termination is involved. The local defect sum is
computed from actual residual c_Q after regular events; C is not spent
again. Full-tile forwarding terms cancel exactly. This proves (2).

## 4. Consequences for the unresolved joint allocation

All seven counts are nonnegative integers. Therefore

    R=0 iff A=U0=Z0=L1=L2bar=L2mutual=L3=0.          (7)

The sum A+U0+Z0+L1+L3 is even, since 2R and the other two terms are even.
The ledger consequently has the exact reserve lower bound

    sigma >= N-G+L2bar+L2mutual
                     +(A+U0+Z0+L1+L3)/2.           (8)

The sufficient joint allocation is EQUIVALENT to

    2G <= 2N+A+U0+Z0+H.                            (9)

Failure of this allocation is equivalent to

    A+U0+Z0+H <= 2G-2N-2,                          (10)

using integrality of N+R-G. These equivalences concern the source ledger's
allocation; failure does not imply failure of actual ambient sigma or of
the grid target, since (1) is a lower bound for sigma.

Every blank-gate tile from the established canonical assignment has
d=f=0 and Lambda>=1, and distinct marked sides have distinct assigned
tiles. By (3), its defect h_Q is at least one. Thus Gb<=H, and (2) also
gives 2R>=A+Gb+U0+Z0 without a second use of blank-gate capacity.

For N=1, any failure of the joint allocation requires G=2,R=0, because
G<=2N and R>=0. Equation (7) forces all seven counts to vanish. In
particular every original phase11 U triple must be full, every activated
zero-rotor singleton must have its paired triple full, and no mixed
nonfull three-endpoint tile is allowed. Also Gb=0. The occupied-gate
activation theorem excludes every phase10 owner, leaving two occupied,
unactivated marks with phase01 upper-corner or phase11 terminal owners.
This is a necessary saturated obstruction, not a realized counterexample.

When N=1 and any one of the seven defects occurs, the even positive sum
in (2) is at least two, so R>=1 and N+R-G>=0. This conditional statement
holds for arbitrary permitted dimensions, unlike a width-restricted
classification. Whether finite geometry forces such a defect for every
remaining two-bad-gate fusion is still open. More generally, proving (9)
requires a common count against these actual unused capacities; an
occurrence must not be reassigned once it has already paid a gate.

## 5. Validation boundaries

develop/check_exact_event_reserve.py checks the exact local table on all
434 feasible profile packings and counts U0,Z0 and the four physical
defects independently on640 complete fusion images. Its physical zero-
reserve controls are zero-rotor images without marks; they cannot prove
the saturated bad-gate obstruction impossible. Finite controls complement
Sections2--3 and do not replace the all-parameter proof.

formal/SubQuorum/ExactEventReserve.lean checks the complete local table,
nonnegative defect weights, conditional global cancellation, parity,
zero-reserve equivalence, joint allocation equivalence and single-positive
consequences. Original source-to-profile completeness, rotor pairing,
global incidence identities and physical-tile summation remain written.
It is not an end-to-end Lean theorem about arbitrary source fusions.
All11 declarations compile with Lean4.33.0 on the user-selected local Mac,
with sequential dependency/source/audit runs and no sorryAx/native_decide.
Individual axiom audits pass. See output/exact-event-reserve-formal-check.json
and output/exact-event-reserve-controls.json for execution and control scope.
Of the640 physical images,24 have zero reserve; all24 are unmarked rotor
fixtures. A new independent review is on original stream67887, without an
observed verdict. The earlier a6ac6319 ACCEPT covers the preceding
singleton/gate pipeline, not this new exact identity.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
