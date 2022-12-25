# -*- coding: utf-8 -*-
import numpy as np

def read_input(lines):
    tree_rows = list(map(lambda l: np.array([int(c) for c in l]), lines))
    return np.stack(tree_rows, axis=0)


if __name__ == '__main__':
    with open("test_input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]

    trees = read_input(lines)
    print(trees)

    print("#### Star one ####")

    print("#### Star two ####")
