# -*- coding: utf-8 -*-
"""
Created on 21 Dec 2022, 16:37

@author: einfalmo
"""

OPS = ["+", "-", "/", "*"]

def parse_line(line):
    line = line.strip("\n")
    name, rest = line[:4], line[6:]
    value, p1, p2, op = None, None, None, None
    for operation in OPS:
        if operation in rest:
            p1, p2 = rest[:4], rest[7:11]
            op = operation
            break
    else:
        value = int(rest)
    return name, value, p1, p2, op


class Node:

    def __init__(self, name):
        self.name = name
        self.value = None
        self.p1 = None
        self.p2 = None
        self.op = None
        self.deps = []
        self.has_run = False

    def run_node(self):
        if not self.has_run:
            if self.value is not None:
                self.has_run = True
                print(f"{self.name} yells {self.value}")
                self.run_deps()
            else:
                if self.p1.has_run and self.p2.has_run:
                    self._run_op()
                    self.has_run = True
                    print(f"{self.name} yells {self.p1.name} {self.op} {self.p2.name} = {self.value}")
                    self.run_deps()

    def _run_op(self):
        v1 = self.p1.value
        v2 = self.p2.value
        if self.op == "+":
            self.value = v1 + v2
        elif self.op == "-":
            self.value = v1 - v2
        elif self.op == "*":
            self.value = v1 * v2
        elif self.op == "/":
            self.value = v1 // v2
            print(self.value)

    def run_deps(self):
        for node in self.deps:
            node.run_node()


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()

    # Parse lines, create initial graph nodes
    parsed_lines = [parse_line(line) for line in lines]
    nodes = [Node(name=pl[0]) for pl in parsed_lines]
    node_dict = {node.name: node for node in nodes}

    # Link nodes
    for (name, value, p1, p2, op) in parsed_lines:
        node = node_dict[name]
        node.value = value
        if p1 is not None:
            p1_node = node_dict[p1]
            node.p1 = p1_node
            p1_node.deps.append(node)
        if p2 is not None:
            p2_node = node_dict[p2]
            node.p2 = p2_node
            p2_node.deps.append(node)
        node.op = op

    for node in nodes:
        if node.value is not None and not node.has_run:
            node.run_node()

    print(f"ROOT: {node_dict['root'].value}")





