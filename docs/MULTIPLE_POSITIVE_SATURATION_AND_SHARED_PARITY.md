# Multiple positive sources: saturation and a shared parity budget

20 October 2026. The saturated two-gate geometry is source-local. Its
single-positive hypothesis was needed only to force zero reserve from a
failure, not for the geometric classification itself. This gives a theorem
for arbitrary numbers of positive sources at zero reserve. The exact demand
count below also identifies what a general compensation proof still needs;
separate rounding for different sources cannot supply that proof.

## 1. Model and exact demand

Retain the complete fixed-source model, original ownership and support
retention of EXACT_GEOMETRIC_EVENT_RESERVE.md. Sources are finitely many
complete U and rotor sources, original endpoint sets are disjoint, final
P and M are the original unions, and each final selected vertex has at most
one occupied neighbor. All allowed independent even dimensions, phases and
square-lattice isometries are permitted. A positive source has exactly two
canonical sides. Marks are the established actual blocked-side marks;
they are not independently chosen flags in the physical theorem.

Let n0,n1,n2 count positive sources with zero, one and two marked sides.
Let N=n0+n1+n2 and G=n1+2n2. Let R=S+C-Kirregular be event reserve, and

    D = A+U0+Z0+L1+2L2bar+2L2mutual+L3 = 2R.

The exact identity and all nonnegativity assertions are the preceding
reserve theorem. The source ledger satisfies sigma>=N+R-G. Consequently

    N+R-G = n0+R-n2,                               (1)
    joint allocation iff 2n2 <= 2n0+D.             (2)

Thus the net demand is n2-n0, not necessarily n2. Each unmarked positive
source already contributes one unit of available ledger margin. One-mark
sources contribute zero to this difference. Formula (1) counts the same
original sources once, so it does not create a second supply of credit.
Integrality gives the necessary and sufficient failure test

    n2 >= n0+R+1.                                  (3)

These equivalences are for the sufficient allocation in the source ledger.
A failure need not make actual sigma negative and does not refute the grid
target. Equations (1)--(3) alone do not prove the allocation.

## 2. Source-local obstruction at zero reserve

For each positive source normalize its dimensions as U(w,a,b). Call it
exceptional for this note precisely when

    w != 6 and (w>=12 or max(a,b)>=8).              (4)

Let L count exceptional positive sources. This is a dimension flag, not a
claim that any obstruction in that range can actually occur.

**Lemma.** In any complete fusion with R=0, every doubly marked positive
source is exceptional. In particular n2<=L, for arbitrary N.

**Proof.** The exact reserve theorem forces all seven geometric counts to
vanish. In particular there are no activated positive terminals, no blank
marks, and no nonfull original 2P0T tiles. Both marked sides of any chosen
doubly marked positive source therefore have occupied unactivated gates.
This conclusion uses global saturation and does not assume N=1.

For w=6, the occupied-gate theorem says that an occupied marked gate on a
shorter or equal side activates its positive terminal, for arbitrary
incoming negative dimensions. Both marked sides include such a side.
This contradicts A=0. Hence w!=6.

For w<=10, use SATURATED_TWO_GATE_GEOMETRY.md, Sections2--5, on this one
chosen positive source. These sections use only its complete supports,
disjoint original endpoints and global zero reserve. They never assume
there are no other positive sources. If one original owner occupies both
gates, its exact upright or inverted nested-U form requires a,b>=8.
Otherwise the two original owners are distinct. Two transverse gate
footprints would overlap, so at least one owner is longitudinal. Its
strict clearance 4<=h<=a-4, or the reflected version, forces the relevant
positive height to be at least eight. Thus either w>=12 or max(a,b)>=8.
This proves (4) for every doubly marked positive source separately.

Finally the mapping from a doubly marked positive source to that same
original positive source is an injection into the exceptional sources.
It does not assign, round or spend any geometric defect. Hence n2<=L
without a resource-reuse assumption. This proves the lemma.

## 3. Global zero-reserve theorem

**Theorem.** Under the same assumptions, if R=0 then

    sigma >= n0-n2 >= n0-L.                         (5)

In particular the joint allocation holds if L<=n0. It holds for arbitrary
numbers of positive sources when each positive source satisfies either

    w=6, with arbitrary independent even a,b>=4;
    or w in {8,10}, with a,b in {4,6}.              (6)

All other negative U sources and all rotor dimensions/phases remain
unrestricted. No separation of the final endpoint components is needed.

**Proof.** Substitute R=0 in (1) and use the source ledger and the lemma.
Condition (6) makes L=0. More generally L<=n0 makes the final bound in
(5) nonnegative. A zero-reserve failure must have n2>=n0+1, hence at
least n0+1 distinct exceptional positive sources. This is a necessary
obstruction count, not a construction in the exceptional range.

The theorem genuinely permits arbitrarily many positives. It does not
extend the same dimension class to R>0: that step would require a shared
count against the actual defects in D. It also does not decompose arbitrary
rectangular-grid configurations into these complete sources.

## 4. Why separate parity rounding does not extend the theorem

The exact reserve says D is even globally. It does not say a proposed
defect subtotal assigned to each doubly marked source is even. Suppose
an attempted argument proves only that each of two doubly marked sources
has a different single unit of defect. With n0=0,n1=0,n2=2 and D=2,
the consistent arithmetic values are N=2,G=4,R=1. The allocation margin
is N+R-G=-1. Rounding each local singleton subtotal up to one reserve
unit would demand two reserve units from the one unit actually present.

More generally, if k assigned subtotals d_j have o odd entries, then

    sum_j ceil(d_j/2) = (sum_j d_j+o)/2.            (7)

For an even total, global reserve is only (sum_j d_j)/2. Separate rounding
adds o/2 units that have not been supplied. This defect persists even
when the assigned underlying defect occurrences are disjoint.

The two-source numbers are an exact counterexample to the inference
"one distinct defect per double mark plus global parity pays every double
mark." They are NOT a complete-source physical fusion, a counterexample
to joint allocation, or a counterexample to the grid inequality. Existence
of physical low-reserve fusions with that demand is still unresolved.

A sufficient next proof is a single count 2(n2-n0)<=D. For example,
assign two DISTINCT unit-capacity slots to each doubly marked source,
using each actual defect occurrence at most its weight and each unmarked
positive source at most two slots. Source-labelled A,U0,Z0 occurrences
and tile-labelled L1,L2bar,L2mutual,L3 occurrences form the actual defect
pool. Distinct labels do not prove availability: the exact reserve
identity is what certifies their simultaneous weights. The displayed
assignment is a proof target; no geometric matching or Hall inequality
is asserted here. More flexible global counts could prove the same bound
without making an explicit assignment.

## 5. Validation and formal scope

develop/check_multiple_positive_saturation.py checks exact source-demand
identities, the parity-rounding obstruction, and complete physical controls
with original side counts reconstructed independently of the aggregate
ledger. Additional isolated-positive controls exercise zero reserve with
arbitrarily extendible finite source arrays. They do not realize the
two-source arithmetic obstruction or occupied zero-reserve bad gates.

formal/SubQuorum/MultiplePositiveSaturation.lean proves finite-list census
identities, the conditional sourcewise dimension-count injection, the
resulting zero-reserve bound and exact demand/failure criteria. Its
zero-reserve-to-physical-gate and source-normalization adapters are the
written proof in Section2 and the preceding gate notes. It is not an
end-to-end formal theorem about arbitrary physical fusions.

All15 declarations compile locally with Lean4.33.0, and their individual
axiom audits PASS without sorryAx/native_decide. Controls PASS on87381
source censuses,844686 reserve margins,5461 parity partitions and672
complete physical images. The56 zero-reserve images include32 isolated
positive-array images; none has a marked zero-reserve gate. There are56
physical images with double-marked sources, all with nonzero reserve.
See output/multiple-positive-saturation-controls.json and
output/multiple-positive-saturation-formal-check.json. The preceding
source-local geometry revieweb184fae completed ACCEPT separately; it is
not a review verdict for this new multiple-positive deduction.

The unrestricted mixed joint allocation, physical low-defect demand
classification, and arbitrary-grid triple equality remain open.

Haobo Ma and Wenlin Zhang used AI tools for search, double-checking and proofreading.
