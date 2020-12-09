from collections import Counter
from itertools import chain
import logging

TEST_INPUT = [
    'abc',
    '',
    'a',
    'b',
    'c',
    '',
    'ab',
    'ac',
    '',
    'a',
    'a',
    'a',
    'a',
    '',
    'b',
]

def group_lines(lines, is_delimiter=lambda l: not bool(l)):
    group = []
    lines = iter(lines)
    try:
        while True:
            line = next(lines)
            if is_delimiter(line):
                yield group
                group = []
            else:
                group.append(line)
    except StopIteration:
        yield group


def part_2(groups):
    counters = [Counter(chain(*group)) for group in groups]

    accumulate = 0
    for counts, group_len in zip(counters, (len(g) for g in groups)):
        for num_of_yes in counts.values():
            accumulate += bool(group_len == num_of_yes)
    print('number of questions to which everyone answered "yes" ', accumulate) 
    return accumulate


def tests():
    print('Tests\n-----\n')
    groups = list(group_lines(TEST_INPUT))

    counters = [Counter(chain(*group)) for group in groups]
    # Counters is a fancy dict, so len() of it is number of keys
    result = sum(len(c) for c in counters)
    print('number of questions anyone answered "yes": ', result)
    part_2(groups)


def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        groups = list(group_lines(line.strip() for line in input_file.readlines()))

    counters = [Counter(chain(*group)) for group in groups]
    # Counters is a fancy dict, so len() of it is number of keys
    result = sum(len(c) for c in counters)
    print('number of questions anyone answered "yes": ', result)
    part_2(groups)


if __name__ == '__main__':
    tests()
    print('')
    main()
