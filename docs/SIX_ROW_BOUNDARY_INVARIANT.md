# An anchor-free six-row boundary invariant

## Statement and proof status

Let `G` be the ordinary rectangular grid with rows `0,...,5` and columns
`0,...,w-1`, where `w >= 1`. Let `M` be any matching of **actual grid edges**,
`P` its endpoints, and `T` a set disjoint from `P`. Write `O=T union P` and assume
every vertex of `T` has at most one neighbour in `O`. There are no retained
endpoints, prescribed partners, colour restrictions, or freezing assumptions.
The fixed boundary certificate below gives the all-length bound

    |T| + |M| <= 3w + (w mod 2).

The bound is attained for every `w`. In particular the exact maximum on every
six-row rectangle of even width is **half its area**. This removes the retained
`P0` hypothesis of the preceding colour-switch theorem, within the six-row
geometry. It is not a bound on arbitrary grid heights and is not a universal
5/6 improvement.

The general argument is the grid adapter and length induction in Sections 1–4.
Its finite local premises are an explicit integer potential table, independently
checked by a solver-free verifier. This is a computer-checked boundary invariant,
not a symbolic classification of all local cases and not an extrapolation from
finite-width optima. Formal and independent-review scope is recorded at the end;
do not describe this as an end-to-end Lean grid theorem.

## 1. Actual column words and complete grid adapter

For each column write a word of length six in the alphabet

| Symbol | Meaning |
|---|---|
| 0 | unoccupied vertex |
| 1 | selected vertex in `T` |
| 2 | endpoint with its actual mate in the previous column |
| 3 | endpoint with its actual mate in the next column |
| 4 | endpoint with its actual mate one row below |
| 5 | endpoint with its actual mate one row above |

A symbol 4 must be followed immediately by 5, and a symbol 5 must be preceded
immediately by 4. Symbol 4 is forbidden in the last row and 5 in the first row.
These conditions are precisely the possible within-column matching pairs; no
vertex has two partners. Every actual grid edge is vertical or joins consecutive
columns, so **every actual matching has this encoding**, with no matching
orientation omitted. Conversely, matching symbols on consecutive columns agree
exactly when their left/right endpoint sets agree.

For a word let `T,O,L,R,V` be six-bit masks. `T` and `O` are its selected and
occupied vertices, `L,R` are its left/right matching endpoints, and `V` is the
set of selected vertices with an occupied vertical neighbour. Discard words with
a selected vertex having two occupied vertical neighbours. There are 3,345
remaining words. Their weight is

    a = 2|T| + |O minus T|.

Here the two selected incidences and the one incidence of **each actual matching
endpoint** are counted once at their own vertex. On a closed board the total
weight is exactly `2(|T|+|M|)`. In particular a horizontal matching edge crossing
a column boundary contributes one endpoint on either side, not a fresh matching
edge in each column.

After processing a column retain the boundary state `s=(O,F,R)`, where `F` is
the set of its selected vertices having exactly one occupied neighbour among
the previous column and the current column's vertical neighbours. Such vertices
force their next-column neighbours to be empty. `F,R` are disjoint subsets of
`O`: selected vertices cannot be matching endpoints. Vertices of `O` in neither
set need no distinction between endpoint and selected status. A selected vertex
in this residual class has no occupied neighbour so far and can receive its
single possible right neighbour without exceeding the degree condition.

Encode each row by a base-four digit: 0 for empty, 1 for occupied in neither
`F` nor `R`, 2 for `F`, 3 for `R`, with row zero the least significant digit.
Thus the index is between 0 and 4^6-1. Call a state valid if no vertex in `F`
has both vertical neighbours in `O`. This is a necessary condition for every
actual state. All 2,404 states meeting this condition are checked; unreachable
states are permitted, making the invariant stronger than reachability alone.

Given old state `(Oold,Fold,Rold)` and a new column word, compatibility is exactly

    L = Rold,
    Fold intersect O = empty,
    V intersect Oold = empty.

The successor is

    (O, V union (T intersect Oold), R).

To verify completeness, the first condition gives the actual horizontal mates
on the boundary. The second prevents an old selected vertex already having one
occupied neighbour from acquiring a second one. For a new selected vertex:

* Two vertical occupied neighbours were already forbidden in the word.
* One vertical occupied neighbour forbids an occupied left neighbour, by the
  third compatibility condition.
* No vertical occupied neighbour allows zero or one occupied left neighbour.

Exactly the selected vertices that now have one such neighbour enter the new
`F`. The same second compatibility condition at the next step enforces their
right-neighbour constraint. These cases exhaust selected vertices. Every
successor is valid: its `F` is contained in `T`, which has no two vertical
occupied neighbours. Its `F` and `R` are disjoint by the column-word meanings.

At the first column the old masks are empty and `L=0`. At the final column
`R=0`, because actual matching edges stay inside the board. The preceding
arguments prove that every feasible board is covered. They also prove that a
compatible word sequence with these end conditions gives a feasible actual
matching and selected set, although only the forward implication is needed
for the bound.

## 2. Fixed local potential lemma

The two arrays `even` and `odd` in
[six-row-potential.json](../output/six-row-potential.json) define integer
functions `E(s), Q(s)` on valid states. A null entry marks an invalid state and
must not be used as a numerical value. The following are the complete local
premises:

1. **First column.** For every compatible first-column word of weight `a`
   and resulting state `s`, `a-6 <= Q(s)`.
2. **Even to odd.** Every compatible transition `s -> t` of weight `a` satisfies
   `a-6+E(s) <= Q(t)`.
3. **Odd to even.** The same transition satisfies `a-6+Q(s) <= E(t)`.
4. **Closed boundary.** If `R(s)=0`, then `E(s)<=0` and `Q(s)<=2`.

The independent [local verifier](../develop/check_six_row_potential.py) generates
all 6^6 row words and filters the matching and degree conditions explicitly. It
decodes all 4^6 states, verifies encode/decode consistency and successor validity,
then checks these exact integer inequalities: 740 first-column cases, 145,524
compatible transitions in each phase, and 433 terminal states. It uses no LP
solver, floating-point tolerance, finite-width search or guessed stabilization.
The verifier is executable local evidence for this finite lemma. The long-length
conclusion additionally requires the general proof below, not a maximum found
at some largest tested width.

The arrays were discovered by finite dynamic programming at widths six and
seven. **Their origin is not a premise.** The published check reads their integer
values as a fixed certificate and verifies the inequalities just stated. In
particular no assertion that a DP vector eventually stabilizes is needed.

## 3. General length induction

Fix an arbitrary feasible board, with arbitrary positive width `w`. Let `s_k`
be the state after its first `k` columns, `a_k` the weight of column `k`, and
`C_k=sum_{i=1}^k a_i`. We prove for every `1<=k<=w` that

    C_k - 6k <= E(s_k) if k is even,
    C_k - 6k <= Q(s_k) if k is odd.

For `k=1` this is exactly the first-column premise. It is important to use this
premise: the empty-state value `E(empty)=-4` is not an initial potential of zero.
Starting the two-phase recurrence from that value without the separate seed
would be an invalid proof.

If the assertion holds for `k`, add `a_{k+1}-6` to both sides and apply the
appropriate phase transition premise from Section 2. This gives the assertion
for `k+1`. The grid adapter ensures this transition and its successor are among
the checked legal ones. This completes the induction for arbitrary length.

At `k=w` the matching is closed, so `R(s_w)=0`. Section 2 gives

    2(|T|+|M|) = C_w <= 6w + 2(w mod 2),

and division by two proves the asserted bound. The proof does not assume any
bound on `w`, any retained vertex, or an equality configuration.

## 4. Why compensation is not spent twice

There is one state at each physical column boundary. If `Phi_k` denotes its
parity-appropriate potential, each transition pays at most

    a_{k+1}-6 <= Phi_{k+1}-Phi_k.

Summing uses every internal potential once with each sign. It cancels, rather
than being offered to multiple components. A right-matching endpoint belongs
to `R`, hence cannot simultaneously belong to the selected-neighbour obligation
`F`. A selected vertex's obligation is retained until the next actual column
checks it, then leaves the boundary. No hole is assigned independently to two
components, and no auxiliary matching is substituted for the actual matching.

This addresses the shared-resource problem by retaining the full six-row
boundary, including interactions between rows, rather than by assuming that
separately counted tiles can all spend the same boundary slack. It does not
give a general geometric compensation rule for arbitrary heights.

## 5. Sharpness and scope of the advance

Take `M` empty. In even-indexed columns select rows `0,2,4,5`; in odd-indexed
columns select rows `1,3`. No selected row is shared by consecutive columns.
The only adjacent selected vertices are the vertical pairs in rows `4,5` of
even-indexed columns. Thus each selected vertex has at most one occupied
neighbour. For width `2n` the count is `4n+2n=6n`; for width `2n+1` it is
`4(n+1)+2n=6n+4`. These equal `3w+(w mod 2)` in both cases. A vertical perfect
matching with `T` empty is another equality example for every even width.

For the earlier boards `w=6m+10`, the new bound is `18m+30` without `P0`.
Previously the same numerical optimum required a retained endpoint scaffold.
The advance is removal of that hypothesis, not a numerical improvement within
the already sharp retained class.

This result cannot simply be stacked to prove the same bound on taller boards:
actual matching edges can cross the cuts between six-row strips. Such endpoints
would require additional external-mate symbols, which are absent here. Proving
and paying those boundary terms remains a separate problem. Likewise, attaining
the bound in a fully frozen subclass requires its own construction; no freezing
claim about the new anchor-free extremizers is made.

## 6. Verification record

Run `python3 develop/check_six_row_potential.py`. Besides the entire finite local
certificate, it checks the adapter on 160 random actual matching/selection boards,
the sharp construction at widths 1 through 80, and rejection of a deliberately
corrupted potential. These board controls check implementation, not the all-length
proof. The exact results are in
[six-row-potential-check.json](../output/six-row-potential-check.json).

[BoundaryPotentialInduction.lean](../formal/SubQuorum/BoundaryPotentialInduction.lean)
formalizes the unrestricted-length induction and the final arithmetic, with
local seed, transition and terminal inequalities as explicit hypotheses. Its
four declarations compile locally without warnings, sorry or nonstandard axioms;
see [the exact formal scope](../output/six-row-induction-formal.json).
The finite table and full coordinate
adapter are not thereby Lean-certified.

Independent review `972e361c-db0a-4bad-aa36-d69049897db8`, observed gpt_6/pro,
is COMPLETED/ACCEPT for the executable finite-certificate proof, adapter, arbitrary
length induction, no reuse and all-width sharpness. Its original stream exactly
matches the terminal response. The reviewer reports executing the checker and
a second independently generated enumeration, but supplied no additional
executable source; that report is not a local execution artifact. The review
did not compile Lean. It recommends an explicit assertion-mode guard, now added.
[Verdict and scope](../output/six-row-independent-review.json). No manuscript
revision or email is part of this note.

The assistance has now returned: it gives a structural
[two-row signed-boundary lemma](TWO_ROW_SIGNED_BOUNDARY_COMPENSATION.md), but
no unrestricted structural six-row proof. Its proposed four-to-two-column
compression has a [realizable structural counterexample](TWO_COLUMN_COMPRESSION_OBSTRUCTION.md).
That failure does not affect this certificate, which uses no short-completion
premise. The separate signed-edge ledger specifies which negative internal
payments a structural cross-strip proof must retain.
