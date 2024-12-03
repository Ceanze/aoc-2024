def is_safe(levels: list[int]) -> bool:
    # Calculate the difference between each report
    differences = [first - second for first, second in zip(levels, levels[1:])]

    max_difference = 3
    return (all(0 < difference <= max_difference for difference in differences)
            or all(-max_difference <= difference < 0 for difference in differences))

def part1():
    with open("input.txt") as levels:
        safe_reports = 0
        for level in levels:
            if is_safe(list(map(int, level.split()))):
                safe_reports += 1

    print(safe_reports)

def part2():
    with open("input.txt") as levels:
        safe_reports = 0
        for level in levels:
            level = list(map(int, level.split()))

            for i in range(len(level)):
                if is_safe(level[:i] + level[i + 1:]):
                    print(level[:i] + level[i + 1:])
                    safe_reports += 1
                    break

    print(safe_reports)



part2()