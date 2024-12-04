template = [
    "S..S..S",
    ".A.A.A.",
    "..MMM.."
    "SAMXMAS",
    "..MMM.."
    ".A.A.A.",
    "S..S..S",
]

def find_xmas(lines: str) -> int:
    total = 0
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "X":
                # Horizontal
                if col + 1 < len(lines[row]) and col + 2 < len(lines[row]) and col + 3 < len(lines[row]):
                    total += lines[row][col+1] == "M" and lines[row][col+2] == "A" and lines[row][col+3] == "S"
                
                # Horizontal reverse
                if col - 1 >= 0 and col - 2 >= 0 and col - 3 >= 0:
                    total += lines[row][col-1] == "M" and lines[row][col-2] == "A" and lines[row][col-3] == "S"

                # Vertical
                if row + 1 < len(lines) and row + 2 < len(lines) and row + 3 < len(lines):
                    total += lines[row+1][col] == "M" and lines[row+2][col] == "A" and lines[row+3][col] == "S"

                # Vertical reverse
                if row - 1 >= 0 and row - 2 >= 0 and row - 3 >= 0:
                    total += lines[row-1][col] == "M" and lines[row-2][col] == "A" and lines[row-3][col] == "S"

                # Diagonal
                if row + 1 < len(lines) and row + 2 < len(lines) and row + 3 < len(lines) and col + 1 < len(lines[row]) and col + 2 < len(lines[row]) and col + 3 < len(lines[row]):
                    total += lines[row+1][col+1] == "M" and lines[row+2][col+2] == "A" and lines[row+3][col+3] == "S"

                # Diagonal reverse
                if row - 1 >= 0 and row - 2 >= 0 and row - 3 >= 0 and col - 1 >= 0 and col - 2 >= 0 and col - 3 >= 0:
                    total += lines[row-1][col-1] == "M" and lines[row-2][col-2] == "A" and lines[row-3][col-3] == "S"

                # Diagonal reverse
                if row - 1 >= 0 and row - 2 >= 0 and row - 3 >= 0 and col + 1 < len(lines[row]) and col + 2 < len(lines[row]) and col + 3 < len(lines[row]):
                    total += lines[row-1][col+1] == "M" and lines[row-2][col+2] == "A" and lines[row-3][col+3] == "S"

                # Diagonal reverse
                if row + 1 < len(lines) and row + 2 < len(lines) and row + 3 < len(lines) and col - 1 >= 0 and col - 2 >= 0 and col - 3 >= 0:
                    total += lines[row+1][col-1] == "M" and lines[row+2][col-2] == "A" and lines[row+3][col-3] == "S"

    return total

def find_x_mas(lines: str) -> int:
    total = 0
    for row in range(len(lines)):
        for col in range(len(lines[row])):
            if lines[row][col] == "A":
                # Diagonal
                if row + 1 < len(lines) and row - 1 >= 0 and col + 1 < len(lines[row]) and col - 1 >= 0:
                    total += (((lines[row+1][col+1] == "M" and lines[row-1][col-1] == "S") or (lines[row+1][col+1] == "S" and lines[row-1][col-1] == "M"))
                    and ((lines[row+1][col-1] == "M" and lines[row-1][col+1] == "S") or (lines[row+1][col-1] == "S" and lines[row-1][col+1] == "M")))

    return total

def part1():
    input = ""
    with open("input.txt") as f:
        input = f.readlines()

    total = find_xmas(input)
    print(total)

def part2():
    input = ""
    with open("input.txt") as f:
        input = f.readlines()

    total = find_x_mas(input)
    print(total)

part2()