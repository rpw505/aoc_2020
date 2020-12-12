from typing import NamedTuple
from math import radians, cos, sin

TEST_INPUT = [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def rotate(self, degrees: float):
        theta = radians(degrees)
        return Point(
            round(self.x * cos(theta) - self.y * sin(theta)),
            round(self.y * cos(theta) + self.x * sin(theta))
        )


NORTH = Point(0, 1)
EAST = Point(1, 0)
SOUTH = Point(0, -1)
WEST = Point(-1, 0)

HEADING_TO_DIR = {
    0: NORTH,
    90: EAST,
    180: SOUTH,
    270: WEST    
}

LETTER_TO_DIR = {
    'N': NORTH,
    'E': EAST,
    'S': SOUTH,
    'W': WEST
}

class State(NamedTuple):
    pos: Point
    # North is 0
    heading_degrees: int

    def add_degrees(self, degrees):
        degrees += self.heading_degrees
        degrees %= 360
        return self._replace(heading_degrees=degrees)

    def forward(self, magnitude):
        vector = HEADING_TO_DIR[self.heading_degrees] * magnitude
        return self._replace(pos=self.pos+vector)

    def move(self, vector):
        return self._replace(pos=self.pos+vector)

class State2(NamedTuple):
    pos: Point
    # North is 0
    waypoint: Point

    def add_degrees(self, degrees):
        # Rotate the waypoint around the ship. Note that positive
        # degrees rotates anti clockwise (as we are using radians) so invert
        return self._replace(waypoint=self.waypoint.rotate(-degrees))

    def forward(self, vector):
        # Move to the waypoint
        return self._replace(pos=self.pos+(self.waypoint*vector))

    def move(self, vector):
        # Move the waypoint
        return self._replace(waypoint=self.waypoint+vector)

def parse_instruction(s: State, line: str):
    code = line[0]
    value = int(line[1:])

    if code == 'R':
        # Rotate right by degrees
        return s.add_degrees(value)
    if code == 'L':
        # Rotate left by degrees
        return s.add_degrees(-value)
    if code == 'F':
        return s.forward(value)
    # Otherwise move in cardinal direction
    vector = LETTER_TO_DIR[code]
    vector *= value
    return s.move(vector)

def run(lines, starting_state):
    # Start facing East
    s = starting_state
    for line in lines:
        # print(s, line)
        s = parse_instruction(s, line)
    print(s)
    print(abs(s.pos.x) + abs(s.pos.y))
    return s

def tests():
    print('Tests\n-----\n')
    run(TEST_INPUT, State(Point(0, 0), 90))
    run(TEST_INPUT, State2(Point(0, 0), Point(10, 1)))


def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    run(lines, State(Point(0, 0), 90))
    run(lines, State2(Point(0, 0), Point(10, 1)))

if __name__ == '__main__':
    tests()
    print('')
    main()
