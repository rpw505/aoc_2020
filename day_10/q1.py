from itertools import chain, tee, combinations
from functools import reduce
import operator

TEST_INPUT = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]

TEST_INPUT_2 = [28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38,
                39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3]

class DifferenceException(Exception):
    pass

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def joltage_differences(numbers, add_ends=True, verbose=True):
    # Add 0 and max + 3 as instructed
    ends = []
    if add_ends:
        ends = [0, max(numbers) + 3]
    numbers = sorted(chain(numbers, ends))

    # Use sets to track differences and easy debug
    sets = [set() for _ in range(4)]

    for i, (a, b) in enumerate(pairwise(numbers)):
        difference = b - a
        if difference > 3:
            raise DifferenceException(f'Got {difference}')
        # print(i, a, b)
        sets[difference].add((i, a, b))

    if verbose:
        for i in range (1,4):
            print(f'{len(sets[i])} differences of {i}')
        print(f'{len(sets[1])} * {len(sets[3])} = {len(sets[1]) * len(sets[3])}')
    return numbers, sets


def valid_combinations(numbers):
    def validate(order):
        order = list(order)
        # Must keep starting and end to meet diff of 3.
        if (order[0] != numbers[0]) or (order[-1] != numbers[-1]):
            # print('starts and ends', order, numbers)
            return False
        # otherwise calculate joltage difference and see if it fails (diff greater than 3)
        try:
            joltage_differences(order, add_ends=False, verbose=False)
        except DifferenceException as e:
            return False
        return True

    all_combinations = list(chain.from_iterable(combinations(numbers, r) for r in range(1, len(numbers) + 1)))
    orderings = list(filter(validate, all_combinations))
    # print(orderings)
    return orderings


def joltage_combinations(numbers, differences):
    # I think the trick is to partition the set of numbers.
    # When the difference is 3 we know that is a break point
    # (the only combination that works).
    partitions = []
    start = 0

    for (i, a, b) in sorted(differences[3], key=lambda t: t[0]):
        partitions.append(numbers[start:i+1])
        start = i + 1
    print(partitions)
    # Within each partition how many combinations are there?

    partitioned_combinations = [valid_combinations(p) for p in partitions]
    print(partitioned_combinations)

    result = reduce(operator.mul, map(len, partitioned_combinations))
    print('Combinations: ', result)
    return result


def tests():
    print('Tests\n-----\n')

    assert valid_combinations([4, 5, 6, 7]) == [(4, 7), (4, 5, 7), (4, 6, 7), (4, 5, 6, 7)]

    print('test 1:')
    t1_out = joltage_differences(TEST_INPUT)
    print('test 2:')
    t2_out = joltage_differences(TEST_INPUT_2)

    print('\npart 2:')
    assert joltage_combinations(*t1_out) == 8
    assert joltage_combinations(*t2_out) == 19208

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        numbers = [int(line) for line in input_file.readlines()]

    out = joltage_differences(numbers)
    joltage_combinations(*out)

if __name__ == '__main__':
    tests()
    print('')
    main()
