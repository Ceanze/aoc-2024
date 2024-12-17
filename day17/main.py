A = 0
B = 1
C = 2

def parse() -> tuple[list[int], list[int]]:
    registers, instructions = open("input.txt").read().split("\n\n")

    out_registers = [int(register[register.find(": ")+2:]) for register in registers.splitlines()]
    out_instructions = [int(i) for i in instructions[instructions.find(": ")+2:].split(",")]

    return out_registers, out_instructions

def get_combo_op_val(op: int, registers: list[int]) -> int:
    match op:
        case 0:
            return op
        case 1:
            return op
        case 2:
            return op
        case 3:
            return op
        case 4:
            return registers[A]
        case 5:
            return registers[B]
        case 6:
            return registers[C]
    # 7 is reserved and does not appear in valid programs
    return None

# Return new pos
def do_instruction(instructions: list[int], pos: int, registers: list[int]) -> tuple[int, str]:
    combo_op = instructions[pos + 1]
    match instructions[pos]:
        case 0: # adv - division with register A, save in A
            registers[A] = registers[A] // pow(2, get_combo_op_val(combo_op, registers))
        case 1: # bxl - bitwise xor with register B and literal op, save in B
            registers[B] = registers[B] ^ instructions[pos + 1]
        case 2: # bst - value of combo % 8, save in B
            registers[B] = get_combo_op_val(combo_op, registers) % 8
        case 3: # jnz - jump if A > 0 - does not increase pos after
            return (combo_op if registers[A] > 0 else pos + 1, None)
        case 4: # bxc - bitwise xor with register B and C, store in B - read but ignore operand
            registers[B] = registers[B] ^ registers[C]
        case 5: # out - combo op % 8, output that value. Separate multiple values with comma
            return (pos + 2, str(get_combo_op_val(combo_op, registers) % 8))
        case 6: # bdv - same as adv, but save to B (read from A)
            registers[B] = registers[A] // pow(2, get_combo_op_val(combo_op, registers))
        case 7: # cdv - same as adv, but save to C (read from A)
            registers[C] = registers[A] // pow(2, get_combo_op_val(combo_op, registers))

    return (pos + 2, None)

def print_registers(registers: list[int]):
    print(f"A: {registers[A]}, B: {registers[B]}, C: {registers[C]}")

def part1():
    registers, instructions = parse()

    print("Registers", registers, "Instructions", instructions)

    next_instruction_pos = 0
    outputs = []
    while next_instruction_pos < len(instructions) - 1:
        next_instruction_pos, output = do_instruction(instructions, next_instruction_pos, registers)
        if output is not None:
            outputs.append(output)

    print(",".join(outputs))

def one_iter(a):
    b = a % 8
    b = b ^ 2
    c = a // 2**b
    b = b ^ 7
    b = b ^ c
    return b % 8

def find(a, answers, instructions, col=0):
    # Build number from left->right, need to check instructions from right->left
    if one_iter(a) != instructions[-(col + 1)]:
        return

    if col == len(instructions) - 1:
        # Save all possible answers
        answers.append(a)
    else:
        for b in range(8):
            # shift a 3 bits to the left, append b, check recursivly
            find(a * 8 + b, answers, instructions, col + 1)

def part2():
    _, instructions = parse()
    answers = []
    for a in range(8):
        find(a, answers, instructions)
    print(min(answers))

part2()
part1()