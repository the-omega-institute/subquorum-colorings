# A vertical-reflection quotient for the width-six frontier

13 November 2026. The exact transfer state for a grid of height (h) records
four retained columns of selected vertices and four retained columns of
deletion-witness flags. The height-six run reached 7,506,432 states at length
four before the existing packed table became the limiting resource. The grid
has a reflection across its horizontal midline, so a state and its reflected
state have identical future values and identical score.

The generator now stores the canonical representative

\[
 \min\{q,\rho(q)\}
\]

of each state (q), where (ho) reverses the six row bits independently
in each retained selected and flag column. Appended columns are still
enumerated in full, so this is a quotient of the exact transition graph,
not a heuristic pruning rule. The score is unchanged by (ho).

The quotient is independently checked at height three by comparing every
canonical endpoint state with both it and its reflected state in the original
unquotiented vector. The established period-three score vector is unchanged:

```text
length 1..15: 2,4,5,7,9,10,12,14,15,17,19,20,22,24,25
length 12 and 15: 7661 canonical states, 14726 original states
```

At height six the measured frontier is:

```text
length=1  SF=4   states=36
length=2  SF=6   states=2080
length=3  SF=10  states=68592
length=4  SF=12  states=3754512
length=5  SF=16  states=18519358
```

The next layer reaches the fixed (2^{25})-slot table limit before a
periodic endpoint vector is found; the run peaks at approximately
1.06 GB resident memory. Thus the reflection quotient removes about half of
the height-six states at the first measured layers, and it reaches the exact
(6\times5) frontier value (16=F(6,5)) in the optimized transfer, but it
does not yet prove a width-six periodic certificate. The result is an
algorithmic reduction and a sharper resource diagnosis; the general
width-six equality remains open.
