visited: list[(int, int)] = []

def get_borders(grid: list[list[int]], x: int, y: int) -> list[str]:
    borders = []
    if y - 1 < 0 or grid[y - 1][x] != grid[y][x]:
        borders.append("up")
    if x + 1 >= len(grid[y]) or grid[y][x + 1] != grid[y][x]:
        borders.append("right")
    if y + 1 >= len(grid) or grid[y + 1][x] != grid[y][x]:
        borders.append("down")
    if x - 1 < 0 or grid[y][x - 1] != grid[y][x]:
        borders.append("left")

    return borders

def start_count(grid: list[list[int]], x: int, y: int, region: str) -> tuple[int, int]:
    corners = {}
    area, perimiter = count(grid, x, y, region, corners)

    corner_count = 0
    for pos, hits in corners.items():
        if hits == 2:
            x, y = pos
            if x - 1 >= 0 and y - 1 >= 0 and y < len(grid) and x < len(grid[y]):
                if grid[y - 1][x - 1] == grid[y][x] or (grid[y - 1][x - 1] != grid[y][x] and (grid[y - 1][x - 1] != region and grid[y][x] != region)):
                    corner_count += 2
        elif hits == 1 or hits == 3:
            corner_count += 1

    return (area, corner_count)

# Returns (area, perimiter) and (border_mask, unique_borders)
def count(grid: list[list[int]], x: int, y: int, region: str, corners: dict) -> tuple[int, int]:
    # print(f"Checking {x}, {y} for region {region}")
    # Out of bonds - perimiter + 1
    if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
        return (0, 1)
    
    curr = grid[y][x]

    # Not same region - perimiter + 1
    if curr != region:
        return (0, 1)

    if (x, y) in visited:
        return (0, 0)
    visited.append((x, y))

    corners[(x, y)] = corners.get((x, y), 0) + 1
    corners[(x+1, y)] = corners.get((x+1, y), 0) + 1
    corners[(x, y+1)] = corners.get((x, y+1), 0) + 1
    corners[(x+1, y+1)] = corners.get((x+1, y+1), 0) + 1
    
    right = count(grid, x + 1, y, region, corners)
    down = count(grid, x, y + 1, region, corners)
    left = count(grid, x - 1, y, region, corners)
    up = count(grid, x, y - 1, region, corners)

    area_perm = tuple(map(sum, zip(right, down, left, up)))
    return (area_perm[0] + 1, area_perm[1])

def part1():
    grid = [[item for item in line.strip()] for line in open("input.txt").readlines()]
    
    area_perim = [count(grid, x, y, grid[y][x], []) for y in range(len(grid)) for x in range(len(grid[y]))]

    prices = [area * perim for area, perim in area_perim]

    print(sum(prices))

def part2():
    grid = [[item for item in line.strip()] for line in open("input.txt").readlines()]
    
    area_corners = [start_count(grid, x, y, grid[y][x]) for y in range(len(grid)) for x in range(len(grid[y]))]

    prices = [area * corner for area, corner in area_corners]

    print(area_corners)
    print(sum(prices))

part2()