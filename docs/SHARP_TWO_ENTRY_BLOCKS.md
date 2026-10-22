# The two-entry bound is sharp, with no degree-four forced endpoint

22 October 2026. Authors: Haobo Ma and Wenlin Zhang.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.

## 1. What the witness excludes

The accepted entry theorem gives 2f<=j for every exchange-terminal feasible
grid pair, where f is the number of flexible allowed-edge blocks and j counts
occupied-degree-four endpoints. Here a connected16-endpoint example has
f=1,j=2. BOTH degree-four endpoints belong to the flexible square; every
forced-block endpoint has occupied degree three. Thus the coefficient2 is
sharp, and there is no compulsory additional degree-four endpoint in the
forced network that transmits freezing into a flexible block.

This is a sharpness example for a structural reduction. Its whole receiver
charge is zero, so it is not a positive-demand sharpness example and does
not contradict compensation or the grid bound. No minimum-size claim is made.

## 2. Exact configuration and its two matchings

Use a6-by8board. The selected set is

    {(0,1),(0,3),(0,6),(1,0),(1,7),(3,6),(4,0),(4,5),(5,1),(5,3)}.

The following six pairs are forced in the order shown:

    (1,1)--(1,2), (1,6)--(1,5), (3,5)--(2,5),
    (4,1)--(4,2), (4,3)--(3,3), (3,2)--(2,2).

The remaining endpoints are the square

    a=(1,3), b=(1,4), c=(2,3), d=(2,4).

Match them as ab,cd or ac,bd. These pairs specify all16endpoints; every
other site is blank. Here T denotes a selection and P an endpoint:

    .T.T..T.
    TPPPPPPT
    ..PPPP..
    ..PP.PT.
    TPPP.T..
    .T.T....

Every selection has exactly one occupied neighbor. Each endpoint has
occupied degree three except a,c, which have degree four. These statements
are direct checks of the displayed coordinates. In particular all twelve
forced-pair endpoints have degree three.

For matching classification, the first endpoint of each of the six listed
pairs is a leaf after earlier pairs are removed. Any perfect matching must
therefore use that pair. The remaining four-cycle has exactly its two
listed perfect matchings. Thus there are exactly two matchings, with six
forced blocks and one flexible square. No matching enumeration is needed
for this proof.

## 3. Complete retained-neighbor certificates

For a fixed matching m, read a table from top to bottom. Each row names
an endpoint x and two distinct occupied neighbors. Each witness is either
an original selection or m(z) for a previously listed endpoint z. Neither
witness is m(x). Inductively neither witness can be deleted by a feasible
promotion bundle, so x cannot be promoted. This argument applies to mixed
as well as monochromatic bundles. A table listing every endpoint excludes
all nonempty bundles for that matching.

### Horizontal square matching ab,cd

| Endpoint | First retained neighbor | Second retained neighbor |
|---|---|---|
| (1,1) | (0,1) | (1,0) |
| (1,6) | (0,6) | (1,7) |
| (3,5) | (3,6) | (4,5) |
| (4,1) | (4,0) | (5,1) |
| (1,3) | (0,3) | (1,2) |
| (4,3) | (4,2) | (5,3) |
| (1,5) | (1,4) | (2,5) |
| (2,4) | (1,4) | (2,5) |
| (3,2) | (3,3) | (4,2) |
| (2,2) | (1,2) | (2,3) |
| (2,3) | (2,2) | (3,3) |
| (1,4) | (1,5) | (2,4) |
| (2,5) | (1,5) | (2,4) |
| (3,3) | (2,3) | (3,2) |
| (1,2) | (1,3) | (2,2) |
| (4,2) | (3,2) | (4,3) |

### Vertical square matching ac,bd

| Endpoint | First retained neighbor | Second retained neighbor |
|---|---|---|
| (1,1) | (0,1) | (1,0) |
| (1,6) | (0,6) | (1,7) |
| (3,5) | (3,6) | (4,5) |
| (4,1) | (4,0) | (5,1) |
| (1,3) | (0,3) | (1,2) |
| (4,3) | (4,2) | (5,3) |
| (2,2) | (1,2) | (2,3) |
| (2,4) | (2,3) | (2,5) |
| (3,2) | (3,3) | (4,2) |
| (1,5) | (1,4) | (2,5) |
| (2,3) | (2,2) | (3,3) |
| (3,3) | (2,3) | (3,2) |
| (1,2) | (1,3) | (2,2) |
| (1,4) | (1,3) | (1,5) |
| (4,2) | (3,2) | (4,3) |
| (2,5) | (1,5) | (2,4) |

Both matching choices have a complete table. Together with the forced-pair
classification this proves exchange terminality, not just freezing under
one prescribed matching. The displayed a,c are therefore the only two
possible degree-four entry endpoints, one in each checkerboard color.

## 4. Arbitrarily many sharp blocks

For any positive integer k, put copies at offsets (0,10i), 0<=i<k, on a
6-by10kboard. Occupied columns of one copy run from10i to10i+7; the next
copy starts at10i+10. Thus at least two blank columns separate occupied
sets, and all occupied-neighbor counts and freezing witnesses are unchanged.
Endpoint components are precisely the k copies. Matching choices factor
independently, giving exactly2^kperfect matchings, all frozen. Consequently

    f=k, j=2k, and no forced endpoint has occupied degree four.

There are10kselections,8kmatching edges and16kendpoints. Each canonical
receiver has charge0; the exact board margin is30k-18k=12k. This is an
all-k construction proof. It makes no claim of a connected multi-block
attainment family; the one-copy endpoint component is connected.

## 5. Validation and scope

`develop/check_sharp_block_entries.py` checks the six forced leaf pairs,
both complete transcripts, the exact matching blocks and both degree
classes directly from coordinates. It additionally rejects all13120nonempty
oriented bundles across the two matchings, checks32phase/symmetry images,
and verifies the separated construction for k=1through5. The fixed witness
was found by a Z3 search with a satisfiable known-three-junction control;
no search exhaustion or solver-completeness claim enters the proof.

The final proof is the explicit matching classification and the two
retained-neighbor tables, not a finite-enumeration argument for a general
inequality. This new sharpness witness has not received a separate Oracle
review or Lean formalization. The accepted entry theorem and independently
accepted matching-block tile ledger retain their own scopes. The universal
missing compensation inequality remains X<=D+B+2J. The submitted manuscript
and public main are unchanged.
