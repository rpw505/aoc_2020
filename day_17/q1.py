from typing import NamedTuple, Tuple, Dict
from collections import Counter, defaultdict
TEST_INPUT = [
    '.#.',
    '..#',
    '###',
]

ACTIVE = '#'
INACTIVE = '.'

class Point(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other,  self.z * other)

    def iter_adjacent(self) -> Tuple['Point']:
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    if (x, y, z) == (0, 0, 0):
                        continue
                    yield Point(self.x + x, self.y + y, self.z + z)
    
    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z})'


def run(pocket_dimension: Dict[Point, str]):
    active = [p for p, state in pocket_dimension.items() if state == ACTIVE]
    to_be_deactivated = set()
    to_be_activated = set()
    # Cubes bordering active ones. The key is the position (point), the
    # count the number of adjacent active cubes.
    edge = Counter()

    for p in active:
        adjacent = tuple(p.iter_adjacent())
        # If a cube is active and exactly 2 or 3 of its neighbors are also active,
        # the cube remains active. Otherwise, the cube becomes inactive.
        active_adjacent = tuple(pa for pa in adjacent if pocket_dimension[pa] == ACTIVE)
        if not (len(active_adjacent) == 2 or len(active_adjacent) == 3):
            to_be_deactivated.add(p)
        edge.update(adjacent)

    # If a cube is inactive but exactly 3 of its neighbors are active, the cube
    # becomes active. Otherwise, the cube remains inactive.
    for p, active_neighbours in edge.items():
        if pocket_dimension[p] == INACTIVE and active_neighbours == 3:
            to_be_activated.add(p)

    # Update state
    print('Activating:  ', to_be_activated)
    print('Deactivating:', to_be_deactivated)
    print('Intersection:', to_be_activated & to_be_deactivated)
    for p in to_be_activated:
        pocket_dimension[p] = ACTIVE
    for p in to_be_deactivated:
        pocket_dimension[p] = INACTIVE


def load_pocket_dimension(lines) -> Dict[Point, str]:
    pocket_dimension = defaultdict(lambda: INACTIVE)
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ACTIVE:
                pocket_dimension[Point(x, y, 0)] = ACTIVE
    return pocket_dimension

def part_1(pocket_dimension: Dict[Point, str]):
    """Returns set of possibly valid tickets (all values valid for at least one field)"""
    for _ in range(6):
        run(pocket_dimension)
    print('Total active:', sum(v == ACTIVE for v in pocket_dimension.values()))

def tests():
    print('Tests\n-----\n')
    pocket_dimension = load_pocket_dimension(TEST_INPUT)
    print(pocket_dimension)
    part_1(pocket_dimension)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        pocket_dimension = load_pocket_dimension((line.strip() for line in input_file.readlines()))
    part_1(pocket_dimension)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    tests()
    print('')
    main()
