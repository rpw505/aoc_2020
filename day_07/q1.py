import re
import logging
from dataclasses import dataclass
from typing import Tuple, List

TEST_INPUT = [
    'light red bags contain 1 bright white bag, 2 muted yellow bags.',
    'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
    'bright white bags contain 1 shiny gold bag.',
    'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
    'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
    'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
    'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
    'faded blue bags contain no other bags.',
    'dotted black bags contain no other bags.',
]

TEST_INPUT_2 = [
    'shiny gold bags contain 2 dark red bags.',
    'dark red bags contain 2 dark orange bags.',
    'dark orange bags contain 2 dark yellow bags.',
    'dark yellow bags contain 2 dark green bags.',
    'dark green bags contain 2 dark blue bags.',
    'dark blue bags contain 2 dark violet bags.',
    'dark violet bags contain no other bags.',
]

@dataclass
class BagNode:
    colour: str
    children: dict

    def __hash__(self):
        return hash(self.colour)
    
    def __eq__(self, other):
        try:
            return other.colour == self.colour
        except:
            return False
    
    def __iter__(self):
        return self.children.__iter__()


def parse_input(line):
    m = re.match(r'(\w* \w*) bags contain ', line) 
    parent_colour = m.group(1)
    line = line[m.end():]
    children = {m.group(2): int(m.group(1)) for m in re.finditer(r'(\d*) (\w* \w*) bags?[,.] ?', line)}
    return BagNode(parent_colour, children)

def build_graph(lines):
    nodes = [parse_input(line) for line in lines]
    graph = {n.colour: n for n in nodes}
    return graph


def find_all_containers_of(colour, graph):
    containers = set()
    l = len(containers)

    # get direct holders
    for containing_bag, contents in graph.items():
        if colour in contents:
            containers.add(containing_bag)

    # Get holders of holders. Repeat until stop mutation.
    while l != len(containers):
        l = len(containers)
        # Not sure if we need to freeze list? Could optimise by finding dif in bags added.
        for bag_colour in list(containers):
            for containing_bag, contents in graph.items():
                if bag_colour in contents:
                    containers.add(containing_bag)
    return containers


def sum_contents(colour, graph):
    bag = graph[colour]
    # + 1 for the bag itself self
    results = sum(sum_contents(colour, graph) * quantity for colour, quantity in bag.children.items()) + 1
    return results


def tests():
    print('Tests\n-----\n')

    graph = build_graph(TEST_INPUT)
    result = find_all_containers_of('shiny gold', graph)
    print(result)

    graph = build_graph(TEST_INPUT_2)
    print('Number: ', sum_contents('shiny gold', graph) - 1)

def main():
    print('Main\n----\n')

    with open("input_1.txt", 'r') as input_file:
        graph = build_graph(input_file.readlines())
    result = find_all_containers_of('shiny gold', graph)
    print(result)
    print('Number of bags: ', len(result))

    print('Number: ', sum_contents('shiny gold', graph) - 1)

if __name__ == '__main__':
    tests()
    print('')
    main()
