# Attachment-aware cross-component compensation

2 October 2026. This note isolates the term that remains when an occupied
adjacent band has matching edges leaving it for saturated tiles. It is a
specialization of the exact tile ledger and the capacitated Hall allocation;
it does not assume that an outward attachment is itself a negative donor.

## The attachment deficit

Let `A_1,...,A_K` be pairwise tile-disjoint positive source regions and let
`S_1,...,S_K` be pairwise tile-disjoint adjacent bands, also disjoint from the
sources. Write `a_i = sigma_i/2`, where `sigma_i` is the number of matching
edges leaving `S_i` and entering saturated tiles outside the accounting
regions. Assume the exact local estimates

```text
rho(A_i) <= 1,
rho(S_i) <= -1 + a_i.
```

The second estimate is the boundary-aware band identity
`rho(S_i)=-Delta_i+sigma_i/2` together with `Delta_i >= 1`. The quantity `a_i`
is a bookkeeping demand. It is not a donor: the receiving saturated tile has
zero charge and cannot be counted as negative compensation.

Let `C_1,...,C_L` be pairwise tile-disjoint donor regions, disjoint from all
`A_i,S_i`, with capacities `c_j >= 0` and

```text
rho(C_j) <= -c_j.
```

For each band `S_i`, specify an admissible donor set `N_i`. A donor may occur
in several `N_i`, but its capacity is one shared budget. The attachment
allocation condition is the capacitated Hall inequality

```text
sum(c_j for j in union(N_i for i in X)) >= sum(a_i for i in X)
```

for every subset `X` of bands. Capacities and demands may be half-integral;
doubling them gives an ordinary integral flow problem.

**Lemma (attachment-aware compensation).** Under these hypotheses, if `W` is
the remaining deficient tile set and `rho(W) <= 0`, then

```text
sum_i rho(A_i) + sum_i rho(S_i) + sum_j rho(C_j) + rho(W) <= 0.
```

Consequently the exact global ledger gives `q <= 0`, so the coefficient of
`|M|` is one on this covered class.

**Proof.** The Hall condition gives a fractional allocation `x_{ij}` with
`sum_j x_{ij}=a_i` and `sum_i x_{ij}<=c_j`; this is the max-flow/min-cut
theorem after multiplying by two. Summing the regional estimates once gives

```text
q <= K + sum_i(-1+a_i) - sum_j c_j + rho(W)
   = sum_i a_i - sum_j c_j + rho(W).
```

Taking `X` to be all bands in Hall gives `sum_i a_i <= sum_j c_j`, and the
right-hand side is at most `rho(W) <= 0`. Each donor region appears once in
the ledger and each flow arc spends at most its capacity, so a shared donor is
never used twice. Crossing residual edges are already split into their two
endpoint halves by the definition of `rho`. QED.

The lemma separates two obligations that are easy to conflate. The local
band argument supplies the `+a_i` attachment debt, while a geometric theorem
must certify negative regions and the Hall incidence. A saturated receiving
tile alone supplies neither. If Hall fails, the exact deficiency is a real
shortage of this proposed donor rule, not a counterexample to the grid
inequality; the unassigned deficit may still be paid by `rho(W)`.

## Interval form and no reuse

If the admissible sets `N_i` are intervals in one ordered donor list, the
interval-deficiency theorem applies directly. In particular, it is enough to
check donor-interval containment inequalities when the windows are arbitrary,
and consecutive source blocks when the endpoint order is proper. This handles
nested and repeated attachment windows without silently treating repeated
visits as new capacity.

For two bands the condition is especially transparent. With windows `N_1,
N_2`, individual capacities must cover `a_1` and `a_2`, and the capacity of
`N_1 union N_2` must cover `a_1+a_2`. The union check is the no-reuse step. Two
bands that each reach only one shared unit have a one-unit shortfall even
though each individual check passes.

## Scope and the current obstruction

The escaping-attachment family in the boundary-aware note has `sigma=2` and
`rho(S)=0`: its adjacent band does not pay the source locally. The family also
has a large negative remainder, so it satisfies the global target inequality,
but it does not certify two local donors. The present lemma therefore gives a
safe interface for a future geometric result: one must either find donors
with total capacity at least `sum sigma_i/2`, or prove the same amount directly
from `rho(W)`. The receiving saturated tiles cannot be counted as donors.

This is a conditional coefficient-one result. It does not establish the
required Hall incidence for arbitrary bends, occupied bands, or merged
capacity-two routes, and it makes no change to the journal manuscript or
arXiv source.
