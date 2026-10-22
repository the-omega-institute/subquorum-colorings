# Terminal exterior closure: one-source classification and two obstructions

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## Model and the actual exterior question

Use the immutable full-even-U/standard-rotor model and Phi of
`ALL_EVEN_GAP_AXIAL_COMPENSATION.md`. Every unconsumed original support
is retained with occupied degree one. Original endpoint sets are disjoint,
their nearest-neighbour graphs are connected, and original matchings are
unchanged. Every original support has an adjacent own endpoint. All
dimensions, orientations and translations permitted by that model remain
available; a decomposition of arbitrary grid configurations is not assumed.

Fix even W>=6 and g>=0, let a_i=2+10i, and write a=a_g. The old family O
has A=U(W+2,D,F), chart(r,c-1), and B_i=U(W,4,4) at row a_i. The even
outer depths satisfy D,F>=a+6. Fix a spanning D or U in every earlier
gap, with any permitted locally complete pocket fillings, and call that
fixed inventory K. For empty earlier pockets, if d gaps use D, then

    Phi(K)=4g+(W-4)d.

All earlier chamber additions have already been assigned to their sealed
chambers. An additional exterior original avoids those chambers. Its
marginal against K equals its marginal against O, by the established
physical-tile separation. The unrestricted exterior may also contain
sources outside A or around its finite wall tips.

The new results classify exactly a ONE-ORIGINAL exterior completion, then
show why neither a single-cap classification nor monotonicity settles
the arbitrary exterior problem. A source original is not the same thing
as a connected component of the final endpoint graph.

The authoritative original charge is

    q=|M|+|original supports inside endpoint tiles|-2|endpoint tiles|.

## Theorem 1: the complete one-original exterior catalogue

Suppose C is the only exterior original and K+C is complete. Then there
is an even integer h>=4 such that

    C=U(W,h,h), chart(r,c)=(a+h+5-r,c),
    D,F>=a+h+6.                                         (1)

Conversely every C in (1) completes this fixed core, including its locally
complete earlier pocket fillings. Its exact exterior marginal is

    Delta_out=5,                                        (2)

independently of W, h, g, the earlier chamber choices and unequal D,F.
Thus a one-original exterior completion exists if and only if
min(D,F)>=a+10. For a+6<=min(D,F)<a+10, any complete exterior completion
requires at least TWO exterior originals, if a completion exists at all.
No existence assertion for that latter case is made here.

### Both terminal supports must be owned by C

The last B has immutable beyond-tip supports

    p=(a+5,1), q=(a+5,W).

At p its own endpoint (a+4,1) and A's endpoint (a+5,0) are occupied;
the symmetric two neighbours are occupied at q. The depth assumption
D,F>=a+6 supplies both wall neighbours. Neither point belongs to K.
Completeness forces their consumption. Earlier chamber sources cannot
own these points, by sealed-chamber localization. Hence C contains both.

At p its north and west neighbours already belong to K, so its own
endpoint neighbours are confined to east and south. In a full U, the
only such endpoint roles are a terminal or an outer bar corner: straight
stem points need opposite directions and inner bar/branch points have
at least three endpoint neighbours. There are four possibilities.

* East/south corner, horizontal bar: a downward D-type U whose bar starts
  at p. Since q is on the same row, its breadth is at least W. The wall
  at (a+5,W+1) forbids greater breadth, so it is exactly W.
* East/south corner, vertical bar: the horizontal stem from p has even
  depth. To reach column W it would have depth at least W, because W-1
  is odd, and would cross the occupied point (a+5,W+1). All other endpoints
  on p's row belong to this stem. Thus this role cannot own q.
* East terminal: the same even-stem and wall argument excludes q.
* South terminal: the bar is below p. On p's row this U has only its two
  side stems, so containing q forces breadth W. Write h for the near
  depth and e for the far depth. Reaching q requires e>=h. If e>h,
  evenness gives e>=h+2 and the far stem contains the already occupied
  point (a+4,W). Thus e=h, giving exactly the upward C in (1).

A standard rotor has horizontal span three in every orientation and
cannot contain both p and q, whose horizontal separation is W-1>=5.
This exhausts all original roles without a dimension bound.

### The downward candidate cannot terminate against a finite outer wall

Write t=a+5+h for its left tip row, which is odd. D is even and cannot
equal t. If D<t, then D+1<=t. A's original beyond-tip support (D+1,0)
has both its own endpoint (D,0) and C's endpoint (D+1,1) as neighbours.
It is not consumed: C has no endpoint in column zero and no other
exterior original exists. If D>t, then D>=t+1. C's beyond-tip support
(t+1,1) has its own tip (t,1) and A's wall endpoint (t+1,0) as neighbours.
It too is unconsumed. Earlier chamber originals reach neither witness.
Both cases contradict completeness. The left wall alone excludes every
downward candidate, including unequal near and far depths.

### The upward candidate has the exact outer-depth threshold

Its left stem runs from row a+5 to t=a+h+5. If D<t, the support (D+1,0)
has the same two neighbours as above and remains unconsumed. Consequently
D>=t+1. The right wall independently gives F>=t+1, proving necessity.

For sufficiency, both inner side columns are occupied continuously from
row2 through t. A's inner odd-row supports through t are consumed;
those starting at t+2 retain only their own wall neighbour. Its outside,
bar-end and beyond-tip supports are isolated exactly as in the previous
whole-cap proof. C's exterior supports are consumed by A; its two terminal
supports are consumed by the last B. Its retained inner supports are

    {(r,2),(r,W-1): r even, a+6<=r<=a+h+2}.             (3)

They have only their own side-stem neighbour. Their successive rows differ
by two; the two columns differ by W-3>=3. They start three rows below
the last B's retained inner supports at row a+3, and the last such row
is two rows above C's inner bar. Earlier chamber support lists remain
unchanged. This proves the whole support condition. Endpoint disjointness,
matching coverage and endpoint degree at least three follow from the
unchanged original records, as in the prior cap theorem. Even translation
embeds all finite records in an even rectangle without clipping supports.

### Exact receipt, counted once

C is in the canonical charge-one alignment. Each wall band has h/2+1
new full mixed tiles and h directed events. The first mixed tile includes
the last B tip and C terminal; its two vertical directions target immutable
original supports and are excluded from the event count. The other events
are the two directions at even rows a+6,a+8,...,a+h+4. No earlier chamber
shares these physical tile rows. Therefore

    Delta_out=1+2(h+2)-2h=5.

This proves the theorem. In particular it does not make a finite outer
wall into an infinite barrier: both possible tip orderings were checked.

## Theorem 2: the unrestricted exterior bound contains the global source problem

Fix any one of the complete capped cores with empty earlier U pockets,
say W=6 and any fixed g. Its exterior contribution is five. Let H be ANY
finite complete canonical U/rotor fusion, and write v=Phi(H). For every
integer k>=0 there is a complete extension of that SAME retained core
with exterior contribution

    Delta_out=5+kv.                                     (4)

**Proof.** Place k copies of H outside the core and all its sealed chambers
by even translations. Since the records are finite, choose their occupied
bounding boxes separated from one another and the capped core by at least
three lattice units. Their endpoint-tile footprints are then disjoint too.
No new retained support neighbour or endpoint collision appears. Thus the
whole union is complete and its original matchings remain disjoint.

Even translation preserves physical tiles, original charges and the
immutable support predicate. Every full mixed tile and source-labelled
intratile event belongs to exactly one copy or the core. Hence inventory
is additive, and each copy is wholly exterior. This proves (4), with no
reuse of the capped core's five units. A sufficiently large even rectangle
contains all records; ambient area is not used as an additive budget. QED.

Consequently ANY finite lower bound depending only on this fixed old core
for all its finite complete exteriors implies

    Phi(H)>=0 for EVERY finite complete canonical fusion H.              (5)

Otherwise v is a negative integer and (4) tends to minus infinity. In
particular an exterior sign proof cannot silently discard disconnected
outside components: it would already prove the unrestricted source-inventory
inequality on them. This is a necessary implication, not a proof of (5),
and not a claim that a negative v exists. Nor does a negative sufficient
source inventory by itself refute the ambient grid inequality.

For completeness, the earlier endpoint-component restriction lemma gives
an exact reduction for this fixed-core problem. All fixed core originals
are in one endpoint component. In any complete extension restrict to its
component containing the core and to the other endpoint components. Each
restriction is complete; no support consumer is lost, because consumption
joins its endpoint to the support's own endpoint anchor. Inventory is
additive: events have adjacent endpoints, and a full tile belongs to one
endpoint component. Thus an exterior bound L holds for all extensions if
and only if BOTH conditions hold:

1. The bound L holds for extensions in which every original is in the
   core's endpoint component.
2. Every complete canonical fusion has nonnegative Phi.

Necessity of condition2 is the amplification argument. Sufficiency is
componentwise addition, spending each component's inventory once. This
uses the existing component lemma rather than claiming it as a new result.

## Theorem 3: even the anchored exterior is not monotone

Disconnected components are not the only obstacle. Take g=0, even B>=6,
k>=1, and W=k(B+34)+2. The old core consists of A and B_0 only. Add the
depth-four cap C; its six-row pocket contains the k-block V/H family from
`SPANNING_CHAMBER_GLOBAL_CAPS.md`. There are no earlier sealed gap chambers,
so ALL these added originals are exterior. The two whole configurations,
before and after adding the k H originals, are complete, with

    Delta_out_before=5+16k,
    Delta_out_after=5+k(B+9),
    H marginal=k(B-7).                                 (6)

Both endpoint graphs are CONNECTED. A and B_0 have adjacent endpoints;
C's terminals are adjacent to B_0's tips. Each V reaches the top and
bottom pocket rows, so its endpoints are adjacent to the old full boundary.
Each H side is adjacent to its contact V bar. Thus every original belongs
to the same endpoint component as the retained core.

The complete support lists and block-interface proof are those already
proved for the local family, glued now into the TERMINAL pocket instead
of an earlier gap pocket. The cap's five units are independent of that
pocket's tiles and events. This proves (6) for all B,k without enumeration.
At B=6,k=1 the whole budget is21 before and20 after. For arbitrary k the
marginal is-k, despite whole completeness and endpoint connectedness of
both states. This refutes monotonicity of the anchored exterior under
complete source addition. It does not refute Delta_out>=0 or>=5: both
displayed total exterior budgets remain positive.

The appropriate next problem is therefore the aggregate inventory of
anchored multi-original closures, together with the separate global sign
on detached complete components. Neither follows from counting gate owners
or retaining only a minimal complete cap. The submitted manuscript remains
unchanged; no unrestricted grid theorem is asserted.

## Validation and review status

The general arguments above are written proofs awaiting independent review.
The source-level checker passed on22October:6048 endpoint-disjoint gate
candidates,152 complete single caps,5184 excluded downward candidates,
80 short-tail controls,108 exact cap receipts,18 both-complete connected
exterior pairs,40 separated-copy and8 zero-charge rotor controls. These
finite checks corroborate the separate general arguments.

`formal/SubQuorum/TerminalExteriorClosure.lean` passed locally with10theorems
and11individual declaration axiom audits, no warnings/errors/sorry/native
evaluation. Its scope is the displayed support predicate and arithmetic;
it does not formalize the role catalogue, physical gluing or global reduction.

A contained-source18x12 discovery window has no exterior inventory below5
(437candidates, known cap SAT). The24x24 search timed out with UNKNOWN
(52859candidates); it excludes nothing. Neither search proves a general
exterior bound. See `output/terminal-exterior-closure-validation.json` and
the separate controls record for commands, scope and pending review handles.
