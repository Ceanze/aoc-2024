from functools import cache

towels = []

def parse():
    local_towels, patterns = open("input.txt").read().split("\n\n")
    local_towels = local_towels.split(", ")
    patterns = [pattern for pattern in patterns.splitlines()]

    # Put the "towels" list in global variable, as it cannot be cached by the @cache
    global towels
    towels = local_towels
    return patterns

@cache
def check(pattern: str):
    if pattern == "":
        # Reached the end
        return 1

    count = 0
    for towel in towels:
        new = pattern.removeprefix(towel)
        if new != pattern:
            count += check(new)

    return count

def part1():
    total = 0
    for pattern in parse():
        total += 1 if check(pattern) > 0 else 0

    print(total)

def part2():
    total = 0
    for pattern in parse():
        total += check(pattern)

    print(total)

part1()
part2()