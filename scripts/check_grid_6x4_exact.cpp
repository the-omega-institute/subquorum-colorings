// Literal exhaustive control for the 6 by 4 rectangle.
// It checks every subset for two-star formation, inclusion-minimality, and
// dissociation.  This is a finite control, not an all-width theorem.
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;

int main(int argc, char** argv) {
    const int h = 6, w = 4, n = h * w;
    const Mask all = (Mask(1) << n) - 1;
    std::vector<Mask> adj(n);
    for (int c = 0; c < w; ++c) for (int r = 0; r < h; ++r) {
        int x = c * h + r;
        if (c) adj[x] |= Mask(1) << (x - h);
        if (c + 1 < w) adj[x] |= Mask(1) << (x + h);
        if (r) adj[x] |= Mask(1) << (x - 1);
        if (r + 1 < h) adj[x] |= Mask(1) << (x + 1);
    }
    std::vector<std::uint8_t> forming(std::size_t(1) << n, 0);
    std::uint64_t forming_count = 0, minimal_count = 0;
    int sf = 0; Mask sf_example = 0;
    for (Mask s = 0; s <= all; ++s) {
        bool ok = true;
        for (int x = 0; x < n && ok; ++x) if (!(s & (Mask(1) << x))) {
            Mask near = adj[x] & s;
            bool formed = __builtin_popcount(near) >= 2;
            while (!formed && near) {
                int u = __builtin_ctz(near); near &= near - 1;
                formed = (adj[u] & s) != 0;
            }
            ok = formed;
        }
        forming[s] = static_cast<std::uint8_t>(ok);
        if (!ok) continue;
        ++forming_count;
        bool minimal = true;
        for (Mask bits = s; bits && minimal; bits &= bits - 1) {
            int x = __builtin_ctz(bits);
            minimal = !forming[s ^ (Mask(1) << x)];
        }
        if (minimal) {
            ++minimal_count;
            int size = __builtin_popcount(s);
            if (size > sf) { sf = size; sf_example = s; }
        }
    }
    int beta = 0; Mask beta_example = 0;
    for (Mask s = 0; s <= all; ++s) {
        int size = __builtin_popcount(s);
        if (size <= beta) continue;
        bool ok = true;
        for (Mask bits = s; bits && ok; bits &= bits - 1) {
            int x = __builtin_ctz(bits);
            ok = __builtin_popcount(adj[x] & s) <= 1;
        }
        if (ok) { beta = size; beta_example = s; }
    }
    std::string report = argc == 2 ? argv[1] : "";
    if (!report.empty()) {
        std::ofstream out(report);
        if (!out) throw std::runtime_error("cannot open report");
        out << "{\n  \"status\": \"PASS\",\n  \"height\": 6,\n  \"width\": 4,\n"
            << "  \"subsets\": " << (std::uint64_t(1) << n)
            << ",\n  \"forming_sets\": " << forming_count
            << ",\n  \"minimal_forming_sets\": " << minimal_count
            << ",\n  \"SF2\": " << sf << ",\n  \"beta2\": " << beta
            << ",\n  \"SF2_example_mask\": " << sf_example
            << ",\n  \"beta2_example_mask\": " << beta_example << "\n}\n";
    }
    std::cout << "PASS 6x4 subsets=" << (std::uint64_t(1) << n)
              << " forming=" << forming_count << " minimal=" << minimal_count
              << " SF2=" << sf << " beta2=" << beta << '\n';
}
