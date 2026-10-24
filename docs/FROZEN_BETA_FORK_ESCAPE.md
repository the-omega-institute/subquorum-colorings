# Frozen beta forks: injective escape sites and a sealed-cycle obstruction

25 October 2026. Continuation of
[LIVE_GATE_CERTIFICATE_TRADEOFF.md](LIVE_GATE_CERTIFICATE_TRADEOFF.md).

A frozen horizontal TP--BP--TP fork with an alpha on one side forces an
occupied diagonal site and an outward actual matching edge on the alpha's
other side. These escape **sites are injective**. However, an explicit frozen
12x14 example puts the escape in a pure two-point PP/M cycle. Adding one
vertical matching edge seals its only adjacent empty column while preserving
freezing. Thus the forced site need supply neither an open beta/mixed owner
nor an adjacent original interval. This refutes automatic local resource
credit, not the global compensation inequality. No improvement of 5/6 follows.

## 1. Definitions and hypotheses

Work in a finite rectangular nearest-neighbor grid. T is the selected set,
P the endpoints of an actual matching M, and B the remaining vertices. The
sets are disjoint; each T has at most one occupied neighbor in T union P.
Fix aligned two-row bands. Within a band a column is TP, BP, PP or BB; the
P in TP or BP is an original strand tip. Original strands are components of
actual matching edges together with the vertical PP partner edges in the
bands. An alpha has two TP tips, a beta two BP tips, and a mixed strand one
of each; a component with no tips is a pure cycle. Parallel actual/PP edges
can give a two-vertex cycle.

Assume complete freezing in the following certificate sense: give every P a
nonnegative integer rank so that it has two distinct nonmate neighbors each
of which is either T or a P whose actual mate has strictly smaller rank.
Such a neighbor is called retained at that endpoint. T is retained without
a rank condition. This is precisely the strict layer certificate checked by
the repository's frozen-endpoint closure. The conclusions below hold for
any such strict certificate, not just the earliest closure layers.

Normalize by reflection so a=(r,c) is in the lower row of its band and its
across-boundary neighbor is a*=(r+1,c). Write s=+1 or -1 and suppose

    m=(r,c-2s), b=(r,c-s), a=(r,c), n=(r,c+s).

Here a is an original TP of an alpha A, b an original BP of a beta,
and m is any original TP. No assumption on m's owner is needed.
All references to intervals below mean original, unmarked whole-support
intervals, with their coordinate identities retained.

## 2. Escape and outward-mate lemma

**Lemma.** The vertex n is not T. If n is B, its band partner is B, giving
a BB port. If n is P, it is BP and the following conclusions hold:

1. a's actual mate is a*, and b's actual mate is b*=(r+1,c-s).
2. Both z=(r+1,c+s) and h=(r+2,c) are retained at a*.
3. z is P, is not an original TP, and
   rank(mate(z)) < rank(a*) < rank(b).
4. n's actual mate is (r,c+2s), and rank(a*) < rank(n).

**Proof.** The T partner of a already sees a; its other neighbors, including
n's band partner, are B. The blank partner of b and the two horizontal TP
neighbors leave only b* as a possible actual mate of b. Similarly a cannot
match a horizontal TP/BP tip of a different original strand, and cannot
match its T partner, so its mate is a*. At b, the only nonmate occupied
neighbors are a and m. Both must be retained. In particular
rank(a*)<rank(b).

The three possible nonmate neighbors of a* are b*, z and h. Retaining b*
would require rank(b)<rank(a*), a contradiction. Therefore z and h must
both be retained. If n were T, it would see a and z, violating feasibility.
If n is B, its already blank band partner gives the claimed BB column.
Otherwise n is P and its blank band partner makes it BP. Now z cannot be T,
since it sees the occupied a* and n. Thus z is P and its retention gives
the first strict rank inequality in (3).

The actual mate of n cannot be a or its blank band partner. If it were z,
retaining z at a* would require rank(n)<rank(a*). At n, the only two
nonmate occupied candidates would be a and its outward horizontal neighbor;
retaining a requires rank(a*)<rank(n). This is impossible. Thus n matches
horizontally outward. Its only possible nonmate occupied neighbors are a
and z; both are retained, proving (4). Finally z cannot have a T partner
inside its band: that partner would see both z and the occupied h. This
proves that z is not TP. Missing boundary vertices count as blank; the
forced occupied sites in particular establish that those coordinates are
inside the board. QED.

**Short-alpha consequence.** If the entire original alpha A has only two
P vertices, a* is its other TP and h is T. A T at z's band partner would
see z and h, and a P there would give h two occupied neighbors. Therefore
z's band partner is blank and z is BP. It is adjacent to A's opposite TP,
so the short alpha has an opposite-end BP bypass. Its owner might be an
unproductive mixed strand; this alone does not prove an unused payment.

## 3. No duplication of escape sites

**Lemma (site injection).** Distinct missing-port motifs (a,b,m,n as above,
with n P) have distinct z.

**Proof.** In the fixed band frame let outRow(r)=r-1 for even r and r+1 for
odd r. This is an involution, so equal escape rows imply equal source rows.
Equal escape columns give c+s=d+t for directions s,t in {+1,-1}. Equal
directions give the same source and the same motif. Opposite directions
give d=c+2s. The forced outward mate of n in the first motif is then the
second motif's alpha tip. But that alpha tip already has its vertical
actual mate. Matching uniqueness gives a contradiction. QED.

This is an injection into actual P **vertices**, not into original open
owners, distinct intervals, or unused payment units.

**Lemma (two-point cycle ownership).** If both vertices of a pure two-point
PP/M cycle occur as escape sites, their source alphas have the same owner.
Consequently such a cycle is charged by at most one distinct source alpha.

**Proof.** Translate the cycle to z0=(0,0), z1=(1,0), in one band. Its actual
edge is also its PP edge. The sources of the two motifs must lie in rows -1
and 2. Write their directions s0,s1; their source columns are -s0,-s1.
If s0=s1, their actual mates (0,-s0),(1,-s0) form a PP column. This joins
the two sources in the same original strand.

If the directions are opposite, reflect horizontally to take s0=+1 and
s1=-1. The lower source is a1=(2,1), its actual mate (1,1), and its forced
inward occupied neighbor is v=(0,1). v is P: it cannot be T next to both
the cycle vertex (0,0) and the occupied (1,1). Its PP partner (1,1) puts
v in the lower source's alpha. Examine the four possible actual mates of v.
The left neighbor (0,0) is already matched inside the cycle; the lower
neighbor (1,1) is already matched to a1. The upper neighbor (-1,1) is the
upper motif's forced outward mate and is already matched to (-1,0).
The remaining neighbor (0,2) lies opposite the lower beta's actual mate
(1,2). If (0,2) is T, it sees both v and (1,2), which is infeasible. If it
is B it cannot match v. If it is P, its PP edge to (1,2) puts it in that
original beta, so matching it to v would identify the alpha and beta,
contradicting their original distinct kinds. All four choices fail. Thus
the opposite-direction case is impossible. QED.

This upper bound makes no assertion that double-ended charging is realizable.
Exploratory unsatisfiable solver searches are not used in either proof.
Longer cycles and routing from them remain separate questions.

## 4. A fully frozen escape cycle, and its PP plug

The complete T coordinates, actual matching and strict freezing layers are
in [the fixture](../develop/fixtures/frozen_beta_fork_escape.json). Coordinates
are zero-based. For readability the raw occupied pattern is below; dots
are B. The fixture specifies which adjacent P vertices are actually matched.

```text
 0 ..............
 1 ....T....T.T..
 2 ....T..T.PPPT.
 3 ......TP.PPP..
 4 ...T.T.PPPPP..
 5 .TPPPPPPPPPP..
 6 ..T.PPP.PPPPT.
 7 ....PPP.PPPP..
 8 ....PPPPPP.PT.
 9 ..TPPPPPPP.T..
10 ...T.T.T.T....
11 ..............
```

There are 19 T and 50 P, with 25 actual matching edges. The open strands
have tips

- alpha: (5,5), (8,11);
- beta: (5,4), (9,3);
- mixed: (3,7), (5,6);
- mixed: (5,3), (5,2).

There are also five pure cycles. Take a=(5,5), b=(5,4), m=(5,3),
n=(5,6). Here n actually matches (5,7), while the forced escape z=(6,6)
belongs to the pure two-point cycle {(6,6),(7,6)}. Earliest closure ranks are
12 at mate(z), 13 at a*, and 14 at both b and n. In particular the rank
inequalities are realized by an actual completely frozen matching.

Now add the actual edge {(6,7),(7,7)}. This does not introduce any T
adjacency. Every old freezing witness remains valid; after all old endpoints
freeze, the two new endpoints freeze using their old horizontal neighbors.
This gives a strict certificate for 52 P and six pure cycles, with precisely
the same four open strands and four TP--BP candidate links. At the escape
cycle, columns 5 and 7 in both rows 6 and 7 are now P. Thus there is **no
adjacent endpoint-free gap** on either side.

The plug deletes exactly the unmarked original singleton interval
(band=3, first=7, last=7): 28 original unmarked intervals become 27. All other
original interval coordinate identities survive. The alpha's whole support
changes from {(2,12,12),(3,7,7),(4,10,10)} to
{(2,12,12),(4,10,10)}. These latter two intervals still pay the alpha with no
links. The new cycle supplies no open owner. Accordingly this example is
not a deficit counterexample: ordinary payment remains 1 at minimum cost 0.
It specifically refutes the rule that each forced escape P supplies a new
local beta or adjacent-interval payment unit. Existing original intervals
must still be accounted for once each, rather than relabelled as new credit.

## 5. Arbitrarily many sealed escape cycles

For any q>=1 take q copies translated by (12i,0), 0<=i<q, and optionally
append any even number of blank columns on the right. Occupied rows of a
copy are 1 through 10. Consecutive copies are separated by three row steps,
so no occupied nearest-neighbor interaction crosses copies. The shifts
preserve the band phase. Transport the raw rank certificate in each copy;
if plugged, append all new edge endpoints after all old layers. This proves
feasibility and complete freezing for all q and all such paddings.

Each copy retains its original open alpha/beta/mixed strands and its two
surviving alpha-support intervals. Their coordinate identities are distinct
across copies. Choosing one surviving interval for each alpha pays all q
with no links, which is optimal. Plugging deletes precisely the q singleton
intervals (3+6i,7,7); the other interval identities are unchanged. At each
of the q forced escape cycles there is no adjacent gap and no open owner.
Thus the failure of automatic local credit persists for arbitrarily many
motifs. This family does not establish any unbounded *payment deficit*.

## 6. Verification, limits and next mathematical question

```sh
python3 develop/check_frozen_beta_fork_escape.py \
  --output output/frozen-beta-fork-escape-validation.json
cd formal
lean SubQuorum/FrozenBetaForkEscape.lean
```

The solver-free verifier rebuilds every fixture, checks feasibility and a
strict freezing certificate, reconstructs original strands and intervals,
and checks the escape ranks, outward mates, site injection and two-point-cycle
owner bound. It passes 712 frozen board scans with 484 motifs: 72 copy/padding
boards (q=1..12, padding=0,2,10, raw and plugged), 36 exact interval-deletion
comparisons, and 640 transformed/offset survey boards. Separately, 16 carried
band isometries check both physical variants with ranks and band identities
transported together. These are finite checks of the general written proofs.

Lean checks six declarations: outRow involution/inequality/injection, the
strict two-of-three rank deduction, the vertical-outer-mate contradiction,
and the actual matching-coordinate injection of escape sites. Only standard
Lean axioms occur. The full geometric adapter, short-alpha consequence,
cycle ownership proof, explicit physical construction and all-q transport
remain written arguments with independent computational checks. No full grid
formalization or fresh external review is claimed. Optional Z3 discovery
scripts and their SAT/UNSAT receipts are retained solely as provenance.

The live-gate abstract obstruction remains unrealized as a frozen grid and
has not been excluded. The new lemma supplies necessary local geometry for
such a realization. The next question is whether whole-strand supports or
longer-cycle boundary structure force a globally usable reserve after
subtracting previously used original intervals. Site injection and even the
stronger two-point-cycle owner bound alone do not provide this reserve.
The universal compensation statement and 5/6 bound remain open. This research
branch preserves the submitted 11 October version and makes no mail changes.

## Positive completion, 25 October

[Protected singleton reserves](PROTECTED_SINGLETON_RESERVES.md) proves that
a different original unit beside the alpha's far tip cannot be sealed by
any feasible extension retaining the old selections and actual matching.
It is private to that source and can be eliminated with it at zero links.
A sharpened frozen variant has exactly one alpha-support unit; reserving
r such units across q copies has exact minimum link cost r, using distinct
whole betas. This does not make the local escape cycle itself a resource.
