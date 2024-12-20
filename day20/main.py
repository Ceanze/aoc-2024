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

def calc_score():
    return 1

def dijkstra(grid: Grid, starts: list[tuple[int, int]]):
    scores = {}
    previous_nodes = {}

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
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (score, neighbor))

    return scores, previous_nodes

def taxicab_distance(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def find_cheats(scores: dict, nodes: list[tuple[int, int]], cheat_time: int) -> dict:
    cheats = {}
    for node_idx, node in enumerate(nodes):
        for other_node in nodes[node_idx:]:
            cheat_distance = taxicab_distance(other_node, node)
            if 0 < cheat_distance <= cheat_time:
                saved_time = scores[other_node] - (scores[node] + cheat_distance)
                cheats[saved_time] = cheats.get(saved_time, 0) + 1

    return cheats

def run(cheat_time: int):
    grid = parse()

    start_pos = grid.get_start_pos()
    scores, nodes = dijkstra(grid, [start_pos])
    nodes = [start_pos] + [node for node in nodes]

    cheats = find_cheats(scores, nodes, cheat_time)

    count = sum([count if time >= 100 else 0 for time, count in cheats.items()])
    print(count)


def part1():
    run(2)

def part2():
    run(20)

part1()
part2()