from itertools import islice
from collections import defaultdict

TEST_INPUT = [0, 3, 6]
TEST_OUTPUT = [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]

TESTS_2020 = [
    ((1,3,2), 1),
    ((2,1,3), 10),
    ((1,2,3), 27),
    ((2,3,1), 78),
    ((3,2,1), 438),
    ((3,1,2), 1836),
]

def run(numbers):
    memory = defaultdict(list)
    t = 1
    last_n = None

    def speak(n):
        nonlocal t, last_n, memory
        memory[n].append(t)
        t += 1
        last_n = n
        yield n

    for n in numbers:
        # print(f'{t}: stating {n} -> {n}')
        yield from speak(n)

    while True:
        if len(memory[last_n]) > 1:
            # Speak difference in age.
            diff = memory[last_n][-1] - memory[last_n][-2]
            # print(f'{t}: last spoke {last_n} at {memory[last_n][-2]}, {memory[last_n][-1]} -> {diff}')
            yield from speak(diff)
        else:
            # New number
            # print(f'{t}: never spoke {last_n} -> 0')
            yield from speak(0)


def tests():
    print('Tests\n-----\n')
    results = list(islice(run(TEST_INPUT), 2020))
    # print(results)
    assert results[:10] == TEST_OUTPUT
    assert results[-1] == 436

    for test_input, expected in TESTS_2020:
        results = list(islice(run(test_input), 2020))
        # print(results)
        assert expected == results[-1]


def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        numbers = [int(n) for n in input_file.readlines()[0].strip().split(',')]
    results = list(islice(run(numbers), 2020))
    print(results[-1])

if __name__ == '__main__':
    tests()
    print('')
    main()
