import time

found = []

def count_antinodes(lines: list[list[str]], x: int, y: int):
    count = 0
    for row_idx, row in enumerate(lines):
        for col_idx, col in enumerate(row):
            if (col_idx, row_idx) == (x, y):
                return count

            flipped_delta = (x - col_idx, y - row_idx)
            anti_pos = (x + flipped_delta[0], y + flipped_delta[1])
            curr_val = col
            checking_val = lines[y][x]

            if 0 <= anti_pos[0] < len(row) and 0 <= anti_pos[1] < len(lines):
                anti_val = lines[anti_pos[1]][anti_pos[0]]

                if curr_val == checking_val:
                    if anti_pos not in found:
                        count += 1
                        found.append(anti_pos)
                if anti_val == checking_val:
                    if (col_idx, row_idx) not in found:
                        count += 1
                        found.append((col_idx, row_idx))

    return None

def part1():
    start_time = time.time()
    lines = [list(line.strip()) for line in open("input.txt").readlines()]

    total_antinodes = 0
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col != ".":
                total_antinodes += count_antinodes(lines, x, y)

    exec_time = time.time() - start_time

    print(total_antinodes)
    print(f"Execution time: {exec_time}")

# Sometimes the more straightfoward solution is just simply better
def part2():
    start_time = time.time()
    lines = [list(line.strip()) for line in open("input.txt").readlines()]

    total_antinodes = 0
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col != ".":
                for inner_y, inner_row in enumerate(lines):
                    for inner_x, inner_col in enumerate(inner_row):
                        if inner_col == col and (inner_x, inner_y) != (x, y):
                            delta = (inner_x - x, inner_y - y)
                            pos = (x, y)

                            while True:
                                if 0 <= pos[0] < len(row) and 0 <= pos[1] < len(lines):
                                    if pos not in found:
                                        found.append(pos)
                                        total_antinodes += 1
                                    pos = (pos[0] + delta[0], pos[1] + delta[1])
                                else:
                                    break




    exec_time = time.time() - start_time

    print(total_antinodes)
    print(f"Execution time: {exec_time}")

part2()