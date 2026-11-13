#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;

struct Result {
    int closed = -1;
    int boundary_bb = -1;
    std::size_t feasible = 0;
};

static bool feasible(Mask t, Mask p, const std::vector<Mask>& adj) {
    Mask occupied = t | p;
    for (unsigned v = 0; v < adj.size(); ++v)
        if ((t & (Mask(1) << v)) && __builtin_popcount(adj[v] & occupied) > 1)
            return false;
    return true;
}

static void enumerate_matchings(unsigned edge, const std::vector<std::pair<unsigned,unsigned>>& edges,
                                Mask used, Mask p, unsigned n, const std::vector<Mask>& adj,
                                Result& result) {
    if (edge == edges.size()) {
        Mask remaining = ((Mask(1) << (2 * n)) - 1) ^ p;
        for (Mask t = remaining;; t = (t - 1) & remaining) {
            if (feasible(t, p, adj)) {
                ++result.feasible;
                int score = __builtin_popcount(t) + __builtin_popcount(p) / 2;
                result.closed = std::max(result.closed, score);
                bool boundary_ok = true;
                for (unsigned c = 0; c < n; c += 2)
                    if ((t | p) & (Mask(3) << (2 * c))) boundary_ok = false;
                if (boundary_ok) result.boundary_bb = std::max(result.boundary_bb, score);
            }
            if (t == 0) break;
        }
        return;
    }
    enumerate_matchings(edge + 1, edges, used, p, n, adj, result);
    auto [a, b] = edges[edge];
    Mask endpoints = (Mask(1) << a) | (Mask(1) << b);
    if (!(used & endpoints))
        enumerate_matchings(edge + 1, edges, used | endpoints, p | endpoints, n, adj, result);
}

int main() {
    for (unsigned n = 1; n <= 6; ++n) {
        std::vector<Mask> adj(2 * n);
        std::vector<std::pair<unsigned,unsigned>> edges;
        auto add = [&](unsigned a, unsigned b) {
            adj[a] |= Mask(1) << b; adj[b] |= Mask(1) << a; edges.emplace_back(a, b);
        };
        for (unsigned c = 0; c < n; ++c) {
            add(2 * c, 2 * c + 1);
            if (c) { add(2 * (c - 1), 2 * c); add(2 * (c - 1) + 1, 2 * c + 1); }
        }
        Result result;
        enumerate_matchings(0, edges, 0, 0, n, adj, result);
        int expected_closed = (n % 2 == 0) ? int(n) : int(n + 1);
        int expected_boundary = (n % 2 == 0) ? result.boundary_bb : int(n - 1);
        if (result.closed != expected_closed || (n % 2 && result.boundary_bb != expected_boundary))
            throw std::runtime_error("two-row control failed");
        std::cout << "n=" << n << " closed=" << result.closed
                  << " odd_boundary_BB=" << result.boundary_bb
                  << " feasible=" << result.feasible << '\n';
    }
    std::cout << "PASS width-six no-crossing local controls\n";
}
