def index(rules: list[str]) -> dict:
    index = {}
    for rule in rules:
        splitted = rule.split("|")
        num = splitted[0]
        min_num = splitted[1]

        if index.get(int(num)) is None:
            index[int(num)] = [int(min_num)]
        else:
            index[int(num)].append(int(min_num))

    return index

def get_filtered_manuals(indexed: dict, manuals: list[str], get_correct: bool) -> list[list[int]]:
    filtered_manuals = []

    for manual in manuals:
        splitted_manual = manual.split(",")

        current_manual = []
        valid = True
        for num in splitted_manual:
            if int(num) in indexed:
                for min_num in indexed[int(num)]:
                    if min_num in current_manual:
                        valid = False

            current_manual.append(int(num))

        if valid and get_correct or not valid and not get_correct:
            filtered_manuals.append(current_manual)

    return filtered_manuals

def add_centers(manuals: list[list[int]]) -> int:
    total = 0
    for manual in manuals:
        total += manual[len(manual) // 2]

    return total

def reorder(indexed: dict, manuals: list[list[int]]) -> list[list[int]]:
    for manual in manuals:
        for i in range(len(manual) - 1, -1, -1):
            for j in range(0, i, 1):
                if manual[i] in indexed:
                    for min_num in indexed[manual[i]]:
                        if manual[j] == min_num:
                            temp = manual[j]
                            manual[j] = manual[i]
                            manual[i] = temp

    return manuals



def part1():
    input = ""
    with open("input.txt") as f:
        input = f.read()

    parts = input.split("\n\n")

    rules = parts[0].split("\n")
    manuals = parts[1].split("\n")

    indexed = index(rules)

    correct_manuals = get_filtered_manuals(indexed, manuals, True)
    added_centers = add_centers(correct_manuals)
    print(added_centers)

def part2():
    input = ""
    with open("input.txt") as f:
        input = f.read()

    parts = input.split("\n\n")

    rules = parts[0].split("\n")
    manuals = parts[1].split("\n")

    indexed = index(rules)
    invalid_manuals = get_filtered_manuals(indexed, manuals, False)
    reordered_manuals = reorder(indexed, invalid_manuals)
    added_centers = add_centers(reordered_manuals)
    print(added_centers)


part2()

# 4 3 2 1