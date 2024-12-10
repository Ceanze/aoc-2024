def start_walk(grid: list[list[int]], x: int, y: int, length: int, previous: int) -> int:
    return walk(grid, x, y, length, previous, [])

def walk(grid: list[list[int]], x: int, y: int, length: int, previous: int, found: list[(int, int)]) -> int:
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return 0
    
    curr = grid[y][x]

    if curr == previous + 1 and curr == 9: # and (x, y) not in found:
        #found.append((x, y))
        return 1
    
    if curr == previous + 1 or length == 0:
        return walk(grid, x + 1, y, length + 1, curr, found) + walk(grid, x, y + 1, length + 1, curr, found) + walk(grid, x - 1, y, length + 1, curr, found) + walk(grid, x, y - 1, length + 1, curr, found)
    else:
        return 0

def part1():
    grid = [[int(item) for item in line.strip()] for line in open("input.txt").readlines()]
    
    lengths = [0 if grid[y][x] != 0 else start_walk(grid, x, y, 0, grid[y][x]) for y in range(len(grid)) for x in range(len(grid[y]))]

    print(lengths)
    print(sum(lengths))

def part2():
    # Same as part 1, just comment out the "found" logic in the walk function
    pass

part1()