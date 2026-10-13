#include <cstdint>
#include <iostream>
#include <array>

using Mask = std::uint32_t;

bool forms(const std::array<Mask, 20>& adjacency, Mask selected) {
    for (int outside = 0; outside < 20; ++outside) {
        if ((selected >> outside) & 1U) continue;
        Mask neighbors = adjacency[outside] & selected;
        if (__builtin_popcount(neighbors) >= 2) continue;
        bool covered = false;
        for (int center = 0; center < 20; ++center) {
            if (((neighbors >> center) & 1U) && (adjacency[center] & selected)) {
                covered = true;
                break;
            }
        }
        if (!covered) return false;
    }
    return true;
}

int main() {
    std::array<Mask, 20> adjacency{};
    const std::array<const char*, 5> matrix = {"11001", "11010", "00011", "01111", "10111"};
    auto add_edge = [&](int first, int second) {
        adjacency[first] |= Mask(1) << second;
        adjacency[second] |= Mask(1) << first;
    };
    for (int block = 0; block < 2; ++block)
        for (int row = 0; row < 5; ++row)
            for (int column = 0; column < 5; ++column)
                if (matrix[row][column] == '1') add_edge(10 * block + row, 10 * block + 5 + column);
    add_edge(5, 10);
    add_edge(15, 0);
    int beta = 0, star_number = 0;
    std::array<int, 21> counts{};
    for (Mask selected = 0; selected < (Mask(1) << 20); ++selected) {
        int size = __builtin_popcount(selected);
        bool independent = true;
        for (int vertex = 0; vertex < 20; ++vertex)
            if (((selected >> vertex) & 1U) && __builtin_popcount(adjacency[vertex] & selected) > 1) {
                independent = false;
                break;
            }
        if (independent && size > beta) beta = size;
        if (!forms(adjacency, selected)) continue;
        bool minimal = true;
        for (int vertex = 0; vertex < 20; ++vertex)
            if (((selected >> vertex) & 1U) && forms(adjacency, selected ^ (Mask(1) << vertex))) {
                minimal = false;
                break;
            }
        if (minimal) {
            ++counts[size];
            if (size > star_number) star_number = size;
        }
    }
    std::cout << "{\"order\":20,\"beta_2\":" << beta << ",\"SF_2\":" << star_number
              << ",\"minimal_set_counts\":{";
    bool first_entry = true;
    for (int size = 0; size <= 20; ++size) if (counts[size]) {
        if (!first_entry) std::cout << ",";
        std::cout << "\"" << size << "\":" << counts[size];
        first_entry = false;
    }
    std::cout << "}}\n";
    return beta == 10 && star_number == 12 ? 0 : 1;
}
