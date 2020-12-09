import re
import logging
from dataclasses import dataclass
from typing import Tuple, List
from copy import deepcopy

TEST_INPUT = [
    'nop +0',
    'acc +1',
    'jmp +4',
    'acc +3',
    'jmp -3',
    'acc -99',
    'acc +1',
    'jmp -4',
    'acc +6',
]

class ProgramException(Exception):
    pass

class BadAddress(ProgramException):
    pass

class DoubleExec(ProgramException):
    pass

@dataclass(frozen=True)
class ProgramState:
    pc: int
    acc: int

    def __str__(self):
        return f'PC: {self.pc}, ACC: {self.acc}'


class Instruction:

    def __init__(self, line: str):
        self.raw = line.strip()
        t = self.raw.split(' ')
        self.op_code = t[0]
        self.parameter = int(t[1])
        self.exec_count = 0

    def exec(self, pc, acc):
        self.exec_count += 1
        if self.exec_count == 2:
            raise DoubleExec('DOUBLE EXEC -> HALT')

        if self.op_code == 'nop':
            return ProgramState(pc + 1, acc)
        if self.op_code == 'acc':
            return ProgramState(pc + 1, acc + self.parameter)
        if self.op_code == 'jmp':
            return ProgramState(pc + self.parameter, acc)
        raise Exception('Unknown Op code')
    
    def mutate(self):
        if self.op_code == 'acc':
            return False
        if self.op_code == 'nop':
            self.op_code = 'jmp'
            return True
        self.op_code = 'nop'
        return True

    def __repr__(self):
        return f'{self.op_code} {self.parameter:+d}'


def run(instructions):
    state = ProgramState(0, 0)
    while True:
        if state.pc == len(instructions):
            break
        if state.pc > len(instructions):
            raise BadAddress(f'Bad address {pc} > {len(instructions)}')
        pc = state.pc
        i = instructions[state.pc]
        try:
            state = i.exec(state.pc, state.acc)
            print(f'{pc}: {i} -> {state}')
        except Exception as e:
            print(f'{pc}: {i} !!')
            raise e
    print('Terminated: ', state)
    return state


def mutate_program(instructions):
    print('~~~~ Mutating ~~~~')
    mutated_program = deepcopy(instructions)

    for i, instruction in enumerate(mutated_program):
        for e in mutated_program:
            e.exec_count = 0

        if instruction.mutate():
            print(f'{i}: ~~ {instruction} ~~')
            # Try running the mutated program.
            try:
                result = run(mutated_program)
            except ProgramException as e:
                # Restore state
                print(e)
                instruction.mutate()
                result = None
            if result is not None:
                break
    print('Done: ', result)


def tests():
    print('Tests\n-----\n')

    instructions = [Instruction(line) for line in TEST_INPUT]
    try:
        run(instructions)
    except DoubleExec as e:
        print(e)

    mutate_program(instructions)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        instructions = [Instruction(line) for line in input_file.readlines()]
    try:
        run(instructions)
    except DoubleExec as e:
        print(e)

    mutate_program(instructions)


if __name__ == '__main__':
    tests()
    print('')
    main()
