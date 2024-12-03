import re

def parse_action(line: str) -> tuple[int, int]:
    mul = r"mul\((\d+),(\d+)\)"
    matches = re.findall(mul, line)

    result = [(int(x), int(y)) for x, y in matches]

    return result

def part1():
    with open("input.txt") as file:
        lines = "".join(file.readlines())

        mults = parse_action(lines)

        total: int = 0
        for mult in mults:
            total += mult[0] * mult[1]

        print(total)

def part2():
    with open("input.txt") as file:
        lines = "".join(file.readlines())
        total = 0

        regex = r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))"
        matches = re.finditer(regex, lines)

        enabled = True
        for match in matches:
            if match.group(1):
                enabled = True
            elif match.group(2):
                enabled = False
            elif match.group(3) and enabled:
                total += int(match.group(4)) * int(match.group(5))
            
        print(total)
    

part2()