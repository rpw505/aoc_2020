from itertools import chain, tee, combinations
from functools import reduce
import operator
from pprint import pprint

TEST_INPUT = [
    'L.LL.LL.LL',
    'LLLLLLL.LL',
    'L.L.L..L..',
    'LLLL.LL.LL',
    'L.LL.LL.LL',
    'L.LLLLL.LL',
    '..L.L.....',
    'LLLLLLLLLL',
    'L.LLLLLL.L',
    'L.LLLLL.LL',
]

TEST_INPUT_2 = [
    '.......#.',
    '...#.....',
    '.#.......',
    '.........',
    '..#L....#',
    '....#....',
    '.........',
    '#........',
    '...#.....',
]

FLOOR = '.'
EMPTY_SEAT = 'L'
OCCUPIED_SEAT = '#'

def make_grid(lines):
    # index by row column.
    grid = [[c for c in line.strip()] for line in lines]
    return grid

def iter_neighbours_adjacent(grid, row, col):
    """Returns iterator for neighbours as tuples of (row, col) accounting for grid bounds and
    floor tiles
    """

    def validate(t):
        return (0 <= t[0] < len(grid)) and (0 <= t[1] < len(grid[0])) and t != (row, col) and not is_floor(grid, *t)

    return filter(validate, ((r, c) for r in range(row-1, row+2) for c in range(col-1, col+2)))

def iter_neighbours_ray(grid, row, col):
    """Returns iterator for neighbours as tuples of (row, col) accounting for grid bounds.
    This is based on line of sight (los) and only returns seats, not floor.
    """
    # Make the gradients, then ascend them looking for non floor tiles.
    grads = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

    def ascend(grad, r, c):
        def in_bounds(r, c):
            return (0 <= r < len(grid)) and (0 <= c < len(grid[0]))
        while True:
            r += grad[0]
            c += grad[1]
            if in_bounds(r, c):
                yield (r, c)
            else:
                break

    neighbours = []
    for grad in grads:
        for coord in ascend(grad, row, col):
            if not is_floor(grid, *coord):
                neighbours.append(coord)
                break
    return neighbours
 

def is_floor(grid, r, c):
    return grid[r][c] == FLOOR

def is_empty_seat(grid, r, c):
    return grid[r][c] == EMPTY_SEAT

def is_occupied_seat(grid, r, c):
    return grid[r][c] == OCCUPIED_SEAT


def run(grid, iter_neighbours=iter_neighbours_adjacent, seat_tolerance=4):
    new_grid = []
    changes = []
    for r, row in enumerate(grid):
        new_row = []
        new_grid.append(new_row)
        for c, seat in enumerate(row):
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if seat == EMPTY_SEAT:
                if all(is_empty_seat(grid, *n) for n in iter_neighbours(grid, r, c)):
                    seat = OCCUPIED_SEAT
                    changes.append((r, c))
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            elif seat == OCCUPIED_SEAT:
                if sum(is_occupied_seat(grid, *n) for n in iter_neighbours(grid, r, c)) >= seat_tolerance:
                    seat = EMPTY_SEAT
                    changes.append((r, c))
            new_row.append(seat)
    return new_grid, changes


def run_until_stable(grid, **kwargs):
    changes = True
    i = 0
    while changes:
        grid, changes = run(grid, **kwargs)
        i += 1
        print(i)
        # pprint(grid)
        # print(changes)
    result = sum(is_occupied_seat(grid, r, c) for r in range(len(grid)) for c in range(len(grid[0])))
    print('Number of occupied: ', result)
    return result, grid


def tests():
    print('Tests\n-----\n')
    grid = make_grid(TEST_INPUT)
    run_until_stable(grid)

    grid_2 = make_grid(TEST_INPUT_2)
    assert list(iter_neighbours_ray(grid_2, 4, 3)) == [(1, 3), (0, 7), (4, 8), (5, 4), (8, 3), (7, 0), (4, 2), (2, 1)]
    run_until_stable(grid, iter_neighbours=iter_neighbours_ray, seat_tolerance=5)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        grid = make_grid(input_file.readlines())
    run_until_stable(grid)
    run_until_stable(grid, iter_neighbours=iter_neighbours_ray, seat_tolerance=5)

if __name__ == '__main__':
    tests()
    print('')
    main()
