def calc(x):
    x = ((x << 6) ^ x) & 0xFFFFFF
    x = ((x >> 5) ^ x) & 0xFFFFFF
    return ((x << 11) ^ x) & 0xFFFFFF

def part1():
    secrets = [int(line.strip()) for line in open("input.txt").readlines()]

    steps = 2000
    for idx, _ in enumerate(secrets):
        for _ in range(steps):
            secrets[idx] = calc(secrets[idx])

    print(sum(secrets))

def part2():
    secrets = [int(line.strip()) for line in open("input.txt").readlines()]

    pattern_sums = {}
    steps = 2000
    for idx, secret in enumerate(secrets):
        results = [secret]
        for _ in range(steps):
            results.append(calc(results[-1]))

        # Calc differences
        diffs = [(x % 10) - (y % 10) for x, y in zip(results, results[1:])]

        sequence_len = 4
        patterns_seen = set()
        for i in range(len(results) - sequence_len):
            pattern = tuple(diffs[i:i + 4])

            # Only count each pattern once
            if pattern not in patterns_seen:
                pattern_sums[pattern] = pattern_sums.get(pattern, 0) + (results[i + 4] % 10)
                patterns_seen.add(pattern)

    print(max(pattern_sums.values()))

part2()