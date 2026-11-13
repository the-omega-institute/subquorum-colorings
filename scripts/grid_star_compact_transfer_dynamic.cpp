// Exact grid deletion-witness frontier with on-demand local windows.
//
// This is the width-six companion to grid_star_compact_transfer.cpp.  The
// older implementation materialises all 2^(5h) local windows.  For h=6 that
// is 2^30 entries, so this version evaluates the same optimized kernel only
// for windows reached by the exact frontier.  The independent checker uses
// the literal star definition and reconstructs every prefix from scratch.
#include <algorithm>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using Word = std::uint64_t;
using Mask = std::uint32_t;
static unsigned key_bits;
static Word key_mask;
static unsigned grid_height;
static constexpr std::size_t state_cap = 50000000;

static Mask reflect_column(Mask column) {
    Mask result = 0;
    for (unsigned r = 0; r < grid_height; ++r)
        if (column & (Mask(1) << r)) result |= Mask(1) << (grid_height - 1 - r);
    return result;
}

static Word reflect_key(Word key) {
    const Word column_mask = (Word(1) << grid_height) - 1;
    Word result = 0;
    for (unsigned c = 0; c < 4; ++c) {
        Mask selected = Mask((key >> (c * grid_height)) & column_mask);
        Mask flags = Mask((key >> (4 * grid_height + c * grid_height)) & column_mask);
        result |= Word(reflect_column(selected)) << (c * grid_height);
        result |= Word(reflect_column(flags)) << (4 * grid_height + c * grid_height);
    }
    return result;
}

static Word canonical_key(Word key) {
    Word reflected = reflect_key(key);
    return std::min(key, reflected);
}

struct Table {
    std::vector<Word> slots;
    std::size_t used = 0;
    explicit Table(std::size_t capacity = 256) : slots(capacity) {}
    static Word hash(Word x) {
        x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27; x *= 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    void put_unchecked(Word key, int value) {
        std::size_t i = hash(key) & (slots.size() - 1);
        while (slots[i] && (slots[i] & key_mask) != key)
            i = (i + 1) & (slots.size() - 1);
        if (!slots[i]) { ++used; slots[i] = key | (Word(value + 1) << key_bits); }
        else if (int(slots[i] >> key_bits) - 1 < value)
            slots[i] = key | (Word(value + 1) << key_bits);
    }
    void put(Word key, int value) {
        if ((used + 1) * 10 > slots.size() * 7) {
            if (slots.size() >= (Word(1) << 25))
                throw std::runtime_error("slot limit exceeded; no successful result");
            Table bigger(slots.size() * 2);
            for (Word entry : slots) if (entry)
                bigger.put_unchecked(entry & key_mask, int(entry >> key_bits) - 1);
            *this = std::move(bigger);
        }
        put_unchecked(key, value);
        if (used > state_cap)
            throw std::runtime_error("state limit exceeded; no successful result");
    }
    int get(Word key) const {
        std::size_t i = hash(key) & (slots.size() - 1);
        while (slots[i]) {
            if ((slots[i] & key_mask) == key) return int(slots[i] >> key_bits) - 1;
            i = (i + 1) & (slots.size() - 1);
        }
        return -1;
    }
    std::vector<Word> entries() const {
        std::vector<Word> result; result.reserve(used);
        for (Word entry : slots) if (entry) result.push_back(entry);
        return result;
    }
};

// Same optimized local rule as the original generator.  It is evaluated only
// for a window that occurs in an exact transition.  Vertical reflection is
// an automorphism of the strip; canonicalizing after each transition keeps
// both reflected states at one score-maximizing table entry.
static Mask optimized_kernel(Mask selected, const std::vector<Mask>& adj, int h) {
    const Mask invalid = std::numeric_limits<Mask>::max();
    Mask flags = 0;
    for (int x = 2 * h; x < 3 * h; ++x) {
        Mask near = adj[x] & selected, bit = Mask(1) << x;
        if (selected & bit) {
            if (!near || (!(near & (near - 1)) && (adj[__builtin_ctz(near)] & selected) == bit))
                flags |= bit;
        } else if (!near) {
            return invalid;
        } else if (!(near & (near - 1))) {
            Mask partners = adj[__builtin_ctz(near)] & selected;
            if (!partners) return invalid;
            flags |= near;
            if (!(partners & (partners - 1))) flags |= partners;
        } else if (!((near & (near - 1)) & ((near & (near - 1)) - 1))) {
            Mask first = near & -near, second = near ^ first;
            if (!(adj[__builtin_ctz(first)] & selected)) flags |= second;
            if (!(adj[__builtin_ctz(second)] & selected)) flags |= first;
        }
    }
    return flags;
}

int main(int argc, char** argv) {
    if (argc != 4) throw std::invalid_argument("usage: HEIGHT LIMIT OUTPUT_DIR");
    int h = std::stoi(argv[1]), limit = std::stoi(argv[2]);
    if (h < 3 || h > 6 || limit < 6 || limit > 100)
        throw std::invalid_argument("require 3<=height<=6, 6<=limit<=100");
    grid_height = unsigned(h);
    const int period = h == 4 ? 2 : 3, increment = h == 3 ? 5 : h == 4 ? 4 : 8;
    const unsigned retained = 4 * h, vertices = 5 * h;
    const Mask column_mask = (Mask(1) << h) - 1;
    const Word retained_mask = (Word(1) << retained) - 1;
    key_bits = 2 * retained; key_mask = (Word(1) << key_bits) - 1;
    if (key_bits + 10 >= 64) throw std::runtime_error("packed score overflow risk");
    std::vector<Mask> adj(vertices);
    for (int c = 0; c < 5; ++c) for (int r = 0; r < h; ++r) {
        int x = c * h + r;
        if (c) adj[x] |= Mask(1) << (x - h);
        if (c < 4) adj[x] |= Mask(1) << (x + h);
        if (r) adj[x] |= Mask(1) << (x - 1);
        if (r + 1 < h) adj[x] |= Mask(1) << (x + 1);
    }
    auto step = [&](Word key, Mask column, bool real, Word& target) {
        Mask s = Mask(key & retained_mask) | (column << retained);
        Mask flags = Mask(key >> retained);
        if (real) {
            flags |= optimized_kernel(s, adj, h);
            if (flags == std::numeric_limits<Mask>::max()) return false;
        }
        if ((s & column_mask) != (flags & column_mask)) return false;
        target = canonical_key(Word(s >> h) | (Word(flags >> h) << retained));
        return true;
    };
    auto closes = [&](Word key, int n) {
        for (int j = 0; j < 4; ++j) {
            Word target;
            if (!step(key, 0, 0 <= n + j - 2 && n + j - 2 < n, target)) return false;
            key = target;
        }
        return key == 0;
    };
    std::filesystem::path out(argv[3]);
    if (std::filesystem::exists(out)) throw std::runtime_error("output directory must be fresh");
    std::filesystem::create_directories(out);
    Table table; table.put(canonical_key(0), 0);
    std::vector<std::vector<Word>> history(period);
    std::vector<int> values;
    bool translated = false; int start = 0; std::size_t peak = 0;
    for (int n = 1; n <= limit; ++n) {
        Table next;
        for (Word entry : table.slots) if (entry) {
            Word key = entry & key_mask; int value = int(entry >> key_bits) - 1;
            for (Mask column = 0; column <= column_mask; ++column) {
                Word target;
                if (step(key, column, n >= 3, target))
                    next.put(target, value + __builtin_popcount(column));
            }
        }
        table = std::move(next); peak = std::max(peak, table.used);
        int best = -1;
        for (Word entry : table.slots) if (entry && closes(entry & key_mask, n))
            best = std::max(best, int(entry >> key_bits) - 1);
        values.push_back(best);
        auto& previous = history[n % period];
        std::size_t mismatch = 0;
        if (previous.empty() || previous.size() != table.used) mismatch = table.used + 1;
        else for (Word entry : previous)
            if (table.get(entry & key_mask) != int(entry >> key_bits) - 1 + increment) ++mismatch;
        std::cerr << "height=" << h << " length=" << n << " SF=" << best
                  << " reachable=" << table.used << " mismatches=" << mismatch << std::endl;
        if (!mismatch && n - period >= 2) {
            start = n - period; translated = true;
            auto save = [&](std::vector<Word> rows, int length) {
                std::sort(rows.begin(), rows.end(), [](Word a, Word b) {
                    return (a & key_mask) < (b & key_mask);
                });
                std::ofstream file(out / ("grid-star-h" + std::to_string(h) + "-v" + std::to_string(length) + ".tsv"));
                for (Word entry : rows) file << (entry & key_mask) << '\t' << (int(entry >> key_bits) - 1) << '\n';
                if (!file) throw std::runtime_error("vector write failed");
            };
            save(std::move(previous), start); save(table.entries(), n); break;
        }
        previous = table.entries();
    }
    if (!translated) throw std::runtime_error("no full-vector certificate within requested limit");
    std::ofstream report(out / "report.json");
    report << "{\n  \"status\": \"PASS\",\n  \"kernel\": \"on-demand-optimized\",\n  \"height\": " << h
           << ",\n  \"start\": " << start << ",\n  \"period\": " << period
           << ",\n  \"increment\": " << increment
           << ",\n  \"quotient\": \"vertical-reflection\""
           << ",\n  \"states\": " << table.used << ",\n  \"peak_states\": " << peak
           << ",\n  \"state_cap\": " << state_cap << "\n}\n";
    if (!report) throw std::runtime_error("report write failed");
    std::cout << "PASS height=" << h << " start=" << start << " period=" << period << std::endl;
}
