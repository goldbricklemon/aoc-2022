# -*- coding: utf-8 -*-

OPS = ["+", "-", "/", "*"]
UNK = "UKNOWN"


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
                # print(f"{self.name} yells {self.value}")
                self.run_deps()
            else:
                if self.p1.has_run and self.p2.has_run:
                    self._run_op()
                    self.has_run = True
                    # print(f"{self.name} yells {self.p1.name} {self.op} {self.p2.name} = {self.value}")
                    self.run_deps()

    def _run_op(self):
        v1 = self.p1.value
        v2 = self.p2.value

        if self.op == "=":
            # Root node with equals check
            unk_node, target_value = self.p1, v2
            if v2 == UNK:
                unk_node, target_value = self.p2, v1
            print("Starting UNK value backtracking")
            unk_node.backtrack_unknown_value(target_value)

        elif v1 == UNK or v2 == UNK:
            self.value = UNK
        elif self.op == "+":
            self.value = v1 + v2
        elif self.op == "-":
            self.value = v1 - v2
        elif self.op == "*":
            self.value = v1 * v2
        elif self.op == "/":
            self.value = v1 // v2

    def run_deps(self):
        for node in self.deps:
            node.run_node()

    def backtrack_unknown_value(self, target_value):
        if self.p1 is None and self.p2 is None:
            # End of backtracking
            self.value = target_value
            print(f"End of backtracking at node {self.name}: Required value {self.value}")
        else:
            v1, v2 = self.p1.value, self.p2.value
            next_target_value = None
            next_backtrack_node = self.p1 if v1 == UNK else self.p2
            if self.op == "+":
                if v1 == UNK:
                    next_target_value = target_value - v2
                else:
                    next_target_value = target_value - v1
            elif self.op == "-":
                if v1 == UNK:
                    next_target_value = target_value + v2
                else:
                    next_target_value = v1 - target_value
            elif self.op == "*":
                if v1 == UNK:
                    next_target_value = target_value // v2
                else:
                    next_target_value = target_value // v1
            elif self.op == "/":
                if v1 == UNK:
                    next_target_value = target_value * v2
                else:
                    next_target_value = v1 / target_value
            next_backtrack_node.backtrack_unknown_value(next_target_value)


def create_nodes_from_lines(lines):
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
    return nodes, node_dict


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        lines = f.readlines()

    print("#### Star one ####")
    nodes, node_dict = create_nodes_from_lines(lines)

    for node in nodes:
        if node.value is not None and not node.has_run:
            node.run_node()

    print(f"ROOT: {node_dict['root'].value}")

    print("#### Star two ####")
    nodes, node_dict = create_nodes_from_lines(lines)

    node_dict["root"].op = "="
    node_dict["humn"].value = UNK

    for node in nodes:
        if node.value is not None and not node.has_run:
            node.run_node()
