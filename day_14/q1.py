from typing import NamedTuple
from math import radians, cos, sin
import collections
import re
import itertools

TEST_INPUT = [
    'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
    'mem[8] = 11',
    'mem[7] = 101',
    'mem[8] = 0',
]

TEST_INPUT_2 = [
    'mask = 000000000000000000000000000000X1001X',
    'mem[42] = 100',
    'mask = 00000000000000000000000000000000X0XX',
    'mem[26] = 1',
]

class Memory(collections.UserDict):

    def exec_line(self, line: str):
        if line.startswith('mask'):
            bit_string = line[len('mask = '):]
            self.set_mask(bit_string)
        else:
            # Wanna see something filthy?
            mem = self
            exec(line)

    def set_mask(self, bit_string):
        self.mask = bit_string
        # print(self.mask)
        # Bit string has X's, denoting no change, really the 'mask' is an AND mask and OR mask combined.
        and_mask = bit_string.replace('X', '1')
        or_mask = bit_string.replace('X', '0')
        # print(and_mask, or_mask, sep='\n')
        # convert to ints
        self.and_mask = int(and_mask, 2)
        self.or_mask = int(or_mask, 2)

    def apply_mask(self, value):
        value &= self.and_mask
        value |= self.or_mask
        return value

    def __setitem__(self, key, value):
        # Mutate value according to mask
        value = self.apply_mask(value)
        super().__setitem__(key, value)


class MemoryV2(Memory):

    def set_mask(self, bit_string):
        self.mask = bit_string
        # print(self.mask)
        # Bit string is an OR mask, but X's denote special floating bits that get set to all possible values.
        # We can model this as sets of masks?
        starting_or_mask = int(bit_string.replace('X', '0'), 2)

        # Need find positions of X.
        indexes = [i for i, char in enumerate(bit_string[::-1]) if char == 'X']
        print(bit_string, indexes)
        self.masks = []
        # Now build masks
        
        for bits in itertools.product(range(2), repeat=len(indexes)):
            or_mask = starting_or_mask
            and_mask = 0xffffffff
            for bit, position in zip(bits, indexes):
                if bit:
                    # Add to or mask to set bit at this position
                    or_mask |= 1 << position
                else:
                    # Add to and mask to clear bit at this postion
                    and_mask &= ~(1 << position)
            # print(bits)
            # print(f'{and_mask:b} AND')
            # print(f'{or_mask:032b} OR')
            self.masks.append((and_mask, or_mask))


    def apply_mask(self, value):
        """Modified to now return list of values."""
        return [(value & and_mask) | or_mask  for and_mask, or_mask in self.masks]

    def __setitem__(self, key, value):
        # Mutate key according to mask, set all keys to value.
        for k in self.apply_mask(key):
            self.data.__setitem__(k, value)


def run(lines, memory_class=Memory):
    mem = memory_class()
    print(mem)
    for line in lines:
        mem.exec_line(line)
    # Sum all values
    # print(mem)
    print('sum of memory: ', sum(mem.values()))
    return mem

def tests():
    print('Tests\n-----\n')
    result = run(TEST_INPUT)
    print(result)

    result = run(TEST_INPUT_2, MemoryV2)
    print(result)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    run(lines, MemoryV2)

if __name__ == '__main__':
    tests()
    print('')
    main()
