// Independent exhaustive evaluation of 20-vertex compositions.
// No local cap, deletion certificate, or composition theorem is assumed.
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

int main() {
    constexpr unsigned n = 20;
    constexpr std::uint32_t limit = 1u << n, universe = limit - 1;
    const std::array<const char*, 5> rows{
        "11001", "11010", "00011", "01111", "10111"};
    bool first_record = true;
    std::cout << "[\n";
    for (unsigned pattern = 0; pattern < 256; ++pattern) {
        std::array<std::uint32_t, n> adj{};
        auto edge = [&](unsigned x, unsigned y) {
            adj[x] |= 1u << y;
            adj[y] |= 1u << x;
        };
        for (unsigned offset : {0u, 10u})
            for (unsigned a = 0; a < 5; ++a)
                for (unsigned b = 0; b < 5; ++b)
                    if (rows[a][b] == '1') edge(offset + a, offset + 5 + b);
        unsigned bit = 0;
        for (unsigned offset : {0u, 10u})
            for (unsigned a = 0; a < 2; ++a)
                for (unsigned b = 0; b < 2; ++b, ++bit)
                    if (pattern & (1u << bit)) edge(offset + a, 10u - offset + 5u + b);
        std::vector<unsigned char> forming(limit, 0);
        unsigned beta = 0, sf = 0;
        std::array<unsigned, n + 1> histogram{};
        for (std::uint32_t selected = 0; selected < limit; ++selected) {
            std::uint32_t active = 0, scan = selected;
            bool dissociation = true;
            while (scan) {
                unsigned u = __builtin_ctz(scan);
                scan &= scan - 1;
                auto neighbors = adj[u] & selected;
                if (neighbors) active |= 1u << u;
                if (neighbors & (neighbors - 1)) dissociation = false;
            }
            const unsigned size = __builtin_popcount(selected);
            if (dissociation && size > beta) beta = size;
            bool forms = true;
            scan = universe ^ selected;
            while (scan) {
                unsigned x = __builtin_ctz(scan);
                scan &= scan - 1;
                auto neighbors = adj[x] & selected;
                if (!(neighbors & (neighbors - 1)) && !(neighbors & active)) {
                    forms = false;
                    break;
                }
            }
            forming[selected] = forms;
            if (!forms) continue;
            bool minimal = true;
            scan = selected;
            while (scan) {
                auto vertex = scan & -scan;
                scan -= vertex;
                // Every deletion has a smaller integer mask, already evaluated.
                if (forming[selected ^ vertex]) { minimal = false; break; }
            }
            if (minimal) {
                if (size > sf) sf = size;
                ++histogram[size];
            }
        }
        if (!first_record) std::cout << ",\n";
        first_record = false;
        std::cout << "  {\"pattern\":" << pattern << ",\"beta_2\":" << beta
                  << ",\"SF_2\":" << sf << ",\"subsets\":" << limit
                  << ",\"minimal_size_counts\":{";
        bool first_count = true;
        for (unsigned size = 0; size <= n; ++size) if (histogram[size]) {
            if (!first_count) std::cout << ',';
            first_count = false;
            std::cout << '\"' << size << "\":" << histogram[size];
        }
        std::cout << "}}";
        if (beta != 10 || sf != 12) return 2;
    }
    std::cout << "\n]\n";
}
