from typing import NamedTuple
from math import radians, cos, sin

TEST_INPUT = [
    '939',
    '7,13,x,x,59,x,31,19'
]

"""Part 2 comments
Consider the example 17,x,13,19 = 3417
t % 17 = 0
t+2 % 13 = 0
t+3 % 19 = 0

Can we solve for just two to begin with?
e.g. '17,x,13'

102
    + 221 <- This 17 * 13
323
    + 221
544
    + 221
765
    + 221
986
    + 221

# This tells us result must satisfy.
t = 102 + (n * 221)
or to put another way there is a bus id 221 at offset -102
From here on out it's divide and conquer!
"""

def departs(bus_id, time):
    return time % bus_id == 0

class Bus:

    def __init__(self, id):
        self.id = id

    def departs(self, time):
        # A bus' ID determines when it departs.
        return departs(self.id, time)

    def __repr__(self):
        return f'Bus:{self.id}'

def parse_input(lines):
    depart_time = int(lines[0])
    buses = [Bus(int(bus_id)) for bus_id in lines[1].split(',') if bus_id != 'x']
    return depart_time, buses

def next_departure(buses, time):
    start_time = time
    while True:
        for bus in buses:
            if bus.departs(time):
                print(f'Next departure is bus {bus} @ {time}')
                print('Result', (time - start_time) * bus.id)
                return bus
        time += 1

class Solver:

    @staticmethod
    def from_line(line):
        return Solver([(int(bus_id), int(offset)) for offset, bus_id in enumerate(line.split(',')) if bus_id != 'x'])

    def __init__(self, list_of_tuples):
        self.buses = list_of_tuples

    def valid(self, time: int):
        return all(departs(b, time + offset) for b, offset in self.buses)

    def search(self):
        """Search for the next valid time these buses departs at."""
        # Find best step size
        step_size, offset = max(self.buses, key=lambda e: e[0])
        t = step_size
        while True:
            if self.valid(t-offset):
                yield (t - offset)
            t += step_size

    def solve(self):
        answer = Solver([self.reduce()])
        result = -answer.buses[0][1]
        print(result)
        return result

    def reduce(self):
        """Retruns a single bus tuple"""
        if len(self.buses) == 1:
            # print(f'reducing {self.buses[0]} -> {self.buses[0]}')
            return self.buses[0]

        if len(self.buses) == 2:
            print(f'reducing {self.buses}')
            results = self.search()
            offset = next(results)
            delta = next(results) - offset
            new_bus = (delta, -offset)
            print(f'         {" "*len(str(self.buses))} -> {new_bus}')
            return new_bus

        # Otherwise reduce the problem set (divide and conquer)
        head = self.buses[0:2]
        tail = self.buses[2:]
        print(f'    head {head}, tail {tail}')
        return Solver([
            Solver(head).reduce(),
            Solver(tail).reduce()
        ]).reduce()

def tests():
    print('Tests\n-----\n')
    depart_time, buses = parse_input(TEST_INPUT)
    next_departure(buses, depart_time)

    s = Solver.from_line(TEST_INPUT[1])
    assert s.valid(1068781)

    s = Solver.from_line('17,x,13')
    results = s.search()
    offset = next(results)
    delta = next(results) - offset
    new_bus = (delta, -offset)
    print(new_bus)

    s2 = Solver([new_bus, (19, 3)])
    assert s2.valid(3417)
    results = s2.search()
    print(next(results))
    print(next(results))
    print(next(results))

    assert Solver.from_line('17,x,13,19').solve() == 3417
    assert Solver.from_line('67,7,59,61').solve() == 754018
    assert Solver.from_line('1789,37,47,1889').solve() == 1202161486

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        depart_time, buses = parse_input(lines)
    
    next_departure(buses, depart_time)
    print('Part 2: ', Solver.from_line(lines[1]).solve())

if __name__ == '__main__':
    tests()
    print('')
    main()
