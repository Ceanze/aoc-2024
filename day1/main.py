def part1():
    left = []
    right = []

    with open('input.txt') as file:
        for line in file.readlines():
            splitted = line.split()
            left.append(splitted[0])
            right.append(splitted[1])

    left = sorted(left)
    right = sorted(right)

    distance = 0
    for i in range(len(left)):
        distance += abs(int(left[i]) - int(right[i]))

    print(distance)

def part2():
    left = []
    right = []

    with open('input.txt') as file:
        for line in file.readlines():
            splitted = line.split()
            left.append(splitted[0])
            right.append(splitted[1])

    similarity = 0
    occurence = {}
    for i in range(len(right)):
        right_num = int(right[i])
        if occurence.get(right_num) == None:
            occurence[right_num] = 1
        else:
            occurence[right_num] += 1

    for i in range(len(left)):
        left_num = int(left[i])
        if occurence.get(left_num) != None and occurence[left_num] > 0:
            similarity += left_num * occurence[left_num]

    print(similarity)

part2()