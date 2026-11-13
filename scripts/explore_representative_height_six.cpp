#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

constexpr int H = 6;
using Mask = std::uint8_t;

struct Option {
    std::uint16_t labels;
    Mask occupied;
    Mask right;
    Mask base_one;
    std::uint8_t t_count;
    std::uint8_t vertical_count;
    std::uint8_t seam_flags;
};

struct StateValue {
    int score;
    Mask base_one;
};

std::array<int, H> decode(std::uint16_t code) {
    std::array<int, H> labels{};
    for (int row = 0; row < H; ++row) {
        labels[row] = code % 3;
        code /= 3;
    }
    return labels;
}

std::uint16_t encode(const std::array<int, H>& labels) {
    std::uint16_t code = 0;
    std::uint16_t power = 1;
    for (int row = 0; row < H; ++row) {
        code += power * labels[row];
        power *= 3;
    }
    return code;
}

Mask occupied(const std::array<int, H>& labels) {
    Mask result = 0;
    for (int row = 0; row < H; ++row)
        if (labels[row] != 0) result |= Mask(1) << row;
    return result;
}

bool vertical(const std::array<int, H>& labels, Mask left, Mask right,
              int& count, Mask& seams) {
    for (int row = 0; row < H; ++row) {
        if ((left >> row & 1) && labels[row] != 2) return false;
        if ((right >> row & 1) && labels[row] != 2) return false;
    }
    if (left & right) return false;

    Mask remaining = 0;
    for (int row = 0; row < H; ++row)
        if (labels[row] == 2 && !(left >> row & 1) && !(right >> row & 1))
            remaining |= Mask(1) << row;

    count = 0;
    seams = 0;
    for (int row = 0; row < H; ++row) {
        if (!(remaining >> row & 1)) continue;
        if (row + 1 >= H || !(remaining >> (row + 1) & 1)) return false;
        remaining &= ~((Mask(1) << row) | (Mask(1) << (row + 1)));
        ++count;
        if (row == 1) seams |= 1;
        if (row == 3) seams |= 2;
    }
    return true;
}

bool option_for(const std::array<int, H>& labels, Mask previous_occupied,
                Mask left, Mask right, Option& result) {
    int vertical_count = 0;
    Mask seams = 0;
    if (!vertical(labels, left, right, vertical_count, seams)) return false;
    Mask occ = occupied(labels);
    Mask base_one = 0;
    for (int row = 0; row < H; ++row) {
        if (labels[row] != 1) continue;
        int base = 0;
        if (row > 0 && (occ >> (row - 1) & 1)) ++base;
        if (row + 1 < H && (occ >> (row + 1) & 1)) ++base;
        if (previous_occupied >> row & 1) ++base;
        if (base > 1) return false;
        if (base == 1) base_one |= Mask(1) << row;
    }
    result = Option{
        encode(labels), occ, right, base_one,
        static_cast<std::uint8_t>(std::count(labels.begin(), labels.end(), 1)),
        static_cast<std::uint8_t>(vertical_count), seams,
    };
    return true;
}

std::uint64_t key(std::uint16_t labels, Mask previous_occupied, Mask left,
                  Mask right, Mask flags) {
    return labels | (std::uint64_t(previous_occupied) << 10)
        | (std::uint64_t(left) << 16) | (std::uint64_t(right) << 22)
        | (std::uint64_t(flags) << 28);
}

void unpack(std::uint64_t value, std::uint16_t& labels, Mask& previous_occupied,
            Mask& left, Mask& right, Mask& flags) {
    labels = value & ((1u << 10) - 1);
    previous_occupied = (value >> 10) & 63;
    left = (value >> 16) & 63;
    right = (value >> 22) & 63;
    flags = (value >> 28) & 3;
}

struct WidthResult {
    std::array<int, 4> maxima;
    std::size_t states;
    std::unordered_map<std::uint64_t, StateValue> values;
};

WidthResult solve(int width) {
    std::array<std::vector<Option>, 4096> options;
    for (std::uint16_t code = 0; code < 729; ++code) {
        auto labels = decode(code);
        for (int previous = 0; previous < 64; ++previous)
            for (int left = 0; left < 64; ++left)
                for (int right = 0; right < 64; ++right) {
                    Option option{};
                    if (option_for(labels, previous, left, right, option))
                        options[previous | (left << 6)].push_back(option);
                }
    }

    std::unordered_map<std::uint64_t, StateValue> current;
    current.reserve(1000000);
    const auto initial = options[0];
    for (const Option& option : initial) {
        auto state = key(option.labels, 0, 0, option.right, option.seam_flags);
        int score = option.t_count + option.vertical_count;
        current[state] = StateValue{score, option.base_one};
    }

    for (int column = 1; column < width; ++column) {
        std::unordered_map<std::uint64_t, StateValue> next;
        next.reserve(current.size() * 2);
        for (const auto& [state, value] : current) {
            std::uint16_t labels_code = 0;
            Mask previous_occupied = 0, left = 0, right = 0, flags = 0;
            unpack(state, labels_code, previous_occupied, left, right, flags);
            auto labels = decode(labels_code);
            Mask current_occupied = occupied(labels);
            const auto& candidates = options[current_occupied | (right << 6)];
            for (const Option& option : candidates) {
                if (option.occupied & value.base_one) continue;
                auto next_state = key(
                    option.labels, current_occupied, right, option.right,
                    flags | option.seam_flags
                );
                int next_score = value.score + option.t_count
                    + option.vertical_count + __builtin_popcount(right);
                auto found = next.find(next_state);
                if (found == next.end() || next_score > found->second.score)
                    next[next_state] = StateValue{next_score, option.base_one};
            }
        }
        current.swap(next);
        std::cerr << "width=" << width << " column=" << (column + 1)
                  << " states=" << current.size() << '\n';
    }

    std::array<int, 4> maxima{-1, -1, -1, -1};
    for (const auto& [state, value] : current) {
        std::uint16_t labels = 0;
        Mask previous = 0, left = 0, right = 0, flags = 0;
        unpack(state, labels, previous, left, right, flags);
        if (right == 0) maxima[flags] = std::max(maxima[flags], value.score);
    }
    return WidthResult{maxima, current.size(), std::move(current)};
}

struct TranslationCheck {
    int from;
    int to;
    bool same_support;
    bool constant_increment;
    int increment;
    int minimum_delta;
    int maximum_delta;
    std::size_t from_states;
    std::size_t to_states;
};

TranslationCheck compare_translation(const WidthResult& from,
                                     const WidthResult& to,
                                     int from_width, int to_width) {
    bool same_support = from.values.size() == to.values.size();
    bool constant_increment = same_support;
    int increment = 0;
    int minimum_delta = 0;
    int maximum_delta = 0;
    bool first = true;
    for (const auto& [state, value] : from.values) {
        auto it = to.values.find(state);
        if (it == to.values.end()) {
            same_support = false;
            constant_increment = false;
            continue;
        }
        int delta = it->second.score - value.score;
        if (first) {
            minimum_delta = maximum_delta = delta;
        } else {
            minimum_delta = std::min(minimum_delta, delta);
            maximum_delta = std::max(maximum_delta, delta);
        }
        if (first) {
            increment = delta;
            first = false;
        } else if (delta != increment) {
            constant_increment = false;
        }
    }
    if (!same_support) constant_increment = false;
    return TranslationCheck{from_width, to_width, same_support,
                            constant_increment, increment,
                            minimum_delta, maximum_delta,
                            from.values.size(), to.values.size()};
}

bool run_potential_certificate(const char* certificate_path) {
    auto even = solve(4);
    auto odd = solve(5);

    std::vector<std::uint64_t> states;
    states.reserve(even.values.size());
    std::unordered_map<std::uint64_t, std::size_t> index;
    index.reserve(even.values.size() * 2);
    for (const auto& [state, value] : even.values) {
        index.emplace(state, states.size());
        states.push_back(state);
    }

    std::array<std::vector<Option>, 4096> options;
    for (std::uint16_t code = 0; code < 729; ++code) {
        auto labels = decode(code);
        for (int previous = 0; previous < 64; ++previous)
            for (int left = 0; left < 64; ++left)
                for (int right = 0; right < 64; ++right) {
                    Option option{};
                    if (option_for(labels, previous, left, right, option))
                        options[previous | (left << 6)].push_back(option);
                }
    }

    const long long NEG = std::numeric_limits<long long>::lowest() / 4;
    std::size_t missing_transitions = 0;
    auto apply_one = [&](const std::vector<long long>& input) {
        std::vector<long long> output(states.size(), NEG);
        for (std::size_t i = 0; i < states.size(); ++i) {
            std::uint16_t labels = 0;
            Mask previous = 0, left = 0, right = 0, flags = 0;
            unpack(states[i], labels, previous, left, right, flags);
            auto decoded = decode(labels);
            Mask current_occupied = occupied(decoded);
            const auto& candidates = options[current_occupied | (right << 6)];
            const Mask base_one = [&] {
                Mask answer = 0;
                for (int row = 0; row < H; ++row) {
                    if (decoded[row] != 1) continue;
                    int base = 0;
                    if (row > 0 && (current_occupied >> (row - 1) & 1)) ++base;
                    if (row + 1 < H && (current_occupied >> (row + 1) & 1)) ++base;
                    if (previous >> row & 1) ++base;
                    if (base == 1) answer |= Mask(1) << row;
                }
                return answer;
            }();
            for (const Option& option : candidates) {
                if (option.occupied & base_one) continue;
                auto next = key(option.labels, current_occupied, right,
                                option.right, flags | option.seam_flags);
                auto found = index.find(next);
                if (found == index.end()) {
                    ++missing_transitions;
                    continue;
                }
                const int reward = option.t_count + option.vertical_count
                    + __builtin_popcount(right);
                if (input[found->second] != NEG)
                    output[i] = std::max(output[i],
                                         static_cast<long long>(reward)
                                             + input[found->second]);
            }
        }
        return output;
    };

    std::vector<long long> potential(states.size(), 0);
    int iterations = 0;
    for (; iterations < 100; ++iterations) {
        auto once = apply_one(potential);
        auto twice = apply_one(once);
        long long largest_increase = 0;
        for (std::size_t i = 0; i < states.size(); ++i) {
            long long candidate = twice[i] - 6;
            largest_increase = std::max(largest_increase,
                                        candidate - potential[i]);
            potential[i] = std::max(potential[i], candidate);
        }
        std::cerr << "potential_iteration=" << (iterations + 1)
                  << " largest_increase=" << largest_increase << '\n';
        if (largest_increase <= 0) break;
    }

    auto once = apply_one(potential);
    auto twice = apply_one(once);
    long long raw_largest_violation = std::numeric_limits<long long>::lowest();
    for (std::size_t i = 0; i < states.size(); ++i)
        raw_largest_violation = std::max(raw_largest_violation,
                                         twice[i] - 6 - potential[i]);
    long long largest_violation = std::max(0LL, raw_largest_violation);

    long long min_final = std::numeric_limits<long long>::max();
    for (std::size_t i = 0; i < states.size(); ++i) {
        std::uint16_t labels = 0;
        Mask previous = 0, left = 0, right = 0, flags = 0;
        unpack(states[i], labels, previous, left, right, flags);
        if (right == 0) min_final = std::min(min_final, potential[i]);
    }
    long long even_start = std::numeric_limits<long long>::lowest();
    long long odd_start = std::numeric_limits<long long>::lowest();
    bool odd_support_in_stable = odd.values.size() == states.size();
    for (const auto& [state, value] : odd.values)
        if (!index.contains(state)) odd_support_in_stable = false;
    for (const auto& [state, value] : even.values)
        even_start = std::max(even_start,
                              static_cast<long long>(value.score)
                                  + potential[index.at(state)]);
    for (const auto& [state, value] : odd.values)
        odd_start = std::max(odd_start,
                             static_cast<long long>(value.score)
                                 + potential[index.at(state)]);

    std::cout << "potential_states=" << states.size()
              << " iterations=" << (iterations + 1)
              << " missing_transitions=" << missing_transitions
              << " largest_violation=" << largest_violation
              << " raw_largest_violation=" << raw_largest_violation
              << " min_final=" << min_final
              << " even_constant=" << (even_start - min_final)
              << " odd_constant=" << (odd_start - min_final)
              << " odd_support_in_stable=" << (odd_support_in_stable ? 1 : 0)
              << '\n';

    const bool pass =
        missing_transitions == 0 && raw_largest_violation <= 0
        && min_final == 0 && even_start - min_final == 12
        && odd_start - min_final == 16 && odd_support_in_stable;

    if (certificate_path != nullptr) {
        std::vector<std::pair<std::uint64_t, long long>> rows;
        rows.reserve(states.size());
        for (std::size_t i = 0; i < states.size(); ++i)
            rows.emplace_back(states[i], potential[i]);
        std::sort(rows.begin(), rows.end());
        std::ofstream certificate(certificate_path);
        if (!certificate) return false;
        certificate << "# representative-height-six-two-seam potential v1\n";
        certificate << "# states " << states.size() << "\n";
        certificate << "# two_column_increment 6\n";
        certificate << "# even_seed_width 4\n";
        certificate << "# odd_seed_width 5\n";
        certificate << "# even_constant " << (even_start - min_final) << '\n';
        certificate << "# odd_constant " << (odd_start - min_final) << '\n';
        certificate << "state potential\n";
        for (const auto& [state, value] : rows)
            certificate << state << ' ' << value << '\n';
    }
    return pass;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc > 1 && std::string(argv[1]) == "--potential") {
        return run_potential_certificate(argc > 2 ? argv[2] : nullptr) ? 0 : 1;
    }
    int maximum_width = argc > 1 ? std::stoi(argv[1]) : 4;
    std::ofstream report;
    if (argc > 2) report.open(argv[2]);
    if (report) report << "{\n  \"status\": \"PASS\",\n  \"rows\": [\n";

    std::vector<WidthResult> results;
    results.reserve(maximum_width);
    for (int width = 1; width <= maximum_width; ++width) {
        auto result = solve(width);
        results.push_back(std::move(result));
        const auto& stored = results.back();
        std::cout << "width=" << width << " no=" << stored.maxima[0]
                  << " seam23=" << stored.maxima[1]
                  << " seam45=" << stored.maxima[2]
                  << " both=" << stored.maxima[3]
                  << " states=" << stored.states << '\n';
        if (report) {
            if (width > 1) report << ",\n";
            report << "    {\"width\": " << width
                   << ", \"F_6_n\": " << (width % 2 ? 3 * width + 1 : 3 * width)
                   << ", \"max_by_flag\": [" << stored.maxima[0] << ", "
                   << stored.maxima[1] << ", " << stored.maxima[2] << ", "
                   << stored.maxima[3] << "]"
                   << ", \"states\": " << stored.states << "}";
        }
    }
    if (report) {
        report << "\n  ],\n  \"translations\": [\n";
        bool first = true;
        for (int width = 1; width + 2 <= maximum_width; ++width) {
            auto check = compare_translation(results[width - 1],
                                             results[width + 1],
                                             width, width + 2);
            if (!first) report << ",\n";
            first = false;
            report << "    {\"from\": " << check.from
                   << ", \"to\": " << check.to
                   << ", \"same_support\": "
                   << (check.same_support ? "true" : "false")
                   << ", \"constant_increment\": "
                   << (check.constant_increment ? "true" : "false")
                   << ", \"increment\": " << check.increment
                   << ", \"minimum_delta\": " << check.minimum_delta
                   << ", \"maximum_delta\": " << check.maximum_delta
                   << ", \"from_states\": " << check.from_states
                   << ", \"to_states\": " << check.to_states << "}";
        }
        report << "\n  ]\n}\n";
    }
}
