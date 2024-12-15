from dataclasses import dataclass

@dataclass
class Grid:
    grid: list[list[str]]
    robot_pos: tuple[int, int] = None

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y])

    def is_wall(self, x: int, y: int) -> bool:
        return self.is_valid(x, y) and self.grid[y][x] == "#"

    def is_box(self, x: int, y: int) -> bool:
        if self.is_valid(x, y):
            if self.grid[y][x] == "O":
                return True
            if self.grid[y][x] == "[" or self.grid[y][x] == "]":
                return True
        return False

    def is_empty(self, x: int, y: int) -> bool:
        return self.is_valid(x, y) and self.grid[y][x] == "."

    def get_robot_pos(self) -> tuple[int, int]:
        if self.robot_pos != None:
            return self.robot_pos

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == "@":
                    self.set_robot_pos(x, y)
                    return (x, y)

        return None

    def set_robot_pos(self, x: int, y: int):
        self.robot_pos = (x, y)

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

def parse() -> tuple[Grid, str]:
    grid_input, moves = open("input.txt").read().split("\n\n")

    grid = Grid([[val for val in line] for line in grid_input.splitlines()])
    return (grid, moves)

def move(grid: Grid, x: int, y: int, delta_x: int, delta_y: int) -> bool:
    new_x, new_y = x + delta_x, y + delta_y
    if grid.is_empty(new_x, new_y):
        grid.swap(new_x, new_y, x, y)
        return True

    if grid.is_box(new_x, new_y):
        if move(grid, new_x, new_y, delta_x, delta_y):
            grid.swap(new_x, new_y, x, y)
            return True
        else:
            return False

    if grid.is_wall(new_x, new_y):
        return False
    return False

def can_move(grid: Grid, x: int, y: int, delta_x: int, delta_y: int) -> bool:
    new_x, new_y = x + delta_x, y + delta_y
    if grid.is_empty(new_x, new_y):
        return True

    if grid.is_box(new_x, new_y):
        possible_to_move = False
        if delta_y != 0:
            if grid.grid[new_y][new_x] == "[":
                possible_to_move |= can_move(grid, new_x + 1, new_y, delta_x, delta_y)
            else:
                possible_to_move |= can_move(grid, new_x - 1, new_y, delta_x, delta_y)
            return possible_to_move and can_move(grid, new_x, new_y, delta_x, delta_y)
        else:
            return can_move(grid, new_x, new_y, delta_x, delta_y)

    if grid.is_wall(new_x, new_y):
        return False
    return False

def wide_move(grid: Grid, x: int, y: int, delta_x: int, delta_y: int) -> bool:
    new_x, new_y = x + delta_x, y + delta_y
    if grid.is_empty(new_x, new_y):
        grid.swap(new_x, new_y, x, y)
        return True

    if grid.is_box(new_x, new_y):
        if delta_y != 0:
            if grid.grid[new_y][new_x] == "[":
                wide_move(grid, new_x + 1, new_y, delta_x, delta_y)
            else:
                wide_move(grid, new_x - 1, new_y, delta_x, delta_y)
        wide_move(grid, new_x, new_y, delta_x, delta_y)
        grid.swap(new_x, new_y, x, y)
        return True

    if grid.is_box(new_x, new_y):
        return False

def part1():
    grid, moves = parse()

    for robot_move in moves:
        x, y = grid.get_robot_pos()
        delta_x, delta_y = (1 if robot_move == ">" else -1 if robot_move == "<" else 0, 1 if robot_move == "v" else -1 if robot_move == "^" else 0)
        if move(grid, x, y, delta_x, delta_y):
            grid.set_robot_pos(x + delta_x, y + delta_y)

    print(grid)
    coords = [100 * y + x if grid.is_box(x, y) else 0 for y in range(len(grid.grid)) for x in range(len(grid.grid[y]))]
    print(sum(coords))

def part2():
    grid, moves = parse()
    new_grid = [[]]
    for idx, row in enumerate(grid.grid):
        new_grid.append([])
        for val in row:
            if val == "#":
                new_grid[idx].append("#")
                new_grid[idx].append("#")
            elif val == "O":
                new_grid[idx].append("[")
                new_grid[idx].append("]")
            elif val == ".":
                new_grid[idx].append(".")
                new_grid[idx].append(".")
            elif val == "@":
                new_grid[idx].append("@")
                new_grid[idx].append(".")
    grid.grid = new_grid

    for robot_move in moves:
        x, y = grid.get_robot_pos()
        delta_x, delta_y = (1 if robot_move == ">" else -1 if robot_move == "<" else 0, 1 if robot_move == "v" else -1 if robot_move == "^" else 0)
        if can_move(grid, x, y, delta_x, delta_y):
            if wide_move(grid, x, y, delta_x, delta_y):
                grid.set_robot_pos(x + delta_x, y + delta_y)
        # print(grid)

    print(grid)
    coords = [100 * y + x if grid.grid[y][x] == "[" else 0 for y in range(len(grid.grid)) for x in range(len(grid.grid[y]))]
    print(sum(coords))

part2()