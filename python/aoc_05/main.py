# -*- coding: utf-8 -*-
import copy


def parse_input(lines):
    # 1. Figure out how many stacks exist
    num_stacks = 0
    for l_i, line in enumerate(lines):
        if len(line) > 1 and line[1].isdigit():
            numbers = [int(num) for num in  line.split(' ') if num.isdigit()]
            num_stacks = max(numbers)
            break

    # 2. Parse initial stacks
    stacks = [list() for _ in range(num_stacks)]
    for line in reversed(lines[:l_i]):
        for s_i in range(num_stacks):
            position = 1 + s_i * 4
            if len(line) > position:
                crate = line[position]
                if crate.isalpha():
                    stacks[s_i].append(crate)
            else:
                break

    # 3. Parse crane operations
    operations = []
    for line in lines[l_i + 2:]:
        line = line.lstrip("move ")
        a, line = line.split(" from ")
        b, c = line.split(" to ")
        operations.append(tuple(int(num) for num in [a, b, c]))

    return stacks, operations


def operate_crane_9000(stacks, operation):
    num, src_i, dst_i = operation
    src, dst = [stacks[i - 1] for i in [src_i, dst_i]]
    for i in range(num):
        crate = src.pop()
        dst.append(crate)
    return stacks


def operate_crane_9001(stacks, operation):
    num, src_i, dst_i = operation
    src, dst = [stacks[i - 1] for i in [src_i, dst_i]]
    buffer = []
    for i in range(num):
        crate = src.pop()
        buffer.append(crate)
    dst.extend(reversed(buffer))
    return stacks


def print_top_crates(stacks):
    top_crates = map(lambda stack: stack[-1], stacks)
    message = "".join(top_crates)
    print(f"Top crates: {message}")


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    stacks, operations = parse_input(lines)
    stacks_copy = copy.deepcopy(stacks)
    operations_copy = copy.deepcopy(operations)

    print("#### Star one ####")
    for op in operations:
        operate_crane_9000(stacks=stacks, operation=op)
    print_top_crates(stacks)

    print("#### Star two ####")
    for op in operations_copy:
        operate_crane_9001(stacks=stacks_copy, operation=op)
    print_top_crates(stacks_copy)
