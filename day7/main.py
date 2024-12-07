from dataclasses import dataclass

add = lambda x, y : x + y
mult = lambda x, y : x * y
concat = lambda x, y : int(str(x) + str(y))

@dataclass
class Equation:
    answer: int
    values: list[int]

def create_equations(lines: list[str]) -> list[Equation]:
    equations: list[Equation] = []
    for line in lines:
        answer, values = line.split(":")
        equations.append(Equation(int(answer), [int(x) for x in values.split()]))
    return equations

def to_base(number, base):
    digits = []
    while number:
        digits.append(number % base)
        number //= base
    return list(reversed(digits))

def do_operation(x: int, y: int, index: int, operator_pattern: int, operators, num_values: int) -> int:
    # Solution only works for base2, but is much faster
    # operation = (operator_pattern >> index) & 1
    # return operators[operation](x, y)

    converted = to_base(operator_pattern, len(operators))
    while len(converted) < num_values - 1:
        converted = [0] + converted
    return operators[converted[index]](x, y)

def run(operators) -> int:
    lines = [line.strip() for line in open("input.txt").readlines()]
    equations = create_equations(lines)

    result = 0
    for equation in equations:
        # Calculate number of equations needed to cover all cases (available_operators^number_of_operators)
        num_operations = pow(len(operators), (len(equation.values) - 1))
        for operator_pattern in range(0, num_operations):
            total = equation.values[0]

            for index, value in enumerate(equation.values[1:]):
                total = do_operation(total, value, index, operator_pattern, operators, len(equation.values))

            if total == equation.answer:
                # print(equation)
                result += equation.answer
                break

    return result

def part1():
    operators = [add, mult]
    print(run(operators))

def part2():
    operators = [add, mult, concat]
    print(run(operators))

part2()