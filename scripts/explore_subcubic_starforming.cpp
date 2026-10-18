#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

using Mask = std::uint32_t;

bool forms(const std::vector<Mask>& adjacency, Mask selected) {
    for (unsigned outside = 0; outside < adjacency.size(); ++outside) {
        if (selected & (Mask{1} << outside)) continue;
        Mask neighbors = adjacency[outside] & selected;
        if (std::popcount(neighbors) >= 2) continue;
        if (!neighbors || !(adjacency[std::countr_zero(neighbors)] & selected)) return false;
    }
    return true;
}

bool check(const std::vector<Mask>& adjacency, bool report = false) {
    Mask limit = Mask{1} << adjacency.size();
    int beta = 0;
    int star = 0;
    Mask beta_set = 0;
    Mask star_set = 0;
    std::vector<bool> forming(limit);
    for (Mask selected = 0; selected < limit; ++selected) {
        forming[selected] = forms(adjacency, selected);
        int size = std::popcount(selected);
        if (size <= beta) continue;
        bool dissociation = true;
        for (unsigned vertex = 0; vertex < adjacency.size(); ++vertex) {
            if ((selected & (Mask{1} << vertex)) && std::popcount(adjacency[vertex] & selected) > 1) {
                dissociation = false;
                break;
            }
        }
        if (dissociation) { beta = size; beta_set = selected; }
    }
    for (Mask selected = 0; selected < limit; ++selected) {
        if (!forming[selected] || std::popcount(selected) <= star) continue;
        bool minimal = true;
        for (Mask remaining = selected; remaining; remaining &= remaining - 1) {
            Mask removed = remaining & -remaining;
            if (forming[selected ^ removed]) { minimal = false; break; }
        }
        if (minimal) { star = std::popcount(selected); star_set = selected; }
    }
    if (star <= beta && !report) return false;
    std::cout << "{\"beta\":" << beta << ",\"SF\":" << star
              << ",\"beta_mask\":" << beta_set << ",\"star_mask\":" << star_set << ",\"adjacency\":[";
    for (unsigned vertex = 0; vertex < adjacency.size(); ++vertex) {
        if (vertex) std::cout << ',';
        std::cout << adjacency[vertex];
    }
    std::cout << "]}" << std::endl;
    return true;
}

int main(int argc, char** argv) {
    if (argc > 1 && std::string(argv[1]) == "--two-block-cycle") {
        std::vector<Mask> adjacency(22);
        std::vector<Mask> base = {2048,896,3584,1344,1152,2176,8,50,10,6,28,37};
        std::vector<int> core = {1,2,3,4,5,7,8,9,10,11};
        for (int block = 0; block < 2; ++block) {
            std::vector<int> image(12);
            image[0] = 20 + (block + 1) % 2;
            image[6] = 20 + block;
            for (int position = 0; position < 10; ++position) image[core[position]] = 10 * block + position;
            for (int vertex = 0; vertex < 12; ++vertex) {
                for (int neighbor = vertex + 1; neighbor < 12; ++neighbor) {
                    if (!(base[vertex] & (Mask{1} << neighbor))) continue;
                    adjacency[image[vertex]] |= Mask{1} << image[neighbor];
                    adjacency[image[neighbor]] |= Mask{1} << image[vertex];
                }
            }
        }
        check(adjacency, true);
        return 0;
    }
    int half = argc > 1 ? std::stoi(argv[1]) : 6;
    int trials = argc > 2 ? std::stoi(argv[2]) : 10000;
    int minimum = argc > 3 ? std::stoi(argv[3]) : 0;
    if (half < 1 || half > 10 || trials < 1 || minimum < 0 || minimum > 3) return 2;
    int checked = 0;
    std::mt19937 generator(20261019);
    std::vector<int> permutation(half);
    std::iota(permutation.begin(), permutation.end(), 0);
    for (int trial = 0; trial < trials; ++trial) {
        std::vector<Mask> adjacency(2 * half);
        for (int matching = 0; matching < 3; ++matching) {
            std::shuffle(permutation.begin(), permutation.end(), generator);
            for (int row = 0; row < half; ++row) {
                if (generator() % 10 < static_cast<unsigned>(trial % 5)) continue;
                int neighbor = half + permutation[row];
                adjacency[row] |= Mask{1} << neighbor;
                adjacency[neighbor] |= Mask{1} << row;
            }
        }
        if (std::any_of(adjacency.begin(), adjacency.end(), [minimum](Mask neighbors) {
            return std::popcount(neighbors) < minimum;
        })) continue;
        ++checked;
        if (check(adjacency)) {
            std::cerr << "seed=20261019 trial=" << trial << " half=" << half << '\n';
            return 0;
        }
    }
    std::cout << "{\"generated\":" << trials << ",\"checked\":" << checked
              << ",\"minimum_degree\":" << minimum << ",\"half\":" << half
              << ",\"seed\":20261019,\"counterexample_found\":false}" << std::endl;
}
