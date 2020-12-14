from typing import NamedTuple
from math import radians, cos, sin
import collections

TEST_INPUT = [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]

class Memory(collections.UserDict):


    def exec_line(self, line: str):
        if line.startswith('mask'):
            bit_string = line[len('mask = '):]
            self.mask = bit_string
            # print(self.mask)
            # Bit string has X's, denoting no change, really the 'mask' is an AND mask and OR mask combined.
            and_mask = bit_string.replace('X', '1')
            or_mask = bit_string.replace('X', '0')
            # print(and_mask, or_mask, sep='\n')
            # convert to ints
            self.and_mask = int(and_mask, 2)
            self.or_mask = int(or_mask, 2)
        else:
            # Wanna see something filthy?
            mem = self
            exec(line)

    def apply_mask(self, value):
        value &= self.and_mask
        value |= self.or_mask
        return value

    def __setitem__(self, key, value):
        # Mutate value according to mask
        value = self.apply_mask(value)
        super().__setitem__(key, value)

def run(lines):
    mem = Memory()
    print(mem)
    for line in lines:
        mem.exec_line(line)
    # Sum all values
    print('sum of memory: ', sum(mem.values()))
    return mem

def tests():
    print('Tests\n-----\n')
    result = run(TEST_INPUT)
    print(result)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    run(lines)

if __name__ == '__main__':
    tests()
    print('')
    main()
