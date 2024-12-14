from dataclasses import dataclass
import re

@dataclass
class Robot:
    pos_x: int
    pos_y: int
    vel_x: int
    vel_y: int

    def __iter__(self):
        return iter((self.pos_x, self.pos_y, self.vel_x, self.vel_y))

    def same_pos(self, x, y) -> bool:
        return self.pos_x == x and self.pos_y == y

def parse() -> list[Robot]:
    regex = R"p=(\d+),(\d+) v=(-*\d+),(-*\d+)\n*"
    matches = re.findall(regex, open("input.txt").read())
    return [Robot(int(pos_x), int(pos_y), int(vel_x), int(vel_y)) for pos_x, pos_y, vel_x, vel_y in matches]

def part1():
    grid_width = 101
    grid_height = 103
    seconds = 100

    robots = parse()
    robots = [
        Robot(
            (pos_x + vel_x * seconds) % grid_width,
            (pos_y + vel_y * seconds) % grid_height, vel_x, vel_y)
            for pos_x, pos_y, vel_x, vel_y in robots]

    quad_count = {(0,0): 0, (1, 0): 0, (0, 1): 0, (1, 1): 0}
    middle_x = grid_width // 2
    middle_y = grid_height // 2
    for robot in robots:
        x = 0 if robot.pos_x < middle_x else (1 if robot.pos_x > middle_x else None)
        y = 0 if robot.pos_y < middle_y else (1 if robot.pos_y > middle_y else None)

        if x is not None and y is not None:
            quad_count[(x, y)] += 1

    total = 1
    for quad in quad_count.items():
        total *= quad[1]

    print(total)

def pretty_print(width, height, robots: list[Robot]):
    for y in range(height):
        line = ""
        for x in range(width):
            has_robot = False
            for robot in robots:
                if robot.same_pos(x, y):
                    has_robot = True
                    break

            if has_robot:
                line += "#"
            else:
                line += "."

        print(line)

def has_bunched_row(grid_width, grid_height, bunch_x, robots: list[Robot]) -> bool:
    pos = {}
    for robot in robots:
        pos[(robot.pos_x, robot.pos_y)] = 1

    for y in range(grid_width):
        row_count = 0
        for x in range(grid_height):
            if (x, y) in pos:
                row_count += 1
            else:
                row_count = 0

            if row_count >= bunch_x:
                return True

    return False

def part2():
    grid_width = 101
    grid_height = 103
    seconds = 10000

    robots = parse()

    for second in range(0, seconds):
        moved_robots = [
            Robot(
                (pos_x + vel_x * second) % grid_width,
                (pos_y + vel_y * second) % grid_height, vel_x, vel_y)
                for pos_x, pos_y, vel_x, vel_y in robots]

        print(f"Grid at {second}")
        if has_bunched_row(grid_width, grid_height, 12, moved_robots):
            pretty_print(grid_width, grid_height, moved_robots)
            print(f"Found at {second}s")
            break

part2()