// Independent literal-star checker for the on-demand transfer certificate.
// It does not import the optimized generator kernel or its state table.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Mask = std::uint32_t;
using Key = std::uint64_t;
using Values = std::unordered_map<Key, int>;
static constexpr Mask invalid = std::numeric_limits<Mask>::max();
static void require(bool test, const char* message) { if (!test) throw std::runtime_error(message); }

std::vector<std::vector<Mask>> stars(int h, int n) {
    int size = h * n;
    std::vector<std::vector<bool>> edge(size, std::vector<bool>(size));
    for (int v = 0; v < size; ++v) for (int w = 0; w < size; ++w)
        edge[v][w] = (v / h == w / h && std::abs(v % h - w % h) == 1)
                  || (v % h == w % h && std::abs(v / h - w / h) == 1);
    std::vector<std::vector<Mask>> result(size);
    for (int x = 0; x < size; ++x)
        for (int a = 0; a < size; ++a) if (a != x)
            for (int b = a + 1; b < size; ++b) if (b != x)
                if (int(edge[x][a]) + int(edge[x][b]) + int(edge[a][b]) >= 2)
                    result[x].push_back((Mask(1) << a) | (Mask(1) << b));
    return result;
}

bool formed(Mask selected, const std::vector<Mask>& pairs) {
    for (Mask pair : pairs) if ((selected & pair) == pair) return true;
    return false;
}

Mask literal_kernel(Mask selected, const std::vector<std::vector<Mask>>& local_stars, int h) {
    Mask flags = 0;
    for (int x = 2 * h; x < 3 * h; ++x) {
        if (selected & (Mask(1) << x)) {
            if (!formed(selected, local_stars[x])) flags |= Mask(1) << x;
        } else {
            Mask common = ~Mask(0); bool found = false;
            for (Mask pair : local_stars[x]) if ((selected & pair) == pair) {
                found = true; common &= pair;
                if (!common) break;
            }
            if (!found) return invalid;
            flags |= common;
        }
    }
    return flags;
}

int main(int argc, char** argv) {
    require(argc == 6, "usage: HEIGHT START PERIOD INCREMENT VECTOR_DIR");
    int h = std::stoi(argv[1]), start = std::stoi(argv[2]);
    int period = std::stoi(argv[3]), increment = std::stoi(argv[4]);
    require(3 <= h && h <= 6 && start >= 2 && period > 0 && start + period <= 100,
            "unsupported audit parameters");
    int end = start + period, retained = 4 * h;
    Key retained_mask = (Key(1) << retained) - 1;
    Mask column_mask = (Mask(1) << h) - 1;
    auto local_stars = stars(h, 5);
    auto step = [&](Key state, Mask column, bool real, Key& target) {
        Mask window = Mask(state & retained_mask) | (column << retained);
        Mask witnessed = Mask(state >> retained);
        if (real) {
            Mask flags = literal_kernel(window, local_stars, h);
            if (flags == invalid) return false;
            witnessed |= flags;
        }
        if ((window & ~witnessed & column_mask) != 0) return false;
        target = Key(window >> h) + (Key(witnessed >> h) << retained);
        return true;
    };
    auto closes = [&](Key state, int length) {
        for (int j = 0; j < 4; ++j) {
            Key target; int centre = length + j - 2;
            if (!step(state, 0, 0 <= centre && centre < length, target)) return false;
            state = target;
        }
        return state == 0;
    };
    std::size_t subset_controls = 0, minimal_sets = 0;
    int control_limit = h <= 5 ? 4 : 3;
    for (int n = 1; n <= control_limit; ++n) {
        auto board_stars = stars(h, n);
        std::size_t masks = std::size_t(1) << (h * n);
        std::vector<bool> forms(masks);
        for (Mask selected = 0; selected < masks; ++selected) {
            bool forming = true;
            for (int x = 0; x < h * n; ++x)
                if (!(selected & (Mask(1) << x)) && !formed(selected, board_stars[x])) {
                    forming = false; break;
                }
            forms[selected] = forming; bool minimal = forming;
            for (int x = 0; minimal && x < h * n; ++x)
                if ((selected & (Mask(1) << x)) && forms[selected ^ (Mask(1) << x)]) minimal = false;
            Key state = 0; bool accepts = true;
            for (int c = 0; c < n; ++c) {
                Key target;
                if (!step(state, (selected >> (h * c)) & column_mask, c >= 2, target)) {
                    accepts = false; break;
                }
                state = target;
            }
            accepts = accepts && closes(state, n);
            require(minimal == accepts, "whole-board minimality/transfer mismatch");
            ++subset_controls; if (minimal) ++minimal_sets;
        }
    }
    auto path = [&](int n) {
        return std::string(argv[5]) + "/grid-star-h" + std::to_string(h) + "-v" + std::to_string(n) + ".tsv";
    };
    auto check_endpoint = [&](const Values& values, int n) {
        std::ifstream file(path(n)); require(bool(file), "missing endpoint vector");
        Key key = 0, last = 0; int score; std::size_t count = 0; std::string line;
        while (std::getline(file, line)) {
            std::istringstream row(line); std::string extra;
            require(bool(row >> key >> score) && !(row >> extra), "malformed endpoint row");
            require(!count || last < key, "noncanonical endpoint keys");
            require(key < (Key(1) << (2 * retained)), "key out of range");
            require(((key >> retained) & ~(key & retained_mask)) == 0, "invalid witness flags");
            auto entry = values.find(key);
            require(entry != values.end() && entry->second == score, "endpoint value mismatch");
            last = key; ++count;
        }
        require(file.eof() && count == values.size(), "endpoint support mismatch");
    };
    Values values{{0, 0}}; std::vector<int> optima; std::size_t states = 0;
    for (int n = 1; n <= end; ++n) {
        Values next; next.reserve(std::min<std::size_t>(12000001, values.size() * 2));
        for (const auto& [state, score] : values)
            for (Mask column = 0; column <= column_mask; ++column) {
                Key target;
                if (step(state, column, n >= 3, target)) {
                    int candidate = score + __builtin_popcount(column);
                    auto [entry, fresh] = next.emplace(target, candidate);
                    if (!fresh) entry->second = std::max(entry->second, candidate);
                    require(next.size() <= 12000000, "reference state resource limit");
                }
            }
        values = std::move(next); int best = -1;
        for (const auto& [state, score] : values) if (closes(state, n)) best = std::max(best, score);
        optima.push_back(best);
        if (n == start || n == end) { check_endpoint(values, n); states = values.size(); }
        std::cerr << "reference height=" << h << " length=" << n << " states=" << values.size()
                  << " SF=" << best << std::endl;
    }
    std::ifstream first(path(start)), last(path(end)); Key a, b; int x, y; std::size_t pairs = 0;
    std::string first_line, last_line;
    while (std::getline(first, first_line)) {
        require(bool(std::getline(last, last_line)), "missing translated row");
        std::istringstream row_first(first_line), row_last(last_line); std::string extra;
        require(bool(row_first >> a >> x) && !(row_first >> extra), "malformed first vector row");
        require(bool(row_last >> b >> y) && !(row_last >> extra), "malformed last vector row");
        require(a == b && y == x + increment, "vector translation mismatch");
        ++pairs;
    }
    require(first.eof(), "invalid first endpoint read");
    require(!std::getline(last, last_line) && last.eof() && pairs == states, "extra endpoint entries");
    std::cout << "{\n  \"status\": \"PASS\",\n  \"kernel\": \"literal-on-demand\",\n  \"height\": " << h
              << ",\n  \"whole_board_subset_acceptance_comparisons\": " << subset_controls
              << ",\n  \"whole_board_minimal_sets\": " << minimal_sets
              << ",\n  \"complete_prefixes_rebuilt\": " << end
              << ",\n  \"endpoint_states\": " << states
              << ",\n  \"start\": " << start << ",\n  \"period\": " << period
              << ",\n  \"increment\": " << increment << ",\n  \"optima\": [";
    for (std::size_t i = 0; i < optima.size(); ++i) { if (i) std::cout << ", "; std::cout << optima[i]; }
    std::cout << "]\n}\n";
}
