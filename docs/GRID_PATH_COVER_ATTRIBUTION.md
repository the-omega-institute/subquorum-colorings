# Verified grid path-cover source locators

2 October 2026. The published PDF of Marko Jakovac and Andrej Taranenko,
*On the k-path vertex cover of some graph products*, Discrete Mathematics
313 (2013), 94-100, DOI [10.1016/j.disc.2012.09.010](https://doi.org/10.1016/j.disc.2012.09.010),
was supplied locally by the user. Text extraction and visual inspection of
the relevant pages establish the following locators.

## Primary statement and attribution

**Theorem 2.1, journal p. 95 (PDF page 2)** gives the three Cartesian-grid
3-path vertex-cover formulas. Its introductory sentence explicitly says that
the theorem was presented in reference [3]. That reference is Brešar,
Jakovac, Katrenič, Semanišin and Taranenko, *On the vertex k-path cover*,
listed in this PDF as submitted for publication; it subsequently appeared in
Discrete Applied Mathematics 161 (2013), 1943-1949. Rafik supplied the locator
Theorem 4.1 for that first paper; the first paper's theorem number has not
been independently checked against its full text in this review.

Here the paper's `psi_3` denotes the minimum 3-path vertex-cover number,
which we write `tau_3`; it is distinct from the sub-quorum parameter `psi_sq`.
The complement relation `diss(G) = |V(G)| - tau_3(G)` is stated on p. 94.
Our `beta_2` is this dissociation number.

Theorem 2.1 states, with `r,s >= 1`:

| Grid dimensions | Part | `tau_3` |
| --- | --- | --- |
| `(2r+1) x (2s)` | (i) | `2rs + floor(2s/3)` |
| `(2r) x (2s)` | (ii) | `2rs` |
| `(2r+1) x (2s+1)`, `r <= s` | (iii) | `r(2s+1) + floor((2s+1)/3)` |

Transposition covers the reversed dimensions. A dimension equal to one is
outside the displayed hypotheses and is handled separately by the path
formula `tau_3(P_w) = floor(w/3)`, also stated on p. 95.

**Proposition 3.1, p. 96 (PDF page 3)** supplies a general `k >= 3`
construction bound for Cartesian products. Immediately after its proof,
the authors state that it is sharp for `k=3` and corresponds to Theorem 2.1
from [3]. Proposition 3.1 explains the periodic construction; Theorem 2.1
is the direct locator for the exact grid values. Theorem 4.1 in this second
paper concerns lexicographic products and is not the grid locator.

## General algebraic comparison with our F

For positive height `h` and width `w`, set `g(w)=w-2 floor(w/3)`. From the
definition of our periodic-construction formula,

```text
2 F(h,w) - hw = max((h mod 2) g(w), (w mod 2) g(h)).
```

This follows by using `ceil(2w/3)=w-floor(w/3)` in both terms of `F`.
For even `h,w`, Theorem 2.1(ii) gives `hw-tau_3=hw/2=F`.
For odd `h` and even `w`, part (i) gives

```text
hw - tau_3 = ((h+1)/2) w - floor(w/3)
           = (hw + g(w))/2 = F(h,w).
```

For odd `h,w >= 3`, transpose so `h <= w`. Along odd integers `g` is
nondecreasing: `g(w+2)-g(w)` is either zero or two. Thus `g(h) <= g(w)`,
and part (iii) yields the same displayed expression and hence `F(h,w)`.
For `h=1`, the path formula gives `w-floor(w/3)=ceil(2w/3)=F(1,w)`;
transpose for `w=1`. This proves agreement in every dimension without
relying on finite enumeration.

There is also a direct construction comparison. In Proposition 3.1 at
`k=3`, the divisor pair is `(a,b)=(1,2)`. One of its cover-size terms is

```text
A = floor(h/2) w + floor(w/3) h - 2 floor(h/2) floor(w/3).
```

Taking its complement gives exactly the first term of `F`:

```text
hw - A = ceil(h/2) ceil(2w/3) + floor(h/2) floor(w/3).
```

The exchanged divisor pair gives the second term. Consequently the minimum
of the two cover bounds is `hw-F(h,w)`. This identifies both the numerical
formula and the periodic lower construction with the older path-cover
results. The independent ladder-equality and directional representative
arguments must be assessed separately; the numerical `beta_2=F` formula
is not a new result.

## Citation-ready text and validation

A reference sentence suitable for coauthor review is:

> The exact dissociation number of rectangular grids follows by complementation
> from the grid 3-path vertex-cover formulas of Brešar et al., reproduced as
> Theorem 2.1 in Jakovac and Taranenko (2013, p. 95); the corresponding periodic
> construction is given in Proposition 3.1 of the latter paper (p. 96).

An exact integer check compared both the parity formulas and the `k=3`
construction expression with the repository's `F` on all 90,000 rectangles
with sides from 1 through 300. All passed; dimensions equal to one were
checked using the separate path formula. This is a transcription and
algebra regression check; the all-dimensional argument is above.

The inspected seven-page PDF has SHA-256
`b24f5782b57135de62736426fc247170fab04467f1cc326ac59065f48b546978`.
The PDF is retained locally and is not redistributed in the research or
tracking repositories. No manuscript, arXiv source or Lean declaration is
changed, and no email is sent by this source review.
