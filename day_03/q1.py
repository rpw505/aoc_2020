from itertools import cycle
from dataclasses import dataclass
from pprint import pprint
from typing import List
from functools import reduce
import operator

TEST_INPUT = [
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#'
]

class TreeRow:

    @staticmethod
    def from_input(lines):
        return [TreeRow(line) for line in lines]

    def __init__(self, line):
        #'..##.......'
        self.text = line.strip()
        self.tree_array = [t == '#' for t in self.text]

    def __getitem__(self, index):
        row = cycle(self.tree_array)
        if index < 0:
            raise IndexError()
        for _ in range(index):
            next(row)
        return next(row)

    def __repr__(self):
        return f'<{self.text}>'


def slope(rows: List[TreeRow], x, y):
    max_y = len(rows)
    tally = 0
    i = 0
    for j in range(0, max_y, y):
        tally += rows[j][i]
        i += x

    print(f'tally ({x}, {y}): {tally}')
    return tally

def check_slopes(rows):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    result = reduce(operator.mul, [slope(rows, *grad) for grad in slopes])
    print('Check slopes: ', result)
    return result


def tests():
    print('Tests\n-----\n')
    
    rows = TreeRow.from_input(TEST_INPUT)

    print(rows)
    check_slopes(rows)
    

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        rows = TreeRow.from_input(input_file.readlines())
    
    slope(rows, 3, 1)
    check_slopes(rows)


if __name__ == '__main__':
    tests()
    print('')
    main()
