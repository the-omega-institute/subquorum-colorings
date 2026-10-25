import SubQuorum.FrozenCertificateReplay

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

namespace SubQuorum.FixedPMaximumFrozenElbow

abbrev Vertex := Fin 448

def vertex (n : Nat) : Vertex := ⟨n % 448, Nat.mod_lt _ (by decide)⟩

def selectedIndices : List Nat := [0, 3, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 24, 26, 27, 28, 30, 33, 35, 37, 39, 41, 44, 46, 48, 50, 53, 57, 59, 60, 62, 64, 66, 68, 70, 71, 73, 75, 77, 79, 80, 82, 83, 84, 86, 89, 97, 100, 102, 104, 106, 109, 112, 114, 116, 119, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 146, 148, 152, 154, 164, 167, 168, 170, 172, 175, 181, 184, 190, 193, 194, 196, 198, 200, 202, 204, 208, 210, 211, 213, 217, 219, 220, 223, 225, 227, 229, 231, 237, 240, 246, 249, 251, 252, 254, 256, 266, 267, 269, 273, 275, 276, 278, 281, 283, 285, 293, 296, 302, 305, 307, 308, 310, 312, 314, 316, 318, 320, 322, 323, 333, 335, 338, 340, 343, 345, 347, 349, 352, 360, 362, 364, 365, 367, 369, 370, 372, 374, 376, 378, 379, 381, 383, 385, 387, 389, 391, 394, 396, 399, 402, 405, 408, 410, 412, 414, 417, 420, 421, 423, 425, 426, 428, 429, 431, 432, 434, 435, 437, 439, 441, 443, 444, 446, 447]

def endpointIndices : List Nat := [90, 91, 92, 93, 94, 95, 96, 121, 122, 123, 149, 150, 151, 155, 156, 157, 158, 159, 160, 161, 162, 163, 177, 178, 179, 186, 187, 188, 205, 206, 207, 214, 215, 216, 233, 234, 235, 242, 243, 244, 259, 260, 261, 262, 263, 270, 271, 272, 286, 287, 288, 289, 290, 291, 292, 298, 299, 300, 326, 327, 328, 329, 330, 353, 354, 355, 356, 357, 358, 359]

def mateIndices : Array Nat := #[
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
  16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
  32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
  48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
  64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
  80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 91, 90, 93, 92, 122, 96,
  95, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
  112, 113, 114, 115, 116, 117, 118, 119, 120, 149, 94, 151, 124, 125, 126, 127,
  128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143,
  144, 145, 146, 147, 148, 121, 178, 123, 152, 153, 154, 156, 155, 158, 157, 187,
  161, 160, 163, 162, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
  176, 205, 150, 207, 180, 181, 182, 183, 184, 185, 214, 159, 216, 189, 190, 191,
  192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 177, 234, 179,
  208, 209, 210, 211, 212, 213, 186, 243, 188, 217, 218, 219, 220, 221, 222, 223,
  224, 225, 226, 227, 228, 229, 230, 231, 232, 261, 206, 263, 236, 237, 238, 239,
  240, 241, 270, 215, 272, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255,
  256, 257, 258, 260, 259, 233, 290, 235, 264, 265, 266, 267, 268, 269, 242, 299,
  244, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 287, 286,
  289, 288, 262, 292, 291, 293, 294, 295, 296, 297, 326, 271, 328, 301, 302, 303,
  304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319,
  320, 321, 322, 323, 324, 325, 298, 355, 300, 330, 329, 331, 332, 333, 334, 335,
  336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351,
  352, 354, 353, 327, 357, 356, 359, 358, 360, 361, 362, 363, 364, 365, 366, 367,
  368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383,
  384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399,
  400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415,
  416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431,
  432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447
]

def rankIndices : Array Nat := #[
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 6, 1, 6,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 4, 3, 4, 0, 0, 0, 0, 7, 1, 6, 2,
  6, 1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 3, 5, 3, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 3,
  0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 3, 6, 0, 0, 0, 0,
  0, 0, 5, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 1, 9, 2, 7, 2, 0, 0, 0, 0, 0, 0, 3, 6,
  3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10,
  1, 8, 1, 8, 0, 0, 0, 0, 0, 0, 7, 3, 7, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 2, 8, 2, 10, 1, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 9, 1, 9, 1, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def witnessX : Array Nat := #[
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 92, 64, 94, 66, 94,
  68, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 93, 121, 95, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 148, 122, 152, 0, 0, 0, 127, 157, 129, 159, 131,
  159, 133, 161, 135, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 149, 177, 151, 0, 0, 0, 0, 0, 0, 158, 186, 160, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 204, 178, 208,
  0, 0, 0, 0, 0, 0, 213, 187, 217, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 205, 233, 207, 0, 0, 0, 0,
  0, 0, 214, 242, 216, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 231, 261, 260, 234, 262, 0, 0, 0, 0, 0, 0, 269, 243,
  273, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 285, 259,
  287, 261, 291, 263, 293, 0, 0, 0, 0, 0, 270, 298, 272, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 327, 299, 327, 328, 302, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 352, 326, 354, 328, 358, 330, 360, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def witnessY : Array Nat := #[
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 89, 119, 91, 121, 95, 123,
  97, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 122, 123, 122, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 177, 149, 179, 0, 0, 0, 154, 184, 156, 186, 158,
  188, 162, 190, 164, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 178, 179, 178, 0, 0, 0, 0, 0, 0, 187, 188, 187, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 233, 205, 235,
  0, 0, 0, 0, 0, 0, 242, 214, 244, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 234, 235, 234, 0, 0, 0, 0,
  0, 0, 243, 244, 243, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 287, 288, 262, 261, 291, 0, 0, 0, 0, 0, 0, 298, 270,
  300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 314, 288,
  316, 290, 318, 290, 320, 0, 0, 0, 0, 0, 299, 300, 299, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 354, 326, 329, 357, 358, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 381, 355, 383, 355, 385, 357, 387, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def actualEdges : List (Vertex × Vertex) := [(vertex 94, vertex 122), (vertex 150, vertex 178), (vertex 206, vertex 234), (vertex 262, vertex 290), (vertex 121, vertex 149), (vertex 177, vertex 205), (vertex 233, vertex 261), (vertex 93, vertex 92), (vertex 91, vertex 90), (vertex 289, vertex 288), (vertex 287, vertex 286), (vertex 260, vertex 259), (vertex 96, vertex 95), (vertex 123, vertex 151), (vertex 292, vertex 291), (vertex 263, vertex 235), (vertex 179, vertex 207), (vertex 159, vertex 187), (vertex 215, vertex 243), (vertex 271, vertex 299), (vertex 327, vertex 355), (vertex 188, vertex 216), (vertex 244, vertex 272), (vertex 300, vertex 328), (vertex 160, vertex 161), (vertex 162, vertex 163), (vertex 356, vertex 357), (vertex 358, vertex 359), (vertex 329, vertex 330), (vertex 157, vertex 158), (vertex 186, vertex 214), (vertex 353, vertex 354), (vertex 326, vertex 298), (vertex 242, vertex 270), (vertex 155, vertex 156)]

def T (v : Vertex) : Prop := v.val ∈ selectedIndices

def P (v : Vertex) : Prop := v.val ∈ endpointIndices

instance (v : Vertex) : Decidable (T v) := inferInstanceAs (Decidable (v.val ∈ selectedIndices))
instance (v : Vertex) : Decidable (P v) := inferInstanceAs (Decidable (v.val ∈ endpointIndices))

def mate (v : Vertex) : Vertex := vertex (mateIndices[v.val]!)
def rank (v : Vertex) : Nat := rankIndices[v.val]!
def x (v : Vertex) : Vertex := vertex (witnessX[v.val]!)
def y (v : Vertex) : Vertex := vertex (witnessY[v.val]!)

/-- Four physical nearest neighbors, with no wrap across the board boundary. -/
def neighbors (v : Vertex) : List Vertex :=
  (if v.val % 28 > 0 then [vertex (v.val + 447)] else []) ++
  (if v.val % 28 < 27 then [vertex (v.val + 1)] else []) ++
  (if v.val ≥ 28 then [vertex (v.val + 420)] else []) ++
  (if v.val < 420 then [vertex (v.val + 28)] else [])

def E (v w : Vertex) : Prop := w ∈ neighbors v
instance (v w : Vertex) : Decidable (E v w) := inferInstanceAs (Decidable (w ∈ neighbors v))

def occupiedDegree (v : Vertex) : Nat :=
  ((neighbors v).filter fun w => decide (T w ∨ P w)).length

/-- Exact stored counts, with no duplicate selected or endpoint index. -/
theorem inventory :
    selectedIndices.length = 186 ∧ selectedIndices.Nodup ∧
    endpointIndices.length = 70 ∧ endpointIndices.Nodup ∧
    actualEdges.length = 35 := by decide

/-- Concrete physical feasibility of the selected vertices. -/
theorem selected_feasible : ∀ v : Vertex, T v → ¬ P v ∧ occupiedDegree v ≤ 1 := by
  decide

/-- The stored actual edges are physical, have the stored mates, and
cover each endpoint exactly once. The mate map is an involution. -/
theorem actual_matching :
    (actualEdges.all fun e => decide (E e.1 e.2 ∧ mate e.1 = e.2 ∧ mate e.2 = e.1)) = true ∧
    (actualEdges.flatMap fun e => [e.1.val,e.2.val]).Nodup ∧
    (∀ v : Vertex, P v ↔ v.val ∈ (actualEdges.flatMap fun e => [e.1.val,e.2.val])) ∧
    (∀ v : Vertex, mate (mate v) = v) := by decide

/-- Every one of the70 concrete endpoints has two distinct physical kept
neighbors, with a strictly earlier actual-mate rank for nonselected witnesses. -/
theorem strict_witness_checks : ∀ p : Vertex, P p →
    x p ≠ y p ∧ E p (x p) ∧ E p (y p) ∧
    FrozenCertificateReplay.Kept T P P mate rank p (x p) ∧
    FrozenCertificateReplay.Kept T P P mate rank p (y p) := by
  unfold FrozenCertificateReplay.Kept
  decide

theorem certificate : FrozenCertificateReplay.Certificate E T P P mate rank := by
  intro p hp
  exact ⟨x p,y p,strict_witness_checks p hp⟩

/-- Every predicate closed under the physical two-kept-neighbor freezing
rule contains all70 matching endpoints. This uses general rank soundness. -/
theorem completely_frozen (F : Vertex → Prop)
    (closed : ∀ p, P p → (∃ a b, a ≠ b ∧ E p a ∧ E p b ∧
      (T a ∨ F (mate a)) ∧ (T b ∨ F (mate b))) → F p) :
    ∀ p, P p → F p := by
  exact FrozenCertificateReplay.certificate_sound E T P P F mate rank certificate closed

end SubQuorum.FixedPMaximumFrozenElbow

#print axioms SubQuorum.FixedPMaximumFrozenElbow.inventory
#print axioms SubQuorum.FixedPMaximumFrozenElbow.selected_feasible
#print axioms SubQuorum.FixedPMaximumFrozenElbow.actual_matching
#print axioms SubQuorum.FixedPMaximumFrozenElbow.strict_witness_checks
#print axioms SubQuorum.FixedPMaximumFrozenElbow.certificate
#print axioms SubQuorum.FixedPMaximumFrozenElbow.completely_frozen
