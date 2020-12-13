from typing import NamedTuple
from math import radians, cos, sin

TEST_INPUT = [
    '939',
    '7,13,x,x,59,x,31,19'
]


class Bus:

    def __init__(self, id):
        self.id = id
    
    def departs(self, time):
        # A bus' ID determines when it departs.
        return time % self.id == 0
    
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


def tests():
    print('Tests\n-----\n')
    depart_time, buses = parse_input(TEST_INPUT)
    next_departure(buses, depart_time)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
        depart_time, buses = parse_input(lines)
    
    next_departure(buses, depart_time)

if __name__ == '__main__':
    tests()
    print('')
    main()
