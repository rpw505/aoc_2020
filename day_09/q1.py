import re
import logging
from dataclasses import dataclass
from typing import Tuple, List
from itertools import tee, combinations

TEST_INPUT = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def window(seq, n):
    start = 0
    end = n
    while end <= len(seq):
        yield seq[start:end]
        start += 1
        end += 1


def xmas_probe(numbers, window_size=25):
    
    for win in window(numbers, window_size + 1):
        preceding = win[:-1]
        new_number = win[-1]
        sums = set(map(sum, combinations(preceding, 2)))
        if new_number not in sums:
            print('HIT: ', new_number)
            return new_number


def xmas_attack(numbers, target):
    start = 0
    while True:
        acc = 0
        end = start
        if numbers[start] > target:
            raise Exception(f'Gone horribly wrong, {numbers[start]}: {start}')
        while acc < target:
            # print(numbers[end])
            acc += numbers[end]
            # print('+ ', acc)
            end += 1
        # print('~~~')
        if acc == target and start < end:
            return (min(numbers[start:end]), max(numbers[start:end]))
        start += 1


def tests():
    print('Tests\n-----\n')

    numbers = TEST_INPUT
    target = xmas_probe(numbers, 5)

    print(xmas_attack(numbers, target))

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        numbers = [int(line) for line in input_file.readlines()]
    
    target = xmas_probe(numbers, 25)

    result = xmas_attack(numbers, target)
    print(result)
    print(sum(result))



if __name__ == '__main__':
    tests()
    print('')
    main()
