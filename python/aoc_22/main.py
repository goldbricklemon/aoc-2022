# -*- coding: utf-8 -*-

import numpy as np

PORTAL = 0
FREE = 1
WALL = 2

character_mapping = dict(zip([" ", ".", "#"], [PORTAL, FREE, WALL]))


def create_board_from_lines(lines):
    instruction_str = lines[-1]
    lines = lines[:-2]
    board_width = max([len(l) for l in lines])
    board_height = len(lines)

    board_input = np.zeros((board_height, board_width), dtype=np.int)
    board_input[:, :] = PORTAL
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            board_input[y, x] = character_mapping[character]

    print(board_input)


if __name__ == '__main__':
    with open("test_input.txt", "r") as f:
        lines = f.readlines()
    lines = [l.strip("\n").strip("\r") for l in lines]
    create_board_from_lines(lines)

