def generate_sparse_disk_map(dense_disk_map: str) -> list[str]:
    sparse_disk_map = []

    id = 0
    is_free_space = False
    for digit in dense_disk_map:
        for idx in range(0, int(digit)):
            if not is_free_space:
                sparse_disk_map.append(id)
            else:
                sparse_disk_map.append(".")

        if not is_free_space:
            id += 1

        is_free_space = not is_free_space

    return sparse_disk_map

def defrag_disk_map(disk_map: list[str]) -> list[str]:
    previous_idx = 0
    for idx, val in enumerate(disk_map[previous_idx:]):
        print(f"Defragging: {idx}/{len(disk_map)}")
        if val == ".":
            previous_idx = idx
            for reversed_idx, reversed_val in enumerate(disk_map[::-1]):
                actual_idx = len(disk_map) - reversed_idx - 1
                if reversed_val != ".":
                    # print(val, idx, reversed_val, actual_idx)
                    disk_map[idx] = reversed_val
                    disk_map[actual_idx] = "."
                    # print(disk_map)
                    break
                elif idx == actual_idx:
                    break

    return disk_map


def defrag_disk_map_segmented(dense_disk_map: str) -> list[str]:
    disk_map = [[(int(i)//2) for _ in range(int(x))] if i % 2 == 0 else ['.' for _ in range(int(x))] for i, x in enumerate(dense_disk_map)]

    for val in reversed(disk_map):
        if len(val) > 0 and val.count(".") == 0:
            for left_val in disk_map[:disk_map.index(val)]:
                num_spaces = left_val.count(".")
                if 0 < num_spaces >= len(val):
                    disk_map[disk_map.index(val)] = ["."] * len(val)
                    disk_map[disk_map.index(left_val)] = left_val[:left_val.index(".")] + [val[0]] * len(val) + ["."] * (num_spaces - len(val))
                    break

    s = [str(item) for sublist in disk_map for item in sublist]

    return s


def calculate_checksum(disk_map: list[str]) -> int:
    total = 0
    for idx, val in enumerate(disk_map):
        if val == ".":
            continue
        total += idx * int(val)
    return total


def part1():
    dense_disk_map = open("input.txt").read().strip()

    sparse_disk_map = generate_sparse_disk_map(dense_disk_map)
    disk_map = defrag_disk_map(sparse_disk_map)
    checksum = calculate_checksum(disk_map)
    print(checksum)

def part2():
    dense_disk_map = open("input.txt").read().strip()

    disk_map = defrag_disk_map_segmented(dense_disk_map)
    checksum = calculate_checksum(disk_map)
    print(checksum)
    pass

part2()