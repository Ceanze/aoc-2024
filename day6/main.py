import time

def check_obstacle(lines: list[str], curr_pos: tuple[int, int], dir: tuple[int, int]) -> bool:
    # Place down a fake block so we can check that one as well
    _, fake_block_x, fake_block_y = get_facing_tile(lines, curr_pos, dir)
    tries, max_tries = 0, 10000
    while tries < max_tries:
        # Get facing tile to determine action, based on current position and direction
        facing_tile, facing_x, facing_y = get_facing_tile(lines, curr_pos, dir) or (None, None, None)
        if facing_tile == None:
            return False

        # If tile is a block (or our fake block), then rotate on the spot
        if facing_tile == "#" or (facing_x == fake_block_x and facing_y == fake_block_y):
            dir = rotate(dir)
        # If anything else ("." or "X"), the virtually move in that direction by updating curr_pos
        else:
            curr_pos = (facing_x, facing_y)
        
        tries += 1

    return True

def get_facing_tile(lines: list[str], curr_pos: tuple[int, int], dir: tuple[int, int]) -> tuple[str, int, int]:
    x, y = curr_pos
    if dir == "^" and y - 1 >= 0:
        return (lines[y-1][x], x, y-1)
    elif dir == ">" and x + 1 < len(lines[y]):
        return (lines[y][x+1], x+1, y)
    elif dir == "v" and y + 1 < len(lines):
        return (lines[y+1][x], x, y+1)
    elif dir == "<" and x - 1 >= 0:
        return (lines[y][x-1], x-1, y)
    else:
        return None
    
def rotate(dir: tuple[int, int]):
    if dir == "^":
        return ">"
    elif dir == ">":
        return "v"
    elif dir == "v":
        return "<"
    elif dir == "<":
        return "^"

def walk_forward(lines: list[str], curr_pos: tuple[int, int], curr_dir: str) -> tuple[int, int, str, bool, bool]:
    x, y = curr_pos
    facing_tile, facing_x, facing_y = get_facing_tile(lines, curr_pos, curr_dir) or (None, None, None)
    if facing_tile == None:
        return None
    if facing_tile == "#":
        curr_dir = rotate(curr_dir)
        return (x, y, curr_dir, False, False)
    if facing_tile == "." or facing_tile == "X":
        lines[y][x] = "X"
        can_place_obstacle = facing_tile == "." and check_obstacle(lines, (x, y), curr_dir)
        return (facing_x, facing_y, curr_dir, facing_tile == ".", can_place_obstacle)


def find_start(lines: list[str]) -> tuple[int, int]:
    for line in lines:
        for char in line:
            if char == "^" or char == ">" or char == "v" or char == "<":
                return line.index(char), lines.index(line)
            
    assert(False)

def count_walk(lines: list[str], start: tuple[int, int]) -> int:
    curr_pos = start
    curr_dir = lines[start[1]][start[0]]
    
    covered = 0
    possible_obstacles = 0
    walking = True
    while walking:
        pos_x, pos_y, dir, new_tile, can_place_obstacle = walk_forward(lines, curr_pos, curr_dir) or (None, None, None, None, None)
        new_pos = (pos_x, pos_y)
        curr_dir = dir
        if pos_x == None or pos_y == None:
            covered += 1
            walking = False
        elif new_tile:
            covered += 1
        curr_pos = new_pos

        if can_place_obstacle:
            possible_obstacles += 1

    return (covered, possible_obstacles)

def pretty_print(lines: list[str]):
    for line in lines:
        print("".join(line))

def part1():
    lines = [list(line.strip()) for line in open("input.txt").readlines()]

    start = find_start(lines)
    print(count_walk(lines, start)[0])

def part2():
    time_start = time.time()
    lines = [list(line.strip()) for line in open("input.txt").readlines()]

    start = find_start(lines)
    print(f"result: {count_walk(lines, start)}")
    # pretty_print(lines)
    time_end = time.time()

    print(f"Time: {time_end - time_start}")

part2()