// Exhaustive contact-pair audit for TWO_C10_LOCAL_COMPLETION.md.
// Build: c++ -O3 -std=c++17 develop/check_two_c10_contact_pairs.cpp -o /tmp/two-c10-contact-pairs
// Run:   /tmp/two-c10-contact-pairs

#include <algorithm>
#include <array>
#include <iostream>
#include <vector>

using namespace std;

vector<array<int, 10>> matchings;

void generate_matchings(vector<int> vertices, array<int, 10>& edges, int used) {
    if (vertices.empty()) {
        matchings.push_back(edges);
        return;
    }
    int first = vertices[0];
    for (int i = 1; i < (int)vertices.size(); ++i) {
        int second = vertices[i];
        edges[2 * used] = first;
        edges[2 * used + 1] = second;
        vector<int> rest;
        for (int j = 1; j < (int)vertices.size(); ++j)
            if (j != i) rest.push_back(vertices[j]);
        generate_matchings(rest, edges, used + 1);
    }
}

bool legal_owner_mask(int mask) {
    for (int i = 0; i < 10; ++i) {
        if (!(mask & (1 << i)) &&
            !(mask & (1 << ((i + 1) % 10))) &&
            !(mask & (1 << ((i + 2) % 10))))
            return false;
    }
    return true;
}

int repair_cost[1024];

int equal_edges(int bits, int offset) {
    int result = 0;
    for (int i = 0; i < 5; ++i)
        if (((bits >> (offset + i)) & 1) ==
            ((bits >> (offset + (i + 1) % 5)) & 1))
            ++result;
    return result;
}

int main() {
    array<int, 10> edges{};
    vector<int> vertices(10);
    for (int i = 0; i < 10; ++i) vertices[i] = i;
    generate_matchings(vertices, edges, 0);

    for (int mask = 0; mask < 1024; ++mask) {
        repair_cost[mask] = 99;
        int missing = (~mask) & 1023;
        for (int added = missing;; added = (added - 1) & missing) {
            if (legal_owner_mask(mask | added)) {
                int final_mask = mask | added;
                int even_count = 0;
                int odd_count = 0;
                for (int i = 0; i < 10; ++i)
                    if (final_mask & (1 << i))
                        ((i % 2) ? odd_count : even_count)++;
                if (even_count <= 4 && odd_count <= 4)
                    repair_cost[mask] = min(repair_cost[mask], __builtin_popcount((unsigned)added));
            }
            if (added == 0) break;
        }
    }

    vector<vector<int>> solutions(matchings.size());
    int exceptional = 0;
    for (int i = 0; i < (int)matchings.size(); ++i) {
        for (int bits = 0; bits < 1024; ++bits) {
            bool proper = true;
            for (int j = 0; j < 10; j += 2) {
                if (((bits >> matchings[i][j]) & 1) ==
                    ((bits >> matchings[i][j + 1]) & 1)) {
                    proper = false;
                    break;
                }
            }
            if (proper) solutions[i].push_back(bits);
        }
        bool good = false;
        for (int bits : solutions[i])
            if (equal_edges(bits, 0) <= 1 && equal_edges(bits, 5) <= 1)
                good = true;
        if (!good) ++exceptional;
    }

    long long pair_count = 0;
    for (int left = 0; left < (int)solutions.size(); ++left) {
        for (int right = 0; right < (int)solutions.size(); ++right) {
            bool found = false;
            for (int bits0 : solutions[left]) {
                for (int bits1 : solutions[right]) {
                    int total = 0;
                    for (int phase0 = 0; phase0 < 2; ++phase0) {
                        for (int phase1 = 0; phase1 < 2; ++phase1) {
                            int owner0 = 0;
                            int owner1 = 0;
                            for (int i = 0; i < 5; ++i) {
                                if (((bits0 >> i) & 1) ^ phase0)
                                    owner0 |= 1 << (2 * i);
                                if (((bits1 >> i) & 1) ^ phase1)
                                    owner0 |= 1 << (2 * i + 1);
                                if (((bits0 >> (5 + i)) & 1) ^ phase0)
                                    owner1 |= 1 << (2 * i);
                                if (((bits1 >> (5 + i)) & 1) ^ phase1)
                                    owner1 |= 1 << (2 * i + 1);
                            }
                            total += repair_cost[owner0] + repair_cost[owner1];
                        }
                    }
                    if (total <= 4) {
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
            if (!found) {
                cerr << "FAIL contact pair " << left << " " << right << "\n";
                return 1;
            }
            ++pair_count;
        }
    }

    cout << "PASS contact_matchings=" << matchings.size()
         << " exceptional=" << exceptional
         << " phase_pairs=" << pair_count << "\n";
}
