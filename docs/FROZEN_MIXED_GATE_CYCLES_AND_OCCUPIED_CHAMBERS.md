# Frozen mixed-gate cycles and occupied-shadow chambers

25 October 2026. Haobo Ma and Wenlin Zhang. Isolated research branch.

An ACTUAL completely frozen board has four different original alpha sources
in an even source/gate cycle and four different mixed gate owners. Thus the
necessary opposite-terminal color condition from
[joint gate/resource cuts](JOINT_GATE_RESOURCE_CUTS.md) cannot be strengthened
to a blanket exclusion of such cycles by complete freezing. This settles the
physical existence of the cycle core, not of the full five-source shared-
resource obstruction in that note.

We reconstruct the original resources, give exact local and complete-network
formulas for every interval-availability subset, and identify which existing
beta paths repair the local defect. An arbitrary-width thin chamber theorem
also explains why the first compact embedding attempts must change gate
types to beta. No universal grid bound or improvement of 5/6 is obtained. All availability
sets below are subsets of the established eligible, unmarked original
resource set; boundary marks remain reserved.

## 1. Actual frozen cycle, with an inductive certificate

Coordinates are zero-based in a 28x24 rectangle. Use the permanent
[actual fixture](../develop/fixtures/frozen_all_mixed_gate_cycle.json):
49 selected sites,154 actual matching edges,308 matching endpoints. Every
selected site has at most one occupied neighbour, every matching edge is a
grid edge, and no endpoint is repeated. The first column is blank and the
last column is blank, so the standard admissible band boundary is retained.

Let p* denote the actual mate. The fixture provides a rank and two distinct
retained neighbours for EVERY endpoint v. A retained neighbour w is selected
or has rank(p*(w))<rank(v). Induction on rank proves complete freezing.
The independent checker reconstructs the process, and the accompanying
Lean file checks the concrete certificate using the actual inductive
freezing relation. The search procedure is not part of this proof.

There are exactly four original alpha owners, with endpoint pairs:

| Source | Actual TP terminals |
| --- | --- |
| A (top) | (5,6),(5,17) |
| B (right) | (5,19),(24,19) |
| C (bottom) | (24,6),(24,17) |
| D (left) | (5,4),(24,4) |

The four different mixed owners have BP/TP pairs:

| Gate | BP entrance | TP exit |
| --- | --- | --- |
| g0 | (5,5) | (14,11) |
| g1 | (5,18) | (12,14) |
| g2 | (24,18) | (18,15) |
| g3 | (24,5) | (19,11) |

All eight M/PP strands are pairwise endpoint-disjoint. Their endpoint-path
lengths are26,20,26,20 for the alphas and22,24,20,22 for the mixed gates.
The original actual horizontal contacts give the cycle

    A -> g0,g1; B -> g1,g2; C -> g2,g3; D -> g3,g0.

They use the two different TP tips of each source. Gate BP chessboard colors
alternate, as required by the general strand parity theorem. The paths bend
through occupied adjacent bands; they are original owners, not virtual ones
created by cancellation. There are also six whole beta paths elsewhere in
the complete original network. They must not be discarded when testing the
global allocation.

This establishes that **complete freezing does not exclude an all-mixed
four-source cycle, even with different source ports at every incidence**.
The cycle alone does not impose the five-source example's resource supports.
We do not claim that entire abstract obstruction is physically realized.

## 2. Exact local resource graph on the original cycle

For this section ONLY, restrict the allocation owners to the four alpha and
four mixed owners above, keeping ALL original links between them. This is
an explicitly local rule, not the complete board. Use the original whole-
support adapter; no new support incidences are invented. Take the union of
the gates' original intervals, excluding those also supported by any of the
four alpha owners. This leaves16 original units. The sources therefore have
empty interval support in this declared pool.

The gate incidences of these16 units are exactly:

| Supporting gates among the four | Original units (band,column) | Count |
| --- | --- | ---: |
| g0,g1 | (5,10),(5,12),(6,12) | 3 |
| g0,g2 | (7,13),(7,15) | 2 |
| g2,g3 | (9,13),(9,14) | 2 |
| g1 only | (6,15),(6,16) | 2 |
| g3 only | (9,8..10),(10,12..15) | 7 |

Each is the original singleton interval at the listed column. A unit
supported by only one of these gates may additionally support an omitted
neutral owner; 'only' in this table is relative to the declared cycle. It
is not a claim of whole-network private ownership. The two-gate shared
units have exactly those original owners, since the physical adapter has
at most two supporting owners per interval.

For ANY available subset Q of these16 original units, form a multigraph R_Q
on the four gates: each shared unit is an edge, each single-gate unit a loop.
Keep parallel units distinct. Let t(R_Q) count tree components, including
isolated gate vertices, and regard loop components as non-trees.

**Theorem 1 (all original local-availability subsets).**

    V_local(Q) = 4-t(R_Q),       c_local(Q) = V_local(Q).       (1)

**Proof.** The cycle has a fixed source-to-gate bijection

    A->g0, B->g1, C->g2, D->g3,

witnessed respectively by the actual links
(5,6)->(5,5), (5,19)->(5,18), (24,17)->(24,18), (24,4)->(24,5).
Hence EVERY subset of gates can be entered simultaneously by different
sources. Any matching of gate owners to distinct original units lifts by
restricting this fixed bijection. Conversely every local payment must enter
one gate and use one original unit; the unit-capacity entrances give the
matching upper bound. Thus the value is precisely the gate/unit matching
rank. The tree rank lemma from the preceding note, applied to R_Q, says this
rank is4-t(R_Q): root each tree, and use a directed unicyclic spanning
subgraph in every non-tree component. All routes use exactly one actual
link, and there is no source direct support or gate-to-gate continuation
in this local rule. Thus the exact minimum cost equals the payment. QED.

This proof works for any source/gate interface admitting a fixed bijection
and simultaneous physical lift, with arbitrary two-owner original resource
incidences. It is not an inference from finitely many tested Q.

### An actual tree deficit and competing repairs

Let

    x=(band5,col10), y=(band7,col13), z=(band9,col13).

These three units form the resource tree g1--g0--g2--g3. With exactly them
available, the local optimum is V3/c3. Releasing ANY one of

    x'=(5,12), y'=(7,15), z'=(9,14), p=(6,15), q=(9,8)

makes the connected resource graph non-tree: the first three create a
parallel edge, the last two a loop. Thus ANY nonempty set of these releases
gives V4/c4. Several such releases do not repair several different missing
sources: there is only one missing payment in this connected block.

For any number n of separated copies, keep x,y,z available in each. If E_r
is the copy set with repair r released, then exactly

    V_local = 3n + |union_r E_r|,       c_local = V_local.      (2)

It is incorrect to replace the union by sum_r |E_r|. Different interval
identities can be released in the same block and still repair the same
one-source deficit. For a literal grid family, place copy i at row offset
32i+2 in a32n-by24 board. The two blank rows on each side preserve band
phase and separate all occupied adjacency, support and actual links.
Replay each copy's strict freezing witnesses. Formula (2) then follows
by additivity of disjoint owner and original-resource identities. This is separate from the requirement to use each
interval identity only once.

## 3. Complete original network: exact value and link cost for every subset

Now retain EVERY original owner, link, whole beta and original interval.
Only interval availability Q may vary, over the ENTIRE original unit set.
No original owner or beta is removed. Define the following disjoint classes:

- L: D's11 direct units, at band7 columns5..7,9,10 and band8 columns5,7..11.
- B0: C's6 direct units, at band12 columns7,12..16.
- G: the11 units supported by g2 or g3: band7 columns13,15; band9
  columns8..10,13,14; band10 columns12..15.

These are different original identities, and L,B0,G are pairwise disjoint.
Top source A and right source B have EMPTY whole interval support. Set

    ell(Q)=0 if Q meets L, else1;
    b(Q)=0 if Q meets bottom-direct class B0,
         1 if it misses B0 but meets G,
         2 otherwise.

**Theorem 2 (complete network, arbitrary original Q).** In both ordinary
and full fork models,

    V_full(Q)=4,        c_full(Q)=2+ell(Q)+b(Q).              (3)

**Lower bound on cost.** Top and right sources have no original support,
so each paid route must contain at least one actual link. The left source
requires at least one unless Q meets L. The bottom source has only the two
original first destinations g2,g3. Without a direct bottom unit it needs at
least one link; without a unit supported by those two gates it needs at
least two. Beta forks cannot evade these source-specific first-link lower
bounds. In the exact primitive normal form the path link costs sum over
sources, even when two arms share a beta body. Thus (3)'s cost is a lower
bound at full value4.

**Simultaneous upper witness.** Use these fixed distinct whole-beta options:

    top:   (5,17)->(5,16),
    right: (5,19)->(5,20),
    left:  (5,4)->(5,3),
    bottom fallback:
           (24,17)->(24,18), (18,15)->(18,16).

The bottom fallback enters g2 and then its TP exits to a fourth, different
whole beta. The four beta owners and the four sources are all distinct,
and none of the first three beta paths uses g2/g3. This pays all four with
5 links even when no interval is available. Replace the left fallback by
its direct L unit whenever available. Independently replace the bottom
fallback by a direct B0 unit, or otherwise by a one-link g2/g3 payment to a
G unit whenever available. The disjoint classes L,B0,G prevent repeated
original-unit use, and the displayed owner disjointness prevents a BP or
mixed conflict. The first two beta paths remain unchanged. This attains
exactly the right side of (3) with ordinary stems; hence ordinary/full
values and minimum costs coincide here. QED. The same separated-copy placement gives
V=4n and c=sum_i(2+ell_i+b_i) for arbitrary original interval availability
across the copies; blank buffer-band units are unreachable and give no credit.

Concrete distinctions are:

| Available original intervals | Local8-owner V/c | Complete original V/c |
| --- | --- | --- |
| none | 0/0 | 4/5 |
| x,y,z | 3/3 | 4/4 |
| x,y,z,x' | 4/4 | 4/4 |
| all original units | 4/4 (using its16-unit pool) | 4/2 |

Thus the local tree deficit is repaired by existing peripheral beta routes
even BEFORE releasing another interval. The actual frozen cycle refutes a
geometric cycle-exclusion rule, not the unrestricted compensation target.
It also shows why importing the abstract local interface while deleting its
original peripheral beta exits is not a proof about the complete board.

## 4. Why the narrow occupied chamber changes gate types

There is nevertheless an all-width geometric exclusion for the first thin
embedding. Let l>=2, r-l odd and at least5. Put four gate BPs at
(5,l),(5,r),(12,r),(12,l), with their band partners permanently blank. Fix
four alpha paths as in the preceding frame: straight vertical side strands
at columns l-1,r+1 from rows5 through12; top and bottom zigzag U strands
with TP pairs (5,l+1)/(5,r-1) and (12,l+1)/(12,r-1). Their actual matching
and PP partners are given by scaffold(12,l,r) in the solver-free checker.
The selected TP band partners are retained. Allow arbitrary feasible
additions/rematching away from those fixed source edges, including arbitrary
exterior geometry; the four blank gate partners must remain blank.

Let F be the fixed source endpoints and define the chamber

    C = { (s,c): c in {l,r}, 5<=s<=12 }
        union { (s,c): s in {8,9}, l<=c<=r }.

**Theorem 3 (occupied-shadow chamber exclusion).** Every original path
through one of the four gate BPs is beta in ANY such feasible extension.
In particular none can be mixed. At least two distinct whole beta owners
contain the four distinct gates, but two gates in one beta supply only ONE
whole-beta resource.

**Proof, actual-matching closure.** F and C are disjoint. Every physical
neighbour of C outside C is in F or is one of the four permanently blank
gate partners. Each point of F has its fixed actual mate in F. An actual
matching edge from C to F would give the wall endpoint two mates. An edge
to a blank site is impossible. Hence actual matching is closed in C.
Every occupied PP band partner of a C endpoint is also in C: gate partners
are blank, and every nongate C band pair is internal.

**Proof, exclusion of TP.** A gate's partner is blank. For a nongate C
endpoint v, let u be its band partner. If u were selected, it would see v
and a second, distinct, occupied wall point: at the chamber rails use the
adjacent side-wall endpoint; at an interior row8 point u is in row9 and
has its bottom wall neighbour in row10; at an interior row9 point u is in
row8 and has its top wall neighbour in row7. Feasibility forbids two
occupied neighbours at a selection. Thus no C endpoint is TP.

The finite actual M/PP component from a gate BP stays in C. It begins at
a degree-one terminal; matching/PP alternation cannot enter a disjoint
cycle or branch. It therefore ends at another terminal. Since there is no
TP in C, the other terminal is BP. This is one original beta owner. A beta
has only two terminals, proving the count of at least two owners for four
gates. QED.

This proof is independent of freezing and independent of any finite SAT
search. Its width is arbitrary. It requires the fixed source wall and blank
partners, not just a visual rectangle. In the larger actual construction,
selected band partners can lie deeper inside the chamber without seeing
a second occupied wall point; the shadow hypothesis fails, and four mixed
paths do occur. A separate20x16 frozen control in the fixture directory
also shows the intermediate behaviour: one gate is mixed, two gates share
a beta and another gate belongs to a second beta.

## 5. Reproduction, formal scope and remaining work

Run:

    python3 develop/check_frozen_mixed_gate_cycle.py \
      --output output/frozen-mixed-gate-cycle-validation.json
    python3 develop/check_occupied_cycle_chambers.py \
      --output output/occupied-cycle-chamber-validation.json

The main verifier reconstructs feasibility, all308endpoint strict freezing,
the four source and gate owners, all eight real entry links, all original
support identities, the local resource multigraph and every peripheral
beta route used by (3). It compares local formulas with independent
primitive packing and tests complete-network availability models against
the existing exact fork flow and independent ordinary/full primitive packs.
The general all-subset and all-copy statements have proofs above. The saved
checks pass373 local resource models/independent packs,5,486 complete original
availability models with224 independent ordinary/full packs,32 overlapping
repair controls and8 literal frozen separated-copy models. The chamber
checks pass21 width controls/1,344 coordinate boundary obligations and
the separate128-endpoint wider strict certificate.

The chamber verifier checks the coordinate boundary and shadow obligations
on an all-width family; the argument in Theorem3 proves arbitrary width,
not finite width tests. Its wider control has its own strict certificate.
The optional Z3 discovery script is separate and not imported by either
verifier. Its bounded UNSAT results for smaller boards, and its earlier
large-board timeout, prove no general impossibility. The eventual frozen
large-board witness is independently certified.

Lean scopes are explicit: OccupiedCycleChambers.lean proves general shadow
exclusion, actual-matching chamber closure and arbitrary-length actual
component closure/no-TP consequences. FrozenMixedGateCycle.lean checks the
concrete feasible board, its inductive complete freezing, all eight disjoint
original strands and all eight actual cycle contacts. The all-availability
resource graph/full-network formulas, all-copy count and full geometric
coordinate adapter are written/Python, not end-to-end Lean flow semantics.
All11 audited declarations pass on local Lean4.33.0, using only propext
and Quot.sound, with no sorry/native execution. Concrete preflight:16GiB,
49% system-wide free memory, no actual lean/lake process under the comm-
basename check, concurrency1. No new external review is claimed.

What remains is the FULL joint geometric problem: can the five-source
shared-resource obstruction occur without compensating original peripheral
beta/interval exits? The cycle core itself is now realized and cannot be
excluded. General sharing before/after gates and reachable beta forks still
require the complete resource-cut model. Universal compensation and5/6
remain open; the submitted manuscript is unchanged.

**Peripheral-repair continuation:** [cyclic beta escape cuts](CYCLIC_BETA_ESCAPE_CUTS.md)
proves the exact tree/gap Hall condition and pruning to the minimum t beta
uses for cyclic interfaces. On this actual board two DIFFERENT peripheral
betas can still give only one additional payment in a declared original
owner interface; another beta permits a different successful pair. The
complete original network continues to pay all four.
