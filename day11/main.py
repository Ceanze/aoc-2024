import time

def generator(input: list[int]):
    for num in input:
        num_digits = 0
        temp = num
        while temp > 0:
            temp //= 10
            num_digits += 1
        
        if num == 0:
            yield 1
        elif num_digits % 2 == 0:
            half_digits = num_digits // 2
            # Calculate the divisor to split the number
            divisor = 10 ** half_digits
            first_half = num // divisor
            second_half = num % divisor
            yield first_half
            yield second_half
        else:
            yield num * 2024

def part1():
    stones = [int(stone) for stone in open('input.txt').read().split(' ')]
    
    blinks = 25
    for i in range(blinks):
        print(f'Processing blink {i+1}')
        stones = list(generator(stones))
    print(len(stones))

def part2():
    start_time = time.time()
    stones = [int(stone) for stone in open('input.txt').read().split(' ')]

    # Create a map, initially with one of each number (true for puzzle input)
    mapped = {stone: 1 for stone in stones}

    blinks = 75
    for blink in range(blinks):
        temp_map = {}
        for num, count in mapped.items():
            num_digits = 0
            temp = num
            while temp > 0:
                temp //= 10
                num_digits += 1
            
            if num == 0:
                temp_map[1] = temp_map.get(1, 0) + count
            elif num_digits % 2 == 0:
                half_digits = num_digits // 2
                # Calculate the divisor to split the number
                divisor = 10 ** half_digits
                first_half = num // divisor
                second_half = num % divisor
                temp_map[first_half] = temp_map.get(first_half, 0) + count
                temp_map[second_half] = temp_map.get(second_half, 0) + count
            else:
                temp_map[num * 2024] = temp_map.get(num * 2024, 0) + count

        mapped = temp_map

    end_time = time.time() - start_time

    print(sum(mapped.values()))
    print(f'Time: {end_time}')

part2()