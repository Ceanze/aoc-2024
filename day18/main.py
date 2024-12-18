from dataclasses import dataclass
import heapq

@dataclass
class Grid:
    grid: list[list[str]]

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y])

    def is_wall(self, x: int, y: int) -> bool:
        return self.is_valid(x, y) and self.grid[y][x] == "#"

    def is_end(self, pos: tuple[int, int]) -> bool:
        return self.is_valid(pos[0], pos[1]) and self.grid[pos[1]][pos[0]] == "E"

    def is_empty(self, x: int, y: int) -> bool:
        return self.is_valid(x, y) and self.grid[y][x] == "."

    def get_start_pos(self) -> tuple[int, int]:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == "S":
                    return (x, y)

        return None

    def get_end_pos(self) -> tuple[int, int]:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == "E":
                    return (x, y)

        return None

    def swap(self, x1: int, y1: int, x2: int, y2: int):
        if self.is_valid(x1, y1) and self.is_valid(x2, y2):
            temp = self.grid[y1][x1]
            self.grid[y1][x1] = self.grid[y2][x2]
            self.grid[y2][x2] = temp

    def __str__(self):
        out = ""
        for row in self.grid:
            line = ""
            for val in row:
                line += val
            out += line + "\n"
        return out

def parse() -> Grid:
    blockers = open("input.txt").readlines()

    blockers = [(int(blocker.split(",")[0]), int(blocker.split(",")[1])) for blocker in blockers]
    return blockers

def calc_score():
    return 1

def dijkstra(grid: Grid, starts: list[tuple[int, int]]):
    scores = {}

    priority_queue = []

    for start in starts:
        scores[start] = 0
        heapq.heappush(priority_queue, (0, start))

    while priority_queue:
        current_score, current_node = heapq.heappop(priority_queue)

        if current_score > scores.get(current_node, float("inf")):
            continue

        for x_delta, y_delta in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            x = current_node[0] + x_delta
            y = current_node[1] + y_delta
            neighbor = (x, y)
            if grid.is_valid(x, y) and not grid.is_wall(x, y):
                weight = calc_score()
                score = current_score + weight

                if score < scores.get((neighbor), float("inf")):
                    scores[neighbor] = score
                    heapq.heappush(priority_queue, (score, neighbor))

    return scores

def place_blockers(grid: Grid, blockers: list[tuple[int, int]], start: int, num: int):
    for blocker_idx in range(start, num):
        blocker = blockers[blocker_idx]
        grid.grid[blocker[1]][blocker[0]] = "#"

def part1():
    blockers = parse()
    grid_width, grid_height = 71, 71
    grid = Grid([["." for x in range(grid_width)] for y in range(grid_height)])
    place_blockers(grid, blockers, 0, 1024)

    start_pos = (0, 0)
    last_idx = len(grid.grid) - 1
    end_pos = (last_idx, last_idx)
    scores = dijkstra(grid, [start_pos])

    steps = scores[end_pos]

    print(steps)

# Slow but works
def part2():
    blockers = parse()
    grid_width, grid_height = 71, 71
    grid = Grid([["." for x in range(grid_width)] for y in range(grid_height)])

    start_pos = (0, 0)
    last_idx = len(grid.grid) - 1
    end_pos = (last_idx, last_idx)
    for blocker_num, blocker in enumerate(blockers):
        place_blockers(grid, blockers, blocker_num, blocker_num + 1)
        scores = dijkstra(grid, [start_pos])

        if scores.get(end_pos, None) == None:
            print(f"Blocker num {blocker_num} (count: {blocker_num + 1}) can't reach with coord {blocker}")
            return

part2()