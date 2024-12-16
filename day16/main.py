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
    grid_input = open("input.txt").read()

    grid = Grid([[val for val in line] for line in grid_input.splitlines()])
    return grid

# Calculates the score from one pos to another - always moving one tile is assumed
def calc_score(from_pos: tuple[int, int], to_pos: tuple[int, int], curr_direction: str):
    score = 1 # Always move one tile

    # Check any rotations (+1000 score)
    x_delta = to_pos[0] - from_pos[0]
    y_delta = to_pos[1] - from_pos[1]
    if curr_direction == "^":
        if x_delta != 0:
            return score + 1000
        if y_delta > 0:
            return score + 2000
    elif curr_direction == ">":
        if y_delta != 0:
            return score + 1000
        if x_delta < 0:
            return score + 2000
    elif curr_direction == "v":
        if x_delta != 0:
            return score + 1000
        if y_delta < 0:
            return score + 2000
    elif curr_direction == "<":
        if y_delta != 0:
            return score + 1000
        if x_delta > 0:
            return score + 2000

    return score

def get_direction(x_delta: int, y_delta: int):
    if x_delta > 0:
        return ">"
    if x_delta < 0:
        return "<"
    if y_delta > 0:
        return "v"
    if y_delta < 0:
        return "^"
    return None

def dijkstra(grid: Grid, starts: list[tuple[int, int]], start_dirs: list[str]):
    scores = {}

    priority_queue = []

    flip_dir = {"^": "v", ">": "<", "v": "^", "<": ">"}

    for start, start_dir in zip(starts, start_dirs):
        scores[start, start_dir] = 0
        heapq.heappush(priority_queue, (0, start, start_dir))

    while priority_queue:
        current_score, current_node, current_direction = heapq.heappop(priority_queue)

        if current_score > scores.get((current_node, current_direction), float("inf")):
            continue

        for x_delta, y_delta in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            if flip_dir[get_direction(x_delta, y_delta)] == current_direction:
                continue

            x = current_node[0] + x_delta
            y = current_node[1] + y_delta
            neighbor = (x, y)
            if grid.is_valid(x, y) and not grid.is_wall(x, y):
                weight = calc_score(current_node, (x, y), current_direction)
                score = current_score + weight
                new_direction = get_direction(x_delta, y_delta)

                if score < scores.get((neighbor, new_direction), float("inf")):
                    scores[(neighbor, new_direction)] = score
                    heapq.heappush(priority_queue, (score, neighbor, new_direction))

    return scores

def part1():
    grid = parse()
    start_pos = grid.get_start_pos()
    end_pos = grid.get_end_pos()
    scores = dijkstra(grid, [start_pos], [">"])

    best = 100000000000
    for dir in "^>v<":
        if (end_pos, dir) in scores:
            best = min(best, scores[(end_pos, dir)])

    print(best)
    return best

def part2():
    grid = parse()
    start_pos = grid.get_start_pos()
    end_pos = grid.get_end_pos()
    scores_from_start = dijkstra(grid, [start_pos], [">"])
    scores_from_end = dijkstra(grid, [end_pos, end_pos, end_pos, end_pos], [">", "^", "<", "v"])

    best_score = part1()

    print(scores_from_start)

    visited_nodes = set()
    flip_dir = {"^": "v", ">": "<", "v": "^", "<": ">"}
    for y in range(len(grid.grid)):
        for x in range(len(grid.grid[y])):
            for dir in "^>v<":
                current_node = ((x, y), dir)
                dirs = "^>v<"
                for rev_dir in dirs:
                    reverse_node = ((x, y), rev_dir)
                    if current_node in scores_from_start and reverse_node in scores_from_end:
                        total_score = scores_from_start[current_node] + scores_from_end[reverse_node]
                        if total_score <= best_score:
                            visited_nodes.add((x, y))

    # Debug
    for node in visited_nodes:
        grid.grid[node[1]][node[0]] = "O"
    print(grid)

    print(len(visited_nodes))

part2()